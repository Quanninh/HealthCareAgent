"""Universal LLM API client and helper functions for stateless clinical case extraction.

Supports any official or custom LLM API provider, including:
- DeepSeek (deepseek-chat, deepseek-reasoner)
- OpenAI (gpt-4o, gpt-4-turbo, o1, o3-mini)
- OpenRouter (openrouter.ai/api/v1)
- Groq, Together AI, Mistral, Perplexity, Anthropic
- Local / self-hosted models (Ollama, vLLM, LocalAI, LM Studio)

Uses Python standard library (urllib.request) only—no third-party dependencies.
"""

import datetime
import json
import os
from pathlib import Path
import re
import socket
import sys
import time
import urllib.error
import urllib.request
from typing import Any, Dict, List, Optional, Union

from config import (
    API_BASE,
    API_KEY,
    API_MODEL,
    MAX_RETRIES,
    REASONING_LOG_DIR,
    RETRY_BACKOFF_SEC,
    TIMEOUT_SEC,
)


# ==========================================
# EXCEPTION HIERARCHY
# ==========================================

class LLMAPIError(Exception):
    """Base exception for all LLM API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_body: Optional[str] = None,
    ):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body


class LLMAuthError(LLMAPIError):
    """Raised for HTTP 401/403 authentication or authorization failures."""
    pass


class LLMBadRequestError(LLMAPIError):
    """Raised for HTTP 400 invalid request."""
    pass


class LLMRateLimitError(LLMAPIError):
    """Raised for HTTP 429 rate limit exceeded or quota exhausted."""
    pass


class LLMServerError(LLMAPIError):
    """Raised for HTTP 500-series server errors."""
    pass


class LLMTimeoutError(LLMAPIError):
    """Raised for network connection or read timeouts."""
    pass


class LLMMalformedResponseError(LLMAPIError):
    """Raised when the API returns malformed JSON or unexpected response structure."""
    pass


# Backwards compatibility aliases
DeepSeekAPIError = LLMAPIError
DeepSeekAuthError = LLMAuthError
DeepSeekBadRequestError = LLMBadRequestError
DeepSeekRateLimitError = LLMRateLimitError
DeepSeekServerError = LLMServerError
DeepSeekTimeoutError = LLMTimeoutError
DeepSeekMalformedResponseError = LLMMalformedResponseError


# ==========================================
# REQUEST BUILDER (STATELESS, MULTI-PROVIDER)
# ==========================================

def resolve_endpoint_url(api_base: str) -> str:
    """Normalize base URL and compute the correct completion endpoint."""
    cleaned = api_base.strip().rstrip("/")
    if (
        cleaned.endswith("/chat/completions")
        or cleaned.endswith("/v1/messages")
        or cleaned.endswith("/api/chat")
        or cleaned.endswith("/api/generate")
    ):
        return cleaned
    if "anthropic.com" in cleaned:
        return f"{cleaned}/v1/messages"
    return f"{cleaned}/chat/completions"


def build_chat_completion_request(
    prompt: str,
    api_key: Optional[str] = None,
    api_base: str = API_BASE,
    model: str = API_MODEL,
    temperature: Optional[float] = None,
    system_prompt: Optional[str] = None,
    max_tokens: Optional[int] = None,
    num_ctx: Optional[int] = None,
) -> urllib.request.Request:
    """Construct a stateless HTTP POST request compatible with any LLM provider.

    Stateless guarantee:
    - 1 API call = 1 case.
    - Optional fixed system prompt + exactly ONE user message for this case.
    - No previous history, no session ID, no conversation tracking.
    """
    key = (api_key or "").strip()
    is_local = "localhost" in api_base or "127.0.0.1" in api_base

    if not key and not is_local:
        raise LLMAuthError(
            "API key is not set or empty. Please set API_KEY, OPENAI_API_KEY, "
            "DEEPSEEK_API_KEY, or LLM_API_KEY."
        )

    endpoint = resolve_endpoint_url(api_base)
    is_anthropic = "anthropic.com" in endpoint

    if is_anthropic:
        headers = {
            "Content-Type": "application/json",
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "User-Agent": "DeepSeek-Extraction-Pipeline/1.0",
        }
        payload: Dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens or 4096,
            "messages": [
                {"role": "user", "content": prompt}
            ],
        }
        if system_prompt:
            payload["system"] = system_prompt
        if temperature is not None:
            payload["temperature"] = temperature
    else:
        # OpenAI, DeepSeek, OpenRouter, Groq, Together, Mistral, Ollama, vLLM
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Khai-LLM-Extraction-Pipeline/1.0",
        }
        if key:
            headers["Authorization"] = f"Bearer {key}"

        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model,
            "messages": messages,
            "stream": False,
        }
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        if num_ctx is not None:
            options: Dict[str, Any] = {"num_ctx": num_ctx}
            if temperature is not None:
                options["temperature"] = temperature
            if max_tokens is not None:
                options["num_predict"] = max_tokens
            payload["options"] = options

    body_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    return urllib.request.Request(
        url=endpoint,
        data=body_bytes,
        headers=headers,
        method="POST",
    )


# ==========================================
# RESPONSE PARSER & REASONING AUDIT LOGGING
# ==========================================

def log_internal_reasoning(
    reasoning: str,
    case_id: Optional[str] = None,
    log_dir: Optional[Path] = None,
) -> Optional[Path]:
    """Save model's internal reasoning (e.g. from gpt-oss-120b, DeepSeek-R1) into logs_internal_reasoning for audit."""
    if not reasoning or not reasoning.strip():
        return None

    target_dir = log_dir or REASONING_LOG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)

    if case_id:
        safe_id = re.sub(r"[^\w\-_\.]", "_", case_id)
        file_path = target_dir / f"{safe_id}.txt"
    else:
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        file_path = target_dir / f"reasoning_{timestamp}.txt"

    file_path.write_text(reasoning.strip() + "\n", encoding="utf-8")
    return file_path


def parse_chat_completion_response(
    response_bytes: bytes,
    case_id: Optional[str] = None,
    log_reasoning: bool = True,
    log_dir: Optional[Path] = None,
) -> str:
    """Parse API response from any LLM provider and extract generated text.

    Supports:
    - OpenAI format (`choices[0].message.content`)
    - DeepSeek-R1 / gpt-oss-120b Reasoning (`choices[0].message.reasoning_content` or `reasoning`)
    - Anthropic format (`content[0].text`)
    - Ollama format (`response` or `message.content`)
    - Legacy completions (`choices[0].text`)
    - Audit logging of internal reasoning to `logs_internal_reasoning`
    """
    try:
        data = json.loads(response_bytes.decode("utf-8"))
    except Exception as e:
        raise LLMMalformedResponseError(f"Malformed JSON response from API: {e}")

    content_str = ""
    reasoning_str = ""

    # 1. Standard OpenAI & DeepSeek format
    if "choices" in data:
        choices = data.get("choices")
        if not isinstance(choices, list) or len(choices) == 0:
            raise LLMMalformedResponseError("Malformed API response: 'choices' is empty or missing")

        first_choice = choices[0]
        if isinstance(first_choice, dict):
            # Message-based (Chat completion)
            if "message" in first_choice and isinstance(first_choice["message"], dict):
                msg = first_choice["message"]
                raw_content = msg.get("content")
                if isinstance(raw_content, str):
                    content_str = raw_content
                elif isinstance(raw_content, list):
                    # Multimodal/block text list
                    parts = [
                        block.get("text", "")
                        for block in raw_content
                        if isinstance(block, dict) and block.get("type") == "text"
                    ]
                    content_str = "".join(parts)

                raw_reasoning = (
                    msg.get("reasoning_content")
                    or msg.get("reasoning")
                    or msg.get("thinking")
                )
                if isinstance(raw_reasoning, str):
                    reasoning_str = raw_reasoning
            # Text-based (legacy completion)
            elif "text" in first_choice and isinstance(first_choice["text"], str):
                content_str = first_choice["text"]

            if not reasoning_str and isinstance(first_choice.get("reasoning"), str):
                reasoning_str = first_choice["reasoning"]

    # 2. Anthropic Messages API format
    elif "content" in data and isinstance(data["content"], list):
        text_parts = [
            block.get("text", "")
            for block in data["content"]
            if isinstance(block, dict) and block.get("type") == "text"
        ]
        content_str = "".join(text_parts)

    # 3. Ollama direct format (/api/chat -> message.content, /api/generate -> response)
    elif "message" in data and isinstance(data["message"], dict):
        raw_content = data["message"].get("content")
        if isinstance(raw_content, str):
            content_str = raw_content
        raw_reasoning = (
            data["message"].get("reasoning_content")
            or data["message"].get("reasoning")
            or data["message"].get("thinking")
        )
        if isinstance(raw_reasoning, str):
            reasoning_str = raw_reasoning
    elif "response" in data and isinstance(data["response"], str):
        content_str = data["response"]

    # Check if internal reasoning is embedded inside <think> tags within content (e.g. from gpt-oss-120b or DeepSeek)
    if "<think>" in content_str and "</think>" in content_str:
        think_match = re.search(r"<think>(.*?)</think>", content_str, re.DOTALL)
        if think_match:
            embedded_reasoning = think_match.group(1).strip()
            if not reasoning_str:
                reasoning_str = embedded_reasoning
            # Strip internal <think> tags from content so they do not pollute the case output
            content_str = re.sub(r"<think>.*?</think>\s*", "", content_str, flags=re.DOTALL).strip()

    # Validate extracted text
    if not content_str.strip():
        raise LLMMalformedResponseError("LLM API returned empty or missing response content.")

    # Audit log internal reasoning if present (strictly logged only; never injected into <case_analysis>)
    if reasoning_str.strip() and log_reasoning:
        log_internal_reasoning(
            reasoning=reasoning_str,
            case_id=case_id,
            log_dir=log_dir,
        )

    return content_str


def parse_api_error(status_code: int, error_body_bytes: bytes) -> LLMAPIError:
    """Construct a typed exception from HTTP status code and response body across providers."""
    body_str = error_body_bytes.decode("utf-8", errors="replace")
    msg = f"HTTP {status_code}"

    try:
        err_json = json.loads(body_str)
        if isinstance(err_json, dict):
            # OpenAI / DeepSeek format: {"error": {"message": ...}}
            if "error" in err_json:
                err_val = err_json["error"]
                if isinstance(err_val, dict) and "message" in err_val:
                    msg = f"HTTP {status_code}: {err_val['message']}"
                elif isinstance(err_val, str):
                    msg = f"HTTP {status_code}: {err_val}"
            # FastAPI / vLLM format: {"detail": ...}
            elif "detail" in err_json:
                msg = f"HTTP {status_code}: {err_json['detail']}"
            # Generic message format: {"message": ...}
            elif "message" in err_json:
                msg = f"HTTP {status_code}: {err_json['message']}"
    except Exception:
        if body_str.strip():
            msg = f"HTTP {status_code}: {body_str[:200]}"

    if status_code == 400:
        return LLMBadRequestError(msg, status_code=status_code, response_body=body_str)
    elif status_code in (401, 403):
        return LLMAuthError(msg, status_code=status_code, response_body=body_str)
    elif status_code == 429:
        return LLMRateLimitError(msg, status_code=status_code, response_body=body_str)
    elif status_code >= 500:
        return LLMServerError(msg, status_code=status_code, response_body=body_str)
    else:
        return LLMAPIError(msg, status_code=status_code, response_body=body_str)


# ==========================================
# CORE EXECUTION
# ==========================================

def execute_api_call(
    request: urllib.request.Request,
    timeout: float = 120.0,
    case_id: Optional[str] = None,
    log_reasoning: bool = True,
    log_dir: Optional[Path] = None,
) -> str:
    """Execute the HTTP request with urllib and return the extracted reply string."""
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            resp_bytes = response.read()
            return parse_chat_completion_response(
                resp_bytes,
                case_id=case_id,
                log_reasoning=log_reasoning,
                log_dir=log_dir,
            )
    except urllib.error.HTTPError as e:
        error_bytes = e.read()
        e.close()
        raise parse_api_error(e.code, error_bytes) from e
    except (socket.timeout, TimeoutError) as e:
        raise LLMTimeoutError(f"Request timed out after {timeout}s: {e}") from e
    except urllib.error.URLError as e:
        if isinstance(e.reason, (socket.timeout, TimeoutError)):
            raise LLMTimeoutError(f"Request timed out after {timeout}s: {e.reason}") from e
        raise LLMAPIError(f"Network/Connection error: {e.reason}") from e


# ==========================================
# HIGH-LEVEL DRIVER (WITH RETRIES)
# ==========================================

def resolve_api_credentials(
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
) -> tuple[str, str, str]:
    """Resolve API key, base URL, and model from arguments or environment variables."""
    resolved_key = (
        api_key
        or os.environ.get("API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or API_KEY
    ).strip()

    resolved_base = (
        api_base
        or os.environ.get("API_BASE")
        or os.environ.get("OPENAI_BASE_URL")
        or API_BASE
    ).strip().rstrip("/")

    resolved_model = (
        model
        or os.environ.get("MODEL")
        or os.environ.get("OPENAI_MODEL")
        or API_MODEL
    ).strip()

    return resolved_key, resolved_base, resolved_model


def query_llm_api(
    prompt: str,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    model: Optional[str] = None,
    timeout: float = TIMEOUT_SEC,
    max_retries: int = MAX_RETRIES,
    retry_backoff: float = RETRY_BACKOFF_SEC,
    temperature: Optional[float] = None,
    case_id: Optional[str] = None,
    log_reasoning: bool = True,
    log_dir: Optional[Path] = None,
    system_prompt: Optional[str] = None,
    max_tokens: Optional[int] = None,
    num_ctx: Optional[int] = None,
) -> str:
    """High-level function to send a stateless case extraction request to any LLM API.

    Retries with exponential backoff on transient errors (429, 5xx, timeouts).
    Client/Auth errors (400, 401, 403) are never retried.
    Logs internal reasoning to logs_internal_reasoning for models like gpt-oss-120b.
    """
    resolved_key, resolved_base, resolved_model = resolve_api_credentials(
        api_key=api_key,
        api_base=api_base,
        model=model,
    )

    is_local = "localhost" in resolved_base or "127.0.0.1" in resolved_base
    if not resolved_key and not is_local:
        raise LLMAuthError(
            "API key is not set. Please export API_KEY or OPENAI_API_KEY in your environment, or pass api_key."
        )

    last_error: Optional[Exception] = None

    for attempt in range(max_retries + 1):
        try:
            req = build_chat_completion_request(
                prompt=prompt,
                api_key=resolved_key,
                api_base=resolved_base,
                model=resolved_model,
                temperature=temperature,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                num_ctx=num_ctx,
            )
            return execute_api_call(
                req,
                timeout=timeout,
                case_id=case_id,
                log_reasoning=log_reasoning,
                log_dir=log_dir,
            )
        except (LLMAuthError, LLMBadRequestError) as e:
            # Client and authentication errors are permanent; do NOT retry.
            raise e
        except (LLMRateLimitError, LLMServerError, LLMTimeoutError, LLMAPIError) as e:
            last_error = e
            if attempt < max_retries:
                sleep_time = retry_backoff * (2 ** attempt)
                sys.stderr.write(
                    f"\n[WARN] API call attempt {attempt + 1}/{max_retries + 1} failed: {e}. "
                    f"Retrying in {sleep_time:.1f}s...\n"
                )
                time.sleep(sleep_time)
            else:
                break

    if last_error:
        raise last_error
    raise LLMAPIError("Unknown error occurred during API call")


# Backward compatibility alias
query_deepseek_api = query_llm_api


# ==========================================
# STANDALONE CLI TEST RUNNER
# ==========================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 api_helpers.py <command> [args]")
        print("Commands:")
        print("  test-config           : Validate API configuration and environment variables (offline, 0 credits)")
        print("  test-request [prompt] : Construct a mock request payload and inspect it (offline, 0 credits)")
        print("  smoke-test            : LIVE API smoke test (1 request, OPT-IN, consumes API credits)")
        sys.exit(0)

    cmd = sys.argv[1].lower()

    if cmd == "test-config":
        key, base, model = resolve_api_credentials()
        masked_key = (key[:4] + "..." + key[-4:]) if len(key) >= 8 else ("SET" if key else "NOT SET")
        print("=" * 60)
        print(" Universal LLM API Configuration Check")
        print("=" * 60)
        print(f" API Base URL:  {base}")
        print(f" Endpoint:      {resolve_endpoint_url(base)}")
        print(f" Target Model:  {model}")
        print(f" Resolved Key:  {masked_key}")
        print(f" Max Retries:   {MAX_RETRIES}")
        print(f" Retry Backoff: {RETRY_BACKOFF_SEC}s")
        print(f" Timeout:       {TIMEOUT_SEC}s")
        print("=" * 60)
        print(" Configuration check complete (0 API credits used).")

    elif cmd == "test-request":
        prompt_text = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else "Test extraction prompt"
        key, base, model = resolve_api_credentials()
        test_key = key if key else "sk-test-mock-key-12345"
        req = build_chat_completion_request(prompt_text, api_key=test_key, api_base=base, model=model)
        print("=" * 60)
        print(" Mock Request Construction Inspection")
        print("=" * 60)
        print(f" Target URL: {req.full_url}")
        print(f" Method:     {req.get_method()}")
        print(f" Headers:    Content-Type={req.headers.get('Content-type')}, Auth=Bearer {test_key[:4]}...")
        print(" Payload JSON:")
        print(json.dumps(json.loads(req.data.decode("utf-8")), indent=2))
        print("=" * 60)
        print(" Request construction verified (0 API credits used).")

    elif cmd == "smoke-test":
        key, base, model = resolve_api_credentials()
        endpoint = resolve_endpoint_url(base)
        print("=" * 65)
        print(" ⚠️  WARNING: LIVE LLM API SMOKE TEST (CONSUMES REAL CREDITS)")
        print("=" * 65)
        print("This command makes a REAL call to the configured API using your API key.")
        print("It will send exactly 1 minimal test prompt ('Please reply with: PONG').")
        print(f"Endpoint: {endpoint}")
        print(f"Model:    {model}")
        print("Max retries is set to 0 to prevent unnecessary charges.")
        print("=" * 65)
        confirm = input("Type 'yes' to proceed with the live test (or anything else to abort): ").strip().lower()
        if confirm != "yes":
            print("Aborted. No API calls were made.")
            sys.exit(0)
        print("\nSending live test request...")
        try:
            resp = query_llm_api("Please reply with: PONG", max_retries=0)
            print("SUCCESS! API replied:")
            print(resp)
        except Exception as e:
            print(f"FAILED: {e}")
            sys.exit(1)

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

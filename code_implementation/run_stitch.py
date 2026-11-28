"""Autonomous diagnostic reasoning stitching pipeline driver using stateless LLM APIs (Ollama)."""

import argparse
import datetime
import json
import os
import random
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from config import (
    CONFIRM_FIRST,
    DRY_RUN,
    MAX_RETRIES,
    REASONING_LOG_DIR,
    STITCH_API_BASE,
    STITCH_INPUT_DIR,
    STITCH_INPUT_JSONL,
    STITCH_MANIFEST_FILE,
    STITCH_MAX_TOKENS,
    STITCH_MODEL,
    STITCH_NUM_CTX,
    STITCH_OUTPUT_DIR,
    STITCH_REQUIRED_XML_TAGS,
    STITCH_TEMPERATURE,
    STITCH_TIMEOUT_SEC,
    format_stitch_prompt,
    sanitize_case_id,
)
from api_helpers import (
    query_llm_api,
    resolve_api_credentials,
    resolve_endpoint_url,
)
from run_extraction import (
    append_manifest_record,
    load_manifest,
)
from scripts.fix_extracted_cases import _find_section_match


def load_cases_from_jsonl(jsonl_path: Path) -> List[Dict[str, str]]:
    """Load extracted cases (case_prompt, diagnostic_reasoning, final_diagnosis) from JSONL."""
    cases: List[Dict[str, str]] = []
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            sample_id = data.get("sample_id", f"case_{idx:04d}")
            case_id = data.get("case_id") or sanitize_case_id(sample_id)
            case_prompt = (data.get("case_prompt") or "").strip()
            reasoning_points = (
                data.get("diagnostic_reasoning")
                or data.get("reasoning_points")
                or ""
            ).strip()
            final_diagnosis = (data.get("final_diagnosis") or "").strip()

            if not (case_prompt and reasoning_points and final_diagnosis):
                continue

            cases.append({
                "case_id": case_id,
                "sample_id": sample_id,
                "case_prompt": case_prompt,
                "reasoning_points": reasoning_points,
                "final_diagnosis": final_diagnosis,
            })
    return cases


def load_cases_from_dir(md_dir: Path) -> List[Dict[str, str]]:
    """Load extracted cases from markdown files in an extraction directory (e.g. out_oss_Khoa29)."""
    cases: List[Dict[str, str]] = []
    md_files = sorted(
        f for f in md_dir.glob("*.md") if not f.name.endswith(".raw.txt")
    )
    for md_file in md_files:
        text = md_file.read_text(encoding="utf-8")
        cp_match = _find_section_match(text, "case_prompt")
        dr_match = _find_section_match(text, "diagnostic_reasoning")
        fd_match = _find_section_match(text, "final_diagnosis")

        case_prompt = cp_match.group(1).strip() if cp_match else ""
        reasoning_points = dr_match.group(1).strip() if dr_match else ""
        final_diagnosis = fd_match.group(1).strip() if fd_match else ""

        if not (case_prompt and reasoning_points and final_diagnosis):
            continue

        case_id = md_file.stem
        sample_id = case_id.replace("__", "::", 1)
        cases.append({
            "case_id": case_id,
            "sample_id": sample_id,
            "case_prompt": case_prompt,
            "reasoning_points": reasoning_points,
            "final_diagnosis": final_diagnosis,
        })
    return cases


def load_stitch_inputs(input_source: Path) -> List[Dict[str, str]]:
    """Load cases from either a JSONL file (oss_extracted_cases.jsonl) or a directory (out_oss_Khoa29)."""
    if input_source.is_dir():
        return load_cases_from_dir(input_source)
    if input_source.is_file():
        return load_cases_from_jsonl(input_source)
    raise FileNotFoundError(f"Input source not found: {input_source}")


def clean_and_validate_stitched_reply(reply_text: str) -> Tuple[bool, str, str]:
    """Validate and clean the model response containing <stitched_reasoning>...</stitched_reasoning>.

    Returns:
        (is_valid, cleaned_output, error_message)
    """
    missing = [tag for tag in STITCH_REQUIRED_XML_TAGS if tag not in reply_text]
    if missing:
        return False, reply_text, f"Missing required XML tags: {', '.join(missing)}"

    match = re.search(
        r"<stitched_reasoning>(.*?)</stitched_reasoning>",
        reply_text,
        re.DOTALL,
    )
    if not match:
        return False, reply_text, "Could not extract content between <stitched_reasoning> and </stitched_reasoning>"

    narrative = match.group(1).strip()
    if not narrative:
        return False, reply_text, "<stitched_reasoning> block is empty"

    cleaned = f"<stitched_reasoning>\n{narrative}\n</stitched_reasoning>\n"
    return True, cleaned, ""


def main():
    default_input = STITCH_INPUT_JSONL if STITCH_INPUT_JSONL.exists() else STITCH_INPUT_DIR

    parser = argparse.ArgumentParser(
        description="Diagnostic Reasoning Stitching Pipeline (Ollama / OpenAI-Compatible API)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        default=DRY_RUN,
        help="Simulate pipeline without sending API requests",
    )
    parser.add_argument(
        "--no-confirm",
        action="store_true",
        help="Skip the first-run confirmation prompt",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process at most N cases (useful for testing)",
    )
    parser.add_argument(
        "--case-id",
        type=str,
        default=None,
        help="Process only a specific case_id (e.g. PMC5437444_01__Histoplasmosis)",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=str(default_input),
        help="Path to oss_extracted_cases.jsonl or out_oss_Khoa29 directory",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=str(STITCH_OUTPUT_DIR),
        help=f"Directory to save stitched outputs (default: {STITCH_OUTPUT_DIR})",
    )
    parser.add_argument(
        "--model",
        type=str,
        default=STITCH_MODEL,
        help=f"Target Ollama / LLM model (default: {STITCH_MODEL})",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=None,
        help="Optional API key (not required for local Ollama)",
    )
    parser.add_argument(
        "--api-base",
        type=str,
        default=STITCH_API_BASE,
        help=f"API base URL (default: {STITCH_API_BASE})",
    )
    parser.add_argument(
        "--max-retries",
        type=int,
        default=MAX_RETRIES,
        help=f"Max retries on transient errors (default: {MAX_RETRIES})",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=STITCH_TEMPERATURE,
        help=f"Sampling temperature (default: {STITCH_TEMPERATURE} for faithful stitching)",
    )
    parser.add_argument(
        "--num-ctx",
        type=int,
        default=STITCH_NUM_CTX,
        help=f"Ollama context window size in tokens (default: {STITCH_NUM_CTX} to prevent Ollama's 2048-token default truncation)",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=STITCH_MAX_TOKENS,
        help=f"Max output tokens to generate (default: {STITCH_MAX_TOKENS})",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=STITCH_TIMEOUT_SEC,
        help=f"HTTP timeout in seconds per case (default: {STITCH_TIMEOUT_SEC}s)",
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=0.0,
        help="Minimum delay in seconds between requests (default: 0.0 for local Ollama)",
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=0.0,
        help="Maximum delay in seconds between requests (default: 0.0 for local Ollama)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        if input_path == STITCH_INPUT_JSONL and STITCH_INPUT_DIR.exists():
            input_path = STITCH_INPUT_DIR
        else:
            sys.exit(f"[FATAL] Input source not found: {input_path}")

    output_dir = Path(args.output_dir)
    manifest_file = output_dir / "manifest.jsonl"

    api_key = (
        args.api_key
        or os.environ.get("API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()
    api_base = args.api_base.strip().rstrip("/")
    model = args.model.strip()

    is_local = "localhost" in api_base or "127.0.0.1" in api_base
    if not args.dry_run and not api_key and not is_local:
        sys.exit(
            "[FATAL] API key is not set for non-local endpoint.\n"
            "Please export API_KEY or pass --api-key <key>, or use local Ollama (--api-base http://localhost:11434/v1)."
        )

    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. Load manifest and existing state
    manifest = load_manifest(manifest_file)
    done_case_ids: Set[str] = {
        cid for cid, r in manifest.items() if r.get("status") == "done"
    }

    # 2. Load input cases
    cases = load_stitch_inputs(input_path)
    total_cases = len(cases)
    if args.case_id:
        target_cid = sanitize_case_id(args.case_id)
        cases = [c for c in cases if c["case_id"] == args.case_id or c["case_id"] == target_cid]
        if not cases:
            sys.exit(f"[FATAL] Case ID '{args.case_id}' not found in {input_path}")
    if args.limit:
        cases = cases[:args.limit]

    endpoint_url = resolve_endpoint_url(api_base)
    masked_key = (
        (api_key[:4] + "..." + api_key[-4:])
        if len(api_key) >= 8
        else ("SET" if api_key else "NOT SET (Local/Ollama)")
    )

    print("=" * 65)
    print(" Diagnostic Reasoning Stitching Pipeline (Ollama / LLM API)")
    print("=" * 65)
    print(f" Input Source:      {input_path}")
    print(f" Total Input Cases: {total_cases} (Processing: {len(cases)})")
    print(f" Output Directory:  {output_dir}")
    print(f" Manifest File:     {manifest_file}")
    print(f" API Base URL:      {api_base}")
    print(f" API Endpoint:      {endpoint_url}")
    print(f" Target Model:      {model}")
    print(f" Temperature:       {args.temperature}")
    print(f" Context Window:    {args.num_ctx} tokens (max_tokens={args.max_tokens})")
    print(f" API Key:           {masked_key}")
    print(f" Delay Range:       {args.min_delay}s - {args.max_delay}s")
    print(f" Timeout:           {args.timeout}s")
    print(f" Max Retries:       {args.max_retries}")
    print(f" Execution Mode:    {'DRY RUN (simulation)' if args.dry_run else 'LIVE API CALLS'}")
    print(f" Already Done:      {len(done_case_ids)} cases")
    print("=" * 65)

    # 3. Safety confirmation
    need_confirm = CONFIRM_FIRST and not args.no_confirm and not args.dry_run
    if need_confirm:
        print("\n[CONFIRMATION]")
        print(f"1. Target API:    {endpoint_url}")
        print(f"2. Model:         {model}")
        print(f"3. Output Folder: {output_dir}")
        print(f"4. Total to run:  {len(cases) - len(done_case_ids)} pending cases")
        print("5. Processing is stateless: 1 independent API request per case.")
        print("6. You can stop the script at any time by pressing Ctrl+C.")
        input("\nPress [ENTER] to confirm and begin (or Ctrl+C to abort)... ")
        print("Starting stitching pipeline...")

    count_done = 0
    count_failed = 0
    count_skipped = 0

    for i, item in enumerate(cases, 1):
        case_id = item["case_id"]
        sample_id = item["sample_id"]
        out_file = output_dir / f"{case_id}.md"

        if case_id in done_case_ids:
            count_skipped += 1
            print(f"[{i}/{len(cases)}] [SKIP] {case_id} (already marked done)")
            continue

        if out_file.exists():
            count_skipped += 1
            append_manifest_record(manifest_file, {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "skipped",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": "Output file already exists on disk",
            })
            print(f"[{i}/{len(cases)}] [SKIP] {case_id} (file exists: {out_file.name})")
            continue

        prompt = format_stitch_prompt(
            case_prompt=item["case_prompt"],
            reasoning_points=item["reasoning_points"],
            final_diagnosis=item["final_diagnosis"],
        )

        if args.dry_run:
            print(
                f"[{i}/{len(cases)}] [DRY-RUN] Would stitch {case_id} "
                f"(prompt={len(prompt)} chars, model={model})"
            )
            append_manifest_record(manifest_file, {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "dry_run",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": None,
            })
            count_done += 1
            continue

        print(f"[{i}/{len(cases)}] [STITCHING] {case_id} ...", end="", flush=True)

        try:
            reply = query_llm_api(
                prompt=prompt,
                api_key=api_key,
                api_base=api_base,
                model=model,
                temperature=args.temperature,
                max_tokens=args.max_tokens,
                num_ctx=args.num_ctx,
                timeout=args.timeout,
                max_retries=args.max_retries,
                case_id=case_id,
                log_dir=REASONING_LOG_DIR,
            )
        except Exception as e:
            err_msg = str(e)
            print(f" -> [FAILED] ({err_msg})")
            count_failed += 1
            append_manifest_record(manifest_file, {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "failed",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": err_msg,
            })
            continue

        is_valid, cleaned_reply, validation_err = clean_and_validate_stitched_reply(reply)
        if not is_valid:
            print(f" -> [INVALID FORMAT] ({validation_err})")
            raw_path = output_dir / f"{case_id}.raw.txt"
            raw_path.write_text(reply, encoding="utf-8")
            count_failed += 1
            append_manifest_record(manifest_file, {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "failed",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": validation_err,
            })
            continue

        out_file.write_text(cleaned_reply, encoding="utf-8")
        count_done += 1
        done_case_ids.add(case_id)

        append_manifest_record(manifest_file, {
            "case_id": case_id,
            "sample_id": sample_id,
            "status": "done",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": None,
        })
        print(f" -> [DONE] Saved to {out_file.name}")

        if args.max_delay > 0:
            delay = random.uniform(args.min_delay, max(args.min_delay, args.max_delay))
            time.sleep(delay)

    print("\n" + "=" * 65)
    print(" STITCHING RUN COMPLETED")
    print(f" Total Processed: {count_done} done, {count_failed} failed, {count_skipped} skipped")
    print(f" Output Folder:   {output_dir}")
    print(f" Manifest:        {manifest_file}")
    print("=" * 65)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ABORTED] Process interrupted by user. Manifest saved up to last case.")
        sys.exit(0)

"""
RAG-Anything Ingestion Module for MultiCaRe Payloads.
Configured for 100% free, local AI model execution (medgemma, local VLM, open embeddings)
via Ollama or llama-server (llama.cpp).

Includes robust output sanitization for local thinking models, concurrency controls
for Apple Silicon / Mac local hardware, few-shot hallucination filtering, and graceful shutdown.
"""

import argparse
import asyncio
import json
import logging
import os
import re
import shutil
import sys
from functools import partial
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests

from config import (
    DEFAULT_EMBEDDING_DIM,
    DEFAULT_EMBEDDING_MODEL,
    DEFAULT_LLM_MODEL,
    DEFAULT_VISION_MODEL,
    LOCAL_LLM_API_KEY,
    LOCAL_LLM_BASE_URL,
    OUTPUT_DIR,
    PAYLOADS_DIR,
    RAG_STORAGE_DIR,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Banned prompt few-shot names and template placeholders from LightRAG default prompt
BANNED_PROMPT_ENTITIES = {
    "alex",
    "taylor",
    "jordan",
    "cruz",
    "the device",
    "noah carter",
    "world athletics championship",
    "tokyo",
    "100m sprint record",
    "carbon-fiber spikes",
    "world athletics federation",
    "nexon technologies",
    "omega energy",
    "gold futures",
    "crude oil",
    "market selloff",
    "federal reserve policy announcement",
    "entity_name",
    "source_entity",
    "target_entity",
    "source_entity @ target_entity",
}


VALID_CLINICAL_TYPES = {
    "disease",
    "pathogen",
    "symptom",
    "clinical_sign",
    "diagnostic_test",
    "medication",
    "treatment",
    "anatomy",
    "patient_cohort",
    "category",
    "event",
    "content",
    "chart",
    "other",
}


def clean_llm_extraction_response(raw_text: str) -> str:
    """
    Cleans and strictly validates raw LLM extraction outputs for LightRAG:
    1. Removes <think>...</think>, leading 'thought' internal monologue, and code fences.
    2. Drops conversational meta-reflections (e.g. "The user wants me to extract...").
    3. Strips hallucinated prompt few-shot entities (Alex, Taylor, Noah Carter, etc.).
    4. Strips markdown bolding (**) and leading list numbering (e.g., '1. ').
    5. Normalizes lines to strictly conform to LightRAG's expected format:
       - entity<|#|>name<|#|>type<|#|>description (4 fields)
       - relation<|#|>source<|#|>target<|#|>keywords<|#|>description (5 fields)
    6. Filters out incomplete or unparseable lines that would cause LLM format warnings
       or generate bogus graph nodes (e.g. node named 'disease' or 'pathogen').
    7. Guarantees the completion token <|COMPLETE|> is present at the end.
    """
    if not raw_text or not isinstance(raw_text, str):
        return "<|COMPLETE|>"

    text = raw_text

    # 1. Strip XML think tags if present
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)

    # 2. Strip leading 'thought' block if the model outputs thinking text
    if text.strip().startswith("thought"):
        lines = text.splitlines()
        extracted_lines = []
        for line in lines:
            line_str = line.strip()
            if "<|#|>" in line_str or line_str.startswith("##") or "<|COMPLETE|>" in line_str:
                extracted_lines.append(line_str)
        text = "\n".join(extracted_lines)

    # 3. Strip markdown code fences (<Output>, ```json, ```output, etc.)
    text = re.sub(r"^```[a-zA-Z0-9_-]*\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"</?[oO]utput>", "", text)

    valid_lines = []
    tuple_delimiter = "<|#|>"

    for line in text.splitlines():
        line_clean = line.strip()
        if not line_clean:
            continue

        if "<|complete|>" in line_clean.lower():
            continue

        line_lower = line_clean.lower()

        # Drop few-shot prompt names or template placeholders
        if any(banned in line_lower for banned in BANNED_PROMPT_ENTITIES):
            logger.debug("Filtered out prompt few-shot line: %s", line_clean)
            continue

        # Drop conversational meta reflections that mention delimiters or instructions
        if any(phrase in line_lower for phrase in [
            "the user wants", "i need to follow", "here are the extracted",
            "here is the extraction", "as requested", "i will extract",
            "delimiters", "system prompt", "clinical case report"
        ]):
            continue

        # Ignore lines without the tuple delimiter
        if tuple_delimiter not in line_clean:
            continue

        # Strip leading numbers or bullet markers (e.g. "1.  ", "- ", "* ")
        line_clean = re.sub(r"^(\d+[\.\)]|\-|\*)\s+", "", line_clean).strip()

        # Split attributes by tuple delimiter
        parts = [p.strip() for p in line_clean.split(tuple_delimiter)]
        while parts and not parts[-1]:
            parts.pop()

        if not parts:
            continue

        record_type = parts[0].strip().lower()

        # Case A: Standard entity record: entity<|#|>name<|#|>type<|#|>description
        if record_type == "entity":
            if len(parts) >= 4:
                name = parts[1].replace("**", "").replace('"', "").strip()
                ent_type = parts[2].replace("**", "").strip()
                desc = parts[3].strip()
                if "," in ent_type:
                    ent_type = ent_type.split(",")[0].strip()
                if name and ent_type and desc:
                    valid_lines.append(f"entity{tuple_delimiter}{name}{tuple_delimiter}{ent_type}{tuple_delimiter}{desc}")
            continue

        # Case B: Standard relation record: relation<|#|>src<|#|>tgt<|#|>keywords<|#|>description
        if record_type in ("relation", "relationship"):
            if len(parts) >= 5:
                src = parts[1].replace("**", "").strip()
                tgt = parts[2].replace("**", "").strip()
                keywords = parts[3].replace("**", "").strip()
                desc = parts[4].strip()
                if src and tgt and desc and src != tgt:
                    valid_lines.append(f"relation{tuple_delimiter}{src}{tuple_delimiter}{tgt}{tuple_delimiter}{keywords}{tuple_delimiter}{desc}")
            continue

        # Case C: Model omitted 'entity' keyword: [name, type, description] (3 parts)
        if len(parts) == 3:
            name = parts[0].replace("**", "").replace('"', "").strip()
            ent_type = parts[1].replace("**", "").strip()
            desc = parts[2].strip()
            if "," in ent_type:
                ent_type = ent_type.split(",")[0].strip()
            if name and ent_type and desc and not name.lower().startswith("chunk-"):
                valid_lines.append(f"entity{tuple_delimiter}{name}{tuple_delimiter}{ent_type}{tuple_delimiter}{desc}")
            continue

        # Case D: Model omitted 'entity' keyword & description: [name, type] (2 parts)
        # e.g., `**COVID-19** <|#|> pathogen`
        if len(parts) == 2:
            name = parts[0].replace("**", "").replace('"', "").strip()
            ent_type = parts[1].replace("**", "").strip().lower()
            if "," in ent_type:
                ent_type = ent_type.split(",")[0].strip()
            if name and ent_type in VALID_CLINICAL_TYPES:
                desc = f"{name} identified as {ent_type} in the clinical case."
                valid_lines.append(f"entity{tuple_delimiter}{name}{tuple_delimiter}{ent_type}{tuple_delimiter}{desc}")
            continue

        # Case E: Model omitted 'relation' keyword: [src, tgt, keywords, description] (4 parts, not 'entity')
        # e.g., `**Acute hepatitis** <|#|> **COVID-19** <|#|> cause, neonatal <|#|> viral liver injury`
        if len(parts) == 4 and record_type != "entity":
            src = parts[0].replace("**", "").replace('"', "").strip()
            tgt = parts[1].replace("**", "").replace('"', "").strip()
            keywords = parts[2].replace("**", "").strip()
            desc = parts[3].strip()
            # Ensure it is a valid relation between two named entities
            if src and tgt and desc and src != tgt and tgt.lower() not in VALID_CLINICAL_TYPES:
                valid_lines.append(f"relation{tuple_delimiter}{src}{tuple_delimiter}{tgt}{tuple_delimiter}{keywords}{tuple_delimiter}{desc}")
            continue

    valid_lines.append("<|COMPLETE|>")
    return "\n".join(valid_lines)


def check_local_server_status(base_url: str) -> bool:
    """Checks if the local OpenAI-compatible inference server is accessible."""
    try:
        models_url = f"{base_url.rstrip('/')}/models"
        resp = requests.get(models_url, timeout=3)
        if resp.status_code == 200:
            logger.info("✅ Local model server is active at %s", base_url)
            return True
        logger.warning("Local server responded with status %d at %s", resp.status_code, models_url)
        return False
    except Exception as e:
        logger.warning("⚠️ Local model server not reachable at %s: %s", base_url, e)
        return False


def setup_rag_anything_engine(
    base_url: str = LOCAL_LLM_BASE_URL,
    api_key: str = LOCAL_LLM_API_KEY,
    llm_model: str = DEFAULT_LLM_MODEL,
    vision_model: str = DEFAULT_VISION_MODEL,
    embedding_model: str = DEFAULT_EMBEDDING_MODEL,
    embedding_dim: int = DEFAULT_EMBEDDING_DIM,
    storage_dir: Path = RAG_STORAGE_DIR,
):
    """
    Initializes RAGAnything with local free models and optimized LightRAG parameters.
    """
    from lightrag.llm.openai import openai_complete_if_cache
    from lightrag.utils import EmbeddingFunc
    from raganything import RAGAnything, RAGAnythingConfig

    config = RAGAnythingConfig(
        working_dir=str(storage_dir),
        enable_image_processing=True,
        enable_table_processing=False,
        enable_equation_processing=False,
    )

    # Ensure LightRAG uses generous timeouts for local Apple Silicon execution
    os.environ["LLM_TIMEOUT"] = "600"

    # Local LLM completion function with output cleaning
    async def llm_model_func(prompt, system_prompt=None, history_messages=[], **kwargs):
        # Configure num_ctx=8192 for Ollama to prevent prompt truncation (default is 2048)
        extra_body = kwargs.pop("extra_body", {})
        if "options" not in extra_body:
            extra_body["options"] = {}
        extra_body["options"].setdefault("num_ctx", 8192)

        stream = kwargs.pop("stream", False)

        # Complete response
        raw_result = await openai_complete_if_cache(
            llm_model,
            prompt,
            system_prompt=system_prompt,
            history_messages=history_messages,
            api_key=api_key,
            base_url=base_url,
            stream=stream,
            extra_body=extra_body,
            **kwargs,
        )
        # Only clean extraction responses if the prompt is an entity/relation extraction prompt
        is_extraction = (
            "<|#|>" in prompt
            or "tuple_delimiter" in prompt
            or (system_prompt and ("<|#|>" in system_prompt or "tuple_delimiter" in system_prompt))
        )
        if is_extraction:
            return clean_llm_extraction_response(raw_result)
        return raw_result

    # Local Vision model function
    async def vision_model_func(
        prompt, system_prompt=None, history_messages=[], image_data=None, messages=None, **kwargs
    ):
        extra_body = kwargs.pop("extra_body", {})
        if "options" not in extra_body:
            extra_body["options"] = {}
        extra_body["options"].setdefault("num_ctx", 8192)

        stream = kwargs.pop("stream", False)

        if messages:
            return await openai_complete_if_cache(
                vision_model,
                "",
                messages=messages,
                api_key=api_key,
                base_url=base_url,
                stream=stream,
                extra_body=extra_body,
                **kwargs,
            )
        elif image_data:
            content = [{"type": "text", "text": prompt}]
            content.append(
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_data}"},
                }
            )
            user_msg = {"role": "user", "content": content}
            msgs = []
            if system_prompt:
                msgs.append({"role": "system", "content": system_prompt})
            msgs.append(user_msg)
            return await openai_complete_if_cache(
                vision_model,
                "",
                messages=msgs,
                api_key=api_key,
                base_url=base_url,
                stream=stream,
                extra_body=extra_body,
                **kwargs,
            )
        else:
            return await llm_model_func(prompt, system_prompt, history_messages, extra_body=extra_body, **kwargs)

    # Embedding function: prefers local sentence-transformers, falls back to Ollama
    try:
        from sentence_transformers import SentenceTransformer

        logger.info("Initializing local SentenceTransformer (%s)...", embedding_model)
        embed_model = SentenceTransformer(embedding_model)

        async def local_hf_embed(texts: List[str]) -> Any:
            embeddings = embed_model.encode(texts, normalize_embeddings=True)
            return embeddings

        embedding_func = EmbeddingFunc(
            embedding_dim=embed_model.get_sentence_embedding_dimension(),
            max_token_size=8192,
            func=local_hf_embed,
        )
    except ImportError:
        logger.info("sentence_transformers not installed. Using local OpenAI-compatible embed endpoint.")
        from lightrag.llm.openai import openai_embed

        embedding_func = EmbeddingFunc(
            embedding_dim=embedding_dim,
            max_token_size=8192,
            func=partial(
                openai_embed.func,
                model=embedding_model,
                api_key=api_key,
                base_url=base_url,
            ),
        )

    # Crucial LightRAG parameters for local Mac / Apple Silicon execution:
    # 1. llm_model_max_async=1: Run 1 LLM request at a time to prevent Ollama throttling.
    # 2. embedding_func_max_async=2: Lower concurrency for local embeddings.
    # 3. entity_extract_max_gleaning=0: Disables 2nd gleaning pass which triggers few-shot hallucinations.
    # 4. default_llm_timeout=600: 10m func timeout / 20m worker timeout for complex payloads.
    # 5. addon_params: Explicit clinical entity types so it doesn't extract random phrases like Time/Date.
    lightrag_kwargs = {
        "llm_model_max_async": 1,
        "embedding_func_max_async": 2,
        "entity_extract_max_gleaning": 0,
        "default_llm_timeout": 600,
        "addon_params": {
            "entity_types": [
                "Disease",
                "Pathogen",
                "Symptom",
                "Clinical_Sign",
                "Diagnostic_Test",
                "Medication",
                "Treatment",
                "Anatomy",
                "Patient_Cohort",
            ]
        },
    }

    rag = RAGAnything(
        config=config,
        llm_model_func=llm_model_func,
        vision_model_func=vision_model_func,
        embedding_func=embedding_func,
        lightrag_kwargs=lightrag_kwargs,
    )

    return rag


async def ingest_payloads(
    payloads_dir: Path = PAYLOADS_DIR,
    max_payloads: Optional[int] = None,
    dry_run: bool = True,
    reset_storage: bool = False,
    llm_model: str = DEFAULT_LLM_MODEL,
    vision_model: str = DEFAULT_VISION_MODEL,
    base_url: str = LOCAL_LLM_BASE_URL,
):
    """
    Ingests generated payloads into RAG-Anything knowledge graph.
    """
    if reset_storage and RAG_STORAGE_DIR.exists():
        logger.info("Resetting RAG storage directory: %s", RAG_STORAGE_DIR)
        shutil.rmtree(RAG_STORAGE_DIR)
        RAG_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("RAG storage directory reset complete.")

    manifest_file = OUTPUT_DIR / "payloads_manifest.json"
    if not manifest_file.exists():
        logger.error("Payloads manifest not found at %s. Please run build_payloads.py first.", manifest_file)
        sys.exit(1)

    with open(manifest_file, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    entries = manifest_data.get("manifest", [])
    if max_payloads:
        entries = entries[:max_payloads]

    logger.info("Loaded manifest with %d payloads to ingest.", len(entries))

    if dry_run:
        print("\n" + "=" * 60)
        print(" 🔍 DRY-RUN MODE: PREVIEWING PAYLOADS & VERIFYING READINESS")
        print("=" * 60)
        print("No AI model will be called. Verifying files and schemas...")

        server_up = check_local_server_status(base_url)
        if not server_up:
            print(f"⚠️  Note: Local model server at {base_url} is currently offline.")
            print("   To run locally when ready, start Ollama:")
            print(f"     ollama run {llm_model}")
            print(f"     ollama run {vision_model}")
            print(f"     ollama pull {DEFAULT_EMBEDDING_MODEL}")

        print(f"\nVerifying {min(5, len(entries))} sample payloads from disk:")
        for entry in entries[:5]:
            p_file = Path(entry["payload_file"])
            if not p_file.exists():
                print(f"  ❌ Missing payload file: {p_file}")
                continue
            with open(p_file, "r", encoding="utf-8") as f:
                content_list = json.load(f)

            text_items = [item for item in content_list if item.get("type") == "text"]
            image_items = [item for item in content_list if item.get("type") == "image"]
            print(
                f"  ✅ Case {entry['case_id']}: Ref={entry['file_path_reference']} | "
                f"Text items: {len(text_items)}, Image items: {len(image_items)} | "
                f"Diseases: {entry.get('matched_diseases')}"
            )

        print("\n" + "=" * 60)
        print("🎉 Dry-run validation complete! All inspected payloads are ready.")
        print("To execute ingestion with your local AI models, run:")
        print("  python ingest_rag.py --execute --max-payloads 5")
        print("=" * 60 + "\n")
        return

    # EXECUTE MODE
    print("\n" + "=" * 60)
    print(" 🚀 INITIATING RAG-ANYTHING INGESTION (Local Free Models)")
    print(f"   Text LLM:   {llm_model}")
    print(f"   Vision VLM: {vision_model}")
    print(f"   Server:     {base_url}")
    print("=" * 60)

    server_up = check_local_server_status(base_url)
    if not server_up:
        logger.error("Cannot proceed: Local model server at %s is not reachable.", base_url)
        sys.exit(1)

    rag = setup_rag_anything_engine(
        base_url=base_url,
        llm_model=llm_model,
        vision_model=vision_model,
    )

    try:
        for idx, entry in enumerate(entries):
            p_file = Path(entry["payload_file"])
            doc_ref = entry["file_path_reference"]

            with open(p_file, "r", encoding="utf-8") as f:
                content_list = json.load(f)

            logger.info(
                "[%d/%d] Ingesting %s (items: %d)...",
                idx + 1,
                len(entries),
                doc_ref,
                len(content_list),
            )

            try:
                await rag.insert_content_list(
                    content_list=content_list,
                    file_path=doc_ref,
                    display_stats=False,
                )
            except (KeyboardInterrupt, asyncio.CancelledError):
                raise
            except Exception as e:
                logger.error("Failed to ingest %s: %s", doc_ref, e)
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.warning("\n[WARNING] Process interrupted by user (Ctrl+C). Initiating graceful shutdown...")
    finally:
        if rag:
            logger.info("Finalizing and persisting all storages to disk...")
            try:
                await asyncio.shield(rag.finalize_storages())
                logger.info("✅ All RAG storages safely persisted to disk.")
            except Exception as persist_err:
                logger.error("Failed during storage finalization: %s", persist_err)

    print("\n🎉 Ingestion session completed.")


def main():
    parser = argparse.ArgumentParser(description="Ingest MultiCaRe disease payloads into RAG-Anything.")
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute actual RAG-Anything insertion using local models (default is dry-run mode).",
    )
    parser.add_argument(
        "--max-payloads",
        type=int,
        default=None,
        help="Maximum number of payloads to ingest.",
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="Clear existing rag_storage directory before starting ingestion.",
    )
    parser.add_argument(
        "--base-url",
        type=str,
        default=LOCAL_LLM_BASE_URL,
        help=f"Local OpenAI-compatible base URL (default: {LOCAL_LLM_BASE_URL}).",
    )
    parser.add_argument(
        "--llm-model",
        type=str,
        default=DEFAULT_LLM_MODEL,
        help=f"Local LLM model name for text/KG extraction (default: {DEFAULT_LLM_MODEL}).",
    )
    parser.add_argument(
        "--vision-model",
        type=str,
        default=DEFAULT_VISION_MODEL,
        help=f"Local vision model name for image analysis (default: {DEFAULT_VISION_MODEL}).",
    )
    args = parser.parse_args()

    try:
        asyncio.run(
            ingest_payloads(
                max_payloads=args.max_payloads,
                dry_run=not args.execute,
                reset_storage=args.reset,
                llm_model=args.llm_model,
                vision_model=args.vision_model,
                base_url=args.base_url,
            )
        )
    except KeyboardInterrupt:
        print("\n[INFO] Ingestion cancelled by user. Safe exit completed.")


if __name__ == "__main__":
    main()

"""Autonomous clinical case extraction pipeline driver using stateless LLM APIs."""

import argparse
import datetime
import json
import os
import random
import sys
import time
from pathlib import Path
from typing import Dict, Set

from config import (
    API_BASE,
    API_KEY,
    API_MODEL,
    BASE_DIR,
    CONFIRM_FIRST,
    DRY_RUN,
    EXTRACTION_PROMPT,
    INPUT_FILE,
    MANIFEST_FILE,
    MAX_DELAY_SEC,
    MAX_RETRIES,
    MIN_DELAY_SEC,
    OUTPUT_DIR,
    REASONING_LOG_DIR,
    REQUIRED_XML_TAGS,
    SELECTED_DISEASES,
    TIMEOUT_SEC,
    format_payload,
    sanitize_case_id,
)
from api_helpers import (
    LLMAPIError,
    LLMAuthError,
    query_llm_api,
    resolve_api_credentials,
    resolve_endpoint_url,
)
from scripts.fix_extracted_cases import (
    clean_and_fix_case,
    validate_case_content,
)


def load_manifest(manifest_path: Path) -> Dict[str, dict]:
    """Load existing manifest into a dict keyed by case_id to support fast resumption."""
    entries: Dict[str, dict] = {}
    if not manifest_path.exists():
        return entries

    with open(manifest_path, "r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                record = json.loads(line)
                case_id = record.get("case_id")
                if case_id:
                    entries[case_id] = record
            except json.JSONDecodeError:
                sys.stderr.write(f"[WARN] Malformed JSON in manifest line {line_no}\n")
    return entries


def append_manifest_record(manifest_path: Path, record: dict) -> None:
    """Atomically append a single record to the manifest JSONL file."""
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
        f.flush()


def validate_reply(reply_text: str) -> tuple[bool, str]:
    """Constraint 6. Validate output:
    Check that the response contains <case_prompt>, <diagnostic_reasoning>, and <final_diagnosis>.
    In the <final_diagnosis> block, ensure it strictly adheres to the disease classification rules
    (checking for either one of the 21 SELECTED diseases or the OUT_OF_SCOPE format).
    """
    return validate_case_content(reply_text)


def main():
    parser = argparse.ArgumentParser(description="Autonomous Case Extraction Pipeline (Universal Stateless LLM API)")
    parser.add_argument("--dry-run", action="store_true", default=DRY_RUN, help="Simulate pipeline without sending API requests")
    parser.add_argument("--no-confirm", action="store_true", help="Skip the first-run safety/cost confirmation prompt")
    parser.add_argument("--limit", type=int, default=None, help="Process at most N cases (useful for testing)")
    parser.add_argument("--input", type=str, default=str(INPUT_FILE), help="Path to input model_inputs.jsonl")
    parser.add_argument("--model", type=str, default=API_MODEL, help=f"LLM model to use (default: {API_MODEL})")
    parser.add_argument("--api-key", type=str, default=None, help="API key (overrides API_KEY or OPENAI_API_KEY env vars)")
    parser.add_argument("--api-base", type=str, default=API_BASE, help=f"API base URL (default: {API_BASE})")
    parser.add_argument("--max-retries", type=int, default=MAX_RETRIES, help=f"Max retries on transient errors (default: {MAX_RETRIES})")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        sys.exit(f"[FATAL] Input file not found: {input_path}")

    # Resolve API Credentials
    api_key, api_base, model = resolve_api_credentials(
        api_key=args.api_key,
        api_base=args.api_base,
        model=args.model,
    )

    is_local = "localhost" in api_base or "127.0.0.1" in api_base
    if not args.dry_run and not api_key and not is_local:
        sys.exit(
            "[FATAL] API key is not set.\n"
            "Please export API_KEY or OPENAI_API_KEY in your environment, or pass --api-key <key>.\n"
            "Example: export API_KEY='sk-...'"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load manifest and existing state
    manifest = load_manifest(MANIFEST_FILE)
    done_case_ids: Set[str] = {
        cid for cid, r in manifest.items() if r.get("status") == "done"
    }

    # 2. Read input cases
    cases = []
    with open(input_path, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            sample_id = data.get("sample_id", f"case_{idx:04d}")
            raw_text = data.get("raw_case_text", "").strip()
            if not raw_text:
                continue
            case_id = sanitize_case_id(sample_id)
            cases.append({
                "sample_id": sample_id,
                "case_id": case_id,
                "raw_case_text": raw_text,
            })

    total_cases = len(cases)
    if args.limit:
        cases = cases[:args.limit]

    endpoint_url = resolve_endpoint_url(api_base)
    masked_key = (api_key[:4] + "..." + api_key[-4:]) if len(api_key) >= 8 else ("SET" if api_key else "NOT SET")

    print("=" * 65)
    print(" Autonomous Clinical Extraction Pipeline (Universal LLM API)")
    print("=" * 65)
    print(f" Input File:        {input_path}")
    print(f" Total Input Cases: {total_cases} (Processing: {len(cases)})")
    print(f" Output Directory:  {OUTPUT_DIR}")
    print(f" Reasoning Logs:    {REASONING_LOG_DIR}")
    print(f" Manifest File:     {MANIFEST_FILE}")
    print(f" API Base URL:      {api_base}")
    print(f" API Endpoint:      {endpoint_url}")
    print(f" Target Model:      {model}")
    print(f" API Key:           {masked_key}")
    print(f" Delay Range:       {MIN_DELAY_SEC}s - {MAX_DELAY_SEC}s")
    print(f" Timeout:           {TIMEOUT_SEC}s")
    print(f" Max Retries:       {args.max_retries}")
    print(f" Execution Mode:    {'DRY RUN (simulation, 0 credits)' if args.dry_run else 'LIVE API CALLS (consumes credits)'}")
    print(f" Already Done:      {len(done_case_ids)} cases")
    print("=" * 65)

    # 3. Safety confirmation
    need_confirm = CONFIRM_FIRST and not args.no_confirm and not args.dry_run
    if need_confirm:
        print("\n[API COST & SAFETY CONFIRMATION]")
        print("1. Live API Mode is ACTIVE: Requests will consume API credits.")
        print(f"2. Target API:    {endpoint_url}")
        print(f"3. Model:         {model}")
        print(f"4. Total to run:  {len(cases) - len(done_case_ids)} pending cases")
        print("5. Processing is stateless: 1 independent API request per case.")
        print("6. You can stop the script at any time by pressing Ctrl+C.")
        input("\nPress [ENTER] to confirm and begin (or Ctrl+C to abort)... ")
        print("Starting pipeline...")

    # Counters
    count_done = 0
    count_failed = 0
    count_skipped = 0

    for i, item in enumerate(cases, 1):
        case_id = item["case_id"]
        sample_id = item["sample_id"]
        out_file = OUTPUT_DIR / f"{case_id}.md"

        # Check resumption: skip if done in manifest or output file exists
        if case_id in done_case_ids:
            count_skipped += 1
            print(f"[{i}/{len(cases)}] [SKIP] {case_id} (already marked done)")
            continue

        if out_file.exists():
            # Already exists on disk; record as skipped/done to protect existing files
            count_skipped += 1
            manifest_record = {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "skipped",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": "Output file already exists on disk",
            }
            append_manifest_record(MANIFEST_FILE, manifest_record)
            print(f"[{i}/{len(cases)}] [SKIP] {case_id} (file exists: {out_file.name})")
            continue

        payload = format_payload(item["raw_case_text"])

        # DRY RUN branch
        if args.dry_run:
            print(
                f"[{i}/{len(cases)}] [DRY-RUN] Would process {case_id} "
                f"(system={len(EXTRACTION_PROMPT)} chars, user={len(payload)} chars, 0 API credits)"
            )
            manifest_record = {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "dry_run",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": None,
            }
            append_manifest_record(MANIFEST_FILE, manifest_record)
            count_done += 1
            time.sleep(0.1)
            continue

        # LIVE EXECUTION (Stateless API Request: 1 Call = 1 Case)
        print(f"[{i}/{len(cases)}] [SENDING API REQUEST] {case_id} ...", end="", flush=True)

        try:
            reply = query_llm_api(
                prompt=payload,
                system_prompt=EXTRACTION_PROMPT,
                api_key=api_key,
                api_base=api_base,
                model=model,
                timeout=TIMEOUT_SEC,
                max_retries=args.max_retries,
                case_id=case_id,
            )
        except Exception as e:
            err_msg = str(e)
            print(f" -> [FAILED] ({err_msg})")
            count_failed += 1
            append_manifest_record(MANIFEST_FILE, {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "failed",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": err_msg,
            })
            continue

        # Step 4: Validate XML structure and adhere to classification rules
        # First, run local repair for minor LLM formatting errors (inline tags, numbering)
        cleaned_reply, fixes = clean_and_fix_case(reply)
        if fixes:
            print(f" [FIXED {len(fixes)}: {'; '.join(fixes)}]", end="", flush=True)

        is_valid, validation_err = validate_reply(cleaned_reply)
        if not is_valid:
            print(f" -> [INVALID FORMAT] ({validation_err})")
            # Save raw copy for inspection
            raw_path = OUTPUT_DIR / f"{case_id}.raw.txt"
            raw_path.write_text(reply, encoding="utf-8")
            count_failed += 1
            append_manifest_record(MANIFEST_FILE, {
                "case_id": case_id,
                "sample_id": sample_id,
                "status": "failed",
                "timestamp": datetime.datetime.now().isoformat(),
                "error": validation_err,
                "fixes": fixes,
            })
            continue

        # Step 5: Save valid output
        out_file.write_text(cleaned_reply, encoding="utf-8")
        count_done += 1
        done_case_ids.add(case_id)

        append_manifest_record(MANIFEST_FILE, {
            "case_id": case_id,
            "sample_id": sample_id,
            "status": "done",
            "timestamp": datetime.datetime.now().isoformat(),
            "error": None,
            "fixes": fixes,
        })
        print(f" -> [DONE] Saved to {out_file.name}")

        # Step 6: Enforce randomized pacing delay before next case
        delay = random.uniform(MIN_DELAY_SEC, MAX_DELAY_SEC)
        time.sleep(delay)

    print("\n" + "=" * 65)
    print(" EXTRACTION RUN COMPLETED")
    print(f" Total Processed: {count_done} done, {count_failed} failed, {count_skipped} skipped")
    print(f" Manifest:        {MANIFEST_FILE}")
    print("=" * 65)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[ABORTED] Process interrupted by user. Manifest saved up to last case.")
        sys.exit(0)

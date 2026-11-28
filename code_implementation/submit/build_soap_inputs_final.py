"""Build model_inputs_soap_21_final.jsonl from structured case files in soap/ with clinical_label and final_diagnosis."""
# this is basically the same with build_soap_inputs.py with clinical_label and final_diagnosis.
# Kept since we used this for stitch reasoning
import argparse
import json
from pathlib import Path
import re
import sys
from typing import Optional, Set

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import SELECTED_DISEASES, sanitize_case_id


def normalize_disease_slug(name: str) -> str:
    """Normalize a disease folder or target_disease name into a canonical slug."""
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_")


def resolve_final_diagnosis(target_disease: str, clinical_label: str) -> str:
    """Return target_disease for POSITIVE cases and OUT_OF_SCOPE for NEGATIVE cases."""
    if clinical_label == "POSITIVE":
        return target_disease
    if clinical_label == "NEGATIVE":
        return "OUT_OF_SCOPE"
    raise ValueError(f"Unsupported clinical_label '{clinical_label}'; expected POSITIVE or NEGATIVE")


def build_soap_inputs_final(
    soap_dir: Path,
    output_file: Path,
    allowed_slugs: Optional[Set[str]] = None,
) -> int:
    """Read case JSON files under soap_dir and write JSONL with clinical_label and final_diagnosis."""
    if not soap_dir.exists() or not soap_dir.is_dir():
        raise FileNotFoundError(f"SOAP directory not found: {soap_dir}")

    seen_sample_ids = set()
    seen_case_ids = set()
    records = []

    disease_dirs = sorted(
        p for p in soap_dir.iterdir()
        if p.is_dir() and not p.name.startswith(".")
    )

    for disease_dir in disease_dirs:
        if allowed_slugs is not None and normalize_disease_slug(disease_dir.name) not in allowed_slugs:
            continue

        for json_path in sorted(disease_dir.glob("*.json")):
            data = json.loads(json_path.read_text(encoding="utf-8"))
            sample_id = (data.get("pair_id") or "").strip()
            raw_case_text = data.get("raw_case_text") or ""
            target_disease = (data.get("target_disease") or disease_dir.name).strip()
            clinical_label = (data.get("clinical_label") or "").strip().upper()

            if allowed_slugs is not None and normalize_disease_slug(target_disease) not in allowed_slugs:
                continue

            if not sample_id:
                raise ValueError(f"Missing pair_id in {json_path}")
            if not raw_case_text.strip():
                raise ValueError(f"Empty raw_case_text in {json_path}")
            if clinical_label not in {"POSITIVE", "NEGATIVE"}:
                raise ValueError(f"Invalid or missing clinical_label '{clinical_label}' in {json_path}")
            if sample_id in seen_sample_ids:
                raise ValueError(f"Duplicate sample_id '{sample_id}' in {json_path}")

            case_id = sanitize_case_id(sample_id)
            if case_id in seen_case_ids:
                raise ValueError(f"Duplicate sanitized case_id '{case_id}' for '{sample_id}'")

            seen_sample_ids.add(sample_id)
            seen_case_ids.add(case_id)

            records.append({
                "sample_id": sample_id,
                "raw_case_text": raw_case_text,
                "target_disease": target_disease,
                "clinical_label": clinical_label,
                "final_diagnosis": resolve_final_diagnosis(target_disease, clinical_label),
            })

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    return len(records)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create final JSONL model inputs with clinical_label and final_diagnosis from soap/ directory."
    )
    parser.add_argument("--soap-dir", type=Path, default=ROOT_DIR / "soap", help="Path to soap directory")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "model_inputs_soap_21_final.jsonl",
        help="Path to output JSONL file",
    )
    parser.add_argument(
        "--all-diseases",
        action="store_true",
        help="Include all diseases in soap/ instead of filtering to SELECTED_DISEASES (21 diseases)",
    )
    args = parser.parse_args()

    allowed_slugs = None if args.all_diseases else {d.lower() for d in SELECTED_DISEASES}
    count = build_soap_inputs_final(args.soap_dir, args.output, allowed_slugs=allowed_slugs)
    print(f"Wrote {count} cases from {args.soap_dir} to {args.output}")


if __name__ == "__main__":
    main()

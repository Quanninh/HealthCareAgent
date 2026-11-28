"""Export out_oss_Khoa29/*.md joined with model_inputs_soap_21_final.jsonl into oss_extracted_cases.jsonl."""
# this is used for stitch reasoning
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Dict

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from config import SELECTED_DISEASES, sanitize_case_id
from scripts.fix_extracted_cases import _find_section_match, _resolve_selected_token


def resolve_canonical_12step(label: str) -> str:
    """Resolve a 12step final_diagnosis label from SOAP to OUT_OF_SCOPE or a canonical SELECTED disease."""
    cleaned = label.strip()
    if cleaned.upper() == "OUT_OF_SCOPE":
        return "OUT_OF_SCOPE"

    resolved = _resolve_selected_token(cleaned)
    if resolved is not None:
        return resolved

    slug = re.sub(r"[^a-z0-9]+", "_", cleaned.lower()).strip("_")
    resolved_slug = _resolve_selected_token(slug)
    if resolved_slug is not None:
        return resolved_slug

    if slug in SELECTED_DISEASES:
        return slug
    raise ValueError(f"Cannot resolve 12step label '{label}' to canonical disease or OUT_OF_SCOPE")


def is_diagnosis_matched(canonical_12step: str, oss_final_diagnosis: str) -> bool:
    """Return True if canonical_12step matches the OSS <final_diagnosis> output."""
    diag = oss_final_diagnosis.strip()
    if not diag:
        return False

    if canonical_12step == "OUT_OF_SCOPE":
        return "OUT_OF_SCOPE" in diag

    if "OUT_OF_SCOPE" in diag:
        return False

    tokens = [t.strip() for t in re.split(r"[,;\n]+", diag) if t.strip()]
    resolved_tokens = set()
    for tok in tokens:
        resolved = _resolve_selected_token(tok)
        if resolved is not None:
            resolved_tokens.add(resolved)
        else:
            resolved_tokens.add(re.sub(r"[^a-z0-9]+", "_", tok.lower()).strip("_"))
    return canonical_12step in resolved_tokens


def extract_sections(md_text: str) -> Dict[str, str]:
    """Extract the 4 XML sections from an extracted case Markdown file."""
    tags = ("case_analysis", "case_prompt", "diagnostic_reasoning", "final_diagnosis")
    result: Dict[str, str] = {}
    for tag in tags:
        match = _find_section_match(md_text, tag)
        result[tag] = match.group(1).strip() if match else ""
    return result


def export_oss_extracted_cases(
    inputs_jsonl: Path,
    md_dir: Path,
    output_jsonl: Path,
) -> Dict[str, int]:
    """Build oss_extracted_cases.jsonl ordered by inputs_jsonl."""
    stats = {
        "total": 0,
        "matched": 0,
        "unmatched": 0,
        "pos_total": 0,
        "pos_matched": 0,
        "neg_total": 0,
        "neg_matched": 0,
    }

    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    with open(inputs_jsonl, "r", encoding="utf-8") as in_f, open(output_jsonl, "w", encoding="utf-8") as out_f:
        for line in in_f:
            if not line.strip():
                continue
            src = json.loads(line)
            sample_id = src["sample_id"]
            case_id = sanitize_case_id(sample_id)
            md_path = md_dir / f"{case_id}.md"
            if not md_path.exists():
                raise FileNotFoundError(f"Missing extracted markdown file: {md_path}")

            sections = extract_sections(md_path.read_text(encoding="utf-8"))
            step_12 = src["final_diagnosis"]
            canonical_12step = resolve_canonical_12step(step_12)
            matched = is_diagnosis_matched(canonical_12step, sections["final_diagnosis"])

            row = {
                "case_id": case_id,
                "sample_id": sample_id,
                "case_analysis": sections["case_analysis"],
                "case_prompt": sections["case_prompt"],
                "diagnostic_reasoning": sections["diagnostic_reasoning"],
                "final_diagnosis": sections["final_diagnosis"],
                "target_disease": src["target_disease"],
                "clinical_label": src["clinical_label"],
                "12step": step_12,
                "matched": matched,
            }
            out_f.write(json.dumps(row, ensure_ascii=False) + "\n")

            stats["total"] += 1
            if matched:
                stats["matched"] += 1
            else:
                stats["unmatched"] += 1
            if src["clinical_label"] == "POSITIVE":
                stats["pos_total"] += 1
                if matched:
                    stats["pos_matched"] += 1
            elif src["clinical_label"] == "NEGATIVE":
                stats["neg_total"] += 1
                if matched:
                    stats["neg_matched"] += 1

    return stats


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Join OSS extracted .md files with model_inputs_soap_21_final.jsonl and compute match."
    )
    parser.add_argument(
        "--inputs",
        type=Path,
        default=ROOT_DIR / "model_inputs_soap_21_final.jsonl",
        help="Path to model_inputs_soap_21_final.jsonl",
    )
    parser.add_argument(
        "--md-dir",
        type=Path,
        default=ROOT_DIR / "out_oss_Khoa29",
        help="Directory containing extracted .md files",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT_DIR / "oss_extracted_cases.jsonl",
        help="Output JSONL path",
    )
    args = parser.parse_args()

    stats = export_oss_extracted_cases(args.inputs, args.md_dir, args.output)
    print(f"Wrote {stats['total']} cases to {args.output}")
    print(
        f"Matched: {stats['matched']}/{stats['total']} "
        f"({stats['matched'] / stats['total']:.2%}) | "
        f"POSITIVE matched: {stats['pos_matched']}/{stats['pos_total']} | "
        f"NEGATIVE matched: {stats['neg_matched']}/{stats['neg_total']}"
    )


if __name__ == "__main__":
    main()

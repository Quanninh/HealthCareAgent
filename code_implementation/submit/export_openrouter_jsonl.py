"""Convert extracted Markdown files into a JSONL file ordered by manifest.jsonl."""
# this may be DELETED since export_oss_extracted_cases.py is the same with comparisons added
# this is used for reasoning extract
import json
import re
from pathlib import Path


def convert_md_to_jsonl(
    manifest_path: Path,
    md_dir: Path,
    output_path: Path,
) -> None:
    manifest_lines = [
        json.loads(line)
        for line in manifest_path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    tags = ["case_analysis", "case_prompt", "diagnostic_reasoning", "final_diagnosis"]

    with open(output_path, "w", encoding="utf-8") as out_f:
        for entry in manifest_lines:
            case_id = entry["case_id"]
            md_file = md_dir / f"{case_id}.md"

            content = md_file.read_text(encoding="utf-8")

            row = {
                "case_id": case_id,
                "sample_id": entry.get("sample_id", ""),
            }

            for tag in tags:
                pattern = rf"<{tag}>(.*?)</{tag}>"
                match = re.search(pattern, content, re.DOTALL)
                row[tag] = match.group(1).strip() if match else ""

            out_f.write(json.dumps(row, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent.parent
    convert_md_to_jsonl(
        manifest_path=base_dir / "out_openrouter" / "manifest.jsonl",
        md_dir=base_dir / "out_openrouter",
        output_path=base_dir / "out_openrouter" / "extracted_cases.jsonl",
    )

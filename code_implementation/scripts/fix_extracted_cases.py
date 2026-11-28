"""Utility and CLI script to inspect, clean, and validate extracted clinical case outputs."""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Optional, Tuple

try:
    from config import OUTPUT_DIR, REQUIRED_XML_TAGS, SELECTED_DISEASES
except ImportError:
    parent_dir = Path(__file__).resolve().parent.parent
    if str(parent_dir) not in sys.path:
        sys.path.insert(0, str(parent_dir))
    from config import OUTPUT_DIR, REQUIRED_XML_TAGS, SELECTED_DISEASES

SELECTED_SET = {d.lower(): d for d in SELECTED_DISEASES}

# Mapping common synonyms to canonical names (Rule 7.5)
SYNONYM_MAP = {
    "sars-cov-2": "covid_19",
    "covid-19": "covid_19",
    "covid19": "covid_19",
    "covid 19": "covid_19",
    "hiv": "hiv_aids",
    "aids": "hiv_aids",
    "hiv/aids": "hiv_aids",
    "hiv aids": "hiv_aids",
    "tb": "tuberculosis",
    "ebola": "ebola_filovirus",
    "ebolavirus": "ebola_filovirus",
    "ebola filovirus": "ebola_filovirus",
    "ebola virus": "ebola_filovirus",
    "yellow fever": "yellow_fever",
    "visceral leishmaniasis": "leishmaniasis",
    "kala-azar": "leishmaniasis",
    "kala azar": "leishmaniasis",
    "cmv": "cytomegalovirus",
    "pjp": "pneumocystis",
    "pcp": "pneumocystis",
    "pneumocystis jirovecii": "pneumocystis",
    "pneumocystis jirovecii pneumonia": "pneumocystis",
    "pneumocystis pneumonia": "pneumocystis",
    "pneumocystis carinii": "pneumocystis",
    "pneumocystis carinii pneumonia": "pneumocystis",
    "hansen": "leprosy",
    "hansen's disease": "leprosy",
    "hansens disease": "leprosy",
    "hansen disease": "leprosy",
}


def _fix_newlines_for_tag(text: str, name: str, start_pos: int = 0) -> Tuple[str, List[str]]:
    """Ensure <name> and </name> are on their own lines starting from start_pos."""
    changes = []
    prefix = text[:start_pos]
    target = text[start_pos:]

    open_tag = f"<{name}>"
    open_pat = re.compile(rf"(?:(?<=^)|(?<=>))[ \t]*({re.escape(open_tag)})[ \t]*(?!\n|$)", re.MULTILINE)
    if open_pat.search(target):
        target = open_pat.sub(r"\1\n", target)
        changes.append(f"Added newline after opening {open_tag}")

    close_tag = f"</{name}>"
    close_pat = re.compile(rf"(?<!\n)[ \t]*{re.escape(close_tag)}")
    if close_pat.search(target):
        target = close_pat.sub(f"\n{close_tag}", target)
        changes.append(f"Added newline before closing {close_tag}")

    return prefix + target, changes


def fix_tag_newlines(text: str) -> Tuple[str, List[str]]:
    """Ensure all XML section tags start and end on their own lines without breaking prose mentions."""
    # Fixes case_analysis from start_pos=0, then locates </case_analysis> and only fixes case_prompt, diagnostic_reasoning, and final_diagnosis after </case_analysis>
    # so prose mentions inside <case_analysis> (such as "so <final_diagnosis> is not spoiled") are never split across lines
    changes = []
    text, ca_changes = _fix_newlines_for_tag(text, "case_analysis", start_pos=0)
    changes.extend(ca_changes)

    ca_end = text.find("</case_analysis>")
    after_ca = ca_end + len("</case_analysis>") if ca_end != -1 else 0

    for name in ("case_prompt", "diagnostic_reasoning", "final_diagnosis"):
        text, tag_changes = _fix_newlines_for_tag(text, name, start_pos=after_ca)
        changes.extend(tag_changes)

    return text, changes

# this code attempts to fix the fix cases analysis block, however 
# AI can behave unexpected so that not all lines are fixed
def fix_case_analysis_block(analysis_text: str) -> Tuple[str, List[str]]:
    """Ensure consistent numbered sections inside <case_analysis>...</case_analysis>."""
    changes = []
    cleaned = analysis_text.strip()
    if not cleaned:
        return "", changes

    section_split_pat = (
        r"\n\s*\n|\n(?=(?:[123]\.\s|"
        r"target\s+diagnosis|ideal\s+breakpoint|best\s+breakpoint|breakpoint|"
        r"author['’]?s\s+analytic|key\s+analytic|analytic\s+distinctions))"
    )
    paras = [p.strip() for p in re.split(section_split_pat, cleaned, flags=re.IGNORECASE) if p.strip()]
    if not paras:
        return cleaned, changes

    section_patterns = [
        (
            r"^(?:1\.\s*)?target\s+diagnosis(?:\s*(?:identification|&\s*(?:scope\s+)?check))?(?:\s*\([^)]*\))?:?\s*",
            "1. Target Diagnosis & Scope Check: ",
        ),
        (
            r"^(?:2\.\s*)?(?:(?:best|ideal)\s+breakpoint|breakpoint(?:\s+(?:selection|choice))?)(?:\s*\([^)]*\))?:?\s*",
            "2. Best breakpoint: ",
        ),
        (
            r"^(?:3\.\s*)?(?:(?:author['’]?s\s+)?(?:key\s+)?analytic\s+distinctions?|distinctions?)(?:\s*\([^)]*\))?:?\s*",
            "3. Key analytic distinctions: ",
        ),
    ]

    fixed_paras = []
    for i, p in enumerate(paras):
        if i < len(section_patterns):
            pat, prefix = section_patterns[i]
            if re.match(pat, p, re.IGNORECASE):
                body = re.sub(pat, "", p, count=1, flags=re.IGNORECASE).strip()
                if not p.startswith(prefix):
                    changes.append(f"Standardized <case_analysis> paragraph {i+1} prefix to '{prefix.strip()}'")
                fixed_paras.append(f"{prefix}{body}")
            elif not re.match(r"^\d+\.\s*", p):
                changes.append(f"Added numbering '{i+1}. ' to <case_analysis> paragraph {i+1}")
                fixed_paras.append(f"{i+1}. {p}")
            else:
                fixed_paras.append(p)
        else:
            fixed_paras.append(p)

    separator = "\n\n" if "\n\n" in cleaned else "\n"
    return separator.join(fixed_paras), changes


def fix_reasoning_block(reasoning_text: str) -> Tuple[str, List[str]]:
    """Ensure all bullet reasons in <diagnostic_reasoning> are properly numbered 1, 2, 3..."""
    changes = []
    cleaned = reasoning_text.strip()
    if not cleaned:
        return "", changes

    raw_paras = [p.strip() for p in re.split(r"\n\s*\n", cleaned) if p.strip()]
    if len(raw_paras) == 1 and "\n" in raw_paras[0] and raw_paras[0].count("|") > 1:
        raw_paras = [p.strip() for p in raw_paras[0].split("\n") if p.strip()]

    fixed_items = []
    for idx, item in enumerate(raw_paras, 1):
        num_match = re.match(r"^(?:\d+[\.\)]|\-|\*)\s*(.*)", item, re.DOTALL)
        if num_match:
            body = num_match.group(1).strip()
            expected_prefix = f"{idx}. "
            if not item.startswith(expected_prefix):
                changes.append(f"Renumbered reasoning item {idx}")
            fixed_items.append(f"{expected_prefix}{body}")
        else:
            if "|" in item or idx == 1:
                changes.append(f"Added number '{idx}. ' to unnumbered reasoning item")
                fixed_items.append(f"{idx}. {item}")
            else:
                fixed_items.append(item)

    return "\n\n".join(fixed_items), changes


def _resolve_selected_token(token: str) -> Optional[str]:
    """Resolve a single diagnosis token to a canonical SELECTED disease if it matches."""
    token_lower = token.strip().lower()
    if token_lower in SYNONYM_MAP:
        return SYNONYM_MAP[token_lower]
    if token_lower in SELECTED_SET:
        return SELECTED_SET[token_lower]
    return None


def fix_final_diagnosis(diag_text: str) -> Tuple[str, List[str]]:
    """Normalize the <final_diagnosis> block using ONLY the <final_diagnosis> text itself.

    Unrecognized or unadorned diagnoses are left untouched so validate_case_content
    rejects them and flags the case to run again.
    """
    changes = []
    cleaned = diag_text.strip()
    if not cleaned:
        return "", changes

    resolved = _resolve_selected_token(cleaned)
    if resolved:
        if cleaned.lower() in SYNONYM_MAP:
            changes.append(f"Mapped synonym '{cleaned}' to canonical SELECTED disease '{resolved}'")
        elif cleaned != resolved:
            changes.append(f"Normalized case of SELECTED disease '{cleaned}' to '{resolved}'")
        return resolved, changes

    parts = [p.strip() for p in re.split(r"[,;\n]+", cleaned) if p.strip()]
    if len(parts) > 1:
        resolved_parts = [_resolve_selected_token(p) for p in parts]
        if all(rp is not None for rp in resolved_parts):
            canonical_multi = ", ".join(resolved_parts)  # type: ignore[arg-type]
            if cleaned != canonical_multi:
                changes.append(f"Normalized multiple SELECTED diseases '{cleaned}' -> '{canonical_multi}'")
            return canonical_multi, changes

    oos_match = re.match(r"^(.+?)\s*->\s*OUT_OF_SCOPE$", cleaned, re.IGNORECASE)
    if oos_match:
        disease_name = oos_match.group(1).strip()
        # Do not silently flip SELECTED -> OUT_OF_SCOPE; validate_case_content will reject it for re-run.
        if _resolve_selected_token(disease_name.strip("[]").strip()) is not None:
            return cleaned, changes
        canonical_oos = f"{disease_name} -> OUT_OF_SCOPE"
        if cleaned != canonical_oos:
            changes.append(f"Cleaned spacing in '{cleaned}' -> '{canonical_oos}'")
        return canonical_oos, changes

    return cleaned, changes


def _find_section_match(text: str, tag_name: str) -> Optional[re.Match]:
    """Find a section block, searching after </case_analysis> for downstream tags."""
    start_pos = 0
    if tag_name != "case_analysis":
        ca_end = text.find("</case_analysis>")
        if ca_end != -1:
            start_pos = ca_end + len("</case_analysis>")

    if tag_name == "final_diagnosis":
        pattern = re.compile(r"<final_diagnosis>(?!.*<final_diagnosis>)(.*?)</final_diagnosis>", re.DOTALL)
    else:
        pattern = re.compile(rf"<{tag_name}>(.*?)</{tag_name}>", re.DOTALL)
    return pattern.search(text, pos=start_pos)


def clean_and_fix_case(text: str) -> Tuple[str, List[str]]:
    """Perform end-to-end cleaning and repair on extracted case markdown text."""
    all_changes = []

    # 0. Strip leading preamble before <case_analysis> (or first XML tag if missing)
    cp_idx = text.find("<case_prompt>")
    if cp_idx != -1:
        analysis_idx = text.rfind("<case_analysis>", 0, cp_idx)
        if analysis_idx > 0:
            if text[:analysis_idx].strip():
                all_changes.append("Stripped leading text before <case_analysis>")
            text = text[analysis_idx:]
        elif analysis_idx == -1 and "<case_analysis>" not in text:
            first_tag_idx = text.find("<")
            if first_tag_idx > 0:
                if text[:first_tag_idx].strip():
                    all_changes.append("Stripped leading text before first XML tag")
                text = text[first_tag_idx:]

    if "<case_analysis>" in text and "</case_analysis>" not in text and "<case_prompt>" in text:
        text = text.replace("<case_prompt>", "</case_analysis>\n\n<case_prompt>", 1)
        all_changes.append("Inserted missing closing </case_analysis> tag before <case_prompt>")

    # 1. Fix tag newlines
    text, nl_changes = fix_tag_newlines(text)
    all_changes.extend(nl_changes)

    # 2. Fix <case_analysis> block
    analysis_match = _find_section_match(text, "case_analysis")
    if analysis_match:
        fixed_analysis, analysis_changes = fix_case_analysis_block(analysis_match.group(1))
        if analysis_changes:
            text = text[:analysis_match.start(1)] + f"\n{fixed_analysis}\n" + text[analysis_match.end(1):]
            all_changes.extend(analysis_changes)

    # 3. Fix <diagnostic_reasoning> block
    reasoning_match = _find_section_match(text, "diagnostic_reasoning")
    if reasoning_match:
        fixed_reasoning, reasoning_changes = fix_reasoning_block(reasoning_match.group(1))
        if reasoning_changes:
            text = text[:reasoning_match.start(1)] + f"\n{fixed_reasoning}\n" + text[reasoning_match.end(1):]
            all_changes.extend(reasoning_changes)

    # 4. Fix <final_diagnosis> block
    diag_match = _find_section_match(text, "final_diagnosis")
    if diag_match:
        fixed_diag, diag_changes = fix_final_diagnosis(diag_match.group(1))
        if diag_changes:
            text = text[:diag_match.start(1)] + f"\n{fixed_diag}\n" + text[diag_match.end(1):]
            all_changes.extend(diag_changes)

    # 5. Normalize spacing between XML blocks
    text = re.sub(r"(</case_analysis>)\s*(<case_prompt>)", r"\1\n\n\2", text)
    text = re.sub(r"(</case_prompt>)\s*(<diagnostic_reasoning>)", r"\1\n\n\2", text)
    text = re.sub(r"(</diagnostic_reasoning>)\s*(<final_diagnosis>)", r"\1\n\n\2", text)

    return text.strip() + "\n", all_changes


def validate_case_content(reply_text: str) -> Tuple[bool, str]:
    """Constraint 6: Verify required XML tags and Rule 7 <final_diagnosis> formatting."""
    # check if the answer has all starting and closing tag
    missing = [tag for tag in REQUIRED_XML_TAGS if tag not in reply_text]
    if missing:
        return False, f"Missing required XML tags: {', '.join(missing)}"

    cp_match = _find_section_match(reply_text, "case_prompt")
    if not cp_match or not cp_match.group(1).strip():
        return False, "Missing or empty <case_prompt> block"

    dr_match = _find_section_match(reply_text, "diagnostic_reasoning")
    if not dr_match or not dr_match.group(1).strip():
        return False, "Missing or empty <diagnostic_reasoning> block"

    match = _find_section_match(reply_text, "final_diagnosis")
    if not match:
        return False, "Could not extract content from <final_diagnosis> tag"

    final_diag = match.group(1).strip()
    if not final_diag:
        return False, "<final_diagnosis> is empty"

    # Rule 7.3: [Exact disease name] -> OUT_OF_SCOPE
    oos_match = re.match(r"^(.+?)\s*->\s*OUT_OF_SCOPE$", final_diag, re.IGNORECASE)
    if oos_match:
        oos_disease = oos_match.group(1).strip()
        oos_unbracketed = oos_disease.strip("[]").strip() # deal with cases when AI outputs [disease]
        if not oos_unbracketed:
            return False, "OUT_OF_SCOPE diagnosis missing disease name before '-> OUT_OF_SCOPE'"
        resolved_oos = _resolve_selected_token(oos_unbracketed)
        if resolved_oos is not None: # check if dengue -> OUT_OF_SCOPE is present
            return False, f"Disease '{oos_disease}' is in SELECTED_DISEASES, cannot be OUT_OF_SCOPE (Rule 7.2/7.3)"
        return True, ""

    # Rule 7.1 & 7.2: One or more SELECTED diseases (reject trailing/empty separators)
    raw_parts = re.split(r"[,;\n]+", final_diag)
    parts = [p.strip() for p in raw_parts]
    if parts and all(p and p.lower() in SELECTED_SET for p in parts):
        return True, ""

    return False, (
        f"Invalid <final_diagnosis>: '{final_diag}'. "
        f"Must strictly be either one of the 21 SELECTED diseases ({', '.join(SELECTED_DISEASES)}) "
        f"or follow the '[disease name] -> OUT_OF_SCOPE' format."
    )


def process_file(file_path: Path, dry_run: bool = False) -> Tuple[bool, List[str]]:
    """Clean and validate a single extracted markdown case file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error reading {file_path.name}: {e}"]

    fixed_content, changes = clean_and_fix_case(content)
    is_valid, val_err = validate_case_content(fixed_content)
    if not is_valid:
        changes.append(f"[VALIDATION FAILED] {val_err}")

    if changes and not dry_run:
        file_path.write_text(fixed_content, encoding="utf-8")

    return is_valid, changes


def main():
    parser = argparse.ArgumentParser(description="Check and fix minor formatting errors in extracted case reports.")
    parser.add_argument("--file", type=str, help="Path to single markdown file to fix")
    parser.add_argument("--dir", type=str, default=str(OUTPUT_DIR), help=f"Path to directory containing markdown cases (default: {OUTPUT_DIR})")
    parser.add_argument("--check", action="store_true", help="Dry run only: check without modifying files")
    args = parser.parse_args()

    if args.file:
        p = Path(args.file)
        if not p.exists():
            sys.exit(f"File not found: {p}")
        files_to_process = [p]
    else:
        d = Path(args.dir)
        if not d.exists():
            sys.exit(f"Directory not found: {d}")
        files_to_process = sorted(f for f in d.glob("*.md") if not f.name.endswith(".raw.txt"))

    print("=" * 65)
    print(" Extracted Case Output Normalizer & Validator")
    print("=" * 65)
    print(f" Target Files: {len(files_to_process)}")
    print(f" Mode:         {'CHECK ONLY (Dry Run)' if args.check else 'FIX IN-PLACE'}")
    print("=" * 65)

    n_fixed = 0
    n_valid = 0
    n_invalid = 0

    for file_path in files_to_process:
        is_valid, changes = process_file(file_path, dry_run=args.check)
        status_str = "VALID" if is_valid else "INVALID"
        if is_valid:
            n_valid += 1
        else:
            n_invalid += 1

        if changes:
            n_fixed += 1
            print(f"\n[{status_str}] {file_path.name} ({len(changes)} changes):")
            for c in changes:
                print(f"  - {c}")
        else:
            print(f"[{status_str}] {file_path.name} (already clean)")

    print("\n" + "=" * 65)
    print(f" Finished: {n_fixed} file(s) modified, {n_valid} valid, {n_invalid} invalid.")
    print("=" * 65)


if __name__ == "__main__":
    main()

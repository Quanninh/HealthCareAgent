#!/usr/bin/env python3
"""
generate_disease_skills.py
===========================
Generates 15 disease-specific SKILL.md files under:
    .agents/skills/disease-agent-{slug}/SKILL.md

Each SKILL.md contains:
  1. The shared 12-step annotation protocol (from clinical-annotator/SKILL.md)
  2. The disease-specific evidence section from 03_evidence_specificity_matrix.md
  3. Cross-disease rules (sections 6-14 from the same matrix)

Usage:
    python3 generate_disease_skills.py [--dry-run]
"""

import re
import argparse
import sys
from pathlib import Path

SANDBOX_DIR = Path(__file__).resolve().parent
REPO_ROOT   = SANDBOX_DIR.parent
sys.path.insert(0, str(REPO_ROOT / "src"))

from clinical_data.curation import DISEASES, DISEASE_EVIDENCE_EXAMPLES

MATRIX_PATH = SANDBOX_DIR / "protocols" / "03_evidence_specificity_matrix.md"
BASE_SKILL  = SANDBOX_DIR / ".agents" / "skills" / "clinical-annotator" / "SKILL.md"
SKILLS_DIR  = SANDBOX_DIR / ".agents" / "skills"


def parse_matrix(matrix_text: str) -> tuple:
    """
    Parse 03_evidence_specificity_matrix.md and extract:
      - per-disease sections (5.1 - 5.15)  → sections dict
      - shared cross-disease sections (6-14) → cross_disease str
      - section 16 reference table rows     → ref_rows dict {disease_key: row_line}
      - universal eligibility rule (sec 4)  → universal_rule str
    Section 15 (Research Questions) and 16 (References) are handled separately.
    """
    lines = matrix_text.splitlines()
    sections = {}   # header_text → content_lines
    current_key = None
    current_lines = []

    # Split at every '#' or '##' heading (sections 6-14 of the matrix use a
    # single '#', so splitting on '## ' alone merged them into 5.15 and left
    # the cross-disease rules empty). '###' and deeper stay inside their parent.
    for line in lines:
        if line.startswith("# ") or line.startswith("## "):
            if current_key is not None:
                sections[current_key] = "\n".join(current_lines).strip()
            current_key = line.lstrip("#").strip()
            current_lines = [line]
        else:
            if current_key is not None:
                current_lines.append(line)
    if current_key is not None:
        sections[current_key] = "\n".join(current_lines).strip()

    # Cross-disease: sections 6-14 only (skip 15 = Research Questions, 16 = References)
    cross_keys = [k for k in sections if re.match(r"^(6|7|8|9|10|11|12|13|14)\.", k)]
    cross_parts = [sections[k] for k in cross_keys]
    cross_disease_content = "\n\n---\n\n".join(cross_parts)

    # Parse section 16 reference table into a dict: disease_label → full table row
    ref_rows: dict[str, str] = {}
    sec16_match = re.search(
        r"# 16\. Primary Reference Sources.*?\|---\|---\|(.+?)(?=\n---|\.md$)",
        matrix_text, re.DOTALL
    )
    if sec16_match:
        for row in sec16_match.group(1).strip().splitlines():
            row = row.strip()
            if row.startswith("|") and row.count("|") >= 3:
                parts = [p.strip() for p in row.strip("|").split("|", 1)]
                if len(parts) == 2:
                    ref_rows[parts[0]] = row  # e.g. ref_rows["Brucellosis"] = "| Brucellosis | ... |"

    # Universal eligibility rule (section 4)
    section4_match = re.search(
        r"(# 4\. Universal Claim Eligibility Rule.*?)(?=\n# 5\.)",
        matrix_text, re.DOTALL
    )
    universal_rule = section4_match.group(1).strip() if section4_match else ""

    return sections, cross_disease_content, ref_rows, universal_rule


def extract_disease_section(sections: dict, section_header: str) -> str:
    """Find the disease section by matching the header suffix."""
    for key, content in sections.items():
        if key.endswith(section_header) or key == section_header:
            return content
    # Try partial match
    for key, content in sections.items():
        if section_header.lower() in key.lower():
            return content
    return f"[WARNING: section '{section_header}' not found in matrix]"


def load_base_skill() -> str:
    """Load the shared clinical-annotator SKILL.md content (body only, strip YAML frontmatter)."""
    text = BASE_SKILL.read_text(encoding="utf-8")
    # Strip YAML frontmatter (--- ... ---)
    if text.startswith("---"):
        end = text.index("---", 3)
        text = text[end + 3:].lstrip()
    return text


def format_disease_protocol(
    base_protocol: str,
    slug: str,
    primary_disease: str,
    display_name: str,
) -> str:
    """
    Specialize the base 12-step protocol for the given disease:
      - Replace generic Step 9 with structured step9_key_evidence specification
        and a disease-specific example.
      - Replace generic Output Record Schema with structured schema tailored to the disease.
    """
    ex = DISEASE_EVIDENCE_EXAMPLES.get(slug, {
        "test_name": f"{display_name} confirmatory test",
        "target_concept": primary_disease,
        "specimen": "blood",
        "start_char": 100,
        "end_char": 180,
        "source_quote": f"Diagnostic testing confirmed presence of {primary_disease}",
        "patient_anchor_id": "patient_1",
        "result": "POSITIVE",
        "temporality": "CURRENT_EPISODE",
        "relation": "SUPPORTS",
        "strength": "E1_CONFIRMATORY",
        "rationale": f"Clinical findings and laboratory test confirmed active {primary_disease} — E1 confirmatory evidence. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied -> POSITIVE.",
    })

    step9_replacement = f"""### Step 9 — Evidence assessment (`evidence_strength` and `step9_key_evidence`)

Use `sandbox/protocols/03_evidence_specificity_matrix.md` for disease-specific rules.

#### Overall Evidence Strength (`evidence_strength` enum)

```
E1_DISEASE_SPECIFIC_CONFIRMATORY  ← PCR+, culture+, NAAT+, species-specific test
E2_HIGHLY_CHARACTERISTIC          ← Disease-specific serology, paired seroconversion
E3_SUPPORTIVE_NON_SPECIFIC        ← Compatible symptoms, nonspecific labs, imaging
E4_BACKGROUND_OR_CONTEXT_ONLY     ← Exposure, epidemiology, vaccine — no patient evidence
E0_CONTRADICTED                   ← Confirmatory test explicitly negative
```

Ask: *"Does this evidence discriminate the target disease from clinically
plausible alternatives?"* — not merely *"Is this compatible with the disease?"*

#### Structured Evidence Extraction (`step9_key_evidence`)

**CRITICAL REQUIREMENT:** `step9_key_evidence` MUST NOT be a list of free-text strings!
It MUST be a structured JSON object containing an array of grounded `evidence_items`:

```json
{{
  "evidence_items": [
    {{
      "source_field": "case_text",
      "start_char": {ex["start_char"]},
      "end_char": {ex["end_char"]},
      "source_quote": "{ex["source_quote"]}",
      "patient_anchor_id": "{ex["patient_anchor_id"]}",
      "test_name": "{ex["test_name"]}",
      "target_concept": "{ex["target_concept"]}",
      "specimen": "{ex["specimen"]}",
      "result": "{ex["result"]}",
      "temporality": "{ex["temporality"]}",
      "relation": "{ex["relation"]}",
      "strength": "{ex["strength"]}"
    }}
  ]
}}
```

#### Field Specifications for each item in `evidence_items`:

| Field | Type | Description | Allowed / Expected Values |
|---|---|---|---|
| `source_field` | string | Field from input record containing the evidence text | `"case_text"` |
| `start_char` | integer | 0-indexed character start offset in `source_field` (inclusive) | Integer >= 0 |
| `end_char` | integer | 0-indexed character end offset in `source_field` (exclusive) | Integer > `start_char` |
| `source_quote` | string | Exact verbatim text from source (`case_text[start_char:end_char]`) | Must match source text character-for-character |
| `patient_anchor_id` | string | Links evidence to patient entity identified in Step 3 | e.g. `"patient_1"`, `"patient_2"`, `"primary_patient"` |
| `test_name` | string | Diagnostic procedure, assay, lab test, or clinical finding | e.g. `"{ex["test_name"]}"`, `"RT-PCR"`, `"Culture"`, `"Serology"` |
| `target_concept` | string | Specific organism, pathogen, antigen, antibody, or disease concept | e.g. `"{ex["target_concept"]}"` |
| `specimen` | string / null | Biological specimen or anatomical site | e.g. `"{ex["specimen"]}"`, `"blood"`, `"serum"`, `"sputum"`, `"CSF"`, `null` |
| `result` | string | Test finding or laboratory qualitative/quantitative result | `"POSITIVE"`, `"NEGATIVE"`, `"DETECTED"`, `"NOT_DETECTED"`, `"REACTIVE"` |
| `temporality` | string | Temporality of this specific evidence item | `"CURRENT_EPISODE"`, `"RECENT_EPISODIC"`, `"HISTORICAL_PAST"`, `"UNKNOWN"` |
| `relation` | string | Relation to candidate disease diagnosis | `"SUPPORTS"`, `"REFUTES"`, `"INCONCLUSIVE"` |
| `strength` | string | Specificity tier of this individual evidence item | `"E1_CONFIRMATORY"`, `"E2_HIGHLY_SPECIFIC"`, `"E3_SUPPORTIVE"`, `"E4_CONTEXT"`, `"E0_CONTRADICTED"` |

#### Evidence Extraction Guidelines:
1. **Verbatim Text Grounding:** Every item MUST have an exact `source_quote` directly extracted from `case_text`. `case_text[start_char:end_char]` MUST equal `source_quote` character-for-character. Do not paraphrase or summarize inside `source_quote`.
2. **Positive Diagnosis Requirement:** For cases labeled `POSITIVE`, `evidence_items` must contain at least one item with `relation: "SUPPORTS"` and `strength` in `["E1_CONFIRMATORY", "E2_HIGHLY_SPECIFIC"]`.
3. **Negative / Ruled Out Evidence:** For cases labeled `NEGATIVE`, include item(s) documenting the negative test or definitive exclusion (`result: "NEGATIVE"`, `relation: "REFUTES"`, `strength: "E0_CONTRADICTED"`).
4. **Excluded / Non-Patient Cases:** If the document is an aggregate study (`EXCLUDED_NON_SINGLE_PATIENT`), animal study (`EXCLUDED_NON_HUMAN`), or homonym (`EXCLUDED_NON_TARGET_CASE`) where no patient clinical evidence exists, `evidence_items` may be empty (`"evidence_items": []`) or cite the study-type statement with `relation: "REFUTES"`.
5. **Multiple Evidence Items:** When multiple pieces of evidence exist (e.g. culture positive + serology high-titer + symptoms), annotate all relevant items in the `evidence_items` array in chronological or order-of-appearance sequence.

"""

    schema_replacement = f"""## Output Record Schema

Each annotated case must produce exactly this JSON structure:

```json
{{
  "pair_id": "PMC8639279_01::{primary_disease}",
  "case_id": "PMC8639279_01",
  "article_id": "PMC8639279",
  "target_disease": "{primary_disease}",

  "step1_document_type": "CLINICAL_CASE_REPORT",
  "step2_ccu_type": "PRIMARY_CARE_EPISODE",
  "step3_patient_anchor": {{
    "anchor_type": "PRIMARY_PATIENT",
    "age": 45.0,
    "gender": "Male",
    "coreference_notes": "Primary subject of case report"
  }},
  "step5_concept_grounding": "TARGET_CONFIRMED",
  "step6_assertion_type": "AFFIRMED",
  "step7_temporality": "CURRENT_ACTIVE",
  "step8_clinical_role": "PRIMARY_DIAGNOSIS",
  "step9_evidence_strength": "E1_DISEASE_SPECIFIC_CONFIRMATORY",
  "step9_key_evidence": {{
    "evidence_items": [
      {{
        "source_field": "case_text",
        "start_char": {ex["start_char"]},
        "end_char": {ex["end_char"]},
        "source_quote": "{ex["source_quote"]}",
        "patient_anchor_id": "{ex["patient_anchor_id"]}",
        "test_name": "{ex["test_name"]}",
        "target_concept": "{ex["target_concept"]}",
        "specimen": "{ex["specimen"]}",
        "result": "{ex["result"]}",
        "temporality": "{ex["temporality"]}",
        "relation": "{ex["relation"]}",
        "strength": "{ex["strength"]}"
      }}
    ]
  }},
  "step10_contradiction_flag": false,
  "step10_contradiction_notes": "",
  "step10_contradiction_resolution_status": null,
  "step11_vpd_satisfied": true,
  "step12_dataset_label": "POSITIVE",

  "failure_flags": [],
  "confidence": "HIGH",
  "rationale": "{ex["rationale"]}",
  "annotator_id": "disease-agent-{slug}",
  "annotation_version": "1.0"
}}
```

"""

    # Replace Step 9
    step9_pat = r"(### Step 9 — Evidence assessment.*?\n)(?=### Step 10 — Reconcile contradictions)"
    protocol = re.sub(step9_pat, step9_replacement, base_protocol, flags=re.DOTALL)

    # Replace Output Record Schema
    schema_pat = r"(## Output Record Schema.*?\n)(?=### Failure flags \(append when applicable\))"
    protocol = re.sub(schema_pat, schema_replacement, protocol, flags=re.DOTALL)

    return protocol


def build_disease_skill(
    slug: str,
    primary_disease: str,
    display_name: str,
    base_protocol: str,
    disease_evidence: str,
    cross_disease: str,
    universal_rule: str,
    ref_row: str,
    pool: str = "tier3_pool",
) -> str:
    ref_section = (
        f"## Primary Reference Source\n\n"
        f"| Disease | Primary source |\n"
        f"|---|---|\n"
        f"{ref_row}\n"
    ) if ref_row else ""

    tailored_protocol = format_disease_protocol(
        base_protocol=base_protocol,
        slug=slug,
        primary_disease=primary_disease,
        display_name=display_name,
    )

    return f"""---
name: disease-agent-{slug}
description: >
  Clinical annotation agent for {display_name}.
  Annotates cases from annotation_workdir/{pool}/input/input_{slug}.jsonl
  following the 12-step protocol with {display_name}-specific evidence rules
  from 03_evidence_specificity_matrix.md.
---

# Clinical Annotation Agent — {display_name}

## Your Assigned Disease

**Target disease:** `{primary_disease}`
**Input file:** `sandbox/workspace/{pool}/input/input_{slug}.jsonl`
**Output file:** `sandbox/workspace/{pool}/output/output_{slug}.jsonl`

---

## PART A — Disease-Specific Evidence Matrix

The following is the full evidence specification for **{display_name}**,
extracted from `sandbox/protocols/03_evidence_specificity_matrix.md`.

### Universal Claim Eligibility Rule

{universal_rule}

---

### {display_name}-Specific Evidence Rules

{disease_evidence}

---

{ref_section}

---

### Cross-Disease Rules (apply to all diseases)

{cross_disease}

---

## PART B — 12-Step Annotation Protocol

The following is the shared annotation protocol. Execute every step
in order for **every case** in your input file.

> [!CAUTION]
> **MANDATORY CLINICAL SEMANTIC REVIEW FOR {primary_disease.upper()} (REGEX STRICTLY FORBIDDEN):**
> 1. **NO REGEX / KEYWORD MATCHING SCRIPTS:** You are strictly forbidden from writing or using Python regex / string search scripts to automate annotations.
> 2. **DEEP CLINICAL READING:** You must read the narrative of every single case to perform nuanced medical reasoning across all 12 steps.
> 3. **GROUNDED ATTRIBUTION:** Every evidence item in `step9_key_evidence` must be grounded with exact character offsets (`start_char`, `end_char`) and verbatim `source_quote`.

{tailored_protocol}
"""


def main():
    parser = argparse.ArgumentParser(description="Generate 15 disease-specific SKILL.md files.")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print what would be written without creating files.")
    parser.add_argument("--pool", type=str, default="tier3_pool", choices=["tier3_pool", "labeled_pool"],
                        help="Target annotation pool (default: tier3_pool)")
    args = parser.parse_args()

    print("=" * 65)
    print("GENERATING 15 DISEASE-SPECIFIC SKILL.md FILES")
    print("=" * 65)
    if args.dry_run:
        print("  [DRY RUN — no files written]\n")

    # Load and parse matrix
    matrix_text = MATRIX_PATH.read_text(encoding="utf-8")
    sections, cross_disease, ref_rows, universal_rule = parse_matrix(matrix_text)
    print(f"  Matrix sections found: {len(sections)}")
    print(f"  Cross-disease sections extracted: {len(cross_disease.split('---'))}")
    print(f"  Reference rows parsed: {len(ref_rows)}")

    # Load base protocol
    base_protocol = load_base_skill()
    print(f"  Base protocol loaded: {len(base_protocol):,} chars\n")

    results = []
    for slug, primary_disease, matrix_header, ref_key in DISEASES:
        disease_evidence = extract_disease_section(sections, matrix_header)
        ref_row = ref_rows.get(ref_key, "")
        skill_content = build_disease_skill(
            slug=slug,
            primary_disease=primary_disease,
            display_name=primary_disease.replace("_", " "),
            base_protocol=base_protocol,
            disease_evidence=disease_evidence,
            cross_disease=cross_disease,
            universal_rule=universal_rule,
            ref_row=ref_row,
            pool=args.pool,
        )

        skill_dir  = SKILLS_DIR / f"disease-agent-{slug}"
        skill_path = skill_dir / "SKILL.md"
        size_kb    = len(skill_content) / 1024

        if not args.dry_run:
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_path.write_text(skill_content, encoding="utf-8")

        status = "[written]" if not args.dry_run else "[dry]"
        print(f"  {status}  {str(skill_path.relative_to(REPO_ROOT)):<60}  ({size_kb:.1f} KB)")
        results.append((slug, skill_path, size_kb))

    print(f"\n  Total: {len(results)} SKILL.md files")
    if not args.dry_run:
        print(f"  Location: {SKILLS_DIR.relative_to(REPO_ROOT)}/disease-agent-*/SKILL.md")


if __name__ == "__main__":
    main()

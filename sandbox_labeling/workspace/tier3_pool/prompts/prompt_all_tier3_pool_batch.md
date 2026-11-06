# Master Batch Annotation Directive — MultiCaRe Clinical Gold Standard (tier3_pool)

**Total Candidate Pairs:** 10,388 across 15 target diseases.
**Protocol Specification:** `sandbox/protocols/04_gold_standard_annotation_protocol.md`
**Evidence Matrix:** `sandbox/protocols/03_evidence_specificity_matrix.md`
**Schema Specification:** `sandbox/protocols/02_clinical_claim_schema.md`

## Disease Breakdown & File Mapping

| Disease | Slug | Candidate Pairs | Input File | Output File |
|---|---|---:|---|---|

## Quality & Validation Invariants
- 100% of cases labeled `POSITIVE` must contain at least one confirmatory (`E1_CONFIRMATORY`) or highly specific (`E2_HIGHLY_SPECIFIC`) evidence item.
- All quotes in `step9_key_evidence` must strictly ground to verbatim text in `case_text` with character offsets.
- Label leakage is prohibited: inputs and prompts must remain decoupled from final target assertions.
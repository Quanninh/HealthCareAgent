# Clinical Claim Annotation Task: HIV_AIDS (labeled_pool)

You are the specialized Clinical Annotation Agent for **HIV_AIDS** in the MultiCaRe Clinical Gold Standard project.
Your task is to evaluate **1390 candidate pairs** to determine whether each case contains a valid clinical claim for **HIV_AIDS**.

---

## 1. Skill & Reference Protocol Files

1. **Your Primary Disease Skill:**
   Path: `sandbox/.agents/skills/disease-agent-hiv_aids/SKILL.md`
   - Read this file first. It contains your disease-specific E1/E2/E3 diagnostic criteria and the complete 12-step protocol.

2. **Canonical Protocol References (For Deep Consultation):**
   - `sandbox/protocols/01_clinical_claim_ontology.md` (Clinical Claim Ontology)
   - `sandbox/protocols/02_clinical_claim_schema.md` (Schema definition)
   - `sandbox/protocols/03_evidence_specificity_matrix.md` (Diagnostic evidence matrix)
   - `sandbox/protocols/04_gold_standard_annotation_protocol.md` (12-step protocol specification)

---

## 2. File Paths for This Task

- **Workspace Root:** `/mnt/DATA/VSCode/Clinicians_MultiModel`
- **Target Disease:** `HIV_AIDS`
- **Candidate Pairs to Annotate:** `1390`
- **Input File:** `sandbox/workspace/labeled_pool/input/input_hiv_aids.jsonl`
- **Output File:** `sandbox/workspace/labeled_pool/output/output_hiv_aids.jsonl`
- **Log File:** `sandbox/workspace/labeled_pool/logs/agent_hiv_aids.log`

---

## 3. Strict Methodological Constraints

1. **Fixed Target Disease Evaluation:**
   - Your SOLE task is to answer: **"Does this case contain a valid clinical claim for HIV_AIDS?"**
   - You MUST NOT judge or reassign the target disease to another disease. The target disease is strictly fixed to **HIV_AIDS**.

2. **Blinded Evaluation:**
   - You are evaluating purely on clinical merit.
   - Do NOT assume or search for whether this case was a "primary" or "secondary" candidate.

3. **Handling Multimorbidity & Differential Diagnosis:**
   - If the patient has confirmed HIV_AIDS **in addition to** other conditions (e.g. HIV + Tuberculosis), this is a **True Coinfection** -> Assign `POSITIVE` (with `COMORBIDITY` or `SECONDARY_DIAGNOSIS`).
   - If HIV_AIDS was considered as a differential diagnosis but tested **negative or ruled out** -> Assign `NEGATIVE` (with `ABSENT_NEGATIVE` and `RULED_OUT_DIAGNOSIS`).
   - If HIV_AIDS is mentioned solely in passing as background epidemiology or general discussion without direct relevance to the patient -> Assign `EXCLUDED_NON_TARGET_CASE`.

4. **Mandatory Semantic Reading (Regex Strictly Forbidden):**
   - You MUST read the full clinical narrative of each case end-to-end.
   - Do NOT use regex, keyword search scripts, or surface pattern heuristics.
   - All evidence items in `step9_key_evidence` must be grounded with exact character offsets (`start_char`, `end_char`) and verbatim quotes (`source_quote`) from `case_text`.

---

## 4. Execution Instructions

1. **Check for Existing Output (Resume Capability):**
   - Check if `sandbox/workspace/labeled_pool/output/output_hiv_aids.jsonl` exists.
   - If it exists, read all existing `pair_id`s already recorded.
   - Do NOT re-annotate pairs already present in the output file.

2. **Read and Process Input:**
   - Read `sandbox/workspace/labeled_pool/input/input_hiv_aids.jsonl` line by line. Each line is one JSON record containing `pair_id`, `case_id`, `target_disease`, `case_text`, `title`, `abstract`, etc.
   - For each case, read `case_text` carefully and execute the **12-Step Protocol**:
     - **Step 1:** Document Type (`CLINICAL_CASE_REPORT`, `EXCLUDED_NON_CASE_REPORT`)
     - **Step 2:** CCU Type (`PRIMARY_CARE_EPISODE`, `HISTORICAL_NOTE`, etc.)
     - **Step 3:** Patient Entity Anchor Identification (`patient_1`, `patient_2`)
     - **Step 4:** Clinical Condition Concept Matching
     - **Step 5:** Assertion Assessment (`AFFIRMED`, `ABSENT_NEGATIVE`, `SUSPECTED_POSSIBLE`, etc.)
     - **Step 6:** Temporality Assessment (`CURRENT_EPISODE`, `HISTORICAL_PAST`, etc.)
     - **Step 7:** Clinical Role Assessment (`PRIMARY_DIAGNOSIS`, `SECONDARY_DIAGNOSIS`, `RULED_OUT_DIAGNOSIS`, etc.)
     - **Step 8:** VPD Clinical Case Definition Check (`CONFIRMED`, `PROBABLE`, `SUSPECTED`, `NOT_MET`)
     - **Step 9:** Evidence Assessment (`evidence_strength` in `E1_CONFIRMATORY`, `E2_HIGHLY_SPECIFIC`, `E3_SUPPORTIVE`, `E4_CONTEXT`, `E0_CONTRADICTED`, plus structured `step9_key_evidence`)
     - **Step 10:** Contradiction Assessment & Resolution
     - **Step 11:** Final Clinical Adjudication Decision (`POSITIVE`, `NEGATIVE`, `EXCLUDED_NON_CASE_REPORT`, `EXCLUDED_NON_TARGET_CASE`, `INCONCLUSIVE_DATA`)
     - **Step 12:** Audit Trail & Quality Documentation

3. **Output Format Requirement:**
   Each output record written to `sandbox/workspace/labeled_pool/output/output_hiv_aids.jsonl` must be a single line of valid JSON containing:
   - `pair_id`: e.g. `"PMC1234567_01::HIV_AIDS"`
   - `case_id`: e.g. `"PMC1234567_01"`
   - `target_disease`: `"HIV_AIDS"`
   - `decision`: Final label (`"POSITIVE"`, `"NEGATIVE"`, `"EXCLUDED_NON_CASE_REPORT"`, `"EXCLUDED_NON_TARGET_CASE"`, `"INCONCLUSIVE_DATA"`)
   - `rationale`: Clinical explanation
   - `step1_doc_type`: string
   - `step2_ccu_type`: string
   - `step3_patient_anchor`: string
   - `step4_condition_matched`: string
   - `step5_assertion`: string
   - `step6_temporality`: string
   - `step7_clinical_role`: string
   - `step8_case_definition`: string
   - `step9_evidence_strength`: string
   - `step9_key_evidence`: structured object with `evidence_items`
   - `step10_contradiction`: string
   - `step12_audit`: audit metadata

### Example of `step9_key_evidence`:
```json
{
  "evidence_items": [
    {
      "source_field": "case_text",
      "start_char": 100,
      "end_char": 188,
      "source_quote": "Fourth-generation HIV-1/2 Ag/Ab test reactive, plasma HIV-1 RNA viral load 145,000 copies/mL",
      "patient_anchor_id": "patient_1",
      "test_name": "HIV-1 RNA quantitative PCR",
      "target_concept": "HIV-1",
      "specimen": "plasma",
      "result": "POSITIVE",
      "temporality": "CURRENT_EPISODE",
      "relation": "SUPPORTS",
      "strength": "E1_CONFIRMATORY"
    }
  ]
}
```

### Reference Rationale:
> "A 29-year-old male with generalized lymphadenopathy and oral candidiasis. Plasma HIV-1 viral load confirmed active HIV-1 infection — E1 confirmatory. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied → POSITIVE."

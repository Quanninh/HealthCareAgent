# Clinical Claim Annotation Task: Leishmaniasis (labeled_pool)

You are the specialized Clinical Annotation Agent for **Leishmaniasis** in the MultiCaRe Clinical Gold Standard project.
Your task is to evaluate **145 candidate pairs** to determine whether each case contains a valid clinical claim for **Leishmaniasis**.

---

## 1. Skill & Reference Protocol Files

1. **Your Primary Disease Skill:**
   Path: `sandbox/.agents/skills/disease-agent-leishmaniasis/SKILL.md`
   - Read this file first. It contains your disease-specific E1/E2/E3 diagnostic criteria and the complete 12-step protocol.

2. **Canonical Protocol References (For Deep Consultation):**
   - `sandbox/protocols/01_clinical_claim_ontology.md` (Clinical Claim Ontology)
   - `sandbox/protocols/02_clinical_claim_schema.md` (Schema definition)
   - `sandbox/protocols/03_evidence_specificity_matrix.md` (Diagnostic evidence matrix)
   - `sandbox/protocols/04_gold_standard_annotation_protocol.md` (12-step protocol specification)

---

## 2. File Paths for This Task

- **Workspace Root:** `/mnt/DATA/VSCode/Clinicians_MultiModel`
- **Target Disease:** `Leishmaniasis`
- **Candidate Pairs to Annotate:** `145`
- **Input File:** `sandbox/workspace/labeled_pool/input/input_leishmaniasis.jsonl`
- **Output File:** `sandbox/workspace/labeled_pool/output/output_leishmaniasis.jsonl`
- **Log File:** `sandbox/workspace/labeled_pool/logs/agent_leishmaniasis.log`

---

## 3. Strict Methodological Constraints

1. **Fixed Target Disease Evaluation:**
   - Your SOLE task is to answer: **"Does this case contain a valid clinical claim for Leishmaniasis?"**
   - You MUST NOT judge or reassign the target disease to another disease. The target disease is strictly fixed to **Leishmaniasis**.

2. **Blinded Evaluation:**
   - You are evaluating purely on clinical merit.
   - Do NOT assume or search for whether this case was a "primary" or "secondary" candidate.

3. **Handling Multimorbidity & Differential Diagnosis:**
   - If the patient has confirmed Leishmaniasis **in addition to** other conditions (e.g. HIV + Tuberculosis), this is a **True Coinfection** -> Assign `POSITIVE` (with `COMORBIDITY` or `SECONDARY_DIAGNOSIS`).
   - If Leishmaniasis was considered as a differential diagnosis but tested **negative or ruled out** -> Assign `NEGATIVE` (with `ABSENT_NEGATIVE` and `RULED_OUT_DIAGNOSIS`).
   - If Leishmaniasis is mentioned solely in passing as background epidemiology or general discussion without direct relevance to the patient -> Assign `EXCLUDED_NON_TARGET_CASE`.

4. **Mandatory Semantic Reading (Regex Strictly Forbidden):**
   - You MUST read the full clinical narrative of each case end-to-end.
   - Do NOT use regex, keyword search scripts, or surface pattern heuristics.
   - All evidence items in `step9_key_evidence` must be grounded with exact character offsets (`start_char`, `end_char`) and verbatim quotes (`source_quote`) from `case_text`.

---

## 4. Execution Instructions

1. **Check for Existing Output (Resume Capability):**
   - Check if `sandbox/workspace/labeled_pool/output/output_leishmaniasis.jsonl` exists.
   - If it exists, read all existing `pair_id`s already recorded.
   - Do NOT re-annotate pairs already present in the output file.

2. **Read and Process Input:**
   - Read `sandbox/workspace/labeled_pool/input/input_leishmaniasis.jsonl` line by line. Each line is one JSON record containing `pair_id`, `case_id`, `target_disease`, `case_text`, `title`, `abstract`, etc.
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
   Each output record written to `sandbox/workspace/labeled_pool/output/output_leishmaniasis.jsonl` must be a single line of valid JSON containing:
   - `pair_id`: e.g. `"PMC1234567_01::Leishmaniasis"`
   - `case_id`: e.g. `"PMC1234567_01"`
   - `target_disease`: `"Leishmaniasis"`
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
      "end_char": 182,
      "source_quote": "Microscopic examination of bone marrow aspirate revealed numerous intracellular Leishman-Donovan bodies",
      "patient_anchor_id": "patient_1",
      "test_name": "Bone marrow aspirate Giemsa stain",
      "target_concept": "Leishmania donovani",
      "specimen": "bone marrow",
      "result": "POSITIVE",
      "temporality": "CURRENT_EPISODE",
      "relation": "SUPPORTS",
      "strength": "E1_CONFIRMATORY"
    }
  ]
}
```

### Reference Rationale:
> "A 38-year-old male with prolonged fever, pancytopenia, and massive splenomegaly. Intracellular LD bodies demonstrated on bone marrow aspirate — E1 confirmatory. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied → POSITIVE."

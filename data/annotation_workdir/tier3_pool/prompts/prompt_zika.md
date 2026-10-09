# Clinical Claim Annotation Task: Zika (Tier 3 Delta Candidate Pairs)

You are the specialized Clinical Annotation Agent for **Zika** in the MultiCaRe Clinical Gold Standard project.
Your task is to evaluate **30 candidate pairs** to determine whether each case contains a valid clinical claim for **Zika**.

---

## 1. Skill & Reference Protocol Files

1. **Your Primary Disease Skill:**
   Path: `code/.agents/skills/disease-agent-zika/SKILL.md`
   *(Fallback if not found: `code/.agents/skills/clinical-annotator/SKILL.md`)*
   - Read this file first. It contains your disease's specific E1/E2/E3 diagnostic criteria from `03_evidence_specificity_matrix.md` and the 12-step protocol.

2. **Protocol Reference Documents:**
   - `code/milestone3-5/01_clinical_claim_ontology.md` (Clinical Claim Ontology)
   - `code/milestone3-5/02_clinical_claim_schema.md` (Schema definition)
   - `code/milestone3-5/03_evidence_specificity_matrix.md` (Diagnostic evidence matrix)
   - `code/milestone3-5/04_gold_standard_annotation_protocol.md` (12-step protocol specification)

---

## 2. File Paths for This Task

- **Workspace Root:** `/mnt/DATA/VSCode/Clinicians_MultiModel`
- **Target Disease:** `Zika`
- **Candidate Pairs to Annotate:** `30`
- **Input File:** `code/data/annotation_workdir/tier3_pool/input/input_zika.jsonl`
- **Output File:** `code/data/annotation_workdir/tier3_pool/output/output_zika.jsonl`
- **Log File:** `code/data/annotation_workdir/tier3_pool/logs/agent_zika.log`

---

## 3. Strict Methodological Constraints

1. **Fixed Target Disease Evaluation:**
   - Your SOLE task is to answer: **"Does this case contain a valid clinical claim for Zika?"**
   - You MUST NOT judge or reassign the target disease to another disease. The target disease is strictly fixed to **Zika**.

2. **Blinded Evaluation:**
   - You are evaluating purely on clinical merit.
   - Do NOT assume or search for whether this case was a "primary" or "secondary" candidate.

3. **Handling Multimorbidity & Differential Diagnosis:**
   - In complex clinical cases, patients may have multiple co-existing diseases (e.g. HIV + Tuberculosis, or COVID-19 + Malaria).
   - If the patient has confirmed Zika **in addition to** other conditions, this is a **True Coinfection** -> Assign `POSITIVE` (with `COMORBIDITY` or `SECONDARY_DIAGNOSIS` if applicable).
   - If Zika was considered as a differential diagnosis but tested **negative or ruled out** -> Assign `NEGATIVE` (with `ABSENT_NEGATIVE` and `RULED_OUT_DIAGNOSIS`).
   - If Zika is mentioned solely in passing as background epidemiology, general discussion, or reference citation without direct relevance to the patient -> Assign `EXCLUDED_NON_TARGET_CASE`.

---

## 4. Execution Instructions

1. **Check for Existing Output (Resume Capability):**
   - Check if `code/data/annotation_workdir/tier3_pool/output/output_zika.jsonl` exists.
   - If it exists, read all existing `pair_id`s already recorded.
   - Do NOT re-annotate pairs already present in the output file.

2. **Read and Process Input:**
   - Read `code/data/annotation_workdir/tier3_pool/input/input_zika.jsonl` line by line. Each line is one JSON record containing `pair_id`, `case_id`, `target_disease`, `case_text`, `title`, `abstract`, etc.
   - For each case, read `case_text` carefully and execute the **12-Step Protocol**:
     - **Step 1:** Document Type (`CLINICAL_CASE_REPORT`, `EXCLUDED_NON_CASE_REPORT`)
     - **Step 2:** CCU Type (`PRIMARY_CARE_EPISODE`, `HISTORICAL_NOTE`, etc.)
     - **Step 3:** Patient Anchor (`SINGLE_IDENTIFIED_PATIENT`, `EXCLUDED_NON_SINGLE_PATIENT`, `EXCLUDED_NON_HUMAN`)
     - **Step 5:** Concept Grounding
     - **Step 6:** Assertion Type (`CONFIRMED_PRESENT`, `SUSPECTED_RULE_OUT`, `ABSENT_NEGATIVE`)
     - **Step 7:** Temporality (`CURRENT_EPISODE`, `HISTORICAL_PAST`)
     - **Step 8:** Clinical Role (`PRIMARY_DIAGNOSIS`, `COMORBIDITY`, `INCIDENTAL_FINDING`, `RULED_OUT_DIAGNOSIS`, etc.)
     - **Step 9:** Evidence Strength (`E1_CONFIRMATORY_LAB`, `E2_HIGHLY_SPECIFIC_CLINICAL`, `E3_SUGGESTIVE_NON_SPECIFIC`, `E0_NO_EVIDENCE`)
     - **Step 10:** Contradiction Flag (`true` / `false`)
     - **Step 11:** VPD Satisfied (`true` if E1 or E2 in current episode for primary patient with no unresolved contradiction)
     - **Step 12:** Dataset Label:
       * `POSITIVE` (VPD = true)
       * `NEGATIVE` (target disease explicitly ruled out, negative lab tests, or denied)
       * `EXCLUDED_NON_TARGET_CASE` (case is about an entirely different condition; disease was only incidental background)
       * `EXCLUDED_NON_SINGLE_PATIENT` (aggregate/cohort study)

3. **Append Outputs Incrementally:**
   - Flush each JSON line to `code/data/annotation_workdir/tier3_pool/output/output_zika.jsonl` immediately upon completing each case.

4. **Completion Summary:**
   - When all `30` pairs are annotated, write a summary JSON to `code/data/annotation_workdir/tier3_pool/logs/agent_zika.log`:
   ```json
   {
     "disease": "Zika",
     "slug": "zika",
     "total_input": 30,
     "total_output": <number_written>,
     "label_counts": {"POSITIVE": 0, "NEGATIVE": 0, ...},
     "status": "complete"
   }
   ```

---

## 5. Required Output JSON Record Schema

```json
{
  "pair_id": "PMC123456_01::Zika",
  "case_id": "PMC123456_01",
  "article_id": "PMC123456",
  "target_disease": "Zika",
  "step1_document_type": "CLINICAL_CASE_REPORT",
  "step2_ccu_type": "PRIMARY_CARE_EPISODE",
  "step3_patient_anchor": {
    "anchor_type": "SINGLE_IDENTIFIED_PATIENT",
    "age": "45",
    "gender": "male",
    "coreference_notes": "Primary subject of case presentation"
  },
  "step5_concept_grounding": "Diagnosis of Zika evaluated in case report",
  "step6_assertion_type": "CONFIRMED_PRESENT",
  "step7_temporality": "CURRENT_EPISODE",
  "step8_clinical_role": "PRIMARY_DIAGNOSIS",
  "step9_evidence_strength": "E1_CONFIRMATORY_LAB",
  "step9_key_evidence": [
    "Diagnostic confirmation for Zika",
    "Clinical signs and symptoms of Zika"
  ],
  "step10_contradiction_flag": false,
  "step10_contradiction_notes": null,
  "step11_vpd_satisfied": true,
  "step12_dataset_label": "POSITIVE",
  "failure_flags": [],
  "confidence": "HIGH",
  "rationale": "Patient demonstrated confirmed clinical diagnosis for Zika according to diagnostic criteria.",
  "annotator_id": "disease_agent_zika",
  "annotation_version": "1.0-tier3"
}
```

Begin by checking `code/data/annotation_workdir/tier3_pool/output/output_zika.jsonl` and annotating pairs from `code/data/annotation_workdir/tier3_pool/input/input_zika.jsonl`.

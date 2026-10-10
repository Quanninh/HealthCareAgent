# Clinical NLP Pipeline: Verification and Multi-Label Diagnosis

This document outlines the end-to-end architecture of the medical pipeline. The system acts as a robust safety net, taking potentially messy extractions from an LLM and filtering them down to mathematically verified clinical facts, before diagnosing the patient using an interpretable, rule-based Snorkel architecture.

---

## Step 1: Ontology Grounding (MedCAT)

**The Goal:** Standardize medical language.
When an LLM reads a chart, it might extract `"trouble breathing"`, `"short of breath"`, or `"dyspnea"`. This step standardizes all of these into a single machine-readable ID.

**How it works:**
1. The pipeline iterates over every `text_span` extracted by the LLM.
2. It passes the full sentence context into the **MedCAT UMLS Model**.
3. MedCAT searches its internal dictionary to find the best matching medical concept.

**The Output:**
Each entity is enriched with an `ontology_mapping` object containing the universal ID (`umls_cui`) and the official medical term (`standard_name`).

---

## Step 2: Weak Supervision Fact-Checking (Snorkel Stage 1)

**The Goal:** Filter out hallucinations, negations, and irrelevant context.
Even if a symptom is extracted perfectly, it doesn't mean the patient actually has it. The LLM might have extracted a symptom that belongs to a family member, or one that was explicitly ruled out. This step proves if the entity is an active problem for the patient.

**How it works:**
The pipeline uses **Snorkel** to run a suite of 6 independent "Labeling Functions" (LFs). Each LF acts as a juror, voting on whether the entity is `VALID` or `INVALID`.

### The 6 Independent Jurors:
1.  **`lf_regex_negation`**: Scans the raw doctor's note for phrases like *"rules out [disease]"* or *"denies [disease]"*. 
2.  **`lf_llm_assertion`**: Checks the LLM's own context tag. If tagged as `"negated"`, votes `INVALID`.
3.  **`lf_experiencer_filter`**: Checks if the LLM tagged the entity as belonging to `"family_member"`.
4.  **`lf_temporality_filter`**: Checks if the LLM tagged the entity as `"historical"`.
5.  **`lf_medcat_validation`**: Checks the MedCAT output. If `"Unmapped"`, it assumes the LLM hallucinated a non-medical word.
6.  **`lf_raw_text_check`**: If the exact `text_span` the LLM extracted does not exist character-for-character in the raw doctor's note, votes `INVALID`.

### The Threshold Routing
Snorkel calculates a **Probability Score** (0.0 to 1.0) representing its mathematical confidence that the entity is a true, active problem.
*   **Confidence >= 0.85:** Routed to the **AUTO-ACCEPTED** queue. Passed to Stage 2.
*   **Confidence < 0.85:** Routed to a **HUMAN REVIEW** queue, preventing the AI from making a dangerous medical guess.

---

## Step 3 (Stage 2): Multi-Label Disease Diagnosis

**The Goal:** Predict the final diagnoses based *only* on the verified clinical facts, supporting comorbidities (patients having multiple diseases at once).

**The Architectural Improvement:**
Instead of a single multi-class model that forces diseases to compete against each other, the new Stage 2 architecture utilizes **15 Independent Binary Classifiers**. This multi-label approach allows the pipeline to accurately diagnose co-infections (e.g., a patient having both COVID-19 and Dengue).

**How it works:**
1. **The Clean Input:** Stage 2 takes *only* the verified symptoms (Auto-Accepted + Human Approved).
2. **The Dynamic LF Factory:** For each of the 15 diseases, the pipeline dynamically generates 4 specialized Labeling Functions based on the `disease_taxonomy.json` profiles:
   * **`lf_hallmarks`**: Votes `POSITIVE` if highly specific pathognomonic signs are present.
   * **`lf_lab_confirmation`**: Votes `POSITIVE` if specific gold-standard lab tests are recorded.
   * **`lf_constellation`**: Votes `POSITIVE` if generic systemic symptoms (fever, fatigue) co-occur with a specific hallmark.
   * **`lf_negative_test`**: Votes `NEGATIVE` if a definitive exclusion or negative lab test is found.
3. **The 15 LabelModels:** Snorkel trains 15 separate binary models to evaluate the overlapping and conflicting votes of these specialized LFs.
4. **The Final Output:** The pipeline outputs 15 independent probability scores per patient, safely identifying the top diagnosis and flagging any concurrent diseases.

---

## How to Run the Pipeline
Run the pipeline in two stages to allow for manual review of ambiguous entities.

**1. Run Stage 1 (Verification):**
```bash
python3 stage1_verification.py
```
*Outputs:* `accepted_entities.json` (auto-approved) and `human_review_queue.json` (requires review).

**2. Manual Review:**
Open `human_review_queue.json` in a text editor. For any valid entity, change `"expert_decision": "PENDING"` to `"APPROVED"`.

**3. Run Stage 2 (Diagnosis):**
```bash
python3 stage2_diagnosis.py
```
*Stage 2 will automatically detect and load your `"APPROVED"` entities alongside the auto-accepted ones to make its final diagnosis.*

### Evaluation
To evaluate the pipeline's predictions against the hand-annotated gold standards:
```bash
python3 evaluate_pipeline.py
```

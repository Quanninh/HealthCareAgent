# Clinical NLP Pipeline: Entity Verification Architecture

This document outlines the architecture of **Step 3** and **Step 4** of the medical pipeline. Together, these steps act as a robust safety net, taking messy and potentially hallucinated extractions from an LLM and filtering them down to mathematically verified clinical facts.

---

## Step 3: Ontology Grounding (MedCAT)

**The Goal:** Standardize medical language.
When an LLM reads a chart, it might extract `"trouble breathing"`, `"short of breath"`, or `"dyspnea"`. Step 3 standardizes all of these into a single machine-readable ID.

**How it works:**
1. The pipeline iterates over every `text_span` extracted by the LLM in Step 2.
2. It passes the raw string into the **MedCAT UMLS Model**.
3. MedCAT searches its internal dictionary to find the best matching medical concept.

**The Output:**
Each entity is enriched with an `ontology_mapping` object containing:
*   `umls_cui`: The universal ID (e.g., `C0013404`).
*   `standard_name`: The official medical term (e.g., `"Dyspnea"`).
*   `status`: Either `"Mapped"` or `"Unmapped"`.

---

## Step 4: Weak Supervision Fact-Checking (Snorkel Stage 1)

**The Goal:** Filter out hallucinations, negations, and irrelevant context.
Even if a disease is extracted perfectly, it doesn't mean the patient actually has it. The LLM might have extracted a disease that belongs to the patient's father, or a disease that was explicitly ruled out by the doctor. Step 4 mathematically proves if the entity is an active problem for the patient.

**How it works:**
The pipeline uses **Snorkel** to run a suite of 6 independent "Labeling Functions" (LFs). Each LF acts as a juror, voting on whether the entity is `VALID` or `INVALID`.

### The 6 Independent Jurors:
1.  **`lf_regex_negation`**: Scans the raw doctor's note for phrases like *"rules out [disease]"* or *"denies [disease]"*. If found, votes `INVALID`.
2.  **`lf_llm_assertion`**: Checks the LLM's own context tag. If the LLM tagged it as `"negated"`, votes `INVALID`.
3.  **`lf_experiencer_filter`**: Checks if the LLM tagged the entity as belonging to `"family_member"`. If so, votes `INVALID`.
4.  **`lf_temporality_filter`**: Checks if the LLM tagged the entity as `"historical"`. If so, votes `INVALID`.
5.  **`lf_medcat_validation`**: Checks the output from Step 3. If MedCAT returned `"Unmapped"`, it assumes the LLM hallucinated a non-medical word and votes `INVALID`.
6.  **`lf_raw_text_check`**: A strict safety check. If the exact `text_span` the LLM extracted does not exist character-for-character in the raw doctor's note, votes `INVALID`.

### The Snorkel LabelModel
Instead of relying on a single IF-statement, Snorkel trains a `LabelModel` that evaluates how often these 6 jurors agree or conflict with each other. 

**The Output:**
Snorkel outputs a single **Probability Score** (from 0.0 to 1.0) representing its mathematical confidence that the entity is a true, active problem.

---

## Step 5: Threshold Routing

The output from Snorkel (Step 4) is used to safely route the data:
*   **Confidence > 0.85:** The entity is routed to the **AUTO-ACCEPTED** queue. It is proven to be true and passed to Stage 2 for final disease diagnosis.
*   **Confidence < 0.85:** The LFs conflicted (e.g., the LLM said it was affirmed, but the regex found a negation). The entity is safely routed to a **HUMAN REVIEW** queue, preventing the AI from making a dangerous medical guess.

## Step 6 (Stage 2): Disease Prediction (Architectural Improvement)

**The Goal:** Predict the final patient diagnosis based *only* on the verified clinical facts, completely bypassing the need for an expensive external LLM API.

**The Architectural Improvement:**
Initially, predicting a final disease required sending the patient's verified symptoms out to a massive third-party LLM (like OpenAI or Hugging Face) and asking it to judge the diagnosis. This approach was slow, expensive, and relied on a "Black Box" model that was hard to interpret. 

The new Stage 2 architecture improves upon this by replacing the external LLM entirely with a **Second Snorkel Model (Multiclass Classification)** running locally.

**How it works:**
1. **The Clean Input:** Stage 2 takes *only* the `AUTO-ACCEPTED` entities from Step 5. It completely ignores anything that Snorkel rejected in Stage 1. 
2. **The Diagnosticians (LFs):** 15 new Labeling Functions are introduced—one for each possible disease (e.g., `lf_diagnose_covid`, `lf_diagnose_dengue`). These LFs act as specialized doctors. They look at the clean list of symptoms for a patient and cast a vote if the patient's symptoms match their specific disease profile.
3. **The Multi-Class LabelModel:** Snorkel evaluates the overlapping and conflicting votes between the 15 LFs (e.g., if a patient has a fever, both the Dengue LF and COVID LF might vote). Snorkel uses statistical analysis to weigh the true accuracy of those conflicting votes.
4. **The Final Output:** Snorkel generates a final probability matrix for all 15 diseases. The pipeline simply picks the disease with the highest confidence score (`argmax`) as the final prediction.

**Why this is the ultimate design:**
This **"Two-Stage Cascade"** provides 100% transparency. If the AI diagnoses a patient with COVID-19, a doctor can instantly trace the reasoning back through Stage 2 (which specific LFs voted for it) all the way down to Stage 1 (exactly which words in the raw text were mathematically verified). It turns disease prediction into a fast, cheap, and fully interpretable mathematical process!

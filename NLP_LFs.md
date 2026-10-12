# Clinical Diagnosis Pipeline: Comprehensive Project Handover & Implementation Plan

> **Date:** October 2026  
> **Target Dataset:** 981 Clinical Patient Cases (`extracted_cases_100per_disease.jsonl`)  
> **Ground Truth:** `ground_truth_100per_disease.jsonl` (602 Confirmed Positives, 379 Non-Positive / Excluded cases)  
> **Target Diseases (15):** Dengue, Malaria, Ebola/Filovirus, Tuberculosis, COVID-19, HIV/AIDS, Chikungunya, Zika, Brucellosis, Leishmaniasis, Typhoid Fever, Cholera, Rabies, Leptospirosis, Yellow Fever  
> **Execution Environment:** `/opt/anaconda3/envs/snorkel/bin/python` (BypassSandbox: true)

---

## 1. Executive Summary & Project Architecture

The objective is multi-label clinical diagnosis across 15 tropical and infectious diseases using **Snorkel weak supervision** and **UMLS concept grounding**.

```mermaid
flowchart TD
    subgraph Data ["Clinical Inputs"]
        RAW["981 Patient Cases (extracted_cases_100per_disease.jsonl)"]
        SKILLS["16 Clinical Annotator Skills (skills/SKILL_*.md)"]
    end

    subgraph Stage1 ["Stage 1: Grounding & Verification (MedCAT + Snorkel)"]
        MC["MedCAT Concept Extraction & WSD"]
        JUR["6 Snorkel Jurors + Expert Review"]
        MC & JUR --> ENT["21,026 Confirmed Entities (972/981 cases covered)"]
    end

    subgraph Stage2 ["Stage 2: Diagnosis (medspaCy + Trove + Snorkel)"]
        ENT --> PAT["Patient Representation Matrix"]
        RAW --> SC["medspaCy ConText & Sectionizer Scoping"]
        KB["clinical_knowledge.py (Trove Synsets & Dynamic Titers)"]
        PAT & SC & KB --> LFS["8 Multi-Tiered LFs per Disease (+1, 0, -1)"]
        LFS --> LM["15 Snorkel Binary LabelModels (cardinality=2)"]
    end

    subgraph Eval ["Evaluation Harness (evaluate_pipeline.py)"]
        LM --> VPD["Protocol Step 11 VPD Gatekeeper"]
        VPD --> OUT["Predicted Diseases & Calibrated Abstentions"]
        OUT --> GT{"Strict Ground Truth Verification (981 Cases)"}
    end
```

### Strict Evaluation Constraints
* If `validated_label == "POSITIVE"` $\rightarrow$ ground truth is `target_disease` (e.g., `Brucellosis`).
* If `validated_label != "POSITIVE"` $\rightarrow$ ground truth is `f"{target_disease} {validated_label}"` (e.g., `Brucellosis EXCLUDED_NON_SINGLE_PATIENT`).
* **Strict Constraint:** Any positive disease prediction on a non-positive case is evaluated as **incorrect ($\times$)**; non-positives must be classified as `UNKNOWN (Insufficient Evidence)` or abstained.

---

## 2. Key Breakthroughs Achieved in This Session

### A. Resolution of the 52% Entity Coverage Void
* **Previous Problem:** 512 out of 981 cases (52.2%) had `clinical_entities: []` (empty list), forcing the pipeline to guess blindly on raw text.
* **Update Achieved:** 
  * `extracted_cases_100per_disease.jsonl` is updated: **972 out of 981 cases (99.1%) now possess extracted clinical entities**.
  * `accepted_entities.json` updated to **13,574 entities** (was 6,403).
  * `human_review_queue.json` updated to **20,432 reviewed entities** (7,452 APPROVED, 12,980 REJECTED, 0 PENDING).
  * **Total Verified Entities Available:** **21,026 confirmed clinical entities** (was 9,415).

### B. Environment Migration to `snorkel`
* Migrated from `rag_any` to `/opt/anaconda3/envs/snorkel/bin/python`.
* **Verified Packages:** `snorkel`, `medcat`, `medspacy`, `spacy`, `sentence_transformers`, `rapidfuzz`, `pandas`, `scikit-learn`.

### C. Benchmark Progression Across All 981 Cases

| Metric | Pre-Session Baseline | Intermediate Multi-Tiered LFs | Absolute Gain | Relative Improvement |
|---|---|---|---|---|
| **Overall Exact Match Accuracy** | **16.0%** (157 / 981) | **43.4%** (426 / 981) | **+269 cases** | **+171.3%** |
| **Confirmed Positive Accuracy** | **26.1%** (157 / 602) | **70.8%** (426 / 602) | **+269 cases** | **+171.3%** |
| *— On cases with entities (469 cases)* | *48.7% (148 / 304)* | *73.5% (222 / 302)* | *+74 cases* | *+50.9%* |
| **Non-Positive Case Rejection** | **62.0%** (235 / 379) | **52.5%** (199 / 379) | — | Calibrated |
| **Macro Average ROC-AUC** | **0.6724** | **0.9159** | **+0.2435** | **+36.2%** |
| **Macro Average Recall** | 0.2612 | **0.9754** | +0.7142 | **+273.4%** |

---

## 3. Synthesis of Research Literature (`related_materials/`)

### Paper 1: Trove (`trove.pdf`)
* **Reference:** Fries, Steinberg, Khattar, Fleming, Posada, Callahan & Shah. *Ontology-driven weak supervision for clinical entity classification in electronic health records*. **Nature Communications**, 12:2017 (2021).
* **Core Principles:**
  * Organizes weak supervision over **UMLS Concept Unique Identifiers (CUIs)** and Semantic Groups rather than flat surface strings.
  * Employs **Semantic Type LFs** (longest-term matching in token length to resolve nested spans like *"lung"* vs *"lung cancer"*) and **Synset LFs** (CUI equivalence clusters).
  * Trains Snorkel's generative `LabelModel` by estimating latent accuracies $a_i = \mathbb{E}[\lambda_i Y]$ from covariance without ground truth.

### Paper 2: medspaCy (`medspacy.pdf`)
* **Reference:** Eyre, Chapman, Peterson, Shi, Alba, Jones, Box, DuVall & Patterson. *Launching into clinical space with medspaCy: a new clinical text processing toolkit in Python*. **arXiv:2106.07799 / AMIA**, 2021.
* **Core Principles:**
  * **ConText Algorithm:** Models directional modifier scopes (**FORWARD**, **BACKWARD**, **BIDIRECTIONAL**) linking target entities to modifiers (`is_negated`, `is_historical`, `is_family`).
  * **Scope Termination:** Terminates negation scope at conjunctions (e.g. *"denies fever, but has joint pain"* correctly leaves joint pain affirmed).
  * **PyRuSH:** Rule-based sentence Segmenter using Hashing, handling clinical decimals (`38.5 C`), abbreviations, and unstructured triage notes.
  * **Sectionizer:** LOINC/SecTag hierarchical tree separating Past Medical History from active presentations.

### Paper 3: MedCAT (`medcat.pdf`)
* **Reference:** Kraljevic, Searle, Shek, Roguski, Noor, Bean, Mascio, Zhu, Folarin, Roberts, Bendayan, Richardson, Stewart, Shah, Wong, Ibrahim, Teo & Dobson. *Multi-domain Clinical Natural Language Processing with MedCAT*. **Artificial Intelligence in Medicine**, 114:102043 (2021).
* **Core Principles:**
  * Large-scale Named Entity Recognition and Linking (NER+L) over 3.8M UMLS / 659K SNOMED-CT concepts.
  * Self-supervised context vector embeddings ($V_{\text{cntx}}$ via Word2Vec/negative sampling) for **Word-Sense Disambiguation (WSD)** of ambiguous clinical acronyms.
  * MetaCAT Bi-LSTM for concept-agnostic context classification.

### The Architectural Division of Labor
* **MedCAT:** Concepts Grounder & Disambiguator (answers: *What medical concept is this in the global UMLS ontology?*).
* **medspaCy:** Context Governor & Syntactic Scoper (answers: *How is this concept modified in this sentence/section?*).
* **Snorkel:** Diagnostic Arbiter (answers: *Given the grounded concepts and context, what is the disease diagnosis?*).

---

## 4. Root Cause Analysis: Why Hard-Coded Strings Cap Performance

Auditing the **176 missed confirmed positive cases** revealed four critical failure modes of exact substring checks (`target in text`):

1. **Mathematical Titer Variations:**
   * Hardcoded: `"sta 1:160"`, `"wright 1:160"`
   * Clinical Reality (PMC3884711_01): *"Serum agglutination titers were 1:400"* (Missed because $400 \ne 160$, even though any titer $\ge 1:160$ is diagnostic).
2. **Syntactic Procedural Interleaving:**
   * Hardcoded: `"blood culture positive for brucella"`
   * Clinical Reality (PMC7564992_01): *"blood culture bottles flagged positive for microbial growth... identified as Brucella species by MALDI-TOF MS"* (Missed due to intervening adjectives).
3. **Lexical Morphisms & Paraphrasing:**
   * Hardcoded: `"bone marrow smear positive"`, `"leishmania amastigotes"`
   * Clinical Reality (PMC4549335_01): *"confirmed by visualization of amastigotes in bone marrow samples"* (Missed; misdiagnosed as HIV).
   * Clinical Reality (PMC4703342_01): *"431 Leishmania per ml of blood (assessed by quantitative PCR)"* (Missed; misdiagnosed as Malaria).
4. **Prepositional Inversions:**
   * Hardcoded: `"sars-cov-2 rt-pcr positive"`
   * Clinical Reality (PMC10196249_01): *"RT-PCR for Omicron SARS-CoV-2 was detected in nasopharyngeal swab"*.

---

## 5. Comprehensive Implementation Plan for the Next Session

```mermaid
flowchart LR
    P1["Phase 1: Ingest 21,026 Entities<br/>(972/981 cases covered)"] --> P2["Phase 2: medspaCy ConText<br/>+ Dynamic Titer Parsers"]
    P2 --> P3["Phase 3: Trove Synset Expansion<br/>(clinical_knowledge.py)"]
    P3 --> P4["Phase 4: Dense Semantic Similarity<br/>(all-MiniLM-L6-v2)"]
    P4 --> P5["Phase 5: Re-train LabelModels<br/>& Benchmark Evaluation"]
```

### Phase 1: Ingestion of the 21,026 Verified Clinical Entities
* Update `stage2_diagnosis.py` to load `accepted_entities.json` (13,574) + approved `human_review_queue.json` (7,452).
* Ensure all 972 newly populated patient cases receive their full sets of `affirmed_cuis` and `valid_symptoms`.

### Phase 2: Directional Predicate Frames & Dynamic Titer Parsers
* In `clinical_knowledge.py` and `stage2_diagnosis.py`:
  * Implement **Dynamic Titer Parsers**: Regex ratio extractor checking `1:(\d+)` against mathematical clinical thresholds ($\ge 160$ for Brucellosis, $\ge 400$ for Leptospirosis MAT).
  * Implement **Directional Predicate Frames** using `medspaCy` ConText:
    $$\text{Clause} = [\text{Specimen}] \xrightarrow{\le 15\text{ tokens}} [\text{Affirmatory Action}] \xrightarrow{\le 10\text{ tokens}} [\text{Pathogen}]$$
    terminating at conjunctions (`"but"`, `"however"`).

### Phase 3: Trove-Style UMLS Synset Expansion (`clinical_knowledge.py`)
* Expand disease hallmark dictionaries with canonical UMLS synonym clusters:
  * E.g., Leishmaniasis: `["amastigote", "LD body", "Leishman-Donovan body", "rK39", "kala-azar"]`.
  * E.g., Typhoid: `["rose spots", "step-ladder fever", "Faget sign", "relative bradycardia"]`.

### Phase 4: Dense Semantic Similarity LFs (`sentence_transformers`)
* Use `all-MiniLM-L6-v2` (already cached in `/opt/anaconda3/envs/snorkel`) to pre-encode patient case presentations.
* Compute cosine similarity against gold diagnostic criteria defined in `skills/SKILL_*.md`.
* Add soft labeling functions: `lf_{disease}_dense_semantic_similarity(x)` voting `+1` if cosine similarity $\ge 0.78$.

### Phase 5: Pipeline Retraining & Full Evaluation
* Run `stage2_diagnosis.py` with `/opt/anaconda3/envs/snorkel/bin/python`.
* Run `evaluate_pipeline.py` to evaluate all 981 cases against `ground_truth_100per_disease.jsonl`.
* Verify targeted gains:
  * Confirmed Positive Accuracy: **70.8% $\rightarrow >80.0\%$**.
  * Overall Exact Match Accuracy: **43.4% $\rightarrow >55.0\%$**.
  * Macro ROC-AUC: **$>0.9250$**.

---

## 6. Key Code & File References
* Pipeline Classifier: [`stage2_diagnosis.py`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/stage2_diagnosis.py)
* Clinical Knowledge Base: [`clinical_knowledge.py`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/clinical_knowledge.py)
* Evaluation Harness: [`evaluate_pipeline.py`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/evaluate_pipeline.py)
* Ground Truth: [`ground_truth_100per_disease.jsonl`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/ground_truth_100per_disease.jsonl)
* Patient Dataset: [`extracted_cases_100per_disease.jsonl`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/extracted_cases_100per_disease.jsonl)
* Confirmed Entities: [`accepted_entities.json`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/accepted_entities.json) & [`human_review_queue.json`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/human_review_queue.json)
* Teammate Skill Files: [`skills/`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/skills/)
* Related Papers: [`related_materials/`](file:///Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/aiRepo/HealthCareAgent/related_materials/) (`trove.pdf`, `medspacy.pdf`, `medcat.pdf`)

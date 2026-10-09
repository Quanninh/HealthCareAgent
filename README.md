# 🏥 MultiCaRe Clinical Gold Standard & Multi-Agent Annotation Pipeline

> **Branch:** `nguyenkhoa-clinical-labeling`  
> **Repository:** [HealthCareAgent](https://github.com/Quanninh/HealthCareAgent)  
> **Clinical Domain:** 15 Priority Tropical & Infectious Diseases  

---

## 📌 Overview

This branch hosts the **Clinical Gold Standard Annotation Pipeline and Dataset** for the MultiCaRe corpus (~98,000 clinical cases extracted from PMC case reports). 

Standard classification often treats a case as having a single exclusive diagnosis ("winner-take-all"). In complex clinical reality, patients frequently present with coinfections, secondary infections, or differential diagnoses. This repository formulates disease identification at the **Pair-Level** `(case_id, target_disease)` and implements a clinically grounded **Coordinator + 15 Specialized Disease Agents** framework to construct a verified gold standard.

---

## 🏗️ Repository Structure

```text
.
├── .agents/                               # Antigravity / Agentic Annotation Skills
│   └── skills/
│       ├── clinical-annotator/            # Master Coordinator: 12-step clinical evaluation protocol
│       ├── disease-agent-brucellosis/     # Specialist agent & CDC/WHO evidence rules for Brucellosis
│       ├── disease-agent-chikungunya/     # Specialist agent for Chikungunya
│       ├── disease-agent-cholera/         # Specialist agent for Cholera
│       ├── disease-agent-covid_19/        # Specialist agent for COVID-19
│       ├── disease-agent-dengue/          # Specialist agent for Dengue
│       ├── disease-agent-ebola_filovirus/ # Specialist agent for Ebola / Filovirus
│       ├── disease-agent-hiv_aids/        # Specialist agent for HIV / AIDS
│       ├── disease-agent-leishmaniasis/   # Specialist agent for Leishmaniasis
│       ├── disease-agent-leptospirosis/   # Specialist agent for Leptospirosis
│       ├── disease-agent-malaria/         # Specialist agent for Malaria
│       ├── disease-agent-rabies/          # Specialist agent for Rabies
│       ├── disease-agent-tuberculosis/    # Specialist agent for Tuberculosis
│       ├── disease-agent-typhoid_fever/   # Specialist agent for Typhoid Fever
│       ├── disease-agent-yellow_fever/    # Specialist agent for Yellow Fever
│       └── disease-agent-zika/            # Specialist agent for Zika
│
├── config/
│   └── disease_taxonomy.json              # Clinical ontology: synonyms, MeSH, pathogens & evidence terms
│
├── data/
│   ├── raw_filtered/
│   │   └── tropical_infectious_candidate_pairs.parquet   # 17,431 unified candidate pairs
│   ├── annotation_workdir/
│   │   ├── labeled_pool/                  # 7,043 fully adjudicated and labeled candidate pairs
│   │   │   ├── coordinator_manifest.json
│   │   │   ├── pair_provenance.json
│   │   │   ├── input/                     # 15 disease-specific input JSONL files
│   │   │   └── output/                    # 15 disease-specific annotated JSONL files
│   │   └── tier3_pool/                    # 10,388 high-recall candidate pairs for agentic labeling
│   │       ├── coordinator_manifest.json
│   │       ├── pair_retrieval_provenance.json
│   │       ├── input/                     # 15 disease-specific input JSONL files
│   │       └── prompts/                   # Clinical adjudication prompt specifications
│   └── gold_standard/
│       ├── pair_annotations_02b_unified.jsonl   # 7,043 consolidated gold-standard records
│       └── annotation_coordinator_report.json   # Comprehensive audit & validation metrics
│
├── scripts/
│   └── 02_create_clinical_candidate_pairs.py     # End-to-end high-recall candidate generator
│
├── .gitignore
└── README.md
```

---

## 🎯 Key Methodological Foundations

### 1. Pair-Level Abstraction `(case_id, target_disease)`
Rather than labeling a case with a single categorical label:
- Each candidate disease mention within a case narrative is treated as an independent `(case_id, target_disease)` pair.
- Multi-infection cases naturally contain $N \ge 2$ valid candidate pairs without inter-disease suppression.

### 2. Multi-Tier Confidence Architecture
Each candidate pair is discovered through a three-tier hierarchical sieve:
- **Tier 1 (Article Metadata):** Explicit match in PubMed article title, author keywords, or major MeSH descriptors.
- **Tier 2 (Article Abstract):** Diagnostic keywords present in abstract sentences.
- **Tier 3 (Case Narrative Mention):** Disease keywords identified directly inside `case_text`.

### 3. Okapi BM25 Physical Boundary Gate
- True **Okapi BM25** scoring ($k_1=1.5, b=0.75$) with global IDF computed across the full MultiCaRe corpus.
- Eliminates noise pairs where a disease is mentioned in metadata/background but has **zero** evidence in the actual patient narrative.

### 4. Negation-Safe Handling
- Proximity negation patterns (e.g., *"ruled out for malaria"*, *"tested negative for dengue"*) are **retained and flagged** (`has_negation_mention: true`), not blindly dropped.
- Downstream clinical agents determine whether the finding represents a true negative differential diagnosis or a false detection.

---

## 🦠 The 15 Target Diseases

The taxonomy in [`config/disease_taxonomy.json`](config/disease_taxonomy.json) defines synonyms, ICD/MeSH mappings, gold standard diagnostic tests, clinical signs, and therapeutic evidence for:

| # | Disease | Primary Pathogen(s) | Gold-Standard Confirmation Examples |
|---|---|---|---|
| 1 | **Brucellosis** | *Brucella abortus / melitensis* | Blood culture, Rose Bengal test, standard tube agglutination |
| 2 | **Chikungunya** | Chikungunya virus (CHIKV) | RT-PCR, anti-CHIKV IgM ELISA, plaque reduction neutralization |
| 3 | **Cholera** | *Vibrio cholerae* (O1/O139) | Stool culture on TCBS agar, PCR, dark-field microscopy |
| 4 | **COVID-19** | SARS-CoV-2 | RT-PCR (nasopharyngeal), rapid antigen test, viral sequencing |
| 5 | **Dengue** | Dengue virus (DENV 1–4) | NS1 antigen ELISA, RT-PCR, IgM antibody capture ELISA |
| 6 | **Ebola / Filovirus** | Ebolavirus, Marburgvirus | RT-PCR, antigen-capture ELISA, viral isolation (BSL-4) |
| 7 | **HIV / AIDS** | Human immunodeficiency virus | 4th-gen Ag/Ab immunoassay, HIV viral load RNA PCR, Western blot |
| 8 | **Leishmaniasis** | *Leishmania donovani / infantum* | Tissue biopsy / smear (amastigotes in macrophages), rK39 dipstick |
| 9 | **Leptospirosis** | *Leptospira interrogans* | Microscopic agglutination test (MAT), urine/blood PCR |
| 10 | **Malaria** | *Plasmodium falciparum / vivax* | Giemsa-stained thick/thin blood smear, rapid diagnostic test (RDT) |
| 11 | **Rabies** | Rabies lyssavirus | Direct fluorescent antibody (DFA) on brain/nuchal skin, RT-PCR |
| 12 | **Tuberculosis** | *Mycobacterium tuberculosis* | Acid-fast bacilli (AFB) smear, GeneXpert MTB/RIF, Löwenstein-Jensen culture |
| 13 | **Typhoid Fever** | *Salmonella enterica* serovar Typhi | Blood/bone marrow culture, Widal test, stool culture |
| 14 | **Yellow Fever** | Yellow fever virus (YFV) | RT-PCR, plaque reduction neutralization test (PRNT), IgM ELISA |
| 15 | **Zika** | Zika virus (ZIKV) | RT-PCR (serum/urine), PRNT, anti-ZIKV IgM |

---

## 📊 Dataset Breakdown

| Dataset Pool | Pair Count | Status | Description |
|---|:---:|:---:|---|
| **Unified Candidates** | **17,431** | Complete | Generated by `02_create_clinical_candidate_pairs.py` |
| **`labeled_pool`** | **7,043** | Audited | Fully annotated and quality-checked clinical gold standard |
| **`tier3_pool`** | **10,388** | Prepared | High-recall narrative pairs prepared for agentic annotation |

- **Zero Overlap:** The `labeled_pool` (7,043) and `tier3_pool` (10,388) are strictly disjoint ($7,043 + 10,388 = 17,431$).
- **Audit Verification:** Validated with 0 invalid records in [`data/gold_standard/annotation_coordinator_report.json`](data/gold_standard/annotation_coordinator_report.json).

---

## 🤖 Multi-Agent Annotation Framework

Located under [`.agents/skills/`](.agents/skills/), the system implements a hybrid clinical decision protocol:
1. **Clinical Annotator Coordinator (`clinical-annotator`):**
   - Orchestrates the 15 disease agents.
   - Enforces the 12-step clinical evaluation protocol (diagnostic certainty, temporal onset, differential adjudication, evidence citation).
2. **15 Disease Specialists (`disease-agent-<disease>`):**
   - Grounded in CDC DPDx, CDC NNDSS, and WHO case definition criteria.
   - Outputs structured JSON including diagnosis classification (`CONFIRMED`, `PROBABLE`, `SUSPECTED`, `RULED_OUT`, `EXCLUDED`), specific textual spans, and reasoning.

---

## 🚀 Getting Started

### 1. Requirements
- Python 3.10+
- `pandas`, `pyarrow`, `numpy`

```bash
pip install pandas pyarrow numpy
```

### 2. Inspecting the Gold Standard
You can directly read the gold standard annotations and summary reports:

```python
import pandas as pd
import json

# Read 7,043 gold standard annotations
df_gold = pd.read_json("data/gold_standard/pair_annotations_02b_unified.jsonl", lines=True)
print(f"Loaded {len(df_gold):,} gold pairs across {df_gold['target_disease'].nunique()} diseases.")

# Inspect coordinator report
with open("data/gold_standard/annotation_coordinator_report.json", "r") as f:
    report = json.load(f)
print(f"Total evaluated pairs: {report['evaluation_summary']['total_pairs_evaluated']:,}")
```

### 3. Re-generating Candidate Pairs
To execute the candidate generation pipeline from raw MultiCaRe parquets:

```bash
python scripts/02_create_clinical_candidate_pairs.py \
    --config config/disease_taxonomy.json \
    --raw-data-dir /path/to/multicare_dataset_repo \
    --output data/raw_filtered/tropical_infectious_candidate_pairs.parquet \
    --summary reports/02_candidate_pairs_summary.json
```

Use `--dry-run` to inspect corpus statistics without writing files.

---

## 📜 Citation & Credits

This pipeline is built on top of:
- **MultiCaRe Dataset**: [doi:10.5281/zenodo.10079369](https://doi.org/10.5281/zenodo.10079369)
- **HealthCareAgent**: [GitHub Repository](https://github.com/Quanninh/HealthCareAgent)

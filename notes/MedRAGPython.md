Here is a clear breakdown of the purpose, internal logic, and relationship between these three files in the **MedRAG** integration:

```
┌─────────────────────────┐
│   Raw Payload JSONs     │ (6,694 clinical cases in payload_for_ref/payloads/)
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│   process_payloads.py   │ ➔ Extracts text + captions (ignores raw image files)
└─────┬──────────────┬────┘
      │              │
      ▼              ▼
┌───────────┐  ┌────────────────────────────────────────────────────────┐
│text_      │  │ MedRAG/corpus/payloads/chunk/payloads.jsonl            │
│payloads   │  └──────────────┬──────────────────────────┬──────────────┘
│.jsonl     │                 │                          │
└───────────┘                 ▼                          ▼
               ┌───────────────────────┐  ┌─────────────────────────────┐
               │ test_native_medrag.py │  │     medrag_payloads.py      │
               │ (Validates MedRAG     │  │ (BM25 + Hybrid RRF +        │
               │  DocExtracter)        │  │  Clinical Reasoning Engine) │
               └───────────────────────┘  └─────────────────────────────┘
```

---

### 1. `HealthCareAgent/process_payloads.py` — *Corpus Ingestion & Formatting*

* **Primary Purpose:**  
  Ingests 6,694 raw clinical case payload files and converts them into standardized, clean text formats ready for retrieval.
* **Key Operations:**
  1. **Clinical Text Parsing (`parse_clinical_text`)**: Uses regex to extract structured sections from the clinical note: Title, Source, Demographics, Target Disease, and Case Presentation.
  2. **Text-Only Extraction (Multimodal Filtering)**: It reads `image_caption` and `image_footnote` (such as radiology/CT findings and histology descriptions) to preserve critical clinical observations, but **strictly ignores `img_path`** to keep the corpus lightweight and text-focused.
  3. **Dual Output Generation**:
     * **`data/text_payloads.jsonl`**: The rich clinical dataset containing full case narratives, demographics, and labels.
     * **`MedRAG/corpus/payloads/chunk/payloads.jsonl`**: Formatted specifically for MedRAG's chunk schema (`id`, `title`, `content`, `contents`).
  4. **Statistics**: Calculates word counts, averages (~511 words/case), and disease distributions (saved to `data/dataset_summary.json`).

---

### 2. `HealthCareAgent/medrag_payloads.py` — *Retrieval & Clinical Reasoning Engine*

* **Primary Purpose:**  
  Executes the core MedRAG retrieval and reasoning pipeline directly on the processed clinical cases.
* **Key Components:**
  1. **`MedRAGPayloadsCorpus`**: Loads all 6,694 processed documents into memory in ~0.1s and indexes them by `id`.
  2. **`BM25Retriever`**: Builds a biomedical token index using `rank_bm25` (preserving biomedical terms and hyphens). It ranks cases using Okapi BM25 in under ~0.05 seconds.
  3. **`DenseRetriever` & `HybridRRFRetriever`**: Supports dense embeddings and Reciprocal Rank Fusion (RRF):
     $$\text{RRF\_score}(d) = \sum \frac{1}{k + \text{rank}(d) + 1}$$
     This merges lexical search (exact clinical terms like "cavitary lesions") with semantic search.
  4. **`MedRAGReasoner`**: Formats the retrieved cases into standard MedRAG evidence snippets (`Document [1] (ID: ... | Evidence: ...)`), attaches retrieval confidence scores, and constructs the clinical prompt context.
  5. **Demonstration Queries**: Runs automated test queries (e.g., *Tuberculosis with immune thrombocytopenic purpura* and *COVID-19 with autoimmune myositis*), verifying that rank-1 retrieved cases match the target clinical conditions.

---

### 3. `HealthCareAgent/test_native_medrag.py` — *Native MedRAG Integration Unit Test*

* **Primary Purpose:**  
  A sanity check ensuring that MedRAG's native library (`MedRAG/src/utils.py`) recognizes `Payloads` as a registered corpus alongside MedRAG's built-in corpora (`PubMed`, `StatPearls`, `Textbooks`).
* **Key Checks:**
  1. **Corpus Registration**: Asserts that `"Payloads"` is registered in `utils.corpus_names` and maps to `["payloads"]`.
  2. **`DocExtracter` Validation**: Instantiates MedRAG’s built-in `DocExtracter(corpus_name="Payloads")` and verifies it can extract documents by ID (`PMC517508_01`) from `MedRAG/corpus/payloads/chunk/payloads.jsonl`.
  3. **Cache Validation**: Tests whether the corpus indexer (`Payloads_id2text.json`) caches document IDs correctly for fast document lookups during multi-hop retrieval.

---

### Summary of How They Work Together:
1. You run **`process_payloads.py`** once to parse the raw clinical JSON files into the MedRAG corpus directory.
2. You run **`test_native_medrag.py`** to confirm MedRAG's built-in components can read and cache the new corpus.
3. You run **`medrag_payloads.py`** (or import its `MedRAGReasoner`) to retrieve similar past cases and ground clinical diagnoses in evidence.

Ran command: `cd HealthCareAgent/`
Ran command: `source .venv/bin/activate`
Ran command: `python medrag_payloads.py
===========================================================================
MEDRAG CLINICAL CASE RETRIEVAL & REASONING ON PAYLOADS DATASET
===========================================================================
[Corpus] Loading documents from: /mnt/DATA/VSCode/Clinicians_MultiModel/HealthCareAgent/MedRAG/corpus/payloads/chunk/payloads.jsonl...
[Corpus] Successfully loaded 6694 documents in 0.11s
[BM25] Building BM25 index on clinical payload documents...
[BM25] Index built for 6694 documents in 1.64s
---------------------------------------------------------------------------
Query 1 (Target: Tuberculosis with bleeding / immune thrombocytopenic purpura):
'Young immigrant male presenting with severe hemoptysis, macroscopic hematuria, extensive cutaneous petechiae, fever, cavitary lung lesions, thrombocytopenia, and positive acid-fast bacilli.'
---------------------------------------------------------------------------
Retrieval took: 0.0473s
Top Retrieved Evidence Cases:
  [Rank 1] PMC517508_01: Tuberculosis presenting as immune thrombocytopenic purpura (Score: 0.0164)
    Excerpt: Demographics: Case ID: PMC517508_01 | Age: 29.0 | Gender: Male Target Disease: Tuberculosis Case Presentation: A 29-year-old previously healthy immigrant male patient from Kazakhstan was admitted to hospital with new-onset severe hemoptysis, macroscopic hematuria and extensive cutaneous petechiae on...
  [Rank 2] PMC12493756_01: A Case of Granulomatosis with Polyangiitis Masquerading as Tuberculosis (Score: 0.0161)
    Excerpt: Demographics: Case ID: PMC12493756_01 | Age: 45.0 | Gender: Male Target Disease: Tuberculosis Case Presentation: A 45-year-old male who recently immigrated from India with no known medical history presented with the chief complaint of worsening shortness of breath at rest (See clinical timeline: Fig...
  [Rank 3] PMC3987999_02: The pathology of severe dengue in multiple organs of human fatal cases: histopathology, ultrastructure and virus replication (Score: 0.0159)
    Excerpt: Demographics: Case ID: PMC3987999_02 | Age: 63.0 | Gender: Male Target Disease: Dengue Case Presentation: Clinical data: A 63-year-old male patient with diabetes mellitus, taking acetylsalicylic acid (100 mg) and Daonil, developed a sudden onset of headache, myalgia, anorexia, abdominal pain. Four d...
---------------------------------------------------------------------------
Query 2 (Target: COVID-19 with autoimmune myositis):
'Female diabetic patient with COVID-19 infection developing severe myalgia, elevated creatine kinase (CK), positive myositis-specific autoantibodies, and ketoacidosis.'
---------------------------------------------------------------------------
Retrieval took: 0.0415s
Top Retrieved Evidence Cases:
  [Rank 1] PMC10007705_01: Positive myositis-specific autoantibodies during COVID-19: a case report (Score: 0.0164)
    Excerpt: Demographics: Case ID: PMC10007705_01 | Age: 27.0 | Gender: Female Target Disease: Covid19 Case Presentation: Coronavirus disease 2019 (COVID-19) is the first large-scale pandemic of the 21st century. It is caused by a pathogen, the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). COVID...
  [Rank 2] PMC10007705_02: Positive myositis-specific autoantibodies during COVID-19: a case report (Score: 0.0161)
    Excerpt: Demographics: Case ID: PMC10007705_02 | Age: 27.0 | Gender: Female Target Disease: Covid19 Case Presentation: Patient information: a 27-year-old woman was admitted to the emergency room with abdominal pain and vomiting for three days. Cough, dyspnea and other respiratory symptoms were not observed. ...
  [Rank 3] PMC10357379_02: Clinical and biological heterogeneity of multisystem inflammatory syndrome in adults following SARS-CoV-2 infection: a case series (Score: 0.0159)
    Excerpt: Demographics: Case ID: PMC10357379_02 | Age: 28.0 | Gender: Male Target Disease: Covid19 Case Presentation: In March 2022, a 28-year-old male with no past medical history was found unresponsive on the floor of his home, last seen 15 h prior, following a one-week prodrome of fatigue and polydipsia. H...
[Finished] Demonstration results saved to: /mnt/DATA/VSCode/Clinicians_MultiModel/HealthCareAgent/data/medrag_demonstration_results.json
===========================================================================`
Ran command: `python medrag_payloads.py
===========================================================================
MEDRAG CLINICAL CASE RETRIEVAL & REASONING ON PAYLOADS DATASET
===========================================================================
[Corpus] Loading documents from: /mnt/DATA/VSCode/Clinicians_MultiModel/HealthCareAgent/MedRAG/corpus/payloads/chunk/payloads.jsonl...
[Corpus] Successfully loaded 6694 documents in 0.15s
[BM25] Building BM25 index on clinical payload documents...
[BM25] Index built for 6694 documents in 1.81s
---------------------------------------------------------------------------
Query 1 (Target: Tuberculosis with bleeding / immune thrombocytopenic purpura):
'Young immigrant male presenting with severe hemoptysis, macroscopic hematuria, extensive cutaneous petechiae, fever, cavitary lung lesions, thrombocytopenia, and positive acid-fast bacilli.'
---------------------------------------------------------------------------
Retrieval took: 0.0467s
Top Retrieved Evidence Cases:
  [Rank 1] PMC517508_01: Tuberculosis presenting as immune thrombocytopenic purpura (Score: 0.0164)
    Excerpt: Demographics: Case ID: PMC517508_01 | Age: 29.0 | Gender: Male Target Disease: Tuberculosis Case Presentation: A 29-year-old previously healthy immigrant male patient from Kazakhstan was admitted to hospital with new-onset severe hemoptysis, macroscopic hematuria and extensive cutaneous petechiae on...
  [Rank 2] PMC12493756_01: A Case of Granulomatosis with Polyangiitis Masquerading as Tuberculosis (Score: 0.0161)
    Excerpt: Demographics: Case ID: PMC12493756_01 | Age: 45.0 | Gender: Male Target Disease: Tuberculosis Case Presentation: A 45-year-old male who recently immigrated from India with no known medical history presented with the chief complaint of worsening shortness of breath at rest (See clinical timeline: Fig...
  [Rank 3] PMC3987999_02: The pathology of severe dengue in multiple organs of human fatal cases: histopathology, ultrastructure and virus replication (Score: 0.0159)
    Excerpt: Demographics: Case ID: PMC3987999_02 | Age: 63.0 | Gender: Male Target Disease: Dengue Case Presentation: Clinical data: A 63-year-old male patient with diabetes mellitus, taking acetylsalicylic acid (100 mg) and Daonil, developed a sudden onset of headache, myalgia, anorexia, abdominal pain. Four d...
---------------------------------------------------------------------------
Query 2 (Target: COVID-19 with autoimmune myositis):
'Female diabetic patient with COVID-19 infection developing severe myalgia, elevated creatine kinase (CK), positive myositis-specific autoantibodies, and ketoacidosis.'
---------------------------------------------------------------------------
Retrieval took: 0.043s
Top Retrieved Evidence Cases:
  [Rank 1] PMC10007705_01: Positive myositis-specific autoantibodies during COVID-19: a case report (Score: 0.0164)
    Excerpt: Demographics: Case ID: PMC10007705_01 | Age: 27.0 | Gender: Female Target Disease: Covid19 Case Presentation: Coronavirus disease 2019 (COVID-19) is the first large-scale pandemic of the 21st century. It is caused by a pathogen, the severe acute respiratory syndrome coronavirus 2 (SARS-CoV-2). COVID...
  [Rank 2] PMC10007705_02: Positive myositis-specific autoantibodies during COVID-19: a case report (Score: 0.0161)
    Excerpt: Demographics: Case ID: PMC10007705_02 | Age: 27.0 | Gender: Female Target Disease: Covid19 Case Presentation: Patient information: a 27-year-old woman was admitted to the emergency room with abdominal pain and vomiting for three days. Cough, dyspnea and other respiratory symptoms were not observed. ...
  [Rank 3] PMC10357379_02: Clinical and biological heterogeneity of multisystem inflammatory syndrome in adults following SARS-CoV-2 infection: a case series (Score: 0.0159)
    Excerpt: Demographics: Case ID: PMC10357379_02 | Age: 28.0 | Gender: Male Target Disease: Covid19 Case Presentation: In March 2022, a 28-year-old male with no past medical history was found unresponsive on the floor of his home, last seen 15 h prior, following a one-week prodrome of fatigue and polydipsia. H...
[Finished] Demonstration results saved to: /mnt/DATA/VSCode/Clinicians_MultiModel/HealthCareAgent/data/medrag_demonstration_results.json
===========================================================================`
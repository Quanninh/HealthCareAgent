# MedGemma GraphRAG Autonomous Clinical Evaluation Report

- **Model:** `google/medgemma-1.5-4b-it`
- **Retrieval Paradigm:** GraphRAG (Neo4j Entity-Relation Knowledge Graph)
- **Evaluation Timestamp:** 2026-09-26 00:10:29
- **Total Evaluated Cases (n):** 50

---

## 1. Primary Clinical Performance (5 Core Metrics)

| Metric | k=3 | k=5 | Clinical Interpretation |
|---|---|---|---|
| **n** | 50 | 50 | Total evaluated clinical test cases |
| **recall@k** | 0.02 | 0.02 | True diagnosis appears within top-k differential list |
| **top1_accuracy** | 0.08 | 0.08 | Primary working diagnosis exact match |
| **mrr@k** | 0.01 | 0.01 | Mean Reciprocal Rank (ranking quality within top-k) |

---

## 2. Target Tropical Disease Breakdown

| Target Disease | Cases (N) | Top-1 Accuracy | Recall@5 |
|---|---|---|---|
| **Covid19** | 25 | 0.08 | 0.04 |
| **Tuberculosis** | 13 | 0.1538 | 0.0 |
| **Echinococcosis** | 2 | 0.0 | 0.0 |
| **Tuberculosis, Neurocysticercosis** | 1 | 0.0 | 0.0 |
| **Leprosy** | 1 | 0.0 | 0.0 |
| **Dengue** | 1 | 0.0 | 0.0 |
| **Cryptococcosis** | 1 | 0.0 | 0.0 |
| **Amoebiasis** | 1 | 0.0 | 0.0 |
| **Tuberculosis, Histoplasmosis** | 1 | 0.0 | 0.0 |
| **Tuberculosis, Covid19** | 1 | 0.0 | 0.0 |
| **Histoplasmosis** | 1 | 0.0 | 0.0 |
| **Tuberculosis, Cryptococcosis** | 1 | 0.0 | 0.0 |
| **Leishmaniasis** | 1 | 0.0 | 0.0 |

---

## 3. Qualitative Clinical Audit Samples (First 3 Cases)

### Sample 1: Case ID `PMC9892994_03`
- **Gold Truth Diagnosis:** `Covid19`
- **Model Primary Diagnosis:** `Covid19`
- **Differential Diagnoses:** `['Tuberculosis', 'Dengue', 'Leishmaniasis', 'Malaria']`
- **Confidence Scores:** `[0.85, 0.1, 0.05, 0.0]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Evidence Weight |
|---|---|---|---|
| **Covid19** | None | thrombocytopenia, pcr | 1243 |
| **Tuberculosis** | None | thrombocytopenia, pcr | 271 |
| **Dengue** | None | pcr, thrombocytopenia | 69 |
| **Leishmaniasis** | None | thrombocytopenia, pcr | 53 |
| **Malaria** | None | pcr, thrombocytopenia | 42 |

**Model Clinical Rationale:**
> The patient is a 6-day-old girl presenting with poor feeding and increasing respiratory distress, initially diagnosed with transient tachypnea of the newborn (TTN) and treated with CPAP. She was transferred due to worsening respiratory symptoms despite CPAP. A nasopharyngeal swab for respiratory multiplex panel and SARS-CoV-2 PCR was performed, and she tested positive for SARS-CoV-2. This confirms the diagnosis of Covid19. The patient's symptoms of respiratory distress, oxygen desaturations, and chest X-ray findings of bilateral patchy granular opacities suggestive of pneumonia are consistent with Covid19 pneumonia. The patient also experienced thrombocytopenia, which is a known complication of Covid19. Although the patient was treated with remdesivir and dexamethasone, the clinical course and positive SARS-CoV-2 PCR strongly support Covid19 as the primary diagnosis. The differential diagnoses listed are less likely given the positive SARS-CoV-2 PCR result. Tuberculosis, Dengue, Leishmaniasis, and Malaria are not supported by the positive SARS-CoV-2 PCR result. The patient's age (6 days old) makes these diagnoses less probable, especially given the lack of specific risk factors mentioned for these diseases in the presentation. The patient's symptoms and lab findings (positive SARS-CoV-2 PCR, thrombocytopenia, pneumonia) align with the evidence provided in the knowledge graph for Covid19. The evidence weight for Covid19 (1243) is significantly higher than for the other candidate diseases (Tuberculosis 271, Dengue 69, Leishmaniasis 53, Malaria 42), indicating a stronger association between the symptoms and labs and Covid19 in the graph.

---

### Sample 2: Case ID `PMC4192926_01`
- **Gold Truth Diagnosis:** `Tuberculosis`
- **Model Primary Diagnosis:** `Unspecified`
- **Differential Diagnoses:** `[]`
- **Confidence Scores:** `[]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Evidence Weight |
|---|---|---|---|
| **Covid19** | vomiting, headache, edema, nausea | chest x-ray, biopsy | 5036 |
| **Tuberculosis** | headache, vomiting, edema, nausea | chest x-ray, biopsy | 4090 |
| **Cryptococcosis** | edema, vomiting, headache, nausea | biopsy, chest x-ray | 470 |
| **Echinococcosis** | edema, headache, nausea, vomiting | chest x-ray, biopsy | 462 |
| **Dengue** | edema, nausea, vomiting, headache | chest x-ray, biopsy | 350 |

**Model Clinical Rationale:**
> ```json
{
  "primary_diagnosis": "Tuberculosis",
  "differential_diagnoses": [
    "Covid19",
    "Cryptococcosis",
    "Echinococcosis"
  ],
  "confidence_scores": [
    0.85,
    0.10,
    0.05
  ],
  "clinical_rationale": "The patient's presentation includes headache, nausea, and vomiting, which are non-specific symptoms that can be seen in various infectious and inflammatory conditions. The patient is a 71-year-old male with a history of kidney transplant on immunosuppressive therapy, diabetes, and hypertension. The patient presented with a 1-day history of headache, nausea, and vomiting. Physical examination revealed no focal neurological symptoms and normal blood pressure. Initial laboratory reports showed an unremarkable cell blood count, and basic metabolic panel, liver function tests, and coagulation panel parameters were all within normal limits. Blood cultures and urine analysis were both negative. Prior PPD test and HIV results were negative. Chest X-ray demonstrated a stable right upper lobe cavitary lesion that had been biopsied twice previously with nondiagnostic results. A head CT demonstrated a cystic mass in the left cerebellum with perilesional edema. Further evaluation with contrast enhanced MRI showed a well circumscribed left cerebellar hemisphere ring enhancing mass on T1 sequences with restricted diffusion, mass effect, and perilesional edema. The patient underwent a left posterior fossa biopsy and drainage. The lesion was well encapsulated with a frankly purulent center. Numerous acid fast bacilli were seen on acid fast stain, and cultures returned positive for mycobacterium tuberculosis. Cerebrospinal fluid (CSF) cultures were also obtained, which were negative. Microbiology revealed pan sensitive mycobacterium tuberculosis and the patient was started on rifampicin, isoniazid, pyrazinamide, ethambutol (RIPE), and B6. Follow-up MRIs showed that the tuberculosis abscess had grown in size from 2.0 x 2.0 x 2.2 to 2.5 x 3.3 x 2.3 cm at 9 months, but the amount of perilesional edema had decreased. The patient's symptoms continued to improve with treatment. The patient's symptoms (headache, nausea, vomiting) and imaging findings (cavitary lesion in the right upper lobe, cystic mass in the left cerebellum with perilesional edema) are consistent with the symptoms

---

### Sample 3: Case ID `PMC9734843_04`
- **Gold Truth Diagnosis:** `Covid19`
- **Model Primary Diagnosis:** `Unspecified`
- **Differential Diagnoses:** `[]`
- **Confidence Scores:** `[]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Evidence Weight |
|---|---|---|---|
| **Covid19** | muscle weakness | None | 29 |
| **Tuberculosis** | muscle weakness | None | 10 |
| **Malaria** | muscle weakness | None | 2 |
| **Dengue** | muscle weakness | None | 2 |
| **Echinococcosis** | muscle weakness | None | 1 |

**Model Clinical Rationale:**
> <unused94>thought
The user wants me to act as a clinical diagnostic assistant and analyze a patient case using the provided Medical Knowledge Graph.

1.  **Identify the primary diagnosis:** The patient presentation strongly suggests a specific condition.
    *   **Patient details:** 53-year-old male, history of ischemic heart disease.
    *   **Timeline:** 14 days after COVID-19 vaccination (ChAdOx1 nCoV-19, AZD1222).
    *   **Symptoms:** Bilateral upper and lower limb numbness, quadriparesis, truncal muscle weakness, lower limbs radicular pain, respiratory muscle weakness.
    *   **Severity:** Admitted to ICU, required CPAP.
    *   **NCS findings:** Bilateral axonal polyradiculoneuropathy of both lower limbs.
    *   **Treatment:** 12 plasmapheresis sessions, daily IV methylprednisolone 1 g for 7 days.
    *   **Outcome:** Partial improvement in respiratory muscle weakness, off CPAP after first 3 sessions, no improvement in limb weakness/numbness, discharged, died one month later.

    This clinical picture, occurring 14 days after a specific COVID-19 vaccine (ChAdOx1 nCoV-19), with symptoms of acute polyradiculoneuropathy (numbness, weakness, radicular pain, respiratory muscle weakness) and confirmed by NCS (bilateral axonal polyradiculoneuropathy), is highly characteristic of **Guillain-Barré Syndrome (GBS)**, specifically the **Acute Inflammatory Demyelinating Polyneuropathy (AIDP)** variant, which is the most common form of GBS. The timing after vaccination is also a known trigger for GBS.

2.  **Ranked list of differential diagnoses:** Based on the symptoms and the provided graph, which diseases are plausible?
    *   **Covid19:** The patient *did* have COVID-19 vaccination, but the symptoms are not typical of acute COVID-19 infection itself. COVID-19 can cause muscle weakness, but the specific pattern of acute polyradiculoneuropathy with radicular pain and axonal findings on NCS is not characteristic. The graph also shows low confidence (29) for Covid19 as a cause of muscle weakness.
    *   **Tuberculosis:** TB typically presents with pulmonary symptoms, systemic symptoms (

---

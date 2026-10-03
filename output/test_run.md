# MedGemma GraphRAG Autonomous Clinical Evaluation Report

- **Model:** `google/medgemma-1.5-4b-it`
- **Retrieval Paradigm:** GraphRAG (Neo4j Entity-Relation Knowledge Graph)
- **Evaluation Timestamp:** 2026-09-25 22:24:14
- **Total Evaluated Cases (n):** 2

---

## 1. Primary Clinical Performance (5 Core Metrics)

| Metric | k=3 | k=5 | Clinical Interpretation |
|---|---|---|---|
| **n** | 2 | 2 | Total evaluated clinical test cases |
| **recall@k** | 0.0 | 0.0 | True diagnosis appears within top-k differential list |
| **top1_accuracy** | 0.5 | 0.5 | Primary working diagnosis exact match |
| **mrr@k** | 0.0 | 0.0 | Mean Reciprocal Rank (ranking quality within top-k) |

---

## 2. Target Tropical Disease Breakdown

| Target Disease | Cases (N) | Top-1 Accuracy | Recall@5 |
|---|---|---|---|
| **Covid19** | 1 | 1.0 | 0.0 |
| **Tuberculosis** | 1 | 0.0 | 0.0 |

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
> The patient is a 6-day-old girl presenting with poor feeding and increasing respiratory distress, initially diagnosed with transient tachypnea of the newborn (TTN) and treated with CPAP. She was transferred due to worsening respiratory symptoms despite CPAP. A nasopharyngeal swab for respiratory multiplex panel and SARS-CoV-2 PCR was performed, and she tested positive for SARS-CoV-2. This confirms the diagnosis of Covid19. The patient's symptoms of respiratory distress, oxygen desaturations, and chest X-ray findings of bilateral patchy granular opacities suggestive of pneumonia are consistent with Covid19 pneumonia. The patient also experienced thrombocytopenia, which is a known complication of Covid19. Although the patient was treated with remdesivir and dexamethasone, the clinical course, including the positive SARS-CoV-2 PCR and the presence of thrombocytopenia, strongly supports Covid19 as the primary diagnosis. The differential diagnoses listed are less likely given the positive SARS-CoV-2 PCR result. Tuberculosis, Dengue, Leishmaniasis, and Malaria are not supported by the positive SARS-CoV-2 PCR result. While thrombocytopenia can be seen in these conditions, the positive PCR result is the most specific finding pointing towards Covid19 in this context. The evidence weight for Covid19 (1243) is significantly higher than for the other candidate diseases (Tuberculosis 271, Dengue 69, Leishmaniasis 53, Malaria 42), indicating a strong association between the symptoms and the positive PCR result.

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
  "clinical_rationale": "The patient's presentation includes headache, nausea, and vomiting, which are non-specific symptoms that can be seen in various infectious and inflammatory conditions. The patient is a 71-year-old male with a history of kidney transplant on immunosuppressive therapy, diabetes, and hypertension. The patient presented with a 1-day history of headache, nausea, and vomiting. Physical examination revealed no focal neurological symptoms and normal blood pressure. Initial laboratory reports showed an unremarkable cell blood count, and basic metabolic panel, liver function tests, and coagulation panel parameters were all within normal limits. Blood cultures and urine analysis were both negative. Prior PPD test and HIV results were negative. Chest X-ray showed a stable right upper lobe cavitary lesion that had been biopsied twice previously with nondiagnostic results. A head CT demonstrated a cystic mass in the left cerebellum with perilesional edema. Further evaluation with contrast enhanced MRI showed a well circumscribed left cerebellar hemisphere ring enhancing mass on T1 sequences with restricted diffusion, mass effect, and perilesional edema. The patient underwent a left posterior fossa biopsy and drainage. The lesion was well encapsulated with a frankly purulent center. Numerous acid fast bacilli were seen on acid fast stain, and cultures returned positive for mycobacterium tuberculosis. CSF cultures were also obtained, which were negative. Microbiology revealed pan sensitive mycobacterium tuberculosis and the patient was started on rifampicin, isoniazid, pyrazinamide, ethambutol (RIPE), and B6. Follow-up MRIs showed that the tuberculosis abscess had grown in size from 2.0 x 2.0 x 2.2 to 2.5 x 3.3 x 2.3 cm at 9 months, but the amount of perilesional edema had decreased. The patient's symptoms continued to improve with treatment. The patient's symptoms (headache, nausea, vomiting) and imaging findings (cavitary lesion in the upper lobe, cystic mass in the cerebellum with perilesional edema) are consistent with Tuberculosis. The patient's history of immunosuppression

---

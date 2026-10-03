# MedGemma GraphRAG Autonomous Clinical Evaluation Report

- **Model:** `google/medgemma-1.5-4b-it`
- **Retrieval Paradigm:** GraphRAG (Neo4j Entity-Relation Knowledge Graph)
- **Evaluation Timestamp:** 2026-09-28 11:44:52
- **Total Evaluated Cases (n):** 50

---

## 1. Primary Clinical Performance (5 Core Metrics)

| Metric | k=3 | k=5 | Clinical Interpretation |
|---|---|---|---|
| **n** | 50 | 50 | Total evaluated clinical test cases |
| **recall@k** | 0.02 | 0.02 | True diagnosis appears within top-k differential list |
| **top1_accuracy** | 0.16 | 0.16 | Primary working diagnosis exact match |
| **mrr@k** | 0.02 | 0.02 | Mean Reciprocal Rank (ranking quality within top-k) |

---

## 2. Target Tropical Disease Breakdown

| Target Disease | Cases (N) | Top-1 Accuracy | Recall@5 |
|---|---|---|---|
| **Covid19** | 25 | 0.28 | 0.0 |
| **Tuberculosis** | 13 | 0.0769 | 0.0769 |
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
| **Covid19** | None | thrombocytopenia, pcr | 3729 |
| **Tuberculosis** | None | thrombocytopenia, pcr | 813 |
| **Dengue** | None | pcr, thrombocytopenia | 207 |
| **Leishmaniasis** | None | thrombocytopenia, pcr | 159 |
| **Malaria** | None | pcr, thrombocytopenia | 126 |

**Model Clinical Rationale:**
> The patient is a 6-day-old girl presenting with respiratory distress, poor feeding, and oxygen desaturations, which started after initial treatment for transient tachypnea of the newborn (TTN) and CPAP. She was diagnosed with SARS-CoV-2 infection via PCR testing of a nasopharyngeal swab. This aligns with the 'Covid19' candidate disease in the knowledge graph, which is associated with symptoms like respiratory distress and potentially thrombocytopenia (although the patient's thrombocytopenia resolved spontaneously). The patient's symptoms of respiratory distress, poor feeding, and oxygen desaturations are consistent with severe respiratory illness, which can be seen in Covid19, especially in infants. The positive SARS-CoV-2 PCR confirms the diagnosis. While other infections like Tuberculosis, Dengue, Leishmaniasis, and Malaria can cause respiratory symptoms and thrombocytopenia, the positive SARS-CoV-2 PCR test is the most direct and specific confirmation of Covid19 in this patient. The other differential diagnoses are less likely given the positive PCR result and the specific context of the patient's presentation (infant with respiratory distress following a known viral illness). Tuberculosis typically presents with different symptoms like cough, fever, and potentially chest X-ray findings like infiltrates or cavities, which are not described here. Dengue, Leishmaniasis, and Malaria are typically associated with fever, rash, and other specific symptoms, and while they can cause thrombocytopenia, the positive SARS-CoV-2 PCR makes Covid19 the most probable diagnosis.

---

### Sample 2: Case ID `PMC4192926_01`
- **Gold Truth Diagnosis:** `Tuberculosis`
- **Model Primary Diagnosis:** `Unspecified`
- **Differential Diagnoses:** `[]`
- **Confidence Scores:** `[]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Evidence Weight |
|---|---|---|---|
| **Covid19** | vomiting, headache, edema, nausea | chest x-ray, biopsy | 15108 |
| **Tuberculosis** | headache, vomiting, edema, nausea | chest x-ray, biopsy | 12270 |
| **Cryptococcosis** | edema, vomiting, headache, nausea | biopsy, chest x-ray | 1410 |
| **Echinococcosis** | edema, headache, nausea, vomiting | chest x-ray, biopsy | 1386 |
| **Dengue** | edema, nausea, vomiting, headache | chest x-ray, biopsy | 1050 |

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
  "clinical_rationale": "The patient's clinical presentation strongly points towards Tuberculosis. The patient is a 71-year-old male with a history of kidney transplant on immunosuppressive therapy, diabetes, and hypertension. He presented with a 1-day history of headache, nausea, and vomiting. Physical examination revealed no focal neurological symptoms and normal blood pressure. Initial labs were unremarkable. Chest X-ray showed a stable right upper lobe cavitary lesion, which was biopsied twice previously with nondiagnostic results. A head CT revealed a cystic mass in the left cerebellum with perilesional edema. Further MRI confirmed a well circumscribed left cerebellar hemisphere ring enhancing mass on T1 sequences with restricted diffusion, mass effect, and perilesional edema. The patient underwent a left posterior fossa biopsy and drainage. The lesion was well encapsulated with a frankly purulent center. Numerous acid fast bacilli were seen on acid fast stain, and cultures returned positive for mycobacterium tuberculosis. CSF cultures were negative. The patient was started on RIPE therapy. Follow-up MRIs showed the tuberculosis abscess had grown in size from 2.0 x 2.0 x 2.2 cm to 2.5 x 3.3 x 2.3 cm at 9 months, but the amount of perilesional edema had decreased. The patient continued to show clinical improvement with treatment. This clinical course, including the specific biopsy findings (purulent center, acid fast bacilli) and positive culture for mycobacterium tuberculosis, confirms the diagnosis of Tuberculosis. The differential diagnoses provided in the knowledge graph are Covid19, Cryptococcosis, and Echinococcosis. Covid19 is less likely given the specific biopsy findings and the patient's history of immunosuppression and prior negative HIV test. Cryptococcosis can present with CNS lesions, but the biopsy findings of acid fast bacilli are characteristic of Tuberculosis, not Cryptococcosis. Echinococcosis can present with CNS lesions, but the biopsy findings of acid fast bacilli are characteristic of Tuberculosis, not Echinococcosis. The patient's symptoms (headache, nausea, vomiting) are non

---

### Sample 3: Case ID `PMC9734843_04`
- **Gold Truth Diagnosis:** `Covid19`
- **Model Primary Diagnosis:** `Unspecified`
- **Differential Diagnoses:** `[]`
- **Confidence Scores:** `[]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Evidence Weight |
|---|---|---|---|
| **Covid19** | muscle weakness | None | 87 |
| **Tuberculosis** | muscle weakness | None | 30 |
| **Malaria** | muscle weakness | None | 6 |
| **Dengue** | muscle weakness | None | 6 |
| **Echinococcosis** | muscle weakness | None | 3 |

**Model Clinical Rationale:**
> <unused94>thought
The user wants me to act as a clinical diagnostic assistant and analyze a patient case using the provided Medical Knowledge Graph.

1.  **Identify the primary diagnosis:** The patient presentation strongly suggests a specific condition.
    *   **Patient Presentation:** 53-year-old male, history of ischemic heart disease, 14 days post-COVID-19 vaccination (ChAdOx1 nCoV-19), presents with acute onset bilateral upper and lower limb numbness, quadriparesis, truncal muscle weakness, lower limbs radicular pain, and respiratory muscle weakness. Admitted to ICU, required CPAP. NCS showed bilateral axonal polyradiculoneuropathy of both lower limbs. Treated with plasmapheresis and methylprednisolone with partial improvement in respiratory weakness but no improvement in limb weakness/numbness. Died one month later.
    *   **Graph Evidence:** The graph lists Covid19, Tuberculosis, Malaria, Dengue, and Echinococcosis. None of these are explicitly linked to the symptoms of muscle weakness, numbness, quadriparesis, truncal weakness, radicular pain, respiratory muscle weakness, or axonal polyradiculoneuropathy.
    *   **Analysis:** The clinical picture is highly characteristic of Guillain-Barré Syndrome (GBS), specifically the acute inflammatory demyelinating polyneuropathy (AIDP) variant, although the NCS finding of axonal polyradiculoneuropathy points towards the acute motor and sensory axonal neuropathy (AMSAN) variant. The timing (14 days post-COVID-19 vaccination) is a well-established trigger for GBS. The symptoms (ascending weakness, numbness, radicular pain, respiratory muscle weakness) and the NCS findings (bilateral axonal polyradiculoneuropathy) are classic for GBS. The treatment response (partial improvement in respiratory weakness, no improvement in limbs) is also typical.
    *   **Conclusion:** The primary diagnosis is Guillain-Barré Syndrome (GBS).

2.  **Provide a ranked list of differential diagnoses:** Consider other conditions that could present with similar symptoms, even if less likely given the specific context.
    *   **Tuberculosis (TB):** Can cause muscle weakness, but typically associated with fever, cough, weight loss, and specific imaging/lab findings (e.g., positive PPD, AFB smear/culture, elevated ESR/CRP). The presentation lacks typical TB symptoms.
    *

---

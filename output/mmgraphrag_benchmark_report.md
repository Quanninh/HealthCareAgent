# MedGemma GraphRAG Autonomous Clinical Evaluation Report

- **Model:** `google/medgemma-1.5-4b-it`
- **Retrieval Paradigm:** GraphRAG (Neo4j Entity-Relation Knowledge Graph)
- **Evaluation Timestamp:** 2026-09-28 10:52:52
- **Total Evaluated Cases (n):** 50

---

## 1. Primary Clinical Performance (5 Core Metrics)

| Metric | k=3 | k=5 | Clinical Interpretation |
|---|---|---|---|
| **n** | 50 | 50 | Total evaluated clinical test cases |
| **recall@k** | 0.22 | 0.22 | True diagnosis appears within top-k differential list |
| **top1_accuracy** | 0.54 | 0.54 | Primary working diagnosis exact match |
| **mrr@k** | 0.21 | 0.21 | Mean Reciprocal Rank (ranking quality within top-k) |

---

## 2. Target Tropical Disease Breakdown

| Target Disease | Cases (N) | Top-1 Accuracy | Recall@5 |
|---|---|---|---|
| **Covid19** | 25 | 0.48 | 0.16 |
| **Tuberculosis** | 13 | 0.6923 | 0.1538 |
| **Echinococcosis** | 2 | 0.5 | 0.5 |
| **Tuberculosis, Neurocysticercosis** | 1 | 0.0 | 0.0 |
| **Leprosy** | 1 | 0.0 | 0.0 |
| **Dengue** | 1 | 1.0 | 1.0 |
| **Cryptococcosis** | 1 | 1.0 | 0.0 |
| **Amoebiasis** | 1 | 1.0 | 0.0 |
| **Tuberculosis, Histoplasmosis** | 1 | 0.0 | 1.0 |
| **Tuberculosis, Covid19** | 1 | 1.0 | 1.0 |
| **Histoplasmosis** | 1 | 0.0 | 0.0 |
| **Tuberculosis, Cryptococcosis** | 1 | 0.0 | 1.0 |
| **Leishmaniasis** | 1 | 1.0 | 0.0 |

---

## 3. Qualitative Clinical Audit Samples (First 3 Cases)

### Sample 1: Case ID `PMC9892994_03`
- **Gold Truth Diagnosis:** `Covid19`
- **Model Primary Diagnosis:** `Covid19`
- **Differential Diagnoses:** `['Tuberculosis', 'Dengue', 'Leishmaniasis', 'Malaria']`
- **Confidence Scores:** `[0.85, 0.1, 0.05, 0.0]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Visual Pathology/Radiology Findings | Modalities | Evidence Weight |
|---|---|---|---|---|---|
| **Covid19** | None | thrombocytopenia, pcr | None | text | 3729 |
| **Tuberculosis** | None | thrombocytopenia, pcr | None | text | 813 |
| **Dengue** | None | pcr, thrombocytopenia | None | text | 207 |
| **Leishmaniasis** | None | thrombocytopenia, pcr | None | text | 159 |
| **Malaria** | None | pcr, thrombocytopenia | None | text | 126 |

**Model Clinical Rationale:**
> The patient is a 6-day-old girl presenting with poor feeding and increasing respiratory distress, initially diagnosed with transient tachypnea of the newborn (TTN) and treated with CPAP. She was transferred for worsening respiratory symptoms despite initial improvement. A nasopharyngeal swab for respiratory multiplex panel and SARS-CoV-2 PCR was performed, and she tested positive for SARS-CoV-2. This positive PCR result strongly supports the diagnosis of Covid19. The patient's symptoms of respiratory distress, oxygen desaturations, and requirement for CPAP are consistent with Covid19 pneumonia, which was further supported by the chest X-ray showing bilateral patchy granular opacities suggestive of pneumonia. The patient also experienced thrombocytopenia, a known complication of Covid19. While the patient was treated with remdesivir and dexamethasone, the clinical course, including the positive SARS-CoV-2 PCR and radiographic findings, points towards Covid19 as the primary diagnosis. The differential diagnoses listed are less likely given the positive SARS-CoV-2 PCR. Tuberculosis, Dengue, Leishmaniasis, and Malaria are not supported by the positive SARS-CoV-2 PCR result. Although thrombocytopenia can be seen in these conditions, the positive PCR result is the most specific finding in this case. The patient's age (6 days old) makes infectious diseases like Covid19, Tuberculosis, Dengue, Leishmaniasis, and Malaria less common, but not impossible, especially in infants. The clinical presentation aligns well with severe respiratory illness secondary to Covid19 in a neonate.

---

### Sample 2: Case ID `PMC4192926_01`
- **Gold Truth Diagnosis:** `Tuberculosis`
- **Model Primary Diagnosis:** `Tuberculosis`
- **Differential Diagnoses:** `['Neurocysticercosis', 'Amoebiasis', 'Covid19']`
- **Confidence Scores:** `[0.85, 0.1, 0.05]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Visual Pathology/Radiology Findings | Modalities | Evidence Weight |
|---|---|---|---|---|---|
| **Tuberculosis** | headache, vomiting, edema, nausea | chest x-ray, biopsy | cavitary lesion, cavitation, perilesional edema, mass effect | radiology, medical_photograph | 597472 |
| **Covid19** | vomiting, headache, edema, nausea | chest x-ray, biopsy | mass effect, cavitation | radiology, medical_photograph | 531692 |
| **Neurocysticercosis** | headache, vomiting, nausea, edema | chest x-ray, biopsy | mass effect, perilesional edema | radiology | 17060 |
| **Amoebiasis** | edema, headache, vomiting, nausea | chest x-ray, biopsy | perilesional edema, mass effect | radiology | 11536 |
| **Tuberculosis, Covid19** | edema, nausea, vomiting, headache | chest x-ray, biopsy | cavitary lesion, cavitation | radiology, medical_photograph | 4532 |

**Model Clinical Rationale:**
> The patient's clinical presentation includes headache, nausea, and vomiting, which are non-specific symptoms. However, the patient's history of kidney transplant on immunosuppressive therapy puts them at increased risk for opportunistic infections, including tuberculosis. The key diagnostic findings are the imaging results. The head CT and MRI show a cystic mass in the left cerebellum with perilesional edema and mass effect upon the 4th ventricle. This finding is consistent with several potential pathologies, including pyogenic abscess, neurocysticercosis, cystic glioma, or other cystic malignant/metastatic process. The contrast enhanced MRI further details a well circumscribed left cerebellar hemispheric lesion with prominent rim enhancement. The patient underwent a biopsy and drainage of the lesion, revealing a frankly purulent center and numerous acid fast bacilli on acid fast stain. Cultures confirmed the presence of mycobacterium tuberculosis. This confirms the diagnosis of Tuberculosis. The patient's symptoms (headache, nausea, vomiting) and the imaging findings (cystic mass in the cerebellum with perilesional edema and mass effect) are consistent with the multimodal knowledge graph evidence for Tuberculosis (597472). Neurocysticercosis (17060) and Amoebiasis (11536) are less likely given the specific findings of acid fast bacilli and mycobacterium tuberculosis on culture, although the imaging findings could overlap. Covid19 (531692) is also less likely given the specific findings of acid fast bacilli and mycobacterium tuberculosis on culture, although the imaging findings could overlap. The patient's immunosuppression increases the risk for TB, and the biopsy findings are definitive for TB.

---

### Sample 3: Case ID `PMC9734843_04`
- **Gold Truth Diagnosis:** `Covid19`
- **Model Primary Diagnosis:** `Covid19`
- **Differential Diagnoses:** `['Tuberculosis', 'Malaria', 'Dengue', 'Echinococcosis']`
- **Confidence Scores:** `[]`

**Retrieved Knowledge Graph Evidence:**
| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Visual Pathology/Radiology Findings | Modalities | Evidence Weight |
|---|---|---|---|---|---|
| **Covid19** | muscle weakness | None | None | text | 87 |
| **Tuberculosis** | muscle weakness | None | None | text | 30 |
| **Malaria** | muscle weakness | None | None | text | 6 |
| **Dengue** | muscle weakness | None | None | text | 6 |
| **Echinococcosis** | muscle weakness | None | None | text | 3 |

**Model Clinical Rationale:**
> ```json
{
  "primary_diagnosis": "Covid19",
  "differential_diagnoses": [
    "Tuberculosis",
    "Malaria",
    "Dengue",
    "Echinococcosis"
  ],
  "confidence_scores": [
    0.85,
    0.10,
    0.05,
    0.00
  ],
  "clinical_rationale": "The patient presents with a constellation of symptoms including bilateral upper and lower limb numbness, quadriparesis, truncal muscle weakness, lower limbs radicular pain, and respiratory muscle weakness, occurring 14 days after receiving the ChAdOx1 nCoV-19 vaccine. This timeline and symptom complex are highly suggestive of a post-vaccination complication. The patient's history of ischemic heart disease is noted but does not directly explain the neurological symptoms. The patient was admitted to ICU and required CPAP, indicating severe respiratory muscle weakness. Nerve conduction studies (NCS) revealed bilateral axonal polyradiculoneuropathy of both lower limbs, a finding consistent with peripheral nerve involvement. The patient received plasmapheresis and methylprednisolone with partial improvement in respiratory muscle weakness but no improvement in limb weakness and numbness. This partial response is characteristic of certain inflammatory neurological conditions. The patient's death one month later suggests a severe, potentially fatal course. The provided knowledge graph evidence strongly supports Covid19 as the primary diagnosis. The symptoms of muscle weakness, numbness, quadriparesis, truncal muscle weakness, lower limbs radicular pain, and respiratory muscle weakness are all listed as matched symptoms for Covid19 in the graph. Although the graph does not explicitly list 'post-vaccination neurological complications' as a symptom for Covid19, the combination of severe neurological symptoms following vaccination, the specific pattern of weakness (including respiratory), and the partial response to plasmapheresis and steroids (often used for inflammatory neurological conditions) strongly points towards a Covid19-related complication. The differential diagnoses are ranked based on the strength of evidence. Tuberculosis, Malaria, Dengue, and Echinococcosis are listed as potential causes of muscle weakness in the graph, but none of these diseases typically present with the specific pattern of acute, severe, post-vaccination neurological symptoms described in this case, especially the combination of quadriparesis, respiratory muscle weakness, and axonal polyradiculoneuropathy. The confidence scores

---

# Clinical Gold Standard Annotation — Typhoid Fever Reasoning Process (All 119 Cases)

## Summary Statistics

| Metric / Label Category | Count | Percentage |
| :--- | ---: | ---: |
| **Total Candidate Pairs Annotated** | **119** | **100.0%** |
| `POSITIVE` (Confirmed *S. Typhi* / *S. Paratyphi* E1/E2 VPD satisfied) | 3 | 2.5% |
| `NEGATIVE` (Explicitly tested negative / ruled out) | 82 | 68.9% |
| `EXCLUDED_NON_TARGET_CASE` (Historical past history, vaccination, empirical misdiagnosis, non-typhoidal *Salmonella*, or background context) | 28 | 23.5% |
| `EXCLUDED_NON_SINGLE_PATIENT` (Multi-patient case series or non-clinical study) | 3 | 2.5% |
| `UNRESOLVED` (`INCONCLUSIVE_DATA` — Widal-only or ambiguous non-confirmatory microbiology) | 3 | 2.5% |
| **Confidence: HIGH** | 114 | 95.8% |
| **Confidence: MEDIUM** | 2 | 1.7% |
| **Confidence: LOW** | 3 | 2.5% |

# Case 001: PMC8864216_01::Typhoid_Fever

- **Case ID:** `PMC8864216_01` | **Article ID:** `PMC8864216` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Kawasaki Disease With Combined Cholestatic Hepatitis and Mycoplasma pneumoniae Infection: A Case Report and Literature Review
- **Established Case Diagnosis:** Kawasaki disease with cholestatic hepatitis and Mycoplasma pneumoniae coinfection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 4-year-2-month-old girl presenting with 3-day high fever, abdominal pain, and cholestatic jaundice (Input metadata: Age `4.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Empirical antibiotic therapy` | Target: `Enteric fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[2934:3067]`
    - **Verbatim Quote:** > "Samples were collected for culture, and the patient was treated with 80 mg/kg ceftriaxone for enteric fever and cholestatic hepatitis"
  - **Evidence Item 2:** `Clinical treatment response to ceftriaxone` | Target: `Enteric fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3153:3206]`
    - **Verbatim Quote:** > "Treatment response was poor, and the fever persisted."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Initial empirical ceftriaxone coverage for suspected enteric fever showed poor response; patient fulfilled Kawasaki disease criteria with positive Mycoplasma pneumoniae serology and responded rapidly to IVIG and aspirin.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 4-year-old girl with prolonged fever, abdominal pain, and cholestatic jaundice received empirical ceftriaxone for suspected enteric fever without clinical improvement. Serology was positive for Mycoplasma pneumoniae and she developed classic mucocutaneous features of Kawasaki disease, resolving rapidly after IVIG and aspirin. Empirical antibiotic administration without microbiological confirmation does not establish typhoid fever (VPD not satisfied -> NEGATIVE).


# Case 002: PMC4977379_01::Typhoid_Fever

- **Case ID:** `PMC4977379_01` | **Article ID:** `PMC4977379` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Melioidosis: A Rare Cause of Liver Abscess
- **Established Case Diagnosis:** Hepatic melioidosis (Burkholderia pseudomallei liver abscess)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 44-year-old male diabetic farmer from the Philippines with 2-week RUQ abdominal pain and fever (Input metadata: Age `44.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Empirical clinical management` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[390:544]`
    - **Verbatim Quote:** > "The patient was admitted to a local hospital and managed as a case of typhoid fever; however, there was no improvement on IV Ampi-Sulbactam for four days."
  - **Evidence Item 2:** `Abscess fluid culture` | Target: `Burkholderia pseudomallei` | Specimen: `liver abscess pus` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1599:1669]`
    - **Verbatim Quote:** > "Culture studies revealed moderate growth of Burkholderia pseudomallei."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Outside hospital managed patient empirically as typhoid fever without improvement; subsequent CT and laparoscopic drainage culture confirmed Burkholderia pseudomallei liver abscess (melioidosis).
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 44-year-old diabetic male farmer was initially managed empirically for typhoid fever at a local hospital without improvement. Abdominal CT identified a segment 8 liver abscess, and aspirated pus culture grew Burkholderia pseudomallei, confirming melioidosis. Initial typhoid suspicion was refuted -> NEGATIVE.


# Case 003: PMC6850740_02::Typhoid_Fever

- **Case ID:** `PMC6850740_02` | **Article ID:** `PMC6850740` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Unexpected diagnosis of basal cell carcinoma in a patient presenting with a secondary location of Leishmania parasites in the skin
- **Established Case Diagnosis:** Visceral and cutaneous Leishmania infantum leishmaniasis co-localized with basal cell carcinoma
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 74-year-old woman from Tunis with prolonged fever, pancytopenia, hepatosplenomegaly, and right arm ulcer (Input metadata: Age `74.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Clinical differential diagnosis` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1803:1934]`
    - **Verbatim Quote:** > "Initially differential diagnosis mainly included brucellosis, typhoid fever, visceral leishmaniasis and hematological malignancies."
  - **Evidence Item 2:** `Blood, stool, urine cultures and Salmonella serology` | Target: `Salmonella / Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1935:2100]`
    - **Verbatim Quote:** > "Bacteriological cultures of blood (3 series), stool and urine revealed all negative. Hepatitis B Virus, Salmonella and Brucella antibody tests were also unrevealing."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 74-year-old woman evaluated for fever and hepatosplenomegaly had typhoid fever in the initial differential diagnosis, but three series of blood cultures, stool and urine cultures, and Salmonella antibody tests were all negative. Visceral leishmaniasis (L. infantum) and basal cell carcinoma were confirmed -> NEGATIVE.


# Case 004: PMC10202396_01::Typhoid_Fever

- **Case ID:** `PMC10202396_01` | **Article ID:** `PMC10202396` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A case of atypical vivax malaria with a global review of reports on myriads of morpho-variations in parasitized red blood cells
- **Established Case Diagnosis:** Atypical Plasmodium vivax malaria
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 13-year-old boy with high-grade fever, severe thrombocytopenia, hypotension, and Plasmodium vivax malaria (Input metadata: Age `13.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[905:1058]`
    - **Verbatim Quote:** > "Other tests such as Dengue (Non-structural protein 1) NS1, scrub typhus card tests, Widal test and COVID 19 reverse transcriptase (RT)-PCR were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 13-year-old boy presenting with fever, thrombocytopenia, and hypovolemia tested negative on Widal testing, while peripheral blood smear and multiplex nested PCR confirmed Plasmodium vivax malaria -> NEGATIVE.


# Case 005: PMC4753744_01::Typhoid_Fever

- **Case ID:** `PMC4753744_01` | **Article ID:** `PMC4753744` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Ataxia in a chronic kidney disease patient on anti-tubercular therapy
- **Established Case Diagnosis:** Tuberculosis lymphadenitis with isoniazid-induced toxic encephalopathy/cerebellar ataxia in stage 5 CKD
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 29-year-old woman with stage 5 chronic kidney disease and 4-month fever developing isoniazid-induced cerebellar ataxia (Input metadata: Age `29.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Enteric fever serology` | Target: `Enteric fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[665:765]`
    - **Verbatim Quote:** > "Serological tests for malaria, dengue, and enteric fever were negative; urine cultures were sterile."
  - **Evidence Item 2:** `Blood culture` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1132:1160]`
    - **Verbatim Quote:** > "Blood cultures were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 29-year-old woman with stage 5 CKD evaluated for 4-month fever had negative serological tests for enteric fever and sterile blood cultures. She had a positive QuantiFERON-TB Gold test and developed isoniazid neurotoxicity -> NEGATIVE.


# Case 006: PMC8213112_01::Typhoid_Fever

- **Case ID:** `PMC8213112_01` | **Article ID:** `PMC8213112` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Fasciola hepatica association with gallbladder malignancy: A rare case report
- **Established Case Diagnosis:** Stage IV gallbladder carcinoma with Fasciola hepatica biliary infestation
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 45-year-old female with obstructive jaundice, Stage IV gallbladder carcinoma, and Fasciola hepatica infestation (Input metadata: Age `45.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Clinical history and bile culture` | Target: `Enteric fever` | Specimen: `bile` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[639:851]`
    - **Verbatim Quote:** > "She did not have any history of smoking and alcoholism and no history of enteric fever in the recent past. Her bile culture was sterile, and she was seronegative for HIV, hepatitis C virus, and hepatitis B virus."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 45-year-old woman with Stage IV gallbladder malignancy and Fasciola hepatica worms extracted on ERCP explicitly had no history of enteric fever in the recent past and a sterile bile culture -> NEGATIVE.


# Case 007: PMC9922567_04::Typhoid_Fever

- **Case ID:** `PMC9922567_04` | **Article ID:** `PMC9922567` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Post-COVID Multisystem Inflammatory Syndrome-Adult Leading to Cardiomyopathy and Autoimmune Thyroiditis: A Case Report
- **Established Case Diagnosis:** Post-COVID-19 Multisystem Inflammatory Syndrome in Adults (MIS-A) with cardiomyopathy and autoimmune thyroiditis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** Adult male patient with post-COVID-19 Multisystem Inflammatory Syndrome in Adults (MIS-A), cardiomyopathy, and autoimmune thyroiditis (Input metadata: Age `None`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid serology and blood/urine cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1507:1841]`
    - **Verbatim Quote:** > "The patient was non-diabetic and was negative for dengue, typhoid, Leptospira, and Malaria serologies; in such a scenario, diagnosis of post-COVID-19, Multisystem inflammatory syndrome-Adult was considered as he fulfilled the validated clinical criteria. The patient's blood and urine cultures showed no growth of any micro-organisms."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** An adult male diagnosed with post-COVID-19 MIS-A tested negative for typhoid serology and had negative blood and urine cultures -> NEGATIVE.


# Case 008: PMC9975493_01::Typhoid_Fever

- **Case ID:** `PMC9975493_01` | **Article ID:** `PMC9975493` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case report: Managing multisystem inflammatory syndrome in children (MIS-C) in Lao People's Democratic Republic, a success story
- **Established Case Diagnosis:** Multisystem inflammatory syndrome in children (MIS-C) secondary to SARS-CoV-2
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 9-year-old Lao boy with 8-day fever and abdominal pain diagnosed with MIS-C following familial COVID-19 exposure (Input metadata: Age `9.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Clinical suspicion at private clinic` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[1622:1827]`
    - **Verbatim Quote:** > "On the day of admission (day 8), his symptoms had not improved, and his family brought him to a new private clinic (PC2) where he was diagnosed with suspected severe sepsis with concerns for typhoid fever."
  - **Evidence Item 2:** `Blood, throat, urine, and stool cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[5036:5131]`
    - **Verbatim Quote:** > "Cultures (blood, throat swab, urine, and stool) were sent (see Figure 1) and returned negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Private clinic suspected severe sepsis with concern for typhoid fever prior to hospital referral, but blood, urine, throat, and stool cultures all returned negative and the child was confirmed to have COVID-19-associated MIS-C.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 9-year-old boy was referred from a private clinic with suspected severe sepsis and concern for typhoid fever; however, blood, stool, urine, and throat cultures all returned negative, SARS-CoV-2 IgG was positive, and he recovered rapidly with IVIG and methylprednisolone for MIS-C -> NEGATIVE.


# Case 009: PMC2808561_01::Typhoid_Fever

- **Case ID:** `PMC2808561_01` | **Article ID:** `PMC2808561` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A case of melioidosis presenting as migrating pulmonary infiltration: the first case in Korea
- **Established Case Diagnosis:** Pulmonary melioidosis (Burkholderia pseudomallei)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 50-year-old Korean man returning from Indonesia with 4-week intermittent fever and migrating pulmonary infiltrates (Input metadata: Age `50.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Prior empirical treatment` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[161:326]`
    - **Verbatim Quote:** > "He had lived in Indonesia for twenty years for business, and visited a local hospital in Indonesia and was treated for typhoid fever without improvement of symptoms."
  - **Evidence Item 2:** `Bronchoscopic washing culture and 16S rRNA sequencing` | Target: `Burkholderia pseudomallei` | Specimen: `bronchial washing` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1794:1953]`
    - **Verbatim Quote:** > "By biochemical examination of API20NE strip and VITEK GNI card (BioMerieux, Inc., Hazelwood, U.S.A.), the organism was identified as Burkholderia pseudomallei."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Patient had been empirically treated for typhoid fever at a local hospital in Indonesia without improvement; bronchoscopic washing culture and 16S rRNA sequencing confirmed Burkholderia pseudomallei (melioidosis).
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 50-year-old man who had been empirically treated for typhoid fever in Indonesia without symptom improvement was found to have pulmonary melioidosis confirmed by isolation and 16S rRNA sequencing of Burkholderia pseudomallei from bronchoscopic washing -> NEGATIVE.


# Case 010: PMC7759084_01::Typhoid_Fever

- **Case ID:** `PMC7759084_01` | **Article ID:** `PMC7759084` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Spontaneous gallbladder perforation occurring at neck in an 8-year old boy
- **Established Case Diagnosis:** Spontaneous gallbladder neck perforation due to acalculous cholecystitis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 8-year-old boy presenting with acute generalized abdominal pain and spontaneous perforation at the gallbladder neck (Input metadata: Age `8.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Postoperative diagnostic workup for enteric fever` | Target: `Enteric fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1809:2016]`
    - **Verbatim Quote:** > "In view of incidentally detected GBP, we further investigated this patient for associated enteric fever, dengue fever and haemolytic disease, and none of these illnesses could be established in this patient."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** An 8-year-old boy with spontaneous perforation at the neck of the gallbladder was specifically investigated for associated enteric fever, dengue fever, and hemolytic disease, and none could be established -> NEGATIVE.


# Case 011: PMC4366991_01::Typhoid_Fever

- **Case ID:** `PMC4366991_01` | **Article ID:** `PMC4366991` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Vitamin B12 and vitamin d deficiencies: an unusual cause of Fever, severe hemolytic anemia and thrombocytopenia
- **Established Case Diagnosis:** Severe vitamin B12 and vitamin D deficiency causing pyrexia, hemolytic anemia, and thrombocytopenia
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 17-year-old strict vegetarian girl with 1-month low-grade intermittent fever, severe hemolytic anemia, and thrombocytopenia (Input metadata: Age `17.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood/urine cultures and Widal test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1313:1398]`
    - **Verbatim Quote:** > "Repeated blood cultures and urine culture were all negative. Widal test was negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 17-year-old girl evaluated for prolonged fever, severe hemolytic anemia, and thrombocytopenia had negative repeated blood cultures, negative urine culture, and a negative Widal test; severe vitamin B12 deficiency was diagnosed and resolved with cyanocobalamin supplementation -> NEGATIVE.


# Case 012: PMC4350044_01::Typhoid_Fever

- **Case ID:** `PMC4350044_01` | **Article ID:** `PMC4350044` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Gallbladder hydrops due to viral hepatitis a infection: a case report
- **Established Case Diagnosis:** Gallbladder hydrops secondary to acute Hepatitis A virus (HAV) infection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 5-year-old boy in Shiraz, Iran with jaundice, severe RUQ abdominal pain, and gallbladder hydrops (Input metadata: Age `5.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood culture and typhoid serology` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1307:1498]`
    - **Verbatim Quote:** > "Blood and urine cultures were negative. Serology of viral hepatitis was positive for HAV IgM, and other viral markers were negative. Serology titers for typhoid and brucellosis were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 5-year-old boy with acute acalculous gallbladder hydrops had negative blood and urine cultures and negative serology titers for typhoid and brucellosis, with positive HAV IgM confirming acute hepatitis A -> NEGATIVE.


# Case 013: PMC8688766_02::Typhoid_Fever

- **Case ID:** `PMC8688766_02` | **Article ID:** `PMC8688766` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case Report: Catatonia Associated With Post-traumatic Stress Disorder
- **Established Case Diagnosis:** Post-traumatic stress disorder (PTSD) and major depressive disorder with severe catatonia
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F3_SUBJECT_COREFERENCE', 'F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 12-year-old female patient (Miss S.S., daughter of a 50-year-old farmer) with severe PTSD and catatonia after physical assault and dog attack (Input metadata: Age `50.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[4009:4195]`
    - **Verbatim Quote:** > "The following neurophysiological measurements were conducted: electrocardiogram (ECG), electroencephalogram (EEG), and Malta and Widal test (to exclude brucellosis), and all were normal."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 12-year-old girl (note: input metadata age 50.0 came from her father's age in sentence 1) admitted with severe catatonia and PTSD had a normal Widal test on workup -> NEGATIVE.


# Case 014: PMC8599285_01::Typhoid_Fever

- **Case ID:** `PMC8599285_01` | **Article ID:** `PMC8599285` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Revealing Chronic Granulomatous Disease in a Patient With Williams-Beuren Syndrome Using Whole Exome Sequencing
- **Established Case Diagnosis:** Williams-Beuren syndrome and autosomal recessive chronic granulomatous disease (NCF1 deficiency)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 7-year-old Murut girl with blended phenotype of Williams-Beuren syndrome (7q11.23 deletion) and autosomal recessive chronic granulomatous disease (NCF1 loss) (Input metadata: Age `1.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Historical medical record of childhood infection` | Target: `Salmonella enterica serovar Typhi` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `SUPPORTS` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[981:1129]`
    - **Verbatim Quote:** > "At the age of three years, she had prolonged fever with diarrhea and vomiting caused by Salmonella typhi, requiring a two-week course of cefuroxime."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 7-year-old girl undergoing whole exome sequencing for Williams-Beuren syndrome and chronic granulomatous disease had a remote childhood history of prolonged fever with diarrhea and vomiting caused by Salmonella typhi at age 3 years, treated with cefuroxime. Because this is a resolved historical episode in early childhood rather than an active clinical episode (temporality = HISTORICAL_RESOLVED, clinical_role = PAST_HISTORY), VPD is not satisfied -> EXCLUDED_NON_TARGET_CASE.


# Case 015: PMC6661959_01::Typhoid_Fever

- **Case ID:** `PMC6661959_01` | **Article ID:** `PMC6661959` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Spontaneous remission of acute monocytic leukemia with trisomy 8 and trisomy 18
- **Established Case Diagnosis:** Acute monocytic leukemia (AML M5b) with partial spontaneous remission
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 67-year-old male with acute monocytic leukemia (AML M5b) with trisomy 8 and trisomy 18 experiencing transient spontaneous remission (Input metadata: Age `67.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `UNKNOWN` (`UNKNOWN`)
8. **Step 8 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Historical literature citation in discussion` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `UNKNOWN` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[4102:4174]`
    - **Verbatim Quote:** > "It was first described following typhoid infection by Eisenlohr in 1878."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 67-year-old man with acute monocytic leukemia had no clinical mention or testing for typhoid fever; the word 'typhoid' appears solely in the discussion noting that spontaneous remission of AML was first described following typhoid infection by Eisenlohr in 1878 -> EXCLUDED_NON_TARGET_CASE.


# Case 016: PMC6419550_01::Typhoid_Fever

- **Case ID:** `PMC6419550_01` | **Article ID:** `PMC6419550` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Spontaneous common hepatic duct perforation in a child: A rare case report
- **Established Case Diagnosis:** Spontaneous perforation of the common hepatic duct
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 6-year-old boy with epigastric pain, abdominal distension, and spontaneous perforation of the common hepatic duct (Input metadata: Age `6.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[575:844]`
    - **Verbatim Quote:** > "Laboratory investigations showed Hemoglobin 8.8 g/dl, total leukocyte count - 18,500/mm3, total bilirubin 3.22 mg/dl (indirect 1.02 mg/dl), alkaline phosphatase 826.5 IU/L, alanine aminotransferase 262 IU/L, and aspartate aminotransferase 490 IU/L, negative Widal test."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 6-year-old boy presenting with biliary peritonitis from spontaneous common hepatic duct perforation had a negative Widal test on laboratory evaluation -> NEGATIVE.


# Case 017: PMC4943127_01::Typhoid_Fever

- **Case ID:** `PMC4943127_01` | **Article ID:** `PMC4943127` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Recurrent mania consequent to quinolones exposure: A case report and review of literature
- **Established Case Diagnosis:** Quinolone-induced (ciprofloxacin) recurrent mania
- **Final Dataset Label:** `UNRESOLVED` (`decision`: `INCONCLUSIVE_DATA`) | **VPD Satisfied:** `False` | **Confidence:** `LOW` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 34-year-old female homemaker presenting with recurrent mania following ciprofloxacin administration (Input metadata: Age `34.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`SUSPECTED_POSSIBLE`)
7. **Step 7 — Temporality:** `RECENT_EPISODIC` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`SECONDARY_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[568:866]`
    - **Verbatim Quote:** > "She consulted a physician after 1 week of onset of fever (10th day) who diagnosed her with typhoid fever on the basis of serological investigations only (Widal test positive; titers for agglutinin O > 1:160 and agglutinin H > 1:160); prescribed her oral ciprofloxacin 500 mg twice a day for a week."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = SUSPECTED`)
12. **Step 12 — Final Adjudication & Rationale:** `UNRESOLVED` (`INCONCLUSIVE_DATA`)
    - **Clinical Rationale:** A 34-year-old woman developed mania after taking oral ciprofloxacin prescribed by an outside physician who diagnosed typhoid fever solely on the basis of a Widal test (O > 1:160, H > 1:160) without blood or stool culture confirmation. Per Typhoid Fever evidence specificity rules (Section 5.9), the Widal test alone is E0/weak evidence and cannot establish a strict positive diagnosis (VPD not satisfied -> UNRESOLVED).


# Case 018: PMC4066596_01::Typhoid_Fever

- **Case ID:** `PMC4066596_01` | **Article ID:** `PMC4066596` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Type 2 lepra reaction in an immunocompromised patient precipitated by filariasis
- **Established Case Diagnosis:** Type 2 lepra reaction (erythema nodosum leprosum) in a patient with AIDS, tubercular lymphadenitis, and filariasis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 35-year-old male with AIDS, tubercular lymphadenitis, lepromatous leprosy with type 2 lepra reaction (ENL), and filariasis (Input metadata: Age `35.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood/stool culture and Widal test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1848:2013]`
    - **Verbatim Quote:** > "Blood and stool culture and streptococcal throat swab showed no growth of organisms and his Widal test for typhoid and microscopy for malarial parasite was negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 35-year-old male with AIDS and lepromatous leprosy presenting with recurrent high-grade fever had negative blood and stool cultures and a negative Widal test for typhoid -> NEGATIVE.


# Case 019: PMC5684584_01::Typhoid_Fever

- **Case ID:** `PMC5684584_01` | **Article ID:** `PMC5684584` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Sarcomatoid Renal Cell Carcinoma in an Adolescent with Sickle Cell Anaemia
- **Established Case Diagnosis:** Sarcomatoid renal cell carcinoma in an adolescent with sickle cell anemia (HbSS)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 17-year-old girl with sickle cell anemia (HbSS) presenting with left renal sarcomatoid renal cell carcinoma (Input metadata: Age `17.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Past medical history at age 10 years` | Target: `Typhoid fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[110:326]`
    - **Verbatim Quote:** > "She had dactylitis at 2 1/2 years and was on regular follow-up with an average of one pain crisis per year until 10 years of life when she had two admissions, managed as typhoid fever and osteomyelitis, respectively."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 17-year-old girl with sickle cell anemia presenting with sarcomatoid renal cell carcinoma had a remote childhood admission at age 10 years 'managed as typhoid fever'. This is a remote historical mention without microbiological details and unrelated to the current care episode -> EXCLUDED_NON_TARGET_CASE.


# Case 020: PMC10327413_02::Typhoid_Fever

- **Case ID:** `PMC10327413_02` | **Article ID:** `PMC10327413` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Leukocytoclastic Vasculitis in a Patient With Crohn Disease: A Case Report
- **Established Case Diagnosis:** Leukocytoclastic vasculitis associated with Crohn disease
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 55-year-old man with Crohn disease in remission presenting with leukocytoclastic vasculitis (Input metadata: Age `55.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Vaccination history` | Target: `Typhoid vaccine` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1002:1225]`
    - **Verbatim Quote:** > "The patient further stated he was up to date on his vaccinations (hepatitis A and B; influenza; anthrax; typhoid; and measles, mumps, and rubella), and he thought he had chickenpox as a child but was not completely certain."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 55-year-old man with leukocytoclastic vasculitis and Crohn disease merely reported being up to date on his vaccinations, including typhoid vaccine. Per Critical Rule 4, vaccination history is PREVENTION_VACCINATION -> EXCLUDED_NON_TARGET_CASE.


# Case 021: PMC10440106_01::Typhoid_Fever

- **Case ID:** `PMC10440106_01` | **Article ID:** `PMC10440106` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Dengue beyond fever-fatal dengue myocarditis and complete heart block: A case report and brief overview of cardiac manifestations of dengue fever
- **Established Case Diagnosis:** Fatal dengue myocarditis (DENV-2) with complete heart block
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 16-year-old boy with dengue virus serotype 2 (DENV-2) myocarditis and complete heart block (Input metadata: Age `16.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood culture and typhoid serology` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1827:1956]`
    - **Verbatim Quote:** > "The patient's blood culture, malarial antigen, typhoid serology, influenza virus, COVID-19, and diphtheria testing were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 16-year-old boy with PCR-confirmed DENV-2 dengue myocarditis and complete heart block had negative blood culture and negative typhoid serology -> NEGATIVE.


# Case 022: PMC3401656_01::Typhoid_Fever

- **Case ID:** `PMC3401656_01` | **Article ID:** `PMC3401656` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Pseudotumoral hemicerebellitis with hemorrhage
- **Established Case Diagnosis:** Pseudotumoral hemicerebellitis with hemorrhage
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 12-year-old boy with pseudotumoral hemicerebellitis and cerebellar hemorrhage (Input metadata: Age `12.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`SUSPECTED_POSSIBLE`)
7. **Step 7 — Temporality:** `RECENT_EPISODIC` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Outside Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[148:310]`
    - **Verbatim Quote:** > "Two weeks before he had fever and was hospitalized in another center with an initial diagnosis of Typhoid fever (Widal positive) and was treated with antibiotics."
  - **Evidence Item 2:** `Blood and CSF cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1435:1615]`
    - **Verbatim Quote:** > "Cultures and neutrophilic virus antibodies, as well as Polymerase Chain Reaction (PCR) for Herpes and Tuberculosis were negative in the cerebrospinal fluid (ventricular) and blood."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Patient was hospitalized 2 weeks earlier at an outside center with an initial Widal-positive diagnosis of typhoid fever, but subsequent blood and CSF cultures at the referral hospital were negative and MRI established pseudotumoral hemicerebellitis.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 12-year-old boy presenting with pseudotumoral hemicerebellitis had been hospitalized 2 weeks prior at another center with an initial diagnosis of typhoid fever based only on a positive Widal test. Blood and CSF cultures at the referral center were negative. Because Widal positivity alone is E0/weak evidence and cultures were negative, VPD is not satisfied -> EXCLUDED_NON_TARGET_CASE.


# Case 023: PMC9957551_01::Typhoid_Fever

- **Case ID:** `PMC9957551_01` | **Article ID:** `PMC9957551` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Expanded Dengue Syndrome Presenting as Intracranial Hemorrhage, Fever, and Rhabdomyolysis: A Case Report
- **Established Case Diagnosis:** Expanded dengue syndrome with intracranial hemorrhage and rhabdomyolysis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 53-year-old hypertensive female with expanded dengue syndrome presenting with basal ganglia hemorrhage, hyperthermia, and rhabdomyolysis (Input metadata: Age `53.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Microbiological cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1702:1747]`
    - **Verbatim Quote:** > "On workup, cultures turned out to be sterile."
  - **Evidence Item 2:** `Tropical fever panel (typhoid workup)` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1932:2198]`
    - **Verbatim Quote:** > "On account of a history of fever with chill and myalgia around a week before ED admission, a tropical workup was sent for malaria, typhoid, leptospirosis, dengue, chikungunya, and scrub typhus, in which serology (IgM antibodies) for dengue turned out to be positive."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 53-year-old woman with intracranial hemorrhage, high-grade fever, and rhabdomyolysis had sterile cultures and a tropical fever panel (including typhoid) in which only dengue IgM was positive -> NEGATIVE.


# Case 024: PMC4010067_01::Typhoid_Fever

- **Case ID:** `PMC4010067_01` | **Article ID:** `PMC4010067` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Hyperglycemia in severe falciparum malaria: a case report
- **Established Case Diagnosis:** Severe Plasmodium falciparum malaria with hyperglycemia and MODS
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 56-year-old Ethiopian immigrant woman returning to Italy from Cote d'Ivoire with severe Plasmodium falciparum malaria (40% parasitemia) and hyperglycemia (Input metadata: Age `56.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Infectious screening panel` | Target: `Enteric fever` | Specimen: `blood` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1477:1692]`
    - **Verbatim Quote:** > "The patient was screened for Human immunodeficiency virus, Parvovirus B19, Hepatitis B virus, Hepatitis C virus, Coxsackie B 1-6, Cytomegalovirus; Herpes Simplex Virus 1 and 2, Epstein-Barr virus, and enteric fever."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 56-year-old woman with severe Plasmodium falciparum malaria (40% parasitemia) underwent broad screening including enteric fever, with no positive enteric fever findings reported -> EXCLUDED_NON_TARGET_CASE.


# Case 025: PMC2822251_01::Typhoid_Fever

- **Case ID:** `PMC2822251_01` | **Article ID:** `PMC2822251` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Adult-onset Still's disease with disseminated intravascular coagulation and multiple organ dysfunctions dramatically treated with cyclosporine A
- **Established Case Diagnosis:** Adult-onset Still's disease (AOSD) with reactive hemophagocytic syndrome and DIC
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 49-year-old woman with Adult-onset Still's disease (AOSD) complicated by reactive hemophagocytic syndrome and DIC (Input metadata: Age `49.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3218:3264]`
    - **Verbatim Quote:** > "Antistreptolysin O and Widal test were normal."
  - **Evidence Item 2:** `Blood, throat, urine, and stool cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[4582:4654]`
    - **Verbatim Quote:** > "Negative results for blood, throat, urine and stool cultures were noted."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 49-year-old woman with AOSD and reactive hemophagocytic syndrome had a normal Widal test and negative blood, throat, urine, and stool cultures -> NEGATIVE.


# Case 026: PMC7365499_01::Typhoid_Fever

- **Case ID:** `PMC7365499_01` | **Article ID:** `PMC7365499` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Pancytopenia induced by secondary hemophagocytic lymphohistiocytosis: A rare, overlooked dreadful complication of Plasmodium vivax
- **Established Case Diagnosis:** Secondary hemophagocytic lymphohistiocytosis (HLH) due to Plasmodium vivax malaria
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 7-year-old girl from New Delhi with pancytopenia and secondary hemophagocytic lymphohistiocytosis induced by Plasmodium vivax malaria (Input metadata: Age `7.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and blood/urine/sputum/stool cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[745:1078]`
    - **Verbatim Quote:** > "Human immunodeficiency virus serology, hepatitis B surface antigen, antibodies against hepatitis C virus, the Epstein-Barr virus, cytomegalovirus, measles, Widal test, K39 test for visceral leishmaniasis, and rapid diagnostic tests (RDTs) for malarial antigen were negative. Her blood, urine, sputum, and stool cultures were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 7-year-old girl with Plasmodium vivax-associated HLH had a negative Widal test and sterile blood, urine, sputum, and stool cultures -> NEGATIVE.


# Case 027: PMC9707495_01::Typhoid_Fever

- **Case ID:** `PMC9707495_01` | **Article ID:** `PMC9707495` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case Report: Multiple autoimmune syndrome (MAS)-An unusual combination
- **Established Case Diagnosis:** Multiple autoimmune syndrome (Type 1 diabetes, Hashimoto thyroiditis, and childhood-onset SLE)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 12-year-old Chinese adolescent boy with multiple autoimmune syndrome (T1DM, Hashimoto thyroiditis, and childhood-onset SLE) (Input metadata: Age `12.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood/bone marrow/stool cultures and Salmonella typhi serology` | Target: `Salmonella enterica serovar Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2698:2949]`
    - **Verbatim Quote:** > "Bacterial cultures from peripheral blood, bone marrow, urine, stool and throat yielded no growth. Serologies for atypical organisms were negative, including Salmonella typhi, Bartonella henselae, Brucella abortus and melitensis, and Toxoplasma gondii."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 12-year-old boy presenting with prolonged fever and cervical lymphadenopathy had negative peripheral blood, bone marrow, urine, and stool cultures and negative Salmonella typhi serology, and was diagnosed with childhood-onset SLE -> NEGATIVE.


# Case 028: PMC7298109_01::Typhoid_Fever

- **Case ID:** `PMC7298109_01` | **Article ID:** `PMC7298109` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A Case Report of Sporadic Adult Neuronal Intranuclear Inclusion Disease (NIID) With Stroke-Like Onset
- **Established Case Diagnosis:** Sporadic adult neuronal intranuclear inclusion disease (NIID)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 61-year-old woman with stroke-like onset of sporadic adult neuronal intranuclear inclusion disease (NIID) (Input metadata: Age `61.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2445:2498]`
    - **Verbatim Quote:** > "The Widal test and the Weil-Felix test were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 61-year-old woman who developed fever after thrombolysis for stroke-like onset of neuronal intranuclear inclusion disease tested negative on the Widal test -> NEGATIVE.


# Case 029: PMC9626822_01::Typhoid_Fever

- **Case ID:** `PMC9626822_01` | **Article ID:** `PMC9626822` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case report: Wallerian degeneration: The innate-immune response to adult-onset Still's disease peripheral nerve injury
- **Established Case Diagnosis:** Adult-onset Still's disease (AOSD) with severe sensory neuropathy
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 20-year-old woman with Adult-onset Still's disease (AOSD) complicated by immune-mediated severe sensory neuropathy with Wallerian degeneration (Input metadata: Age `20.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Salmonella typhi testing and repeated blood cultures` | Target: `Salmonella enterica serovar Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1452:1934]`
    - **Verbatim Quote:** > "Laboratory examinations for common pathogens (respiratory pathogens, such as influenza virus, mycoplasma, chlamydia, legionella, adenovirus, etc.) and specific disease-related pathogens (cytomegalovirus/Epstein-Barr virus, mycobacterium tuberculosis, rickettsia of typhus, Coxiella burnetii of Q fever, Salmonella typhi, Brucella, etc.) were all negative. The blood culture was repeatedly negative, and screening tests for AIDS, hepatitis B, hepatitis C, and syphilis were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 20-year-old woman evaluated for fever of unknown origin had negative testing for Salmonella typhi and repeatedly negative blood cultures, fulfilling Yamaguchi criteria for AOSD -> NEGATIVE.


# Case 030: PMC3401657_01::Typhoid_Fever

- **Case ID:** `PMC3401657_01` | **Article ID:** `PMC3401657` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Concurrent infection of Japanese encephalitis and mixed plasmodium infection
- **Established Case Diagnosis:** Concurrent Japanese encephalitis and mixed Plasmodium vivax / Plasmodium falciparum infection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 3-year-old male child from Gorakhpur with concurrent Japanese encephalitis and mixed Plasmodium vivax and P. falciparum malaria (Input metadata: Age `3.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and blood cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1272:1371]`
    - **Verbatim Quote:** > "The Widal test and viral markers for acute hepatitis were negative and blood cultures were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 3-year-old boy with febrile encephalopathy confirmed to have mixed malaria and Japanese encephalitis had a negative Widal test and sterile blood cultures -> NEGATIVE.


# Case 031: PMC3507127_03::Typhoid_Fever

- **Case ID:** `PMC3507127_03` | **Article ID:** `PMC3507127` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Challenges of recognition of the psychiatric aspects of intimate partner violence
- **Established Case Diagnosis:** Depressive disorder secondary to recurrent intimate partner violence
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 33-year-old female primary school teacher in Nigeria with depressive disorder and somatic complaints secondary to intimate partner violence (Input metadata: Age `33.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Repeated outpatient empirical treatment` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[2357:2752]`
    - **Verbatim Quote:** > "The doctor had referred the patient after he and several others had been treating her for malaria, typhoid fever and other infectious diseases on several occasions along with prescriptions of various multivitamin and haematinic medications. However, despite the fact that none of these treatments ameliorated the patient's persistent distress, the pattern of treatment was repeated several times"
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — General practitioners had repeatedly treated her somatic symptoms empirically as malaria and typhoid fever without relief; psychiatric assessment established depressive disorder secondary to intimate partner abuse.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 33-year-old female primary school teacher (note: input gender metadata 'Male' is erroneous; case text explicitly uses 'she/her') with somatic complaints from intimate partner abuse had been repeatedly treated empirically for malaria and typhoid fever by general practitioners without any diagnostic evidence or clinical improvement -> EXCLUDED_NON_TARGET_CASE.


# Case 032: PMC10071914_01::Typhoid_Fever

- **Case ID:** `PMC10071914_01` | **Article ID:** `PMC10071914` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Acute respiratory distress syndrome in Scrub typhus - An under recognized complication!
- **Established Case Diagnosis:** Scrub typhus (Orientia tsutsugamushi) complicated by acute respiratory distress syndrome (ARDS)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** Woman in her mid-twenties presenting with 10-day high-grade fever, abdominal eschar, and moderate ARDS due to scrub typhus (Input metadata: Age `None`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Clinical differential diagnosis` | Target: `Enteric fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1828:2100]`
    - **Verbatim Quote:** > "Though the differential diagnosis for febrile illness is exhaustive and includes malaria, dengue fever, leptospirosis, enteric fever, and brucellosis, the presence of eschar is pathognomonic and boils it down to the rickettsial infection as the most likely cause of fever."
  - **Evidence Item 2:** `Blood and sputum cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2632:2675]`
    - **Verbatim Quote:** > "The blood and sputum cultures were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A young woman with scrub typhus complicated by ARDS had enteric fever listed in the general differential diagnosis of febrile illness, with sterile blood and sputum cultures and positive Orientia tsutsugamushi IgM -> NEGATIVE.


# Case 033: PMC4746982_01::Typhoid_Fever

- **Case ID:** `PMC4746982_01` | **Article ID:** `PMC4746982` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Laparoscopic splenectomy for spontaneous rupture of the spleen
- **Established Case Diagnosis:** Idiopathic spontaneous rupture of the spleen
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 23-year-old male with idiopathic spontaneous rupture of the spleen managed by laparoscopic splenectomy (Input metadata: Age `23.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Diagnostic workup for typhoid` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1199:1388]`
    - **Verbatim Quote:** > "Since there was no history of trauma, a detailed workup was done for the cause of splenic rupture, tests for typhoid, dengue, malaria, leptospirosis, infectious mononucleosis were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 23-year-old male presenting with atraumatic hemoperitoneum and splenic rupture tested negative for typhoid, dengue, malaria, leptospirosis, and infectious mononucleosis -> NEGATIVE.


# Case 034: PMC8272493_01::Typhoid_Fever

- **Case ID:** `PMC8272493_01` | **Article ID:** `PMC8272493` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Peripheral adenomatoid odontogenic tumor of mandible - A synchronous presentation or a subtype?!
- **Established Case Diagnosis:** Peripheral adenomatoid odontogenic tumor (PAOT) of the anterior mandible
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 16-year-old female with a 6-month painless anterior mandibular gingival swelling diagnosed as peripheral adenomatoid odontogenic tumor (PAOT) (Input metadata: Age `16.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Past medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[722:879]`
    - **Verbatim Quote:** > "Past medical and dental history revealed that she had typhoid few months ago and had multiple restorations for her posterior teeth 2 years ago, respectively."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 16-year-old female evaluated for an odontogenic mandibular tumor had an incidental note in her past medical history that she 'had typhoid few months ago'. No diagnostic evidence or current active infection is present (HISTORICAL_RESOLVED / PAST_HISTORY) -> EXCLUDED_NON_TARGET_CASE.


# Case 035: PMC7217305_01::Typhoid_Fever

- **Case ID:** `PMC7217305_01` | **Article ID:** `PMC7217305` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Successful Treatment of a Multidrug-Resistant Tuberculosis Patient with a Negative Xpert MTB/RIF Test for Rifampicin-Resistant Tuberculosis in Guizhou Province of China: A Case Report
- **Established Case Diagnosis:** Multidrug-resistant pulmonary tuberculosis (MDR-TB)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 32-year-old Chinese woman with multidrug-resistant pulmonary tuberculosis (MDR-TB) harboring a rare rpoB Ile572Phe mutation (Input metadata: Age `32.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[632:747]`
    - **Verbatim Quote:** > "The patient claimed to have no history of hypertension, diabetes, hepatitis, typhoid and other infectious diseases."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 32-year-old woman with multidrug-resistant pulmonary tuberculosis explicitly reported no history of typhoid or other infectious diseases -> NEGATIVE.


# Case 036: PMC6159193_01::Typhoid_Fever

- **Case ID:** `PMC6159193_01` | **Article ID:** `PMC6159193` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Isolated splenic tuberculosis detected only on FDG-PET
- **Established Case Diagnosis:** Isolated splenic tuberculosis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 17-year-old immunocompetent female with 4-week fever of unknown origin diagnosed with isolated splenic tuberculosis via FDG-PET/CT (Input metadata: Age `17.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and blood culture` | Target: `Typhoid / Paratyphoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[809:1068]`
    - **Verbatim Quote:** > "The investigations for various types of fevers, including Widal test for typhoid/ paratyphoid, malarial parasite, leptospira immunoglobulin M antibodies, Weil Felix test for rickettsial infection, urine test and sputum and blood culture were non-contributing."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 17-year-old female with isolated splenic tuberculosis had non-contributing Widal testing for typhoid/paratyphoid and negative blood cultures -> NEGATIVE.


# Case 037: PMC5661914_01::Typhoid_Fever

- **Case ID:** `PMC5661914_01` | **Article ID:** `PMC5661914` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** An outbreak of Leptospirosis among United States military personnel in Guam
- **Established Case Diagnosis:** Leptospirosis outbreak among US military personnel in Guam
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CASE_SERIES` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `MULTI_PATIENT_CASE_SERIES` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 24-year-old male US service member on Guam (index patient among 8 patients in a leptospirosis outbreak) (Input metadata: Age `24.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Immunization history` | Target: `Typhoid vaccine` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[549:650]`
    - **Verbatim Quote:** > "He had been immunized against hepatitis A and B, typhoid, influenza, and took no routine medications."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** This report describes a 24-year-old male index patient and 7 additional patients in a Guam leptospirosis outbreak; the only mention of typhoid is that the index patient had been immunized against typhoid (`PREVENTION_VACCINATION`) and blood cultures were negative -> EXCLUDED_NON_TARGET_CASE.


# Case 038: PMC2636058_01::Typhoid_Fever

- **Case ID:** `PMC2636058_01` | **Article ID:** `PMC2636058` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Branch retinal artery occlusion secondary to dengue fever
- **Established Case Diagnosis:** Classic dengue fever complicated by branch retinal artery occlusion
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 28-year-old woman with branch retinal artery occlusion complicating classic dengue fever (Input metadata: Age `28.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Serological and hematological workup` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[102:377]`
    - **Verbatim Quote:** > "Detailed history- taking, hematological and serological investigations established the diagnosis of classic dengue fever (a positive IgM antibody titer); and ruled out mimicking infections like leptospirosis, typhoid, malaria, syphilis, as well as collagen vascular diseases."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 28-year-old woman with dengue fever and branch retinal artery occlusion had mimicking infections including typhoid explicitly ruled out by hematological and serological investigations -> NEGATIVE.


# Case 039: PMC3410081_01::Typhoid_Fever

- **Case ID:** `PMC3410081_01` | **Article ID:** `PMC3410081` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Thyroid storm presenting as acute abdomen and normothermia
- **Established Case Diagnosis:** Thyroid storm presenting as acute abdomen
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 40-year-old male farm laborer presenting with acute abdomen and normothermia due to thyroid storm (Input metadata: Age `0.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood culture and typhoid serology` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2987:3080]`
    - **Verbatim Quote:** > "Blood culture, urine culture, serological tests for brucella, typhoid and VDRL were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 40-year-old male presenting with thyroid storm mimicking an acute abdomen had negative blood culture, urine culture, and serological tests for typhoid -> NEGATIVE.


# Case 040: PMC3396855_01::Typhoid_Fever

- **Case ID:** `PMC3396855_01` | **Article ID:** `PMC3396855` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Duodenal perforation in a 12-month old child with severe malaria
- **Established Case Diagnosis:** Perforated duodenal ulcer in a 12-month-old child with severe malaria
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 12-month-old boy in Ghana with severe malaria and perforated duodenal ulcer (Input metadata: Age `0.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`SUSPECTED_POSSIBLE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Diagnostic workup note` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[825:873]`
    - **Verbatim Quote:** > "Neither Widal test nor stool cultures were done."
  - **Evidence Item 2:** `Empirical antibiotic therapy` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[966:1051]`
    - **Verbatim Quote:** > "Treatment of severe anaemia secondary to malaria and suspected typhoid was continued."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Empirical treatment included coverage for suspected typhoid without Widal or culture testing; exploratory laparotomy subsequently demonstrated an anterior duodenal ulcer perforation rather than typhoid ileal perforation.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 12-month-old boy with smear-positive malaria received empirical antibiotics covering suspected typhoid, but neither Widal test nor stool cultures were performed, and exploratory laparotomy revealed a perforated anterior duodenal ulcer -> EXCLUDED_NON_TARGET_CASE.


# Case 041: PMC9899929_01::Typhoid_Fever

- **Case ID:** `PMC9899929_01` | **Article ID:** `PMC9899929` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case report: Sarcomatoid urothelial carcinoma of the renal pelvis masquerading as a renal abscess
- **Established Case Diagnosis:** Sarcomatoid urothelial carcinoma of the renal pelvis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 71-year-old male with sarcomatoid urothelial carcinoma of the right renal pelvis masquerading as a renal abscess (Input metadata: Age `71.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[437:672]`
    - **Verbatim Quote:** > "Laboratory test results were as follows: white blood cell count 14.79 x 109 cells/L, urine occult blood (UOB) 1+, urinary leukocytes (U-LEU) 3+, erythrocyte sedimentation rate (ESR) 96 mm/h, urine bacterial culture (-), Widal test (-)."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 71-year-old man presenting with 20 days of fever and right flank pain had a negative Widal test and was diagnosed with sarcomatoid urothelial carcinoma of the right renal pelvis -> NEGATIVE.


# Case 042: PMC10070333_01::Typhoid_Fever

- **Case ID:** `PMC10070333_01` | **Article ID:** `PMC10070333` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Cervical epidural abscess complicated by a pharyngoesophageal perforation after anterior cervical spine surgery for subaxial spondylodiscitis
- **Established Case Diagnosis:** Cervical spondylodiscitis and epidural abscess due to Methicillin-Sensitive Staphylococcus aureus (MSSA)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 47-year-old woman with C4-C6 cervical spondylodiscitis and epidural abscess due to MSSA, later complicated by pharyngoesophageal perforation (Input metadata: Age `47.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood cultures and Widal test` | Target: `Salmonella Paratyphi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[779:944]`
    - **Verbatim Quote:** > "Blood cultures, Wright test, and tuber test were negative, while the Widal test was positive for antigen H of Salmonella paratyphi, expression of previous infection."
  - **Evidence Item 2:** `CT-guided epidural abscess biopsy culture` | Target: `Methicillin-Sensitive Staphylococcus aureus` | Specimen: `epidural abscess` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1506:1614]`
    - **Verbatim Quote:** > "A CT scan-guided biopsy of the collection resulted positive for Methicillin-Sensitive Staphylococcus Aureus."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Widal test was positive only for antigen H of Salmonella paratyphi, which the authors explicitly interpreted as an expression of previous infection; blood cultures were negative and CT-guided biopsy confirmed MSSA.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 47-year-old woman with cervical epidural abscess had negative blood cultures and an isolated Widal H-antigen positivity explicitly noted as an 'expression of previous infection', while CT-guided biopsy of the collection grew Methicillin-Sensitive Staphylococcus aureus -> NEGATIVE.


# Case 043: PMC9204269_01::Typhoid_Fever

- **Case ID:** `PMC9204269_01` | **Article ID:** `PMC9204269` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case Report: Metagenomic Next-Generation Sequencing Clinches the Diagnosis of Acute Q Fever and Verified by Indirect Immunofluorescence Assay
- **Established Case Diagnosis:** Acute Q fever (Coxiella burnetii)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 48-year-old man in Taizhou, China with acute Q fever (Coxiella burnetii) diagnosed by mNGS and confirmed by IFA (Input metadata: Age `48.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood culture and Widal test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2730:2945]`
    - **Verbatim Quote:** > "Other examinations, including blood culture, mycobacterial culture, Widal test, viral hepatitis markers, antinuclear antibody, antineutrophil cytoplasmic antibody, and thyroid function, all suggested no abnormality."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 48-year-old man with recurrent high fever had unremarkable blood culture and Widal test results, and was diagnosed with acute Q fever via peripheral blood mNGS and Coxiella burnetii IFA seroconversion -> NEGATIVE.


# Case 044: PMC7081463_01::Typhoid_Fever

- **Case ID:** `PMC7081463_01` | **Article ID:** `PMC7081463` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** An Unusual Etiology of Cerebellar Ataxia
- **Established Case Diagnosis:** Scrub typhus cerebellitis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 7-year-old girl from West Bengal with 15-day fever, cerebellar ataxia, and abducens nerve palsy due to scrub typhus cerebellitis (Input metadata: Age `7.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid test and blood culture` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3548:3767]`
    - **Verbatim Quote:** > "Tests for dengue and typhoid, Japanese encephalitis, Herpes simplex, and human immunodeficiency virus were performed as per routine investigations for fever, all of which were negative. Blood culture revealed no growth."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 7-year-old girl presenting with fever and acute cerebellar ataxia tested negative for typhoid and had no growth on blood culture, with positive serum and CSF Scrub typhus IgM confirming scrub typhus cerebellitis -> NEGATIVE.


# Case 045: PMC9897698_01::Typhoid_Fever

- **Case ID:** `PMC9897698_01` | **Article ID:** `PMC9897698` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Long-Segment Epidural Hemorrhage of the Cervical and Dorsal Spine: A Case Report of a Rare Complication of Dengue Virus Disease
- **Established Case Diagnosis:** Dengue virus disease with subarachnoid and long-segment spinal epidural hemorrhage
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 37-year-old male with dengue hemorrhagic fever complicated by subarachnoid hemorrhage and long-segment cervicodorsal spinal epidural hemorrhage (Input metadata: Age `37.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid serological test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[693:759]`
    - **Verbatim Quote:** > "Serological tests for malaria and typhoid infection were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 37-year-old male with dengue fever complicated by spinal epidural hemorrhage had negative serological tests for malaria and typhoid infection -> NEGATIVE.


# Case 046: PMC5833192_01::Typhoid_Fever

- **Case ID:** `PMC5833192_01` | **Article ID:** `PMC5833192` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Tubular Duplication of the Midgut Presenting with Acute Abdomen and Hematochezia: A Case Report from Northern Tanzania
- **Established Case Diagnosis:** Perforated tubular jejunoileal duplication of the midgut
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 3-year-old boy from Northern Tanzania with perforated tubular duplication of the midgut presenting with acute abdomen and hematochezia (Input metadata: Age `3.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1838:1866]`
    - **Verbatim Quote:** > "The Widal test was negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 3-year-old boy presenting with peritonitis and lower GI bleeding from a 90 cm jejunoileal enteric duplication had a negative Widal test -> NEGATIVE.


# Case 047: PMC6881760_01::Typhoid_Fever

- **Case ID:** `PMC6881760_01` | **Article ID:** `PMC6881760` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A Western Case of Intravascular Large B-Cell Lymphoma as Unusual Cause of Persistent Fever
- **Established Case Diagnosis:** Intravascular large B-cell lymphoma (IVLBCL)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 58-year-old Caucasian woman presenting with fever of unknown origin ultimately diagnosed at autopsy with intravascular large B-cell lymphoma (IVLBCL) (Input metadata: Age `58.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Salmonella typhi IgM serology` | Target: `Salmonella enterica serovar Typhi` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1018:1455]`
    - **Verbatim Quote:** > "Acute infectious diseases (hepatitis A, hepatitis B, hepatitis C, and hepatitis E virus, human immunodeficiency virus, cytomegalovirus, parvovirus B19, Epstein-Barr virus, echoviruses, poliovirus, coxsackieviruses, Treponema pallidum, Coxiella burnetii, Toxoplasma, Salmonella typhi, Legionella pneumophila, Mycoplasma pneumoniae, Leishmania donovani, Chlamydya, Brucella, Leptospira, Rickettsia, and Borrelia species IgM) were negative."
  - **Evidence Item 2:** `Blood, stool, and urine cultures for Salmonella` | Target: `Salmonella species` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2206:2358]`
    - **Verbatim Quote:** > "Bacterial (Salmonella, Shigella, and Campylobacter), mycobacterial, and parasitic culture obtained from blood, stool, and urinary samples were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 58-year-old woman evaluated for fever of unknown origin tested negative for Salmonella typhi IgM and negative on blood, stool, and urine cultures for Salmonella, with autopsy establishing intravascular large B-cell lymphoma -> NEGATIVE.


# Case 048: PMC10230527_01::Typhoid_Fever

- **Case ID:** `PMC10230527_01` | **Article ID:** `PMC10230527` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Pancytopenia in Carbamazepine Therapy: A Rare and Serious Entity with Simple Prevention
- **Established Case Diagnosis:** Carbamazepine-induced pancytopenia
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 29-year-old female with schizophrenia presenting with fever and carbamazepine-induced pancytopenia (Input metadata: Age `29.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1102:1188]`
    - **Verbatim Quote:** > "Malaria serology, dengue serology test, Widal test, and viral markers tested negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 29-year-old female with carbamazepine-induced pancytopenia and a 4-day fever tested negative on the Widal test -> NEGATIVE.


# Case 049: PMC5147401_01::Typhoid_Fever

- **Case ID:** `PMC5147401_01` | **Article ID:** `PMC5147401` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Bacteremia caused by a rare pathogen - Chromobacterium violaceum: a case report from Nepal
- **Established Case Diagnosis:** Chromobacterium violaceum bacteremia
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 36-year-old female in Kathmandu, Nepal with wound-related sepsis and Chromobacterium violaceum bacteremia after paddy field toe injury (Input metadata: Age `36.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Diagnostic workup ordered on admission` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1365:1579]`
    - **Verbatim Quote:** > "After necessary physical examination, blood and urine samples were collected aseptically for laboratory investigations viz blood culture, urine culture, hematology parameters, widal test, and blood chemistry tests."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 36-year-old woman with Chromobacterium violaceum bacteremia following a paddy-field toe injury had blood collected for routine investigations including a Widal test on admission, with no typhoid diagnosis or positive result reported -> EXCLUDED_NON_TARGET_CASE.


# Case 050: PMC4173377_01::Typhoid_Fever

- **Case ID:** `PMC4173377_01` | **Article ID:** `PMC4173377` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Takayasu's arteritis: Anesthetic significance and management of a patient for cesarean section using the epidural volume extension technique
- **Established Case Diagnosis:** Takayasu's arteritis type III in pregnancy managed with epidural volume extension anesthesia
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 23-year-old primigravida with Takayasu's arteritis type III undergoing emergency cesarean section (Input metadata: Age `23.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Past medical history` | Target: `Enteric fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[516:834]`
    - **Verbatim Quote:** > "A detailed cardiovascular evaluation, including a review of the angiography recorded for unexplained tachycardia and high BP recording (following an attack of enteric fever 5 years back), revealed 70% and 100% occlusion of the left and right renal artery, respectively, along with bilateral subclavian artery stenosis."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 23-year-old primigravida with Takayasu's arteritis had an incidental mention of prior angiography performed following 'an attack of enteric fever 5 years back'. This is remote resolved past history (`HISTORICAL_RESOLVED` / `PAST_HISTORY`) -> EXCLUDED_NON_TARGET_CASE.


# Case 051: PMC6214173_01::Typhoid_Fever

- **Case ID:** `PMC6214173_01` | **Article ID:** `PMC6214173` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Hyper IgE recurrent infection syndrome in South Asia: is there a different outcome?
- **Established Case Diagnosis:** Autosomal dominant Hyper IgE recurrent infection syndrome (STAT3 R382Q)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 5-year-old girl from South Asia with autosomal dominant Hyper IgE syndrome (STAT3 R382Q mutation) (Input metadata: Age `5.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Polysaccharide vaccine response assay` | Target: `Typhoid Vi vaccine` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[550:591]`
    - **Verbatim Quote:** > "The anti typhoid Vi vaccine was not done."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 5-year-old girl evaluated for Hyper IgE syndrome had a note that the anti-typhoid Vi vaccine (used to assess antipolysaccharide antibody response in immunodeficiency workups) was not done -> EXCLUDED_NON_TARGET_CASE.


# Case 052: PMC6214173_02::Typhoid_Fever

- **Case ID:** `PMC6214173_02` | **Article ID:** `PMC6214173` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Hyper IgE recurrent infection syndrome in South Asia: is there a different outcome?
- **Established Case Diagnosis:** Autosomal dominant Hyper IgE recurrent infection syndrome (STAT3 V637M)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 9-year-old girl from South Asia with autosomal dominant Hyper IgE syndrome (STAT3 V637M mutation) (Input metadata: Age `9.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Anti-typhoid Vi vaccine antibody response titer` | Target: `Typhoid Vi vaccine antibody` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[511:639]`
    - **Verbatim Quote:** > "Her serum immunoglobulins, isohemagglutinin titre, anti typhoid Vi antibody titre, lymphocyte subsets and NBT assay were normal."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 9-year-old girl evaluated for Hyper IgE syndrome had a normal anti-typhoid Vi antibody titer as part of her humoral immune competence evaluation (post-vaccination polysaccharide response), not a typhoid fever infection -> EXCLUDED_NON_TARGET_CASE.


# Case 053: PMC6214173_03::Typhoid_Fever

- **Case ID:** `PMC6214173_03` | **Article ID:** `PMC6214173` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Hyper IgE recurrent infection syndrome in South Asia: is there a different outcome?
- **Established Case Diagnosis:** Autosomal dominant Hyper IgE recurrent infection syndrome (STAT3 R382W)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 7-year-old girl from South Asia with autosomal dominant Hyper IgE syndrome (STAT3 R382W mutation) (Input metadata: Age `7.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Polysaccharide vaccine response assay` | Target: `Typhoid Vi vaccine` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[918:1029]`
    - **Verbatim Quote:** > "The anti-typhoid Vi vaccine was not performed as the patient died before the post vaccine sample was collected."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 7-year-old girl with Hyper IgE syndrome did not have the post-vaccination anti-typhoid Vi vaccine response test completed because she died prior to sample collection -> EXCLUDED_NON_TARGET_CASE.


# Case 054: PMC6214173_04::Typhoid_Fever

- **Case ID:** `PMC6214173_04` | **Article ID:** `PMC6214173` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Hyper IgE recurrent infection syndrome in South Asia: is there a different outcome?
- **Established Case Diagnosis:** Autosomal dominant Hyper IgE recurrent infection syndrome (STAT3 V637M)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 11-year-old boy from South Asia with autosomal dominant Hyper IgE syndrome (STAT3 V637M mutation) (Input metadata: Age `11.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Anti-typhoid Vi vaccine antibody response titer` | Target: `Typhoid Vi vaccine antibody` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[377:523]`
    - **Verbatim Quote:** > "His eosinophil count, serum immunoglobulins, isohemagglutinin titre, anti typhoid Vi antibody titre, lymphocyte subsets and NBT assay were normal."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** An 11-year-old boy evaluated for Hyper IgE syndrome had a normal anti-typhoid Vi antibody titer during humoral immunodeficiency evaluation -> EXCLUDED_NON_TARGET_CASE.


# Case 055: PMC5566360_01::Typhoid_Fever

- **Case ID:** `PMC5566360_01` | **Article ID:** `PMC5566360` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Early treatment failure in concurrent dengue and mixed malaria species infection with suspected resistance to artemisinin combination therapy from a tertiary care center in Delhi: a case report
- **Established Case Diagnosis:** Concurrent dengue fever and mixed Plasmodium vivax and Plasmodium falciparum malaria
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 17-year-old male in Delhi with concurrent dengue and mixed Plasmodium vivax / P. falciparum malaria (Input metadata: Age `17.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Initial differential diagnosis` | Target: `Enteric fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1171:1342]`
    - **Verbatim Quote:** > "On the basis of these findings, a provisional diagnosis of acute undifferentiated fever was made with a differential diagnosis of malaria, dengue fever, and enteric fever."
  - **Evidence Item 2:** `Tube Widal test` | Target: `Typhoid / Paratyphoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1824:1877]`
    - **Verbatim Quote:** > "Tube Widal test titers were <1:40 for TO, TH, and AH."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 17-year-old male had enteric fever considered in the differential diagnosis of acute undifferentiated fever, but tube Widal test titers were <1:40 for TO, TH, and AH, and PCR/serology confirmed mixed P. vivax + P. falciparum malaria and dengue coinfection -> NEGATIVE.


# Case 056: PMC4230886_01::Typhoid_Fever

- **Case ID:** `PMC4230886_01` | **Article ID:** `PMC4230886` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Clinical features and patient management of Lujo hemorrhagic fever
- **Established Case Diagnosis:** Lujo virus hemorrhagic fever
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 36-year-old white female from Lusaka, Zambia (index Patient 1 of the 2008 Lujo virus hemorrhagic fever outbreak) (Input metadata: Age `36.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood cultures and typhoid fever test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2806:2931]`
    - **Verbatim Quote:** > "Blood cultures remained negative, as well as tests for malaria, typhoid fever, brucellosis, syphilis, and autoimmune disease."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** The 36-year-old female index patient with Lujo hemorrhagic fever had negative blood cultures and negative tests for typhoid fever -> NEGATIVE.


# Case 057: PMC7468372_01::Typhoid_Fever

- **Case ID:** `PMC7468372_01` | **Article ID:** `PMC7468372` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Retinal Vasculitis with Macular Infarction: A Dengue-related Ophthalmic Complication
- **Established Case Diagnosis:** Dengue fever complicated by bilateral retinal vasculitis and right macular infarction
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 44-year-old male with bilateral retinal vasculitis and right macular infarction secondary to dengue fever (Input metadata: Age `44.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Clinical and laboratory fever evaluation` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[338:508]`
    - **Verbatim Quote:** > "During clinical evaluation and laboratory investigation for fever; typhoid, malaria, tuberculosis, syphilis, collagen vascular disease and bleeding disorders were absent."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 44-year-old man with dengue-related retinal vasculitis and macular infarction had typhoid, malaria, and tuberculosis excluded during clinical and laboratory investigation for fever -> NEGATIVE.


# Case 058: PMC6159304_01::Typhoid_Fever

- **Case ID:** `PMC6159304_01` | **Article ID:** `PMC6159304` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Endovascular management of a mycotic group A streptococcal abdominal aortic dissection
- **Established Case Diagnosis:** Mycotic Group A streptococcal abdominal aortic dissection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 58-year-old male returning from Kashmir with pyrexia, abdominal/back pain, and mycotic Group A streptococcal abdominal aortic dissection (Input metadata: Age `58.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Initial travel-related differential diagnosis` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[822:897]`
    - **Verbatim Quote:** > "A diagnosis of typhoid or malaria was suspected owing to his recent travel."
  - **Evidence Item 2:** `Peripheral blood culture` | Target: `Group A Streptococcus (excluding Salmonella Typhi)` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1123:1231]`
    - **Verbatim Quote:** > "Peripheral blood cultures taken on presentation grew group A streptococcus, the source of which was unclear."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Typhoid was initially suspected due to travel to Kashmir, but peripheral blood cultures grew Group A Streptococcus and CT revealed a mycotic abdominal aortic dissection.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 58-year-old man returning from Kashmir had typhoid suspected initially due to travel history, but peripheral blood cultures grew Group A Streptococcus and CT established a mycotic abdominal aortic dissection -> NEGATIVE.


# Case 059: PMC5366795_01::Typhoid_Fever

- **Case ID:** `PMC5366795_01` | **Article ID:** `PMC5366795` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Dengue and Scrub Typhus Coinfection in a Patient Presenting with Febrile Illness
- **Established Case Diagnosis:** Dengue and scrub typhus coinfection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 50-year-old female from Chitwan District, Nepal with dengue and scrub typhus coinfection (Input metadata: Age `50.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal agglutination test` | Target: `Salmonella typhi and Salmonella paratyphi` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2371:2598]`
    - **Verbatim Quote:** > "Further reports showed that IgM/IgG antibody for Leptospira was negative, IgM/IgG antibody for dengue was positive (method: immunochromatography), and Widal agglutination test for Salmonella typhi and S. paratyphi was negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 50-year-old woman with dengue and scrub typhus coinfection tested negative on the Widal agglutination test for Salmonella typhi and S. paratyphi -> NEGATIVE.


# Case 060: PMC5436409_01::Typhoid_Fever

- **Case ID:** `PMC5436409_01` | **Article ID:** `PMC5436409` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Biosafety level-2 laboratory diagnosis of Zaire Ebola virus disease imported from Liberia to Nigeria
- **Established Case Diagnosis:** Zaire Ebola virus disease (EVD)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 40-year-old Liberian man arriving in Lagos, Nigeria with imported Zaire Ebola virus disease (Input metadata: Age `40.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Empirical treatment non-response` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[325:694]`
    - **Verbatim Quote:** > "He presented with high fever, lymphadenopathy and sore throat and was treated for malaria and typhoid fever until he later developed diarrhoea, vomiting and microscopic haematuria. The culmination of the clinical presentation, the patient's non-response to treatment for malaria and typhoid, as well as his epidemiological link to Liberia, raised the suspicion for EVD."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Patient was initially treated empirically for malaria and typhoid fever upon arrival in Lagos, but non-response to treatment and progression of symptoms led to RT-PCR and sequencing confirmation of Zaire ebolavirus.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 40-year-old traveler from Liberia was initially treated empirically for malaria and typhoid fever without response; subsequent RT-PCR and sequencing confirmed Zaire Ebola virus disease -> NEGATIVE.


# Case 061: PMC2732535_01::Typhoid_Fever

- **Case ID:** `PMC2732535_01` | **Article ID:** `PMC2732535` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** First documentation of human Crimean-Congo hemorrhagic fever, Kenya
- **Established Case Diagnosis:** Crimean-Congo hemorrhagic fever (C-CHFV)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 25-year-old male farmer in western Kenya with fatal acute Crimean-Congo hemorrhagic fever (Input metadata: Age `25.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[637:785]`
    - **Verbatim Quote:** > "Results of a blood smear for malaria parasites and Widal test for typhoid were negative, and cerebrospinal fluid and urine examinations were normal."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 25-year-old Kenyan farmer presenting with fatal acute hemorrhagic illness had a negative Widal test for typhoid, and RT-PCR plus sequencing confirmed Crimean-Congo hemorrhagic fever virus -> NEGATIVE.


# Case 062: PMC9547605_01::Typhoid_Fever

- **Case ID:** `PMC9547605_01` | **Article ID:** `PMC9547605` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Omadacycline for the Treatment of Severe Chlamydia psittaci Pneumonia Complicated with Multiple Organ Failure: A Case Report
- **Established Case Diagnosis:** Severe Chlamydia psittaci pneumonia (psittacosis) with ARDS and multiple organ failure
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 62-year-old male farmer with severe Chlamydia psittaci pneumonia and multiple organ failure treated with omadacycline (Input metadata: Age `62.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and blood/sputum/BALF cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3997:4448]`
    - **Verbatim Quote:** > "During this period, the Widal test, Weil-Felix test, tuberculosis antibodies, anti-neutrophil cytoplasmic antibodies, and IgM antibodies for respiratory pathogens (Legionella pneumophila, Chlamydia pneumoniae, Mycoplasma pneumoniae, Q fever Rickettsia, adenovirus, respiratory syncytial virus, influenza A virus, influenza B virus, and parainfluenza virus) were all negative. The bacterial and fungal cultures of blood, phlegm, and BALF were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 62-year-old farmer with severe Chlamydia psittaci pneumonia diagnosed by BALF mNGS had negative Widal testing and negative bacterial cultures of blood, sputum, and BALF -> NEGATIVE.


# Case 063: PMC3294367_01::Typhoid_Fever

- **Case ID:** `PMC3294367_01` | **Article ID:** `PMC3294367` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Fluoroquinolone-resistant Salmonella Paratyphi A
- **Established Case Diagnosis:** Cholecystic infection/carriage of fluoroquinolone-resistant Salmonella enterica serovar Paratyphi A
- **Final Dataset Label:** `POSITIVE` (`decision`: `POSITIVE`) | **VPD Satisfied:** `True` | **Confidence:** `HIGH` | **Failure Flags:** `[]`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 87-year-old woman in Yokohama, Japan found to have cholecystic carriage/infection with highly fluoroquinolone-resistant Salmonella enterica serovar Paratyphi A (Input metadata: Age `87.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 3 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `AFFIRMED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PRIMARY_DIAGNOSIS` (`PRIMARY_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E1_DISEASE_SPECIFIC_CONFIRMATORY` (`E1_CONFIRMATORY`)
  - **Evidence Item 1:** `Urine culture` | Target: `Salmonella enterica serovar Paratyphi A` | Specimen: `urine` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E1_CONFIRMATORY`
    - **Offsets:** `case_text[0:182]`
    - **Verbatim Quote:** > "An 87-year-old woman was referred from a local clinic to Yokohama Municipal Citizen's Hospital in July 2002 because Salmonella enterica serovar Paratyphi A was detected in her urine."
  - **Evidence Item 2:** `Stool culture` | Target: `Salmonella enterica serovar Paratyphi A` | Specimen: `stool` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E1_CONFIRMATORY`
    - **Offsets:** `case_text[772:961]`
    - **Verbatim Quote:** > "S. Paratyphi A was not detected in the urine but was confirmed in the stool; therefore, the previous report of bacteriuria could have been due to contamination of a urine sample with feces."
  - **Evidence Item 3:** `Duodenal bile aspiration culture` | Target: `Salmonella enterica serovar Paratyphi A` | Specimen: `bile` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E1_CONFIRMATORY`
    - **Offsets:** `case_text[1062:1227]`
    - **Verbatim Quote:** > "Bile was obtained by duodenal aspiration and was positive for S. Paratyphi A. The patient was considered to be an asymptomatic cholecystic carrier of S. Paratyphi A."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = True` (`step8_case_definition = CONFIRMED`)
12. **Step 12 — Final Adjudication & Rationale:** `POSITIVE` (`POSITIVE`)
    - **Clinical Rationale:** An 87-year-old woman had Salmonella enterica serovar Paratyphi A isolated from stool and from bile obtained by duodenal aspiration (with gyrA and parC fluoroquinolone-resistance mutations characterized by PCR and sequencing), and was cured by open cholecystectomy. Under Section 5.9 (Typhoid Fever / Paratyphoid Fever), microbiological isolation of S. Paratyphi A from stool and duodenal bile across repeated specimens is E1 confirmatory -> POSITIVE.


# Case 064: PMC8732773_01::Typhoid_Fever

- **Case ID:** `PMC8732773_01` | **Article ID:** `PMC8732773` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Diffuse Large B-Cell Lymphoma of the Mandible Diagnosed by Metagenomic Sequencing: A Case Report
- **Established Case Diagnosis:** Diffuse large B-cell lymphoma (DLBCL) of the mandible
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 52-year-old female with recurrent fever for >1 month and left mandibular numbness diagnosed with primary mandibular diffuse large B-cell lymphoma (DLBCL) (Input metadata: Age `52.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood/urine cultures and Widal test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1555:1751]`
    - **Verbatim Quote:** > "Stool routine, blood transfusion routine, blood culture, urine culture, humoral immunity, Widal test, Ana antibody spectrum, antineutrophil cytoplasmic antibody, G test, and EBV-DNA were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 52-year-old woman presenting with recurrent fever and left jaw numbness had negative blood culture, urine culture, stool routine, and Widal test, and was diagnosed with mandibular diffuse large B-cell lymphoma -> NEGATIVE.


# Case 065: PMC4531755_01::Typhoid_Fever

- **Case ID:** `PMC4531755_01` | **Article ID:** `PMC4531755` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Pleural empyema due to Salmonella: a case report
- **Established Case Diagnosis:** Pleural empyema due to Salmonella group B
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `MEDIUM` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 70-year-old diabetic female in Korea presenting with right flank/chest pain and pleural empyema due to Salmonella group B (Input metadata: Age `70.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 3 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`SUSPECTED_POSSIBLE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Blood culture` | Target: `Salmonella group B (serovar not specified as Typhi/Paratyphi)` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[1705:1818]`
    - **Verbatim Quote:** > "On the third hospital day, urine culture yielded E. coli (>105 CFU) and blood culture yielded salmonella group B."
  - **Evidence Item 2:** `Widal test` | Target: `Salmonella agglutinins` | Specimen: `serum` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[1996:2176]`
    - **Verbatim Quote:** > "Widal test showed O agglutinin titer positive at 1:160, H agglutinin titer positive at 1:320, para A agglutinin titer positive at 1:40 and para B agglutinin titer positive at 1:80."
  - **Evidence Item 3:** `Pleural fluid culture` | Target: `Salmonella group B` | Specimen: `pleural fluid` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[3375:3424]`
    - **Verbatim Quote:** > "Pleural fluid culture yielded salmonella group B."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Blood and pleural fluid cultures grew 'salmonella group B' (which includes non-typhoidal serovars such as S. Typhimurium as well as S. Paratyphi B); however, the Widal para B titer was only 1:80 while O/H cross-reacted, and species/serovar confirmation of S. Typhi or S. Paratyphi was never established.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 70-year-old diabetic woman developed bacteremia and pleural empyema yielding 'salmonella group B' without species/serovar identification of Salmonella Typhi or Paratyphi (and para B agglutinin titer was only 1:80, with cross-reactive O/H agglutinins). Per Section 5.9, invasive non-typhoidal Salmonella infections are a major confusable disease and Widal testing is non-confirmatory; without serovar-specific identification of S. Typhi or S. Paratyphi, VPD for Typhoid_Fever is not satisfied -> EXCLUDED_NON_TARGET_CASE.


# Case 066: PMC3701398_01::Typhoid_Fever

- **Case ID:** `PMC3701398_01` | **Article ID:** `PMC3701398` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Clinically lesser known entity in India: A Report of two cases of Melioidosis
- **Established Case Diagnosis:** Disseminated melioidosis (Burkholderia pseudomallei)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 65-year-old diabetic male in India presenting with 2-month fever, cough, left lung consolidation, and bilateral ankle septic arthritis/cellulitis (Input metadata: Age `65.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 3 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Prior empirical treatment` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[157:257]`
    - **Verbatim Quote:** > "Two months earlier, he was treated for clinically suspected typhoid with no resolution of the fever."
  - **Evidence Item 2:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1384:1504]`
    - **Verbatim Quote:** > "acid-fast stain (AFB) from sputum carried out for 3 days, malarial antigen, Widal test, Urine culture were all negative."
  - **Evidence Item 3:** `Blood culture` | Target: `Burkholderia pseudomallei` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1924:2166]`
    - **Verbatim Quote:** > "Blood culture put up in the fully automated Bactec (Beckton and Dickinson) showed positivity on the third day and grew nonfermenting, oxidase-positive flat,dry, wrinkled colonies which were subsequently identified as Burkholderia pseudomallei"
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Patient had been treated 2 months earlier for clinically suspected typhoid without resolution of fever; on admission Widal test was negative and blood, endotracheal secretion, and ankle pus cultures grew Burkholderia pseudomallei.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 65-year-old diabetic male previously treated for clinically suspected typhoid without resolution tested negative on Widal testing, and cultures of blood, endotracheal secretions, and ankle pus isolated Burkholderia pseudomallei -> NEGATIVE.


# Case 067: PMC3701398_02::Typhoid_Fever

- **Case ID:** `PMC3701398_02` | **Article ID:** `PMC3701398` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Clinically lesser known entity in India: A Report of two cases of Melioidosis
- **Established Case Diagnosis:** Disseminated melioidosis (Burkholderia pseudomallei)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 58-year-old diabetic male in India presenting with intermittent fever, bilateral nodular lung opacities, and left knee arthritis (Input metadata: Age `58.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[975:1065]`
    - **Verbatim Quote:** > "Sputum for AFB (stain and culture), Malaria antigen test and Widal test were all negative."
  - **Evidence Item 2:** `Blood cultures` | Target: `Burkholderia pseudomallei` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1238:1306]`
    - **Verbatim Quote:** > "Burkholderia pseudomallei was isolated from all these blood samples."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 58-year-old diabetic male with fever, pulmonary nodules, and knee arthritis had a negative Widal test and multiple blood cultures isolating Burkholderia pseudomallei -> NEGATIVE.


# Case 068: PMC3959514_01::Typhoid_Fever

- **Case ID:** `PMC3959514_01` | **Article ID:** `PMC3959514` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Splenic abscess due to chronic melioidosis in a patient previously misdiagnosed as tuberculosis
- **Established Case Diagnosis:** Splenic abscess due to chronic melioidosis (Burkholderia pseudomallei)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 47-year-old Indian diabetic male with splenic abscess due to chronic melioidosis (Input metadata: Age `47.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Enteric fever screen` | Target: `Enteric fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2654:2734]`
    - **Verbatim Quote:** > "Infectious screen was negative for enteric fever, malaria and brucella serology."
  - **Evidence Item 2:** `Blood, sputum, and urine cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3234:3280]`
    - **Verbatim Quote:** > "Blood, sputum and urine cultures were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 47-year-old diabetic man with a splenic abscess had a negative infectious screen for enteric fever and sterile blood cultures, while splenic abscess aspirate culture isolated Burkholderia pseudomallei -> NEGATIVE.


# Case 069: PMC4989586_01::Typhoid_Fever

- **Case ID:** `PMC4989586_01` | **Article ID:** `PMC4989586` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Delirium as presenting symptom of neuro-Behcet's disease
- **Established Case Diagnosis:** Neuro-Behcet's disease presenting with acute delirium and bilateral thalamic lesions
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 30-year-old married female presenting with fever, progressive headache, acute delirium, and bilateral thalamic lesions due to neuro-Behcet's disease (Input metadata: Age `30.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1156:1227]`
    - **Verbatim Quote:** > "Widal test for typhoid and Wright test for Brucella were both negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 30-year-old woman presenting with fever and acute delirium had a negative Widal test for typhoid and was diagnosed with neuro-Behcet's disease -> NEGATIVE.


# Case 070: PMC10244548_01::Typhoid_Fever

- **Case ID:** `PMC10244548_01` | **Article ID:** `PMC10244548` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Microscopic polyangiitis initially presenting with idiopathic pulmonary fibrosis: a case report
- **Established Case Diagnosis:** Microscopic polyangiitis (MPA) initially presenting as idiopathic pulmonary fibrosis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 69-year-old male with a 10-year history of pulmonary fibrosis developing fever of unknown origin, hematuria, and MPO-ANCA-positive microscopic polyangiitis (Input metadata: Age `69.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3262:3461]`
    - **Verbatim Quote:** > "The microbiological analysis for induced sputum, 1,3-beta-D-glucan test, Widal test, Weil-Felix test, mycoplasma pneumoniae antibodies, chlamydia antibody and Legionella antibodies were all negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 69-year-old man evaluated for 3 months of intermittent fever had a negative Widal test and tested positive for MPO-ANCA, establishing microscopic polyangiitis -> NEGATIVE.


# Case 071: PMC9868268_01::Typhoid_Fever

- **Case ID:** `PMC9868268_01` | **Article ID:** `PMC9868268` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** The successful treatment of Enterocytozoon bieneusi Microsporidiosis with nitazoxanide in a patient with B-ALL: A Case Report
- **Established Case Diagnosis:** Enterocytozoon bieneusi microsporidiosis in a patient with B-cell acute lymphoblastic leukemia
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 47-year-old male with B-ALL on maintenance chemotherapy presenting with chronic watery diarrhea and fever due to Enterocytozoon bieneusi microsporidiosis (Input metadata: Age `47.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Stool/urine/blood cultures and Widal test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1811:2085]`
    - **Verbatim Quote:** > "Stool routine, urine routine, stool culture, urine culture, blood culture, Widal test, waffian reaction, anti-nuclear antibody, anticardiolipin antibody, antineutrophil cytoplasmic antibody, G and GM test, T-spot TB test, EB virus, and cytomegalovirus DNA were all negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 47-year-old man with B-ALL presenting with chronic diarrhea and fever had negative stool, urine, and blood cultures and a negative Widal test, with peritoneal fluid mNGS identifying Enterocytozoon bieneusi -> NEGATIVE.


# Case 072: PMC6458662_01::Typhoid_Fever

- **Case ID:** `PMC6458662_01` | **Article ID:** `PMC6458662` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Lifelong immunoglobulin replacement is not always necessary: A case description of a patient with recurrent infections and hypogammaglobulinemia
- **Established Case Diagnosis:** Transient secondary humoral immunodeficiency (IgG1/IgG2 hypogammaglobulinemia) in pregnancy
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 39-year-old woman with transient secondary hypogammaglobulinemia (IgG1 and IgG2 subclass deficiency) diagnosed during pregnancy (Input metadata: Age `39.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Vaccine-response IgG assay availability note` | Target: `Salmonella typhi IgG antibody (PID evaluation)` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[2216:2430]`
    - **Verbatim Quote:** > "Unfortunately, despite the importance of the determination of antibodies against Salmonella typhi in the IgG class in the diagnosis of PID, this test was not available in the hospital where the patient was staying."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 39-year-old woman evaluated for hypogammaglobulinemia during pregnancy had no clinical suspicion of typhoid fever; the text only notes that anti-Salmonella typhi IgG testing (used to evaluate polysaccharide vaccine response in primary immunodeficiency) was unavailable at the hospital -> EXCLUDED_NON_TARGET_CASE.


# Case 073: PMC5337772_01::Typhoid_Fever

- **Case ID:** `PMC5337772_01` | **Article ID:** `PMC5337772` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Kikuchi-Fujimoto Disease: A Rare Presentation with Localized Iliac Lymphadenitis
- **Established Case Diagnosis:** Kikuchi-Fujimoto disease (histiocytic necrotizing lymphadenitis)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 32-year-old male from Gwalior, India with 1-month high-grade fever and localized iliac/mesenteric lymphadenitis diagnosed as Kikuchi-Fujimoto disease (Input metadata: Age `32.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1760:2028]`
    - **Verbatim Quote:** > "The patient was further subjected to a full FUO workup, including blood tests for malarial antigen as well as parasite, Widal test, dengue serology, leptospira serology, scrub-typhus serology and RPR for syphilis. All these tests as well as Mantoux test were negative."
  - **Evidence Item 2:** `Blood cultures (3 sets)` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2083:2186]`
    - **Verbatim Quote:** > "Blood cultures were taken on three different occasions from three different sites and all were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 32-year-old man evaluated for fever of unknown origin had a negative Widal test and three sterile blood cultures, with laparoscopic excisional biopsy of iliac lymph nodes confirming Kikuchi-Fujimoto disease -> NEGATIVE.


# Case 074: PMC3542945_01::Typhoid_Fever

- **Case ID:** `PMC3542945_01` | **Article ID:** `PMC3542945` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** An unusual presentation of ovarian teratoma: a case report
- **Established Case Diagnosis:** Left ovarian mature cystic teratoma rupturing into the sigmoid colon causing perforation peritonitis
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 18-year-old female presenting with perforation peritonitis caused by a left ovarian mature cystic teratoma rupturing into the sigmoid colon (Input metadata: Age `18.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Past medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[198:297]`
    - **Verbatim Quote:** > "There was history of typhoid fever four months back for which she received treatment and recovered."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** An 18-year-old female presenting with perforation peritonitis from an ovarian dermoid cyst rupturing into the sigmoid colon had a resolved history of typhoid fever 4 months earlier ('received treatment and recovered'). Because this is a resolved historical infection (`HISTORICAL_RESOLVED` / `PAST_HISTORY`), VPD is not satisfied -> EXCLUDED_NON_TARGET_CASE.


# Case 075: PMC8381346_01::Typhoid_Fever

- **Case ID:** `PMC8381346_01` | **Article ID:** `PMC8381346` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Trichrome-positive intrahepatic cytoplasmic globules are potential histopathological clue for COVID-19-induced hepatitis: a case report
- **Established Case Diagnosis:** Post-COVID-19-associated hepatitis in a child with autoimmune hemolytic anemia
- **Final Dataset Label:** `UNRESOLVED` (`decision`: `INCONCLUSIVE_DATA`) | **VPD Satisfied:** `False` | **Confidence:** `LOW` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 12-year-old girl with a 5-year history of autoimmune hemolytic anemia (AIHA) developing fever and severe hepatitis attributed to post-COVID-19 hepatitis (Input metadata: Age `12.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`SUSPECTED_POSSIBLE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Widal test and stool culture` | Target: `Salmonella typhi / Paratyphi A` | Specimen: `stool` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[368:570]`
    - **Verbatim Quote:** > "Microbiological investigations including Widal test and stool culture were negative for any infection except for salmonella typhi a, and the patient received cephalosporin, with no improvement of fever."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — The text states 'Microbiological investigations including Widal test and stool culture were negative for any infection except for salmonella typhi a, and the patient received cephalosporin, with no improvement of fever'; it is ambiguous whether 'salmonella typhi a' reflects a Widal agglutinin titer or stool culture, the patient had no GI symptoms, failed cephalosporin therapy, and liver biopsy plus SARS-CoV-2 IgG established post-COVID-19 hepatitis.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = SUSPECTED`)
12. **Step 12 — Final Adjudication & Rationale:** `UNRESOLVED` (`INCONCLUSIVE_DATA`)
    - **Clinical Rationale:** A 12-year-old girl with AIHA developed fever on day 60 of admission without respiratory or GI symptoms. The text states 'Microbiological investigations including Widal test and stool culture were negative for any infection except for salmonella typhi a, and the patient received cephalosporin, with no improvement of fever', before liver biopsy and SARS-CoV-2 IgG established COVID-19-induced hepatitis. Because the phrasing conflates Widal and stool culture ('salmonella typhi a') and cephalosporin failed to improve the fever, clinical certainty is insufficient -> UNRESOLVED (LOW confidence).


# Case 076: PMC8213119_01::Typhoid_Fever

- **Case ID:** `PMC8213119_01` | **Article ID:** `PMC8213119` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Pancytopenia with hemophagocytic lymphohistiocytosis in Plasmodium falciparum: A unusual presentation
- **Established Case Diagnosis:** Plasmodium falciparum malaria-associated secondary hemophagocytic lymphohistiocytosis (sHLH)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 6-year-old female child with pancytopenia and secondary hemophagocytic lymphohistiocytosis (sHLH) due to Plasmodium falciparum malaria (Input metadata: Age `6.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Fever workup including typhoid serology and blood culture` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1096:1667]`
    - **Verbatim Quote:** > "Due to persistent high-grade fever, fever workup, including rapid malarial antigen test, peripheral smear for malaria parasite, serology for typhoid and rickettsial infection, blood culture, etc., as well as a supportive workup for hemophagocytic lymphohistiocytosis (HLH) (liver transaminases, lactate dehydrogenase, triglyceride, serum ferritin, and fibrinogen) were sent [Table 1]. In peripheral smear, malaria parasite was seen as trophozoites for Pf malaria and revised the diagnosis as malaria-associated secondary HLH (sHLH) and the anti-malarial drug was started."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 6-year-old girl had typhoid serology and blood culture sent as part of a fever workup; peripheral smear identified Plasmodium falciparum trophozoites and she recovered completely on antimalarial therapy -> NEGATIVE.


# Case 077: PMC3284420_01::Typhoid_Fever

- **Case ID:** `PMC3284420_01` | **Article ID:** `PMC3284420` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Epstein-Barr virus co-infection in a patient with dengue fever presenting with post-infectious cerebellitis: a case report
- **Established Case Diagnosis:** Post-infectious cerebellitis associated with dengue virus and Epstein-Barr virus coinfection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 43-year-old Sri Lankan man with dengue fever and Epstein-Barr virus coinfection presenting with acute post-infectious cerebellitis (Input metadata: Age `43.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Salmonella typhi and paratyphi serology` | Target: `Salmonella Typhi / Paratyphi` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[4907:4976]`
    - **Verbatim Quote:** > "Serological studies for Salmonella typhi and paratyphi were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 43-year-old man with post-infectious cerebellitis secondary to dengue and EBV coinfection had negative serological studies for Salmonella typhi and paratyphi -> NEGATIVE.


# Case 078: PMC6592131_01::Typhoid_Fever

- **Case ID:** `PMC6592131_01` | **Article ID:** `PMC6592131` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A Pediatric Case of Antibiotic-Associated Hemorrhagic Colitis Caused by Klebsiella Oxytoca
- **Established Case Diagnosis:** Klebsiella oxytoca antibiotic-associated hemorrhagic colitis
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 5.5-year-old boy treated empirically for typhoid fever in Nigeria who developed Klebsiella oxytoca antibiotic-associated hemorrhagic colitis (Input metadata: Age `5.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `RECENT_EPISODIC` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Outside hospital clinical diagnosis and antibiotic administration` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[76:440]`
    - **Verbatim Quote:** > "Watery diarrhea and fever had begun 14 days before, and he admitted to Nisa Hospital in Nigeria for more evaluation. Intravenous (IV) ceftriaxone and then ciprofloxacin were administered for him by diagnosis of typhoid fever. After 48 hours, bloody diarrhea appeared and colonoscopy was done for him, which showed membranous colitis; so antibiotic was discontinued"
  - **Evidence Item 2:** `Stool culture` | Target: `Klebsiella oxytoca` | Specimen: `stool` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1314:1475]`
    - **Verbatim Quote:** > "Stool culture only showed pure klebsiella [Figure 1]. In further investigation, indole was positive [Figure 2], and klebsiella oxytoca colitis was the diagnosis."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Child received IV ceftriaxone and ciprofloxacin at an outside hospital in Nigeria for an unconfirmed diagnosis of typhoid fever, which precipitated antibiotic-associated hemorrhagic colitis; stool culture grew pure Klebsiella oxytoca and symptoms resolved after stopping antibiotics.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 5.5-year-old boy was given ceftriaxone and ciprofloxacin at an outside hospital for an unverified diagnosis of typhoid fever, precipitating hemorrhagic colitis; stool culture grew pure Klebsiella oxytoca and symptoms resolved upon discontinuing antibiotics. Per Section 8, prior empirical antibiotic treatment without microbiological confirmation does not establish typhoid fever -> EXCLUDED_NON_TARGET_CASE.


# Case 079: PMC4967050_02::Typhoid_Fever

- **Case ID:** `PMC4967050_02` | **Article ID:** `PMC4967050` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** How to communicate climate change 'impact and solutions' to vulnerable population of Indian Sundarbans? From theory to practice
- **Established Case Diagnosis:** Non-clinical socio-environmental climate change adaptation study in the Indian Sundarbans
- **Final Dataset Label:** `EXCLUDED_NON_SINGLE_PATIENT` (`decision`: `EXCLUDED_NON_CASE_REPORT`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `METHODOLOGICAL_PAPER` (`EXCLUDED_NON_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `NON_CLINICAL_DOCUMENT` (`AGGREGATE_STUDY_UNIT`)
3. **Step 3 — Patient Anchor:** No human patient (community socio-environmental climate change adaptation project involving 2,100 families in the Indian Sundarbans) (Input metadata: Age `0.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `FUTURE_CONDITIONAL` (`UNKNOWN`)
8. **Step 8 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Environmental disaster risk discussion` | Target: `Typhoid fever` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `UNKNOWN` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[9151:9410]`
    - **Verbatim Quote:** > "Lastly, the deaths of livestock animal/fresh water fishes due to drowning and purification of their flesh contaminate the fresh water sources resulting in epidemics like Cholera/Typhoid/dysentery and other water borne diseases amongst the stranded population."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_SINGLE_PATIENT` (`EXCLUDED_NON_CASE_REPORT`)
    - **Clinical Rationale:** This article is a non-clinical community-level socio-environmental study of 2,100 families in the Indian Sundarbans (`NON_CLINICAL_DOCUMENT` / `AGGREGATE_STUDY_UNIT`), mentioning 'Cholera/Typhoid/dysentery' only as potential post-cyclone water-borne epidemics -> EXCLUDED_NON_SINGLE_PATIENT.


# Case 080: PMC7530217_01::Typhoid_Fever

- **Case ID:** `PMC7530217_01` | **Article ID:** `PMC7530217` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Splenic abscess complicated by pleural empyema: A rare case report from rural Nepal
- **Established Case Diagnosis:** Splenic abscess complicated by Streptococcus pyogenes pleural empyema
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 39-year-old male chronic alcoholic in rural Nepal with splenic abscess complicated by left pleural empyema due to Streptococcus pyogenes (Input metadata: Age `39.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and stool examination` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1491:1542]`
    - **Verbatim Quote:** > "Stool examination along with WIDAL test was normal."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 39-year-old man with a splenic abscess and Streptococcus pyogenes pleural empyema had a normal Widal test and stool examination -> NEGATIVE.


# Case 081: PMC4352732_01::Typhoid_Fever

- **Case ID:** `PMC4352732_01` | **Article ID:** `PMC4352732` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Myocarditis leading to severe dilated cardiomyopathy in a patient with dengue Fever
- **Established Case Diagnosis:** Dengue virus serotype 3 (DEN-3) myocarditis and severe dilated cardiomyopathy
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 44-year-old male with fatal dilated cardiomyopathy secondary to dengue virus serotype 3 (DEN-3) myocarditis (Input metadata: Age `44.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood cultures and typhoid serology` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3804:3974]`
    - **Verbatim Quote:** > "Blood cultures, ESR, hepatitis panel, thyroid profile, and urine drug screen were all within normal limits. Malarial antigen test and typhoid serology were also negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 44-year-old male with RT-PCR-confirmed DEN-3 dengue myocarditis and dilated cardiomyopathy had normal blood cultures and negative typhoid serology -> NEGATIVE.


# Case 082: PMC3960813_01::Typhoid_Fever

- **Case ID:** `PMC3960813_01` | **Article ID:** `PMC3960813` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Visceral leishmaniasis with pleural effusion in an immunocompetent patient
- **Established Case Diagnosis:** Visceral leishmaniasis (Leishmania donovani) with pleural effusion
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 62-year-old immunocompetent male from West Bengal presenting with cough, chest pain, pleural effusion, and visceral leishmaniasis (Input metadata: Age `62.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Enteric fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1899:1972]`
    - **Verbatim Quote:** > "Widal test for enteric fever and test for malaria antigens were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 62-year-old man with visceral leishmaniasis confirmed by bone marrow aspiration had a negative Widal test for enteric fever -> NEGATIVE.


# Case 083: PMC2822302_01::Typhoid_Fever

- **Case ID:** `PMC2822302_01` | **Article ID:** `PMC2822302` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Molecular analysis of X-linked chronic granulomatous disease in five unrelated Korean patients
- **Established Case Diagnosis:** X-linked chronic granulomatous disease (CYBB gene defect)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`HISTORICAL_NOTE`)
3. **Step 3 — Patient Anchor:** 12-year-old Korean boy (Patient 2) with X-linked chronic granulomatous disease (CYBB mutation) (Input metadata: Age `12.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Historical summary of lifetime infections` | Target: `Group B Salmonella spp. enteric fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[0:354]`
    - **Verbatim Quote:** > "Patient 2 was a 12-yr-old boy who had suffered from many infectious diseases since 2 months after birth, including recurrent subcutaneous abscesses caused by K. pneumoniae, Enterobacter aerogenes, and Serratia marcescens, enteric fever by group B Salmonella spp., pneumonia by Haemophilus influenzae and Staphylococcus aureus, liver abscess by S. aureus."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** Patient 2, a 12-year-old boy in a molecular genetics study of X-linked chronic granulomatous disease, had a lifetime history since 2 months of age of multiple infections including 'enteric fever by group B Salmonella spp.' Both because this is a cumulative historical summary (`HISTORICAL_RESOLVED` / `PAST_HISTORY`) and because only generic 'group B Salmonella spp.' (not confirmed S. Typhi/Paratyphi) is stated, VPD is not satisfied -> EXCLUDED_NON_TARGET_CASE.


# Case 084: PMC2822302_02::Typhoid_Fever

- **Case ID:** `PMC2822302_02` | **Article ID:** `PMC2822302` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Molecular analysis of X-linked chronic granulomatous disease in five unrelated Korean patients
- **Established Case Diagnosis:** X-linked chronic granulomatous disease (CYBB gene defect)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`HISTORICAL_NOTE`)
3. **Step 3 — Patient Anchor:** 22-year-old Korean man (Patient 3) with X-linked chronic granulomatous disease (CYBB mutation) (Input metadata: Age `22.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E3_SUPPORTIVE`)
  - **Evidence Item 1:** `Historical summary of lifetime infections since age 6` | Target: `Group B Salmonella spp.` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[0:341]`
    - **Verbatim Quote:** > "Patient 3 was a 22-yr-old man who had suffered from tuberculosis, lymphadenitis, hepatitis, enteric fever, meningitis, and Behcet's disease since he was 6 yr old. The following bacterial species were isolated: group B Salmonella spp. in his blood, liver biopsy and stool; coagulase negative Staphylococcus in bile; and Enterococcus in urine."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** Patient 3, a 22-year-old man in a genetic study of X-linked chronic granulomatous disease, had a cumulative past medical history since age 6 years of multiple conditions including 'enteric fever' with 'group B Salmonella spp.' isolated. Because the infection is historical (`HISTORICAL_RESOLVED` / `PAST_HISTORY`) and only generic group B Salmonella spp. (without species/serovar confirmation of S. Typhi or S. Paratyphi) is listed, VPD is not satisfied -> EXCLUDED_NON_TARGET_CASE.


# Case 085: PMC8068525_01::Typhoid_Fever

- **Case ID:** `PMC8068525_01` | **Article ID:** `PMC8068525` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Rituximab Treatment in Acute Disseminated Encephalomyelitis Associated with Salmonella Infection
- **Established Case Diagnosis:** Refractory acute disseminated encephalomyelitis (ADEM) associated with positive Widal titer
- **Final Dataset Label:** `UNRESOLVED` (`decision`: `INCONCLUSIVE_DATA`) | **VPD Satisfied:** `False` | **Confidence:** `LOW` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 17-year-old girl with refractory acute disseminated encephalomyelitis (ADEM) treated with rituximab (Input metadata: Age `17.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `POSSIBLE_HYPOTHETICAL` (`SUSPECTED_POSSIBLE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `ACTIVE_COMORBIDITY` (`SECONDARY_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E3_SUPPORTIVE_NON_SPECIFIC` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood/urine cultures and Gruber-Widal test` | Target: `Salmonella enterica serovar Typhi` | Specimen: `serum` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[2273:2428]`
    - **Verbatim Quote:** > "Blood and urine cultures were also negative. The Gruber-Widal test result was positive, with a Salmonella typhi O antigen titer of 1/160 (control as 1/80)."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Blood and urine cultures were negative; the association with Salmonella infection was based solely on a single Gruber-Widal Salmonella typhi O antigen titer of 1:160, which is E0/weak evidence under Typhoid Fever specificity rules.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = SUSPECTED`)
12. **Step 12 — Final Adjudication & Rationale:** `UNRESOLVED` (`INCONCLUSIVE_DATA`)
    - **Clinical Rationale:** A 17-year-old girl with severe refractory ADEM had negative blood, urine, and CSF cultures, and was linked to Salmonella infection solely on the basis of a Gruber-Widal Salmonella typhi O antigen titer of 1:160. Per Section 5.9 of the Evidence Specificity Matrix, the Widal test alone is E0/weak evidence (not recommended due to false-positive rates) and cannot satisfy E1/E2 confirmation for a strict positive diagnosis -> UNRESOLVED (LOW confidence).


# Case 086: PMC3101735_02::Typhoid_Fever

- **Case ID:** `PMC3101735_02` | **Article ID:** `PMC3101735` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A rare human infection of Raoultella ornithinolytica in a diabetic foot lesion
- **Established Case Diagnosis:** Raoultella ornithinolytica diabetic foot infection (literature review section)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F1_LEXICAL_HOMONYM', 'F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `SYSTEMATIC_REVIEW` (`EXCLUDED_NON_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `MULTI_PATIENT_CASE_SERIES` (`AGGREGATE_STUDY_UNIT`)
3. **Step 3 — Patient Anchor:** Literature review excerpt describing 3 prior published cases of Raoultella ornithinolytica infection alongside a diabetic foot wound discussion (Input metadata: Age `82.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `NON_TARGET_CONCEPT`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Literature review description of Raoultella ornithinolytica` | Target: `Raoultella ornithinolytica (enteric fever-like syndrome)` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[355:504]`
    - **Verbatim Quote:** > "The first patient was an 82-year-old woman in whom the microorganism caused an enteric fever-like syndrome, and the organism was isolated from blood."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** This text segment summarizes three previously published literature cases of Raoultella ornithinolytica infection, noting that in the first literature patient (an 82-year-old woman) R. ornithinolytica caused an 'enteric fever-like syndrome'. It neither describes a single primary patient episode nor refers to Salmonella Typhi/Paratyphi -> EXCLUDED_NON_TARGET_CASE.


# Case 087: PMC6454994_01::Typhoid_Fever

- **Case ID:** `PMC6454994_01` | **Article ID:** `PMC6454994` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Long-term response of metastatic renal clear cell carcinoma following a subcutaneous injection of mixed bacterial vaccine: a case report
- **Established Case Diagnosis:** Metastatic renal clear cell carcinoma treated with mixed bacterial vaccine immunotherapy
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 56-year-old Chinese male with metastatic renal clear cell carcinoma treated with subcutaneous mixed bacterial vaccine (MBV) (Input metadata: Age `56.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Mixed bacterial vaccine (MBV) composition` | Target: `Heat-inactivated Typhoid and Paratyphoid A/B bacilli` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[1859:2278]`
    - **Verbatim Quote:** > "The MBV includes 6 kinds of heat-inactivated bacteria, namely 1) Pertussis bacillus (concentration 9 billion/mL), 2) Diphtheria bacillus endotoxin (concentration 20 Lf/mL), 3) Tetanus bacillus endotoxin (concentration 5 Lf/mL), 4) Typhoid bacillus (concentration of 300 million/mL), 5) Bacillus paratyphoid A/B (concentration 150 million/mL each), and 6) 10% Staphylococcus aureus solution (concentration 1 billion/mL)."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 56-year-old man with metastatic renal clear cell carcinoma received immunotherapy with a mixed bacterial vaccine (MBV) containing heat-inactivated Typhoid bacillus and Bacillus paratyphoid A/B. Vaccine/immunotherapy administration is not typhoid fever infection (`PREVENTION_VACCINATION`) -> EXCLUDED_NON_TARGET_CASE.


# Case 088: PMC10183597_01::Typhoid_Fever

- **Case ID:** `PMC10183597_01` | **Article ID:** `PMC10183597` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case Report: Atrial myxoma combined with hyperthyroidism in an adolescent with literature review
- **Established Case Diagnosis:** Left atrial myxoma with cerebral embolism and Graves' disease
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 15-year-old female adolescent with Graves' disease presenting with acute cerebral embolism and lower extremity rash due to left atrial myxoma (Input metadata: Age `15.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `DIFFERENTIAL_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Clinical differential diagnosis of rash` | Target: `Typhoid spotted rash` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[3108:3592]`
    - **Verbatim Quote:** > "The differential diagnosis of red rash includes infectious diseases (measles, rubella, scarlet fever, typhoid spotted rash, septicemia), immune system diseases (kawasaki disease, allergic purpura), hematologic diseases (infectious mononucleosis, thrombocytopenic purpura) and allergic reactive diseases (urticaria, eczema, drug rashes). It was determined to be secondary to either micro-embolic phenomena or vasospasm in combination with the rheumatology and dermatology consultation."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 15-year-old girl with left atrial myxoma and recurrent lower extremity rash had 'typhoid spotted rash' listed generically in the textbook differential diagnosis of red rash, which was determined to be secondary to micro-emboli/vasospasm from her atrial myxoma -> EXCLUDED_NON_TARGET_CASE.


# Case 089: PMC7344764_01::Typhoid_Fever

- **Case ID:** `PMC7344764_01` | **Article ID:** `PMC7344764` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Uncommon cause of fever in a child with steroid-dependent nephrotic syndrome
- **Established Case Diagnosis:** Mixed Mycoplasma pneumoniae and cytomegalovirus (CMV) infection in steroid-dependent nephrotic syndrome
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 3-year-old girl with steroid-dependent nephrotic syndrome presenting with 2-week fever due to mixed Mycoplasma pneumoniae and CMV infection (Input metadata: Age `3.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood and urine cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1587:1693]`
    - **Verbatim Quote:** > "At presentation, two sets of blood and urine cultures were sent for analysis, and they reported no growth."
  - **Evidence Item 2:** `Typhoid serologic testing` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1695:1776]`
    - **Verbatim Quote:** > "Serologic testing for dengue, malaria, typhoid, and rickettsia were non-reactive."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 3-year-old girl with steroid-dependent nephrotic syndrome evaluated for prolonged fever had two negative sets of blood and urine cultures and non-reactive serologic testing for typhoid -> NEGATIVE.


# Case 090: PMC3371802_01::Typhoid_Fever

- **Case ID:** `PMC3371802_01` | **Article ID:** `PMC3371802` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Concurrent dengue and malaria
- **Established Case Diagnosis:** Concurrent Plasmodium falciparum malaria and dengue virus serotype 3 infection
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 37-year-old French woman returning from West Africa with concurrent Plasmodium falciparum malaria and dengue virus serotype 3 infection (Input metadata: Age `37.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `UNCERTAIN` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `UNKNOWN` (`UNKNOWN`)
8. **Step 8 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Literature review discussion of dengue coinfections` | Target: `Salmonella enterica serovar Typhi` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `UNKNOWN` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[4185:4369]`
    - **Verbatim Quote:** > "Only 6 published studies reported concurrent infection with dengue virus and a bacterium (Salmonella typhi, Shigella sonnei, Leptospira spp.) or with a virus such as Chikungunya virus."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 37-year-old woman was diagnosed with concurrent Plasmodium falciparum malaria and dengue virus type 3 infection; Salmonella typhi is mentioned solely in the literature review paragraph summarizing prior published studies of dengue-bacterial coinfections -> EXCLUDED_NON_TARGET_CASE.


# Case 091: PMC8132842_01::Typhoid_Fever

- **Case ID:** `PMC8132842_01` | **Article ID:** `PMC8132842` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case report of infective spondylodiscitis due to nalidixic acid-resistant Salmonella paratyphi A
- **Established Case Diagnosis:** Thoracic infective spondylodiscitis (T11-T12) due to nalidixic acid-resistant Salmonella Paratyphi A
- **Final Dataset Label:** `POSITIVE` (`decision`: `POSITIVE`) | **VPD Satisfied:** `True` | **Confidence:** `HIGH` | **Failure Flags:** `[]`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 57-year-old male banker with 6-week high-grade fever and 4-week severe backache diagnosed with T11-T12 infective spondylodiscitis due to nalidixic acid-resistant Salmonella paratyphi A (Input metadata: Age `57.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `AFFIRMED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PRIMARY_DIAGNOSIS` (`PRIMARY_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E1_DISEASE_SPECIFIC_CONFIRMATORY` (`E1_CONFIRMATORY`)
  - **Evidence Item 1:** `Thoracic vertebral biopsy culture, blood culture, and Widal test` | Target: `Salmonella enterica serovar Paratyphi A` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E1_CONFIRMATORY`
    - **Offsets:** `case_text[1012:1262]`
    - **Verbatim Quote:** > "Computed tomography-guided biopsy from thoracic vertebra showed necrotic bone with lymphocyte and neutrophil infiltration. Biopsy specimen and blood culture showed growth of NARST. Widal test was positive for Salmonella paratyphi A in 1280 dilutions."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = True` (`step8_case_definition = CONFIRMED`)
12. **Step 12 — Final Adjudication & Rationale:** `POSITIVE` (`POSITIVE`)
    - **Clinical Rationale:** A 57-year-old male banker presented with 6 weeks of high-grade fever and 4 weeks of severe backache. Both CT-guided thoracic vertebral biopsy culture and blood culture isolated nalidixic acid-resistant Salmonella Paratyphi A (with Widal test positive for S. Paratyphi A at 1:1280 dilution), and he responded to intravenous ceftriaxone, azithromycin, and trimethoprim-sulfamethoxazole. Isolation of S. Paratyphi A from blood and bone biopsy culture is E1 confirmatory -> POSITIVE.


# Case 092: PMC6051122_01::Typhoid_Fever

- **Case ID:** `PMC6051122_01` | **Article ID:** `PMC6051122` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** An Unusual Presentation of Kawasaki Disease: Gallbladder Hydrops and Acute Cholestatic Hepatitis
- **Established Case Diagnosis:** Incomplete Kawasaki disease with gallbladder hydrops and acute cholestatic hepatitis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 7-year-old boy with incomplete Kawasaki disease presenting with gallbladder hydrops and acute cholestatic hepatitis (Input metadata: Age `7.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Microbial cultures` | Target: `Enteric fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1524:1723]`
    - **Verbatim Quote:** > "Cultures were taken, and treatment with ceftriaxone 80 mg/kg for enteric fever and cholecystitis was initiated. The next day, antibiotic was stopped because of negative results of microbial cultures."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Empirical ceftriaxone was initiated for suspected enteric fever and cholecystitis, but was discontinued the next day when microbial cultures returned negative.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 7-year-old boy with incomplete Kawasaki disease was briefly started on empirical ceftriaxone for enteric fever and cholecystitis, which was stopped the next day because microbial cultures returned negative -> NEGATIVE.


# Case 093: PMC5306962_01::Typhoid_Fever

- **Case ID:** `PMC5306962_01` | **Article ID:** `PMC5306962` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Disseminated Histoplasmosis with Oral Manifestation in an Immunocompetent Patient
- **Established Case Diagnosis:** Disseminated histoplasmosis (Histoplasma capsulatum)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 60-year-old immunocompetent female from Jaipur, India with disseminated histoplasmosis and oral/cutaneous lesions (Input metadata: Age `60.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Febrile agglutination test (Widal)` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1955:2052]`
    - **Verbatim Quote:** > "Febrile agglutination tests for typhoid, brucellosis, and infectious mononucleosis were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 60-year-old woman with biopsy-confirmed disseminated histoplasmosis had negative febrile agglutination tests for typhoid, brucellosis, and infectious mononucleosis -> NEGATIVE.


# Case 094: PMC4052119_01::Typhoid_Fever

- **Case ID:** `PMC4052119_01` | **Article ID:** `PMC4052119` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Secondary hemophagocytic syndrome: the importance of clinical suspicion
- **Established Case Diagnosis:** Secondary hemophagocytic syndrome
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 75-year-old man developing fatal secondary hemophagocytic syndrome 1 month after stage I colon cancer resection (Input metadata: Age `75.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Salmonella typhi serology` | Target: `Salmonella enterica serovar Typhi` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[485:663]`
    - **Verbatim Quote:** > "Blood tests showed pancytopenia (Table 2) with negative serology for HIV, B and C hepatitis, EBV, CMV, Rickettsia conorii, Leptospira, Borrelia burgdorferi, and Salmonella typhi."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 75-year-old man with unremitting fever and pancytopenia diagnosed with secondary hemophagocytic syndrome had negative serology for Salmonella typhi -> NEGATIVE.


# Case 095: PMC3336250_01::Typhoid_Fever

- **Case ID:** `PMC3336250_01` | **Article ID:** `PMC3336250` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Miliary tuberculosis presenting as puerperial Fever
- **Established Case Diagnosis:** Postpartum miliary tuberculosis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 28-year-old postpartum female presenting with puerperal fever of unknown origin diagnosed after 8 weeks as miliary tuberculosis (Input metadata: Age `28.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and urine/blood cultures` | Target: `Enteric fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[840:954]`
    - **Verbatim Quote:** > "Widal test for enteric fever, strip test for malarial parasite, and urine and blood culture were not contributory."
  - **Evidence Item 2:** `Empirical treatment for enteric fever` | Target: `Enteric fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[1099:1260]`
    - **Verbatim Quote:** > "Patient was initially treated as a case of viral fever and then empirically for enteric fever. She, however, continued to have low-grade fever with night sweats."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Patient received empirical treatment for enteric fever despite non-contributory Widal test and blood/urine cultures; fever persisted and HRCT subsequently confirmed miliary tuberculosis.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 28-year-old postpartum woman had non-contributory Widal testing and blood/urine cultures and failed empirical treatment for enteric fever before chest radiograph and HRCT confirmed miliary tuberculosis -> NEGATIVE.


# Case 096: PMC6385320_01::Typhoid_Fever

- **Case ID:** `PMC6385320_01` | **Article ID:** `PMC6385320` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Salmonella enterica Serotype Panama: An exceptionally virulent cause of illness in children?
- **Established Case Diagnosis:** Familial outbreak of non-typhoidal Salmonella enterica serotype Panama gastroenteritis and bacteremia
- **Final Dataset Label:** `EXCLUDED_NON_SINGLE_PATIENT` (`decision`: `EXCLUDED_NON_CASE_REPORT`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT', 'F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CASE_SERIES` (`EXCLUDED_NON_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `MULTI_PATIENT_CASE_SERIES` (`AGGREGATE_STUDY_UNIT`)
3. **Step 3 — Patient Anchor:** Three pediatric siblings (Patient A 14yo M, Patient B 11yo F, Patient C 13yo M) and parents in a family outbreak of non-typhoidal Salmonella enterica serotype Panama after travel to Costa Rica (Input metadata: Age `18.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `NON_TARGET_CONCEPT`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Family vaccination history` | Target: `Typhoid vaccine` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[572:620]`
    - **Verbatim Quote:** > "No family members received typhoid immunization."
  - **Evidence Item 2:** `Blood culture (Patient A)` | Target: `Salmonella enterica serotype Panama (non-typhoidal)` | Specimen: `blood` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1778:1956]`
    - **Verbatim Quote:** > "Blood cultures, however, were positive for a Salmonella serogroup D organism subsequently identified by the state public health laboratory as Salmonella enterica serotype Panama."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_SINGLE_PATIENT` (`EXCLUDED_NON_CASE_REPORT`)
    - **Clinical Rationale:** This report is a multi-patient family case series describing three siblings (Patients A, B, and C) infected with non-typhoidal Salmonella enterica serotype Panama following travel to Costa Rica, with the only mention of typhoid being 'No family members received typhoid immunization' -> EXCLUDED_NON_SINGLE_PATIENT.


# Case 097: PMC1334206_01::Typhoid_Fever

- **Case ID:** `PMC1334206_01` | **Article ID:** `PMC1334206` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Lymph node infarction--a rare complication associated with disseminated intra vascular coagulation in a case of dengue fever
- **Established Case Diagnosis:** Dengue fever with disseminated intravascular coagulation (DIC) and lymph node infarction
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 27-year-old male (note: input age 7.0 is a truncation artifact of 'twenty-seven years old') with dengue shock syndrome, DIC, and cervical lymph node infarction (Input metadata: Age `7.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and blood/throat/urine cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1619:1825]`
    - **Verbatim Quote:** > "The serology tests for anti- cytomegalovirus antibody, anti leptospira antibody, Widal test, brucella (abortus and melitensis), and HIV were negative. The blood, throat swab and urine cultures were sterile."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 27-year-old male with dengue fever complicated by DIC and lymph node infarction had a negative Widal test and sterile blood, throat swab, and urine cultures -> NEGATIVE.


# Case 098: PMC10570831_01::Typhoid_Fever

- **Case ID:** `PMC10570831_01` | **Article ID:** `PMC10570831` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case Report: Omadacycline in the treatment of macrolide-unresponsive Mycoplasma pneumoniae pneumonia in an adolescent patient
- **Established Case Diagnosis:** Macrolide-unresponsive Mycoplasma pneumoniae pneumonia
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 16-year-old adolescent boy in Huizhou, China with macrolide-unresponsive Mycoplasma pneumoniae pneumonia treated with omadacycline (Input metadata: Age `16.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and sputum/blood/urine cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1831:2086]`
    - **Verbatim Quote:** > "serum 1,3-beta-D-glucan assay, galactomannan assay, Widal test, and Weil-Felix reaction: negative; thyroid function, antinuclear antibody spectrum, and anti-neutrophil cytoplasmic antibodies: negative; sputum, blood, and midstream urine cultures: negative"
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 16-year-old boy with macrolide-unresponsive Mycoplasma pneumoniae pneumonia confirmed by BALF mNGS had a negative Widal test and negative sputum, blood, and urine cultures -> NEGATIVE.


# Case 099: PMC10928401_01::Typhoid_Fever

- **Case ID:** `PMC10928401_01` | **Article ID:** `PMC10928401` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Unveiling Neurobrucellosis: A Case Report Emphasizing Early Diagnosis for Better Outcomes
- **Established Case Diagnosis:** Neurobrucellosis (Brucella melitensis)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 55-year-old male farmer from Jodhpur, India presenting with 3-week fever and acute right-sided weakness due to neurobrucellosis (Brucella melitensis) (Input metadata: Age `55.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2696:3037]`
    - **Verbatim Quote:** > "With pyrexia of unknown origin (PUO) as the working diagnosis, human immunodeficiency virus 1 and 2 antibody, japanese encephalitis IgM serology, scrub typhus IgM serology, non-structural one dengue antigen, typhoid WIDAL test and pan plasmodium lactate dehydrogenase and histidine rich protein-2 malarial antigens were found to be negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 55-year-old Indian farmer evaluated for pyrexia of unknown origin and neurological deficits had a negative typhoid Widal test, and three paired blood cultures plus ELISA confirmed Brucella melitensis neurobrucellosis -> NEGATIVE.


# Case 100: PMC10964487_01::Typhoid_Fever

- **Case ID:** `PMC10964487_01` | **Article ID:** `PMC10964487` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Talaromycosis from Wuhan: two-case report and literature review
- **Established Case Diagnosis:** Disseminated talaromycosis (Talaromyces marneffei) in a patient with AIDS
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 48-year-old male with AIDS (Case 1) presenting with fever, melena, jaundice, and disseminated Talaromyces marneffei infection (Input metadata: Age `48.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2544:2775]`
    - **Verbatim Quote:** > "Laboratory tests showed that galactomannan (GM) test was positive; (1,3)-beta-D-glucan test (G test) was 80.10 pg/mL; and urine culture, Widal test, T-SPOT.TB, tuberculosis gene, and respiratory pathogen 9 antibodies were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 48-year-old man with AIDS and disseminated Talaromyces marneffei infection (confirmed in blood, sputum, and BALF cultures) tested negative on the Widal test -> NEGATIVE.


# Case 101: PMC11384573_01::Typhoid_Fever

- **Case ID:** `PMC11384573_01` | **Article ID:** `PMC11384573` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Fever of unknown origin, blood and cerebrospinal fluid involvement: a leprosy case report
- **Established Case Diagnosis:** Multibacillary leprosy (Mycobacterium leprae) with type II leprosy reaction
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 39-year-old male from Hunan Province, China with multibacillary leprosy and type II leprosy reaction presenting as fever of unknown origin (Input metadata: Age `39.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood culture and Widal test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1131:1390]`
    - **Verbatim Quote:** > "No abnormalities were detected in blood culture, viral testing, rheumatism screening, lupus evaluation, idiopathic inflammatory myopathy spectrum investigation, vasculitis assessment, brucella antibody examination, Widal test, Weil-Felix test and T-spot test."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 39-year-old man presenting with fever and systemic rash had negative blood culture and Widal test results, and was diagnosed with multibacillary leprosy via skin biopsy, slit-skin smear, nested PCR, and mNGS -> NEGATIVE.


# Case 102: PMC10904597_01::Typhoid_Fever

- **Case ID:** `PMC10904597_01` | **Article ID:** `PMC10904597` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** A case report of Pseudomonas citronellolis and Escherichia coli isolated from acute suppurative appendicitis: reveals the potential intestinal colonization and pathogenicity of Pseudomonas citronellolis
- **Established Case Diagnosis:** Acute suppurative appendicitis with Pseudomonas citronellolis and Escherichia coli co-isolation
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 38-year-old female with acute suppurative appendicitis from which Pseudomonas citronellolis and Escherichia coli were isolated (Input metadata: Age `38.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Past medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[244:456]`
    - **Verbatim Quote:** > "This female had a normal menstrual cycle, no history of chronic diseases such as diabetes or hypertension, no known allergies, and no recorded infectious diseases like tuberculosis, typhoid fever, hepatitis, etc."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 38-year-old woman with acute suppurative appendicitis explicitly had no recorded history of infectious diseases such as tuberculosis, typhoid fever, or hepatitis -> NEGATIVE.


# Case 103: PMC10847276_01::Typhoid_Fever

- **Case ID:** `PMC10847276_01` | **Article ID:** `PMC10847276` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Case report: Page kidney with multiple serosal effusions caused by bilateral spontaneous renal subcapsular hemorrhage
- **Established Case Diagnosis:** Page kidney with multiple serosal effusions due to bilateral spontaneous renal subcapsular hemorrhage
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 40-year-old woman with Page kidney and multiple serosal effusions caused by bilateral spontaneous renal subcapsular hemorrhage (Input metadata: Age `40.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Past medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[132:490]`
    - **Verbatim Quote:** > "The patient denied a history of trauma and surgery, a history of chronic diseases such as hypertension, diabetes, and heart disease, a history of infectious diseases such as hepatitis, tuberculosis, and typhoid fever, and a history of gastrointestinal and gynecological tumors, and no symptoms such as bone pain, butterfly erythematosus, or photosensitivity."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 40-year-old woman presenting with Page kidney explicitly denied any history of infectious diseases including hepatitis, tuberculosis, and typhoid fever -> NEGATIVE.


# Case 104: PMC10585990_01::Typhoid_Fever

- **Case ID:** `PMC10585990_01` | **Article ID:** `PMC10585990` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Psychopathology associated with cardiac pacing in Tanzania: A case series
- **Established Case Diagnosis:** Case series of 5 cardiac pacemaker patients with post-pacing psychopathology (and Staphylococcus epidermidis lead endocarditis in Case 5)
- **Final Dataset Label:** `EXCLUDED_NON_SINGLE_PATIENT` (`decision`: `EXCLUDED_NON_CASE_REPORT`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CASE_SERIES` (`EXCLUDED_NON_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `MULTI_PATIENT_CASE_SERIES` (`AGGREGATE_STUDY_UNIT`)
3. **Step 3 — Patient Anchor:** Five patients (Cases 1 to 5, aged 58 to 81 years) in Tanzania developing psychiatric disorders associated with permanent cardiac pacemaker implantation (Input metadata: Age `58.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Regional febrile illness workup in Case 5` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[9510:9650]`
    - **Verbatim Quote:** > "The fever was intermittent and common regional causes of febrile illness (i.e. malaria, typhoid and urinary tract infection) were ruled out."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_SINGLE_PATIENT` (`EXCLUDED_NON_CASE_REPORT`)
    - **Clinical Rationale:** This record contains a 5-patient case series (Cases 1-5) describing psychiatric disorders after pacemaker implantation (`MULTI_PATIENT_CASE_SERIES`), and in Case 5 typhoid was explicitly ruled out before Staphylococcus epidermidis pacemaker lead infection was identified -> EXCLUDED_NON_SINGLE_PATIENT.


# Case 105: PMC11402080_01::Typhoid_Fever

- **Case ID:** `PMC11402080_01` | **Article ID:** `PMC11402080` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Gossypiboma: A case of retained intra-luminal surgical sponge leading to delayed diagnosis and treatment in a Nigerian patient
- **Established Case Diagnosis:** Intraluminal ileal gossypiboma (retained surgical sponge) causing mechanical bowel obstruction and ileal perforations
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 42-year-old Nigerian female presenting 3 months after open myomectomy with intestinal obstruction and ileal perforations caused by a retained intraluminal surgical sponge (gossypiboma) (Input metadata: Age `42.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 3 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Initial outpatient Widal test and empirical treatment` | Target: `Typhoid enteritis` | Specimen: `serum` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `INCONCLUSIVE` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[708:1144]`
    - **Verbatim Quote:** > "Vital signs were stable with a weight of 77 kg, and initial investigations showed positive malaria test (2+), elevated Widal titers (>160: range), decreased haematocrit (27%: range from 35.0% to 59.0%) and total white cell count of 6.2 x 103/muL (3.50-9.50 x 103/muL), suggesting possible infection. The patient, after further review, was treated for malaria and typhoid enteritis, and she was discharged with antibiotics and hematinic."
  - **Evidence Item 2:** `Repeat serology test on readmission` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1574:1726]`
    - **Verbatim Quote:** > "Laboratory investigations revealed serum potassium of 3.22 mmol/L (3.5-5.1 mmol/L), a haematocrit of 24% (35.0%-59.0%), and a nonreactive serology test."
  - **Evidence Item 3:** `Exploratory laparotomy finding` | Target: `Intraluminal gossypiboma (retained surgical mop)` | Specimen: `ileum` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3690:4017]`
    - **Verbatim Quote:** > "With further dissection and adhesiolysis, the intra-luminal ileal abdominal mop was extracted through the perforation between the proximal and distal (about 100 cm from ileocaecal junction) ileal perforations; and approximately 60 cm of the ileal segment with multiple (major and minor) perforations was resected (Figure 2(b))."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Initial outpatient visit showed elevated Widal titers (>160) and she was treated for malaria and typhoid enteritis, but symptoms worsened, repeat serology on readmission was nonreactive, and exploratory laparotomy revealed a retained intraluminal surgical mop (gossypiboma) causing multiple ileal perforations.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 42-year-old woman who had undergone open myomectomy 3 months prior was initially misdiagnosed at her first clinic visit with malaria and typhoid enteritis based on elevated Widal titers (>160). She worsened, repeat serology on readmission was nonreactive, and exploratory laparotomy established that her ileal perforations were caused by a transmurally migrated retained surgical mop (gossypiboma) -> NEGATIVE.


# Case 106: PMC10908293_01::Typhoid_Fever

- **Case ID:** `PMC10908293_01` | **Article ID:** `PMC10908293` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Raptured gas forming pyogenic liver abscess with a biliary fistula in Botswana: a case report
- **Established Case Diagnosis:** Ruptured gas-forming pyogenic liver abscess with biliary fistula
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 39-year-old diabetic male in Botswana with a ruptured gas-forming pyogenic liver abscess and postoperative biliary fistula (Input metadata: Age `39.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and stool analysis` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1521:1590]`
    - **Verbatim Quote:** > "Widal test results were negative and stool analysis was unremarkable."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 39-year-old diabetic man presenting with peritonitis from a ruptured gas-forming pyogenic liver abscess had negative Widal test results and unremarkable stool analysis -> NEGATIVE.


# Case 107: PMC11259356_01::Typhoid_Fever

- **Case ID:** `PMC11259356_01` | **Article ID:** `PMC11259356` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Multisystem inflammatory syndrome in children with COVID-19 in a multitransfused patient
- **Established Case Diagnosis:** Multisystem inflammatory syndrome in children (MIS-C) in a child with beta-thalassemia major
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 3-year-old male child with transfusion-dependent beta-thalassemia major presenting with COVID-19-associated MIS-C (Input metadata: Age `3.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid serology and blood/urine cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2206:2404]`
    - **Verbatim Quote:** > "Serological tests sent for dengue, scrub typhus, and typhoid came negative. Blood and urine cultures did not grow any organism, and bacterial sepsis and urinary tract infections were also ruled out."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 3-year-old boy with beta-thalassemia major diagnosed with SARS-CoV-2-associated MIS-C had negative serological tests for typhoid and negative blood and urine cultures -> NEGATIVE.


# Case 108: PMC10906542_01::Typhoid_Fever

- **Case ID:** `PMC10906542_01` | **Article ID:** `PMC10906542` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Neurological Spectrum of Epstein-Barr Virus Infection: A Rare Clinical Case
- **Established Case Diagnosis:** Polyradiculoneuropathy secondary to acute Epstein-Barr virus (EBV) infection
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 61-year-old Caucasian male teacher with acute Epstein-Barr virus-associated polyradiculoneuropathy (Input metadata: Age `61.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid and paratyphoid serology` | Target: `Typhoid and paratyphoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[4293:4378]`
    - **Verbatim Quote:** > "Serological tests for Brucellosis, typhoid fever, paratyphoid, and HIV were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 61-year-old man with EBV-induced polyradiculoneuropathy tested negative on serological tests for typhoid fever and paratyphoid -> NEGATIVE.


# Case 109: PMC10870101_01::Typhoid_Fever

- **Case ID:** `PMC10870101_01` | **Article ID:** `PMC10870101` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Leptospirosis and Dengue Coinfection-Associated Multi-Organ Dysfunction Syndrome: A Case Report
- **Established Case Diagnosis:** Leptospirosis and dengue coinfection-associated multi-organ dysfunction syndrome (MODS)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 51-year-old female presenting with fever, altered sensorium, and multi-organ dysfunction syndrome due to leptospirosis and dengue coinfection (Input metadata: Age `51.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Acute febrile illness workup for typhoid` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1078:1389]`
    - **Verbatim Quote:** > "We investigated dengue, Leptospira, malaria, typhoid, and rickettsia, which are common causes of acute febrile illness with associated altered sensorium and mild-to-severe hepatic impairment. Day 1 reports (Tables 1, 2) suggested dengue and Leptospira coinfection fever with mild hepatitis and thrombocytopenia."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 51-year-old woman investigated for dengue, Leptospira, malaria, typhoid, and rickettsia was found to have dengue and Leptospira coinfection -> NEGATIVE.


# Case 110: PMC11401736_01::Typhoid_Fever

- **Case ID:** `PMC11401736_01` | **Article ID:** `PMC11401736` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Multifocal Osteomyelitis in an Adolescent Patient With Cat Scratch Disease
- **Established Case Diagnosis:** Cat scratch disease (Bartonella henselae) with multifocal vertebral osteomyelitis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 15-year-old girl with right axillary lymphadenopathy and multifocal vertebral osteomyelitis due to Cat Scratch Disease (Bartonella henselae) (Input metadata: Age `15.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Gruber-Widal test` | Target: `Typhoid fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[769:928]`
    - **Verbatim Quote:** > "Brucella Rose Bengal test, Brucella tube agglutination test, Gruber-Widal test, CMV IgM index, Brucella abortus IgM, and Quantiferon assay tests were negative."
  - **Evidence Item 2:** `Repeated blood cultures` | Target: `Salmonella Typhi` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2482:2533]`
    - **Verbatim Quote:** > "There was no growth in the repeated blood cultures."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 15-year-old girl with multifocal osteomyelitis secondary to Bartonella henselae cat scratch disease had a negative Gruber-Widal test and no growth in repeated blood cultures -> NEGATIVE.


# Case 111: PMC10895081_01::Typhoid_Fever

- **Case ID:** `PMC10895081_01` | **Article ID:** `PMC10895081` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Perioperative Management Conundrum for a Case With Multiple Commonly Used Drug Hypersensitivity
- **Established Case Diagnosis:** Postoperative inflammatory fever in a patient with multiple drug hypersensitivity
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 14-year-old boy undergoing tibialis posterior tendon transfer with multiple drug hypersensitivity (paracetamol, diclofenac, ranitidine, ondansetron) and postoperative fever (Input metadata: Age `14.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Typhoid test` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3232:3449]`
    - **Verbatim Quote:** > "Complete blood counts, urine routine, malaria, typhoid, and dengue tests were sent. The total leucocyte counts (TLC) were 7,560/dL, with neutrophils comprising of 89.5%. Other investigations were within normal limits."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 14-year-old boy evaluated for postoperative fever after tendon transfer surgery had malaria, typhoid, and dengue tests sent, all of which were within normal limits -> NEGATIVE.


# Case 112: PMC10637264_01::Typhoid_Fever

- **Case ID:** `PMC10637264_01` | **Article ID:** `PMC10637264` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Chlamydia psittaci Pneumonia-Induced Pulmonary Thrombosis: A Case Report
- **Established Case Diagnosis:** Severe Chlamydia psittaci pneumonia complicated by pulmonary thrombosis
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 47-year-old woman with severe Chlamydia psittaci pneumonia complicated by acute pulmonary artery thrombosis (Input metadata: Age `47.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Widal test and blood/sputum cultures` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1754:2271]`
    - **Verbatim Quote:** > "Laboratory examination revealed negative results for nucleic acids of COVID-19 in nasopharyngeal swab and dengue virus in peripheral venous blood; Influenza A and B virus antigens; the Weil-Felix test, Widal test, 1,3-beta-D-glucan assay, galactomannan test, and respiratory pathogens (ie, parainfluenza virus, Pneumocystis, Mycoplasma pneumoniae, respiratory syncytial virus, "Q fever" rickettsia, adenovirus, Legionella); IgM antibodies; and blood and sputum culture, along with sputum smear for acid-fast bacillus."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 47-year-old woman with mNGS-confirmed Chlamydia psittaci pneumonia and pulmonary thrombosis tested negative on the Widal test and blood and sputum cultures -> NEGATIVE.


# Case 113: PMC11152966_02::Typhoid_Fever

- **Case ID:** `PMC11152966_02` | **Article ID:** `PMC11152966` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Two cases of misleading Epstein-Barr virus infection and the role of EBV-DNA
- **Established Case Diagnosis:** Epstein-Barr virus (EBV) infectious mononucleosis confirmed by plasma EBV-DNA PCR
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 15-year-old boy with 4 weeks of night sweats, fatigue, generalized hypermetabolic lymphadenopathy, and initially seronegative infectious mononucleosis confirmed by EBV-DNA PCR (Input metadata: Age `15.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Tests for bacteremia and typhoid fever` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1328:1439]`
    - **Verbatim Quote:** > "Additionally, tests for toxoplasmosis, bacteremia, brucellosis, typhoid fever, and rickettsiosis were negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 15-year-old boy presenting with fever, night sweats, and generalized lymphadenopathy tested negative for bacteremia and typhoid fever, and was diagnosed with EBV infectious mononucleosis via blood EBV-DNA PCR and subsequent anti-VCA IgM seroconversion -> NEGATIVE.


# Case 114: PMC11338764_01::Typhoid_Fever

- **Case ID:** `PMC11338764_01` | **Article ID:** `PMC11338764` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Ceftriaxone-resistant Salmonella enterica serovar Newport: a case report from South India
- **Established Case Diagnosis:** Acute gastroenteritis due to ceftriaxone-resistant non-typhoidal Salmonella enterica serovar Newport
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F6_EVIDENCE_SPECIFICITY']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 60-year-old woman with type 2 diabetes and poliomyelitis presenting with acute gastroenteritis in shock due to ceftriaxone-resistant non-typhoidal Salmonella enterica serovar Newport (Input metadata: Age `60.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 3 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `NON_TARGET_CONCEPT`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Tropical fever workup` | Target: `Enteric fever` | Specimen: `serum` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[2078:2277]`
    - **Verbatim Quote:** > "As the patient presented with fever and features of gastroenteritis, she was examined to rule out the causes of tropical fever such as enteric fever, dengue, leptospirosis, scrub typhus, and malaria."
  - **Evidence Item 2:** `Salmonella antisera serotyping` | Target: `Salmonella O2/O4/O9/H-i antisera` | Specimen: `stool isolate` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[3676:3795]`
    - **Verbatim Quote:** > "In serotyping, the isolate showed agglutination with poly(O) antisera and was negative for HI, O2, O4, and O9 antisera."
  - **Evidence Item 3:** `Reference laboratory speciation and serotyping (NICED)` | Target: `Salmonella enterica serovar Newport (non-typhoidal Salmonella)` | Specimen: `stool` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[4812:4922]`
    - **Verbatim Quote:** > "The NICED report identified the isolate as Salmonella enterica serovar Newport with resistance to ceftriaxone."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Initial biochemical TSI pattern raised differential between Salmonella Paratyphi B and Salmonella Typhimurium, but reference serotyping at NICED confirmed non-typhoidal Salmonella enterica serovar Newport.
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 60-year-old woman presenting with acute gastroenteritis had stool culture growth of a Salmonella isolate that was negative for O2, O4, O9, and H-i antisera and definitively identified by the National Institute of Cholera and Enteric Diseases (NICED) as non-typhoidal Salmonella enterica serovar Newport -> NEGATIVE.


# Case 115: PMC11249797_01::Typhoid_Fever

- **Case ID:** `PMC11249797_01` | **Article ID:** `PMC11249797` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Mixed Neuroendocrine-Non-Neuroendocrine Neoplasms of the Rectum: A Case Report
- **Established Case Diagnosis:** Stage IV mixed neuroendocrine-non-neuroendocrine neoplasm (MiNEN) of the rectum
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 55-year-old male presenting with stage IV mixed neuroendocrine-non-neuroendocrine neoplasm (MiNEN) of the rectum (Input metadata: Age `55.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `HISTORICAL_RESOLVED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `PAST_HISTORY` (`PAST_HISTORY`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Past medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `HISTORICAL_PAST` | Relation: `INCONCLUSIVE` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[0:124]`
    - **Verbatim Quote:** > "A 55-year-old male presented with a medical history of typhoid fever at the age of 12 years and no surgical history of note."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 55-year-old man evaluated for metastatic rectal MiNEN had a remote childhood history of typhoid fever at age 12 years (43 years prior to presentation). Remote resolved history (`HISTORICAL_RESOLVED` / `PAST_HISTORY`) does not satisfy VPD -> EXCLUDED_NON_TARGET_CASE.


# Case 116: PMC11333127_02::Typhoid_Fever

- **Case ID:** `PMC11333127_02` | **Article ID:** `PMC11333127` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Two Unrelated Iranian Patients with Adenosine Deaminase 2 Deficiency: A Case Report and Review of Treatment
- **Established Case Diagnosis:** Adenosine deaminase 2 deficiency (DADA2) with concurrent Salmonella Paratyphi C enteric infection
- **Final Dataset Label:** `POSITIVE` (`decision`: `POSITIVE`) | **VPD Satisfied:** `True` | **Confidence:** `MEDIUM` | **Failure Flags:** `[]`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 6-year-old Iranian girl (Patient 2) from consanguineous parents admitted with 1-month intermittent fever, bicytopenia, cervical lymphadenopathy, positive Widal test, and stool culture positive for Salmonella Paratyphi C, with underlying DADA2 deficiency (Input metadata: Age `6.0`, Gender `Female`)
4. **Step 4 — Disease Mentions & Spans:** Identified 2 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `AFFIRMED` (`AFFIRMED`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `ACTIVE_COMORBIDITY` (`SECONDARY_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E1_DISEASE_SPECIFIC_CONFIRMATORY` (`E1_CONFIRMATORY`)
  - **Evidence Item 1:** `Clinical admission diagnosis` | Target: `Typhoid fever` | Specimen: `None` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E3_SUPPORTIVE`
    - **Offsets:** `case_text[0:259]`
    - **Verbatim Quote:** > "A 6-year-old girl from consanguineous parents (third cousins) was admitted to the hospital due to intermittent fever since a month ago, aphthous lesion in mouth, weakness, cervical lymphadenopathy, and bicytopenia with an admission diagnosis of typhoid fever."
  - **Evidence Item 2:** `Widal test and stool culture` | Target: `Salmonella enterica serovar Paratyphi C` | Specimen: `stool` | Result: `POSITIVE` | Temporality: `CURRENT_EPISODE` | Relation: `SUPPORTS` | Strength: `E1_CONFIRMATORY`
    - **Offsets:** `case_text[1277:1401]`
    - **Verbatim Quote:** > "Infectious laboratory workups revealed a positive Widal test. Salmonella Paratyphi C was detected in the stool culture test."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = True` — Although Salmonella Paratyphi C was isolated on stool culture with a positive Widal test during the febrile episode, her persistent bicytopenia, lymphadenopathy, and systemic inflammation did not resolve with broad-spectrum antibiotics and WES later identified underlying Adenosine Deaminase 2 (DADA2) deficiency (CECR1/ADA2 c.934C>T; p.R312*).
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = True` (`step8_case_definition = CONFIRMED`)
12. **Step 12 — Final Adjudication & Rationale:** `POSITIVE` (`POSITIVE`)
    - **Clinical Rationale:** A 6-year-old girl admitted with a 1-month intermittent fever had a clinical admission diagnosis of typhoid fever, a positive Widal test, and isolation of Salmonella Paratyphi C in stool culture (E1 confirmatory microbiological isolation under Section 5.9 Typhoid/Paratyphoid Fever), alongside underlying autosomal recessive DADA2 deficiency identified on whole exome sequencing. Per the multimorbidity/coinfection rule, confirmed Salmonella Paratyphi C infection in a patient with an underlying genetic immunodeficiency is a valid active comorbidity (`ACTIVE_COMORBIDITY` / `SECONDARY_DIAGNOSIS`) -> POSITIVE (MEDIUM confidence).


# Case 117: PMC11769995_01::Typhoid_Fever

- **Case ID:** `PMC11769995_01` | **Article ID:** `PMC11769995` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Successful management of coagulation dysfunction in a patient with fulminant myocarditis: a case report
- **Established Case Diagnosis:** Fulminant viral myocarditis with cardiogenic shock and coagulopathy
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 51-year-old male with viral fulminant myocarditis (coxsackievirus B3 and echovirus IgM positive), cardiogenic shock, and severe coagulopathy (Input metadata: Age `51.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `HISTORICAL_RESOLVED` (`HISTORICAL_PAST`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Past medical history` | Target: `Typhoid fever` | Specimen: `None` | Result: `NEGATIVE` | Temporality: `HISTORICAL_PAST` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[1263:1457]`
    - **Verbatim Quote:** > "Upon taking the patient's medical history, he denied any history of hypertension, diabetes, stroke, hepatitis, typhoid fever, or schistosomiasis, and he reported no known drug or food allergies."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 51-year-old man with fulminant viral myocarditis explicitly denied any history of typhoid fever -> NEGATIVE.


# Case 118: PMC11817083_01::Typhoid_Fever

- **Case ID:** `PMC11817083_01` | **Article ID:** `PMC11817083` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Moisturizer induced contact anaphylaxis
- **Established Case Diagnosis:** Moisturizer-induced contact anaphylaxis (attributed to phenoxyethanol)
- **Final Dataset Label:** `EXCLUDED_NON_TARGET_CASE` (`decision`: `EXCLUDED_NON_TARGET_CASE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F5_DISCOURSE_CONTEXT']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 69-year-old non-atopic male who developed contact anaphylaxis after applying phenoxyethanol-containing moisturizer to chemical burns (Input metadata: Age `69.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `FUTURE_CONDITIONAL` (`UNKNOWN`)
8. **Step 8 — Clinical Role:** `PREVENTION_VACCINATION` (`EPIDEMIOLOGICAL_CONTEXT`)
9. **Step 9 — Evidence Assessment:** `E4_BACKGROUND_OR_CONTEXT_ONLY` (`E4_CONTEXT`)
  - **Evidence Item 1:** `Allergen avoidance counseling` | Target: `Vivaxim (Hepatitis A-typhoid vaccine)` | Specimen: `None` | Result: `NOT_DETECTED` | Temporality: `UNKNOWN` | Relation: `REFUTES` | Strength: `E4_CONTEXT`
    - **Offsets:** `case_text[3198:3440]`
    - **Verbatim Quote:** > "This included avoiding vaccines such as Vivaxim (Hepatitis A-typhoid), Quadracel (diptheria, tetanus, acellular pertussis, inactivated poliovirus) or other vaccines containing phenoxyethanol until further immunology review could be conducted."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `EXCLUDED_NON_TARGET_CASE` (`EXCLUDED_NON_TARGET_CASE`)
    - **Clinical Rationale:** A 69-year-old man with contact anaphylaxis to phenoxyethanol in a moisturizer was advised to avoid phenoxyethanol-containing products, including the combined Hepatitis A-typhoid vaccine (Vivaxim). Vaccine avoidance counseling is `PREVENTION_VACCINATION` -> EXCLUDED_NON_TARGET_CASE.


# Case 119: PMC12894103_01::Typhoid_Fever

- **Case ID:** `PMC12894103_01` | **Article ID:** `PMC12894103` | **Target Disease:** `Typhoid_Fever`
- **Article Title:** Adult-Onset Still's Disease: A Diagnostic Odyssey and Therapeutic Triumph
- **Established Case Diagnosis:** Adult-onset Still's disease (AOSD)
- **Final Dataset Label:** `NEGATIVE` (`decision`: `NEGATIVE`) | **VPD Satisfied:** `False` | **Confidence:** `HIGH` | **Failure Flags:** `['F4_ASSERTION_TEMPORAL']`

## 12-Step Clinical Reasoning Process

1. **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
2. **Step 2 — CCU Type (Unit of Analysis):** `SINGLE_HUMAN_PATIENT` (`PRIMARY_CARE_EPISODE`)
3. **Step 3 — Patient Anchor:** 34-year-old Asian man with quotidian fevers, symmetrical polyarthralgia, hepatic dysfunction, and extreme hyperferritinemia (6,900 ng/mL) diagnosed with Adult-onset Still's disease (AOSD) (Input metadata: Age `34.0`, Gender `Male`)
4. **Step 4 — Disease Mentions & Spans:** Identified 1 grounded span(s) in `case_text`.
5. **Step 5 — Concept Grounding:** `TARGET_CONFIRMED`
6. **Step 6 — Assertion Type:** `NEGATED` (`ABSENT_NEGATIVE`)
7. **Step 7 — Temporality:** `CURRENT_ACTIVE` (`CURRENT_EPISODE`)
8. **Step 8 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
9. **Step 9 — Evidence Assessment:** `E0_CONTRADICTED` (`E0_CONTRADICTED`)
  - **Evidence Item 1:** `Blood/urine/sputum cultures and typhoid serology` | Target: `Typhoid fever` | Specimen: `blood` | Result: `NEGATIVE` | Temporality: `CURRENT_EPISODE` | Relation: `REFUTES` | Strength: `E0_CONTRADICTED`
    - **Offsets:** `case_text[2050:2326]`
    - **Verbatim Quote:** > "Extensive cultures of blood, urine, and sputum remained sterile. Viral and zoonotic serologies, including dengue, chikungunya, leptospirosis, brucellosis, typhoid, Epstein-Barr virus, cytomegalovirus, human immunodeficiency virus, and hepatitis A, B, and C, were all negative."
10. **Step 10 — Contradiction Reconciliation:** `contradiction_flag = False` (No contradiction)
11. **Step 11 — Valid Positive Diagnosis (VPD) Test:** `step11_vpd_satisfied = False` (`step8_case_definition = NOT_MET`)
12. **Step 12 — Final Adjudication & Rationale:** `NEGATIVE` (`NEGATIVE`)
    - **Clinical Rationale:** A 34-year-old man diagnosed with Adult-onset Still's disease had sterile blood, urine, and sputum cultures and negative typhoid serology -> NEGATIVE.

# Clinical Gold Standard Annotation — Leishmaniasis (95 Candidate Pairs)

This document records the complete 12-step clinical semantic reasoning process for all **95 candidate pairs** in `input_leishmaniasis.jsonl`, evaluated against the **Leishmaniasis** evidence specificity matrix (`03_evidence_specificity_matrix.md`) and the 12-step Gold Standard Annotation Protocol (`04_gold_standard_annotation_protocol.md`).

## Executive Summary of Adjudicated Labels

| Dataset Label (`step12_dataset_label`) | Count | Share (%) | Clinical Summary |
| :--- | ---: | ---: | :--- |
| `POSITIVE` | 2 | 2.1% | Confirmed human visceral leishmaniasis with E1 bone marrow parasitological/histopathological evidence (`PMC3420495_01`, `PMC8014250_01`) |
| `NEGATIVE` | 74 | 77.9% | Single human patients in whom Leishmaniasis was explicitly tested negative (serology, PCR, microscopy, culture, skin test) or ruled out in differential diagnosis |
| `EXCLUDED_NON_HUMAN` | 10 | 10.5% | Veterinary case reports (9 canine cases, 1 feline leishmaniosis case `PMC5362848_01`) |
| `EXCLUDED_NON_TARGET_CASE` | 5 | 5.3% | Remote resolved childhood history only (`PMC8264782_01`, `PMC3168563_01`), negative travel history only (`PMC10868469_01`), or background literature review mentions (`PMC9248758_02`, `PMC4138934_01`) |
| `EXCLUDED_NON_SINGLE_PATIENT` | 4 | 4.2% | Bibliometric/narrative reviews (`PMC10434771_01`, `PMC7239889_01`), 16-patient aggregate series (`PMC6607709_01`), and multi-paper editorial (`PMC10482395_09`) |
| **Total** | **95** | **100.0%** | **100% verbatim character-offset grounded across all 95 cases** |

## Positive Cases Highlight

1. **Case 30 (`PMC3420495_01::Leishmaniasis`)**: A 43-year-old Caucasian German salesman newly diagnosed with advanced HIV-1 infection (CD4 140 cells/uL), Kaposi's sarcoma, plasma cell variant multicentric Castleman's disease, and latent syphilis, in whom a **bone marrow trephine biopsy demonstrated Leishmaniasis (Figure 5)** (`E1_DISEASE_SPECIFIC_CONFIRMATORY`) that was successfully eradicated with liposomal amphotericin B (`AmBisome`).
2. **Case 72 (`PMC8014250_01::Leishmaniasis`)**: A 29-month-old boy with a 2-month history of fever, splenomegaly (130 mm), pancytopenia, hyperferritinemia, and concurrent COVID-19 PCR positivity, in whom repeat **bone marrow aspiration directly demonstrated Leishman-Donovan bodies and hemophagocytic cells (Figure 3)** (`E1_DISEASE_SPECIFIC_CONFIRMATORY`), establishing hemophagocytic lymphohistiocytosis secondary to visceral leishmaniasis with clinical improvement on amphotericin.

## Case-by-Case 12-Step Clinical Reasoning Log

### Case 01: `PMC9815528_01::Leishmaniasis` (`PMC9815528_01`)

- **Article Title:** Acrofacial necrotic ulcers in an infant: An undiagnosed presentation
- **Demographics (Metadata):** Age `8.0`, Gender `Male`, Year `2022`, Journal `Front Pediatr`
- **Primary Established Diagnosis of Case:** Undiagnosed autoinflammatory disorder / suspected type I interferonopathy
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 8-year-old Arab boy presenting in infancy with cold-exacerbated acrofacial ulceronecrotic plaques.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1714:1795]` | Test: `Skin smear and PCR` | Target: `Leishmania` | Specimen: `skin lesion` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Cutaneous leishmaniasis was also excluded by smear and polymerase chain reaction."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** An 8-year-old male presented with severe acrofacial ulceronecrotic lesions exacerbated by cold weather (suspected novel type I interferonopathy). Cutaneous leishmaniasis was explicitly excluded by both skin smear and PCR. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS, evidence E0_CONTRADICTED -> NEGATIVE.

### Case 02: `PMC3952285_01::Leishmaniasis` (`PMC3952285_01`)

- **Article Title:** Primary labial tuberculosis: a rare presentation
- **Demographics (Metadata):** Age `24.0`, Gender `Male`, Year `2014`, Journal `Ann Med Health Sci Res`
- **Primary Established Diagnosis of Case:** Primary labial tuberculosis (Mycobacterium tuberculosis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 24-year-old male with ulcerated swelling of the lip diagnosed with primary labial tuberculosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[681:931]` | Test: `Clinical differential diagnosis` | Target: `Leishmaniasis` | Specimen: `None` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "A provisional diagnosis of Chelitis granulomatosis was made with a differential diagnosis of Baelz disease, tuberculous granulomatosis, sarcoidosis, a deep mycosis, primary syphilis, leishmaniasis, Squamous cell carcinoma, and non-Hodgkin's lymphoma."
   - **Evidence Item 2:** `case_text[1003:1134]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serologies for syphilis and Leishmania, Mantoux test, and Enzyme-linked immunosorbent assay (ELISA) for HIV gave a negative result."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 24-year-old male presented with a persistent labial swelling and ulceration. Leishmaniasis was considered in the clinical differential diagnosis, and Leishmania serology tested negative. Incisional biopsy with Ziehl-Neelsen staining and culture confirmed primary labial Mycobacterium tuberculosis infection. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 03: `PMC6005278_01::Leishmaniasis` (`PMC6005278_01`)

- **Article Title:** Cutaneous Disease as Sole Clinical Manifestation of Protothecosis in a Boxer Dog
- **Demographics (Metadata):** Age `6.0`, Gender `Female`, Year `2016`, Journal `Case Rep Vet Med`
- **Primary Established Diagnosis of Case:** Canine cutaneous protothecosis (Prototheca wickerhamii)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 6-year-old female Boxer dog with cutaneous protothecosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1838:2088]` | Test: `SNAP ELISA serology` | Target: `Leishmania infantum` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Hematology, serum biochemistry, and urinalysis did not display any abnormalities and serology (snap ELISA, IDEXX ) for all of Leishmania infantum, Ehrlichia canis, and Anaplasma phagocytophilum antibodies and Dirofilaria immitis antigen was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case report of a 6-year-old female Boxer dog diagnosed with cutaneous protothecosis (Prototheca wickerhamii), in which SNAP ELISA serology for Leishmania infantum was negative. Because ccu_type is ANIMAL_CASE (canine patient), the case is excluded from the human benchmark -> EXCLUDED_NON_HUMAN.

### Case 04: `PMC6997440_01::Leishmaniasis` (`PMC6997440_01`)

- **Article Title:** Use of Slow-Release Injectable Moxidectin for Treatment of Dirofilaria immitis Infection During Pregnancy
- **Demographics (Metadata):** Age `4.0`, Gender `Female`, Year `2020`, Journal `Front Vet Sci`
- **Primary Established Diagnosis of Case:** Canine heartworm disease (Dirofilaria immitis)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 4-year-old female Pit Bull cross dog with Dirofilaria immitis heartworm infection.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[461:570]` | Test: `TR DPP canine visceral leishmaniasis rapid test` | Target: `Leishmania infantum` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "She was seronegative for Leishmania infantum (TR DPP  canine visceral leishmaniasis, Bio-Manguinhos, Brazil)."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case report describing a 4-year-old female Pit Bull cross dog treated for Dirofilaria immitis infection during pregnancy, who tested seronegative for Leishmania infantum. Because ccu_type is ANIMAL_CASE (canine subject), VPD is not applicable -> EXCLUDED_NON_HUMAN.

### Case 05: `PMC8264782_01::Leishmaniasis` (`PMC8264782_01`)

- **Article Title:** Case Report: Interleukin-2 Receptor Common Gamma Chain Defect Presented as a Hyper-IgE Syndrome
- **Demographics (Metadata):** Age `7.0`, Gender `Male`, Year `2021`, Journal `Front Immunol`
- **Primary Established Diagnosis of Case:** Hypomorphic IL2RG deficiency (leaky X-SCID) presenting as Hyper-IgE-like syndrome
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_TARGET_CASE`** (Prompt Decision Enum: `EXCLUDED_NON_TARGET_CASE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 7-year-old Algerian boy admitted for recurrent sinopulmonary infections and refractory eczema due to hypomorphic IL2RG mutation; had resolved cutaneous leishmaniasis at age 5.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `HISTORICAL_RESOLVED`
6. **Step 7 — Temporality (`step7_temporality`):** `HISTORICAL_RESOLVED`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `PAST_HISTORY`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E3_SUPPORTIVE_NON_SPECIFIC`
   - **Evidence Item 1:** `case_text[750:1014]` | Test: `Past medical history of cutaneous leishmaniasis treatment` | Target: `Cutaneous leishmaniasis` | Specimen: `skin` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E3_SUPPORTIVE`)
     > "He suffered from severe eczema since the age of 4 years, refractory to topical corticosteroids; one year later, he also developed a cutaneous leishmaniasis treated successfully with pentavalent antimonial salts (meglumine antimoniate) by parenteral administration."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_TARGET_CASE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 7-year-old Algerian boy presented for evaluation of recurrent sinopulmonary infections and refractory eczema and was diagnosed with a hypomorphic IL2RG mutation (leaky X-SCID). His medical history noted an episode of cutaneous leishmaniasis at age 5 that was successfully treated with parenteral meglumine antimoniate. Because the infection was a resolved historical episode (temporality HISTORICAL_RESOLVED, clinical role PAST_HISTORY) with no active disease or E1/E2 laboratory confirmation in the current episode, VPD is not satisfied -> EXCLUDED_NON_TARGET_CASE.

### Case 06: `PMC6662440_01::Leishmaniasis` (`PMC6662440_01`)

- **Article Title:** Lymphomatoid Papulosis Type A: A Case Report of the "Wait-and-See Strategy" in a 27-Year-Old Male Patient with Extensive Disease
- **Demographics (Metadata):** Age `27.0`, Gender `Male`, Year `2019`, Journal `Case Rep Dermatol Med`
- **Primary Established Diagnosis of Case:** Lymphomatoid papulosis type A (primary cutaneous CD30+ lymphoproliferative disorder)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 27-year-old male with extensive lymphomatoid papulosis type A.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[870:1098]` | Test: `Clinical differential diagnosis` | Target: `Cutaneous leishmaniasis` | Specimen: `None` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The differential diagnosis included lymphomatoid papulosis, other cutaneous lymphomas, sarcoidosis, histiocytosis, and cutaneous infections (cutaneous leishmaniasis, atypical mycobacterial infection, and bacillary angiomatosis)."
   - **Evidence Item 2:** `case_text[1297:1556]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "No other abnormal laboratory results were found (serology for CMV, EBV, HIV, HBV, HCV, Toxoplasma, Treponema pallidum, Leishmania, Coxiella burnetii, Mycoplasma pneumonia, Chlamydia pneumonia, Quantiferon test, RF, IgA, IgG, IgM, C3, C4, ANA, and ENA Screen)."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 27-year-old male presented with ulcerated and nodular skin lesions ultimately diagnosed by biopsy and CD30+ immunophenotyping as lymphomatoid papulosis type A. Cutaneous leishmaniasis was included in the initial differential diagnosis, and Leishmania serology was normal/negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 07: `PMC4160901_01::Leishmaniasis` (`PMC4160901_01`)

- **Article Title:** Challenging clinical cases in HCV infection
- **Demographics (Metadata):** Age `68.0`, Gender `Male`, Year `2014`, Journal `BMC Infect Dis`
- **Primary Established Diagnosis of Case:** Hepatocellular carcinoma secondary to chronic Hepatitis C virus infection
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 68-year-old Italian male with chronic HCV infection and hepatocellular carcinoma.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1341:1456]` | Test: `Leishmania IgG and IgM serology` | Target: `Leishmania spp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serology for Salmonella spp. (Widal), Rickettsia spp. (Weil Felix) and Leishmania spp. (IgG and IgM) were negative;"
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 68-year-old male with prolonged fever, hepatomegaly, and a cystic-appearing hepatic mass was evaluated for infectious causes before liver biopsy confirmed HCV-associated hepatocellular carcinoma. Serology (IgG and IgM) for Leishmania spp. was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 08: `PMC3938368_01::Leishmaniasis` (`PMC3938368_01`)

- **Article Title:** Extra-pulmonary manifestations of paracoccidioidomycosis associated with acquired immunodeficiency syndrome: a case report
- **Demographics (Metadata):** Age `28.0`, Gender `Male`, Year `2014`, Journal `An Bras Dermatol`
- **Primary Established Diagnosis of Case:** Disseminated paracoccidioidomycosis (Paracoccidioides brasiliensis) with HIV/AIDS coinfection
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 28-year-old Brazilian male with HIV/AIDS and disseminated paracoccidioidomycosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1340:1386]` | Test: `Leishmaniasis screening exam` | Target: `Leishmaniasis` | Specimen: `None` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The Leishmaniasis screening exam was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 28-year-old HIV-positive male presented with left knee monoarthritis and polymorphic ulcerated skin lesions. The leishmaniasis screening exam was negative, and biopsy and culture of synovial tissue and skin confirmed disseminated Paracoccidioides brasiliensis infection. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 09: `PMC6587139_01::Leishmaniasis` (`PMC6587139_01`)

- **Article Title:** Case Report: Ocular toxoplasmosis in a WHIM syndrome immunodeficiency patient
- **Demographics (Metadata):** Age `14.0`, Gender `Male`, Year `2019`, Journal `F1000Res`
- **Primary Established Diagnosis of Case:** Ocular toxoplasmosis (Toxoplasma gondii) in WHIM syndrome
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 14-year-old Hispanic male with WHIM syndrome and ocular toxoplasmosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3221:3432]` | Test: `Parasitic pathogen testing` | Target: `Leishmania` | Specimen: `None` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Tests for other viral (CMV, EBV, VZV, HSV, dengue), fungal (Histoplasma, Cryptococcus), bacterial (Bartonella, Rickettsia, Legionella, Mycobacterium) and parasitic (Leishmania, Toxocara) pathogens were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 14-year-old male with WHIM syndrome presented with sudden right-eye blindness caused by ocular toxoplasmosis (Toxoplasma gondii PCR positive in vitreous fluid). Diagnostic testing for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 10: `PMC4782654_01::Leishmaniasis` (`PMC4782654_01`)

- **Article Title:** Phaeohyphomycosis in renal transplantation: report of two cases
- **Demographics (Metadata):** Age `57.0`, Gender `Male`, Year `2016`, Journal `An Bras Dermatol`
- **Primary Established Diagnosis of Case:** Cutaneous phaeohyphomycosis (Exophiala sp.)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 57-year-old male kidney transplant recipient with cutaneous phaeohyphomycosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[429:544]` | Test: `Clinical differential diagnosis` | Target: `Leishmaniasis` | Specimen: `skin lesion` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The initial diagnostic hypotheses were sporotrichosis, paracoccidioidomycosis, leishmaniasis and phaeohyphomycosis."
   - **Evidence Item 2:** `case_text[545:790]` | Test: `Direct mycological examination and culture` | Target: `Exophiala sp.` | Specimen: `skin lesion` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Direct mycological examination revealed irregular and septate moniliform hyphae of pigmented fungi. Culture on Sabouraud-Agar with chloramphenicol demonstrated vegetative chambered hyphae with septate annellophores, compatible with Exophiala sp."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 57-year-old male renal transplant recipient presented with sporotrichoid nodules on the right foot and leg. Leishmaniasis was considered among the initial diagnostic hypotheses, but direct mycological examination, Sabouraud culture, and histopathology (Fontana-Masson and Gridley stains) confirmed phaeohyphomycosis caused by Exophiala sp., ruling out leishmaniasis -> NEGATIVE.

### Case 11: `PMC6936928_01::Leishmaniasis` (`PMC6936928_01`)

- **Article Title:** Cervical Lymphadenopathy in a Nonagenarian Woman: What to Think?
- **Demographics (Metadata):** Age `93.0`, Gender `Female`, Year `2019`, Journal `Eur J Case Rep Intern Med`
- **Primary Established Diagnosis of Case:** Cervical tuberculous lymphadenitis (Mycobacterium tuberculosis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 93-year-old Caucasian woman with cervical tuberculous lymphadenitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2259:2451]` | Test: `Lymph node biopsy PCR` | Target: `Leishmania infantum` | Specimen: `cervical lymph node` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "PCR assessment of the samples was negative for MT, Nocardia, Mycobacterium avium complex, Toxoplasma gondii, Aspergillus fumigatus, Bartonella spp., Treponema pallidum and Leishmania infantum."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 93-year-old woman with suppurative cervical lymphadenitis underwent excisional lymph node biopsy. PCR testing of the biopsy sample for Leishmania infantum was explicitly negative, and lymph node culture subsequently isolated Mycobacterium tuberculosis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 12: `PMC6875186_01::Leishmaniasis` (`PMC6875186_01`)

- **Article Title:** A Case of Oral Histoplasmosis Concomitant with Pulmonary Tuberculosis
- **Demographics (Metadata):** Age `46.0`, Gender `Male`, Year `2019`, Journal `Case Rep Dent`
- **Primary Established Diagnosis of Case:** Oral histoplasmosis (Histoplasma capsulatum) concomitant with pulmonary tuberculosis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 46-year-old man with oral histoplasmosis concomitant with pulmonary tuberculosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1575:1769]` | Test: `Oral biopsy immunohistochemistry` | Target: `Leishmania spp.` | Specimen: `oral mucosa biopsy` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "In addition, the immunohistochemical reactivity to Histoplasma using polyclonal antibody was positive; for polyclonal P. brasiliensis, Leishmania spp. and Calmette-Guerin bacillus were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 46-year-old man with pulmonary tuberculosis presented with vegetative intraoral lesions. Immunohistochemistry on the oral mucosal biopsy was positive for Histoplasma capsulatum and explicitly negative for polyclonal Leishmania spp. antibody. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 13: `PMC3573448_01::Leishmaniasis` (`PMC3573448_01`)

- **Article Title:** A rare case of keloidal granuloma faciale with extra-facial lesions
- **Demographics (Metadata):** Age `33.0`, Gender `Male`, Year `2013`, Journal `Indian Dermatol Online J`
- **Primary Established Diagnosis of Case:** Keloidal granuloma faciale
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 33-year-old male with keloidal granuloma faciale on the face and left shoulder.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[700:873]` | Test: `Clinical differential diagnosis` | Target: `Cutaneous leishmaniasis` | Specimen: `skin` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The clinical differential diagnoses considered were keloid, lupus vulgaris, nodular sarcoidosis, cutaneous leishmaniasis, granuloma annulare, and erythema elevatum diutinum."
   - **Evidence Item 2:** `case_text[1379:1452]` | Test: `Skin biopsy histopathology` | Target: `Granuloma faciale` | Specimen: `forehead and shoulder skin biopsy` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The above findings were consistent with a diagnosis of granuloma faciale."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 33-year-old male presented with chronic reddish-brown keloidal plaques and nodules on the face and shoulder. Cutaneous leishmaniasis was listed in the clinical differential diagnosis, but skin biopsies from the forehead and shoulder established the diagnosis of granuloma faciale, ruling out cutaneous leishmaniasis -> NEGATIVE.

### Case 14: `PMC4600861_01::Leishmaniasis` (`PMC4600861_01`)

- **Article Title:** A Case Report of an Atypical Presentation of IgG4-Related Disease and Idiopathic CD4 Lymphocytopenia
- **Demographics (Metadata):** Age `43.0`, Gender `Unknown`, Year `2015`, Journal `Case Rep Med`
- **Primary Established Diagnosis of Case:** IgG4-related disease and idiopathic CD4 lymphocytopenia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 43-year-old patient (50 years old at later follow-up) with IgG4-related disease and idiopathic CD4 lymphocytopenia.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1701:1844]` | Test: `Serology and bone marrow aspirate` | Target: `Leishmaniasis` | Specimen: `blood and bone marrow` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Tests for leishmaniasis, toxoplasma, and HIV were also negative. The bone marrow aspirate excluded lymphoproliferative and parasitic disorders."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A patient with multiorgan IgG4-related disease and idiopathic CD4 lymphocytopenia underwent extensive infectious evaluation. Tests for leishmaniasis were explicitly negative and bone marrow aspirate excluded parasitic disorders. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 15: `PMC10436321_01::Leishmaniasis` (`PMC10436321_01`)

- **Article Title:** Case report: Coxiella burnetii endocarditis in the absence of evident exposure
- **Demographics (Metadata):** Age `55.0`, Gender `Male`, Year `2023`, Journal `Front Med (Lausanne)`
- **Primary Established Diagnosis of Case:** Chronic Q fever endocarditis (Coxiella burnetii)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 55-year-old male with prosthetic aortic valve and Coxiella burnetii endocarditis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1997:2169]` | Test: `Serological analysis` | Target: `Leishmania spp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Tests for Legionella pneumophila, Treponema pallidum, Coxsackie virus A and B, Parvovirus B19, Leishmania spp., Toxoplasma gondii, HIV, and Hepatitis B and C were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 55-year-old male with fever of unknown origin and a prosthetic aortic valve was diagnosed with chronic Q fever (Coxiella burnetii) endocarditis. Serological testing for Leishmania spp. was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 16: `PMC5866856_01::Leishmaniasis` (`PMC5866856_01`)

- **Article Title:** Postinfantile Giant Cell Hepatitis with Features of Acute Severe Autoimmune Hepatitis Probably Triggered by Diclofenac in a Patient with Primary Myelofibrosis
- **Demographics (Metadata):** Age `76.0`, Gender `Female`, Year `2018`, Journal `Case Reports Hepatol`
- **Primary Established Diagnosis of Case:** Postinfantile giant cell hepatitis / acute severe autoimmune hepatitis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 76-year-old female with postinfantile giant cell hepatitis and acute severe autoimmune hepatitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1808:2173]` | Test: `Microbiological investigation` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The remaining haematological, microbiological, virological, and biochemical parameters including blood cultures and investigation for hepatitis viruses A, B, C, and E as well as Epstein-Barr virus (EBV), cytomegalovirus (CMV), human immunodeficiency virus (HIV), herpes simplex virus (HSV), tuberculosis, leishmaniasis, brucellosis, and leptospirosis were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 76-year-old woman with primary myelofibrosis presented with acute severe hepatitis and postinfantile giant cell hepatitis (AS-AIH likely triggered by diclofenac). Microbiological investigation for leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 17: `PMC7778187_01::Leishmaniasis` (`PMC7778187_01`)

- **Article Title:** Pseudotumoral form of schistosomiasis mimicking neuroendocrine tumor: a case report and brief review of the differential diagnosis of retroperitoneal masses
- **Demographics (Metadata):** Age `45.0`, Gender `Male`, Year `2020`, Journal `Pan Afr Med J`
- **Primary Established Diagnosis of Case:** Pseudotumoral retroperitoneal schistosomiasis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 45-year-old Caucasian male with retroperitoneal pseudotumoral schistosomiasis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2494:2900]` | Test: `Serological study` | Target: `Leishmania spp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The following serological studies were carried out: hepatitis A virus; Epstein-Barr virus; Trypanosoma cruzi; cytomegalovirus; Ac HBs; Ag HBs; Ac HBc T; HIV 1 + 2; Toxoplasma gondii; Entamoeba histolytica; Echinococcus granulosus; Taenia solium (IgG); Leishmania spp.; strongyloides and schistosoma. All results were negative and do not showed acute infection, except schistosoma with IgM and IgG positive."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 45-year-old male with a 4-cm paraaortic retroperitoneal mass was diagnosed with pseudotumoral schistosomiasis. Serological testing for Leishmania spp. was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 18: `PMC3120277_01::Leishmaniasis` (`PMC3120277_01`)

- **Article Title:** Infective endocarditis presents as isolated splenomegaly
- **Demographics (Metadata):** Age `45.0`, Gender `Male`, Year `2011`, Journal `J Cardiovasc Dis Res`
- **Primary Established Diagnosis of Case:** Subacute bacterial infective endocarditis (Streptococcus viridans)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 45-year-old man presenting with isolated splenomegaly later diagnosed with Streptococcus viridans infective endocarditis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1651:1960]` | Test: `Kala-azar workup` | Target: `Leishmania donovani (kala-azar)` | Specimen: `blood/serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "A complete blood cell count, chest X-ray, liver enzymes examination, thyroid function test, malaria smear, kala-azar, infectious mononucleosis Ab, anti-nuclear factor, Coomb's test, blood cultures, Serology for HIV, hepatitis and other infections, electrocardiogram, and urinalysis all showed normal findings."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 45-year-old man evaluated for isolated splenomegaly had normal/negative findings on kala-azar (visceral leishmaniasis) testing and bone marrow biopsy, and was subsequently diagnosed with Streptococcus viridans aortic valve endocarditis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 19: `PMC8252363_01::Leishmaniasis` (`PMC8252363_01`)

- **Article Title:** Sirolimus is effective in autoimmune lymphoproliferative syndrome-type III: A pedigree case report with homozygous variation PRKCD
- **Demographics (Metadata):** Age `10.0`, Gender `Male`, Year `2021`, Journal `Int J Immunopathol Pharmacol`
- **Primary Established Diagnosis of Case:** Autoimmune lymphoproliferative syndrome type III (homozygous PRKCD deficiency)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 10-year-old boy with autoimmune lymphoproliferative syndrome-type III due to homozygous PRKCD nonsense mutation.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[948:1084]` | Test: `Infection marker analysis` | Target: `Leishmania donovani` | Specimen: `serum/blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "In addition, the analysis of markers for measles virus, parvovirus B19, schistosomiasis, and Leishmania donovani infection was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 10-year-old boy with splenomegaly, lymphadenopathy, and cytopenias was diagnosed with ALPS-type III caused by a homozygous PRKCD variant (c.36T>G, p.Y12X). Testing for Leishmania donovani infection was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 20: `PMC7387958_01::Leishmaniasis` (`PMC7387958_01`)

- **Article Title:** Hemophagocytic Lymphohistiocytosis (HLH) in a Patient with Disseminated Histoplasmosis
- **Demographics (Metadata):** Age `61.0`, Gender `Female`, Year `2020`, Journal `Case Rep Hematol`
- **Primary Established Diagnosis of Case:** Disseminated histoplasmosis (Histoplasma capsulatum) with secondary HLH
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 61-year-old immunocompromised female with rheumatoid arthritis who developed HLH secondary to disseminated histoplasmosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2926:3034]` | Test: `Giemsa stain, immunohistochemistry, and PCR` | Target: `Leishmania` | Specimen: `bone marrow` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Giemsa staining, immunohistochemistry, and polymerase chain reaction (PCR) for leishmania were all negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 61-year-old female on methotrexate and infliximab developed HLH secondary to disseminated histoplasmosis (confirmed on bone marrow silver stain and urine Histoplasma antigen). Giemsa staining, immunohistochemistry, and PCR for Leishmania on bone marrow were all explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 21: `PMC6378761_01::Leishmaniasis` (`PMC6378761_01`)

- **Article Title:** Secondary Hemophagocytic Lymphohistiocytosis: A Challenging Diagnosis in a Patient with Autoimmune Hepatitis
- **Demographics (Metadata):** Age `34.0`, Gender `Male`, Year `2019`, Journal `Case Rep Crit Care`
- **Primary Established Diagnosis of Case:** Secondary hemophagocytic lymphohistiocytosis associated with autoimmune hepatitis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 34-year-old Pakistani male with cirrhosis from autoimmune hepatitis who developed secondary HLH.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2378:2429]` | Test: `Bone marrow testing for leishmaniasis` | Target: `Leishmaniasis` | Specimen: `bone marrow` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Bone marrow testing for leishmaniasis was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 34-year-old male with autoimmune hepatitis cirrhosis presented with secondary HLH. Bone marrow testing for leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 22: `PMC10434771_01::Leishmaniasis` (`PMC10434771_01`)

- **Article Title:** The application of metagenomic next-generation sequencing in pathogen diagnosis: a bibliometric analysis based on Web of Science
- **Demographics (Metadata):** Age `14.0`, Gender `Male`, Year `2023`, Journal `Front Cell Infect Microbiol`
- **Primary Established Diagnosis of Case:** Not applicable (bibliometric review of mNGS in pathogen diagnosis)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_SINGLE_PATIENT`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `SYSTEMATIC_REVIEW`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `AGGREGATE_STUDY_UNIT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `NONE` — Bibliometric review of 325 publications on metagenomic next-generation sequencing (mNGS); not a clinical case report.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `CONTEXT_ONLY`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `UNCERTAIN`
6. **Step 7 — Temporality (`step7_temporality`):** `UNKNOWN`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[4416:4670]` | Test: `Bibliometric literature discussion` | Target: `Leishmaniasis` | Specimen: `None` | Result: `NOT_APPLICABLE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "This is possibly because mNGS is used for detecting rare pathogens, which are distributed regionally, such as leishmaniasis in the central and western regions of China, hepatic echinococcosis in cattle-producing areas, and Dengue fever in tropical areas."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_SINGLE_PATIENT` | Failure Flags: `['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
12. **Clinical Rationale:** This article is a bibliometric analysis of 325 studies on metagenomic next-generation sequencing (mNGS) from Web of Science, not a single-patient case report. Leishmaniasis is mentioned solely as an example of a regionally distributed pathogen in China. Document scope is SYSTEMATIC_REVIEW / AGGREGATE_STUDY_UNIT -> EXCLUDED_NON_SINGLE_PATIENT.

### Case 23: `PMC6305016_01::Leishmaniasis` (`PMC6305016_01`)

- **Article Title:** Streptococcus thoraltensis Bacteremia: First Described Case as a Fever of Unknown Origin in Human
- **Demographics (Metadata):** Age `55.0`, Gender `Female`, Year `2018`, Journal `Case Rep Infect Dis`
- **Primary Established Diagnosis of Case:** Streptococcus thoraltensis bacteremia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 55-year-old female with fever of unknown origin caused by Streptococcus thoraltensis bacteremia.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1204:1459]` | Test: `Diagnostic workup excluding Leishmania` | Target: `Leishmania` | Specimen: `blood/serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "From three blood cultures obtained on the 1st, 2nd, and 3rd day of her hospitalization, when she was febrile, Streptococcus thoraltensis was identified, while infection caused by Brucella, Mycobacterium tuberculosis, Coxiella, and Leishmania was excluded."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 55-year-old woman admitted with a 2-month history of fever of unknown origin had Streptococcus thoraltensis isolated in three blood cultures, while infection caused by Leishmania was explicitly excluded. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 24: `PMC4150115_01::Leishmaniasis` (`PMC4150115_01`)

- **Article Title:** Importance of the association of molecular and immunological diagnosis in immunocompetent patient with Histoplasma capsulatum and Cryptoccocus neoformans infection: a case report
- **Demographics (Metadata):** Age `29.0`, Gender `Female`, Year `2014`, Journal `J Venom Anim Toxins Incl Trop Dis`
- **Primary Established Diagnosis of Case:** Histoplasma capsulatum and Cryptococcus neoformans coinfection
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 29-year-old immunocompetent Brazilian woman with Histoplasma capsulatum and Cryptococcus neoformans coinfection.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1018:1232]` | Test: `Leishmaniasis antibody serology` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Antibodies against HIV, viral hepatitis, leishmaniasis, Chagas' disease, malaria, paracoccidioidomycosis, histoplasmosis and aspergillosis, as well as skin tests for paracoccidioidin and histoplasmin were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 29-year-old immunocompetent woman in Brazil presented with respiratory symptoms and was diagnosed by nested PCR and sequencing with Histoplasma capsulatum and Cryptococcus neoformans coinfection. Antibodies against leishmaniasis were explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 25: `PMC4909855_01::Leishmaniasis` (`PMC4909855_01`)

- **Article Title:** Urinary capillariosis in six dogs from Italy
- **Demographics (Metadata):** Age `5.0`, Gender `Male`, Year `2016`, Journal `Open Vet J`
- **Primary Established Diagnosis of Case:** Canine urinary capillariosis (Pearsonema plica) and glomerular amyloidosis
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_SERIES`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient (Case 1 of 6 dogs): 5-year-old intact male Maremma hound dog with urinary capillariosis and glomerular amyloidosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[440:579]` | Test: `Canine Leishmania serology` | Target: `Leishmania sp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serological tests were negative for Leishmania sp. and tick-borne diseases, except for a low positive IgG titer (1:40) for Ehrlichia canis."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case (Case 1 of a 6-dog series) describing a 5-year-old male Maremma hound dog with Pearsonema plica urinary capillariosis and glomerular amyloidosis, in which serology for Leishmania sp. was negative. Excluded as non-human animal case -> EXCLUDED_NON_HUMAN.

### Case 26: `PMC4909855_02::Leishmaniasis` (`PMC4909855_02`)

- **Article Title:** Urinary capillariosis in six dogs from Italy
- **Demographics (Metadata):** Age `4.0`, Gender `Male`, Year `2016`, Journal `Open Vet J`
- **Primary Established Diagnosis of Case:** Canine urinary capillariosis (Pearsonema plica) and canine leishmaniasis
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_SERIES`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient (Case 2 of 6 dogs): 4-year-old intact male mixed-breed dog referred for leishmaniasis and diagnosed with Pearsonema plica urinary capillariosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `AFFIRMED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `ACTIVE_COMORBIDITY`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E3_SUPPORTIVE_NON_SPECIFIC`
   - **Evidence Item 1:** `case_text[128:263]` | Test: `Clinical referral history` | Target: `Leishmaniasis` | Specimen: `None` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E3_SUPPORTIVE`)
     > "This patient was referred for leishmaniasis, with no history of urinary signs and renal function parameters were in their normal range."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT']`
12. **Clinical Rationale:** Veterinary case (Case 2 of a 6-dog series) describing a 4-year-old male mixed-breed dog referred for leishmaniasis and found to have Pearsonema plica eggs in urine sediment. Because ccu_type is ANIMAL_CASE (canine subject), it is ineligible for a human positive diagnosis -> EXCLUDED_NON_HUMAN.

### Case 27: `PMC4909855_03::Leishmaniasis` (`PMC4909855_03`)

- **Article Title:** Urinary capillariosis in six dogs from Italy
- **Demographics (Metadata):** Age `4.0`, Gender `Male`, Year `2016`, Journal `Open Vet J`
- **Primary Established Diagnosis of Case:** Canine urinary capillariosis (Pearsonema plica)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_SERIES`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient (Case 3 of 6 dogs): 4-year-old intact male mixed-breed dog presented for evaluation of leishmaniasis and diagnosed with urinary capillariosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `POSSIBLE_HYPOTHETICAL`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `DIFFERENTIAL_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[98:248]` | Test: `Clinical evaluation reason` | Target: `Leishmaniasis` | Specimen: `None` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The dog was presented for an evaluation of leishmaniasis, he had no history of urinary signs and renal function parameters were in their normal range."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT']`
12. **Clinical Rationale:** Veterinary case (Case 3 of a 6-dog series) describing a 4-year-old male mixed-breed dog rescued from a shelter and presented for evaluation of leishmaniasis, diagnosed with Pearsonema plica urinary capillariosis. Excluded as non-human veterinary case -> EXCLUDED_NON_HUMAN.

### Case 28: `PMC6390538_01::Leishmaniasis` (`PMC6390538_01`)

- **Article Title:** Evolution into Takayasu arteritis in a patient presenting with acute pulmonary oedema due to severe aortic regurgitation; a case report
- **Demographics (Metadata):** Age `25.0`, Gender `Female`, Year `2018`, Journal `BMC Rheumatol`
- **Primary Established Diagnosis of Case:** Takayasu arteritis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 25-year-old Sri Lankan female with severe aortic regurgitation evolving into Takayasu arteritis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[4008:4179]` | Test: `Bone marrow culture for Leishmania` | Target: `Leishmania` | Specimen: `bone marrow` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Bone marrow biopsy revealed reactive marrow with no other abnormalities while bone marrow culture for bacteria, fungi, mycobacteria, brucella and leishmania were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 25-year-old Sri Lankan woman with acute pulmonary edema from severe aortic regurgitation and persistently elevated ESR was ultimately diagnosed with Takayasu arteritis. Bone marrow culture for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 29: `PMC7661936_01::Leishmaniasis` (`PMC7661936_01`)

- **Article Title:** Tuberculosis-Associated HLH in an 8-Month-Old Infant: A Case Report and Review
- **Demographics (Metadata):** Age `0.0`, Gender `Male`, Year `2020`, Journal `Front Pediatr`
- **Primary Established Diagnosis of Case:** Disseminated tuberculosis-associated hemophagocytic lymphohistiocytosis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 8-month-old male infant (age=0.0 in metadata) with disseminated tuberculosis-associated HLH managed on ECMO.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[4028:4202]` | Test: `Leishmania PCR and IgG/IgM serology` | Target: `Leishmania` | Specimen: `blood/serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Also negative were results of testing for leishmania, legionella, aspergillus, Pneumocystis jirovecii, Hemophilus influenza b, and pneumococcus-PCR/immunoglobulins (IgG/IgM)."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** An 8-month-old boy with fever, pancytopenia, and acute respiratory failure requiring ECMO was diagnosed with HLH secondary to disseminated Mycobacterium tuberculosis. Testing (PCR and IgG/IgM) for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 30: `PMC8417874_01::Leishmaniasis` (`PMC8417874_01`)

- **Article Title:** Case Report: Positive Outcome of a Suspected Drug-Associated (Immune Mediated) Reaction in a 4-Year-Old Male French Bulldog
- **Demographics (Metadata):** Age `4.0`, Gender `Male`, Year `2021`, Journal `Front Vet Sci`
- **Primary Established Diagnosis of Case:** Canine drug-induced toxic epidermal necrolysis (TEN)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 4-year-old intact male French Bulldog with drug-associated toxic epidermal necrolysis (TEN).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[884:1062]` | Test: `Outside presumptive clinical diagnosis` | Target: `Leishmaniosis` | Specimen: `None` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E3_SUPPORTIVE`)
     > "The dog was then treated with allopurinol [400 mg once daily, (10 mg/kg/twice a day):Allopurinol Teva 200 mg, TEVA, Paris, France] after a presumptive diagnosis of leishmaniosis."
   - **Evidence Item 2:** `case_text[4981:5092]` | Test: `Indirect immunofluorescence / ELISA test` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "An indirect immunofluorescence test [Enzyme-linked immunosorbent assay (ELISA)] for leishmaniasis was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `True` — An outside veterinarian initially prescribed allopurinol for presumptive leishmaniosis, but subsequent indirect immunofluorescence / ELISA testing for leishmaniasis at the referral hospital was negative and biopsy confirmed toxic epidermal necrolysis.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case report of a 4-year-old male French Bulldog with beta-lactam-associated toxic epidermal necrolysis (TEN), in which an initial presumptive diagnosis of leishmaniosis was refuted by a negative ELISA/IFAT test. Excluded from the human benchmark because ccu_type is ANIMAL_CASE -> EXCLUDED_NON_HUMAN.

### Case 31: `PMC3420495_01::Leishmaniasis` (`PMC3420495_01`)

- **Article Title:** A delayed diagnosis: conflicting investigation results should be challenged
- **Demographics (Metadata):** Age `43.0`, Gender `Female`, Year `2011`, Journal `Case Rep Pathol`
- **Primary Established Diagnosis of Case:** Advanced HIV-1 infection with multicentric Castleman's disease, Kaposi's sarcoma, latent syphilis, and visceral leishmaniasis coinfection
- **Final Dataset Label (`step12_dataset_label`):** **`POSITIVE`** (Prompt Decision Enum: `POSITIVE` | VPD Satisfied: `True` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 43-year-old Caucasian German salesman (male in case_text; metadata gender field erroneously states Female) with advanced HIV-1, Kaposi's sarcoma, multicentric Castleman's disease, latent syphilis, and visceral leishmaniasis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `AFFIRMED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `ACTIVE_COMORBIDITY`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E1_DISEASE_SPECIFIC_CONFIRMATORY`
   - **Evidence Item 1:** `case_text[5496:5595]` | Test: `Bone marrow trephine biopsy histopathology` | Target: `Leishmania (visceral leishmaniasis)` | Specimen: `bone marrow` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E1_CONFIRMATORY`)
     > "A bone marrow trephine biopsy also showed Leishmaniasis (Figure 5) which was treated with ambisome."
   - **Evidence Item 2:** `case_text[6187:6375]` | Test: `Clinical response to liposomal amphotericin B (AmBisome)` | Target: `Leishmaniasis` | Specimen: `None` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E3_SUPPORTIVE`)
     > "Apart from mild shingles which responded to high-dose acyclovir, he showed a good splenic and CT response to chemotherapy with the syphilis and leishmaniasis being successfully eradicated."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `True`
11. **Step 12 — Final Label & Failure Flags:** `POSITIVE` | Failure Flags: `[]`
12. **Clinical Rationale:** A 43-year-old male salesman presented with anemia, weight loss, pancytopenia, and massive hepatosplenomegaly, and was diagnosed with advanced HIV-1 infection, Kaposi's sarcoma, plasma-cell variant multicentric Castleman's disease, latent syphilis, and visceral leishmaniasis. Bone marrow trephine biopsy directly demonstrated Leishmaniasis (Figure 5; E1 confirmatory evidence), and the infection was successfully eradicated following treatment with liposomal amphotericin B (AmBisome). Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role ACTIVE_COMORBIDITY. All VPD criteria are satisfied -> POSITIVE.

### Case 32: `PMC5759608_01::Leishmaniasis` (`PMC5759608_01`)

- **Article Title:** Type 1 autoimmune hepatitis presenting with severe autoimmune neutropenia
- **Demographics (Metadata):** Age `59.0`, Gender `Female`, Year `2018`, Journal `Ann Gastroenterol`
- **Primary Established Diagnosis of Case:** Type 1 autoimmune hepatitis with severe autoimmune neutropenia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 59-year-old female with type 1 autoimmune hepatitis and severe autoimmune neutropenia.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1937:2153]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serological markers for hepatitis A, B and C, cytomegalovirus, Epstein-Barr virus, herpes simplex viruses, parvovirus B19, human herpes virus 6, HIV, toxoplasma, brucella, leishmania and mycoplasma were all negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 59-year-old female presented with acute hepatocellular injury, marginal splenomegaly, and agranulocytosis, and was diagnosed with type 1 autoimmune hepatitis and autoimmune neutropenia. Serological markers for Leishmania were explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 33: `PMC7239889_01::Leishmaniasis` (`PMC7239889_01`)

- **Article Title:** Idiopathic CD4 Lymphocytopenia: Current Insights
- **Demographics (Metadata):** Age `9.0`, Gender `Female`, Year `2020`, Journal `Immunotargets Ther`
- **Primary Established Diagnosis of Case:** Not applicable (narrative review of Idiopathic CD4 Lymphocytopenia)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_SINGLE_PATIENT`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `SYSTEMATIC_REVIEW`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `AGGREGATE_STUDY_UNIT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `NONE` — Narrative literature review of Idiopathic CD4 Lymphocytopenia summarizing 164 published cases; not a single-patient case report.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `CONTEXT_ONLY`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `UNCERTAIN`
6. **Step 7 — Temporality (`step7_temporality`):** `UNKNOWN`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[10359:10419]` | Test: `Literature review summary` | Target: `Leishmaniasis` | Specimen: `None` | Result: `NOT_APPLICABLE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "Leishmaniasis is the most common parasitic infection in ICL."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_SINGLE_PATIENT` | Failure Flags: `['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
12. **Clinical Rationale:** This article is a narrative literature review of Idiopathic CD4 Lymphocytopenia (ICL) summarizing findings across published cohorts (including 164 cases reviewed by the authors). Leishmaniasis is discussed only as an opportunistic parasitic infection reported in ICL literature. Document scope is SYSTEMATIC_REVIEW / AGGREGATE_STUDY_UNIT -> EXCLUDED_NON_SINGLE_PATIENT.

### Case 34: `PMC6399754_01::Leishmaniasis` (`PMC6399754_01`)

- **Article Title:** An immigrant with acquired immunodeficiency syndrome presenting with a rash: A case report
- **Demographics (Metadata):** Age `58.0`, Gender `Female`, Year `2019`, Journal `SAGE Open Med Case Rep`
- **Primary Established Diagnosis of Case:** Disseminated histoplasmosis (Histoplasma capsulatum) in HIV/AIDS
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 58-year-old Zimbabwean woman in Canada with untreated HIV/AIDS and disseminated histoplasmosis presenting with leonine facies.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1229:1443]` | Test: `Clinical differential diagnosis` | Target: `Disseminated leishmaniasis` | Specimen: `skin` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The clinical differential diagnosis for her rash included a systemic fungal infection, mycobacterial infection, viral exanthem, disseminated leishmaniasis, crusted scabies, cutaneous lymphoma, and Kaposi's sarcoma."
   - **Evidence Item 2:** `case_text[2045:2227]` | Test: `Skin, bone marrow, lymph node, and blood fungal cultures` | Target: `Histoplasma capsulatum` | Specimen: `skin, bone marrow, lymph node, blood` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "A second lesional skin biopsy for culture grew Histoplasma capsulatum. Biopsies of her bone marrow and retroperitoneal lymph nodes also grew H. capsulatum, as did her blood cultures."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 58-year-old woman with advanced HIV/AIDS presented with leonine facies and a widespread papular/plaque rash. Disseminated leishmaniasis was considered in the clinical differential diagnosis, but skin, bone marrow, lymph node, and blood cultures all grew Histoplasma capsulatum, establishing disseminated histoplasmosis and ruling out leishmaniasis -> NEGATIVE.

### Case 35: `PMC7365499_01::Leishmaniasis` (`PMC7365499_01`)

- **Article Title:** Pancytopenia induced by secondary hemophagocytic lymphohistiocytosis: A rare, overlooked dreadful complication of Plasmodium vivax
- **Demographics (Metadata):** Age `7.0`, Gender `Female`, Year `2020`, Journal `Trop Parasitol`
- **Primary Established Diagnosis of Case:** Plasmodium vivax malaria-induced hemophagocytic lymphohistiocytosis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 7-year-old Indian girl with secondary HLH caused by Plasmodium vivax malaria.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[745:1019]` | Test: `rK39 rapid immunochromatographic test` | Target: `Visceral leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Human immunodeficiency virus serology, hepatitis B surface antigen, antibodies against hepatitis C virus, the Epstein-Barr virus, cytomegalovirus, measles, Widal test, K39 test for visceral leishmaniasis, and rapid diagnostic tests (RDTs) for malarial antigen were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 7-year-old girl from New Delhi presented with fever, hepatosplenomegaly, and pancytopenia due to secondary HLH triggered by Plasmodium vivax (confirmed on peripheral blood smear and bone marrow hemozoin bleaching). The K39 test for visceral leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 36: `PMC7657701_02::Leishmaniasis` (`PMC7657701_02`)

- **Article Title:** Severe Pharyngodynia Followed by Migratory Polyarthritis and High Fever in Young Immigrants: Remember That Rheumatic Fever Is Still Relevant in 2020!
- **Demographics (Metadata):** Age `18.0`, Gender `Male`, Year `2020`, Journal `Case Rep Infect Dis`
- **Primary Established Diagnosis of Case:** Acute rheumatic fever with rheumatic heart disease
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 18-year-old Pakistani male immigrant in Greece (Patient 2 of a 2-case report) with acute rheumatic fever and rheumatic heart disease.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2286:2676]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Actually, a serological work-up for zoonosis (Brucella, Coxiella, Rickettsia, Borrelia, Leptospira, Leishmania, and other parasites including investigation for Trichinella, Entamoeba, and Echinococcus), sexually transmitted diseases (syphilis, N. gonorrhoeae, U. urealyticum, M. hominis, and C. trachomatis), viral hepatitis A, B, C, and E, and human immunodeficiency virus tested negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** An 18-year-old male immigrant presented with fever, pharyngodynia, ankle arthritis, and carditis, and was diagnosed with acute rheumatic fever. Serological testing for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 37: `PMC7083192_01::Leishmaniasis` (`PMC7083192_01`)

- **Article Title:** Fever During Anti-integrin Therapy: New Immunodeficiency
- **Demographics (Metadata):** Age `33.0`, Gender `Male`, Year `2020`, Journal `Eur J Case Rep Intern Med`
- **Primary Established Diagnosis of Case:** Primary cytomegalovirus (CMV) infection
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 33-year-old male with ulcerative colitis and primary sclerosing cholangitis on vedolizumab and azathioprine who developed primary CMV infection.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1636:1866]` | Test: `Diagnostic test for leishmaniasis` | Target: `Leishmaniasis` | Specimen: `blood/serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Furthermore, diagnostic tests for malaria parasites, Brucella, toxoplasma, Borrelia, Rickettsiae, leishmaniasis, beta-D-glucan and HIV were negative, as were other tests: quantiferon, monotest and antistreptolysin O titer (ASLOT)."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 33-year-old male with ulcerative colitis on vedolizumab and azathioprine presented with fever and splenomegaly and was diagnosed with primary cytomegalovirus (CMV) infection. Diagnostic testing for leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 38: `PMC7669275_02::Leishmaniasis` (`PMC7669275_02`)

- **Article Title:** Paracoccidioidomycosis due to Paracoccidioides lutzii complicated with adrenal injury and pulmonary arterial hypertension
- **Demographics (Metadata):** Age `9.0`, Gender `Male`, Year `2020`, Journal `Rev Inst Med Trop Sao Paulo`
- **Primary Established Diagnosis of Case:** Chronic paracoccidioidomycosis (Paracoccidioides lutzii)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Adult Brazilian male truck/tractor driver (metadata age=9.0 reflects childhood move to Paraguay at age 9) with chronic paracoccidioidomycosis due to Paracoccidioides lutzii; had cutaneous leishmaniasis 16 years earlier and tested seronegative for leishmaniasis in current episode.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[730:794]` | Test: `Past medical history` | Target: `Cutaneous leishmaniasis` | Specimen: `skin` | Result: `POSITIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "He has also reported a cutaneous leishmaniasis 16 years earlier."
   - **Evidence Item 2:** `case_text[899:1055]` | Test: `Leishmaniasis serology` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serological tests for HIV infection, leishmaniasis, Chagas disease, and hepatitis C virus were negative, but serum anti-HBc Ag IgG antibodies were detected."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** An adult male presented with skin lesions, chronic cough, and bilateral adrenal enlargement, confirmed by culture and ITS/gp43 sequencing as Paracoccidioides lutzii paracoccidioidomycosis. Although he reported a history of cutaneous leishmaniasis 16 years earlier (HISTORICAL_PAST), serological testing for leishmaniasis during the current episode was explicitly negative. Assertion NEGATED for current episode, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 39: `PMC10188974_02::Leishmaniasis` (`PMC10188974_02`)

- **Article Title:** Case Report: Interindividual variability and possible role of heterozygous variants in a family with deficiency of adenosine deaminase 2: are all heterozygous born equals?
- **Demographics (Metadata):** Age `47.0`, Gender `Male`, Year `2023`, Journal `Front Immunol`
- **Primary Established Diagnosis of Case:** Deficiency of adenosine deaminase 2 (DADA2)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `FAMILY_MEMBER` — Family report of DADA2 (proband 17yo male III:2, mother 51yo II:6, father 47yo II:5, and deceased 12yo brother III:1). Leishmania qRT-PCR was performed on the deceased 12-year-old brother (III:1) and was negative.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `HISTORICAL_RESOLVED`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[975:1226]` | Test: `qRT-PCR for Leishmania spp.` | Target: `Leishmania spp.` | Specimen: `blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Microbiological tests were negative, including blood cultures, qRT PCR for EBV, CMV, Mycobacteria, Leishmania spp., and serology for herpes viruses, enterovirus, Salmonella and Brucella spp., Borrelia spp., Echinococcus spp., Mycoplasma spp., and HIV."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F3_SUBJECT_COREFERENCE', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** In this familial DADA2 report (ADA2 c.1358A>G variant), microbiological workup of the proband's older brother (III:1, who died at age 12 of multiorgan failure and DRESS-like syndrome) included qRT-PCR for Leishmania spp., which was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 40: `PMC4899662_02::Leishmaniasis` (`PMC4899662_02`)

- **Article Title:** Spinal Cord Schistosomiasis: Two Different Outcomes
- **Demographics (Metadata):** Age `29.0`, Gender `Male`, Year `2016`, Journal `Case Rep Neurol`
- **Primary Established Diagnosis of Case:** Spinal cord schistosomiasis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 29-year-old Saudi male (Case 2 of 2) with spinal cord schistosomiasis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1732:1982]` | Test: `Leishmaniasis serology` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "His results for brucellosis, HIV, leishmaniasis, amebiasis, echinococcosis, and cytomegalovirus serology were all negative; furthermore, a rectal snip biopsy was negative for ova, and no schistosomal ova were detected in the patient's urine or stool."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 29-year-old Saudi male presented with bilateral lower limb weakness and urinary incontinence due to conus medullaris schistosomiasis (Schistosoma antibody titers 1:512 and 1:4096). Serology for leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 41: `PMC5585634_01::Leishmaniasis` (`PMC5585634_01`)

- **Article Title:** Isolated Splenic Cold Abscesses with Perisplenic Extension: Treated Successfully without Splenectomy
- **Demographics (Metadata):** Age `22.0`, Gender `Male`, Year `2017`, Journal `Case Rep Gastrointest Med`
- **Primary Established Diagnosis of Case:** Primary splenic tuberculosis (Mycobacterium tuberculosis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 22-year-old Nepali male with primary isolated splenic tuberculosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1831:1920]` | Test: `Leishmaniasis serology` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serologic tests for malaria, leptospirosis, brucellosis, and leishmaniasis were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 22-year-old male from Nepal presented with fever, left lower chest pain, and multiple splenic abscesses confirmed by ultrasound-guided aspiration PCR to be Mycobacterium tuberculosis. Serologic testing for leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 42: `PMC3168563_01::Leishmaniasis` (`PMC3168563_01`)

- **Article Title:** Digestive malacoplakia in children: case report
- **Demographics (Metadata):** Age `9.0`, Gender `Female`, Year `2011`, Journal `ISRN Gastroenterol`
- **Primary Established Diagnosis of Case:** Intestinal malacoplakia
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_TARGET_CASE`** (Prompt Decision Enum: `EXCLUDED_NON_TARGET_CASE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 9-year-old girl hospitalized for digestive malacoplakia; had resolved cutaneous leishmaniasis at 3 years of age.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `HISTORICAL_RESOLVED`
6. **Step 7 — Temporality (`step7_temporality`):** `HISTORICAL_RESOLVED`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `PAST_HISTORY`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[101:223]` | Test: `Past medical history` | Target: `Cutaneous leishmaniasis` | Specimen: `skin` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E4_CONTEXT`)
     > "She presented cutaneous leishmaniasis at 3-year-old, diffuse verruca vulgaris, recurrent skin, and respiratory infections."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_TARGET_CASE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 9-year-old girl presented with abdominal pain, chronic diarrhea, and rectal bleeding, and was diagnosed by colonic histopathology (Michaelis-Gutmann bodies) with intestinal malacoplakia. Cutaneous leishmaniasis is mentioned solely as a remote past history at age 3 (6 years prior), with no active disease or diagnostic workup for leishmaniasis during the current episode. Temporality HISTORICAL_RESOLVED, clinical role PAST_HISTORY -> EXCLUDED_NON_TARGET_CASE.

### Case 43: `PMC7821814_01::Leishmaniasis` (`PMC7821814_01`)

- **Article Title:** Treatment of auricular relapsing polychondritis in a Saudi child using only non-steroidal anti-inflammatory drugs: a case report
- **Demographics (Metadata):** Age `5.0`, Gender `Male`, Year `2020`, Journal `Pan Afr Med J`
- **Primary Established Diagnosis of Case:** Auricular relapsing polychondritis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 5-year-old Saudi boy with bilateral auricular relapsing polychondritis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1649:1937]` | Test: `Leishmania IgM antibody test` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Laboratory examinations revealed a white blood cell count of 8.95 x 109/L (normal), an erythrocyte sedimentation rate of 32 (slightly elevated), negative C-reactive protein, negative antinuclear antibody, negative leishmania antibody immunoglobulin M, and complement within normal ranges."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 5-year-old boy presented with bilateral ear redness, swelling, and ulceration diagnosed as auricular relapsing polychondritis responsive to ibuprofen. Leishmania IgM antibody testing was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 44: `PMC6261242_01::Leishmaniasis` (`PMC6261242_01`)

- **Article Title:** An Unusual Presentation of Lupus Vulgaris and the Practical Usefulness of Dermatoscopy
- **Demographics (Metadata):** Age `80.0`, Gender `Male`, Year `2018`, Journal `Case Rep Dermatol Med`
- **Primary Established Diagnosis of Case:** Lupus vulgaris (cutaneous Mycobacterium tuberculosis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 80-year-old Caucasian man with lupus vulgaris (cutaneous tuberculosis) on the extremities.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[877:1053]` | Test: `Clinical differential diagnosis` | Target: `Leishmaniasis` | Specimen: `skin` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The clinical differential diagnosis included psoriasis, lupus erythematosus, tinea incognita, mycosis fungoides as well as leprae, leishmaniasis, sarcoidosis, and tuberculosis."
   - **Evidence Item 2:** `case_text[1512:1786]` | Test: `Skin biopsy histopathology and M. tuberculosis PCR` | Target: `Mycobacterium tuberculosis (lupus vulgaris)` | Specimen: `skin biopsy` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Biopsy of a representative lesion was performed and the histological examination revealed the presence of tuberculoid granulomas accompanied by caseation necrosis. The tuberculin skin test was found positive. PCR for M. Tuberculosis DNA done on a tissue sample was positive."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** An 80-year-old man with chronic erythematosquamous plaques on the extremities had leishmaniasis considered in the clinical differential diagnosis. Skin biopsy showing caseating tuberculoid granulomas, positive tuberculin skin test, and positive tissue PCR for Mycobacterium tuberculosis confirmed lupus vulgaris and ruled out leishmaniasis -> NEGATIVE.

### Case 45: `PMC7607781_01::Leishmaniasis` (`PMC7607781_01`)

- **Article Title:** Pacemaker-Associated Post-cardiac Injury Syndrome Presenting with Tamponade and Recurrent Pleural Effusion
- **Demographics (Metadata):** Age `62.0`, Gender `Female`, Year `2020`, Journal `Clin Med Insights Case Rep`
- **Primary Established Diagnosis of Case:** Pacemaker-associated post-cardiac injury syndrome (PCIS)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 62-year-old woman with pacemaker-associated post-cardiac injury syndrome (PCIS).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3302:3575]` | Test: `Infectious evaluation for Leishmania sp.` | Target: `Leishmania sp.` | Specimen: `serum/blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Due to her travel history, she was evaluated for infectious causes, including a Lyme titer, Trypanosoma sp., Babesia sp., Leishmania sp., and Plasmodium sp. Anti-Ro/SSA and La/SSB antibodies, antinuclear antibody, rheumatoid factor, and acid-fast stains were also negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 62-year-old woman developed cardiac tamponade and recurrent pleural effusions 8 weeks after pacemaker placement in Central America. Infectious evaluation for Leishmania sp. was negative, and she was diagnosed with post-cardiac injury syndrome (PCIS). Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 46: `PMC4302184_01::Leishmaniasis` (`PMC4302184_01`)

- **Article Title:** Paraneoplastic limbic encephalitis in a male with squamous cell carcinoma of the lung
- **Demographics (Metadata):** Age `54.0`, Gender `Male`, Year `2015`, Journal `J Clin Neurol`
- **Primary Established Diagnosis of Case:** Paraneoplastic limbic encephalitis secondary to lung squamous cell carcinoma
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 54-year-old Caucasian male with paraneoplastic limbic encephalitis secondary to squamous cell carcinoma of the lung.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[555:761]` | Test: `Leishmaniasis serology` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "All blood test findings were within normal limits, and serology was negative for hepatitis B virus, hepatitis C virus, human immunodeficiency virus, leishmaniasis, histoplasmosis, syphilis, and borreliosis."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 54-year-old male presented with anterograde amnesia, apathy, and disorientation due to paraneoplastic limbic encephalitis associated with lung squamous cell carcinoma. Serology for leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 47: `PMC4372314_01::Leishmaniasis` (`PMC4372314_01`)

- **Article Title:** Mycobacterium marinum infection: a case report
- **Demographics (Metadata):** Age `51.0`, Gender `Male`, Year `2015`, Journal `J Venom Anim Toxins Incl Trop Dis`
- **Primary Established Diagnosis of Case:** Cutaneous Mycobacterium marinum infection (aquarium granuloma)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 51-year-old male aquarium hobbyist with Mycobacterium marinum infection on the fifth right finger.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1284:1530]` | Test: `Clinical differential diagnosis` | Target: `Leishmaniasis` | Specimen: `skin` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The injuries could also indicate cutaneous tuberculosis, sporotrichosis, chromoblastomycosis, leishmaniasis, verruca vulgaris, sarcoidosis, foreign body granuloma, tuberculoid leprosy, cat scratch disease, psoriasis or lichen planus hypertrophic."
   - **Evidence Item 2:** `case_text[4637:4842]` | Test: `Lowenstein-Jensen culture and PRA-hsp65 PCR` | Target: `Mycobacterium marinum` | Specimen: `skin biopsy` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "In the present case, the mycobacterial culture in Lowenstein-Jensen medium was positive for M. marinum (Figure 3), and PCR-restriction enzyme analysis (PRA) of hsp65 was indicative of M. marinum infection."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 51-year-old male presented with a 5-year verrucous plaque on his right fifth finger. Leishmaniasis was included among the clinical differential diagnoses, but Lowenstein-Jensen culture and PRA-hsp65 PCR confirmed Mycobacterium marinum infection and ruled out leishmaniasis -> NEGATIVE.

### Case 48: `PMC5857332_01::Leishmaniasis` (`PMC5857332_01`)

- **Article Title:** Infective Endocarditis in a Young Adult due to Lactococcus lactis: A Case Report and Review of the Literature
- **Demographics (Metadata):** Age `35.0`, Gender `Male`, Year `2018`, Journal `Case Rep Med`
- **Primary Established Diagnosis of Case:** Lactococcus lactis infective endocarditis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 35-year-old male blacksmith with Lactococcus lactis infective endocarditis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1698:1902]` | Test: `Serum immunological investigation` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The serum immunological investigation for HIV, HAV, HBV, HCV, CMV, Toxoplasma, EBV, HSV, Coxsackie, RF, C3, C4, ANA, ANCA, Coxiella burnetii, Leishmania, Leptospira, and Brucella was found to be negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 35-year-old male with a bicuspid aortic valve vegetation and 3-week fever was diagnosed by blood cultures with Lactococcus lactis infective endocarditis. Serum immunological testing for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 49: `PMC4323713_01::Leishmaniasis` (`PMC4323713_01`)

- **Article Title:** Cutaneous tuberculosis with nonreactive PPD skin test: a diagnostic challenge
- **Demographics (Metadata):** Age `63.0`, Gender `Female`, Year `2015`, Journal `An Bras Dermatol`
- **Primary Established Diagnosis of Case:** Cutaneous tuberculosis (Mycobacterium tuberculosis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 63-year-old female with cutaneous tuberculosis on the right leg and nonreactive PPD.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[398:608]` | Test: `Serology for leishmaniasis` | Target: `Leishmaniasis` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The following tests were normal: blood cell count, VDRL, ANA, AFB in the lymph nodes, HIV, culture for bacteria and fungi (in biopsy material), serology for leishmaniasis, and radiography of the chest and legs."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 63-year-old woman presented with an ulcerated plaque on her right leg. Serology for leishmaniasis was normal/negative, and tissue culture plus IS6110 PCR confirmed cutaneous Mycobacterium tuberculosis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 50: `PMC5394404_01::Leishmaniasis` (`PMC5394404_01`)

- **Article Title:** Severe Murine Typhus Presenting with Acalculous Cholecystitis: A Case Report and Literature Review
- **Demographics (Metadata):** Age `54.0`, Gender `Male`, Year `2017`, Journal `Case Rep Med`
- **Primary Established Diagnosis of Case:** Severe murine typhus (Rickettsia typhi) with acute acalculous cholecystitis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 54-year-old Caucasian male from Kasos island with severe murine typhus (Rickettsia typhi) presenting with acalculous cholecystitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1857:2191]` | Test: `Zoonosis serology panel` | Target: `Leishmania spp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The patient was placed off the antibiotics that he was taking, blood and urine cultures were drawn, and serology was obtained for viral infections (HIV, hepatitis B and C viruses, CMV, and EBV) and zoonoses (Brucella spp., Rickettsia spp., Coxiella burnetii, Leishmania spp., and leptospirosis) because of his epidemiological history."
   - **Evidence Item 2:** `case_text[2644:2856]` | Test: `Serological workup results` | Target: `Leishmania spp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "On day 3, indirect immunofluorescence (IFA) obtained on admission revealed a high titer for R. typhi (IgM 1 : 800, IgG negative), while the remaining workup was negative, including serology for other rickettsiae."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 54-year-old male presented with prolonged fever and acute acalculous cholecystitis. Serology for Leishmania spp. was obtained as part of the zoonotic workup and returned negative, while Rickettsia typhi IFA confirmed murine typhus (IgM 1:800 rising to 1:51,200). Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 51: `PMC8143047_01::Leishmaniasis` (`PMC8143047_01`)

- **Article Title:** Case Report: Hemophagocytic Lymphohistiocytosis and Non-Tuberculous Mycobacteriosis Caused by a Novel GATA2 Variant
- **Demographics (Metadata):** Age `29.0`, Gender `Female`, Year `2021`, Journal `Front Immunol`
- **Primary Established Diagnosis of Case:** Disseminated Mycobacterium avium infection and HLH due to GATA2 deficiency
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 29-year-old female student with HLH and disseminated Mycobacterium avium infection caused by a novel heterozygous GATA2 variant.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1192:1366]` | Test: `Serology and PCR on peripheral blood and bone marrow` | Target: `Leishmania spp.` | Specimen: `peripheral blood and bone marrow` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "After ruling out Leishmania spp., HIV, EBV, and CMV infections by serology and PCR (peripheral blood and bone marrow, BM), biopsies of retroperitoneal lymph nodes were taken."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 29-year-old female presented with recurrent fever, hepatosplenomegaly, pancytopenia, and HLH secondary to disseminated Mycobacterium avium infection in the setting of GATA2 deficiency. Leishmania spp. infection was explicitly ruled out by serology and PCR on peripheral blood and bone marrow. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 52: `PMC3389709_01::Leishmaniasis` (`PMC3389709_01`)

- **Article Title:** Chronic q Fever with no elevation of inflammatory markers: a case report
- **Demographics (Metadata):** Age `55.0`, Gender `Male`, Year `2012`, Journal `Case Rep Med`
- **Primary Established Diagnosis of Case:** Chronic Q fever endocarditis and hepatitis (Coxiella burnetii)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 55-year-old male lawyer with biological prosthetic aortic valve and chronic Q fever (Coxiella burnetii) endocarditis and hepatitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3509:3609]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serologies for HIV, HBV, HCV, Schistosoma, Borrelia, Rickettsia, Leishmania, and VDRL were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 55-year-old male with a bioprosthetic aortic valve, night sweats, weight loss, and hepatosplenomegaly was diagnosed with chronic Q fever (Coxiella burnetii phase I IgG 1:204,800 and positive liver PCR). Serology for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 53: `PMC9152189_01::Leishmaniasis` (`PMC9152189_01`)

- **Article Title:** Lumbar swelling and migrating edema in 3- and 4-year-old boys
- **Demographics (Metadata):** Age `3.0`, Gender `Male`, Year `2022`, Journal `SAGE Open Med Case Rep`
- **Primary Established Diagnosis of Case:** Henoch-Schonlein purpura (IgA vasculitis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 3-year-old boy with Henoch-Schonlein purpura presenting with lumbar swelling and migrating edema.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1875:1991]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Viral serology for EBV, CMV, Parvovirus B19, Borrelia, Rickettsiae, Leishmania, and Toxoplasma gondii were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 3-year-old boy presented with ankle and paravertebral lumbar swelling and migrating livedo, and was diagnosed with Henoch-Schonlein purpura. Serology for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 54: `PMC7333364_01::Leishmaniasis` (`PMC7333364_01`)

- **Article Title:** Transient Decrease of Circulating and Tissular Dendritic Cells in Patients With Mycobacterial Disease and With Partial Dominant IFNγR1 Deficiency
- **Demographics (Metadata):** Age `5.0`, Gender `Female`, Year `2020`, Journal `Front Immunol`
- **Primary Established Diagnosis of Case:** Disseminated Mycobacterium avium infection with autosomal dominant partial IFNGR1 deficiency
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 2.5-year-old girl (P1; metadata age=5.0) with autosomal dominant partial IFNGR1 deficiency and disseminated Mycobacterium avium lymphadenitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1126:1337]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The infectious disease screening included blood cultures, Brucella, Rickettsia, Bartonella, Coxiella, Leishmania, Toxoplasma, Plasmodium, Herpesviruses, Epstein-Barr virus, and HIV serology, all tested negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 2.5-year-old girl with autosomal dominant partial IFNGR1 deficiency (818del4) presented with prolonged fever, splenomegaly, and disseminated Mycobacterium avium necrotizing granulomatous lymphadenitis. Serology for Leishmania tested negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 55: `PMC8514908_01::Leishmaniasis` (`PMC8514908_01`)

- **Article Title:** Lymphocutaneous Sporotrichosis Refractory to First-Line Treatment
- **Demographics (Metadata):** Age `61.0`, Gender `Female`, Year `2021`, Journal `Case Rep Dermatol Med`
- **Primary Established Diagnosis of Case:** Lymphocutaneous sporotrichosis (Sporothrix sp.)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 61-year-old Brazilian woman with lymphocutaneous sporotrichosis on the right upper limb.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1492:1681]` | Test: `Clinical differential diagnosis` | Target: `Leishmaniasis` | Specimen: `skin lesion` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "Skin fragments were collected to identify the etiologic agent of the lesions, as the morphology of the lesions suggested lymphocutaneous sporotrichosis, skin tuberculosis, or leishmaniasis."
   - **Evidence Item 2:** `case_text[2322:2516]` | Test: `Sabouraud agar fungal culture and microscopy` | Target: `Sporothrix sp.` | Specimen: `skin biopsy` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Microscopically septate hyaline hyphae present in the apex conidiophores and bouquet-like structures were observed, suggesting a fungus belonging to the genus Sporothrix (Figures 2(b) and 2(c))."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 61-year-old female in Sao Paulo presented with ulcerated and ascending nodular lesions on the right upper limb. Leishmaniasis was considered in the differential diagnosis based on lesion morphology, but Sabouraud culture and thermal dimorphism confirmed lymphocutaneous sporotrichosis (Sporothrix sp.), ruling out leishmaniasis -> NEGATIVE.

### Case 56: `PMC6881760_01::Leishmaniasis` (`PMC6881760_01`)

- **Article Title:** A Western Case of Intravascular Large B-Cell Lymphoma as Unusual Cause of Persistent Fever
- **Demographics (Metadata):** Age `58.0`, Gender `Female`, Year `2019`, Journal `Case Rep Hematol`
- **Primary Established Diagnosis of Case:** Intravascular large B-cell lymphoma (IVLBCL)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 58-year-old Caucasian woman with fever of unknown origin diagnosed at autopsy with intravascular large B-cell lymphoma (IVLBCL).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1018:1455]` | Test: `Leishmania donovani IgM serology` | Target: `Leishmania donovani` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Acute infectious diseases (hepatitis A, hepatitis B, hepatitis C, and hepatitis E virus, human immunodeficiency virus, cytomegalovirus, parvovirus B19, Epstein-Barr virus, echoviruses, poliovirus, coxsackieviruses, Treponema pallidum, Coxiella burnetii, Toxoplasma, Salmonella typhi, Legionella pneumophila, Mycoplasma pneumoniae, Leishmania donovani, Chlamydya, Brucella, Leptospira, Rickettsia, and Borrelia species IgM) were negative."
   - **Evidence Item 2:** `case_text[3513:3696]` | Test: `Bone marrow trephine biopsy` | Target: `Leishmania` | Specimen: `bone marrow` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Bone marrow trephine biopsy was hypocellular with a mild increase in granulopoietic and erythropoietic precursors and reactive plasmacytosis, and no evidence of leishmanial infection."
   - **Evidence Item 3:** `case_text[4425:4563]` | Test: `Empirical AmBisome trial` | Target: `Leishmania` | Specimen: `None` | Result: `NEGATIVE` | Relation: `REFUTES` (`E3_SUPPORTIVE`)
     > "An empirical treatment with doxycyclin and AmBisome was commenced on suspicion of chlamydial or leishmania infection, without improvement."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `True` — Empirical treatment with AmBisome was briefly tried on clinical suspicion of leishmania infection without improvement, while Leishmania donovani IgM and bone marrow trephine biopsy were negative and autopsy confirmed intravascular large B-cell lymphoma.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 58-year-old woman admitted for fever of unknown origin tested negative for Leishmania donovani IgM and showed no evidence of leishmanial infection on bone marrow trephine biopsy. An empirical trial of AmBisome yielded no improvement, and autopsy confirmed intravascular large B-cell lymphoma (IVLBCL). Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 57: `PMC5771918_01::Leishmaniasis` (`PMC5771918_01`)

- **Article Title:** Unexpected disseminated histoplasmosis detected by bone marrow biopsy in a solid organ transplant patient
- **Demographics (Metadata):** Age `29.0`, Gender `Male`, Year `2017`, Journal `Clin Case Rep`
- **Primary Established Diagnosis of Case:** Disseminated histoplasmosis (Histoplasma capsulatum)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 29-year-old male renal transplant recipient with disseminated histoplasmosis detected on bone marrow biopsy.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2005:2247]` | Test: `Bone marrow aspirate smear morphology differential` | Target: `Leishmania species` | Specimen: `bone marrow` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "A single histiocyte with oval-shaped organisms was seen on the aspirate smear (Fig. 1A). The morphological differential diagnosis included Histoplasma capsulatum, Leishmania species, Candida glabrata, Blastomyces dermatitidis, among others 1."
   - **Evidence Item 2:** `case_text[2248:2710]` | Test: `GMS stain, urine Histoplasma antigen, and fungal blood culture` | Target: `Histoplasma capsulatum` | Specimen: `bone marrow, urine, blood` | Result: `POSITIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Grocott-methenamine silver stain performed on the bone marrow core demonstrated additional histiocytes containing multiple yeast forms exhibiting narrow-based budding (Fig. 1B). Rare hemophagocytes were noted (Fig. 1C). Based on these findings, intravenous liposomal amphotericin was started. Subsequent urine Histoplasma antigen test results (above the limit of quantification) and fungal blood culture results returned, confirming a diagnosis of H. capsulatum."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 29-year-old male kidney transplant recipient presented with fever and hyperferritinemia. Bone marrow aspirate showed a histiocyte with oval organisms whose morphological differential included Histoplasma capsulatum and Leishmania species; Grocott-methenamine silver staining (narrow-based budding yeasts), urine Histoplasma antigen, and fungal blood cultures confirmed Histoplasma capsulatum and ruled out Leishmania -> NEGATIVE.

### Case 58: `PMC9366043_01::Leishmaniasis` (`PMC9366043_01`)

- **Article Title:** Case report: Effectiveness of sirolimus in a de novo FAS mutation leading to autoimmune lymphoproliferative syndrome-FAS and elevated DNT/Treg ratio
- **Demographics (Metadata):** Age `2.0`, Gender `Male`, Year `2022`, Journal `Front Pediatr`
- **Primary Established Diagnosis of Case:** Autoimmune lymphoproliferative syndrome (ALPS-FAS)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 2-year-old boy with autoimmune lymphoproliferative syndrome (ALPS-FAS) due to a de novo germline FAS mutation.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[934:1070]` | Test: `Leishmania donovani infection marker analysis` | Target: `Leishmania donovani` | Specimen: `serum/blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "In addition, the analysis of markers for measles virus, parvovirus B19, schistosomiasis, and Leishmania donovani infection was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 2-year-old boy with massive splenomegaly, lymphadenopathy, and multilineage autoimmune cytopenias was diagnosed with ALPS-FAS (de novo FAS c.857G>A, p.G286E mutation). Testing for Leishmania donovani infection was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 59: `PMC6203242_01::Leishmaniasis` (`PMC6203242_01`)

- **Article Title:** Splenic epithelial cyst mistaken with Hydatid cyst: A case report
- **Demographics (Metadata):** Age `17.0`, Gender `Female`, Year `2018`, Journal `Int J Surg Case Rep`
- **Primary Established Diagnosis of Case:** Splenic epithelial cyst
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 17-year-old female with a primary splenic epithelial cyst initially mistaken for a splenic hydatid cyst.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1423:1622]` | Test: `Leishmania braziliensis and L. donovani serology` | Target: `Leishmania braziliensis and Leishmania donovani` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serologic test for Hepatitis B virus (HBV), hepatitis C virus (HCV), Cytomegalovirus (CMV), HIV, Toxoplasmosis, Entamoeba histolytica, Leishmania brazilensis, donovani, and EBV IgM were all negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 17-year-old girl presented with left upper quadrant pain and a 15-cm splenic cyst confirmed histologically after partial resection as a splenic epithelial cyst. Serologic tests for Leishmania braziliensis and L. donovani were explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 60: `PMC5312191_01::Leishmaniasis` (`PMC5312191_01`)

- **Article Title:** Exuberant pyoderma gangrenosum in a patient with autoimmune hepatitis
- **Demographics (Metadata):** Age `25.0`, Gender `Female`, Year `2017`, Journal `An Bras Dermatol`
- **Primary Established Diagnosis of Case:** Pyoderma gangrenosum associated with type 1 autoimmune hepatitis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 25-year-old female with type 1 autoimmune hepatitis and exuberant lower-limb pyoderma gangrenosum.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1344:1410]` | Test: `Leishmaniasis PCR and leishmanin skin test` | Target: `Leishmania` | Specimen: `skin biopsy / intradermal test` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "PCR for leishmaniasis and leishmanin skin test were also negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 25-year-old woman with type 1 autoimmune hepatitis presented with seven deep lower-extremity ulcers diagnosed as pyoderma gangrenosum. Both PCR for leishmaniasis and the leishmanin skin test were explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 61: `PMC10026180_04::Leishmaniasis` (`PMC10026180_04`)

- **Article Title:** A horse or a zebra? Unusual manifestations of common cutaneous infections in primary immunodeficiency pediatric patients
- **Demographics (Metadata):** Age `11.0`, Gender `Female`, Year `2023`, Journal `Front Pediatr`
- **Primary Established Diagnosis of Case:** Cutaneous fungal infection and Staphylococcus aureus impetigo in ataxia telangiectasia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 11-year-old Arab girl with ataxia telangiectasia (Case 4 of an 8-patient pediatric PID series) who developed facial fungal and Staphylococcus aureus impetigo lesions.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1230:1320]` | Test: `Leishmania PCR test` | Target: `Leishmania` | Specimen: `skin lesion` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "An atypical infection was suspected. The result of a PCR test for Leishmania was negative."
   - **Evidence Item 2:** `case_text[2512:2673]` | Test: `Differential diagnosis assessment` | Target: `Leishmaniasis` | Specimen: `skin lesion` | Result: `NEGATIVE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "Due to residence in an endemic region, leishmaniasis was initially high on the differential, but eventually, clinical suspicion and fungal cultures were of help."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** An 11-year-old girl with ataxia telangiectasia developed an erythematous eroded plaque on her nose and nostrils. Because she resided in an endemic area, cutaneous leishmaniasis was high on the differential diagnosis, but a PCR test for Leishmania was explicitly negative, and mycological/bacterial cultures identified fungal hyphae, Candida, and Staphylococcus aureus. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 62: `PMC10013466_01::Leishmaniasis` (`PMC10013466_01`)

- **Article Title:** Trypanosoma cruzi DTU II coinfection with bacteria producing prolonged cutaneous lesion in a healthy young male
- **Demographics (Metadata):** Age `27.0`, Gender `Male`, Year `2023`, Journal `Rev Inst Med Trop Sao Paulo`
- **Primary Established Diagnosis of Case:** Cutaneous Chagas disease (Trypanosoma cruzi DTU II) coinfected with Bacillus velezensis and Corynebacterium sp.
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 27-year-old Mexican male with a prolonged mandibular cutaneous lesion caused by Trypanosoma cruzi DTU II coinfection with Bacillus velezensis and Corynebacterium sp.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2424:2894]` | Test: `Parasitic serological assays` | Target: `Leishmania sp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Consequently, serological diagnoses were requested to confirm the diagnosis of Chagas disease or Leishmania sp. The initial tests, executed in 3 independent laboratories (blood bank laboratory [chemiluminescence architect Chagas kit (Abbott)], a research laboratory specialized in parasitic infections in our institution [ELISA home with the Ninoa strain as antigen]  , as well as an external private laboratory [chemiluminescence technique]), were reported as negative."
   - **Evidence Item 2:** `case_text[2895:3066]` | Test: `Genus- and species-specific Leishmania PCR` | Target: `Leishmania sp.` | Specimen: `skin biopsy and blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "PCR analysis was done to identify Leishmania sp. and specific Leishmania species with DNA isolated from the tissue biopsies and blood; these tests showed negative results."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 27-year-old Mexican man presented with a 5-month fistulous cutaneous lesion on the right mandible showing intracellular amastigotes and trypomastigotes on biopsy. PCR analysis for Leishmania sp. and specific Leishmania species on DNA from tissue biopsies and blood was explicitly negative, whereas satellite DNA PCR and sequencing confirmed Trypanosoma cruzi DTU II. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 63: `PMC5726683_01::Leishmaniasis` (`PMC5726683_01`)

- **Article Title:** Folliculotropic mycosis fungoides: challenging clinical, histopathological and immunohistochemical diagnosis
- **Demographics (Metadata):** Age `63.0`, Gender `Male`, Year `2017`, Journal `An Bras Dermatol`
- **Primary Established Diagnosis of Case:** Folliculotropic mycosis fungoides (cutaneous T-cell lymphoma)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 63-year-old male with folliculotropic mycosis fungoides presenting with a deforming nasal tumor and plaques.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1007:1147]` | Test: `Clinical differential diagnosis` | Target: `Leishmaniasis` | Specimen: `skin/nasal lesion` | Result: `INCONCLUSIVE` | Relation: `INCONCLUSIVE` (`E4_CONTEXT`)
     > "The suspicion was of paracoccidioidomycosis, leishmaniasis, syphilis, leprosy, sarcoidosis, mycosis fungoides, and lethal midline granuloma."
   - **Evidence Item 2:** `case_text[1148:1327]` | Test: `Microscopy and Montenegro's skin test` | Target: `Leishmania` | Specimen: `skin/blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Blood samples were collected, and microscopy, Montenegro's test, tuberculin test, bacilloscopy, serology for hepatitis, HIV and syphilis were all performed, and all were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 63-year-old male presented with infiltrated plaques and an ulcerated nasal tumor. Leishmaniasis was suspected in the differential diagnosis, but microscopy and Montenegro's (leishmanin) skin test were explicitly negative, and histopathology/immunohistochemistry confirmed folliculotropic mycosis fungoides. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 64: `PMC3469179_01::Leishmaniasis` (`PMC3469179_01`)

- **Article Title:** Fatal Case of Plasmodium vivax Malaria in a Splenectomized Patient
- **Demographics (Metadata):** Age `40.0`, Gender `Male`, Year `2012`, Journal `Iran J Parasitol`
- **Primary Established Diagnosis of Case:** Fatal Plasmodium vivax malaria in a splenectomized patient
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 40-year-old splenectomized Iranian man with fatal Plasmodium vivax malaria.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[961:1118]` | Test: `Direct agglutination test (DAT)` | Target: `Visceral leishmaniasis (kala-azar)` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "In addition, direct agglutination test (DAT) for detection of visceral leishmaniasis (kala-azar), blood and urine culture for bacterial growth were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 40-year-old splenectomized man in Iran presented with fever, anemia, jaundice, and thrombocytopenia, and was diagnosed by blood smear and semi-nested multiplex PCR with fatal Plasmodium vivax malaria. Direct agglutination test (DAT) for visceral leishmaniasis (kala-azar) was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 65: `PMC9516294_01::Leishmaniasis` (`PMC9516294_01`)

- **Article Title:** Case report: Atypical and chronic masticatory muscle myositis in a 5-month old Cavalier King Charles Spaniel. Clinical and diagnostic findings, treatment and successful outcome
- **Demographics (Metadata):** Age `0.0`, Gender `Male`, Year `2022`, Journal `Front Vet Sci`
- **Primary Established Diagnosis of Case:** Canine juvenile masticatory muscle myositis
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 5-month-old male Cavalier King Charles Spaniel dog (age=0.0 in metadata) with juvenile masticatory muscle myositis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[940:1318]` | Test: `Canine infectious disease serology panel` | Target: `Leishmania infantum` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Blood analysis, serology for infectious diseases (Dirofilaria immitis, Ehrlichia canis, Leishmania infantum, Borrelia spp., Anaplasma phagocytophilum, Babesia canis, Hepatozoon canis, Toxoplasma gondii, and Neospora caninum), fine needle aspiration of lymph nodes, 2M antibodies assay ELISA, CT and MRI of the head and biopsies of temporalis and masseter muscles were performed."
   - **Evidence Item 2:** `case_text[3213:3424]` | Test: `Canine infectious disease serology result` | Target: `Leishmania infantum` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serology for infectious diseases was negative with exception of mild positivity for B. canis (15.8 U, reference range < 14 U); serology for B. canis was repeated two weeks later and ruled out an acute infection."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case report of a 5-month-old male Cavalier King Charles Spaniel dog diagnosed with atypical chronic masticatory muscle myositis, in which serology for Leishmania infantum was negative. Excluded from the human benchmark because ccu_type is ANIMAL_CASE -> EXCLUDED_NON_HUMAN.

### Case 66: `PMC5917533_01::Leishmaniasis` (`PMC5917533_01`)

- **Article Title:** Granuloma of the labial minor salivary glands in tuberculosis
- **Demographics (Metadata):** Age `46.0`, Gender `Male`, Year `2018`, Journal `J Oral Maxillofac Pathol`
- **Primary Established Diagnosis of Case:** Disseminated tuberculosis (Mycobacterium tuberculosis) with labial minor salivary gland granulomas
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 46-year-old man with disseminated tuberculosis involving labial minor salivary glands, skin, mediastinum, and liver.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[299:413]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serologies were negative for C-hepatits, HIV, Epstein-Barr, Parvo, HHV8 viruses and for bilharzias and leishmania."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 46-year-old man presented with weight loss, compressive mediastinal lymphadenopathy, and multiorgan granulomas confirmed by QuantiFERON and mediastinal lymph node culture to be Mycobacterium tuberculosis. Serology for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 67: `PMC8784545_01::Leishmaniasis` (`PMC8784545_01`)

- **Article Title:** Case Report: High Doses of Intravenous Immunoglobulins as a Successful Treatment for Late Onset Immune Agranulocytosis After Rituximab Plus Bendamustine
- **Demographics (Metadata):** Age `69.0`, Gender `Male`, Year `2022`, Journal `Front Immunol`
- **Primary Established Diagnosis of Case:** Late-onset immune agranulocytosis following rituximab plus bendamustine in Waldenstrom's macroglobulinemia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 69-year-old male with Waldenstrom's macroglobulinemia and late-onset immune agranulocytosis after rituximab plus bendamustine.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1841:2031]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serologies for human immunodeficiency virus, hepatitis B virus, hepatitis C virus, Epstein-Barr virus, leishmania, cryptococcus, treponema pallidum, and parvovirus showed no acute infection."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 69-year-old male with Waldenstrom's macroglobulinemia presented with febrile neutropenia and immune agranulocytosis following rituximab plus bendamustine. Serology for Leishmania showed no acute infection. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 68: `PMC5362848_01::Leishmaniasis` (`PMC5362848_01`)

- **Article Title:** Successful treatment of feline leishmaniosis using a combination of allopurinol and N-methyl-glucamine antimoniate
- **Demographics (Metadata):** Age `2.0`, Gender `Male`, Year `2016`, Journal `JFMS Open Rep`
- **Primary Established Diagnosis of Case:** Feline leishmaniosis (Leishmania infantum)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 2-year-old neutered male domestic European cat with feline leishmaniosis (Leishmania infantum).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `AFFIRMED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `PRIMARY_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E1_DISEASE_SPECIFIC_CONFIRMATORY`
   - **Evidence Item 1:** `case_text[2467:2612]` | Test: `IFAT anti-Leishmania antibody test` | Target: `Leishmania` | Specimen: `serum` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E2_HIGHLY_SPECIFIC`)
     > "The cat tested negatively for FIV antibodies and FeLV antigens, but was positive for anti-Leishmania antibodies, with a titre >=1:1280 (Table 1)."
   - **Evidence Item 2:** `case_text[2862:3014]` | Test: `Fine-needle aspirate Giemsa smear` | Target: `Leishmania amastigotes` | Specimen: `ear skin nodule` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E1_CONFIRMATORY`)
     > "The smears revealed Leishmania amastigotes (Figure 3), and absence of bacteria/neutrophilic infiltration or characteristic cells of autoimmune diseases."
   - **Evidence Item 3:** `case_text[3486:3693]` | Test: `TaqMan kDNA qPCR` | Target: `Leishmania infantum` | Specimen: `skin nodules and blood` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E1_CONFIRMATORY`)
     > "RT-qPCR was negative for coronavirus, while qPCR of skin nodules and blood samples were positive for L infantum kDNA, showing a parasitic load of 1700 and 0.1 parasites per 50 ng DNA, respectively (Table 2)."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT']`
12. **Clinical Rationale:** Veterinary case report of a 2-year-old domestic cat with confirmed feline leishmaniosis (Leishmania infantum confirmed by IFAT >=1:1280, Giemsa cytology showing amastigotes, promastigote culture, and kDNA qPCR) treated with allopurinol and N-methyl-glucamine antimoniate. Although leishmaniosis is confirmed in the animal, ccu_type is ANIMAL_CASE (feline patient); per Step 2 and Step 12, non-human cases are strictly excluded -> EXCLUDED_NON_HUMAN.

### Case 69: `PMC6792362_01::Leishmaniasis` (`PMC6792362_01`)

- **Article Title:** An autochthonous case of paracoccidioidomycosis in a new area of Ceara State, Northeastern Brazil
- **Demographics (Metadata):** Age `65.0`, Gender `Male`, Year `2019`, Journal `Rev Inst Med Trop Sao Paulo`
- **Primary Established Diagnosis of Case:** Autochthonous chronic paracoccidioidomycosis (Paracoccidioides brasiliensis)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 65-year-old male farmer in Ceara State, Brazil, with autochthonous paracoccidioidomycosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1858:2110]` | Test: `Giemsa-stained palatal lesion imprint` | Target: `Leishmania` | Specimen: `hard palate mucosal lesion` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "An imprint of the palatal lesion showed a moderate presence of intra- and extracellular yeast structures with considerably variable sizes (small and oval, medium, large and rounded) by Giemsa staining; Leishmania was not found in the analyzed material."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 65-year-old male farmer in Ceara, Brazil, presented with a 3-year infiltrative palatal lesion, nasal ulceration, and pulmonary nodules. Giemsa imprint of the palatal lesion showed yeast structures and explicitly no Leishmania, while biopsy, culture, ITS PCR/sequencing, and double radial immunodiffusion confirmed Paracoccidioides brasiliensis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 70: `PMC5918120_01::Leishmaniasis` (`PMC5918120_01`)

- **Article Title:** Indolent, T-cell, large granular lymphocytic leukaemia in a dog presenting with severe neutropenia and an absence of lymphocytosis
- **Demographics (Metadata):** Age `6.0`, Gender `Male`, Year `2018`, Journal `Open Vet J`
- **Primary Established Diagnosis of Case:** Canine T-cell large granular lymphocytic leukaemia (LGLL)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 6-year-old entire male Golden Retriever dog with T-cell large granular lymphocytic leukaemia (LGLL).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2869:2959]` | Test: `EDTA blood PCR` | Target: `Leishmania` | Specimen: `EDTA blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "PCR on EDTA blood for Leishmania, Babesia, Borrelia, Ehrlichia and Anaplasma was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case report of a 6-year-old male Golden Retriever dog in the UK diagnosed with indolent T-cell large granular lymphocytic leukaemia (LGLL) and secondary immune-mediated neutropenia, in which EDTA blood PCR for Leishmania was negative. Excluded because ccu_type is ANIMAL_CASE -> EXCLUDED_NON_HUMAN.

### Case 71: `PMC6607709_01::Leishmaniasis` (`PMC6607709_01`)

- **Article Title:** Deep Venous Thrombosis in Patients with Erythema Nodosum Leprosum in the Use of Thalidomide and Systemic Corticosteroid in Reference Service in Belo Horizonte, Minas Gerais
- **Demographics (Metadata):** Age `None`, Gender `Male`, Year `2019`, Journal `Case Rep Dermatol Med`
- **Primary Established Diagnosis of Case:** Erythema nodosum leprosum complicated by deep venous thrombosis (16-patient series)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_SINGLE_PATIENT`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_SERIES`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `AGGREGATE_STUDY_UNIT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `NONE` — Aggregate case series of 16 patients with erythema nodosum leprosum (ENL) who developed deep venous thrombosis (DVT) on thalidomide and corticosteroids.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `AFFIRMED`
6. **Step 7 — Temporality (`step7_temporality`):** `UNKNOWN`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[683:864]` | Test: `Aggregate cohort comorbidity summary` | Target: `Cutaneous leishmaniasis` | Specimen: `None` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E4_CONTEXT`)
     > "Three patients had HIV-AIDS, one had cutaneous leishmaniasis, one had hypertension and dyslipidemia, one had diabetes, and one had diabetes, asthma, alcoholism, and a mood disorder."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_SINGLE_PATIENT` | Failure Flags: `['F2_SCOPE_COHORT']`
12. **Clinical Rationale:** This text presents aggregate statistics for a 16-patient case series of deep venous thrombosis in erythema nodosum leprosum (8 institutional cases and 8 literature cases, age range 33-75 years, mean 48.3 years), noting in aggregate that one of the 16 patients had cutaneous leishmaniasis. Because the unit of analysis is an aggregate multi-patient series (AGGREGATE_STUDY_UNIT) rather than a single human patient, it is excluded -> EXCLUDED_NON_SINGLE_PATIENT.

### Case 72: `PMC9248758_02::Leishmaniasis` (`PMC9248758_02`)

- **Article Title:** Rhino-Orbital-Cerebral Mycosis and Extranodal Natural Killer or/and T-Cell Lymphoma, Nasal Type
- **Demographics (Metadata):** Age `35.0`, Gender `Male`, Year `2022`, Journal `Front Med (Lausanne)`
- **Primary Established Diagnosis of Case:** Rhino-orbital-cerebral mycosis (Rhizopus arrhizus) and ENKTL-NT (review article)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_TARGET_CASE`** (Prompt Decision Enum: `EXCLUDED_NON_TARGET_CASE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `SYSTEMATIC_REVIEW`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `MULTI_PATIENT_CASE_SERIES`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Review article of 149 papers on rhino-orbital-cerebral mycosis (ROCM) and ENKTL-NT that briefly recaps a 35-year-old Chinese male with Rhizopus arrhizus; Leishmania is mentioned only as a literature example from other studies.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `CONTEXT_ONLY`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `UNCERTAIN`
6. **Step 7 — Temporality (`step7_temporality`):** `UNKNOWN`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[6908:7183]` | Test: `Literature review citation` | Target: `Leishmania infantum` | Specimen: `None` | Result: `NOT_APPLICABLE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "We retrieved, from the peers, a series of reports about the proliferation of cytotoxic T lymphocytes induced by Staphyloccus aureus, Nocardia farcinica, Mycobacterium fortuitum, M. marinum, and Leishmania infantum, all of which were reported to induce ENKTL-NT-like syndrome."
   - **Evidence Item 2:** `case_text[8904:9146]` | Test: `Literature review citation` | Target: `Leishmania spp.` | Specimen: `None` | Result: `NOT_APPLICABLE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "Other researchers have reported that in some ENKTL-NT patients, these immunopathological markers were induced by microbes like Staphyloccus aureus, Nocardia sp., Mycobacterium fortuitum, M marinum, Pseudomonas aeruginosa, and Leishmania spp.."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_TARGET_CASE` | Failure Flags: `['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
12. **Clinical Rationale:** This article is a systematic review of 149 publications on ROCM and ENKTL-NT that opens with a brief recap of a 35-year-old Chinese male with Rhizopus arrhizus infection. Mentions of Leishmania infantum and Leishmania spp. occur exclusively in the general literature discussion citing other researchers' reports of microbes inducing ENKTL-NT-like proliferation, with no relevance to the 35-year-old patient -> EXCLUDED_NON_TARGET_CASE.

### Case 73: `PMC8014250_01::Leishmaniasis` (`PMC8014250_01`)

- **Article Title:** Clinical Misdiagnosis of COVID-19 Infection with Confusing Clinical Course
- **Demographics (Metadata):** Age `0.0`, Gender `Male`, Year `2021`, Journal `Case Rep Infect Dis`
- **Primary Established Diagnosis of Case:** Visceral leishmaniasis with secondary hemophagocytic lymphohistiocytosis and concurrent COVID-19
- **Final Dataset Label (`step12_dataset_label`):** **`POSITIVE`** (Prompt Decision Enum: `POSITIVE` | VPD Satisfied: `True` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 29-month-old boy (age=0.0 in metadata) with COVID-19 and hemophagocytic lymphohistiocytosis secondary to visceral leishmaniasis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `AFFIRMED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `PRIMARY_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E1_DISEASE_SPECIFIC_CONFIRMATORY`
   - **Evidence Item 1:** `case_text[1763:1953]` | Test: `Bone marrow aspirate microscopy` | Target: `Leishmania donovani (Leishman-Donovan bodies)` | Specimen: `bone marrow` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E1_CONFIRMATORY`)
     > "Subsequently, Leishman Donovan bodies and hemophagocytic cells were seen in bone marrow aspiration (Figure 3), and treatment was started with amphotericin, which led to clinical improvement."
   - **Evidence Item 2:** `case_text[1954:2091]` | Test: `Final clinical diagnosis` | Target: `Visceral leishmaniasis` | Specimen: `bone marrow` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E1_CONFIRMATORY`)
     > "Then, the suggested diagnosis was hemophagocytic lymphohistiocytosis secondary to visceral leishmaniasis, and prednisolone was initiated."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `True` — An initial bone marrow aspiration was reported as normal, but a subsequent bone marrow aspiration demonstrated Leishman-Donovan bodies and hemophagocytic cells, confirming visceral leishmaniasis.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `True`
11. **Step 12 — Final Label & Failure Flags:** `POSITIVE` | Failure Flags: `[]`
12. **Clinical Rationale:** A 29-month-old boy presented with a 2-month history of fever, splenomegaly (130 mm), pancytopenia, hyperferritinemia, hypertriglyceridemia, hypofibrinogenemia, and a positive SARS-CoV-2 PCR. Repeat bone marrow aspiration directly demonstrated intracellular Leishman-Donovan bodies and hemophagocytic cells (Figure 3; E1 confirmatory evidence), and treatment with amphotericin led to clinical improvement, establishing hemophagocytic lymphohistiocytosis secondary to visceral leishmaniasis. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. All VPD criteria are satisfied -> POSITIVE.

### Case 74: `PMC6560963_01::Leishmaniasis` (`PMC6560963_01`)

- **Article Title:** Haemophagocytic lymphohistiocytosis in patients with human immunodeficiency virus infection: to treat or not to treat
- **Demographics (Metadata):** Age `38.0`, Gender `Female`, Year `2019`, Journal `Pan Afr Med J`
- **Primary Established Diagnosis of Case:** HIV-associated hemophagocytic lymphohistiocytosis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 38-year-old HIV-positive female (Case 1 of 2) with hemophagocytic lymphohistiocytosis attributed to uncontrolled HIV replication.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2243:2357]` | Test: `rK39 antibody test` | Target: `Visceral leishmaniasis` | Specimen: `serum/blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Also, pp65 antigen detection test in blood for CMV and rk39-antibody test for visceral leishmaniasis was negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 38-year-old HIV-infected woman presented with prolonged fever, hepatosplenomegaly, and pancytopenia, and was diagnosed with HLH. The rK39 antibody test for visceral leishmaniasis was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 75: `PMC3305386_01::Leishmaniasis` (`PMC3305386_01`)

- **Article Title:** Antiretroviral activity of 5-azacytidine during treatment of a HTLV-1 positive myelodysplastic syndrome with autoimmune manifestations
- **Demographics (Metadata):** Age `58.0`, Gender `Male`, Year `2012`, Journal `Virol J`
- **Primary Established Diagnosis of Case:** HTLV-1-positive myelodysplastic syndrome (RAEB-1) with autoimmune vasculitis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 58-year-old man with HTLV-1-positive myelodysplastic syndrome (RAEB-1) and leukocytoclastic vasculitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[910:1069]` | Test: `Leishmania antibody testing` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The evaluation included antibody testing for viral infections (HBV, HCV, HIV, HTLV, herpesviruses), Leishmania, Brucella, syphilis, Ricketsiae, and Toxoplasma."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 58-year-old man with night sweats, weight loss, cytopenias, and leukocytoclastic vasculitis underwent infectious antibody testing including Leishmania (negative/unremarkable) and was diagnosed with HTLV-1-positive myelodysplastic syndrome (RAEB-1) confirmed by bone marrow biopsy and HTLV-1 PCR. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 76: `PMC9792245_01::Leishmaniasis` (`PMC9792245_01`)

- **Article Title:** A Case Report of Purtscher-Like Retinopathy Secondary to Pneumocystis jirovecii Pneumonia in an Immunocompromised Patient
- **Demographics (Metadata):** Age `30.0`, Gender `Male`, Year `2022`, Journal `Case Rep Ophthalmol Med`
- **Primary Established Diagnosis of Case:** Purtscher-like retinopathy secondary to Pneumocystis jirovecii pneumonia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 30-year-old Caucasian male live-donor kidney transplant recipient with Purtscher-like retinopathy secondary to Pneumocystis jirovecii pneumonia.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2779:2871]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serological tests for toxoplasma and leishmania and the autoimmune screen were all negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 30-year-old male renal transplant recipient presented with exertional dyspnea and bilateral visual loss, and was diagnosed with Purtscher-like retinopathy secondary to Pneumocystis jirovecii pneumonia (BAL PCR positive). Serological testing for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 77: `PMC6885199_01::Leishmaniasis` (`PMC6885199_01`)

- **Article Title:** An Italian Case of Disseminated Histoplasmosis Associated with HIV
- **Demographics (Metadata):** Age `33.0`, Gender `Female`, Year `2019`, Journal `Case Rep Infect Dis`
- **Primary Established Diagnosis of Case:** Progressive disseminated histoplasmosis (Histoplasma capsulatum) in HIV/AIDS
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 33-year-old Cuban woman in Italy with newly diagnosed HIV/AIDS and progressive disseminated histoplasmosis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2001:2166]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Routine blood and urine cultures, serology for syphilis, toxoplasma, and Leishmania, latex for Cryptococcus neoformans, and smear test for malaria resulted negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 33-year-old Cuban woman with newly diagnosed HIV/AIDS (CD4 2 cells/uL) presented with high fever, skin lesions, hepatosplenomegaly, and pancytopenia. Serology for Leishmania was explicitly negative, and bone marrow/blood cultures confirmed disseminated Histoplasma capsulatum. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 78: `PMC4138934_01::Leishmaniasis` (`PMC4138934_01`)

- **Article Title:** Tuberculosis of the adrenal gland: a case report and review of the literature of infections of the adrenal gland
- **Demographics (Metadata):** Age `46.0`, Gender `Male`, Year `2014`, Journal `Int J Endocrinol`
- **Primary Established Diagnosis of Case:** Adrenal tuberculosis (Mycobacterium tuberculosis) causing primary adrenal insufficiency
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_TARGET_CASE`** (Prompt Decision Enum: `EXCLUDED_NON_TARGET_CASE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 46-year-old Filipino male in the US with primary adrenal insufficiency due to extrapulmonary tuberculosis; visceral leishmaniasis is mentioned solely in the accompanying literature review section.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `CONTEXT_ONLY`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `UNCERTAIN`
6. **Step 7 — Temporality (`step7_temporality`):** `UNKNOWN`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[16934:17000]` | Test: `Literature review discussion` | Target: `Visceral leishmaniasis` | Specimen: `None` | Result: `NOT_APPLICABLE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "Visceral leishmaniasis is another cause of cystic adrenal disease."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_TARGET_CASE` | Failure Flags: `['F5_DISCOURSE_CONTEXT']`
12. **Clinical Rationale:** A 46-year-old man was diagnosed with peritoneal and adrenal tuberculosis causing primary adrenal insufficiency (Addison's disease). Visceral leishmaniasis is mentioned only in a single sentence within the general literature review section on parasitic causes of adrenal disease, with no relevance to the patient -> EXCLUDED_NON_TARGET_CASE.

### Case 79: `PMC11415944_01::Leishmaniasis` (`PMC11415944_01`)

- **Article Title:** Cutaneous infection with Mycobacterium chelonae in a patient with multiple sclerosis
- **Demographics (Metadata):** Age `46.0`, Gender `Female`, Year `2024`, Journal `IDCases`
- **Primary Established Diagnosis of Case:** Cutaneous Mycobacterium chelonae infection
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 46-year-old Canadian woman with multiple sclerosis on teriflunomide who developed a right wrist cutaneous infection caused by Mycobacterium chelonae.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2026:2178]` | Test: `Leishmaniasis diagnostic test` | Target: `Leishmaniasis` | Specimen: `wrist skin lesion` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Her physician ordered a range of tests, including a Leishmaniasis test, smear, culture, and polymerase chain reaction (PCR) for mycobacterial diagnosis."
   - **Evidence Item 2:** `case_text[2615:2689]` | Test: `Clinical test results` | Target: `Leishmaniasis` | Specimen: `wrist skin lesion / blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Additionally, the results of her clinical tests were within normal ranges."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 46-year-old woman with multiple sclerosis developed a refractory granulomatous and cavitary lesion on her right wrist. A leishmaniasis test was ordered and clinical tests were normal/negative, while Lowenstein-Jensen culture and PCR (hsp65, rpoB, 16S rDNA) confirmed Mycobacterium chelonae. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 80: `PMC10612464_01::Leishmaniasis` (`PMC10612464_01`)

- **Article Title:** Brucella infection-induced hemophagocytic syndrome with subsequent development of the probable vanishing bile duct syndrome: A case report and literature review
- **Demographics (Metadata):** Age `37.0`, Gender `Male`, Year `2023`, Journal `SAGE Open Med Case Rep`
- **Primary Established Diagnosis of Case:** Brucellosis-induced hemophagocytic syndrome with probable vanishing bile duct syndrome
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 37-year-old Chinese male with Brucella infection-induced hemophagocytic syndrome and probable vanishing bile duct syndrome.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3460:3584]` | Test: `Kala-azar infectious workup` | Target: `Leishmania donovani (kala-azar)` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "To determine the etiology of HPS, Further testing for infectious indicators such as kala-azar and brucellosis was conducted."
   - **Evidence Item 2:** `case_text[7247:7396]` | Test: `Etiological investigation for HPS` | Target: `Leishmania donovani (kala-azar)` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Further investigations were conducted to determine the cause of HPS, including kala-azar, Brucella, ultimately leading to a diagnosis of brucellosis."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 37-year-old male presented with fever, jaundice, cytopenias, probable vanishing bile duct syndrome, and hemophagocytic syndrome (HPS). Testing for kala-azar (visceral leishmaniasis) and brucellosis was conducted to identify the trigger of HPS; kala-azar was excluded and Brucella IgG, tube agglutination (1:200++), and rose bengal tests confirmed brucellosis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 81: `PMC11286409_01::Leishmaniasis` (`PMC11286409_01`)

- **Article Title:** Chromoblastomycosis caused by Alternaria infectoria, concurrent with myiasis, in a recipient of a kidney transplant: a compelling case report
- **Demographics (Metadata):** Age `46.0`, Gender `Female`, Year `2024`, Journal `Front Med (Lausanne)`
- **Primary Established Diagnosis of Case:** Chromoblastomycosis (Alternaria infectoria) concurrent with cutaneous myiasis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 46-year-old Iranian female kidney transplant recipient with chromoblastomycosis caused by Alternaria infectoria and concurrent myiasis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3888:4129]` | Test: `Dermoscopic, microscopic, and ITS sequencing evaluation` | Target: `Leishmaniasis` | Specimen: `leg skin lesions` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "After conducting dermoscopic and microscopic examinations, as well as the result of ITS sequencing, the lesions were determined to be different from deep mycosis, atopic mycobacterium, TB, leishmaniasis, pyoderma gangrenosum, and vasculitis."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 46-year-old female renal transplant recipient presented with verrucous, ulcerative leg lesions showing medlar bodies on KOH prep, fly larvae (myiasis), and Alternaria infectoria on culture and ITS sequencing. Dermoscopic, microscopic, and molecular examinations explicitly excluded leishmaniasis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 82: `PMC10482395_09::Leishmaniasis` (`PMC10482395_09`)

- **Article Title:** Editorial: Case reports in dermatology
- **Demographics (Metadata):** Age `64.0`, Gender `Male`, Year `2023`, Journal `Front Med (Lausanne)`
- **Primary Established Diagnosis of Case:** Not applicable (Editorial summarizing 5 dermatology case reports)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_SINGLE_PATIENT`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `SYSTEMATIC_REVIEW`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `MULTI_PATIENT_CASE_SERIES`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `NONE` — Editorial ('Editorial: Case reports in dermatology') summarizing 5 distinct published case reports by different author groups (Tozaki et al., Xue et al., Scholl et al.). Metadata age=64.0/Male belongs to Tozaki et al.'s VEXAS patient, whereas Leishmania infantum is mentioned in a 3-sentence summary of Scholl et al.'s patient.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `AFFIRMED`
6. **Step 7 — Temporality (`step7_temporality`):** `UNKNOWN`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[1071:1308]` | Test: `Secondary editorial summary of Scholl et al.` | Target: `Leishmania infantum` | Specimen: `None` | Result: `POSITIVE` | Relation: `SUPPORTS` (`E4_CONTEXT`)
     > "Scholl et al. describe a patient with long-term plaque psoriasis and psoriasis arthropathica who was treated with methotrexate and adalimumab. Then, this patient developed cutaneous pseudolymphoma caused by Leishmania infantum infection."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_SINGLE_PATIENT` | Failure Flags: `['F2_SCOPE_COHORT', 'F3_SUBJECT_COREFERENCE']`
12. **Clinical Rationale:** This document is a journal Editorial summarizing five separate dermatology case reports published in a Research Topic. The metadata anchor (64-year-old male) refers to Tozaki et al.'s VEXAS syndrome case in paragraph 1, whereas Leishmania infantum is mentioned in paragraph 4 as a secondary summary of Scholl et al.'s case without primary clinical or diagnostic data. Because the document is a multi-paper editorial rather than a single-patient primary case report (and exhibits subject coreference mismatch), it is excluded -> EXCLUDED_NON_SINGLE_PATIENT.

### Case 83: `PMC11066154_01::Leishmaniasis` (`PMC11066154_01`)

- **Article Title:** Antiphospholipid antibody-related hepatic vasculitis in a juvenile after non-severe COVID-19: a case report and literature review
- **Demographics (Metadata):** Age `15.0`, Gender `Female`, Year `2024`, Journal `Front Immunol`
- **Primary Established Diagnosis of Case:** Antiphospholipid antibody-related hepatic vasculitis and probable antiphospholipid syndrome
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 15-year-old girl with antiphospholipid antibody-related hepatic vasculitis and cerebral infarcts following mild COVID-19.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[861:1305]` | Test: `Blood/liver mNGS and Leishmania serology screening` | Target: `Leishmania` | Specimen: `peripheral blood, liver biopsy, serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Possible pathogens were under intense exploration, but all proved negative after following tests: traditional microbiologic culture and metagenomic next-generation sequencing of peripheral blood samples and liver biopsy specimens; serology screenings for fungi, SASR-CoV-2, hepatitis viruses, TORCH pathogens, Leishmania, and mycobacteria tuberculosis; Epstein-Barr virus DNA analysis; and microscopic examination of parasites in stool samples."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 15-year-old girl presented with hyperpyrexia, abdominal pain, and hepatic necrosis due to antiphospholipid antibody-related hepatic vasculitis after mild SARS-CoV-2 infection. Metagenomic next-generation sequencing (blood and liver biopsy) and serology screening for Leishmania were explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 84: `PMC10921100_01::Leishmaniasis` (`PMC10921100_01`)

- **Article Title:** Severe murine typhus complicated by multiple organ dysfunctions: A case report
- **Demographics (Metadata):** Age `70.0`, Gender `Male`, Year `2024`, Journal `Caspian J Intern Med`
- **Primary Established Diagnosis of Case:** Severe murine typhus (Rickettsia typhi) with multiorgan failure
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 70-year-old Albanian male farmer with fatal severe murine typhus (Rickettsia typhi) complicated by multiorgan dysfunction.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1436:1580]` | Test: `Serological test for Leishmania spp.` | Target: `Leishmania spp.` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Serological tests of Leptospira, Brucella spp., Leishmania spp, and viral infections such as HIV, hepatitis B and C, CMV, and EBV were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 70-year-old male farmer in Albania presented in coma with fever, rash, hepatosplenomegaly, and multiorgan failure due to severe murine typhus (Rickettsia typhi IgM and IgG ELISA positive, Weil-Felix OX19 1:640). Serological testing for Leishmania spp. was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 85: `PMC11152966_01::Leishmaniasis` (`PMC11152966_01`)

- **Article Title:** Two cases of misleading Epstein-Barr virus infection and the role of EBV-DNA
- **Demographics (Metadata):** Age `15.0`, Gender `Female`, Year `2024`, Journal `IDCases`
- **Primary Established Diagnosis of Case:** Acute Epstein-Barr virus infectious mononucleosis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 15-year-old Italian girl returning from Kenya with infectious mononucleosis (EBV-DNA positive).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1694:2001]` | Test: `Microbiological test for leishmaniasis` | Target: `Leishmaniasis` | Specimen: `blood/serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Blood culture and pharynx swab did not yield any microorganisms and tests for hepatitis A, B, C, cytomegalovirus (CMV) infections, human immunodeficiency virus (HIV) infection, West Nile virus infection, dengue virus infection, rickettsiosis, brucellosis, leptospirosis, and leishmaniasis were all negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 15-year-old girl returning to Italy from Kenya presented with high fever, tonsillitis, cervical lymphadenopathy, and splenomegaly. Testing for leishmaniasis was explicitly negative, and quantitative blood PCR (4452 copies/mL) and repeat serology confirmed acute Epstein-Barr virus infectious mononucleosis. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 86: `PMC11382317_01::Leishmaniasis` (`PMC11382317_01`)

- **Article Title:** Mucocutaneous relapse during late latent syphilis as initial presentation of HIV infection
- **Demographics (Metadata):** Age `38.0`, Gender `Male`, Year `2024`, Journal `IDCases`
- **Primary Established Diagnosis of Case:** Mucocutaneous relapse of late latent syphilis with HIV coinfection
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 38-year-old Caucasian man with mucocutaneous relapse of late latent syphilis and newly diagnosed HIV infection.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1655:1923]` | Test: `Leishmaniasis serology and PCR screening` | Target: `Leishmania` | Specimen: `serum/blood` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Screening for opportunistic infections, including tuberculosis (Quantiferon Tb Gold), cryptococcosis (serum antigen), toxoplasmosis (serology), and leishmaniasis (serology and polymerase chain reaction) was unremarkable all but positive Toxoplasma gondii IgG serology."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 38-year-old man presented with mucocutaneous relapse of late latent syphilis (RPR 1:128) as the initial manifestation of HIV infection. Opportunistic infection screening for leishmaniasis by both serology and PCR was negative/unremarkable. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 87: `PMC10868469_01::Leishmaniasis` (`PMC10868469_01`)

- **Article Title:** Management of pemphigoid vegetans with mycophenolate mofetil: A case report
- **Demographics (Metadata):** Age `63.0`, Gender `Female`, Year `2024`, Journal `SAGE Open Med Case Rep`
- **Primary Established Diagnosis of Case:** Pemphigoid vegetans
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_TARGET_CASE`** (Prompt Decision Enum: `EXCLUDED_NON_TARGET_CASE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 63-year-old woman with pemphigoid vegetans.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `CONTEXT_ONLY`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `EPIDEMIOLOGICAL_CONTEXT`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E4_BACKGROUND_OR_CONTEXT_ONLY`
   - **Evidence Item 1:** `case_text[426:574]` | Test: `Epidemiological travel history` | Target: `Leishmaniasis` | Specimen: `None` | Result: `NEGATIVE` | Relation: `REFUTES` (`E4_CONTEXT`)
     > "She had not travelled to endemic regions for leishmaniasis or other parasitic infections and had no new medication introduced prior to her symptoms."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_TARGET_CASE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F5_DISCOURSE_CONTEXT']`
12. **Clinical Rationale:** A 63-year-old woman presented with painful vesicular and vegetative plaques on the nostril, fingertips, and perineum, and was diagnosed by histopathology and direct immunofluorescence with pemphigoid vegetans. Leishmaniasis is mentioned solely to note that she had not traveled to endemic regions for leishmaniasis, with special stains negative for microorganisms -> EXCLUDED_NON_TARGET_CASE.

### Case 88: `PMC10586894_01::Leishmaniasis` (`PMC10586894_01`)

- **Article Title:** Reactive Granulomatous Dermatitis in a Child with Acute Lymphoblastic Leukemia
- **Demographics (Metadata):** Age `3.0`, Gender `Female`, Year `2023`, Journal `Case Rep Dermatol Med`
- **Primary Established Diagnosis of Case:** Reactive granulomatous dermatitis in acute lymphoblastic leukemia
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 3-year-old female with acute lymphoblastic leukemia (ALL) and reactive granulomatous dermatitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[2459:2782]` | Test: `Histopathology special stains and clinico-epidemiological exclusion` | Target: `Leishmaniasis` | Specimen: `skin biopsy` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Special stains did not reveal any infectious organisms. Bacterial, fungal, and acid-fast tissue cultures were negative. Due to the rarity of leishmaniasis and leprosy in her geographic area, absence of travel history, and lack of specific features on pathology, additional specialty microbiologic testing was not performed."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F5_DISCOURSE_CONTEXT']`
12. **Clinical Rationale:** A 3-year-old girl on maintenance chemotherapy for ALL presented with ulcerated papules and nodules on her extremities showing palisading granulomas on skin biopsy. Special stains revealed no infectious organisms, and leishmaniasis was excluded based on lack of histopathologic features, absence of travel history, and geographic rarity, establishing reactive granulomatous dermatitis -> NEGATIVE.

### Case 89: `PMC11829613_01::Leishmaniasis` (`PMC11829613_01`)

- **Article Title:** Pneumocystis Pneumonia and Disseminated Cryptococcosis Dual Infection: A Case Report
- **Demographics (Metadata):** Age `56.0`, Gender `Male`, Year `2025`, Journal `Cureus`
- **Primary Established Diagnosis of Case:** Pneumocystis jirovecii pneumonia and disseminated Cryptococcus neoformans coinfection in HIV/AIDS
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 56-year-old man with untreated HIV/AIDS presenting with Pneumocystis jirovecii pneumonia and disseminated Cryptococcus neoformans infection.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1626:1742]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Additional serologic studies for syphilis, Toxoplasma gondii, Leishmania, and Hepatitis B and C virus were negative."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 56-year-old man with untreated HIV/AIDS (CD4 1 cell/uL) was admitted with Pneumocystis jirovecii pneumonia and disseminated cryptococcosis (Cryptococcus neoformans in BAL, blood, and CSF). Serologic testing for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 90: `PMC11753555_01::Leishmaniasis` (`PMC11753555_01`)

- **Article Title:** Unsuspecting Plaque on the Forearm: A Diagnostic Challenge
- **Demographics (Metadata):** Age `45.0`, Gender `Male`, Year `2024`, Journal `Indian Dermatol Online J`
- **Primary Established Diagnosis of Case:** Microcystic adnexal carcinoma (MAC)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 45-year-old male chef with a microcystic adnexal carcinoma (MAC) plaque on the right forearm.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[625:1008]` | Test: `Incisional skin biopsy histopathology` | Target: `Leishmaniasis` | Specimen: `forearm plaque biopsy` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Basidiobolomycosis, sarcoidosis, and leishmaniasis were considered as differential diagnoses, and an incisional biopsy was done and sent for histopathological examination. The pathologist's initial report was suggestive of syringoma, however, this did not correlate with the clinical presentation, further revaluation of the slide was done and a final diagnosis of MAC was concluded."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']`
12. **Clinical Rationale:** A 45-year-old male presented with a solitary indurated plaque on the right forearm present for 20 years. Leishmaniasis was considered in the clinical differential diagnosis, and incisional biopsy histopathology with S100 immunohistochemistry established microcystic adnexal carcinoma (MAC), ruling out leishmaniasis -> NEGATIVE.

### Case 91: `PMC11790262_01::Leishmaniasis` (`PMC11790262_01`)

- **Article Title:** Navigating Challenges in a Case of Unusual Hepatic and Pulmonar Sarcoidosis: A Comprehensive Clinical Journey
- **Demographics (Metadata):** Age `35.0`, Gender `Female`, Year `2024`, Journal `GE Port J Gastroenterol`
- **Primary Established Diagnosis of Case:** Hepatic and pulmonary sarcoidosis with vanishing bile duct syndrome
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 35-year-old Congolese female with hepatic and pulmonary sarcoidosis and vanishing bile duct syndrome.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3557:3781]` | Test: `Hepatic granuloma etiological study` | Target: `Leishmaniasis` | Specimen: `serum/liver biopsy` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Mycobacterium tuberculosis work-up was negative, and the hepatic granuloma etiological study was negative for syphilis, toxoplasmosis, rubella, leptospirosis, Q fever, Schistosoma, brucella, leishmaniasis and histoplasmosis."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 35-year-old Congolese woman presented with cholestatic jaundice, pruritus, weight loss, and non-caseating bronchial and hepatic granulomas with vanishing bile duct syndrome. Etiological testing for leishmaniasis was explicitly negative, and hepatic and pulmonary sarcoidosis was diagnosed. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 92: `PMC11831705_03::Leishmaniasis` (`PMC11831705_03`)

- **Article Title:** Eosinophilic Fasciitis: A Case Series
- **Demographics (Metadata):** Age `70.0`, Gender `Male`, Year `2025`, Journal `Cureus`
- **Primary Established Diagnosis of Case:** Eosinophilic fasciitis
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 70-year-old male (Patient 3 of a 4-patient case series) diagnosed with eosinophilic fasciitis.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[814:1063]` | Test: `Parasite serology panel` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "The etiological workup revealed negative parasite serologies (Strongyloides, Echinococcus, Fasciola, Toxocara, Leishmania), negative stool parasitology, and negative immune tests for antinuclear antibodies and anti-neutrophil cytoplasmic antibodies."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 70-year-old man presented with asthenia, fever, bilateral limb edema, marked peripheral eosinophilia, and skin thickening, and was diagnosed by full-thickness biopsy with eosinophilic fasciitis. Parasite serology for Leishmania was explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 93: `PMC12869808_01::Leishmaniasis` (`PMC12869808_01`)

- **Article Title:** Diagnostic Challenges in Seronegative Celiac Disease: A Case of Massive Splenomegaly and Persistent Metabolic Imbalance
- **Demographics (Metadata):** Age `41.0`, Gender `Female`, Year `2026`, Journal `Cureus`
- **Primary Established Diagnosis of Case:** Suspected seronegative celiac disease with massive splenomegaly
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 41-year-old Egyptian woman from Al Fayoum with suspected seronegative celiac disease and massive splenomegaly.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1876:2002]` | Test: `Leishmania serology` | Target: `Leishmania` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Infectious screening, including hepatitis B and C, HIV, EBV, CMV, Brucella, and Leishmania serologies, was negative (Table 6)."
   - **Evidence Item 2:** `case_text[3755:4041]` | Test: `Duodenal and jejunal biopsy histopathology` | Target: `Parasites (including Leishmania)` | Specimen: `duodenum and jejunum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Histological examination of duodenal and jejunal biopsies showed preserved villous architecture with a mild increase in intraepithelial lymphocytes (50-60 per 100 enterocytes), consistent with Marsh I-II changes. No parasites, granulomas, dysplasia, or malignant features were observed."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 41-year-old Egyptian woman presented with chronic diarrhea, severe electrolyte derangements, and massive splenomegaly (25 cm), and was diagnosed with seronegative celiac disease responsive to a gluten-free diet. Leishmania serology was explicitly negative, and duodenal/jejunal and bone marrow biopsies showed no parasites. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 94: `PMC12860415_01::Leishmaniasis` (`PMC12860415_01`)

- **Article Title:** Primary Extracranial Ewing Sarcoma Complicated by Hemorrhagic Shock and Multimicrobial Infection: A Diagnostic and Therapeutic Challenge
- **Demographics (Metadata):** Age `19.0`, Gender `Male`, Year `2026`, Journal `Cureus`
- **Primary Established Diagnosis of Case:** Primary extracranial Ewing sarcoma (EWSR1-rearranged)
- **Final Dataset Label (`step12_dataset_label`):** **`NEGATIVE`** (Prompt Decision Enum: `NEGATIVE` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `SINGLE_HUMAN_PATIENT`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — 19-year-old male from Sao Tome and Principe with primary extracranial parieto-occipital Ewing sarcoma.
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[1861:2045]` | Test: `Parasitic culture and Leishmania testing` | Target: `Leishmania` | Specimen: `scalp mass biopsy` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Bacterial, fungal, and parasitic cultures, as well as PCR for Mycobacterium tuberculosis, nontuberculous mycobacteria, and pan-fungal targets, were negative, as was Leishmania testing."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `NEGATIVE` | Failure Flags: `['F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** A 19-year-old man from Sao Tome and Principe presented with a large ulcerated, bleeding parieto-occipital mass confirmed by histopathology, CD99 positivity, and EWSR1 rearrangement as primary extracranial Ewing sarcoma. Parasitic cultures and Leishmania testing on the mass biopsy were explicitly negative. Assertion NEGATED, clinical role RULED_OUT_DIAGNOSIS -> NEGATIVE.

### Case 95: `PMC12602206_01::Leishmaniasis` (`PMC12602206_01`)

- **Article Title:** Case Report: α1-antitrypsin deficiency causing persistent pleural effusion and multilobar alveolar emphysema in a young dog
- **Demographics (Metadata):** Age `3.0`, Gender `Male`, Year `2025`, Journal `Front Vet Sci`
- **Primary Established Diagnosis of Case:** Canine alpha-1 antitrypsin deficiency (A1ATD)
- **Final Dataset Label (`step12_dataset_label`):** **`EXCLUDED_NON_HUMAN`** (Prompt Decision Enum: `EXCLUDED_NON_CASE_REPORT` | VPD Satisfied: `False` | Confidence: `HIGH`)

#### 12-Step Protocol Reasoning Trace
1. **Step 1 — Document Type (`step1_document_type`):** `CASE_REPORT`
2. **Step 2 — Unit of Analysis (`step2_ccu_type`):** `ANIMAL_CASE`
3. **Step 3 — Patient Anchor (`step3_patient_anchor`):** `PRIMARY_PATIENT` — Veterinary patient: 3-year-old intact male mixed-breed dog with alpha-1 antitrypsin deficiency (A1ATD).
4. **Step 4 & 5 — Disease Mentions & Concept Grounding (`step5_concept_grounding`):** `TARGET_CONFIRMED`
5. **Step 6 — Assertion Type (`step6_assertion_type`):** `NEGATED`
6. **Step 7 — Temporality (`step7_temporality`):** `CURRENT_ACTIVE`
7. **Step 8 — Clinical Role (`step8_clinical_role`):** `RULED_OUT_DIAGNOSIS`
8. **Step 9 — Evidence Strength (`step9_evidence_strength`):** `E0_CONTRADICTED`
   - **Evidence Item 1:** `case_text[3386:3526]` | Test: `Canine Leishmania infantum serology` | Target: `Leishmania infantum` | Specimen: `serum` | Result: `NEGATIVE` | Relation: `REFUTES` (`E0_CONTRADICTED`)
     > "Furthermore, serologic testing for Leishmania infantum, Ehrlichia canis, and Borrelia burgdorferi yielded negative results (all below 1:20)."
9. **Step 10 — Contradiction Reconciliation (`step10_contradiction_flag`):** `False` — No contradictory claims.
10. **Step 11 — Valid Positive Diagnosis Test (`step11_vpd_satisfied`):** `False`
11. **Step 12 — Final Label & Failure Flags:** `EXCLUDED_NON_HUMAN` | Failure Flags: `['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
12. **Clinical Rationale:** Veterinary case report of a 3-year-old male mixed-breed dog with persistent transudative pleural effusion and multilobar alveolar emphysema due to alpha-1 antitrypsin deficiency (A1ATD), in which serology for Leishmania infantum was negative (<1:20). Excluded from the human benchmark because ccu_type is ANIMAL_CASE -> EXCLUDED_NON_HUMAN.

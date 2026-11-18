# Nocardiosis Clinical Claim Annotation — 12-Step Reasoning Log

## Case 1: `PMC9852504_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 54.0 | Gender: Male (54-year-old male ceramic worker)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 54-year-old immunocompetent male ceramic worker with large mediastinal mass. EBUS-TBNA purulent exudate showed weakly acid-fast branching filamentous rods, mNGS identified Nocardia arizonensis and Nocardia cyriacigeorgica, and culture grew Nocardia species (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 2: `PMC4363670_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 46.0 | Gender: Male (46-year-old HIV-1/HBV-infected male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 46-year-old HIV-1/HBV-infected male with disseminated abscesses (brain, adrenal, lung, skin). Adrenal mass puncture culture grew Nocardia spp. (E1 confirmatory from sterile site). VPD satisfied -> POSITIVE.

## Case 3: `PMC8183679_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 61.0 | Gender: Male (61-year-old male with nephrotic syndrome on prednisolone and tacrolimus)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 61-year-old immunocompromised male with multiple intermuscular abscesses and bilateral interstitial pneumonia. Blood mNGS and BALF mNGS both detected Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 4: `PMC10115452_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 77.0 | Gender: Female (77-year-old woman with type 2 diabetes mellitus)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 77-year-old diabetic woman with lower extremity purulent ulceration. Culture of purulent material showed partially acid-fast branching Gram-positive bacilli and MALDI-TOF MS identified Nocardia brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 5: `PMC10115452_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 63.0 | Gender: Female (63-year-old female with ankylosing spondylitis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 63-year-old woman with right hand mass after rose thorn injury. Culture, MALDI-TOF MS, and PCR confirmed Mycobacterium marinum; Nocardiosis is neither diagnosed nor mentioned in this patient's case_text. -> EXCLUDED_NON_TARGET_CASE.

## Case 6: `PMC6643105_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 53.0 | Gender: Female (53-year-old woman with ANCA-associated renal vasculitis on methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 53-year-old immunosuppressed woman with cavitary pneumonia and brain abscess. Deep tracheal sputum grew Nocardia asteroides confirmed by 16S rDNA sequencing (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 7: `PMC4894989_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 59.0 | Gender: Male (59-year-old male with prostate adenocarcinoma and ITP on prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 59-year-old immunocompromised male with cavitated right middle lobe pneumonia. CT-guided lung biopsy culture yielded waxy colonies with weak Gram-positive branched filamentous bacilli (Nocardia infection), resolving on TMP-SMX (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 8: `PMC9127990_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 61.0 | Gender: Male (61-year-old man with macroglobulinemia on prednisone and thalidomide)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 61-year-old immunocompromised man with pulmonary nodules, scalp/skin abscesses, and brain abscess. Blood culture grew weak acid-fast filamentous Gram-positive bacilli confirmed by 16S rRNA sequencing as Nocardia vulneris (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 9: `PMC9006427_01::Nocardiosis`
- **Step 1 (Document Type):** SYSTEMATIC_REVIEW
- **Step 2 (CCU Type):** AGGREGATE_STUDY_UNIT
- **Step 3 (Patient Anchor):** POPULATION | Age: 60.0 | Gender: Unknown (27 patients with nipple piercing infections)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Qualitative systematic review summarizing 27 patients with nipple piercing infections, not a single-human-patient case report. -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 10: `PMC6399552_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 56.0 | Gender: Female (56-year-old female with AML and neutropenic fever)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Nocardiosis was considered in differential diagnosis, but BAL fungal PCR confirmed Rhizomucor pusillus.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 56-year-old woman with AML and multifocal septic emboli. Nocardiosis was only suspected in the differential diagnosis; broad-range fungal PCR on BAL fluid confirmed Rhizomucor pusillus (mucormycosis). -> NEGATIVE.

## Case 11: `PMC9128046_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 51.0 | Gender: Female (51-year-old female with SLE and ILD on high-dose methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 51-year-old woman with SLE on long-term high-dose methylprednisolone and right upper lobe cavitary mass who developed fatal bilateral polymicrobial pneumonia explicitly including Nocardia (E2 clinical/microbiologic diagnosis, specific assay not named). VPD satisfied -> POSITIVE.

## Case 12: `PMC9234165_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 52.0 | Gender: Female (52-year-old female with Kartagener syndrome / PCD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 52-year-old woman with Kartagener syndrome (DNAH9 mutations) admitted with productive cough and tree-in-bud lung lesions. BALF metagenomic sequencing identified Nocardia gelsenkircheni (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 13: `PMC4213137_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old man on prednisolone with bilateral subretinal abscess)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Nocardia suspected empirically, but cultures grew only Candida albicans and Gram-negative rods were seen.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 64-year-old man with bilateral endogenous subretinal abscesses. Nocardia was suspected empirically without improvement; vitreous cultures confirmed Candida albicans and Gram-negative rods. -> NEGATIVE.

## Case 14: `PMC6936928_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 93.0 | Gender: Female (93-year-old woman with cervical lymphadenopathy)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 93-year-old woman with cervical lymphadenopathy. Lymph node PCR was explicitly negative for Nocardia, and culture confirmed Mycobacterium tuberculosis. -> NEGATIVE.

## Case 15: `PMC2799960_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 83.0 | Gender: Male (83-year-old male with ITP on long-term corticosteroids)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 83-year-old male on long-term corticosteroids for ITP with necrotizing right upper lobe mass and cerebellar lesion. Sputum cultures grew Nocardia sp. (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 16: `PMC9391167_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old male kidney transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 64-year-old male kidney transplant recipient with right lower lobe pneumonia. Expanded sputum culture grew Nocardia species (E1 confirmatory), resolving on minocycline. VPD satisfied -> POSITIVE.

## Case 17: `PMC9880008_01::Nocardiosis`
- **Step 1 (Document Type):** CASE_SERIES
- **Step 2 (CCU Type):** MULTI_PATIENT_CASE_SERIES
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 62.0 | Gender: Female (Multi-patient case series (Case 1: 62F, Case 2: 2M, Case 3: 56F))
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Multi-patient case series concatenating three distinct patients (Case 1: 62F N. otitidiscaviarum; Case 2: 2M N. cyriacigeorgica; Case 3: 56F N. farcinica) in a single case_text. Fails single-human-patient CCU requirement -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 18: `PMC4489939_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 27.0 | Gender: Male (27-year-old male immigrant from Mali)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** POSSIBLE_HYPOTHETICAL
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** DIFFERENTIAL_DIAGNOSIS
- **Step 9 (Evidence Strength):** E3_SUPPORTIVE_NON_SPECIFIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `UNRESOLVED` | Confidence: MEDIUM | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 27-year-old male with arm actinomycetoma. Cultures were negative and histopathology gave only a probable diagnosis ('actinomycetoma probably due to Nocardia') without species/culture/molecular confirmation (E3 only). VPD not satisfied -> UNRESOLVED.

## Case 19: `PMC8053466_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 58.0 | Gender: Female (58-year-old female with rheumatoid arthritis on leflunomide)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 58-year-old woman with rheumatoid arthritis and brain abscess. Intraoperative cultures for Nocardia came up negative. -> NEGATIVE.

## Case 20: `PMC5350350_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Unknown (Primary patient with arm nodule and bilateral lung nodules)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** Patient with arm nodule and bilateral upper lung nodules. Punch biopsy showed Gram-positive filamentous rods, positive modified Kinyoun stain, and tissue culture grew Nocardia brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 21: `PMC5350350_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Unknown (Primary patient at discharge/follow-up)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** UNKNOWN
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (0 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `UNRESOLVED` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** Follow-up excerpt describing discharge on TMP-SMX and 5-week CT/PFT improvement without mentioning Nocardia or diagnostic evidence in case_text (title-only signal). Insufficient evidence in this case unit -> UNRESOLVED.

## Case 22: `PMC9830566_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 59.0 | Gender: Male (59-year-old immunocompetent man)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 59-year-old immunocompetent man with pneumonia, sepsis, and endobronchial mass. Both blood and BALF quantitative mNGS detected Nocardia farcinica (E1 confirmatory), resolving on sulfamethoxazole. VPD satisfied -> POSITIVE.

## Case 23: `PMC7471810_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 79.0 | Gender: Male (79-year-old man with CLL)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 79-year-old man with CLL and mixed invasive mold (Aspergillus fumigatus, Lichtheimia corymbifera) plus Nocardia coinfection. Plasma cfDNA NGS detected Nocardia abscessus and autopsy brain abscess showed Fite-positive filamentous organisms consistent with Nocardia (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 24: `PMC7301693_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 0.0 | Gender: Male (9-month-old boy with Type 1 Hyper-IgM syndrome)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 9-month-old boy with Pneumocystis jirovecii-associated PAP. Screening test for Nocardia was explicitly negative. -> NEGATIVE.

## Case 25: `PMC8046554_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 0.0 | Gender: Female (4-month-old female infant with Mycobacterium abscessus pneumonia)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F1_LEXICAL_HOMONYM', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** 4-month-old infant with Mycobacterium abscessus pneumonia. 'Nocardia' appears solely in the name of the reference laboratory ('Mycobacteria/Nocardia lab'). -> EXCLUDED_NON_TARGET_CASE.

## Case 26: `PMC6694281_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** ANIMAL_CASE
- **Step 3 (Patient Anchor):** ANIMAL | Age: 5.0 | Gender: Female (7.5-year-old female spayed Great Dane dog)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_HUMAN` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Veterinary case report of a 7.5-year-old Great Dane dog with Nocardia niigatensis infection. Non-human subject -> EXCLUDED_NON_HUMAN.

## Case 27: `PMC2852743_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 45.0 | Gender: Female (45-year-old female renal transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 45-year-old female renal transplant recipient with cavitary left upper lobe pneumonia. BAL cultures grew Nocardia nova (E1 confirmatory), treated with TMP-SMX. VPD satisfied -> POSITIVE.

## Case 28: `PMC2874368_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 39.0 | Gender: Female (39-year-old HIV-positive woman with fatal H1N1 2009 pneumonia)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** HISTORICAL_RESOLVED
- **Step 7 (Temporality):** HISTORICAL_RESOLVED
- **Step 8 (Clinical Role):** PAST_HISTORY
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Past history of pleuropericardial Nocardia; current BAL/blood/pleural cultures negative for Nocardia and only H1N1 RT-PCR positive.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 39-year-old HIV+ woman with past history of pleuropericardial Nocardia infection. During current admission, no Nocardia or other pathogens were detected in blood, sputum, BAL, or pleural fluid; fatal pneumonia was due to H1N1 2009 RT-PCR+. -> NEGATIVE.

## Case 29: `PMC9113660_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 34.0 | Gender: Male (34-year-old male on CAPD with Tsukamurella inchonensis peritonitis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 34-year-old male with CAPD peritonitis caused by Tsukamurella inchonensis. Nocardia is mentioned solely as a CLSI antimicrobial susceptibility breakpoint reference. -> EXCLUDED_NON_TARGET_CASE.

## Case 30: `PMC9432383_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 35.0 | Gender: Male (35-year-old male renal transplant recipient with C. striatum endocarditis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 35-year-old male with Corynebacterium striatum endocarditis. Nocardia is mentioned solely in the mNGS bioinformatics positivity threshold rule. -> EXCLUDED_NON_TARGET_CASE.

## Case 31: `PMC7468610_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 40.0 | Gender: Female (40-year-old woman with breast cancer and AML post-HSCT)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 40-year-old woman post-allogeneic HSCT with bilateral pneumonia and pulmonary abscess. BAL microbiology and lobectomy histology both confirmed Nocardia spp. (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 32: `PMC9490265_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old male post liver transplantation)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 64-year-old male post-liver transplantation with high fever and bilateral pulmonary infiltrates. Sputum culture grew Nocardia farcinica (E1 confirmatory), resolving on SMX, minocycline, and amikacin. VPD satisfied -> POSITIVE.

## Case 33: `PMC8486545_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 33.0 | Gender: Male (33-year-old male with Hantavirus cardiopulmonary syndrome)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 33-year-old male with Hantavirus cardiopulmonary syndrome and DAH. BAL Nocardia cultures were explicitly negative. -> NEGATIVE.

## Case 34: `PMC7169360_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** ANIMAL_CASE
- **Step 3 (Patient Anchor):** ANIMAL | Age: 11.0 | Gender: Female (11-year-old spayed female cat)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** DIFFERENTIAL_DIAGNOSIS
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_HUMAN` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Veterinary case report of an 11-year-old cat with Cryptococcus neoformans (nocardiosis only in differential). Non-human subject -> EXCLUDED_NON_HUMAN.

## Case 35: `PMC4070928_02::Nocardiosis`
- **Step 1 (Document Type):** CASE_SERIES
- **Step 2 (CCU Type):** MULTI_PATIENT_CASE_SERIES
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 46.0 | Gender: Male (46-year-old Albanian male with Actinomadura madurae plus literature review)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** Patient 2 had Actinomadura madurae mycetoma; Nocardia appears only in a multi-patient literature review of Greek cases within the same text. -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 36: `PMC9445126_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 2.0 | Gender: Male (2-year-old male with X-linked CGD and McLeod syndrome)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 2-year-old boy with X-linked CGD presenting with new-onset Nocardia lymphadenitis and multiple cavitary lung nodules (disseminated Nocardia infection) necessitating allogeneic HSCT (E2 characteristic syndrome/established diagnosis, specific lab assay not detailed). VPD satisfied -> POSITIVE.

## Case 37: `PMC3768339_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 20.0 | Gender: Female (20-year-old female with crystal storing histiocytosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 20-year-old female with temporal lobe crystal storing histiocytosis. Special stains for Nocardia on resected brain tissue were negative. -> NEGATIVE.

## Case 38: `PMC7328479_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 67.0 | Gender: Female (67-year-old immunocompetent female)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 67-year-old immunocompetent woman with sporotrichoid nodular lymphangitis after rose thorn injury. Wound culture grew filamentous acid-fast organisms identified by MALDI-TOF MS and PCR sequencing as N. pseudobrasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 39: `PMC5820550_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 63.0 | Gender: Female (63-year-old female redo lung transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 63-year-old lung transplant recipient with FDG-avid right renal mass. Nephrectomy specimen showed Fite-positive filamentous bacteria and PCR identified Nocardia paucivorans (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 40: `PMC10443697_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 46.0 | Gender: Female (46-year-old female with scalp Mycobacterium abscessus infection)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 46-year-old woman with scalp Mycobacterium abscessus infection. Nocardia seriolae ATCC 43993 was mentioned solely as an outgroup in the phylogenetic tree. -> EXCLUDED_NON_TARGET_CASE.

## Case 41: `PMC6867963_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 16.0 | Gender: Male (16-year-old boy with cannabis-related DAH)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 16-year-old boy with cannabis-related diffuse alveolar hemorrhage. Blood and sputum cultures for Nocardia spp. were negative. -> NEGATIVE.

## Case 42: `PMC5340051_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 35.0 | Gender: Male (35-year-old male with MPGN on oral prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 35-year-old immunosuppressed male with bilateral endophthalmitis and intracerebral abscess. Brain biopsy and abscess drainage revealed Nocardia organism with granulomatous reactions (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 43: `PMC6167885_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 62.0 | Gender: Male (62-year-old male renal transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 62-year-old renal transplant recipient with cutaneous lesions at transplant scar. Microscopy showed branching filamentous AFB and aerobic culture identified Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 44: `PMC3885780_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 77.0 | Gender: Male (77-year-old immunocompetent Korean male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 77-year-old immunocompetent male with necrotizing pneumonia and empyema. Serial pleural fluid cultures grew modified acid-fast Gram-positive branching filaments confirmed by 16S rRNA and secA1 sequencing as N. cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 45: `PMC9329676_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 61.0 | Gender: Female (61-year-old female with RA/allergic vasculitis on methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 61-year-old immunosuppressed woman with cavitary lung nodules and frontal brain abscesses. Blood NGS, sputum culture, and BALF all confirmed Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 46: `PMC5128003_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 75.0 | Gender: Male (75-year-old male with DM and COPD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Initially suspected Nocardia spp. due to Gram+ AFB+ bacilli, but blood cultures grew Tsukamurella tyrosinosolvens and bronchial washings grew Mycobacterium bovis.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 75-year-old male initially suspected of Nocardia spp. due to Gram-positive acid-fast bacilli, but final cultures confirmed Tsukamurella tyrosinosolvens bacteremia and Mycobacterium bovis pneumonia. Competing diagnosis -> NEGATIVE.

## Case 47: `PMC7451144_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 22.0 | Gender: Female (22-year-old immunocompetent female with brainstem abscess)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** POSSIBLE_HYPOTHETICAL
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** DIFFERENTIAL_DIAGNOSIS
- **Step 9 (Evidence Strength):** E3_SUPPORTIVE_NON_SPECIFIC (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `UNRESOLVED` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 22-year-old female with brainstem abscess and lung lesion. All cultures and serologies were negative; only a presumptive diagnosis of nocardiosis was made without E1/E2 confirmation. -> UNRESOLVED.

## Case 48: `PMC4283927_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 70.0 | Gender: Male (70-year-old male with multiple myeloma on lenalidomide and dexamethasone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 70-year-old male with multiple myeloma and 6 brain abscesses. CT-guided brain biopsy showed modified Kinyoun partially acid-fast branching Gram-positive rods, and 16S rRNA sequencing confirmed N. paucivorans (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 49: `PMC9805727_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 49.0 | Gender: Male (49-year-old immunocompetent male truck driver)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 49-year-old immunocompetent man with left temporo-occipital brain abscess. Excised tissue showed weak acid-fast branching filamentous bacilli, mNGS identified N. brevicatena, and culture grew weak acid-fast branched bacilli (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 50: `PMC7239889_01::Nocardiosis`
- **Step 1 (Document Type):** SYSTEMATIC_REVIEW
- **Step 2 (CCU Type):** AGGREGATE_STUDY_UNIT
- **Step 3 (Patient Anchor):** POPULATION | Age: 9.0 | Gender: Female (Review of idiopathic CD4 lymphocytopenia (164 cases))
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Review article on Idiopathic CD4 Lymphocytopenia summarizing 164 cases and literature studies. Not a single-human-patient case report -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 51: `PMC8517639_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 66.0 | Gender: Female (66-year-old woman with membranous nephropathy on prednisone and cyclophosphamide)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 66-year-old immunosuppressed woman with pulmonary nodules, brain lesions, and abdominal abscess. EBUS-TBNA culture grew partial acid-fast Gram-positive rods identified by MALDI-TOF MS as Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 52: `PMC3785346_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 67.0 | Gender: Male (67-year-old male with angioimmunoblastic T-cell lymphoma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 67-year-old male with AIBTCL and cavitary pneumonia (coinfection with Aspergillus niger). BAL and sputum cultures grew branching Gram-positive rods identified as Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 53: `PMC534796_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 32.0 | Gender: Male (32-year-old previously healthy male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 32-year-old immunocompetent man with hand trauma and sporotrichoid lymphocutaneous nodules. Tissue smear showed partially acid-fast Gram-positive branching filaments and culture identified Nocardia brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 54: `PMC4808525_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 50.0 | Gender: Female (50-year-old female post-cataract surgery)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 50-year-old female with postoperative endophthalmitis. Vitreous/AC fluid showed Gram-positive beaded branching filaments on modified Kinyoun stain and culture identified Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 55: `PMC6791275_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 40.0 | Gender: Male (40-year-old male welder on oral/inhaled steroids)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 40-year-old male on steroids with bilateral bronchiectasis and consolidation. Sputum modified acid-fast stain showed weakly acid-fast branching filamentous bacilli and culture/16S rRNA sequencing confirmed Nocardia cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 56: `PMC6791275_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 28.0 | Gender: Female (28-year-old female with bilateral bronchiectasis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 28-year-old female with bronchiectasis and consolidation. Sputum modified acid-fast stain showed weakly acid-fast branching filamentous bacilli and culture/16S rRNA sequencing confirmed Nocardia beijingensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 57: `PMC5362858_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** ANIMAL_CASE
- **Step 3 (Patient Anchor):** ANIMAL | Age: 1.0 | Gender: Female (1-year-old female domestic shorthair spayed cat)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** DIFFERENTIAL_DIAGNOSIS
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_HUMAN` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Veterinary case report of a 1-year-old cat with eosinophilic dermatosis (nocardiosis only in differential). Non-human subject -> EXCLUDED_NON_HUMAN.

## Case 58: `PMC4696691_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 67.0 | Gender: Female (67-year-old woman with COPD on corticosteroids)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 67-year-old woman on corticosteroids for COPD who developed respiratory failure; high-quality sputum culture isolated N. cerradoensis and she was treated with TMP-SMX for pulmonary nocardiosis with resolution (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 59: `PMC4696691_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 82.0 | Gender: Male (82-year-old man with emphysema on corticosteroids)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 82-year-old man on corticosteroids with subpleural consolidations; sputum culture grew N. cerradoensis (E1 confirmatory), treated with TMP-SMX for pulmonary nocardiosis with clearance. VPD satisfied -> POSITIVE.

## Case 60: `PMC8227459_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 51.0 | Gender: Female (51-year-old HIV-positive woman)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Nocardiosis suspected clinically, but lung core biopsy confirmed granulomatous Pneumocystis jirovecii pneumonia.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 51-year-old HIV+ woman with cavitating lung masses. Nocardiosis was suspected clinically, but lung core biopsy confirmed granulomatous Pneumocystis jirovecii pneumonia. -> NEGATIVE.

## Case 61: `PMC8216818_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 44.0 | Gender: Male (44-year-old immunocompromised male with LGL leukemia)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 44-year-old immunocompromised male with right parietal brain abscess. Craniotomy culture grew branching Gram-positive rods identified by 16S rDNA sequencing as Nocardia thailandica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 62: `PMC9780257_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 23.0 | Gender: Female (23-year-old immunocompetent female with bronchiectasis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 23-year-old immunocompetent female with bronchiectasis and pneumonia. BALF mNGS, whole genome sequencing, and qPCR confirmed Nocardia gipuzkoensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 63: `PMC6669421_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 49.0 | Gender: Male (49-year-old male renal transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 49-year-old male renal transplant recipient with RUL mass-like consolidation and mitral valve vegetation. Bronchoscopy biopsy showed filamentous Gram-positive bacteria and Nocardia PCR was positive (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 64: `PMC2841376_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 20.0 | Gender: Male (20-year-old male with scalp/eyelid sinuses and orbital invasion)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 20-year-old male with scalp and eyelid discharging sinuses and orbital extradural invasion. Microbiology testing identified Nocardia asteroides/brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 65: `PMC7849851_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 1.25 | Gender: Male (15-month-old boy with left eye panophthalmitis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 15-month-old boy with left eye panophthalmitis/intraconal abscess. Intraocular contents showed modified ZN-positive Gram-positive beaded filaments and culture confirmed Nocardia (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 66: `PMC3952898_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 45.0 | Gender: Male (45-year-old immunocompetent male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 45-year-old healthy male with wrist abscess and axillary lymphadenitis after swamp trauma. Pus culture grew Nocardia brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 67: `PMC10165100_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 57.0 | Gender: Female (57-year-old female with SLE on oral steroids and immunosuppressants)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 57-year-old woman with SLE on long-term immunosuppressants with disseminated Nocardia infection involving lungs, brain, and lower limb (E2 characteristic disseminated syndrome/established diagnosis, specific lab method not detailed). VPD satisfied -> POSITIVE.

## Case 68: `PMC4822357_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old male with sarcoidosis on prednisolone and diabetes)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 64-year-old male on steroids for sarcoidosis with thigh ulcer, skin papules, and intracranial ring-enhancing lesions. Ulcer discharge was modified acid-fast positive and cultures confirmed Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 69: `PMC9279908_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 75.0 | Gender: Male (75-year-old male with COP on methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 75-year-old male on methylprednisolone for COP with subcutaneous masses and bilateral frontal brain abscesses. Culture of mass aspirate and cranial abscess drainage confirmed Nocardia (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 70: `PMC8278857_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 8.0 | Gender: Female (8-year-old immunocompetent female child)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 8-year-old immunocompetent girl with cavitary lung destruction, empyema, and CNS involvement. Endotracheal aspirates and pleural fluid cultured Nocardia spp. (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 71: `PMC8278857_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 6.0 | Gender: Male (6-year-old brother with persistent cough)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 6-year-old boy admitted with persistent cough; sputum cultured Nocardia spp. (spelled 'Norcadia spp.' in text) (E1 confirmatory), recovered on ceftriaxone and co-trimoxazole. VPD satisfied -> POSITIVE.

## Case 72: `PMC9434960_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 30.0 | Gender: Female (30-year-old woman with SLE on MMF and prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 30-year-old woman with SLE and persistent SARS-CoV-2 PCR+ who developed a right frontoparietal brain abscess. Excised pus grew partially acid-fast Gram-positive filaments identified by MALDI-TOF MS as Nocardia cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 73: `PMC7673915_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 13.0 | Gender: Female (13-year-old female with Crohn disease on adalimumab and azathioprine)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 13-year-old female with Crohn disease on adalimumab/azathioprine and purulent plaque on back. Wound culture and MALDI-TOF MS confirmed Nocardia nova (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 74: `PMC9844142_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 47.0 | Gender: Female (47-year-old immunocompetent woman)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 47-year-old immunocompetent woman with lumbar subcutaneous abscess. Pus showed partially acid-fast branching Gram-positive rods and culture/MALDI-TOF MS identified N. cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 75: `PMC4977971_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 65.0 | Gender: Male (65-year-old man with AIHA on prednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 65-year-old man on prednisolone with bilateral occipital brain abscesses. Resected capsule culture showed Gram-positive branching filaments and 16S rRNA sequencing identified N. asiatica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 76: `PMC8606951_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 50.0 | Gender: Female (50-year-old female with varicella pneumonia)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 50-year-old female with disseminated varicella pneumonia. Bronchial washings for nocardiosis were explicitly negative. -> NEGATIVE.

## Case 77: `PMC9992866_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Male (Male patient in his 50s)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** Male in his 50s with ring-enhancing frontal/parietal brain abscesses. Neurosurgical biopsy showed beaded filamentous bacilli confirmed by Public Health Laboratory culture as N. farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 78: `PMC9992866_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Unknown (Primary patient post-mild COVID-19)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** Patient with cerebral abscess and lymphopenia post-COVID-19; second neurological biopsy and Public Health Laboratory testing confirmed N. farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 79: `PMC9812439_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** ANIMAL_CASE
- **Step 3 (Patient Anchor):** ANIMAL | Age: 10.0 | Gender: Female (10-year-old female mixed-breed cat (FeLV-positive))
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_HUMAN` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Veterinary case report of a 10-year-old FeLV-positive cat with Nocardia pyothorax. Non-human subject -> EXCLUDED_NON_HUMAN.

## Case 80: `PMC3320492_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 80.0 | Gender: Female (80-year-old woman with Williamsia muralis pulmonary infection)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 80-year-old woman with Williamsia muralis pulmonary infection. Nocardia is mentioned solely for 95% 16S rRNA sequence similarity and CLSI susceptibility breakpoints. -> EXCLUDED_NON_TARGET_CASE.

## Case 81: `PMC8308935_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old immunocompetent man)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 64-year-old immunocompetent man with posterior neck lesion, scalp fistulas, occipital osteomyelitis, and sagittal sinus thrombosis. Biopsy histopathology showed filamentous pathogens and established cutaneous/cerebral nocardiosis responding to TMP-SMX/doxycycline (E2). VPD satisfied -> POSITIVE.

## Case 82: `PMC5588403_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 53.0 | Gender: Male (53-year-old male with Aspergillus vertebral osteomyelitis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Lung tissue initially suggested probable Nocardia without pathogenic proof; later spine surgery confirmed Aspergillus hyphae.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 53-year-old male with lung granuloma and vertebral osteomyelitis. Lung specimen initially suggested probable Nocardia without pathogenic proof, but spine histopathology confirmed septate fungal hyphae (Aspergillus) responding to voriconazole. -> NEGATIVE.

## Case 83: `PMC6447646_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 1.58 | Gender: Male (19-month-old male with CGD)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (0 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 19-month-old male evaluated for X-linked CGD due to family history (Burkholderia sepsis in half-brother). Nocardiosis is not mentioned or diagnosed in case_text. -> EXCLUDED_NON_TARGET_CASE.

## Case 84: `PMC7667583_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 84.0 | Gender: Female (84-year-old female on corticosteroids for PMR/GCA)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 84-year-old woman on high-dose corticosteroids with endogenous endophthalmitis, pulmonary opacities, and calf mass. Vitreous culture and calf mass biopsy grew Nocardia nova (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 85: `PMC6501261_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old male with Cladophialophora bantiana brain abscess)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 64-year-old male with Cladophialophora bantiana brain abscess and cavitary left lower lobe pneumonia. Lung biopsy culture and MALDI-TOF MS identified Nocardia araoensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 86: `PMC7451151_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 20.0 | Gender: Female (20-year-old female with intrapulmonary schwannoma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 20-year-old female with primary intrapulmonary schwannoma. BAL cultures were explicitly negative for Nocardia. -> NEGATIVE.

## Case 87: `PMC8167374_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 82.0 | Gender: Female (82-year-old female on IV methylprednisolone for GCA)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 82-year-old female on IV methylprednisolone for GCA with bilateral choroidal abscesses, lung nodules, CNS lesions, and psoas abscess. Three blood cultures confirmed Nocardia cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 88: `PMC4225828_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 46.0 | Gender: Female (46-year-old female post-pterygium surgery)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 46-year-old female with infectious nodular scleritis post-pterygium surgery. Scleral scraping showed Gram-positive beaded branching rods and scleral abscess culture confirmed Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 89: `PMC5760871_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 65.0 | Gender: Female (65-year-old woman with COPD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 65-year-old woman with COPD and multilobar consolidating pneumonia requiring mechanical ventilation. Sputum culture grew Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 90: `PMC5282893_01::Nocardiosis`
- **Step 1 (Document Type):** METHODOLOGICAL_PAPER
- **Step 2 (CCU Type):** ANIMAL_CASE
- **Step 3 (Patient Anchor):** ANIMAL | Age: 0.0 | Gender: Unknown (Four equine Corynebacterium pseudotuberculosis strains)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_HUMAN` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** Genomic analysis of four Corynebacterium pseudotuberculosis strains isolated from horses; Nocardia is mentioned only as a phylogenetic reference in the CMNR group. Non-human genomic study -> EXCLUDED_NON_HUMAN.

## Case 91: `PMC10392123_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 71.0 | Gender: Female (71-year-old woman on high-dose corticosteroids, cyclosporine, and tocilizumab)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 71-year-old immunosuppressed woman with bacteremic pneumonia and empyema. Blood, pleural fluid, and BAL cultures grew modified ZN-positive rods identified by 16S rDNA tNGS as N. kroppenstedtii (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 92: `PMC3463145_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 41.0 | Gender: Male (41-year-old HIV-positive male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 41-year-old HIV-positive male with right temporal brain abscess. Burr hole aspiration cultures grew Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 93: `PMC3463145_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 22.0 | Gender: Male (22-year-old immunocompetent male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 22-year-old male with right temporoccipital brain abscess. Brain abscess cultures grew Nocardia farcinica and CSF cultures were also positive for Nocardia (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 94: `PMC3463145_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 71.0 | Gender: Male (71-year-old male with silicosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 71-year-old male with silicosis and multiple brain abscesses. Frontal lesion biopsy pus cultures grew Nocardia arthritidis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 95: `PMC3463145_04::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 58.0 | Gender: Male (58-year-old male on long-term steroids for sarcoidosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 58-year-old male on long-term steroids with right parietal brain abscess. Craniotomy cultures grew Nocardia cerradoensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 96: `PMC3366756_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 51.0 | Gender: Female (51-year-old previously healthy female tsunami survivor)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 51-year-old tsunami survivor with polymicrobial wound infections who developed a thigh abscess; cultures grew Nocardia africanum (E1 confirmatory), treated with TMP-SMX. VPD satisfied -> POSITIVE.

## Case 97: `PMC10467026_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 59.0 | Gender: Female (59-year-old immunocompetent female with COPD and bronchiectasis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 59-year-old woman with pulmonary Mycobacterium abscessus and cutaneous Nocardia wallacei back abscess. Both abscess tissue and blood mNGS identified N. wallacei (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 98: `PMC10455842_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 54.0 | Gender: Male (54-year-old male with anti-IFN-gamma autoantibodies)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 54-year-old male with anti-IFN-gamma autoantibodies, pulmonary talaromycosis, and brain abscess. Brain tissue showed Gram-positive filamentous bacilli and purulent fluid culture confirmed Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 99: `PMC8461374_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 29.0 | Gender: Female (29-year-old female with newly diagnosed SLE on MMF and prednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 29-year-old female with SLE on immunosuppressants presenting with disseminated abscesses (skin, lung, liver, spleen, kidney, brain). Cultures from sputum, BAL, and skin pustules showed partially acid-fast branching Gram-positive bacilli identified by MALDI-TOF as N. otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 100: `PMC6334373_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 45.0 | Gender: Female (45-year-old female with esophageal actinomycosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 45-year-old female with esophageal stricture caused by Actinomyces. AFB stain was negative, explicitly ruling out Nocardia. -> NEGATIVE.

## Case 101: `PMC4605260_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 71.0 | Gender: Female (71-year-old female with COPD on recurrent oral prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 71-year-old woman with severe COPD and ongoing productive cough/wheezing. AFB sputum culture identified Nocardia cyriacigeorgica (E1 confirmatory), treated with TMP-SMX. VPD satisfied -> POSITIVE.

## Case 102: `PMC4605260_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 68.0 | Gender: Female (68-year-old female with bronchiectasis post breast cancer therapy)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 68-year-old woman with bronchiectasis, new nodular opacities, and intermittent fevers. Sputum cultures grew Nocardia cyriacigeorgica (E1 confirmatory), resolving with TMP-SMX then linezolid/tobramycin. VPD satisfied -> POSITIVE.

## Case 103: `PMC4605260_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 75.0 | Gender: Female (75-year-old woman with COPD and bronchiectasis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 75-year-old woman with COPD, bronchiectasis, and worsening dyspnea/productive cough. Repeated sputum cultures grew Nocardia cyriacigeorgica (E1 confirmatory), improving on 11 months of TMP-SMX. VPD satisfied -> POSITIVE.

## Case 104: `PMC4605260_04::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 77.0 | Gender: Female (77-year-old woman with bronchiectasis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 77-year-old woman with bronchiectasis whose sputum grew multiple organisms including Nocardia nova, but symptoms resolved with levofloxacin alone and she remained asymptomatic without Nocardia treatment (colonization/carriage, not active disease). -> NEGATIVE.

## Case 105: `PMC4998259_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 63.0 | Gender: Male (63-year-old man with nephrotic syndrome on methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 63-year-old man with nephrotic syndrome on steroids and >10 subcutaneous abscesses. Pus cultures from 5 abscesses grew Nocardia confirmed by gene sequencing as N. brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 106: `PMC6083539_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 58.0 | Gender: Male (58-year-old male with orbital and pulmonary actinomycosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 58-year-old male with orbital/pulmonary actinomycosis. Nocardia was excluded by negative modified AFB stain and 16S rDNA confirmed Actinomyces israelii. -> NEGATIVE.

## Case 107: `PMC9422990_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 62.0 | Gender: Male (62-year-old male on dexamethasone after tooth extraction)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 62-year-old male on dexamethasone with multiple brain lesions and pulmonary GGOs. CSF NGS (37,235 reads) and blood NGS (61 reads) detected Nocardia farcinica (E1 confirmatory, coinfection with A. fumigatus/P. jirovecii). VPD satisfied -> POSITIVE.

## Case 108: `PMC3961935_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 60.0 | Gender: Male (60-year-old male with COPD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 60-year-old male with lymphocutaneous thigh ulcers after thorn prick. Modified Kinyoun stain showed acid-fast branching filaments and culture/16S rRNA sequencing at CDC confirmed N. otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 109: `PMC9062894_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 69.0 | Gender: Male (69-year-old male with SLE on prednisolone, tacrolimus, and azathioprine)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 69-year-old male with SLE on immunosuppressants and right parietal brain abscess. Intraoperative puncture fluid culture was Kinyoun-positive and identified by 16S rRNA and MALDI-TOF MS as N. thailandica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 110: `PMC9969748_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 52.0 | Gender: Male (52-year-old man with autoimmune PAP and COVID-19)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 52-year-old man with autoimmune PAP and COVID-19. Specific search for Nocardia in whole lung lavage fluid was negative. -> NEGATIVE.

## Case 111: `PMC3438302_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 79.0 | Gender: Female (79-year-old woman on prednisone for GCA)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 79-year-old woman on prednisone for GCA with left eye endogenous endophthalmitis. Vitreous cultures grew Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 112: `PMC2838367_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 66.0 | Gender: Male (66-year-old male with MGUS and amyloid/non-amyloid deposition)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 66-year-old male with MGUS and pulmonary/cerebral amyloid-like depositions. BAL cultures for Nocardia were negative. -> NEGATIVE.

## Case 113: `PMC5831598_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 68.0 | Gender: Male (68-year-old male renal transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 68-year-old renal transplant recipient with RML pneumonia and hypoxic respiratory failure. Bronchial washing cultures grew branching filamentous bacteria identified by HPLC as Nocardia pseudobrasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 114: `PMC5759803_01::Nocardiosis`
- **Step 1 (Document Type):** METHODOLOGICAL_PAPER
- **Step 2 (CCU Type):** NON_CLINICAL_DOCUMENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 90.0 | Gender: Female (90-year-old female Mycobacterium simiae genomic isolate)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** Genomic study of a Mycobacterium simiae isolate; Nocardia is mentioned solely in comparative microbiology background regarding trehalose dimycolate (TDM). -> EXCLUDED_NON_TARGET_CASE.

## Case 115: `PMC4209706_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 51.0 | Gender: Male (51-year-old male with primary leptomeningeal melanomatosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** True — Brain biopsy pathology initially raised concern for Nocardia asteroides, which was determined to be a contaminant; final diagnosis was primary leptomeningeal melanomatosis.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 51-year-old male with primary leptomeningeal melanomatosis. Initial surgical pathology concern for Nocardia asteroides was determined to be a contaminant. -> NEGATIVE.

## Case 116: `PMC2817494_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 34.0 | Gender: Male (34-year-old male kidney-pancreas transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 34-year-old kidney-pancreas transplant recipient with foot abscess and osteomyelitis. Culture of purulent material identified Nocardia asteroides (E1 confirmatory), resolving on amoxicillin. VPD satisfied -> POSITIVE.

## Case 117: `PMC6416759_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 52.0 | Gender: Female (52-year-old immunocompetent female)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 52-year-old immunocompetent female with right cerebellar abscess. Resected lesion culture showed branching filamentous Gram-positive bacilli identified by 16S rRNA sequencing as N. paucivorans (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 118: `PMC8819730_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 71.0 | Gender: Female (71-year-old woman with nephrotic syndrome on methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 71-year-old woman with nephrotic syndrome on methylprednisolone and left lower lobe pneumonia. BALF modified acid-fast stain, culture, and 16S rRNA sequencing confirmed N. cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 119: `PMC8819730_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 68.0 | Gender: Male (68-year-old man with nephrotic syndrome on prednisone and cyclosporine)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 68-year-old man with nephrotic syndrome on prednisone/cyclosporine and cavitary lung lesions. Sputum isolate was identified by 16S rRNA sequencing as N. brasiliensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 120: `PMC8819730_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 69.0 | Gender: Male (69-year-old man with nephrotic syndrome on prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 69-year-old man with nephrotic syndrome on prednisone with pulmonary nodules/cavities and groin abscess. Both pus and sputum cultures confirmed N. farcinica by gene sequencing (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 121: `PMC9610571_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 51.0 | Gender: Male (51-year-old man with autoimmune hepatitis on prednisolone and azathioprine)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 51-year-old immunosuppressed man with pneumonia and ruptured infected ACA aneurysm. Sputum culture and subdural pus/aneurysm cultures confirmed N. otitidiscaviarum by 16S rRNA sequencing (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 122: `PMC10323790_05::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Unknown (Immunocompetent patient with brain abscess)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** True — Gram stain showed branched Gram-positive bacilli consistent with Nocardia or Actinomyces, but sulfur granules and MALDI-TOF MS culture confirmed Actinomyces israelii and Fusobacterium nucleatum.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** Immunocompetent patient with brain abscess. Direct Gram stain showed branched Gram-positive bacilli resembling Nocardia or Actinomyces, but sulfur granules and MALDI-TOF MS confirmed Actinomyces israelii and Fusobacterium nucleatum. -> NEGATIVE.

## Case 123: `PMC9485662_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 57.0 | Gender: Male (57-year-old man with HBV membranous nephropathy on methylprednisolone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 57-year-old immunosuppressed man with mixed cavitary pulmonary infection (M. tuberculosis, A. fumigatus, N. nova, CMV). Both BALF mNGS (148 reads) and lung tissue biopsy mNGS (92 reads) detected N. nova (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 124: `PMC6535853_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 39.0 | Gender: Male (39-year-old male with open elbow fracture and quadriparesis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 39-year-old man with open elbow fracture-dislocation who developed Nocardia septic arthritis and subsequent Nocardia osteomyelitis of the humerus requiring surgical debridement and IV antibiotics (E2 established clinical diagnosis, specific lab assay not detailed). VPD satisfied -> POSITIVE.

## Case 125: `PMC7171607_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old male with COPD and HCV)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 64-year-old male with COPD exacerbation and CAP. Sputum culture revealed branching filamentous bacilli positive on modified acid-fast stain (1% H2SO4) consistent with Nocardia spp. (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 126: `PMC7171607_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 78.0 | Gender: Male (78-year-old male with uncontrolled T2DM)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 78-year-old male with uncontrolled T2DM and bilateral pulmonary opacities. Sputum showed weak acid-fast filamentous bacilli (standard AFB negative) resembling Nocardia spp. (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 127: `PMC7171607_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 47.0 | Gender: Female (47-year-old female with lung squamous cell carcinoma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 47-year-old female with lung squamous cell carcinoma, bilateral cavitary consolidation, and multiple brain abscesses. Sputum showed weak acid-fast filamentous bacilli resembling Nocardia spp., and final diagnosis was disseminated nocardiosis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 128: `PMC7171607_04::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 62.0 | Gender: Female (62-year-old female with T2DM)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 62-year-old diabetic female with cough and fever. Sputum showed weak acid-fast filamentous bacilli resembling Nocardia spp. (E1 confirmatory), improving on 3 months of TMP-SMX and linezolid. VPD satisfied -> POSITIVE.

## Case 129: `PMC7171607_05::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 73.0 | Gender: Male (73-year-old male with T2DM and prior TB)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 73-year-old diabetic male with fever and dyspnea. Sputum showed branching filaments on modified acid-fast stain and culture/MALDI-TOF identified Nocardia araoensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 130: `PMC9330429_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 3.0 | Gender: Male (3-year-old boy post-ocular trauma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 3-year-old boy with post-traumatic endophthalmitis. Intraocular exudate culture grew dry chalky colonies; MinION WGS, Gram stain, and weak acid-fast stain confirmed Nocardia spp. (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 131: `PMC10248429_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 68.0 | Gender: Male (68-year-old male with lung squamous cell carcinoma and active TB)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 68-year-old male with lung squamous cell carcinoma and subsequent TB. Etiological examination for nocardiosis was explicitly negative. -> NEGATIVE.

## Case 132: `PMC9868268_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 47.0 | Gender: Male (47-year-old male with B-ALL and Enterocytozoon bieneusi microsporidiosis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 47-year-old male with Enterocytozoon bieneusi peritonitis. Nocardia is mentioned solely in the mNGS bioinformatics read-count threshold rule. -> EXCLUDED_NON_TARGET_CASE.

## Case 133: `PMC3697147_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 70.0 | Gender: Male (70-year-old male heart-kidney transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** RECENT_EPISODIC
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 70-year-old heart-kidney transplant recipient with a recent diagnosis of disseminated nocardia actively treated with TMP-SMX and moxifloxacin (E2 established diagnosis under ongoing therapy). VPD satisfied -> POSITIVE.

## Case 134: `PMC3697147_04::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 58.0 | Gender: Male (58-year-old male renal transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 58-year-old renal transplant recipient admitted to ICU with fevers and dyspnea, found to have pseudomonal pneumonia and pulmonary nocardiosis (E2 established clinical diagnosis, specific lab assay not detailed). VPD satisfied -> POSITIVE.

## Case 135: `PMC9251553_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 84.0 | Gender: Female (84-year-old female with Child-Pugh C liver cirrhosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 84-year-old woman with cirrhosis and empyema necessitans. Abscess showed filamentous branching rods on Gram/Kinyoun stain and MALDI-TOF MS identified Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 136: `PMC3395676_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 22.0 | Gender: Male (22-year-old male post-HSCT with Madurella mycetomatis eumycetoma)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 22-year-old male with Madurella mycetomatis foot eumycetoma. Cutaneous nocardiosis is mentioned solely in the general discussion of eumycetoma differential diagnosis. -> EXCLUDED_NON_TARGET_CASE.

## Case 137: `PMC3118057_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 50.0 | Gender: Male (50-year-old male farmer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 50-year-old farmer with right foot actinomycetes mycetoma. Pus smear showed weakly acid-fast branching Gram-positive filamentous bacilli and culture/biochemical testing identified N. asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 138: `PMC9248758_02::Nocardiosis`
- **Step 1 (Document Type):** SYSTEMATIC_REVIEW
- **Step 2 (CCU Type):** AGGREGATE_STUDY_UNIT
- **Step 3 (Patient Anchor):** POPULATION | Age: 35.0 | Gender: Male (Review of ROCM and ENKTL-NT)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** Review/research article on ROCM and ENKTL-NT; Nocardia is mentioned only in literature review citations. Not a single-human-patient Nocardiosis case -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 139: `PMC8573330_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Male (Male patient with CGD and Candida glabrata lymphadenitis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** HISTORICAL_RESOLVED
- **Step 7 (Temporality):** HISTORICAL_RESOLVED
- **Step 8 (Clinical Role):** PAST_HISTORY
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** Male CGD patient evaluated years later for IBD and infliximab-associated complications; Nocardia pneumonia occurred in past medical history at age 15 (historical/resolved, not current active episode). -> NEGATIVE.

## Case 140: `PMC4797532_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 31.0 | Gender: Male (31-year-old immunocompetent male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 31-year-old immunocompetent male with brain abscess after sea-swimming toe cut. Stereotactic pus showed partially acid-fast Gram-positive bacilli and culture/PCR/16S rDNA confirmed N. crassostreae (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 141: `PMC7609154_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 37.0 | Gender: Male (37-year-old immunocompetent male farmer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 37-year-old immunocompetent male with recurrent thoracic empyema. Decortication tissue culture and modified Ziehl-Neelsen stain showed Gram-positive branching acid-fast bacilli consistent with Nocardia species (E1 confirmatory), resolving on imipenem and Bactrim. VPD satisfied -> POSITIVE.

## Case 142: `PMC4617009_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 42.0 | Gender: Male (42-year-old male with PAP)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 42-year-old male with pulmonary alveolar proteinosis and multiple bilateral brain abscesses. Stereotactic brain biopsy smear showed branching filamentous Gram-positive elements and culture grew Nocardia asteroides (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 143: `PMC5838848_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 47.0 | Gender: Female (47-year-old female with intracranial actinomycosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 47-year-old female with intracranial actinomycosis. Acid-fast staining was explicitly negative for Nocardia species, and final diagnosis was Actinomyces-like organisms. -> NEGATIVE.

## Case 144: `PMC5362853_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** ANIMAL_CASE
- **Step 3 (Patient Anchor):** ANIMAL | Age: 9.0 | Gender: Male (9-year-old male neutered domestic shorthair cat)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_HUMAN` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Veterinary case report of a 9-year-old cat with Aelurostrongylus abstrusus verminous pneumonia (acid-fast stain negative for Nocardia). Non-human subject -> EXCLUDED_NON_HUMAN.

## Case 145: `PMC5359233_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 75.0 | Gender: Female (75-year-old healthy woman with CNS Propionibacterium acnes)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Nocardia was covered empirically due to Gram+ filamentous rods on brain biopsy, but AFB was negative and DNA sequencing confirmed Propionibacterium acnes.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 75-year-old woman with multiple CNS lesions. Nocardia was covered empirically, but AFB stain was negative and DNA sequencing confirmed Propionibacterium acnes. -> NEGATIVE.

## Case 146: `PMC5994559_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 28.0 | Gender: Female (Adult female with autosomal-recessive CGD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** Adult female with autosomal-recessive CGD and spinal cord/brainstem meningitis and ventriculitis. CSF PCR detected Nocardia otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 147: `PMC3403161_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 49.0 | Gender: Male (49-year-old male with myasthenia gravis on prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 49-year-old male with myasthenia gravis on prednisone with anterior mediastinal/pericardial abscesses and brain cysts. Pericardiocentesis purulent fluid grew Nocardia asiatica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 148: `PMC8055275_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Male (55-year-old male with nephrotic syndrome on steroid and cyclophosphamide)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 55-year-old male on steroids/cyclophosphamide with right thigh abscesses after thorn injury. Ultrasound-guided aspirated pus identified Nocardia farcinica (E1 confirmatory), resolving on TMP-SMX and linezolid. VPD satisfied -> POSITIVE.

## Case 149: `PMC4904555_01::Nocardiosis`
- **Step 1 (Document Type):** CASE_SERIES
- **Step 2 (CCU Type):** MULTI_PATIENT_CASE_SERIES
- **Step 3 (Patient Anchor):** POPULATION | Age: None | Gender: Female (Five cases of pulmonary nocardiosis (4M, 1F))
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Aggregate summary of a 5-patient case series of pulmonary nocardiosis without separable single-patient narrative. -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 150: `PMC8040973_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 41.0 | Gender: Male (41-year-old male with Cushing's syndrome)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 41-year-old male with Cushing's syndrome, cavitary lung lesions, and brain abscesses. Sputum and percutaneous lung biopsy modified acid-fast stains and cultures grew Nocardia cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 151: `PMC5025916_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Male (55-year-old male with DM and isolated pulmonary candidiasis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 55-year-old male with DM and isolated pulmonary candidiasis. BAL evaluation for Nocardia was explicitly negative. -> NEGATIVE.

## Case 152: `PMC10966995_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 81.0 | Gender: Male (81-year-old man with B-CLL on ibrutinib and Apophysomyces mucormycosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 81-year-old man with B-CLL and Apophysomyces cutaneous mucormycosis. Biopsy cultures for Nocardia were negative. -> NEGATIVE.

## Case 153: `PMC10710253_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 56.0 | Gender: Male (56-year-old male with T2DM and chronic corticosteroid use)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 56-year-old male on chronic corticosteroids with retroperitoneal/pelvic abscesses. CT-guided abscess pus showed modified acid-fast thin branching bacilli and culture/MALDI-TOF MS identified N. farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 154: `PMC10921472_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Male (55-year-old male with Brucella melitensis and Nocardia coinfection)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 55-year-old male with Brucella melitensis bacteremia and bilateral pulmonary nodules/effusion. Deep purulent sputum culture grew Nocardia otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 155: `PMC11333241_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 33.0 | Gender: Male (33-year-old man with hidradenitis suppurativa and Lawsonella clevelandensis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (0 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 33-year-old man with hidradenitis suppurativa and septic shock caused by Lawsonella clevelandensis. Nocardiosis is not mentioned or diagnosed in case_text. -> EXCLUDED_NON_TARGET_CASE.

## Case 156: `PMC10896460_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 75.0 | Gender: Male (75-year-old male with T2DM)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 75-year-old diabetic male with bilateral nodular pneumonia. Sputum modified ZN stain (1% H2SO4) showed beaded branching acid-fast filamentous bacilli and 16S rRNA sequencing identified N. wallacei (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 157: `PMC11032677_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 75.0 | Gender: Male (75-year-old male with granulomatous hepatitis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 75-year-old male with persistent fever, lung nodules, and hepatosplenic lesions. Liver biopsy mNGS identified Nocardia farcinica (E1 confirmatory), with fever controlled by TMP-SMX/amikacin/meropenem. VPD satisfied -> POSITIVE.

## Case 158: `PMC11193390_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 61.0 | Gender: Female (61-year-old immunocompetent female farmer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 61-year-old immunocompetent female with bronchiectasis and pulmonary inflammation. BALF showed beaded Gram-positive filamentous bacteria with weak acid-fast positivity and culture/MALDI-TOF MS identified Nocardia wallacei (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 159: `PMC10858340_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 38.0 | Gender: Male (38-year-old HIV-positive male on steroids)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 38-year-old HIV-positive male on steroids with pleural empyema. Pleural fluid modified ZN stain showed branching acid-fast filaments and culture/MALDI-TOF MS/16S rRNA confirmed Nocardia otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 160: `PMC11045883_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 56.0 | Gender: Male (56-year-old man with IgM kappa PGNMID on prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 56-year-old man on prednisone for IgM kappa PGNMID who developed neck, lumbar, and tibial abscesses. Abscess drainage fluid NGS detected 58,017 Nocardia sequences (E1 confirmatory), resolving on TMP-SMX and minocycline. VPD satisfied -> POSITIVE.

## Case 161: `PMC11370755_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 51.0 | Gender: Male (51-year-old male with anti-synthetase syndrome on methylprednisolone/cyclosporine)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 51-year-old immunosuppressed male with anti-synthetase syndrome and cavitary pneumonia (coinfection with P. jirovecii). BALF mNGS (73,406 reads) and sputum culture confirmed Nocardia terpene (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 162: `PMC10657549_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 71.0 | Gender: Female (71-year-old female with cerebral abscess)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 71-year-old female with left parietal and right frontal cerebral lesions. Resected abscess culture grew weakly acid-fast branching rods and mNGS identified N. gipuzkoensis (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 163: `PMC10832585_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 60.0 | Gender: Female (60-year-old woman 9 years post-pneumonectomy)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 60-year-old woman 9 years post-pneumonectomy with new pleural thickening. VATS pleural cultures grew Nocardia nova (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 164: `PMC10961017_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 1.58 | Gender: Female (19-month-old female child)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 19-month-old girl with febrile watery diarrhea. Fecal smear showed weak acid-fast positivity and Columbia blood agar culture/MALDI-TOF MS + WGS confirmed N. farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 165: `PMC11179430_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 66.0 | Gender: Male (66-year-old man with MCD nephrotic syndrome on prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 66-year-old man on high-dose prednisone with disseminated infection (epididymitis, cavitary pneumonia, skin pustules, brain lesions). CSF culture, skin culture/VITEK MS, and BALF tNGS confirmed N. otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 166: `PMC10702378_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 41.0 | Gender: Male (41-year-old male renal transplant recipient)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 41-year-old renal transplant recipient with progressive bilateral nodular consolidations. Transbronchial lung biopsy showed modified ZN-positive branching filamentous bacilli and culture/MALDI-TOF MS identified N. cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 167: `PMC10481806_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 62.0 | Gender: Female (62-year-old female with cervical tuberculosis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_TARGET_CASE` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** 62-year-old female with cervical tuberculosis (educational quiz). Nocardia is mentioned solely in an answer explanation regarding Ziehl-Neelsen acid concentration. -> EXCLUDED_NON_TARGET_CASE.

## Case 168: `PMC10809415_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 27.0 | Gender: Female (27-year-old immunocompetent female)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 27-year-old immunocompetent woman with a solitary bronchial neoplasm-like nodule causing decubitus dyspnea. Electrotomy biopsy mNGS detected 14,850 reads of Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 169: `PMC10928402_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Male (55-year-old male on hemodialysis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 55-year-old male on hemodialysis with pneumothorax and pleural effusion. Pleural fluid modified ZN stain showed acid-fast branching filaments and culture/VITEK MS confirmed Nocardia otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 170: `PMC11288846_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 60.0 | Gender: Female (60-year-old previously healthy female farmer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 60-year-old immunocompetent female with gingivitis/tonsillitis progressing to severe bilateral pneumonia. BALF smear and culture confirmed Nocardia (E1 confirmatory), resolving on TMP-SMX and meropenem. VPD satisfied -> POSITIVE.

## Case 171: `PMC11378987_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 63.0 | Gender: Male (63-year-old male with Babesia microti and multi-pathogen pneumonia)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 63-year-old male on steroids/cyclosporine for hemophagocytic syndrome with new RUL mass. Sputum mNGS identified Nocardia cyriacigeorgica (E1 confirmatory, coinfection with Babesia microti and P. jirovecii), resolving on TMP-SMX. VPD satisfied -> POSITIVE.

## Case 172: `PMC10550213_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old man with left foot mycetoma caused by Gordonia soli)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Initially presumed Nocardia spp. based on actinomycetoma histopathology with negative cultures; later cultures, MALDI-TOF MS, and 16S rRNA confirmed Gordonia soli.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 64-year-old man with foot mycetoma initially presumed to be Nocardia spp., but later cultures, MALDI-TOF MS, and 16S rRNA sequencing confirmed Gordonia soli. -> NEGATIVE.

## Case 173: `PMC10520695_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 68.0 | Gender: Male (68-year-old male lung transplant recipient post-COVID-19)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 68-year-old lung transplant recipient post-COVID-19 with right lower lobe consolidation. BALF mNGS identified Nocardia farcinica (E1 confirmatory), resolving on linezolid and TMP-SMX. VPD satisfied -> POSITIVE.

## Case 174: `PMC10601863_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 70.0 | Gender: Male (70-year-old immunocompetent male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 70-year-old immunocompetent male with post-traumatic keratitis. Corneal scraping cultures grew dry chalky white colonies with Gram-positive branched filaments and VITEK MS identified N. africana (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 175: `PMC11163097_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 78.0 | Gender: Male (78-year-old immunocompetent male farmer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 78-year-old male with bilateral lung lesions. CT-guided lung puncture pus mNGS and culture identified Nocardia otitidiscaviarum (E1 confirmatory), resolving on TMP-SMX and meropenem. VPD satisfied -> POSITIVE.

## Case 176: `PMC11179496_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 48.0 | Gender: Male (48-year-old immunocompetent male firefighter)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 48-year-old immunocompetent male with forearm pyomyositis after gardening. Both wound pus and deep I&D cultures identified N. brasiliensis by MALDI-TOF MS (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 177: `PMC11806675_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 81.0 | Gender: Male (81-year-old male with COPD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 81-year-old male with COPD and fatal empyema thoracis. Sputum and pleural fluid cultures/MALDI-TOF MS confirmed Nocardia otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 178: `PMC11748329_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Male (55-year-old male with CLL on FCR chemotherapy)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** 55-year-old neutropenic male with CLL and pansinusitis. Sinus biopsy histopathology showed filamentous Gram-positive thin-walled bacteria compatible with Nocardia species (no fungi), completely resolving on co-trimoxazole and meropenem (E2). VPD satisfied -> POSITIVE.

## Case 179: `PMC11702207_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Male (Male patient with newly diagnosed AIDS)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** UNKNOWN
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (0 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `UNRESOLVED` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** Initial presentation excerpt of AIDS/NHL patient; case_text does not mention Nocardia or any Nocardia diagnostic evidence (title-only signal). Insufficient evidence in this chunk -> UNRESOLVED.

## Case 180: `PMC11702207_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Male (Male patient with AIDS)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** UNKNOWN
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (0 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `UNRESOLVED` | Confidence: HIGH | Flags: ['F5_DISCOURSE_CONTEXT']
- **Rationale:** Hospitalization excerpt describing chest CT, negative BM Histoplasma/mycobacteria PCR, and empiric PJP/histoplasmosis treatment without mentioning Nocardia in case_text. Insufficient evidence in this chunk -> UNRESOLVED.

## Case 181: `PMC11702207_03::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: None | Gender: Male (Male patient with AIDS and B-cell NHL)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** Male patient with AIDS and B-cell NHL. Postmortem bone marrow aspirate culture showed partially acid-fast Gram-positive microsiphonated filaments biochemically identified as N. farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 182: `PMC11832390_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 69.0 | Gender: Male (69-year-old man with bronchiectasis and IgA nephropathy on prednisone)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 69-year-old man on prednisone with severe pneumonia. BALF culture grew dry white colonies with Gram-positive weak acid-fast positivity confirmed by VITEK MS as N. otitidiscaviarum (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 183: `PMC11825202_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 69.0 | Gender: Male (69-year-old male with subxiphoid and thigh abscesses)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 69-year-old male with subxiphoid and thigh abscesses. Surgical drainage fluid showed branching filamentous Gram-positive bacilli and MALDI-TOF MS confirmed Nocardia kroppenstedtii (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 184: `PMC11703450_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 19.0 | Gender: Male (19-year-old male with EVALI)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 19-year-old male with EVALI requiring ECMO. BAL microbiological assessment for Nocardia was explicitly negative. -> NEGATIVE.

## Case 185: `PMC11787046_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 33.0 | Gender: Male (33-year-old Colombian male with HIV/AIDS, PJP, and histoplasmosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 33-year-old HIV/AIDS male with extrapulmonary P. jirovecii and Histoplasma capsulatum coinfection. Liver biopsy sent for modified Kinyoun stain/culture for Nocardia had negative bacterial culture and confirmed PJP/histoplasmosis. -> NEGATIVE.

## Case 186: `PMC13034707_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 64.0 | Gender: Male (64-year-old male on chemotherapy for metastatic colorectal adenocarcinoma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 64-year-old immunocompromised man with forearm subcutaneous abscess, pulmonary focus, and brain abscess. Intraoperative forearm abscess cultures identified Nocardia paucivorans (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 187: `PMC12515561_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 43.0 | Gender: Male (43-year-old male with AIDS and disseminated GI Kaposi sarcoma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 43-year-old male with AIDS and disseminated GI Kaposi sarcoma. BAL cultures for Nocardia were explicitly negative. -> NEGATIVE.

## Case 188: `PMC12587269_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 77.0 | Gender: Male (77-year-old male with COPD and pulmonary fibrosis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 77-year-old male with COPD, pulmonary fibrosis, and 10 kg weight loss. BAL culture was positive for N. wallacei (E1 confirmatory), resolving on imipenem/amikacin and moxifloxacin. VPD satisfied -> POSITIVE.

## Case 189: `PMC12275057_01::Nocardiosis`
- **Step 1 (Document Type):** CASE_SERIES
- **Step 2 (CCU Type):** MULTI_PATIENT_CASE_SERIES
- **Step 3 (Patient Anchor):** POPULATION | Age: 90.0 | Gender: Female (Case series of 8 elderly immunocompetent females with Scedosporium)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** HISTORICAL_RESOLVED
- **Step 7 (Temporality):** HISTORICAL_RESOLVED
- **Step 8 (Clinical Role):** PAST_HISTORY
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT']
- **Rationale:** Case series of 8 patients with Scedosporium in respiratory samples (one patient had prior pulmonary nocardiosis, currently Nocardia-negative). Multi-patient case series -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 190: `PMC13168027_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 8.0 | Gender: Female (8-year-old girl with Aggregatibacter actinomycetemcomitans lung infection)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (2 grounded item(s))
- **Step 10 (Contradictions):** True — Nocardia considered in histopathologic differential, but compact sulfur granules favored Actinomyces and cultures/MS/16S rRNA confirmed Aggregatibacter actinomycetemcomitans.
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 8-year-old girl with thoracic mass. Nocardia was excluded by histomorphology (no branching delicate beaded filaments) and 16S rRNA/MS confirmed Aggregatibacter actinomycetemcomitans. -> NEGATIVE.

## Case 191: `PMC12488295_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 43.0 | Gender: Male (43-year-old man with ankylosing spondylitis and anterior opercular syndrome)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** HISTORICAL_RESOLVED
- **Step 7 (Temporality):** HISTORICAL_RESOLVED
- **Step 8 (Clinical Role):** PAST_HISTORY
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL', 'F6_EVIDENCE_SPECIFICITY']
- **Rationale:** 43-year-old man with past history (6 months prior) of suspected cerebral nocardiosis; current blood/CSF cultures were normal and frontal brain biopsy showed only nonspecific inflammatory tissue. -> NEGATIVE.

## Case 192: `PMC13092237_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Male (55-year-old male with history of TB)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 55-year-old male with multiple intracranial ring-enhancing nodules. Blood and CSF NGS identified Nocardia brevicatena (E1 confirmatory), resolving on TMP-SMX, amikacin, and imipenem. VPD satisfied -> POSITIVE.

## Case 193: `PMC12667243_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 55.0 | Gender: Female (55-year-old immunocompetent female)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 55-year-old immunocompetent female presenting with massive hemoptysis and bilateral consolidations/pleural effusion. BALF mNGS and bacterial culture confirmed Nocardia cyriacigeorgica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 194: `PMC12646876_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 52.0 | Gender: Male (52-year-old immunocompetent male)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 52-year-old male with multiple brain abscesses. Stereotactic abscess pus mNGS (1,863 reads), aerobic culture, modified acid-fast stain, and MALDI-TOF MS all confirmed N. asiatica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 195: `PMC13138953_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 60.0 | Gender: Male (60-year-old male with T2DM and DLBCL)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 60-year-old male with pulmonary cavities from diffuse large B-cell lymphoma. BALF cultures for Nocardia were explicitly negative. -> NEGATIVE.

## Case 196: `PMC12681903_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 54.0 | Gender: Female (54-year-old woman with bronchiectasis (30yo in metadata was her son))
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: ['F3_SUBJECT_COREFERENCE']
- **Rationale:** 54-year-old woman with bronchiectasis and multifocal lung consolidation (metadata age 30.0 belonged to her son). Sputum and BAL cultures grew Nocardia sp. classified by 16S rDNA sequencing as Nocardia pneumoniae (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 197: `PMC12681903_05::Nocardiosis`
- **Step 1 (Document Type):** SYSTEMATIC_REVIEW
- **Step 2 (CCU Type):** AGGREGATE_STUDY_UNIT
- **Step 3 (Patient Anchor):** OTHER_HUMAN | Age: 69.0 | Gender: Female (Literature review summary of Nakagoshi et al. case and Table 2)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** HISTORICAL_RESOLVED
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** Literature review excerpt summarizing a previously published case (Nakagoshi et al.) and Table 2 of all N. pneumoniae cases, not a primary single-patient case report. -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 198: `PMC13043398_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 50.0 | Gender: Female (50-year-old woman with immunotherapy-induced pneumonitis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 50-year-old woman with steroid-refractory immunotherapy-induced pneumonitis. Bronchoscopy testing for Nocardia species was explicitly negative. -> NEGATIVE.

## Case 199: `PMC12870019_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 79.0 | Gender: Male (79-year-old man with COPD and large B-cell lymphoma)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** ACTIVE_COMORBIDITY
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 79-year-old man with COPD and large B-cell lymphoma presenting with brain lesions, lung nodule, and splenic mass. Splenic aspiration and brain biopsy cultures grew filamentous branching N. ignorata identified by MALDI-TOF MS (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 200: `PMC13161159_02::Nocardiosis`
- **Step 1 (Document Type):** SYSTEMATIC_REVIEW
- **Step 2 (CCU Type):** AGGREGATE_STUDY_UNIT
- **Step 3 (Patient Anchor):** POPULATION | Age: 1.0 | Gender: Unknown (Review of nasal-oral microbiome axis in allergic rhinitis)
- **Step 4–5 (Mentions & Concept Grounding):** NON_TARGET_ENTITY
- **Step 6 (Assertion):** UNMENTIONED
- **Step 7 (Temporality):** UNKNOWN
- **Step 8 (Clinical Role):** EPIDEMIOLOGICAL_CONTEXT
- **Step 9 (Evidence Strength):** E4_BACKGROUND_OR_CONTEXT_ONLY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `EXCLUDED_NON_SINGLE_PATIENT` | Confidence: HIGH | Flags: ['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']
- **Rationale:** Review article on the nasal-oral microbiome axis in allergic rhinitis; Nocardia coeliaca is mentioned solely as a normal nasal commensal in a 32-subject microbiome study. -> EXCLUDED_NON_SINGLE_PATIENT.

## Case 201: `PMC12863413_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 86.0 | Gender: Female (86-year-old female on oral prednisone for Sjogren's/ILD)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (2 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 86-year-old female on prednisone with bilateral chorioretinitis/endophthalmitis, 6 brain lesions, and gluteal/paraspinal abscesses. Gluteal abscess culture identified Nocardia farcinica (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 202: `PMC12854188_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 56.0 | Gender: Male (56-year-old male with disseminated tuberculous myositis)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** ABSENT_NEGATIVE
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** RULED_OUT_DIAGNOSIS
- **Step 9 (Evidence Strength):** E0_CONTRADICTED (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** False
- **Step 12 (Final Dataset Label):** `NEGATIVE` | Confidence: HIGH | Flags: ['F4_ASSERTION_TEMPORAL']
- **Rationale:** 56-year-old male with disseminated tuberculous pyomyositis. Modified ZN staining and cultures for Nocardia were negative, while CBNAAT, LPA, and culture confirmed Mycobacterium tuberculosis. -> NEGATIVE.

## Case 203: `PMC12375495_01::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 67.0 | Gender: Male (67-year-old immunocompetent male bricklayer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E1_DISEASE_SPECIFIC_CONFIRMATORY (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: HIGH | Flags: []
- **Rationale:** 67-year-old immunocompetent bricklayer with bilateral frontal lesions and purulent meningitis after thigh laceration. CSF mNGS detected Nocardia otitidiscaviarum (82 reads) (E1 confirmatory). VPD satisfied -> POSITIVE.

## Case 204: `PMC12375495_02::Nocardiosis`
- **Step 1 (Document Type):** CLINICAL_CASE_REPORT
- **Step 2 (CCU Type):** SINGLE_HUMAN_PATIENT
- **Step 3 (Patient Anchor):** PRIMARY_PATIENT | Age: 67.0 | Gender: Male (67-year-old immunocompetent male bricklayer)
- **Step 4–5 (Mentions & Concept Grounding):** TARGET_CONFIRMED
- **Step 6 (Assertion):** AFFIRMED
- **Step 7 (Temporality):** CURRENT_ACTIVE
- **Step 8 (Clinical Role):** PRIMARY_DIAGNOSIS
- **Step 9 (Evidence Strength):** E2_HIGHLY_CHARACTERISTIC (1 grounded item(s))
- **Step 10 (Contradictions):** False 
- **Step 11 (VPD Satisfied):** True
- **Step 12 (Final Dataset Label):** `POSITIVE` | Confidence: MEDIUM | Flags: []
- **Rationale:** Continuation of 67-year-old bricklayer case explicitly stating definitive diagnosis of Nocardia otitidiscaviarum-induced purulent meningitis based on CSF routine and mNGS findings, with full clinical/MRI/CSF recovery after 12 months of TMP-SMX/linezolid therapy (E2). VPD satisfied -> POSITIVE.


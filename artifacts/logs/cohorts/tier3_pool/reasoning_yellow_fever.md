# Clinical Claim Annotation Reasoning Log: Yellow_Fever (`tier3_pool`)

**Target Disease:** `Yellow_Fever`  
**Total Candidate Pairs Evaluated:** `19`  
**Annotator ID:** `disease-agent-yellow_fever`  
**Protocol Version:** `1.0` (12-Step Clinical Gold Standard Annotation Protocol)  

## Executive Summary & Distribution of Adjudications

| Metric / Label Category | Prompt `decision` Count | SKILL `step12_dataset_label` Count | Case IDs |
| :--- | :---: | :---: | :--- |
| **Valid Positive Diagnosis (`POSITIVE`)** | 0 | 0 | None |
| **Explicitly Tested Negative / Ruled Out (`NEGATIVE`)** | 8 | 8 | `PMC5176231_01`, `PMC4662510_01`, `PMC5529618_01`, `PMC4085831_01`, `PMC2732535_01`, `PMC5956635_01`, `PMC6884810_01`, `PMC11769472_01` |
| **Non-Target / Vaccination / Remote History (`EXCLUDED_NON_TARGET_CASE`)** | 8 | 8 | `PMC5748105_01`, `PMC5748105_02`, `PMC10169240_01`, `PMC5388347_01`, `PMC5485372_01`, `PMC6180980_01`, `PMC10313350_01`, `PMC10481985_01` |
| **Non-Case Report / Aggregate Study (`EXCLUDED_NON_CASE_REPORT` / `EXCLUDED_NON_SINGLE_PATIENT`)** | 3 | 3 | `PMC9474833_01`, `PMC7078104_02`, `PMC11131420_01` |
| **Inconclusive / Unresolved (`INCONCLUSIVE_DATA` / `UNRESOLVED`)** | 0 | 0 | None |

## Summary Table of All 19 Candidate Pairs

| # | Pair ID | Primary Confirmed Condition / Document Topic | Yellow Fever Context in Text | Evidence Tier | Final `decision` | `step12_dataset_label` |
| :-: | :--- | :--- | :--- | :---: | :---: | :---: |
| 1 | `PMC5176231_01::Yellow_Fever` | Persistent Zika Virus Detection in Semen in a Traveler Returning ... | Yellow fever virus infection (serologic workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 2 | `PMC5748105_01::Yellow_Fever` | Emergence of Lassa Fever Disease in Northern Togo: Report of Two ... | Yellow fever vaccination history | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 3 | `PMC5748105_02::Yellow_Fever` | Emergence of Lassa Fever Disease in Northern Togo: Report of Two ... | Yellow fever vaccination history | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 4 | `PMC10169240_01::Yellow_Fever` | Severe Malaria with a Rare Tetrad of Blackwater Fever, Acute Rena... | Pretravel yellow fever prophylaxis/vaccination status | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 5 | `PMC9474833_01::Yellow_Fever` | Use of mobile medical teams to fill critical gaps in health servi... | Population-level suspected yellow fever outbreak investigation in Nzara County | `E4_CONTEXT` | `EXCLUDED_NON_CASE_REPORT` | `EXCLUDED_NON_SINGLE_PATIENT` |
| 6 | `PMC4662510_01::Yellow_Fever` | Pox-like lesions and haemorrhagic fever in two concurrent cases i... | Yellow Fever virus infection (hemorrhagic fever differential workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 7 | `PMC5388347_01::Yellow_Fever` | First case of imported chikungunya infection in Croatia, 2016... | Prior yellow fever vaccination and postvaccinal YFV IgG antibodies | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 8 | `PMC5529618_01::Yellow_Fever` | Fulminant Myocarditis Managed by Extracorporeal Life Support (Imp... | Yellow fever virus (broad viral myocarditis etiology workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 9 | `PMC5485372_01::Yellow_Fever` | Chorea and tick-borne encephalitis, Poland... | Absence of yellow fever vaccination history (flavivirus cross-reactivity exclusion context) | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 10 | `PMC4085831_01::Yellow_Fever` | First case of autochthonous human visceral leishmaniasis in the u... | Yellow fever (differential diagnosis and serologic workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 11 | `PMC6180980_01::Yellow_Fever` | A Case of Malaria Predisposing to Salmonella Bacteremia in a Retu... | Prior yellow fever vaccination history | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 12 | `PMC2732535_01::Yellow_Fever` | First documentation of human Crimean-Congo hemorrhagic fever, Ken... | Yellow fever virus (IgM capture ELISA and flavivirus RT-PCR in VHF workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 13 | `PMC7078104_02::Yellow_Fever` | BCG as a Case Study for Precision Vaccine Development: Lessons Fr... | Yellow fever live-attenuated vaccine human challenge model in BCG trained immunity studies | `E4_CONTEXT` | `EXCLUDED_NON_CASE_REPORT` | `EXCLUDED_NON_SINGLE_PATIENT` |
| 14 | `PMC5956635_01::Yellow_Fever` | First report of African tick-bite fever in a South American trave... | Yellow fever serology (acute febrile traveler differential workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 15 | `PMC10313350_01::Yellow_Fever` | Case report: Injected corticosteroids for treating leprosy isolat... | Remote past medical history of yellow fever (4 years previously) | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 16 | `PMC6884810_01::Yellow_Fever` | Dengue fever and chikungunya virus infections: identification in ... | Yellow fever virus (IgM capture ELISA and flavivirus RT-PCR in arboviral workup, plus prior travel vaccination) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |
| 17 | `PMC10481985_01::Yellow_Fever` | Reply to Letter to Editor: Unilateral Acute Central Serous Chorio... | Literature background mention of yellow fever vaccination associated with central serous chorioretinopathy | `E4_CONTEXT` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` |
| 18 | `PMC11131420_01::Yellow_Fever` | Presidents and vaccines: head of state inoculation as a tool for ... | Household childhood yellow fever vaccination rate in a survey cohort | `E4_CONTEXT` | `EXCLUDED_NON_CASE_REPORT` | `EXCLUDED_NON_SINGLE_PATIENT` |
| 19 | `PMC11769472_01::Yellow_Fever` | Acute Febrile Illness Accompanied by 7th and 12th Cranial Nerve P... | Yellow Fever serology (post-travel febrile and cranial neuropathy differential workup) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` |

## Case-by-Case 12-Step Clinical Reasoning Process

### Case 1: `PMC5176231_01::Yellow_Fever`

- **Article Title:** Persistent Zika Virus Detection in Semen in a Traveler Returning to the United Kingdom from Brazil, 2016
- **Journal / Year / DOI:** *Emerg Infect Dis* (2017) | DOI: `10.3201/eid2301.161300`
- **Input Metadata Demographics:** Age: `45.0`, Gender: `Male`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report describing a 45-year-old male traveler returning from Brazil to the UK.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 45-year-old male traveler (primary patient; his partner remained well and was not tested).
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever virus infection (serologic workup)`):** Yellow fever is mentioned in the acute arboviral serologic workup ('Results of serologic testing for chikungunya, dengue, and yellow fever were negative by commercial assays.').
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to true Yellow Fever virus infection evaluated via serology (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED because commercial serologic testing for yellow fever was explicitly negative.
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE (diagnostic testing performed during the current acute febrile illness).
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET. Primary confirmed diagnosis is Zika virus infection.
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength for Yellow Fever is E0_CONTRADICTED based on negative commercial serologic assays and confirmation of an alternative flavivirus etiology (Zika virus RNA in urine and semen plus Zika IgM/IgG seroconversion).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction regarding Yellow Fever status; all testing consistently rules out Yellow Fever.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (assertion is negated, role is ruled-out diagnosis, evidence is E0_CONTRADICTED).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[649:755]`
  - **Quote:** "Results of serologic testing for chikungunya, dengue, and yellow fever were negative by commercial assays."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Commercial serologic assay for Yellow fever`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 2:** `case_text[458:536]`
  - **Quote:** "On day 3 of his illness, Zika virus RNA was detected in urine but not in serum"
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Zika virus RNA RT-PCR`, `target_concept=Zika virus`, `specimen=urine`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 45-year-old man returning to the UK from Brazil presented with fever, retro-orbital headache, arthralgia, myalgia, and rash. Commercial serologic testing for yellow fever on day 3 was explicitly negative, whereas Zika virus RNA was detected in urine and serial semen samples (up to day 92) with Zika IgM/IgG seroconversion at day 20. Yellow fever was ruled out in the differential workup -> NEGATIVE.

### Case 2: `PMC5748105_01::Yellow_Fever`

- **Article Title:** Emergence of Lassa Fever Disease in Northern Togo: Report of Two Cases in Oti District in 2016
- **Journal / Year / DOI:** *Case Rep Infect Dis* (2017) | DOI: `10.1155/2017/8242313`
- **Input Metadata Demographics:** Age: `47.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Clinical case report describing the first of two linked Lassa fever cases in northern Togo.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 47-year-old male surgeon at Hopital de l'Esperance in northern Togo.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever vaccination history`):** Yellow fever is mentioned once in the clinical history: 'He was vaccinated against yellow fever.'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to prophylactic immunization (PREVENTION_VACCINATION), not wild-type Yellow Fever infection.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** No claim of Yellow Fever disease is asserted (ABSENT_NEGATIVE / NEGATED for infection; affirmative only for prior vaccine receipt).
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality of the vaccination is HISTORICAL_PAST.
8. **Step 8 — Clinical Role & Case Definition (`PREVENTION_VACCINATION` / `NOT_MET`):** Clinical role is PREVENTION_VACCINATION; Case definition for Yellow Fever is NOT_MET. Primary diagnosis is Lassa fever (confirmed by postmortem PCR) with malaria co-detection on thick smear.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (background immunization history only, zero patient-level diagnostic evidence for Yellow Fever).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (vaccination is never a positive disease claim).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[197:236]`
  - **Quote:** "He was vaccinated against yellow fever."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Vaccination history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=POSITIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[1361:1459]`
  - **Quote:** "A postmortem diagnosis of Lassa fever was confirmed by polymerase chain reaction (PCR) in Germany."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Lassa fever virus PCR`, `target_concept=Lassa fever virus`, `specimen=blood/tissue (postmortem)`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 47-year-old male surgeon in northern Togo presented with persistent febrile illness, abdominal pain, leukopenia, thrombocytopenia, and hemorrhage, and was diagnosed postmortem with Lassa fever by PCR in Germany (with initial thick smear positive for malaria). Yellow fever is mentioned solely as prior vaccination history ('He was vaccinated against yellow fever.'). Per protocol, vaccination history (PREVENTION_VACCINATION) does not constitute a clinical claim of Yellow Fever disease -> EXCLUDED_NON_TARGET_CASE.

### Case 3: `PMC5748105_02::Yellow_Fever`

- **Article Title:** Emergence of Lassa Fever Disease in Northern Togo: Report of Two Cases in Oti District in 2016
- **Journal / Year / DOI:** *Case Rep Infect Dis* (2017) | DOI: `10.1155/2017/8242313`
- **Input Metadata Demographics:** Age: `33.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Clinical case report describing the second of two linked Lassa fever cases in northern Togo.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 33-year-old male healthcare worker who cared for the index surgeon.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever vaccination history`):** Yellow fever is mentioned once: 'He was vaccinated against yellow fever.'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to prior prophylactic vaccination (PREVENTION_VACCINATION), not Yellow Fever disease.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion for Yellow Fever infection is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality of vaccination is HISTORICAL_PAST.
8. **Step 8 — Clinical Role & Case Definition (`PREVENTION_VACCINATION` / `NOT_MET`):** Clinical role is PREVENTION_VACCINATION; Case definition is NOT_MET. Primary confirmed diagnosis is Lassa fever (RT-PCR positive on day 5 blood sample).
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (immunization history only).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[264:303]`
  - **Quote:** "He was vaccinated against yellow fever."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Vaccination history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=POSITIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[1329:1500]`
  - **Quote:** "A reverse transcriptase polymerase chain reaction (RT-PCR) assay was performed on the blood sample on day 5 after onset, which confirmed the presence of Lassa fever virus."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Lassa fever virus RT-PCR`, `target_concept=Lassa fever virus`, `specimen=blood`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 33-year-old male healthcare worker who cared for the index Lassa fever patient in Togo developed fever, chills, abdominal pain, severe transaminitis, thrombocytopenia, and renal impairment. Blood RT-PCR on day 5 confirmed Lassa fever virus, and he recovered following IV ribavirin therapy and evacuation to Atlanta. Yellow fever is mentioned only as prior immunization ('He was vaccinated against yellow fever.'). Because vaccination history (PREVENTION_VACCINATION) is not a clinical disease claim, the case is adjudicated as EXCLUDED_NON_TARGET_CASE.

### Case 4: `PMC10169240_01::Yellow_Fever`

- **Article Title:** Severe Malaria with a Rare Tetrad of Blackwater Fever, Acute Renal Failure, Disseminated Intravascular Coagulopathy, and Acute Acalculous Cholecystitis
- **Journal / Year / DOI:** *Case Rep Infect Dis* (2023) | DOI: `10.1155/2023/5796881`
- **Input Metadata Demographics:** Age: `24.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of severe malaria and blackwater fever in a returning traveler.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 24-year-old African American male traveler returning from Sierra Leone.
4. **Step 4 — Disease Mentions & Condition Matched (`Pretravel yellow fever prophylaxis/vaccination status`):** Yellow fever is mentioned once in pretravel history: 'He did not receive pretravel prophylaxis against malaria, hepatitis A, or yellow fever.'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to absence of pretravel immunization (PREVENTION_VACCINATION), not a clinical claim of Yellow Fever disease.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality is HISTORICAL_PAST (pretravel preparation prior to illness).
8. **Step 8 — Clinical Role & Case Definition (`PREVENTION_VACCINATION` / `NOT_MET`):** Clinical role is PREVENTION_VACCINATION / EPIDEMIOLOGICAL_CONTEXT; Case definition is NOT_MET. Primary confirmed diagnosis is severe P. falciparum malaria.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (background pretravel vaccination status only).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[665:752]`
  - **Quote:** "He did not receive pretravel prophylaxis against malaria, hepatitis A, or yellow fever."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Pretravel vaccination/prophylaxis history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=NEGATIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[1274:1413]`
  - **Quote:** "A blood smear revealed ring-shaped trophozoites consistent with Plasmodium falciparum with a blood parasitemia percentage of 1% (Figure 1)."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Peripheral blood smear`, `target_concept=Plasmodium falciparum`, `specimen=blood`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 24-year-old male returning from Sierra Leone presented with severe Plasmodium falciparum malaria complicated by blackwater fever, acute renal failure, DIC, and acalculous cholecystitis, confirmed by peripheral blood smear (parasitemia peaking at 9%). Yellow fever is mentioned solely in the pretravel history ('He did not receive pretravel prophylaxis against malaria, hepatitis A, or yellow fever.'). No clinical suspicion or diagnostic testing for Yellow Fever was performed -> EXCLUDED_NON_TARGET_CASE.

### Case 5: `PMC9474833_01::Yellow_Fever`

- **Article Title:** Use of mobile medical teams to fill critical gaps in health service delivery in complex humanitarian settings, 2017-2020: a case study of South Sudan
- **Journal / Year / DOI:** *Pan Afr Med J* (2022) | DOI: `10.11604/pamj.supp.2022.42.1.33865`
- **Input Metadata Demographics:** Age: `5.0`, Gender: `Unknown`
- **Final Decision (`decision`):** `EXCLUDED_NON_CASE_REPORT`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_SINGLE_PATIENT`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`EXCLUDED_NON_CASE_REPORT` / `AGGREGATE_COHORT`):** Public health programmatic case study / aggregate review (EXCLUDED_NON_CASE_REPORT / AGGREGATE_COHORT), not a clinical case report.
2. **Step 2 — CCU Type (`AGGREGATE_STUDY_UNIT`):** Unit of analysis is AGGREGATE_STUDY_UNIT (320,988 consultations across 38 counties in South Sudan). Per Step 2 rule, non-single-patient documents are excluded.
3. **Step 3 — Patient Anchor (`none`):** No individual patient anchor ('none'); the input metadata age=5.0 was spuriously extracted from 'under-5-year-old children'.
4. **Step 4 — Disease Mentions & Condition Matched (`Population-level suspected yellow fever outbreak investigation in Nzara County`):** Yellow fever is mentioned once in passing regarding team deployments: 'deployed to investigate suspected outbreaks of cholera in Pibor and Kapoeta East Counties, yellow fever in Nzara County...'
5. **Step 5 — Concept Grounding (`EPIDEMIOLOGICAL_CONTEXT`):** Concept is population-level epidemiological outbreak surveillance (EPIDEMIOLOGICAL_CONTEXT).
6. **Step 6 — Assertion Assessment (`SUSPECTED_POSSIBLE` / `POSSIBLE_HYPOTHETICAL`):** Assertion is SUSPECTED_POSSIBLE / POSSIBLE_HYPOTHETICAL at the county outbreak level, with no patient-level claim.
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality is HISTORICAL_PAST (2017-2020 program review).
8. **Step 8 — Clinical Role & Case Definition (`EPIDEMIOLOGICAL_CONTEXT` / `NOT_MET`):** Clinical role is EPIDEMIOLOGICAL_CONTEXT; Case definition is NOT_MET.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (background programmatic summary only).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (not a single human patient).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[10774:11000]`
  - **Quote:** "The eMMTs have been deployed to investigate suspected outbreaks of cholera in Pibor and Kapoeta East Counties, yellow fever in Nzara County, and Rift Valley fever in Yirol East County, measles and COVID-19 in several counties."
  - **Parameters:** `patient_anchor_id=none`, `test_name=Outbreak investigation summary`, `target_concept=Yellow fever`, `specimen=None`, `result=INCONCLUSIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> This article is a public health programmatic review of World Health Organization emergency mobile medical teams (eMMTs) in South Sudan from 2017 to 2020 (covering 320,988 consultations across 38 counties), not an individual clinical case report. Yellow fever is mentioned once as a population-level deployment ('deployed to investigate suspected outbreaks of... yellow fever in Nzara County'). Because there is no single human patient CCU, it is adjudicated as EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 6: `PMC4662510_01::Yellow_Fever`

- **Article Title:** Pox-like lesions and haemorrhagic fever in two concurrent cases in the Central African Republic: case investigation and management in difficult circumstances
- **Journal / Year / DOI:** *Pan Afr Med J* (2015) | DOI: `10.11604/pamj.2015.22.23.6620`
- **Input Metadata Demographics:** Age: `28.0`, Gender: `Male`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_SERIES`):** Clinical case report describing two concurrent adult male patients with pox-like lesions and hemorrhagic manifestations in the Central African Republic.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Individual patient care episode(s) evaluated at the patient level (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_2`):** patient_1 (28-year-old man) and patient_2 (26-year-old male farmer); the explicit Yellow Fever exclusion statement appears in the workup of patient_2.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow Fever virus infection (hemorrhagic fever differential workup)`):** Yellow Fever is mentioned in the reference laboratory workup: 'Filo-, Yellow Fever and Dengue virus infections were ruled out.'
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to true Yellow Fever virus infection (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED ('ruled out').
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET.
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED (reference laboratory exclusion of Yellow Fever virus infection).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction regarding Yellow Fever exclusion.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (explicitly ruled out).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[5404:5467]`
  - **Quote:** "Filo-, Yellow Fever and Dengue virus infections were ruled out."
  - **Parameters:** `patient_anchor_id=patient_2`, `test_name=Reference laboratory viral hemorrhagic fever testing`, `target_concept=Yellow fever virus`, `specimen=blood`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`

#### Clinical Synthesis Rationale

> This report describes two concurrent adult males (ages 28 and 26) in the Central African Republic presenting with fever, myalgia, vesiculo-bullous skin lesions, and transient hemorrhage (epistaxis, hematemesis/bloody stools). Because hemorrhagic fever etiologies were considered alongside suspected monkeypox, blood samples were sent to the reference laboratory in Bangui, where 'Filo-, Yellow Fever and Dengue virus infections were ruled out.' Yellow Fever was explicitly excluded -> NEGATIVE.

### Case 7: `PMC5388347_01::Yellow_Fever`

- **Article Title:** First case of imported chikungunya infection in Croatia, 2016
- **Journal / Year / DOI:** *Int Med Case Rep J* (2017) | DOI: `10.2147/IMCRJ.S130210`
- **Input Metadata Demographics:** Age: `27.0`, Gender: `Female`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT, F6_EVIDENCE_SPECIFICITY`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of imported Chikungunya fever in Croatia.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 27-year-old female cruise ship stewardess returning from Costa Rica.
4. **Step 4 — Disease Mentions & Condition Matched (`Prior yellow fever vaccination and postvaccinal YFV IgG antibodies`):** Yellow fever is mentioned in the vaccination history ('Six months before this illness, she was vaccinated against yellow fever.') and in the arboviral cross-reactivity serology panel ('postvaccinal YFV IgG antibodies were found (titer 100)').
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept grounding: Both mentions reflect prior immunization (PREVENTION_VACCINATION) and expected vaccine-induced IgG seropositivity, not wild-type Yellow Fever infection.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion for wild-type Yellow Fever disease is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality of vaccination is HISTORICAL_PAST (6 months prior to illness).
8. **Step 8 — Clinical Role & Case Definition (`PREVENTION_VACCINATION` / `NOT_MET`):** Clinical role is PREVENTION_VACCINATION; Case definition is NOT_MET. Primary confirmed diagnosis is chronic Chikungunya infection.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT. As emphasized in Section 5.15 of the Evidence Specificity Matrix, yellow fever vaccination produces IgG antibodies; here the authors explicitly identify the YFV IgG titer of 1:100 as postvaccinal.
10. **Step 10 — Contradiction Reconciliation (`NONE`):** Potential serological confounder (YFV IgG reactivity) is explicitly resolved in the text as postvaccinal immunity from immunization 6 months earlier.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[294:366]`
  - **Quote:** "Six months before this illness, she was vaccinated against yellow fever."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Vaccination history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=POSITIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[3562:3729]`
  - **Quote:** "CHIKV IgM and IgG antibodies were detected with titre 1:100 and 1:10,000, respectively (Figure 2). In addition, postvaccinal YFV IgG antibodies were found (titer 100)."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Indirect immunofluorescence assay (IFA) for YFV and CHIKV IgM/IgG`, `target_concept=Yellow fever virus postvaccinal IgG`, `specimen=serum`, `result=REACTIVE`, `temporality=HISTORICAL_PAST`, `relation=REFUTES`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> A 27-year-old female stewardess returning to Croatia from Costa Rica presented with fever, rash, and persistent symmetric polyarthralgia, confirmed as imported Chikungunya infection (CHIKV IgM 1:100, IgG 1:10,000). She had been vaccinated against yellow fever 6 months prior, and arboviral cross-reactivity testing detected 'postvaccinal YFV IgG antibodies (titer 100)' without acute YFV infection. Per Section 5.15 ('Critical vaccination confounder') and Rule 4 ('Vaccination is never a POSITIVE case'), vaccine-induced IgG represents PREVENTION_VACCINATION -> EXCLUDED_NON_TARGET_CASE.

### Case 8: `PMC5529618_01::Yellow_Fever`

- **Article Title:** Fulminant Myocarditis Managed by Extracorporeal Life Support (Impella® CP): A Rare Case
- **Journal / Year / DOI:** *Case Rep Cardiol* (2017) | DOI: `10.1155/2017/9231959`
- **Input Metadata Demographics:** Age: `49.0`, Gender: `Female`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of fulminant myocarditis managed with Impella CP.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 49-year-old female with cardiogenic shock and cardiac arrest.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever virus (broad viral myocarditis etiology workup)`):** Yellow fever virus is listed among the viral pathogens tested in blood and myocardial biopsy specimens.
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to Yellow fever virus (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED ('none of these triggers was detected'; 'demonstrated absence of infectious causative organisms').
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET.
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED (viral testing in EDTA blood and RNA-stabilized endomyocardial biopsy was negative for yellow fever virus).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[1132:1659]`
  - **Quote:** "Blood and biopsy specimens were tested for common causative agents, such as Coxsackieviruses A and B, echoviruses, polioviruses, influenza A and B viruses, respiratory syncytial virus, mumps virus, measles virus, rubella virus, hepatitis C virus, dengue virus, yellow fever virus, Chikungunya virus, human immunodeficiency virus-1, adenoviruses, parvovirus B19, cytomegalovirus, human herpes virus-6, Epstein-Barr virus, varicella-zoster virus, and herpes simplex virus, as recommended, but none of these triggers was detected."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Viral PCR / microbiological panel on blood and endomyocardial biopsy`, `target_concept=Yellow fever virus`, `specimen=blood and endomyocardial biopsy`, `result=NOT_DETECTED`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 2:** `case_text[1897:2061]`
  - **Quote:** "Viral PCR (polymerase chain reaction) in RNA-stabilized EMB and EDTA (ethylenediaminetetraacetic acid) blood demonstrated absence of infectious causative organisms."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Viral PCR`, `target_concept=Infectious viral agents including Yellow fever virus`, `specimen=RNA-stabilized endomyocardial biopsy and EDTA blood`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`

#### Clinical Synthesis Rationale

> A 49-year-old woman presented with fulminant lymphocytic myocarditis and cardiogenic shock requiring Impella CP support. Blood and endomyocardial biopsy specimens were tested by viral PCR for a broad panel of pathogens including yellow fever virus, and 'none of these triggers was detected.' Because yellow fever virus was explicitly tested and negative, the case is adjudicated as NEGATIVE.

### Case 9: `PMC5485372_01::Yellow_Fever`

- **Article Title:** Chorea and tick-borne encephalitis, Poland
- **Journal / Year / DOI:** *Emerg Infect Dis* (2013) | DOI: `10.3201/eid1909.130804`
- **Input Metadata Demographics:** Age: `38.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of chorea complicating tick-borne encephalitis in Poland.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 38-year-old male forest worker in Bialystok, Poland.
4. **Step 4 — Disease Mentions & Condition Matched (`Absence of yellow fever vaccination history (flavivirus cross-reactivity exclusion context)`):** Yellow fever is mentioned once in the discussion of flavivirus serologic specificity: 'Because of his religious beliefs, the patient had not been vaccinated against TBE or yellow fever; he had not traveled abroad and had not been exposed to dengue virus.'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to prior vaccination status (PREVENTION_VACCINATION) used as background to rule out flavivirus cross-reactivity.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality is HISTORICAL_PAST.
8. **Step 8 — Clinical Role & Case Definition (`PREVENTION_VACCINATION` / `NOT_MET`):** Clinical role is PREVENTION_VACCINATION / EPIDEMIOLOGICAL_CONTEXT; Case definition is NOT_MET. Primary confirmed diagnosis is tick-borne encephalitis (TBE).
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (background vaccination/travel history only).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[2934:3101]`
  - **Quote:** "Because of his religious beliefs, the patient had not been vaccinated against TBE or yellow fever; he had not traveled abroad and had not been exposed to dengue virus."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Vaccination and travel history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=NEGATIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[2623:2843]`
  - **Quote:** "The diagnosis was confirmed with serologic test results, which were strongly positive in serum and CSF, and virus neutralization testing performed as described in Stiasny et al. showed a strongly positive titer of 1:320."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=TBE virus serology and virus neutralization test`, `target_concept=Tick-borne encephalitis virus`, `specimen=serum and CSF`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 38-year-old male forest worker in Poland developed meningoencephalitis and chorea due to tick-borne encephalitis (TBE), confirmed by CSF/serum IgM and IgG and a TBE virus neutralization titer of 1:320. Yellow fever is mentioned solely to document the absence of prior flavivirus vaccination ('the patient had not been vaccinated against TBE or yellow fever; he had not traveled abroad'). There is no clinical claim or diagnostic testing for Yellow Fever -> EXCLUDED_NON_TARGET_CASE.

### Case 10: `PMC4085831_01::Yellow_Fever`

- **Article Title:** First case of autochthonous human visceral leishmaniasis in the urban center of Rio de Janeiro: case report
- **Journal / Year / DOI:** *Rev Inst Med Trop Sao Paulo* (2014) | DOI: `10.1590/S0036-46652014000100013`
- **Input Metadata Demographics:** Age: `29.0`, Gender: `Female`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL, F6_EVIDENCE_SPECIFICITY`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of autochthonous visceral leishmaniasis in urban Rio de Janeiro.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 29-year-old female resident of Rio de Janeiro working at Caju cemetery.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever (differential diagnosis and serologic workup)`):** Yellow fever is mentioned twice in the diagnostic workup paragraph: as a secondary diagnostic hypothesis ('Other hypotheses covered dengue, yellow fever...') and in the ordered serologic panel ('serology for dengue, yellow fever, brucellosis and Chagas disease were requested').
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to Yellow Fever disease (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `POSSIBLE_HYPOTHETICAL`):** Initial mention is a differential hypothesis (POSSIBLE_HYPOTHETICAL) that is superseded/ruled out (ABSENT_NEGATIVE) once visceral leishmaniasis is confirmed.
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is DIFFERENTIAL_DIAGNOSIS / RULED_OUT_DIAGNOSIS; Case definition is NOT_MET. Primary confirmed diagnosis is visceral leishmaniasis.
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED / E4_CONTEXT: no positive evidence for Yellow Fever exists, the 5-month chronic course with massive splenomegaly (25 cm) is classic for visceral leishmaniasis rather than acute yellow fever, and bone marrow aspirate confirmed Leishmania amastigotes.
10. **Step 10 — Contradiction Reconciliation (`RESOLVED_TO_ALTERNATIVE_DIAGNOSIS`):** Initial broad differential hypotheses were resolved by confirmatory bone marrow microscopy demonstrating Leishmania amastigotes and response to amphotericin B.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[2010:2360]`
  - **Quote:** "Other hypotheses covered dengue, yellow fever, prolonged septicemic salmonellosis, brucellosis, malaria, Chagas disease and lymphoproliferative malignancies. An evaluation by thick and thin blood smear, blood culture, stool tests, bone marrow biopsy and aspiration and serology for dengue, yellow fever, brucellosis and Chagas disease were requested."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Yellow fever serology (differential workup)`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 2:** `case_text[2409:2492]`
  - **Quote:** "The bone marrow aspirate confirmed the presence of Leishmania amastigotes (Fig. 2)."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Bone marrow aspirate microscopy`, `target_concept=Leishmania amastigotes (Visceral leishmaniasis)`, `specimen=bone marrow`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 29-year-old woman in Rio de Janeiro presented with a 5-month history of intermittent fever, weight loss, cholestatic jaundice, massive hepatosplenomegaly, and pancytopenia. Yellow fever was included as an initial differential diagnostic hypothesis and serology was requested, but bone marrow aspirate confirmed Leishmania amastigotes (visceral leishmaniasis), and the patient recovered with amphotericin B therapy. Because yellow fever was considered only in the differential diagnosis and ruled out by definitive confirmation of visceral leishmaniasis, it is adjudicated as NEGATIVE.

### Case 11: `PMC6180980_01::Yellow_Fever`

- **Article Title:** A Case of Malaria Predisposing to Salmonella Bacteremia in a Returning Traveler from Nigeria
- **Journal / Year / DOI:** *Case Rep Infect Dis* (2018) | DOI: `10.1155/2018/8463417`
- **Input Metadata Demographics:** Age: `50.0`, Gender: `Female`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of malaria and nontyphoidal Salmonella bacteremia in a returning traveler.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 50-year-old female traveler returning to South Carolina from Nigeria.
4. **Step 4 — Disease Mentions & Condition Matched (`Prior yellow fever vaccination history`):** Yellow fever is mentioned once in the past immunization history: 'She had received oral typhoid, yellow fever, hepatitis A, TDaP, influenza, and meningococcal vaccines within the preceding year.'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to prophylactic vaccination (PREVENTION_VACCINATION), not Yellow Fever disease.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion for Yellow Fever infection is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality of vaccination is HISTORICAL_PAST (within the preceding year).
8. **Step 8 — Clinical Role & Case Definition (`PREVENTION_VACCINATION` / `NOT_MET`):** Clinical role is PREVENTION_VACCINATION; Case definition is NOT_MET. Active confirmed diagnoses are P. falciparum malaria and Salmonella bacteremia.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (vaccination history only).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[1169:1297]`
  - **Quote:** "She had received oral typhoid, yellow fever, hepatitis A, TDaP, influenza, and meningococcal vaccines within the preceding year."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Vaccination history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=POSITIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> A 50-year-old woman returning from Lagos, Nigeria, presented with syncope, diarrhea, and fever, and was diagnosed with Plasmodium falciparum malaria (3.5% parasitemia, BinaxNOW positive) and invasive nontyphoidal Salmonella enterica serovar Stanleyville bacteremia. Yellow fever is mentioned solely as part of her pretravel immunization history ('She had received oral typhoid, yellow fever... vaccines within the preceding year.'). Per protocol Rule 4, vaccination history (PREVENTION_VACCINATION) is adjudicated as EXCLUDED_NON_TARGET_CASE.

### Case 12: `PMC2732535_01::Yellow_Fever`

- **Article Title:** First documentation of human Crimean-Congo hemorrhagic fever, Kenya
- **Journal / Year / DOI:** *Emerg Infect Dis* (2002) | DOI: `10.3201/eid0809.010510`
- **Input Metadata Demographics:** Age: `25.0`, Gender: `Male`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report (published as a Letter to the Editor) of fatal Crimean-Congo hemorrhagic fever in Kenya.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 25-year-old male farmer in western Kenya.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever virus (IgM capture ELISA and flavivirus RT-PCR in VHF workup)`):** Yellow fever is mentioned twice: (1) in the patient's viral hemorrhagic fever laboratory workup ('Serologic tests in Nairobi were negative for yellow fever... and RT-PCR tests for flaviviruses... were also negative'), and (2) in the concluding epidemiological background sentence listing endemic VHFs in East/Central Africa.
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to true Yellow Fever virus infection (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion for the patient is ABSENT_NEGATIVE / NEGATED (explicitly negative by both IgM-capture ELISA and flavivirus RT-PCR).
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET. Primary confirmed diagnosis is Crimean-Congo hemorrhagic fever (C-CHFV).
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED (both yellow fever IgM-capture ELISA and flavivirus RT-PCR were negative).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (explicitly ruled out).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[1523:1858]`
  - **Quote:** "Serologic tests in Nairobi were negative for yellow fever, dengue, West Nile, Chikungunya, and Rift Valley fever (immunoglobulin [Ig] M-capture enzyme-linked immunosorbent assay) and reverse transcriptase-polymerase chain reaction (RT-PCR) tests for flaviviruses, alphaviruses, and Bunyamwera serogroup bunyaviruses were also negative."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=IgM-capture ELISA for yellow fever and flavivirus RT-PCR`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 2:** `case_text[1859:1930]`
  - **Quote:** "RT-PCR for Crimean-Congo hemorrhagic fever virus (C-CHFV) was positive."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=C-CHFV RT-PCR`, `target_concept=Crimean-Congo hemorrhagic fever virus`, `specimen=serum`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 25-year-old male farmer in western Kenya died of an acute hemorrhagic fever. Diagnostic testing of serum at the reference laboratory in Nairobi was explicitly negative for yellow fever by IgM-capture ELISA and negative for flaviviruses by RT-PCR, whereas RT-PCR and sequencing confirmed Crimean-Congo hemorrhagic fever virus (C-CHFV) in both Nairobi and Johannesburg. Yellow fever was definitively ruled out -> NEGATIVE.

### Case 13: `PMC7078104_02::Yellow_Fever`

- **Article Title:** BCG as a Case Study for Precision Vaccine Development: Lessons From Vaccine Heterogeneity, Trained Immunity, and Immune Ontogeny
- **Journal / Year / DOI:** *Front Microbiol* (2020) | DOI: `10.3389/fmicb.2020.00332`
- **Input Metadata Demographics:** Age: `5.0`, Gender: `Female`
- **Final Decision (`decision`):** `EXCLUDED_NON_CASE_REPORT`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_SINGLE_PATIENT`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`EXCLUDED_NON_CASE_REPORT` / `SYSTEMATIC_REVIEW`):** Narrative/systematic scientific review article (EXCLUDED_NON_CASE_REPORT / SYSTEMATIC_REVIEW).
2. **Step 2 — CCU Type (`NON_CLINICAL_DOCUMENT`):** Unit of analysis is NON_CLINICAL_DOCUMENT / AGGREGATE_STUDY_UNIT (no individual patient case).
3. **Step 3 — Patient Anchor (`none`):** No individual patient anchor ('none'); metadata age=5.0 was extracted from a cohort sentence ('0-5 year-old BCG vaccinated children').
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever live-attenuated vaccine human challenge model in BCG trained immunity studies`):** Yellow fever is mentioned in two paragraphs summarizing randomized trials where live-attenuated yellow fever vaccine was administered 1 month after BCG vaccination to assess vaccine-strain viremia and IL-1beta trained immunity.
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to experimental live-attenuated yellow fever vaccine challenge (PREVENTION_VACCINATION / EPIDEMIOLOGICAL_CONTEXT) in aggregate trial cohorts.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** No clinical claim of wild-type Yellow Fever disease in an individual patient (ABSENT_NEGATIVE / NEGATED).
7. **Step 7 — Temporality Assessment (`UNKNOWN` / `UNKNOWN`):** Temporality is UNKNOWN / not applicable.
8. **Step 8 — Clinical Role & Case Definition (`EPIDEMIOLOGICAL_CONTEXT` / `NOT_MET`):** Clinical role is EPIDEMIOLOGICAL_CONTEXT / PREVENTION_VACCINATION; Case definition is NOT_MET.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT.
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (review article with no single human patient).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[4178:4434]`
  - **Quote:** "In a randomized placebo-controlled adult study, yellow fever virus vaccine recipients who had been BCG vaccinated with the Denmark strain 1 month prior, had significantly lower yellow fever viremia compared to subjects who had received placebo vaccination."
  - **Parameters:** `patient_anchor_id=none`, `test_name=Randomized placebo-controlled BCG / yellow fever vaccine challenge study summary`, `target_concept=Yellow fever vaccine viremia`, `specimen=None`, `result=INCONCLUSIVE`, `temporality=UNKNOWN`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[8096:8472]`
  - **Quote:** "In a randomized placebo-controlled human BCG immunization study with subsequent yellow fever vaccine challenge, reduction of viremia was highly correlated with the upregulation of IL-1beta, a cytokine associated with the induction of trained immunity, but not with the specific IFNgamma response, supporting a key role for IL-1beta as a mediator of trained immunity responses."
  - **Parameters:** `patient_anchor_id=none`, `test_name=Randomized BCG / yellow fever vaccine challenge study summary`, `target_concept=Yellow fever vaccine challenge`, `specimen=None`, `result=INCONCLUSIVE`, `temporality=UNKNOWN`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> This document is a scientific review article on Bacille Calmette-Guerin (BCG) vaccinology, trained immunity, and immune ontogeny, not a clinical case report of an individual patient. Yellow fever is mentioned only in reference to randomized trials using attenuated yellow fever vaccine as an experimental challenge to measure BCG-induced trained immunity and post-vaccination viremia reduction. Because it is a non-case-report review and involves vaccine challenge in aggregate cohorts, it is adjudicated as EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 14: `PMC5956635_01::Yellow_Fever`

- **Article Title:** First report of African tick-bite fever in a South American traveler
- **Journal / Year / DOI:** *SAGE Open Med Case Rep* (2018) | DOI: `10.1177/2050313X18775301`
- **Input Metadata Demographics:** Age: `32.0`, Gender: `Male`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of African tick-bite fever (Rickettsia africae) in a Brazilian traveler.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 32-year-old Brazilian male returning from South Africa.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever serology (acute febrile traveler differential workup)`):** Yellow fever is mentioned in the acute serological workup ('serum samples for serological tests (spotted fever group rickettsiae, dengue, yellow fever, leptospirosis)'), followed by 'All the other serological tests... were negative.'
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to true Yellow Fever virus infection (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED (serological test explicitly reported as negative).
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET. Primary confirmed diagnosis is African tick-bite fever (Rickettsia africae).
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED (negative yellow fever serology plus definitive culture and molecular confirmation of R. africae).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[2349:2621]`
  - **Quote:** "Whole blood and blood clot were collected (in BHI solution and frozen at -70 C) for microbiological procedures and serum samples for serological tests (spotted fever group rickettsiae, dengue, yellow fever, leptospirosis), malaria and dengue-NS1 point-of-care rapid tests."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Yellow fever serology`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 2:** `case_text[3510:3635]`
  - **Quote:** "All the other serological tests, and antigen detection (for malaria and dengue-NS1) and routine blood cultures were negative."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Serological panel including yellow fever, dengue, and leptospirosis`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`

#### Clinical Synthesis Rationale

> A 32-year-old Brazilian traveler returning from South Africa presented with fever, headache, myalgia, maculopapular rash, inguinal lymphadenopathy, and a necrotic eschar. Serum samples were tested for spotted fever group rickettsiae, dengue, yellow fever, and leptospirosis; while Rickettsia spp. IgG seroconverted and Rickettsia africae was isolated in culture and confirmed by PCR/sequencing, 'All the other serological tests, and antigen detection (for malaria and dengue-NS1) and routine blood cultures were negative.' Yellow fever was tested and ruled out -> NEGATIVE.

### Case 15: `PMC10313350_01::Yellow_Fever`

- **Article Title:** Case report: Injected corticosteroids for treating leprosy isolated neuritis
- **Journal / Year / DOI:** *Front Med (Lausanne)* (2023) | DOI: `10.3389/fmed.2023.1202108`
- **Input Metadata Demographics:** Age: `24.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL, F6_EVIDENCE_SPECIFICITY`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report (Case 1 of 2) describing ultrasound-guided corticosteroid injection for isolated leprosy ulnar neuritis.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 24-year-old male resident of metropolitan Rio de Janeiro.
4. **Step 4 — Disease Mentions & Condition Matched (`Remote past medical history of yellow fever (4 years previously)`):** Yellow fever is mentioned once in the background history: 'Past medical history: yellow fever 4 years previously, was a non-drinker and non-smoker, and said he did not use medications regularly.'
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to a self-reported remote episode of yellow fever 4 years prior (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`HISTORICAL_RESOLVED` / `HISTORICAL_RESOLVED`):** Assertion is HISTORICAL_RESOLVED (remote resolved history).
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality is HISTORICAL_PAST / HISTORICAL_RESOLVED (4 years prior to the current presentation).
8. **Step 8 — Clinical Role & Case Definition (`PAST_HISTORY` / `NOT_MET`):** Clinical role is PAST_HISTORY; Case definition for current episode is NOT_MET. Current active diagnosis is borderline lepromatous leprosy with acute ulnar neuritis.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (unverified historical note in past medical history; no diagnostic tests or clinical details for yellow fever).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (Protocol Step 11 explicitly requires temporality = CURRENT_ACTIVE or RECENT_EPISODIC, clinical_role = PRIMARY_DIAGNOSIS or ACTIVE_COMORBIDITY, and E1/E2 evidence; 'Historical resolved infection' alone never satisfies VPD).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[240:375]`
  - **Quote:** "Past medical history: yellow fever 4 years previously, was a non-drinker and non-smoker, and said he did not use medications regularly."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Past medical history`, `target_concept=Yellow fever (historical)`, `specimen=None`, `result=POSITIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> A 24-year-old male in Rio de Janeiro was diagnosed with borderline lepromatous leprosy (bacilloscopy 5.25, Mitsuda 5 mm) and developed acute left ulnar neuritis (type 1 reaction) after 4 months of multidrug therapy, managed with ultrasound-guided perineural methylprednisolone injections. Yellow fever is mentioned solely in a single phrase of remote past medical history ('Past medical history: yellow fever 4 years previously'). Under Step 11, historical resolved infection (temporality = HISTORICAL_PAST / HISTORICAL_RESOLVED, clinical_role = PAST_HISTORY) with no current disease or E1/E2 evidence does not satisfy VPD -> EXCLUDED_NON_TARGET_CASE.

### Case 16: `PMC6884810_01::Yellow_Fever`

- **Article Title:** Dengue fever and chikungunya virus infections: identification in travelers in Uganda - 2017
- **Journal / Year / DOI:** *Trop Dis Travel Med Vaccines* (2019) | DOI: `10.1186/s40794-019-0099-3`
- **Input Metadata Demographics:** Age: `40.0`, Gender: `Male`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL, F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Clinical case report summarizing travel-related arbovirus cases in Uganda (primary narrative focuses on Case 1, a 40-year-old Bangladeshi male traveler).
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode for Case 1 (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 40-year-old male traveler from Bangladesh admitted to Nakasero Hospital in Uganda (ARB01183/Uganda).
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow fever virus (IgM capture ELISA and flavivirus RT-PCR in arboviral workup, plus prior travel vaccination)`):** Yellow fever is mentioned both in pretravel history ('had received yellow fever specific travel-related vaccination') and in the acute laboratory workup ('tested for yellow virus (YFV)... antibodies by IgM capture ELISA... All serological testing in case report 1 (ARB01183/Uganda) were negative' and 'negative for flavivirus and bunyavirus').
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to Yellow Fever virus (TARGET_CONFIRMED) in diagnostic testing as well as prior vaccination.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion for acute Yellow Fever infection is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality of diagnostic exclusion is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET. Primary confirmed diagnosis for Case 1 is Chikungunya virus infection (and Dengue virus type 2 for the two sisters in Case 2).
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED (negative YFV IgM capture ELISA and negative flavivirus group-specific RT-PCR on cell culture supernatant).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[179:328]`
  - **Quote:** "The patient had no significant past medical history, was on no regular medication, and had received yellow fever specific travel-related vaccination."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Vaccination history`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=POSITIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`
- **Evidence Item 2:** `case_text[1200:1734]`
  - **Quote:** "A total of 284 serum samples collected in 2017 were tested for yellow virus (YFV), West Nile virus (WNV), DENV1-4, CHIKV and Zika virus (ZIKV) antibodies by IgM capture ELISA. Only the diagnostic testing results for arbovirus infections of the three travel-related cases are shown and summarized in Table 1. All serological testing in case report 1 (ARB01183/Uganda) were negative, while high neutralizing antibodies against DENV2 were found for both sisters that traveled to Ethiopia in case report 2 (ARB01227UVRI and ARB01228UVRI)."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=YFV IgM capture ELISA`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 3:** `case_text[1923:2077]`
  - **Quote:** "RNA extracted from harvested virus supernatant and tested by group-specific RT-PCR was positive for alphavirus and negative for flavivirus and bunyavirus."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Group-specific flavivirus RT-PCR on Vero cell culture supernatant`, `target_concept=Flavivirus (including Yellow fever virus)`, `specimen=serum virus culture supernatant`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`

#### Clinical Synthesis Rationale

> A 40-year-old male traveling from Bangladesh to the DRC via Uganda presented with acute fever and joint pain. He had previously received yellow fever travel vaccination. Acute serum testing at the Uganda Virus Research Institute (UVRI) was explicitly negative for yellow fever virus (YFV) IgM by capture ELISA, and viral culture supernatant was negative for flavivirus by group-specific RT-PCR, whereas Chikungunya virus (CHIKV) was confirmed by real-time RT-PCR and next-generation sequencing. Because Yellow Fever was directly tested and ruled out, the case is adjudicated as NEGATIVE.

### Case 17: `PMC10481985_01::Yellow_Fever`

- **Article Title:** Reply to Letter to Editor: Unilateral Acute Central Serous Chorioretinopathy with Inactivated Coronavirus Disease 2019 Vaccination - A Case Report and Review of Literature
- **Journal / Year / DOI:** *J Curr Ophthalmol* (2023) | DOI: `10.4103/joco.joco_111_23`
- **Input Metadata Demographics:** Age: `39.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_TARGET_CASE`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_TARGET_CASE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`EXCLUDED_NON_CASE_REPORT` / `CASE_REPORT`):** Reply to a Letter to the Editor commentary referencing a prior case report.
2. **Step 2 — CCU Type (`NON_CLINICAL_DOCUMENT`):** Discourse commentary / non-target mention (NON_CLINICAL_DOCUMENT / PRIMARY_CARE_EPISODE reference).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 39-year-old male who developed CSC after Sinopharm COVID-19 vaccination.
4. **Step 4 — Disease Mentions & Condition Matched (`Literature background mention of yellow fever vaccination associated with central serous chorioretinopathy`):** Yellow fever is mentioned once in the final paragraph as general literature background: 'Furthermore, CSC has been reported after vaccination for influenza, yellow fever, anthrax, and smallpox; however, the causality has not been established in a proper manner.'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to yellow fever vaccine adverse events in the medical literature (PREVENTION_VACCINATION / EPIDEMIOLOGICAL_CONTEXT), not the patient.
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion for the patient is ABSENT_NEGATIVE / NEGATED.
7. **Step 7 — Temporality Assessment (`UNKNOWN` / `UNKNOWN`):** Temporality is UNKNOWN / not applicable to the patient.
8. **Step 8 — Clinical Role & Case Definition (`EPIDEMIOLOGICAL_CONTEXT` / `NOT_MET`):** Clinical role is EPIDEMIOLOGICAL_CONTEXT; Case definition is NOT_MET.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT (general literature citation only).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_TARGET_CASE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[1855:2027]`
  - **Quote:** "Furthermore, CSC has been reported after vaccination for influenza, yellow fever, anthrax, and smallpox; however, the causality has not been established in a proper manner."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Literature review commentary`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=INCONCLUSIVE`, `temporality=UNKNOWN`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> This document is a Reply to a Letter to the Editor regarding a previously reported 39-year-old man who developed unilateral acute central serous chorioretinopathy (CSC) 2 days after receiving the inactivated Sinopharm COVID-19 vaccine. Yellow fever is mentioned solely in passing as general literature background ('Furthermore, CSC has been reported after vaccination for influenza, yellow fever, anthrax, and smallpox'). It has no connection to the patient and refers only to vaccine literature -> EXCLUDED_NON_TARGET_CASE.

### Case 18: `PMC11131420_01::Yellow_Fever`

- **Article Title:** Presidents and vaccines: head of state inoculation as a tool for vaccine promotion
- **Journal / Year / DOI:** *Front Public Health* (2024) | DOI: `10.3389/fpubh.2024.1364927`
- **Input Metadata Demographics:** Age: `44.0`, Gender: `Male`
- **Final Decision (`decision`):** `EXCLUDED_NON_CASE_REPORT`
- **Dataset Label (`step12_dataset_label`):** `EXCLUDED_NON_SINGLE_PATIENT`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`EXCLUDED_NON_CASE_REPORT` / `AGGREGATE_COHORT`):** Aggregate population survey study / randomized survey experiment (EXCLUDED_NON_CASE_REPORT / AGGREGATE_COHORT).
2. **Step 2 — CCU Type (`AGGREGATE_STUDY_UNIT`):** Unit of analysis is AGGREGATE_STUDY_UNIT (N=600 survey respondents in the DRC).
3. **Step 3 — Patient Anchor (`none`):** No individual patient anchor ('none'); metadata age=44.0 was extracted from the cohort mean ('On average, a sample respondent is 44 years old').
4. **Step 4 — Disease Mentions & Condition Matched (`Household childhood yellow fever vaccination rate in a survey cohort`):** Yellow fever is mentioned once in the descriptive survey statistics: 'Almost nine out of ten households indicate to have vaccinated their children against tuberculosis, diphtheria, polio, measles, and yellow fever...'
5. **Step 5 — Concept Grounding (`PREVENTION_VACCINATION`):** Concept refers to childhood immunization rates in a survey sample (PREVENTION_VACCINATION / EPIDEMIOLOGICAL_CONTEXT).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** No patient-level claim of Yellow Fever disease (ABSENT_NEGATIVE / NEGATED).
7. **Step 7 — Temporality Assessment (`HISTORICAL_PAST` / `HISTORICAL_RESOLVED`):** Temporality is HISTORICAL_PAST.
8. **Step 8 — Clinical Role & Case Definition (`EPIDEMIOLOGICAL_CONTEXT` / `NOT_MET`):** Clinical role is EPIDEMIOLOGICAL_CONTEXT / PREVENTION_VACCINATION; Case definition is NOT_MET.
9. **Step 9 — Evidence Specificity (`E4_CONTEXT`):** Evidence strength is E4_CONTEXT.
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied (aggregate study unit, not a single human patient).
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[730:964]`
  - **Quote:** "Almost nine out of ten households indicate to have vaccinated their children against tuberculosis, diphtheria, polio, measles, and yellow fever, while 98% of households vaccinated their children against at least one of these diseases."
  - **Parameters:** `patient_anchor_id=none`, `test_name=Household vaccination survey (N=600)`, `target_concept=Yellow fever vaccine`, `specimen=None`, `result=INCONCLUSIVE`, `temporality=HISTORICAL_PAST`, `relation=INCONCLUSIVE`, `strength=E4_CONTEXT`

#### Clinical Synthesis Rationale

> This article presents a randomized survey experiment of 600 citizens in the Democratic Republic of Congo evaluating the effect of President Felix Tshisekedi's public COVID-19 inoculation on vaccine acceptance. Yellow fever is mentioned once in aggregate survey statistics ('Almost nine out of ten households indicate to have vaccinated their children against tuberculosis, diphtheria, polio, measles, and yellow fever'). Because this is an aggregate population survey rather than a single-patient case report and refers only to childhood vaccination rates, it is adjudicated as EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 19: `PMC11769472_01::Yellow_Fever`

- **Article Title:** Acute Febrile Illness Accompanied by 7th and 12th Cranial Nerve Palsy Due to Lyme Disease Following Travel to Rural Ecuador: A Case Report and Mini-Review
- **Journal / Year / DOI:** *Trop Med Infect Dis* (2025) | DOI: `10.3390/tropicalmed10010021`
- **Input Metadata Demographics:** Age: `65.0`, Gender: `Male`
- **Final Decision (`decision`):** `NEGATIVE`
- **Dataset Label (`step12_dataset_label`):** `NEGATIVE`
- **VPD Satisfied (`step11_vpd_satisfied`):** `False`
- **Confidence / Failure Flags:** `HIGH` | `F4_ASSERTION_TEMPORAL`

#### 12-Step Protocol Walkthrough

1. **Step 1 — Document Type (`CLINICAL_CASE_REPORT` / `CASE_REPORT`):** Single-patient clinical case report of acute Lyme neuroborreliosis (CN VII and XII palsies) following travel to Ecuador.
2. **Step 2 — CCU Type (`PRIMARY_CARE_EPISODE`):** Single human patient care episode (PRIMARY_CARE_EPISODE / SINGLE_HUMAN_PATIENT).
3. **Step 3 — Patient Anchor (`patient_1`):** patient_1: 65-year-old Canadian male residing in Lyme-endemic southern Ontario.
4. **Step 4 — Disease Mentions & Condition Matched (`Yellow Fever serology (post-travel febrile and cranial neuropathy differential workup)`):** Yellow Fever is mentioned in the emergency department infectious workup: 'serologic testing for Hepatitis A, B, C, and E, Dengue virus, Chikungunya virus, West Nile virus, Yellow Fever, Rickettsia (spotted fever and typhi), and Trypanosome cruzi, were negative.'
5. **Step 5 — Concept Grounding (`TARGET_CONFIRMED`):** Concept refers to true Yellow Fever virus infection (TARGET_CONFIRMED).
6. **Step 6 — Assertion Assessment (`ABSENT_NEGATIVE` / `NEGATED`):** Assertion is ABSENT_NEGATIVE / NEGATED (serologic testing was explicitly negative).
7. **Step 7 — Temporality Assessment (`CURRENT_EPISODE` / `CURRENT_ACTIVE`):** Temporality is CURRENT_EPISODE / CURRENT_ACTIVE.
8. **Step 8 — Clinical Role & Case Definition (`RULED_OUT_DIAGNOSIS` / `NOT_MET`):** Clinical role is RULED_OUT_DIAGNOSIS; Case definition is NOT_MET. Primary confirmed diagnosis is Lyme neuroborreliosis (Borrelia burgdorferi).
9. **Step 9 — Evidence Specificity (`E0_CONTRADICTED`):** Evidence strength is E0_CONTRADICTED (negative Yellow Fever serology and reactive modified two-tier Borrelia burgdorferi serology).
10. **Step 10 — Contradiction Reconciliation (`NONE`):** No contradiction.
11. **Step 11 — Valid Positive Diagnosis (VPD) Evaluation (`False`):** VPD test is NOT satisfied.
12. **Step 12 — Final Clinical Adjudication & Audit:** Final adjudication: NEGATIVE (HIGH confidence).

#### Verbatim Grounded Evidence (`step9_key_evidence`)

- **Evidence Item 1:** `case_text[3269:3609]`
  - **Quote:** "A broad infectious work up, including blood and urine cultures, respiratory virus PCR, malaria thick and thin blood smear and rapid diagnostic test, and serologic testing for Hepatitis A, B, C, and E, Dengue virus, Chikungunya virus, West Nile virus, Yellow Fever, Rickettsia (spotted fever and typhi), and Trypanosome cruzi, were negative."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Yellow Fever serologic testing`, `target_concept=Yellow fever virus`, `specimen=serum`, `result=NEGATIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E0_CONTRADICTED`
- **Evidence Item 2:** `case_text[5108:5374]`
  - **Quote:** "Shortly after his clinic visit, the Borrelia burgdorferi serologic testing performed during his first visit to the ED was reported as reactive (tier 1 IgG/IgM ELISA: reactive; tier 2 anti-VlsE1+pepC10 IgG/IgM ELISA: reactive), confirming a diagnosis of Lyme disease."
  - **Parameters:** `patient_anchor_id=patient_1`, `test_name=Modified two-tier testing (MTTT) Borrelia burgdorferi serology`, `target_concept=Borrelia burgdorferi (Lyme disease)`, `specimen=serum`, `result=POSITIVE`, `temporality=CURRENT_EPISODE`, `relation=REFUTES`, `strength=E1_CONFIRMATORY`

#### Clinical Synthesis Rationale

> A 65-year-old Canadian man returning from Ecuador presented with fever, erythema migrans rash, and cranial nerve VII and XII palsies. Because of his tropical travel history, a comprehensive infectious workup was performed, and serologic testing for Yellow Fever was explicitly negative. Modified two-tier serologic testing for Borrelia burgdorferi was reactive, confirming acute Lyme neuroborreliosis, and his symptoms resolved completely after a 4-week course of doxycycline. Yellow Fever was explicitly tested and ruled out -> NEGATIVE.

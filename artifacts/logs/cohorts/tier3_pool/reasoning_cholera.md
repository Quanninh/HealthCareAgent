# Clinical Claim Annotation Reasoning Log — Cholera (`tier3_pool`)

## 1. Executive Summary & Adjudication Breakdown

- **Target Disease:** `Cholera` (*Vibrio cholerae*)
- **Input File:** `input_cholera.jsonl` (21 candidate pairs)
- **Output File:** `output_cholera.jsonl` (21 annotated records)
- **Total Verbatim Grounded Evidence Spans Verified:** 34 (`case_text[start_char:end_char] == source_quote` verified 100%)
- **Adjudication Distribution (`decision` / `step12_dataset_label`):**
  - `POSITIVE`: 1 (`PMC8415062_01::Cholera`)
  - `NEGATIVE`: 10
  - `EXCLUDED_NON_TARGET_CASE`: 4
  - `EXCLUDED_NON_CASE_REPORT` (`EXCLUDED_NON_SINGLE_PATIENT`): 6

## 2. Summary Table of All 21 Candidate Pairs

| # | Pair ID | Age / Sex | Step 1 Doc Type | Step 2 CCU Type | Step 5 Assertion | Step 7 Clinical Role | Step 9 Evidence | Final Decision | Failure Flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `PMC10018008_01::Cholera` | N/A / Unknown | `EXCLUDED_NON_CASE_REPORT` | `AGGREGATE_STUDY_UNIT` | `NOT_APPLICABLE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_CASE_REPORT`** | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT` |
| 2 | `PMC10018008_03::Cholera` | 65 / Unknown | `EXCLUDED_NON_CASE_REPORT` | `AGGREGATE_STUDY_UNIT` | `NOT_APPLICABLE` | `PREVENTION_VACCINATION` | `E4_CONTEXT` | **`EXCLUDED_NON_CASE_REPORT`** | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT` |
| 3 | `PMC4255052_01::Cholera` | 61 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 4 | `PMC9355657_01::Cholera` | N/A / Unknown | `EXCLUDED_NON_CASE_REPORT` | `MULTI_PATIENT_CASE_SERIES` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E4_CONTEXT` | **`EXCLUDED_NON_CASE_REPORT`** | `F2_SCOPE_COHORT, F4_ASSERTION_TEMPORAL` |
| 5 | `PMC6374571_01::Cholera` | 32 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `NOT_APPLICABLE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_TARGET_CASE`** | `F1_LEXICAL_HOMONYM, F5_DISCOURSE_CONTEXT` |
| 6 | `PMC6388674_01::Cholera` | 18 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `PREVENTION_VACCINATION` | `E4_CONTEXT` | **`EXCLUDED_NON_TARGET_CASE`** | `F5_DISCOURSE_CONTEXT` |
| 7 | `PMC3792539_01::Cholera` | 64 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `NOT_APPLICABLE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_TARGET_CASE`** | `F5_DISCOURSE_CONTEXT` |
| 8 | `PMC8415062_01::Cholera` | 63 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `AFFIRMED` | `SECONDARY_DIAGNOSIS` | `E1_CONFIRMATORY` | **`POSITIVE`** | `None` |
| 9 | `PMC9043682_01::Cholera` | 8 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 10 | `PMC6180980_01::Cholera` | 50 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 11 | `PMC6532487_01::Cholera` | 57 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 12 | `PMC9083785_01::Cholera` | 74 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 13 | `PMC9996308_02::Cholera` | 26 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_TARGET_CASE`** | `F3_SUBJECT_COREFERENCE, F5_DISCOURSE_CONTEXT` |
| 14 | `PMC8383206_01::Cholera` | 21 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 15 | `PMC4967050_02::Cholera` | N/A / Female | `EXCLUDED_NON_CASE_REPORT` | `NON_CLINICAL_DOCUMENT` | `NOT_APPLICABLE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_CASE_REPORT`** | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT` |
| 16 | `PMC4588357_01::Cholera` | 7 / Unknown | `EXCLUDED_NON_CASE_REPORT` | `AGGREGATE_STUDY_UNIT` | `NOT_APPLICABLE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_CASE_REPORT`** | `F1_LEXICAL_HOMONYM, F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT` |
| 17 | `PMC10641789_01::Cholera` | 10 / Male | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 18 | `PMC10945545_01::Cholera` | 38 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL` |
| 19 | `PMC11338764_01::Cholera` | 60 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL, F5_DISCOURSE_CONTEXT` |
| 20 | `PMC10481634_22::Cholera` | 47 / Male | `EXCLUDED_NON_CASE_REPORT` | `NON_CLINICAL_DOCUMENT` | `NOT_APPLICABLE` | `EPIDEMIOLOGICAL_CONTEXT` | `E4_CONTEXT` | **`EXCLUDED_NON_CASE_REPORT`** | `F2_SCOPE_COHORT, F5_DISCOURSE_CONTEXT` |
| 21 | `PMC11754817_01::Cholera` | 14 / Female | `CLINICAL_CASE_REPORT` | `PRIMARY_CARE_EPISODE` | `ABSENT_NEGATIVE` | `RULED_OUT_DIAGNOSIS` | `E0_CONTRADICTED` | **`NEGATIVE`** | `F4_ASSERTION_TEMPORAL, F5_DISCOURSE_CONTEXT` |

## 3. Case-by-Case 12-Step Clinical Semantic Reasoning

### Case 1: `PMC10018008_01::Cholera`
- **Article Title:** Oral inactivated whole cell vaccine for mucosal immunization: ETVAX case study
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `EXCLUDED_NON_CASE_REPORT` (`EXCLUDED_NON_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `AGGREGATE_STUDY_UNIT`
- **Step 3 — Patient Anchor:** `none` (`anchor_type=NONE_COHORT`, `age=None`, `gender=Unknown`) — Review and multi-cohort clinical trial summary of the ETVAX oral ETEC vaccine across Swedish and Bangladeshi adult, child, and infant trial cohorts; no individual patient case.
- **Step 4 — Condition Concept Matched:** Cholera toxin B-subunit (CTB) vaccine component and oral cholera vaccine (OCV) comparator discussed in an ETEC vaccine review
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `NOT_APPLICABLE` (`UNCERTAIN`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[170:496]` | `test_name="Vaccine formulation review"` | `target_concept="Cholera toxin B-subunit (CTB)"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "A first-generation precursor of the current ETVAX candidate was a whole cell vaccine consisting of formalin-inactivated ETEC bacteria expressing CFA/I and CS1 to CS5, combined with cholera toxin B-subunit (CTB), which is highly homologous to the B-subunit (LTB) of LT enterotoxin produced by approximately 66% of ETEC strains."
  - **Evidence Item 2:** `case_text[7236:7486]` | `test_name="Vaccine immunogenicity comparison"` | `target_concept="Oral cholera vaccine (OCV)"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "These observations may have implications for more successful use of dmLT with other oral vaccines, like cholera (OCV), which have experienced difficulty in inducing protective O antigen antibody responses in children and infants under 5 years of age."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — No clinical claim of cholera infection; document is an aggregate vaccine review.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_CASE_REPORT`** (`step12_dataset_label="EXCLUDED_NON_SINGLE_PATIENT"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** Review article summarizing phase 1/2 clinical trials of the oral inactivated ETEC vaccine candidate ETVAX in adult and pediatric cohorts in Sweden and Bangladesh. Not a single-patient clinical case report (AGGREGATE_STUDY_UNIT). Mentions of cholera refer solely to the recombinant cholera toxin B-subunit (CTB) antigen component and oral cholera vaccine (OCV) immunogenicity comparisons in children -> EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 2: `PMC10018008_03::Cholera`
- **Article Title:** Oral inactivated whole cell vaccine for mucosal immunization: ETVAX case study
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `EXCLUDED_NON_CASE_REPORT` (`EXCLUDED_NON_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `AGGREGATE_STUDY_UNIT`
- **Step 3 — Patient Anchor:** `none` (`anchor_type=NONE_COHORT`, `age=None`, `gender=Unknown`) — Aggregate clinical trial review covering 729 Finnish adult volunteers and 4,936 Gambian children in ETVAX vaccine trials.
- **Step 4 — Condition Concept Matched:** Licensed inactivated whole-cell oral cholera vaccines (Dukoral, Hikojima, Euvichol) discussed as delivery and co-formulation comparators
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `NOT_APPLICABLE` (`UNCERTAIN`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `PREVENTION_VACCINATION` (`PREVENTION_VACCINATION`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[2615:2791]` | `test_name="Vaccine formulation comparison"` | `target_concept="Inactivated whole-cell cholera vaccine"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "To date the only licensed inactivated whole cell vaccines against enteric diseases are against cholera, and most depend upon delivery of acid-resistant polysaccharide antigens."
  - **Evidence Item 2:** `case_text[4707:4833]` | `test_name="Vaccine co-formulation discussion"` | `target_concept="Hikojima and Euvichol cholera vaccines"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "These could include the cross-protective inactivated Shigella whole cell vaccine or the Hikojima or Euvichol cholera vaccines."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Aggregate clinical trial summary; cholera mentions refer exclusively to oral cholera vaccines.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_CASE_REPORT`** (`step12_dataset_label="EXCLUDED_NON_SINGLE_PATIENT"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** Aggregate review section describing phase 2b ETVAX vaccine trials in 729 Finnish volunteers and 4,936 Gambian children (AGGREGATE_STUDY_UNIT). Mentions of cholera refer exclusively to licensed inactivated whole-cell oral cholera vaccines (Dukoral, Hikojima, Euvichol) as formulation and co-administration comparators -> EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 3: `PMC4255052_01::Cholera`
- **Article Title:** Aeromonas hydrophila Sepsis Associated with Consumption of Raw Oysters
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=61.0`, `gender=Male`) — 61-year-old male presenting with acute pancreatitis and Aeromonas hydrophila sepsis following raw oyster consumption.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae infection tested and ruled out during microbiological workup
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[1547:1584]` | `test_name="Microbiological test for Vibrio cholerae"` | `target_concept="Vibrio cholerae"` | `specimen=blood` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Test for Vibrio cholera was negative."
  - **Evidence Item 2:** `case_text[1585:1634]` | `test_name="rpoD gene sequencing"` | `target_concept="Aeromonas hydrophila"` | `specimen=blood` | `result=POSITIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Sequencing via rpoD gene confirmed A. hydrophila."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Testing for Vibrio cholerae was explicitly negative, and rpoD gene sequencing confirmed Aeromonas hydrophila.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 61-year-old male presented with acute pancreatitis and sepsis after consuming raw oysters in Florida. Blood cultures grew Gram-negative bacilli confirmed as Aeromonas hydrophila by MicroScan and rpoD gene sequencing, while testing for Vibrio cholerae was explicitly negative -> NEGATIVE.

### Case 4: `PMC9355657_01::Cholera`
- **Article Title:** Detection of Echovirus-18 in Children Suspected With SARS-CoV-2 Infection With Multisystem Inflammatory Syndrome: A Case Report From India
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `EXCLUDED_NON_CASE_REPORT` (`CASE_SERIES`)
- **Step 2 — CCU Type (Unit of Analysis):** `MULTI_PATIENT_CASE_SERIES`
- **Step 3 — Patient Anchor:** `none` (`anchor_type=MULTI_PATIENT_GROUP`, `age=None`, `gender=Unknown`) — Four children aged 11-15 years described collectively with aggregate statistics (mean duration of illness 5 days, range 3-10 days) and infected with Echovirus-18.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae included in routine bacterial stool screening panel across four pediatric MIS-C-like cases caused by Echovirus-18
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`DIFFERENTIAL_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[0:241]` | `test_name="Case series description"` | `target_concept="Multi-patient pediatric cohort (n=4)"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "Four children between 11 and 15 years of age were admitted to the hospital, over a week, with similar clinical presentations, i.e., fever, vomiting, diarrhea, abdominal pain, difficulty breathing, shock, and myocardial dysfunction (Table 1)."
  - **Evidence Item 2:** `case_text[1058:1386]` | `test_name="Stool bacterial pathogen panel"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "Due to the clinical presentation of diarrhea, vomiting, and abdominal pain, testing was performed for common enteric viruses [i.e., rotavirus A (RVA), norovirus gr I and II, astrovirus, adenovirus, and enterovirus] and common bacterial pathogens (i.e., diarrheagenic E.coli, Salmonella spp., Shigella spp., and Vibrio cholerae)."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Multi-patient case series (4 children summarized together) where Vibrio cholerae was only part of the routine enteric screening panel and Echovirus-18 was identified as the etiology.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_CASE_REPORT`** (`step12_dataset_label="EXCLUDED_NON_SINGLE_PATIENT"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F2_SCOPE_COHORT', 'F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** Case series describing four children (ages 11-15 years, mean illness duration 5 days, range 3-10 days) in aggregate rather than an individual single-patient case unit (MULTI_PATIENT_CASE_SERIES). Stool samples were screened for common viral and bacterial pathogens including Vibrio cholerae, and molecular analysis identified Echovirus-18 in all four children -> EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 5: `PMC6374571_01::Cholera`
- **Article Title:** A case report of acute rheumatic fever and a brief review of the literature
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=32.0`, `gender=Female`) — 32-year-old woman diagnosed with acute rheumatic fever presenting with migratory polyarthritis, subcutaneous nodules, and erythema marginatum.
- **Step 4 — Condition Concept Matched:** Typographical homonym 'Huntington cholera' (intended: Huntington chorea) in literature review of conditions mimicking acute rheumatic fever
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `NOT_APPLICABLE` (`UNCERTAIN`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[6821:7159]` | `test_name="Literature review differential list"` | `target_concept="Huntington chorea (misspelled as Huntington cholera)"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "These include congenital heart disease, viral myocarditis, infective endocarditis, other causes of pericarditis such as connective tissue disease, innocent cardiac murmurs, septic arthritis, reactive arthritis, juvenile idiopathic arthritis, sickle cell disease, gout, leukemia, Wilson disease, Huntington cholera, and intracranial tumor."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — The string 'Huntington cholera' is a typographical error for 'Huntington chorea' in the general literature review section and has no relation to Vibrio cholerae.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_TARGET_CASE`** (`step12_dataset_label="EXCLUDED_NON_TARGET_CASE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F1_LEXICAL_HOMONYM', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** A 32-year-old woman was diagnosed with acute rheumatic fever based on migratory polyarthritis, erythema marginatum, subcutaneous nodules, and elevated ASO/anti-DNase B titers. The word 'cholera' appears only once in the general literature review section as a typographical error ('Huntington cholera' for Huntington chorea, a neurological mimic of Sydenham chorea) -> EXCLUDED_NON_TARGET_CASE.

### Case 6: `PMC6388674_01::Cholera`
- **Article Title:** Relapse of typhoid fever following delayed response to meropenem: A case report and review of previously published cases indicating limited clinical efficacy of meropenem for the treatment of typhoid fever
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=18.0`, `gender=Male`) — 18-year-old Caucasian male returning traveler with blood-culture-confirmed Salmonella enterica serovar Typhi typhoid fever and relapse.
- **Step 4 — Condition Concept Matched:** Unvaccinated pre-travel status for cholera ('The patient did not receive any vaccination against cholera or typhoid fever')
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `HISTORICAL_PAST` (`HISTORICAL_RESOLVED`)
- **Step 7 — Clinical Role:** `PREVENTION_VACCINATION` (`PREVENTION_VACCINATION`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[1353:1430]` | `test_name="Pre-travel immunization history"` | `target_concept="Cholera vaccination"` | `specimen=None` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "The patient did not receive any vaccination against cholera or typhoid fever."
  - **Evidence Item 2:** `case_text[2243:2324]` | `test_name="Stool culture"` | `target_concept="Enteric bacterial pathogens"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Blood, urine, and stool cultures were performed. The latter two showed no growth."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Cholera is mentioned solely regarding the absence of pre-travel cholera vaccination; blood cultures confirmed Salmonella enterica serovar Typhi and stool cultures showed no growth.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_TARGET_CASE`** (`step12_dataset_label="EXCLUDED_NON_TARGET_CASE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** An 18-year-old male traveler returning from Asia presented with fever and watery diarrhea and was confirmed via blood culture to have typhoid fever (Salmonella enterica serovar Typhi), while stool cultures showed no growth. Cholera is mentioned exclusively in the pre-travel immunization history ('The patient did not receive any vaccination against cholera or typhoid fever') -> EXCLUDED_NON_TARGET_CASE.

### Case 7: `PMC3792539_01::Cholera`
- **Article Title:** Severe Wound Infection with Photobacterium damselae ssp. damselae and Vibrio harveyi, following a Laceration Injury in Marine Environment: A Case Report and Review of the Literature
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=64.0`, `gender=Male`) — 64-year-old male with a lower-leg laceration wound co-infected with Photobacterium damselae ssp. damselae and Vibrio harveyi after marine exposure in Western Australia.
- **Step 4 — Condition Concept Matched:** Laboratory methodology citation of CLSI disk-diffusion guidelines for Vibrio spp. (excluding Vibrio cholerae)
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `NOT_APPLICABLE` (`UNCERTAIN`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[5819:6119]` | `test_name="CLSI antimicrobial susceptibility guideline reference"` | `target_concept="CLSI guidelines for Vibrio spp. (excluding Vibrio cholerae)"` | `specimen=wound swab` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "Since the genus Photobacterium is a member of the family Vibrionaceae, interpretation of the inhibition zones (Table 2) was done using the CLSI guidelines for Vibrio ssp. (excluding Vibrio cholerae), which are implemented in the Sirweb expert system (i2a, Perols Cedex, France), operated in our unit."
  - **Evidence Item 2:** `case_text[4833:4962]` | `test_name="MALDI-TOF and 16S rDNA sequencing"` | `target_concept="Photobacterium damselae and Vibrio harveyi"` | `specimen=wound swab` | `result=POSITIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Based on the combined results of MALDI-TOF and 16S rDNA analysis, we reported P. damselae and V. harveyi as final identification."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Vibrio cholerae is mentioned solely as an exclusion note in the title of the CLSI susceptibility breakpoint standard used to interpret Photobacterium damselae zone diameters.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_TARGET_CASE`** (`step12_dataset_label="EXCLUDED_NON_TARGET_CASE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** A 64-year-old male developed a severe tibial wound infection following a marine laceration in Western Australia, caused by Photobacterium damselae ssp. damselae and Vibrio harveyi (confirmed by MALDI-TOF and 16S rDNA sequencing). Vibrio cholerae is mentioned solely in parenthetical reference to the CLSI antimicrobial susceptibility breakpoint guidelines ('CLSI guidelines for Vibrio ssp. (excluding Vibrio cholerae)') -> EXCLUDED_NON_TARGET_CASE.

### Case 8: `PMC8415062_01::Cholera`
- **Article Title:** Locally transmitted malaria in Tawau, Sabah, Malaysia
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=63.0`, `gender=Male`) — 63-year-old male admitted for stool-culture-confirmed Vibrio cholerae enteritis from 10-15 July 2016 and readmitted on 1 August 2016 with hospital-acquired Plasmodium falciparum malaria.
- **Step 4 — Condition Concept Matched:** Confirmed Vibrio cholerae infection (cholera) with voluminous diarrhea and positive stool culture during hospitalization from 10-15 July 2016
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `AFFIRMED` (`AFFIRMED`)
- **Step 6 — Temporality:** `RECENT_EPISODIC` (`RECENT_EPISODIC`)
- **Step 7 — Clinical Role:** `SECONDARY_DIAGNOSIS` (`ACTIVE_COMORBIDITY`)
- **Step 8 — VPD Case Definition Check:** `CONFIRMED` (`vpd_satisfied=True`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E1_CONFIRMATORY`
  - **Evidence Item 1:** `case_text[1444:1640]` | `test_name="Clinical presentation"` | `target_concept="Cholera (voluminous diarrhea and stomach cramps)"` | `specimen=None` | `result=POSITIVE` | `relation=SUPPORTS` | `strength=E3_SUPPORTIVE`
    > "Prior to his admission for malaria, the patient was admitted for cholera between the 10-15 July. He had presented prior to the 10th with a 3-day history of voluminous diarrhoea and stomach cramps."
  - **Evidence Item 2:** `case_text[1641:1741]` | `test_name="Stool culture"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=POSITIVE` | `relation=SUPPORTS` | `strength=E1_CONFIRMATORY`
    > "Upon testing in the emergency department, he tested positive on a stool culture for Vibrio cholerae."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Three consecutive negative stool samples post-treatment document microbiological clearance following antibiotic therapy, not a contradiction of the confirmed cholera diagnosis.
- **Step 11 — Final Clinical Adjudication Decision:** **`POSITIVE`** (`step12_dataset_label="POSITIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=[]`
  - **Clinical Rationale:** A 63-year-old male was admitted from 10 to 15 July 2016 with a 3-day history of voluminous diarrhea and stomach cramps; emergency department stool culture tested positive for Vibrio cholerae (E1_CONFIRMATORY). He was treated with antibiotics and intravenous fluids and achieved microbiological clearance prior to his subsequent readmission on 1 August 2016 for nosocomially transmitted Plasmodium falciparum malaria acquired during his cholera hospitalization. Assertion AFFIRMED, temporality RECENT_EPISODIC, clinical role SECONDARY_DIAGNOSIS / ACTIVE_COMORBIDITY, VPD satisfied -> POSITIVE.

### Case 9: `PMC9043682_01::Cholera`
- **Article Title:** Successful Treatment of Carbamazepine-Induced Toxic Epidermal Necrolysis With Clinical Gastrointestinal Involvement: A Case Report
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=8.0`, `gender=Female`) — 8-year-old girl with epilepsy and HLA-B*15:02-positive carbamazepine-induced toxic epidermal necrolysis complicated by severe gastrointestinal involvement.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae tested and ruled out via 24-pathogen stool real-time PCR panel and stool culture
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[4829:5341]` | `test_name="Stool real-time multiplex PCR (24 pathogens)"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "However, a stool real-time PCR failed to detect 24 infectious pathogens, involving Vibrio vulnificus, Vibrio parahaemolyticus, Vibrio cholera, Campylobacter spp. (C. jejuni, C. upsaliensis, and C. coli), Salmonella spp., Clostridium difficile (tcdA/tcdB), Yersinia enterocolitica, EAEC, ETEC, STEC, STEC O157:H7, EPEC, EIEC, Plesiomonasshigelloides, Norovirus GI and GII, Rotavirus A, Astrovirus, Spovirus GI, GII, GIV, GV, Entamoebahistolytica, Cryptosporidium spp., Giardia lamblia, and Cyclosporacayetanensis."
  - **Evidence Item 2:** `case_text[5342:5376]` | `test_name="Stool culture"` | `target_concept="Enteric bacterial pathogens including Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Stool cultures were also negative."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Stool real-time PCR for 24 enteric pathogens (explicitly including Vibrio cholerae) and stool cultures were negative.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** An 8-year-old girl with carbamazepine-induced toxic epidermal necrolysis developed severe watery bloody diarrhea (15-20 stools/day) on hospital day 3. Stool real-time PCR failed to detect 24 enteric pathogens including Vibrio cholerae, and stool cultures were also negative, confirming TEN-related gastrointestinal mucosal involvement rather than cholera -> NEGATIVE.

### Case 10: `PMC6180980_01::Cholera`
- **Article Title:** A Case of Malaria Predisposing to Salmonella Bacteremia in a Returning Traveler from Nigeria
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=50.0`, `gender=Female`) — 50-year-old female returning traveler from Lagos, Nigeria diagnosed with Plasmodium falciparum malaria and Salmonella enterica serovar Stanleyville bacteremia.
- **Step 4 — Condition Concept Matched:** Vibrio and Vibrio cholerae tested negative by BioFire FilmArray Gastrointestinal Panel NAAT on stool
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[2754:3335]` | `test_name="BioFire FilmArray Gastrointestinal Panel NAAT"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Nucleic acid amplification-based testing of a stool specimen was negative for adenovirus, Campylobacter, Cyclospora cayetanensis, Clostridium difficile, enteroaggregative Escherichia coli, enteropathogenic E. coli, enterotoxigenic E. coli, Shiga-like toxin producing E. coli, Shigella, enteroinvasive E. coli, Entamoeba histolytica, Giardia lamblia, human astrovirus, norovirus GI/GII, Plesiomonas shigelloides, rotavirus A, Salmonella, sapovirus, Vibrio, Vibrio cholera, and Yersinia enterocolitica (FilmArray  Gastrointestinal Panel, BioFire Diagnostics LLC, Salt Lake City, UT)."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Stool nucleic acid amplification panel was explicitly negative for Vibrio and Vibrio cholerae.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 50-year-old female returning from Nigeria presented with diarrhea, fevers, and syncope, and was diagnosed with Plasmodium falciparum malaria and nontyphoidal Salmonella enterica serovar Stanleyville bacteremia. Stool nucleic acid amplification testing (BioFire FilmArray Gastrointestinal Panel) was explicitly negative for Vibrio and Vibrio cholerae -> NEGATIVE.

### Case 11: `PMC6532487_01::Cholera`
- **Article Title:** Eosinophilic gastroenteritis: Atypical cause for chronic diarrhea in human immunodeficiency virus-associated immunosuppression
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=57.0`, `gender=Male`) — 57-year-old HIV-positive Indian male presenting with 4 months of large-volume watery diarrhea diagnosed as eosinophilic gastroenteritis.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae tested negative on stool analysis and culture
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[1061:1217]` | `test_name="Stool analysis and culture"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Stool analysis including culture was negative for Clostridium difficile toxin, Cryptosporidium, Vibrio cholerae, acid-fast bacteria, or any other parasites."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Stool analysis including culture was negative for Vibrio cholerae; duodenal biopsy confirmed eosinophilic gastroenteritis.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 57-year-old male with HIV presented with 4 months of large-volume watery diarrhea and 20 kg weight loss. Stool analysis including culture was explicitly negative for Vibrio cholerae, Clostridium difficile toxin, Cryptosporidium, and acid-fast bacteria, and upper gastrointestinal biopsies established eosinophilic gastroenteritis -> NEGATIVE.

### Case 12: `PMC9083785_01::Cholera`
- **Article Title:** Ulcerative colitis after SARS-CoV-2 infection
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=74.0`, `gender=Male`) — 74-year-old male presenting with bloody diarrhea and fever one month after SARS-CoV-2 infection, diagnosed with new-onset ulcerative colitis.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae tested negative via stool cultures and gastrointestinal multiplex PCR panel
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[1222:1449]` | `test_name="Stool culture and gastrointestinal PCR panel"` | `target_concept="Enteric pathogens including Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Stool studies, including cultures for common pathogens, parasites, tests for Clostridium difficile GDH, toxins A and B all returned negative. Moreover, the gastrointestinal PCR panel test for common pathogens was also negative."
  - **Evidence Item 2:** `case_text[1450:1912]` | `test_name="Gastrointestinal PCR panel target specification"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "This panel test targets bacterial infections (Campylobacter jejuni, Campylobacter coli, C. difficile toxin A/B, Salmonella spp, Vibrio cholerae, Yersinia enterocolitica, Enteroaggregative E. coli, Enteropathogenic E. coli, Enterotoxigenic E. coli, Shigella-like toxin-producing E. coli, Shigella spp), parasitic infections (Cryptosporidium, Entamoeba histolytica, Giardia lamblia) and viral infections (Adenovirus, Astrovirus, Norovirus, Rotavirus A, Sapovirus)."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Stool cultures and gastrointestinal PCR panel targeting Vibrio cholerae were negative; colonoscopy and biopsy confirmed ulcerative colitis.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 74-year-old male developed fever and bloody diarrhea one month after COVID-19. Stool cultures and a gastrointestinal PCR panel targeting Vibrio cholerae and other enteric pathogens were all negative, and ileocolonoscopy with biopsy established new-onset ulcerative colitis -> NEGATIVE.

### Case 13: `PMC9996308_02::Cholera`
- **Article Title:** Case report: Fecal microbiota transplantation in refractory ankylosing spondylitis
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=26.0`, `gender=Female`) — Patient with refractory ankylosing spondylitis and ulcerative colitis undergoing fecal microbiota transplantation (FMT); Vibrio cholerae stool culture was performed on the healthy stool donors (26-year-old man and 36-year-old woman), not the recipient patient.
- **Step 4 — Condition Concept Matched:** Pre-FMT donor stool screening culture for Vibrio cholerae in healthy donors
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[252:916]` | `test_name="FMT donor screening stool culture"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "Briefly, a preliminary questionnaire including queries on medical history and lifestyle habits was used to exclude any exposure to infectious agents or risky behaviors, and laboratory examinations, including serology screening tests for HIV, hepatitis A, B, C, and E, syphilis, Epstein-Barr virus, cytomegalovirus, and rotavirus, and stool culturing for enteric pathogens including Escherichia coli O157, Salmonella spp., Shigella spp., Campylobacter spp., Staphylococcus aureus, Yersinia, Vibrio parahaemolyticus, Vibrio cholerae, Candida albicans, Clostridium difficile toxin A/B, ova, and parasites was performed to avoid a potential infection risk through FMT."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Stool culture for Vibrio cholerae was performed solely on healthy FMT donors to prevent transmission risk, not as a clinical evaluation of the patient.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_TARGET_CASE`** (`step12_dataset_label="EXCLUDED_NON_TARGET_CASE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F3_SUBJECT_COREFERENCE', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** Case report of a patient with refractory ankylosing spondylitis and comorbid ulcerative colitis treated with three fecal microbiota transplantations (FMTs). Vibrio cholerae is mentioned exclusively as part of the routine infectious screening stool culture performed on the two healthy stool donors prior to FMT to avoid transmission risk -> EXCLUDED_NON_TARGET_CASE.

### Case 14: `PMC8383206_01::Cholera`
- **Article Title:** Case Report: Near-Fatal Intestinal Hemorrhage and Acute Acalculous Cholecystitis due to Vi-Negative and Fluoroquinolone-Insensitive Salmonella enterica Serovar Typhi Infection: A Rare Entity
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=21.0`, `gender=Male`) — 21-year-old Mexican male in China with Vi-negative Salmonella enterica serovar Typhi typhoid fever complicated by acute acalculous cholecystitis and massive intestinal hemorrhage.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae O1/O139 tested negative by both rapid test and fecal bacterial isolation
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[1136:1195]` | `test_name="Rapid test for Vibrio cholerae O1/O139"` | `target_concept="Vibrio cholerae O1/O139"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Rapid tests for Vibrio cholerae O1/O139 were also negative."
  - **Evidence Item 2:** `case_text[2503:2886]` | `test_name="Fecal bacterial isolation"` | `target_concept="Vibrio cholerae O1/O139"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "The following test results were negative: the full panel for hepatitis; serologic tests for hantavirus, EB virus, and TORCH (Toxoplasma gondii, rubella, cytomegalovirus, herpes simplex virus, and other pathogenic microorganisms); nucleic acid assay for cytomegalovirus, EB virus, and the new Bunya virus; fecal bacterial isolation of V. cholerae O1/O139 and Escherichia coli O157:H7."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Both rapid tests and fecal bacterial isolation for Vibrio cholerae O1/O139 were negative; blood culture confirmed Salmonella enterica serovar Typhi.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 21-year-old male presented with fever, watery diarrhea, jaundice, acute acalculous cholecystitis, and massive lower gastrointestinal bleeding. Rapid testing for Vibrio cholerae O1/O139 at the initial hospital and fecal bacterial isolation of V. cholerae O1/O139 at the referral hospital were both explicitly negative, while blood cultures confirmed Salmonella enterica serovar Typhi -> NEGATIVE.

### Case 15: `PMC4967050_02::Cholera`
- **Article Title:** How to communicate climate change 'impact and solutions' to vulnerable population of Indian Sundarbans? From theory to practice
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `EXCLUDED_NON_CASE_REPORT` (`AGGREGATE_COHORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `NON_CLINICAL_DOCUMENT`
- **Step 3 — Patient Anchor:** `none` (`anchor_type=NONE_COHORT`, `age=None`, `gender=Unknown`) — Socio-environmental community adaptation project among 2,100 families in the Indian Sundarbans; not a medical case report.
- **Step 4 — Condition Concept Matched:** Background mention of post-cyclone waterborne epidemics ('epidemics like Cholera/Typhoid/dysentery')
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `NOT_APPLICABLE` (`POSSIBLE_HYPOTHETICAL`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[9151:9410]` | `test_name="Disaster hazard background description"` | `target_concept="Cholera"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "Lastly, the deaths of livestock animal/fresh water fishes due to drowning and purification of their flesh contaminate the fresh water sources resulting in epidemics like Cholera/Typhoid/dysentery and other water borne diseases amongst the stranded population."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Non-clinical socio-environmental paper mentioning cholera only as a general hazard following cyclones.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_CASE_REPORT`** (`step12_dataset_label="EXCLUDED_NON_SINGLE_PATIENT"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** Socio-environmental study describing a participatory climate change adaptation, mangrove restoration, and microfinance project involving 2,100 vulnerable families in the Indian Sundarbans (NON_CLINICAL_DOCUMENT / AGGREGATE_STUDY_UNIT). Cholera is mentioned once as a general example of waterborne epidemics following cyclone-induced freshwater contamination -> EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 16: `PMC4588357_01::Cholera`
- **Article Title:** Stem Cell Therapy for Corneal Epithelium Regeneration following Good Manufacturing and Clinical Procedures
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `EXCLUDED_NON_CASE_REPORT` (`AGGREGATE_COHORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `AGGREGATE_STUDY_UNIT`
- **Step 3 — Patient Anchor:** `none` (`anchor_type=NONE_COHORT`, `age=None`, `gender=Unknown`) — Prospective interventional cohort study of 20 eyes with limbal stem cell deficiency undergoing cultivated limbal epithelial transplantation (CLET).
- **Step 4 — Condition Concept Matched:** In-vitro cell culture reagent '0.5 ng/mL cholera toxin' added to DMEM/F12 medium for limbal epithelial cell expansion
- **Step 5 — Concept Grounding & Assertion:** Grounding = `NON_TARGET_CONCEPT` | Assertion = `NOT_APPLICABLE` (`UNCERTAIN`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[1713:2203]` | `test_name="Cell culture medium preparation"` | `target_concept="Cholera toxin reagent (0.5 ng/mL)"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "After 24 hr., 3 mL of the following culture medium was added: DMEM/F12 media (1 : 1 mixture) (Life Technologies-Gibco), 5% FBS (Life Technologies-Gibco), 50 mug/mL hydrocortisone (Sigma Aldrich, St Louis, MO, USA), 0.5 ng/mL cholera toxin (Gentaur, Kampenhout, Belgium), 5 ng/mL insulin-transferrin-selenium (ITS) (Sigma Aldrich), 0.5% dimethyl sulfoxide (Sigma Aldrich), 2.5 ng/mL human epidermal growth factor (Life Technologies-Gibco), and 0.5 mg/mL gentamicin (Life Technologies-Gibco)."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Prospective 20-eye study where cholera toxin is used solely as a biochemical supplement in ex-vivo cell culture media.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_CASE_REPORT`** (`step12_dataset_label="EXCLUDED_NON_SINGLE_PATIENT"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F1_LEXICAL_HOMONYM', 'F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** Prospective interventional study of 20 eyes with limbal stem cell deficiency treated with cultivated limbal epithelial transplantation (AGGREGATE_STUDY_UNIT). The word 'cholera' appears solely in the GMP cell culture protocol where '0.5 ng/mL cholera toxin' is used as a mitogenic media supplement for ex-vivo epithelial cell proliferation -> EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 17: `PMC10641789_01::Cholera`
- **Article Title:** Cryptosporidiosis diagnosed using metagenomic next-generation sequencing in a healthy child admitted to pediatric intensive care unit: a case report
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=10.0`, `gender=Male`) — 10-year-old boy admitted to PICU with severe Cryptosporidium parvum diarrhea, hypovolemic shock, rhabdomyolysis, acute kidney injury, and pancreatitis.
- **Step 4 — Condition Concept Matched:** Vibrio cholerae slide agglutination test explicitly negative
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[4293:4455]` | `test_name="Vibrio cholerae slide agglutination test"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Furthermore, PCR results of Entamoeba trophozoites and cysts, Enterovirus 71, Coxsackie virus A16, and Vibrio cholerae slide agglutination test were all negative."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Vibrio cholerae slide agglutination test was negative, and blood/anal-swab mNGS confirmed Cryptosporidium parvum.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 10-year-old immunocompetent boy presented to the PICU with severe watery diarrhea, shock, rhabdomyolysis, acute kidney injury, and pancreatitis. A Vibrio cholerae slide agglutination test was explicitly negative, and metagenomic next-generation sequencing (mNGS) of blood and anal swabs confirmed Cryptosporidium parvum infection -> NEGATIVE.

### Case 18: `PMC10945545_01::Cholera`
- **Article Title:** Case report: Rapidly progressive neurocognitive disorder with a fatal outcome in a patient with PU.1 mutated agammaglobulinemia
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=38.0`, `gender=Female`) — 38-year-old female with PU.1-mutated agammaglobulinemia, chronic enteropathy, recurrent infections, and fatal rapidly progressive neurocognitive disorder.
- **Step 4 — Condition Concept Matched:** Vibrio (V. parahaemolyticus/V. vulnificus/V. cholerae) and Vibrio cholerae tested on gastrointestinal multiplex PCR panel, which detected only Clostridioides difficile (toxin A/B) alongside Norovirus GI/GII
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`RECENT_EPISODIC`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[6429:7193]` | `test_name="Gastrointestinal multiplex PCR panel"` | `target_concept="Vibrio cholerae"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "A gastrointestinal multiplex PCR panel (Campylobacter (C. jejuni/C. coli/C. upsaliensis), Clostridioides (Clostridium) difficile (toxin A/B), Plesiomonas shigelloides, Salmonella, Yersinia enterocolitica, Vibrio (V. parahaemolyticus/V. vulnificus/V. cholerae), Vibrio cholerae, Enteroaggregative E. coli, Enteropathogenic E. coli, Enterotoxigenic E. coli lt/st, Shiga-like toxin-producing E. coli stx1/stx2, E. coli O157, Shigella/Enteroinvasive E. coli; Cryptosporidium, Cyclospora cayetanensis, Entamoeba histolytica, Giardia lamblia; Adenovirus F40/41, Astrovirus, Norovirus GI/GII, Rotavirus A, Sapovirus (I, II, IV, and V) also revealed Clostridium difficile (toxin A/B), and the patient was treated with oral vancomycin at a daily dose of 500 mg for 14 days."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Gastrointestinal multiplex PCR panel covering Vibrio cholerae detected only Clostridioides difficile toxin A/B (in addition to Norovirus GI/GII RNA).
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL']`
  - **Clinical Rationale:** A 38-year-old female with PU.1-mutated agammaglobulinemia underwent stool microbiological testing during a severe diarrheal episode prior to her neurocognitive decline. Stool testing identified Norovirus GI/GII RNA, and a 22-target gastrointestinal multiplex PCR panel (explicitly including Vibrio and Vibrio cholerae) detected only Clostridioides difficile (toxin A/B), ruling out cholera -> NEGATIVE.

### Case 19: `PMC11338764_01::Cholera`
- **Article Title:** Ceftriaxone-resistant Salmonella enterica serovar Newport: a case report from South India
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=60.0`, `gender=Female`) — 60-year-old female presenting with acute watery gastroenteritis and shock, diagnosed with ceftriaxone-resistant Salmonella enterica serovar Newport.
- **Step 4 — Condition Concept Matched:** Empirical IV doxycycline initiated to cover suspected Vibrio cholerae, then discontinued after stool culture and NICED reference speciation confirmed oxidase-negative Salmonella enterica serovar Newport
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[1259:1548]` | `test_name="Empirical antibiotic therapy"` | `target_concept="Vibrio cholerae (empirical coverage)"` | `specimen=None` | `result=INDETERMINATE` | `relation=INCONCLUSIVE` | `strength=E3_SUPPORTIVE`
    > "In view of the shock caused by gastroenteritis, the patient was empirically started on piperacillin-tazobactam 4.5 g QID to empirically cover Gram-negative infections, doxycycline (injection) 100 mg BD to cover Vibrio cholerae, and metronidazole (injection) 500 mg TID to cover protozoans."
  - **Evidence Item 2:** `case_text[4643:4922]` | `test_name="Stool culture and reference serotyping at NICED"` | `target_concept="Salmonella enterica serovar Newport"` | `specimen=stool` | `result=POSITIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Consequently, the isolate was forwarded to the National Institute of Cholera and Enteric Diseases (NICED) in Kolkata, West Bengal, India, for speciation and serotyping. The NICED report identified the isolate as Salmonella enterica serovar Newport with resistance to ceftriaxone."
  - **Evidence Item 3:** `case_text[4923:5112]` | `test_name="Definitive treatment reconciliation"` | `target_concept="Vibrio cholerae ruled out (doxycycline stopped)"` | `specimen=None` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Once gastroenteritis due to NTS with ceftriaxone resistance was diagnosed, the injection of piperacillin-tazobactam was continued for 9 days, and doxycycline and metronidazole were stopped."
- **Step 10 — Contradiction Assessment:** `RESOLVED_BY_LATER_CONFIRMATORY_TEST` (`contradiction_flag=True`) — Initial empirical coverage with IV doxycycline for suspected Vibrio cholerae was discontinued once stool culture grew cytochrome-oxidase-negative bacilli identified by the National Institute of Cholera and Enteric Diseases (NICED) as Salmonella enterica serovar Newport.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** A 60-year-old woman presented with acute watery diarrhea, vomiting, and shock and received empirical intravenous doxycycline to cover Vibrio cholerae alongside piperacillin-tazobactam and metronidazole. Stool culture isolated cytochrome-oxidase-negative, non-lactose-fermenting Gram-negative bacilli confirmed by the National Institute of Cholera and Enteric Diseases (NICED) as ceftriaxone-resistant Salmonella enterica serovar Newport, leading to discontinuation of doxycycline -> NEGATIVE.

### Case 20: `PMC10481634_22::Cholera`
- **Article Title:** Between the personal and the political: life experiences during the covid-19 pandemic in Tucumán, Argentina, 2020-2022
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `EXCLUDED_NON_CASE_REPORT` (`AGGREGATE_COHORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `NON_CLINICAL_DOCUMENT`
- **Step 3 — Patient Anchor:** `none` (`anchor_type=NONE_COHORT`, `age=47.0`, `gender=Male`) — Sociological mixed-methods discourse analysis of COVID-19 pandemic experiences in Tucuman, Argentina (including a quote from Survey 199, a 47-year-old male citizen); not a clinical case report.
- **Step 4 — Condition Concept Matched:** Sociological historiography quote citing cholera as an example of how microorganisms acquire cultural and political meaning
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `NOT_APPLICABLE` (`UNCERTAIN`)
- **Step 6 — Temporality:** `NOT_APPLICABLE` (`UNKNOWN`)
- **Step 7 — Clinical Role:** `EPIDEMIOLOGICAL_CONTEXT` (`EPIDEMIOLOGICAL_CONTEXT`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E4_CONTEXT`
  - **Evidence Item 1:** `case_text[1345:1680]` | `test_name="Sociological historiography quotation"` | `target_concept="Cholera (sociological metaphor)"` | `specimen=None` | `result=NOT_APPLICABLE` | `relation=REFUTES` | `strength=E4_CONTEXT`
    > "Like any other disease, cholera has in itself no meaning: it is only a microorganism. It acquires meaning and significance from its human context, from the ways in which it infiltrates the lives of the people, from the reactions it provokes, and from the manner in which it gives expression to cultural and political values ( , p.151)."
- **Step 10 — Contradiction Assessment:** `NONE` (`contradiction_flag=False`) — Non-clinical social science article citing cholera in a theoretical quote on epidemic historiography.
- **Step 11 — Final Clinical Adjudication Decision:** **`EXCLUDED_NON_CASE_REPORT`** (`step12_dataset_label="EXCLUDED_NON_SINGLE_PATIENT"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F2_SCOPE_COHORT', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** Sociological mixed-methods discourse analysis examining personal and political framing during the COVID-19 pandemic in Tucuman, Argentina (NON_CLINICAL_DOCUMENT). Cholera is mentioned solely in a theoretical historiography quotation illustrating how epidemics acquire cultural and political meaning -> EXCLUDED_NON_CASE_REPORT / EXCLUDED_NON_SINGLE_PATIENT.

### Case 21: `PMC11754817_01::Cholera`
- **Article Title:** Clinical case of co-infection: Dengue fever and respiratory mycoplasmosis in a child
- **Retrieval Metadata (Ignored for Ground-Truth Decision):** `confidence_tier=None`, `evidence_score=None`, `matched_evidence_terms=None`
- **Step 1 — Document Type:** `CLINICAL_CASE_REPORT` (`CLINICAL_CASE_REPORT`)
- **Step 2 — CCU Type (Unit of Analysis):** `PRIMARY_CARE_EPISODE`
- **Step 3 — Patient Anchor:** `patient_1` (`anchor_type=PRIMARY_PATIENT`, `age=14.0`, `gender=Female`) — 14-year-old female returning to Moscow from the Maldives with imported dengue fever and respiratory Mycoplasma pneumoniae co-infection.
- **Step 4 — Condition Concept Matched:** Differential diagnostic examination for cholera performed and excluded in a patient with confirmed dengue fever and Mycoplasma pneumoniae co-infection
- **Step 5 — Concept Grounding & Assertion:** Grounding = `TARGET_CONFIRMED` | Assertion = `ABSENT_NEGATIVE` (`NEGATED`)
- **Step 6 — Temporality:** `CURRENT_EPISODE` (`CURRENT_ACTIVE`)
- **Step 7 — Clinical Role:** `RULED_OUT_DIAGNOSIS` (`RULED_OUT_DIAGNOSIS`)
- **Step 8 — VPD Case Definition Check:** `NOT_MET` (`vpd_satisfied=False`)
- **Step 9 — Evidence Strength & Grounded Spans:** `E0_CONTRADICTED`
  - **Evidence Item 1:** `case_text[3964:4194]` | `test_name="Differential diagnostic workup for cholera"` | `target_concept="Vibrio cholerae / Cholera"` | `specimen=stool` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "For differential diagnostics, examination for malaria and cholera, acute intestinal infections, herpes virus infections, and examination of oropharyngeal swab materials for nucleic acids of 16 respiratory pathogens were performed."
  - **Evidence Item 2:** `case_text[7826:8146]` | `test_name="Final clinical adjudication"` | `target_concept="Dengue fever and Mycoplasma pneumoniae co-infection (cholera excluded)"` | `specimen=None` | `result=NEGATIVE` | `relation=REFUTES` | `strength=E0_CONTRADICTED`
    > "Thus, based on the data of the disease history, epidemiological anamnesis, complaints, physical and laboratory-instrumental examination data, the final diagnosis was established. The primary diagnosis: dengue fever of moderate severity. The secondary diagnosis: mycoplasma infection (M. pneumoniae) of moderate severity."
- **Step 10 — Contradiction Assessment:** `CONFIRMATORY_TEST_NEGATIVE` (`contradiction_flag=False`) — Differential diagnostic testing for malaria, cholera, and acute intestinal infections excluded cholera; dengue virus RNA NAAT and M. pneumoniae IgM confirmed the final co-infection diagnosis.
- **Step 11 — Final Clinical Adjudication Decision:** **`NEGATIVE`** (`step12_dataset_label="NEGATIVE"`)
- **Step 12 — Audit Trail & Rationale:** `confidence=HIGH` | `failure_flags=['F4_ASSERTION_TEMPORAL', 'F5_DISCOURSE_CONTEXT']`
  - **Clinical Rationale:** A 14-year-old girl returning to Moscow from the Maldives presented with fever, rash, epistaxis, cough, abdominal pain, and liquid stools. Differential diagnostic testing for malaria, cholera, and acute intestinal infections was performed, and the final confirmed diagnoses were moderate dengue fever (positive blood dengue antigen RDT and arbovirus RNA NAAT) and Mycoplasma pneumoniae respiratory co-infection (positive M. pneumoniae IgM), ruling out cholera -> NEGATIVE.

# Nocardiosis annotation — per-case rationale and audit trail

**Input:** `input_nocardiosis.jsonl` (204 records)  
**Target disease:** Nocardiosis  
**Protocol:** supplied Nocardiosis SKILL + Clinical Claim Ontology, Schema, Evidence Specificity Matrix, and Gold-Standard 12-step Protocol  
**Date:** 2026-11-16  
**Review status:** one semantic annotation pass; not independently adjudicated by two clinicians.

## Dataset-level summary

- Total records annotated: **204**
- POSITIVE: **128**
- NEGATIVE: **33**
- INCONCLUSIVE_DATA: **15**
- EXCLUDED_NON_TARGET_CASE: **22**
- EXCLUDED_NON_CASE_REPORT: **6**

## Method and interpretation notes

The annotation unit was the supplied JSONL row. Each `case_text` was read as the clinical narrative; the candidate tier, retrieval signals, and disease match metadata were not treated as diagnostic evidence. The target remained fixed to Nocardiosis. Disease mentions were interpreted through patient anchoring, assertion, temporality, clinical role, evidence specificity, and contradiction reconciliation.

For POSITIVE, the strict standard required a patient-attributed E1 confirmatory result or E2 highly specific evidence supported by coherent current clinical context. E3-only cases were not promoted to strict positives. Coinfections were preserved as positives when the Nocardia claim had its own support. Historical Nocardiosis, asymptomatic respiratory isolation without a compatible active episode, and false attribution to a subsequently identified alternative organism were not counted as current positives.

The JSONL evidence items use a conservative **whole-`case_text` span** (0-based, end-exclusive) where a patient-level Nocardia-related result or contradiction is present. This guarantees that each quote is verbatim and offset-valid, but it is broader than an ideal minimal sentence-level evidence span. The separate rationale identifies the specific test/result to guide review. Records without patient-anchored target evidence in `case_text` have an empty evidence item list rather than fabricated offsets from the title/abstract.

Records split across multiple JSONL rows were adjudicated independently. Evidence from a neighboring fragment was not imported into a row whose supplied `case_text` did not contain it. This produces INCONCLUSIVE_DATA for some incomplete fragments even where the shared article abstract or a neighboring row contains the later diagnosis.

This is a single-agent research annotation and is **not a substitute for independent clinical adjudication**. In particular, cases with low-read mNGS detections, non-sterile respiratory specimens, species-level uncertainty, or incomplete narrative fragments merit expert review before inclusion as gold-standard labels.

## Per-case annotations

### 1. `PMC9852504_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (54-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** EBUS-guided aspirate showed partially acid-fast branching beaded rods; mNGS/16S and culture identified Nocardia species.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** EBUS-guided aspirate showed partially acid-fast branching beaded rods; mNGS/16S and culture identified Nocardia species. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 2. `PMC4363670_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (46-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** The patient had disseminated pulmonary, adrenal and cerebral disease; Nocardia was recovered from adrenal abscess material, although species-level confirmation is not documented in the supplied narrative.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The patient had disseminated pulmonary, adrenal and cerebral disease; Nocardia was recovered from adrenal abscess material, although species-level confirmation is not documented in the supplied narrative. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 3. `PMC8183679_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (61-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Blood and bronchoalveolar lavage metagenomic sequencing identified Nocardia farcinica in the current episode.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Blood and bronchoalveolar lavage metagenomic sequencing identified Nocardia farcinica in the current episode. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 4. `PMC10115452_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (77-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Skin lesion material showed branching partially acid-fast organisms and MALDI-TOF identified Nocardia brasiliensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Skin lesion material showed branching partially acid-fast organisms and MALDI-TOF identified Nocardia brasiliensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 5. `PMC10115452_02::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (63-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The full case narrative was reviewed against the Nocardiosis evidence matrix.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The full case narrative was reviewed against the Nocardiosis evidence matrix. The abstract refers to Nocardia in another patient from the same report, but this row’s case_text is the Mycobacterium marinum patient; no evidence is transferred across patient anchors. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The abstract refers to Nocardia in another patient from the same report, but this row’s case_text is the Mycobacterium marinum patient; no evidence is transferred across patient anchors.

### 6. `PMC6643105_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (53-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pulmonary and cerebral nocardiosis was supported by Nocardia asteroides culture and molecular identification.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pulmonary and cerebral nocardiosis was supported by Nocardia asteroides culture and molecular identification. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 7. `PMC4894989_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (59-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** The narrative describes a compatible pulmonary syndrome and treatment for Nocardia, but the supplied case text does not document a definitive species-specific result.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The narrative describes a compatible pulmonary syndrome and treatment for Nocardia, but the supplied case text does not document a definitive species-specific result. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 8. `PMC9127990_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (61-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Blood culture isolate was resolved by 16S rRNA sequencing as Nocardia vulneris despite discordant preliminary phenotypic/MALDI findings.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Blood culture isolate was resolved by 16S rRNA sequencing as Nocardia vulneris despite discordant preliminary phenotypic/MALDI findings. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 9. `PMC9006427_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_CASE_REPORT | **Document:** SYSTEMATIC_REVIEW | **CCU:** AGGREGATE_STUDY_UNIT
- **Patient anchor:** No eligible single-human patient anchor in this record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / BACKGROUND_LITERATURE_REFERENCE
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The record is a systematic review aggregating organisms from nipple-piercing infections; it does not provide one eligible index patient with a Nocardia claim.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The record is a systematic review aggregating organisms from nipple-piercing infections; it does not provide one eligible index patient with a Nocardia claim. Systematic review of organisms in piercing-associated infections; no separable single-human Nocardiosis CCU. The document/unit is outside the eligible single-human-patient case-report target; excluded as EXCLUDED_NON_CASE_REPORT.
- **Audit note:** Systematic review of organisms in piercing-associated infections; no separable single-human Nocardiosis CCU.

### 10. `PMC6399552_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (56-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia was considered, but bronchial lavage fungal PCR identified Rhizomucor pusillus, providing a competing explanation without Nocardia confirmation.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Rhizomucor pusillus was identified by fungal PCR; no Nocardia confirmation.
- **Adjudication rationale:** Nocardia was considered, but bronchial lavage fungal PCR identified Rhizomucor pusillus, providing a competing explanation without Nocardia confirmation. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 11. `PMC9128046_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (51-year-old female index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** Nocardia appears among organisms in a polymicrobial terminal infection narrative, but the supplied text does not specify a patient-linked confirmatory Nocardia test.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia appears among organisms in a polymicrobial terminal infection narrative, but the supplied text does not specify a patient-linked confirmatory Nocardia test. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 12. `PMC9234165_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (52-year-old female index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / TEST_RESULT
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** BAL metagenomic sequencing detected Nocardia gelsenkircheni, but the article narrative does not establish that this finding was adjudicated as active nocardiosis rather than an incidental detection in recurrent respiratory disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL metagenomic sequencing detected Nocardia gelsenkircheni, but the article narrative does not establish that this finding was adjudicated as active nocardiosis rather than an incidental detection in recurrent respiratory disease. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 13. `PMC4213137_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The ocular lesion workup identified Candida albicans; the Nocardia differential was not confirmed and an alternative organism was recovered.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Candida albicans was recovered from the ocular specimen and explains the lesion.
- **Adjudication rationale:** The ocular lesion workup identified Candida albicans; the Nocardia differential was not confirmed and an alternative organism was recovered. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 14. `PMC6936928_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (93-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia PCR from the lymph-node specimen was negative and Mycobacterium tuberculosis was confirmed by culture.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia PCR negative; tuberculosis confirmed.
- **Adjudication rationale:** Nocardia PCR from the lymph-node specimen was negative and Mycobacterium tuberculosis was confirmed by culture. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 15. `PMC2799960_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (83-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** The patient had a compatible pulmonary/cerebral disseminated syndrome and sputum evidence reported as Nocardia species; evidence is strong but not species-level confirmation from a sterile site.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The patient had a compatible pulmonary/cerebral disseminated syndrome and sputum evidence reported as Nocardia species; evidence is strong but not species-level confirmation from a sterile site. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 16. `PMC9391167_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Nocardia species was cultured from sputum in a renal-transplant recipient with progressive pulmonary disease and treated as nocardiosis; species-level identification is not supplied.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia species was cultured from sputum in a renal-transplant recipient with progressive pulmonary disease and treated as nocardiosis; species-level identification is not supplied. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 17. `PMC9880008_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_SERIES | **CCU:** MULTI_PATIENT_CASE_SERIES
- **Patient anchor:** patient_1 (62-year-old female), patient_2 (2-year-old male), and patient_3 (56-year-old female); each has a separately described Nocardia infection confirmed by culture and 16S sequencing
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** The record describes multiple separately described human patients with Nocardia confirmed by 16S testing; this row is retained as a positive series-level record because it contains patient-level case narratives.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The record describes multiple separately described human patients with Nocardia confirmed by 16S testing; this row is retained as a positive series-level record because it contains patient-level case narratives. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 18. `PMC4489939_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (27-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** The mycetoma was described as probably Nocardia, but cultures were negative and morphology/therapeutic response were not sufficiently specific.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The mycetoma was described as probably Nocardia, but cultures were negative and morphology/therapeutic response were not sufficiently specific. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 19. `PMC8053466_02::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (58-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia cultures from the brain-abscess workup were negative; the case did not establish nocardiosis.
- **Contradiction resolution:** C1_NEGATIVE_TEST: Nocardia culture from the brain-abscess workup was negative.
- **Adjudication rationale:** Nocardia cultures from the brain-abscess workup were negative; the case did not establish nocardiosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 20. `PMC5350350_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (unknown index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Tissue demonstrated Gram-positive branching partially acid-fast filaments and culture identified Nocardia brasiliensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Tissue demonstrated Gram-positive branching partially acid-fast filaments and culture identified Nocardia brasiliensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 21. `PMC5350350_03::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (unknown index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** This is a follow-up fragment with clinical response during anti-Nocardia therapy but no Nocardia-specific diagnostic evidence in this supplied segment.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a follow-up fragment with clinical response during anti-Nocardia therapy but no Nocardia-specific diagnostic evidence in this supplied segment. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 22. `PMC9830566_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (59-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Blood and BAL metagenomic sequencing identified Nocardia farcinica in a patient with pulmonary infection and bacteremia.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Blood and BAL metagenomic sequencing identified Nocardia farcinica in a patient with pulmonary infection and bacteremia. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 23. `PMC7471810_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (79-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Plasma sequencing and post-mortem tissue morphology supported Nocardia in a brain-abscess presentation, with fungal coinfection also documented.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Plasma sequencing and post-mortem tissue morphology supported Nocardia in a brain-abscess presentation, with fungal coinfection also documented. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 24. `PMC7301693_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (0-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia testing was negative in the infant’s workup; Pneumocystis jirovecii was the relevant diagnosis.
- **Contradiction resolution:** C1_NEGATIVE_TEST: Nocardia investigation was negative.
- **Adjudication rationale:** Nocardia testing was negative in the infant’s workup; Pneumocystis jirovecii was the relevant diagnosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 25. `PMC8046554_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (0-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The patient’s infection was attributed to Mycobacterium abscessus; Nocardia is only laboratory/context wording, not a patient diagnosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The patient’s infection was attributed to Mycobacterium abscessus; Nocardia is only laboratory/context wording, not a patient diagnosis. The patient is described with Mycobacterium abscessus; Nocardia is only a laboratory department name. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The patient is described with Mycobacterium abscessus; Nocardia is only a laboratory department name.

### 26. `PMC6694281_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** ANIMAL_CASE
- **Patient anchor:** animal_1 (non-human subject; outside the human benchmark)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This is a canine Nocardia infection and is outside the human-patient benchmark.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a canine Nocardia infection and is outside the human-patient benchmark. Veterinary dog case; non-human subject. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Veterinary dog case; non-human subject.

### 27. `PMC2852743_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (45-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Bronchoalveolar lavage culture identified Nocardia nova in a kidney-transplant recipient with active cavitary pulmonary disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Bronchoalveolar lavage culture identified Nocardia nova in a kidney-transplant recipient with active cavitary pulmonary disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 28. `PMC2874368_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (39-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / HISTORICAL_RESOLVED / PAST_HISTORY
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The patient had a history of nocardial serositis, but current BAL/fluid investigations were negative and H1N1 influenza was confirmed.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: current Nocardia studies negative; H1N1 influenza confirmed; Nocardia is historical.
- **Adjudication rationale:** The patient had a history of nocardial serositis, but current BAL/fluid investigations were negative and H1N1 influenza was confirmed. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 29. `PMC9113660_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (34-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The patient’s peritonitis was caused by Tsukamurella; Nocardia is not a patient-level diagnosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The patient’s peritonitis was caused by Tsukamurella; Nocardia is not a patient-level diagnosis. Nocardia is not the index patient diagnosis; Tsukamurella caused the reported peritonitis. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Nocardia is not the index patient diagnosis; Tsukamurella caused the reported peritonitis.

### 30. `PMC9432383_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (35-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The patient’s endocarditis was attributed to Corynebacterium striatum; Nocardia appears only in methodological/background text.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The patient’s endocarditis was attributed to Corynebacterium striatum; Nocardia appears only in methodological/background text. Nocardia is only a technical/phylogenetic mention; the patient condition is Corynebacterium striatum endocarditis. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Nocardia is only a technical/phylogenetic mention; the patient condition is Corynebacterium striatum endocarditis.

### 31. `PMC7468610_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (40-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Nocardia was demonstrated in BAL microbiology and surgical lung tissue in an immunocompromised patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia was demonstrated in BAL microbiology and surgical lung tissue in an immunocompromised patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 32. `PMC9490265_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Nocardia farcinica was isolated from sputum in a liver-transplant recipient with active pneumonia; the respiratory specimen and syndrome support a probable diagnosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia farcinica was isolated from sputum in a liver-transplant recipient with active pneumonia; the respiratory specimen and syndrome support a probable diagnosis. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 33. `PMC8486545_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (33-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia cultures from BAL were negative and an alternative infectious workup was pursued.
- **Contradiction resolution:** C1_NEGATIVE_TEST: BAL Nocardia cultures negative.
- **Adjudication rationale:** Nocardia cultures from BAL were negative and an alternative infectious workup was pursued. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 34. `PMC7169360_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** ANIMAL_CASE
- **Patient anchor:** animal_1 (non-human subject; outside the human benchmark)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This is a feline cryptococcal case, not a human Nocardiosis case.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a feline cryptococcal case, not a human Nocardiosis case. Veterinary cat case; non-human subject. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Veterinary cat case; non-human subject.

### 35. `PMC4070928_02::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_SERIES | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (46-year-old Albanian male; identified as Patient 2 in the source article)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The record is a two-patient mycetoma report attributed to Actinomadura madurae; Nocardia is background differential material.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The record is a two-patient mycetoma report attributed to Actinomadura madurae; Nocardia is background differential material. Two mycetoma cases attributed to Actinomadura madurae; Nocardia appears only as background differential/literature. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The supplied row is an extracted narrative for one index patient (the article labels him Patient 2); other patients occur only in comparative/background discussion. The index patient’s mycetoma is attributed to Actinomadura madurae, so Nocardiosis remains non-target.

### 36. `PMC9445126_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (2-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** The narrative labels new lymphadenitis/cavitary pulmonary lesions as Nocardia in a child with CGD, but the supplied text lacks a documented disease-specific microbiological result.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The narrative labels new lymphadenitis/cavitary pulmonary lesions as Nocardia in a child with CGD, but the supplied text lacks a documented disease-specific microbiological result. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 37. `PMC3768339_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (20-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia tests/stains were negative and the final explanation was crystal-storing histiocytosis.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: crystal-storing histiocytosis established; Nocardia testing negative.
- **Adjudication rationale:** Nocardia tests/stains were negative and the final explanation was crystal-storing histiocytosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 38. `PMC7328479_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (67-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Wound culture and molecular/species identification established cutaneous Nocardia pseudobrasiliensis infection.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Wound culture and molecular/species identification established cutaneous Nocardia pseudobrasiliensis infection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 39. `PMC5820550_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (63-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Renal abscess tissue showed branching Gram-positive/weakly Fite-positive organisms and PCR identified Nocardia paucivorans.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Renal abscess tissue showed branching Gram-positive/weakly Fite-positive organisms and PCR identified Nocardia paucivorans. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 40. `PMC10443697_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (46-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** Nocardia appears as a phylogenetic comparator in a Mycobacterium abscessus scalp-infection report, not as the patient’s infection.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia appears as a phylogenetic comparator in a Mycobacterium abscessus scalp-infection report, not as the patient’s infection. Nocardia is a comparator organism in a genomic report, not a patient condition. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Nocardia is a comparator organism in a genomic report, not a patient condition.

### 41. `PMC6867963_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (16-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The broad workup for diffuse alveolar hemorrhage included Nocardia cultures, which were negative.
- **Contradiction resolution:** C1_NEGATIVE_TEST: Nocardia cultures negative during the workup.
- **Adjudication rationale:** The broad workup for diffuse alveolar hemorrhage included Nocardia cultures, which were negative. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 42. `PMC5340051_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (35-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain biopsy microbiology identified Nocardia in a patient with endophthalmitis and disseminated infection.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain biopsy microbiology identified Nocardia in a patient with endophthalmitis and disseminated infection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 43. `PMC6167885_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (62-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Skin specimen findings and culture supported cutaneous Nocardiosis due to Nocardia asteroides.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Skin specimen findings and culture supported cutaneous Nocardiosis due to Nocardia asteroides. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 44. `PMC3885780_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (77-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pleural fluid showed branching partially acid-fast rods and sequencing identified Nocardia cyriacigeorgica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural fluid showed branching partially acid-fast rods and sequencing identified Nocardia cyriacigeorgica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 45. `PMC9329676_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (61-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Blood/molecular and respiratory specimens identified Nocardia farcinica; Aspergillus and CMV were concurrent infections, not refutations.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Blood/molecular and respiratory specimens identified Nocardia farcinica; Aspergillus and CMV were concurrent infections, not refutations. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 46. `PMC5128003_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (75-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia was suspected, but blood culture identified Tsukamurella and bronchial cultures identified Mycobacterium bovis; Nocardia was not recovered.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Tsukamurella and Mycobacterium bovis were isolated; Nocardia was not recovered.
- **Adjudication rationale:** Nocardia was suspected, but blood culture identified Tsukamurella and bronchial cultures identified Mycobacterium bovis; Nocardia was not recovered. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 47. `PMC7451144_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (22-year-old female index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** Brainstem abscess was treated presumptively as nocardiosis, but cultures and serologies were negative and the diagnosis rests on non-specific imaging/response.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brainstem abscess was treated presumptively as nocardiosis, but cultures and serologies were negative and the diagnosis rests on non-specific imaging/response. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 48. `PMC4283927_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (70-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess aspirate showed branching partially acid-fast organisms and culture/16S identified Nocardia paucivorans.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess aspirate showed branching partially acid-fast organisms and culture/16S identified Nocardia paucivorans. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 49. `PMC9805727_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (49-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain biopsy culture and sequencing identified Nocardia brevicatena with compatible branching organisms.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain biopsy culture and sequencing identified Nocardia brevicatena with compatible branching organisms. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 50. `PMC7239889_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_CASE_REPORT | **Document:** SYSTEMATIC_REVIEW | **CCU:** NON_CLINICAL_DOCUMENT
- **Patient anchor:** No eligible single-human patient anchor in this record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / BACKGROUND_LITERATURE_REFERENCE
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The record is a narrative review of idiopathic CD4 lymphocytopenia and contains no single-patient Nocardiosis case unit.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The record is a narrative review of idiopathic CD4 lymphocytopenia and contains no single-patient Nocardiosis case unit. The document/unit is outside the eligible single-human-patient case-report target; excluded as EXCLUDED_NON_CASE_REPORT.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 51. `PMC8517639_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (66-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pulmonary lesion culture and MALDI-TOF identified Nocardia farcinica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pulmonary lesion culture and MALDI-TOF identified Nocardia farcinica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 52. `PMC3785346_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (67-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL identified Nocardia asteroides in a patient with lymphoma; Aspergillus was a coinfection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** BAL identified Nocardia asteroides in a patient with lymphoma; Aspergillus was a coinfection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 53. `PMC534796_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (32-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Tissue/pus culture and morphology identified Nocardia brasiliensis in lymphocutaneous disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Tissue/pus culture and morphology identified Nocardia brasiliensis in lymphocutaneous disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 54. `PMC4808525_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (0-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Vitreous/anterior-chamber material showed partially acid-fast branching beaded rods and culture identified Nocardia asteroides.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Vitreous/anterior-chamber material showed partially acid-fast branching beaded rods and culture identified Nocardia asteroides. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 55. `PMC6791275_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (40-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Culture and 16S sequencing identified Nocardia cyriacigeorgica in the first pulmonary case.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Culture and 16S sequencing identified Nocardia cyriacigeorgica in the first pulmonary case. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 56. `PMC6791275_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (28-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum smear and culture/16S sequencing identified Nocardia beijingensis in the second pulmonary case.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum smear and culture/16S sequencing identified Nocardia beijingensis in the second pulmonary case. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 57. `PMC5362858_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_SERIES | **CCU:** ANIMAL_CASE
- **Patient anchor:** animal_1 (non-human subject; outside the human benchmark)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The record is a cat dermatology case; Nocardia was only a differential and Streptococcus was cultured.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The record is a cat dermatology case; Nocardia was only a differential and Streptococcus was cultured. Veterinary cat case; Nocardia is a ruled-out differential. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Veterinary cat case; Nocardia is a ruled-out differential.

### 58. `PMC4696691_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_SERIES | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (67-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum culture identified Nocardia cerradoensis in a symptomatic patient; the clinical course and targeted treatment support probable pulmonary nocardiosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum culture identified Nocardia cerradoensis in a symptomatic patient; the clinical course and targeted treatment support probable pulmonary nocardiosis. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 59. `PMC4696691_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_SERIES | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (82-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum culture identified Nocardia cerradoensis in the third case, with pulmonary symptoms and targeted treatment.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum culture identified Nocardia cerradoensis in the third case, with pulmonary symptoms and targeted treatment. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 60. `PMC8227459_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (51-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Pneumocystis jirovecii was demonstrated and AFB studies were negative; Nocardia remained only a differential.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Pneumocystis jirovecii confirmed; Nocardia not established.
- **Adjudication rationale:** Pneumocystis jirovecii was demonstrated and AFB studies were negative; Nocardia remained only a differential. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 61. `PMC8216818_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (44-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain abscess culture and 16S sequencing identified Nocardia thailandica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain abscess culture and 16S sequencing identified Nocardia thailandica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 62. `PMC9780257_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (23-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL metagenomic sequencing and confirmatory molecular work identified Nocardia gipuzkoensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL metagenomic sequencing and confirmatory molecular work identified Nocardia gipuzkoensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 63. `PMC6669421_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (9-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Bronchoscopic biopsy/molecular testing identified Nocardia in a renal-transplant recipient with pulmonary/cardiac disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Bronchoscopic biopsy/molecular testing identified Nocardia in a renal-transplant recipient with pulmonary/cardiac disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 64. `PMC2841376_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (20-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Clinical specimens showed Nocardia bacilli in a disseminated orbital actinomycetoma presentation.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Clinical specimens showed Nocardia bacilli in a disseminated orbital actinomycetoma presentation. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 65. `PMC7849851_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (0-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Ocular specimen microscopy and culture established Nocardia infection in the child with endophthalmitis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Ocular specimen microscopy and culture established Nocardia infection in the child with endophthalmitis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 66. `PMC3952898_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (45-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Abscess culture identified Nocardia brasiliensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Abscess culture identified Nocardia brasiliensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 67. `PMC10165100_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (57-year-old female index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** The narrative describes active multisite Nocardia foci in a patient with SLE, but the supplied segment does not document a confirmatory Nocardia test.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The narrative describes active multisite Nocardia foci in a patient with SLE, but the supplied segment does not document a confirmatory Nocardia test. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 68. `PMC4822357_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Ulcer material showed branching organisms with modified acid-fast confirmation and culture of Nocardia asteroides.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Ulcer material showed branching organisms with modified acid-fast confirmation and culture of Nocardia asteroides. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 69. `PMC9279908_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (75-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Skin lesion microscopy and culture supported active cutaneous Nocardiosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Skin lesion microscopy and culture supported active cutaneous Nocardiosis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 70. `PMC8278857_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_SERIES | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (8-year-old female index patient); her 6-year-old brother is mentioned as a separate other-person reference
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Pleural/endotracheal cultures recovered Nocardia species in a child with a compatible disseminated presentation.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural/endotracheal cultures recovered Nocardia species in a child with a compatible disseminated presentation. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** Although the source publication is a case series, this supplied JSONL row contains the separately identifiable index child’s narrative. The sibling’s separate case is represented in another input row.

### 71. `PMC8278857_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_SERIES | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (6-year-old male index patient; brother of the child described in the adjacent case row)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum culture reported Nocardia species in the sibling with persistent respiratory symptoms and targeted therapy.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum culture reported Nocardia species in the sibling with persistent respiratory symptoms and targeted therapy. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** Although the source publication is a case series, this supplied JSONL row contains only the separately identifiable brother’s patient narrative. The other child is represented in another input row.

### 72. `PMC9434960_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (30-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture and MALDI-TOF identified Nocardia cyriacigeorgica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture and MALDI-TOF identified Nocardia cyriacigeorgica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 73. `PMC7673915_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (13-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Skin culture and MALDI-TOF identified Nocardia nova.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Skin culture and MALDI-TOF identified Nocardia nova. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 74. `PMC9844142_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (47-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Abscess culture and MALDI-TOF identified Nocardia cyriacigeorgica with characteristic partial acid-fast branching filaments.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Abscess culture and MALDI-TOF identified Nocardia cyriacigeorgica with characteristic partial acid-fast branching filaments. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 75. `PMC4977971_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (65-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain abscess culture and 16S sequencing identified Nocardia asiatica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain abscess culture and 16S sequencing identified Nocardia asiatica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 76. `PMC8606951_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (50-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia testing was negative in a varicella pneumonia case; varicella was the alternative diagnosis.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia negative; varicella pneumonia established.
- **Adjudication rationale:** Nocardia testing was negative in a varicella pneumonia case; varicella was the alternative diagnosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 77. `PMC9992866_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain biopsy culture identified Nocardia farcinica, confirmed by a public-health laboratory.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain biopsy culture identified Nocardia farcinica, confirmed by a public-health laboratory. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 78. `PMC9992866_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (unknown index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** The follow-up fragment documents additional positive Nocardia farcinica biopsy/public-health testing in the same case.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The follow-up fragment documents additional positive Nocardia farcinica biopsy/public-health testing in the same case. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 79. `PMC9812439_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** ANIMAL_CASE
- **Patient anchor:** animal_1 (non-human subject; outside the human benchmark)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This is a feline pyothorax case and is excluded from the human-patient target population.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a feline pyothorax case and is excluded from the human-patient target population. Veterinary cat pyothorax; excluded from human clinical benchmark. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Veterinary cat pyothorax; excluded from human clinical benchmark.

### 80. `PMC3320492_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** METHODOLOGICAL_PAPER | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (80-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The isolate was Williamsia muralis; Nocardia transvalensis was only a comparator in species identification.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The isolate was Williamsia muralis; Nocardia transvalensis was only a comparator in species identification. Williamsia muralis, not Nocardia, was the patient isolate; the Nocardia species is a comparator. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Williamsia muralis, not Nocardia, was the patient isolate; the Nocardia species is a comparator.

### 81. `PMC8308935_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Histopathology and clinical findings were interpreted as cutaneous Nocardiosis, but no species-level culture is provided.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Histopathology and clinical findings were interpreted as cutaneous Nocardiosis, but no species-level culture is provided. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 82. `PMC5588403_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (53-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia was only suspected from lung biopsy; invasive Aspergillus was subsequently established and treated.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Aspergillus hyphae/invasive fungal diagnosis explain the lung findings; Nocardia remained speculative.
- **Adjudication rationale:** Nocardia was only suspected from lung biopsy; invasive Aspergillus was subsequently established and treated. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 83. `PMC6447646_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (0-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The Nocardia material is epidemiological context in a pediatric CGD article, not a diagnosis in the index patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The Nocardia material is epidemiological context in a pediatric CGD article, not a diagnosis in the index patient. The patient does not have a Nocardia diagnosis; the article discusses Nocardia in epidemiological context. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The patient does not have a Nocardia diagnosis; the article discusses Nocardia in epidemiological context.

### 84. `PMC7667583_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (84-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Vitreal and calf-mass cultures identified Nocardia nova in disseminated disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Vitreal and calf-mass cultures identified Nocardia nova in disseminated disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 85. `PMC6501261_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Lung biopsy/MALDI identified Nocardia araoensis; the cerebral Cladophialophora infection was a separate coinfection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Lung biopsy/MALDI identified Nocardia araoensis; the cerebral Cladophialophora infection was a separate coinfection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 86. `PMC7451151_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (20-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The report concerns an intrapulmonary schwannoma without a patient-level Nocardia diagnosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The report concerns an intrapulmonary schwannoma without a patient-level Nocardia diagnosis. No patient-level Nocardia claim is made; the case is an intrapulmonary schwannoma. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** No patient-level Nocardia claim is made; the case is an intrapulmonary schwannoma.

### 87. `PMC8167374_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (82-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Multiple blood cultures grew Nocardia cyriacigeorgica in disseminated infection.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Multiple blood cultures grew Nocardia cyriacigeorgica in disseminated infection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 88. `PMC4225828_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (46-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Postoperative ocular cultures grew Nocardia asteroides.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Postoperative ocular cultures grew Nocardia asteroides. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 89. `PMC5760871_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (65-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum culture grew Nocardia asteroides in a symptomatic COPD patient; the respiratory syndrome supports probable pulmonary nocardiosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum culture grew Nocardia asteroides in a symptomatic COPD patient; the respiratory syndrome supports probable pulmonary nocardiosis. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 90. `PMC5282893_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_CASE_REPORT | **Document:** METHODOLOGICAL_PAPER | **CCU:** NON_CLINICAL_DOCUMENT
- **Patient anchor:** No eligible single-human patient anchor in this record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / BACKGROUND_LITERATURE_REFERENCE
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The record is an equine genome/phylogenetic study, not a human clinical case.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The record is an equine genome/phylogenetic study, not a human clinical case. Equine genome/phylogenetic paper rather than a human clinical case. The document/unit is outside the eligible single-human-patient case-report target; excluded as EXCLUDED_NON_CASE_REPORT.
- **Audit note:** Equine genome/phylogenetic paper rather than a human clinical case.

### 91. `PMC10392123_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (71-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Blood, pleural fluid and BAL testing with molecular identification established Nocardia kroppenstedtii.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Blood, pleural fluid and BAL testing with molecular identification established Nocardia kroppenstedtii. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 92. `PMC3463145_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (41-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture identified Nocardia asteroides in the first patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture identified Nocardia asteroides in the first patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 93. `PMC3463145_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (22-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess and CSF cultures identified Nocardia farcinica in the second patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess and CSF cultures identified Nocardia farcinica in the second patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 94. `PMC3463145_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (71-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture identified Nocardia arthritidis in the third patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture identified Nocardia arthritidis in the third patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 95. `PMC3463145_04::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (58-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture identified Nocardia cerradoensis in the fourth patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture identified Nocardia cerradoensis in the fourth patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 96. `PMC3366756_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (51-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Thigh-abscess culture identified Nocardia africanum in the tsunami-wound patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Thigh-abscess culture identified Nocardia africanum in the tsunami-wound patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 97. `PMC10467026_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (59-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Abscess tissue mNGS identified Nocardia wallacei; Mycobacterium abscessus was a separate coinfection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Abscess tissue mNGS identified Nocardia wallacei; Mycobacterium abscessus was a separate coinfection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 98. `PMC10455842_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (54-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain tissue culture identified Nocardia farcinica; Talaromyces marneffei was a concurrent pulmonary infection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Brain tissue culture identified Nocardia farcinica; Talaromyces marneffei was a concurrent pulmonary infection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 99. `PMC8461374_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (29-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Multiple specimens and MALDI-TOF identified Nocardia otitidiscaviarum in disseminated disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Multiple specimens and MALDI-TOF identified Nocardia otitidiscaviarum in disseminated disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 100. `PMC6334373_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (45-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Acid-fast testing was negative for Nocardia and Actinomyces israelii was identified as the cause.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia acid-fast test negative; Actinomyces confirmed.
- **Adjudication rationale:** Acid-fast testing was negative for Nocardia and Actinomyces israelii was identified as the cause. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 101. `PMC4605260_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (71-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum culture identified Nocardia cyriacigeorgica in a symptomatic COPD patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum culture identified Nocardia cyriacigeorgica in a symptomatic COPD patient. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 102. `PMC4605260_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (68-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum culture identified Nocardia cyriacigeorgica in a symptomatic patient with breast cancer.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum culture identified Nocardia cyriacigeorgica in a symptomatic patient with breast cancer. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 103. `PMC4605260_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (75-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Repeated symptomatic pulmonary episodes with Nocardia cyriacigeorgica isolates and targeted treatment support active infection.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Repeated symptomatic pulmonary episodes with Nocardia cyriacigeorgica isolates and targeted treatment support active infection. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 104. `PMC4605260_04::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (77-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia nova was isolated in an asymptomatic patient without Nocardia-directed treatment; this is most consistent with colonization rather than disease.
- **Contradiction resolution:** C0_RESOLVED_AMBIGUITY: Nocardia isolated in an asymptomatic patient without evidence of active infection; interpreted as colonization.
- **Adjudication rationale:** Nocardia nova was isolated in an asymptomatic patient without Nocardia-directed treatment; this is most consistent with colonization rather than disease. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 105. `PMC4998259_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (63-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Multiple abscess cultures and sequencing identified Nocardia brasiliensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Multiple abscess cultures and sequencing identified Nocardia brasiliensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 106. `PMC6083539_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (58-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Modified acid-fast testing was negative for Nocardia and Actinomyces israelii was confirmed.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: modified acid-fast stain negative for Nocardia; Actinomyces israelii confirmed.
- **Adjudication rationale:** Modified acid-fast testing was negative for Nocardia and Actinomyces israelii was confirmed. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 107. `PMC9422990_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (62-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** CSF/blood sequencing identified Nocardia farcinica in a patient with documented multiple opportunistic infections.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** CSF/blood sequencing identified Nocardia farcinica in a patient with documented multiple opportunistic infections. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 108. `PMC3961935_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (60-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Culture, branching partially acid-fast morphology and 16S sequencing established Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Culture, branching partially acid-fast morphology and 16S sequencing established Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 109. `PMC9062894_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (69-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture, Kinyoun stain and 16S/MALDI established Nocardia thailandica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture, Kinyoun stain and 16S/MALDI established Nocardia thailandica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 110. `PMC9969748_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (52-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia-directed studies were negative and SARS-CoV-2 was detected.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia-directed workup negative; SARS-CoV-2 detected.
- **Adjudication rationale:** Nocardia-directed studies were negative and SARS-CoV-2 was detected. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 111. `PMC3438302_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (79-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Vitreal cultures grew Nocardia farcinica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Vitreal cultures grew Nocardia farcinica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 112. `PMC2838367_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (66-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia cultures were negative; alternative pulmonary/cerebral diagnoses were identified.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia cultures negative; alternative diagnoses established.
- **Adjudication rationale:** Nocardia cultures were negative; alternative pulmonary/cerebral diagnoses were identified. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 113. `PMC5831598_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (68-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Bronchial washings showed characteristic branching organisms and HPLC identified Nocardia pseudobrasiliensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Bronchial washings showed characteristic branching organisms and HPLC identified Nocardia pseudobrasiliensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 114. `PMC5759803_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (90-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** Nocardia was cited only in the comparative background of a Mycobacterium simiae genome report.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia was cited only in the comparative background of a Mycobacterium simiae genome report. Nocardia appears only as a comparative background mention in a Mycobacterium simiae genome article. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Nocardia appears only as a comparative background mention in a Mycobacterium simiae genome article.

### 115. `PMC4209706_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (51-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The suspected Nocardia isolate was considered a contaminant; final diagnosis was leptomeningeal melanomatosis.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: suspected Nocardia isolate was judged a contaminant; final diagnosis was leptomeningeal melanomatosis.
- **Adjudication rationale:** The suspected Nocardia isolate was considered a contaminant; final diagnosis was leptomeningeal melanomatosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 116. `PMC2817494_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (34-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Foot-abscess culture identified Nocardia asteroides.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Foot-abscess culture identified Nocardia asteroides. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 117. `PMC6416759_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (52-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Cerebellar abscess culture and 16S sequencing identified Nocardia paucivorans.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Cerebellar abscess culture and 16S sequencing identified Nocardia paucivorans. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 118. `PMC8819730_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (71-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BALF microscopy and culture/16S sequencing identified Nocardia cyriacigeorgica in patient 1.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BALF microscopy and culture/16S sequencing identified Nocardia cyriacigeorgica in patient 1. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 119. `PMC8819730_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (68-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sputum pathogen identification/16S detected Nocardia brasiliensis with compatible pulmonary symptoms in patient 2.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum pathogen identification/16S detected Nocardia brasiliensis with compatible pulmonary symptoms in patient 2. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 120. `PMC8819730_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (69-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum/pus culture, partial acid-fast branching morphology and sequencing identified Nocardia farcinica in patient 3.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum/pus culture, partial acid-fast branching morphology and sequencing identified Nocardia farcinica in patient 3. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 121. `PMC9610571_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (51-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Multiple sterile-site cultures and sequencing identified Nocardia otitidiscaviarum in an infected aneurysm.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Multiple sterile-site cultures and sequencing identified Nocardia otitidiscaviarum in an infected aneurysm. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 122. `PMC10323790_05::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (unknown index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The brain abscess was attributed to Actinomyces israelii and Fusobacterium; Nocardia was not confirmed.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Actinomyces israelii and Fusobacterium were cultured; Nocardia was not confirmed.
- **Adjudication rationale:** The brain abscess was attributed to Actinomyces israelii and Fusobacterium; Nocardia was not confirmed. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 123. `PMC9485662_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (57-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BALF and lung-tissue mNGS identified Nocardia nova in a documented polymicrobial pulmonary infection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** BALF and lung-tissue mNGS identified Nocardia nova in a documented polymicrobial pulmonary infection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 124. `PMC6535853_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (39-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** The narrative names Nocardia septic arthritis/osteomyelitis, but the supplied text lacks diagnostic microbiology needed for a strict positive.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The narrative names Nocardia septic arthritis/osteomyelitis, but the supplied text lacks diagnostic microbiology needed for a strict positive. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 125. `PMC7171607_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** Weak acid-fast filamentous bacilli were described as resembling Nocardia, but there is no definitive culture/speciation in the supplied case segment.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Weak acid-fast filamentous bacilli were described as resembling Nocardia, but there is no definitive culture/speciation in the supplied case segment. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 126. `PMC7171607_02::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (78-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** The case was clinically labelled disseminated Nocardia based on weak acid-fast filaments and compatible findings, but organism confirmation is not supplied.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The case was clinically labelled disseminated Nocardia based on weak acid-fast filaments and compatible findings, but organism confirmation is not supplied. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 127. `PMC7171607_03::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (47-year-old female index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** SUSPECTED / E3_SUPPORTIVE
- **Evidence assessment:** Nocardia was suspected from weak acid-fast sputum findings and empiric treatment, without definitive species-level confirmation.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia was suspected from weak acid-fast sputum findings and empiric treatment, without definitive species-level confirmation. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No separate limitations recorded.

### 128. `PMC7171607_04::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (62-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** The case reports weak acid-fast filamentous bacilli and culture/MALDI identification of Nocardia araoensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The case reports weak acid-fast filamentous bacilli and culture/MALDI identification of Nocardia araoensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 129. `PMC7171607_05::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (73-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum microscopy and culture/MALDI identified Nocardia araoensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum microscopy and culture/MALDI identified Nocardia araoensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 130. `PMC9330429_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (3-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Ocular isolate with Gram-positive weakly acid-fast organisms and molecular identification established Nocardia infection.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Ocular isolate with Gram-positive weakly acid-fast organisms and molecular identification established Nocardia infection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 131. `PMC10248429_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (68-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The clinical narrative concerns tuberculosis; no patient-level Nocardia disease claim is established.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The clinical narrative concerns tuberculosis; no patient-level Nocardia disease claim is established. The record concerns an immune-checkpoint-associated tuberculosis case; no index-patient Nocardiosis claim is established. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The record concerns an immune-checkpoint-associated tuberculosis case; no index-patient Nocardiosis claim is established.

### 132. `PMC9868268_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (47-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** Nocardia appears only as a technical example in a pathogen-sequencing threshold discussion.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia appears only as a technical example in a pathogen-sequencing threshold discussion. Nocardia is mentioned only in a technical threshold rule for metagenomic assays, not as an infection in the case patient. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Nocardia is mentioned only in a technical threshold rule for metagenomic assays, not as an infection in the case patient.

### 133. `PMC3697147_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (70-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** The narrative documents recent disseminated Nocardiosis under ongoing antimicrobial treatment as an active comorbidity, but this fragment does not reproduce the original microbiological confirmation.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The narrative documents recent disseminated Nocardiosis under ongoing antimicrobial treatment as an active comorbidity, but this fragment does not reproduce the original microbiological confirmation. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 134. `PMC3697147_04::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (58-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** The narrative documents pulmonary Nocardiosis as an active concurrent condition under treatment, but the supplied segment lacks the original confirmatory test details.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The narrative documents pulmonary Nocardiosis as an active concurrent condition under treatment, but the supplied segment lacks the original confirmatory test details. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 135. `PMC9251553_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (84-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pleural infection microscopy and MALDI-TOF identified Nocardia farcinica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural infection microscopy and MALDI-TOF identified Nocardia farcinica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 136. `PMC3395676_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (22-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The mycetoma was caused by Madurella; Nocardia was only part of the differential/background.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The mycetoma was caused by Madurella; Nocardia was only part of the differential/background. The causative mycetoma organism is Madurella; Nocardia is only discussed as a differential/background agent. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The causative mycetoma organism is Madurella; Nocardia is only discussed as a differential/background agent.

### 137. `PMC3118057_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (50-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Tissue and drainage cultures identified Nocardia species in a compatible actinomycetoma presentation.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Tissue and drainage cultures identified Nocardia species in a compatible actinomycetoma presentation. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 138. `PMC9248758_02::Nocardiosis`
- **Decision:** EXCLUDED_NON_CASE_REPORT | **Document:** SYSTEMATIC_REVIEW | **CCU:** NON_CLINICAL_DOCUMENT
- **Patient anchor:** No eligible single-human patient anchor in this record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / BACKGROUND_LITERATURE_REFERENCE
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This is a literature review; Nocardia appears in literature cases rather than a single index patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a literature review; Nocardia appears in literature cases rather than a single index patient. Review/literature-search record; no single index patient with Nocardiosis. The document/unit is outside the eligible single-human-patient case-report target; excluded as EXCLUDED_NON_CASE_REPORT.
- **Audit note:** Review/literature-search record; no single index patient with Nocardiosis.

### 139. `PMC8573330_02::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (male index patient)
- **Assertion / temporality / role:** NEGATED / HISTORICAL_RESOLVED / PAST_HISTORY
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia is described as a past pulmonary infection; the current episode concerns Candida and does not establish active Nocardiosis.
- **Contradiction resolution:** HISTORICAL_ONLY: Nocardia is described as a prior episode, not current disease.
- **Adjudication rationale:** Nocardia is described as a past pulmonary infection; the current episode concerns Candida and does not establish active Nocardiosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 140. `PMC4797532_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (31-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess aspirate culture and molecular identification established Nocardia crassostreae.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess aspirate culture and molecular identification established Nocardia crassostreae. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 141. `PMC7609154_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (37-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pleural/empyema tissue demonstrated branching partially acid-fast organisms consistent with Nocardia.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural/empyema tissue demonstrated branching partially acid-fast organisms consistent with Nocardia. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 142. `PMC4617009_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (42-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture identified Nocardia asteroides after earlier negative respiratory workup.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture identified Nocardia asteroides after earlier negative respiratory workup. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 143. `PMC5838848_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (47-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia stains/tests were negative and an Actinomyces-like organism was favored.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia testing negative; Actinomyces-like disease favored.
- **Adjudication rationale:** Nocardia stains/tests were negative and an Actinomyces-like organism was favored. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 144. `PMC5362853_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** ANIMAL_CASE
- **Patient anchor:** animal_1 (non-human subject; outside the human benchmark)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This is a cat infection; Nocardia was suspected but tests were negative and the final cause was Aelurostrongylus abstrusus.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a cat infection; Nocardia was suspected but tests were negative and the final cause was Aelurostrongylus abstrusus. Animal case; Aelurostrongylus abstrusus was identified and Nocardia was not confirmed. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Animal case; Aelurostrongylus abstrusus was identified and Nocardia was not confirmed.

### 145. `PMC5359233_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (75-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** DNA sequencing established Propionibacterium acnes, not Nocardia, in the brain lesion.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Propionibacterium acnes was identified by sequencing.
- **Adjudication rationale:** DNA sequencing established Propionibacterium acnes, not Nocardia, in the brain lesion. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 146. `PMC5994559_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (28-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** CSF PCR identified Nocardia otitidiscaviarum in the current spinal/CNS episode.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** CSF PCR identified Nocardia otitidiscaviarum in the current spinal/CNS episode. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 147. `PMC3403161_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (49-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pericardial pus culture identified Nocardia asiatica in disseminated disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pericardial pus culture identified Nocardia asiatica in disseminated disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 148. `PMC8055275_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Cutaneous abscess culture identified Nocardia farcinica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Cutaneous abscess culture identified Nocardia farcinica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 149. `PMC4904555_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_CASE_REPORT | **Document:** CASE_SERIES | **CCU:** MULTI_PATIENT_CASE_SERIES
- **Patient anchor:** No eligible single-human patient anchor in this record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / BACKGROUND_LITERATURE_REFERENCE
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** Five pulmonary Nocardiosis patients are aggregated in one case-series narrative; no single-patient CCU is separable in this row.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Five pulmonary Nocardiosis patients are aggregated in one case-series narrative; no single-patient CCU is separable in this row. Five patients are summarized in one case-series unit; because the supplied row does not resolve the five patient narratives into separate patient-level records, it is excluded from the single-patient benchmark. The document/unit is outside the eligible single-human-patient case-report target; excluded as EXCLUDED_NON_CASE_REPORT.
- **Audit note:** Five patients are summarized in one case-series unit; because the supplied row does not resolve the five patient narratives into separate patient-level records, it is excluded from the single-patient benchmark.

### 150. `PMC8040973_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (41-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum/lung-tissue modified acid-fast staining and culture identified Nocardia cyriacigeorgica; Aspergillus was a true coinfection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Sputum/lung-tissue modified acid-fast staining and culture identified Nocardia cyriacigeorgica; Aspergillus was a true coinfection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 151. `PMC5025916_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia was included in BAL testing, which was negative; Candida albicans was identified in BAL and lung tissue.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: BAL Nocardia workup negative; Candida albicans confirmed.
- **Adjudication rationale:** Nocardia was included in BAL testing, which was negative; Candida albicans was identified in BAL and lung tissue. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 152. `PMC10966995_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (81-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Cultures for Nocardia were negative; tissue PCR/sequencing identified Apophysomyces, explaining the cutaneous infection.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia cultures negative; Apophysomyces species identified by PCR/sequencing.
- **Adjudication rationale:** Cultures for Nocardia were negative; tissue PCR/sequencing identified Apophysomyces, explaining the cutaneous infection. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 153. `PMC10710253_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (56-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Abdominal abscess aspirate showed branching partially acid-fast organisms and culture/MALDI identified Nocardia farcinica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Abdominal abscess aspirate showed branching partially acid-fast organisms and culture/MALDI identified Nocardia farcinica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 154. `PMC10921472_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum smear/culture identified Nocardia otitidiscaviarum while blood culture independently confirmed Brucella melitensis; this is true coinfection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Sputum smear/culture identified Nocardia otitidiscaviarum while blood culture independently confirmed Brucella melitensis; this is true coinfection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 155. `PMC11333241_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (33-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The patient’s abscesses were attributed to Leucobacter clevelandensis by NGS, not Nocardia.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The patient’s abscesses were attributed to Leucobacter clevelandensis by NGS, not Nocardia. The abscess case was attributed to Leucobacter clevelandensis by NGS; no Nocardia claim is made in the supplied patient narrative. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The abscess case was attributed to Leucobacter clevelandensis by NGS; no Nocardia claim is made in the supplied patient narrative.

### 156. `PMC10896460_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (75-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum showed partially acid-fast branching filaments and 16S sequencing identified Nocardia wallacei despite negative culture.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum showed partially acid-fast branching filaments and 16S sequencing identified Nocardia wallacei despite negative culture. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 157. `PMC11032677_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (75-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Liver-tissue mNGS identified Nocardia farcinica in the current febrile/granulomatous episode.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Liver-tissue mNGS identified Nocardia farcinica in the current febrile/granulomatous episode. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 158. `PMC11193390_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (61-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL microscopy showed branching partially acid-fast organisms and MALDI-TOF identified Nocardia wallacei.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL microscopy showed branching partially acid-fast organisms and MALDI-TOF identified Nocardia wallacei. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 159. `PMC10858340_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (38-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pleural fluid microscopy/culture and MALDI-TOF/16S sequencing identified Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural fluid microscopy/culture and MALDI-TOF/16S sequencing identified Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 160. `PMC11045883_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (56-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Cutaneous abscess-fluid NGS detected abundant Nocardia sequences and infectious-disease specialists diagnosed cutaneous nocardiosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Cutaneous abscess-fluid NGS detected abundant Nocardia sequences and infectious-disease specialists diagnosed cutaneous nocardiosis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 161. `PMC11370755_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (51-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL mNGS and sputum culture identified Nocardia with Pneumocystis coinfection; the case explicitly confirmed both infections.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** BAL mNGS and sputum culture identified Nocardia with Pneumocystis coinfection; the case explicitly confirmed both infections. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 162. `PMC10657549_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (71-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess culture, mNGS and weak acid-fast branching bacilli identified Nocardia gipuzkoensis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Brain-abscess culture, mNGS and weak acid-fast branching bacilli identified Nocardia gipuzkoensis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 163. `PMC10832585_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (60-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pleural biopsy culture identified Nocardia nova in a post-pneumonectomy empyema.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural biopsy culture identified Nocardia nova in a post-pneumonectomy empyema. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 164. `PMC10961017_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (0-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Fecal microscopy/culture and MALDI-TOF identified Nocardia farcinica in a symptomatic child with diarrhea.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Fecal microscopy/culture and MALDI-TOF identified Nocardia farcinica in a symptomatic child with diarrhea. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 165. `PMC11179430_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (66-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** CSF culture, MALDI-TOF and BAL tNGS confirmed disseminated Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** CSF culture, MALDI-TOF and BAL tNGS confirmed disseminated Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 166. `PMC10702378_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (41-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Transbronchial lung-tissue microscopy/culture and MALDI-TOF identified Nocardia cyriacigeorgica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Transbronchial lung-tissue microscopy/culture and MALDI-TOF identified Nocardia cyriacigeorgica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 167. `PMC10481806_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (62-year-old female index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** Nocardia is mentioned as a stain-related background organism in an educational cervical-TB quiz, not as the patient’s disease.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Nocardia is mentioned as a stain-related background organism in an educational cervical-TB quiz, not as the patient’s disease. Educational case/question about cervical tuberculosis; Nocardia appears only in general stain discussion. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** Educational case/question about cervical tuberculosis; Nocardia appears only in general stain discussion.

### 168. `PMC10809415_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (27-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Bronchial lesion mNGS detected Nocardia farcinica and the case narrative states a definitive localized diagnosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Bronchial lesion mNGS detected Nocardia farcinica and the case narrative states a definitive localized diagnosis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 169. `PMC10928402_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Pleural-fluid microscopy, culture and VITEK/MALDI identified Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Pleural-fluid microscopy, culture and VITEK/MALDI identified Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 170. `PMC11288846_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (60-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL culture identified Nocardia and the patient improved after targeted anti-Nocardia therapy.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL culture identified Nocardia and the patient improved after targeted anti-Nocardia therapy. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 171. `PMC11378987_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (63-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum mNGS detected Nocardia cyriacigeorgica during a documented polymicrobial pulmonary episode; Babesia and Pneumocystis were concurrent detections.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Sputum mNGS detected Nocardia cyriacigeorgica during a documented polymicrobial pulmonary episode; Babesia and Pneumocystis were concurrent detections. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 172. `PMC10550213_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The mycetoma initially presumed to be Nocardia was later cultured and sequenced as Gordonia soli.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: repeat culture and 16S sequencing established Gordonia soli rather than Nocardia.
- **Adjudication rationale:** The mycetoma initially presumed to be Nocardia was later cultured and sequenced as Gordonia soli. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 173. `PMC10520695_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (68-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL mNGS identified Nocardia farcinica in a lung-transplant recipient with a current post-COVID pulmonary syndrome.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL mNGS identified Nocardia farcinica in a lung-transplant recipient with a current post-COVID pulmonary syndrome. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 174. `PMC10601863_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (70-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Corneal scraping culture and MALDI-TOF identified Nocardia africana.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Corneal scraping culture and MALDI-TOF identified Nocardia africana. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 175. `PMC11163097_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (78-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Lung-lesion puncture-fluid mNGS and culture identified Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Lung-lesion puncture-fluid mNGS and culture identified Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 176. `PMC11179496_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (48-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Draining pus and repeat deep-muscle cultures identified Nocardia brasiliensis by MALDI-TOF.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Draining pus and repeat deep-muscle cultures identified Nocardia brasiliensis by MALDI-TOF. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 177. `PMC11806675_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (81-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum and pleural-fluid microbiology, culture and mass spectrometry identified Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum and pleural-fluid microbiology, culture and mass spectrometry identified Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 178. `PMC11748329_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** Sinus biopsy showed Gram-positive thin-walled filamentous bacterial aggregates compatible with Nocardia; the clinical diagnosis and targeted response support a probable case despite absent species-level culture.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sinus biopsy showed Gram-positive thin-walled filamentous bacterial aggregates compatible with Nocardia; the clinical diagnosis and targeted response support a probable case despite absent species-level culture. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 179. `PMC11702207_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (male index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This initial fragment describes the patient presentation but does not contain Nocardia-specific diagnostic evidence in its supplied case_text.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This initial fragment describes the patient presentation but does not contain Nocardia-specific diagnostic evidence in its supplied case_text. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 180. `PMC11702207_02::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (unknown index patient)
- **Assertion / temporality / role:** UNCERTAIN / CURRENT_ACTIVE / DIFFERENTIAL_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This continuation fragment contains no Nocardia-specific result; the later post-mortem culture is present in a separate row.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This continuation fragment contains no Nocardia-specific result; the later post-mortem culture is present in a separate row. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 181. `PMC11702207_03::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Post-mortem bone-marrow culture and phenotypic identification confirmed Nocardia farcinica.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Post-mortem bone-marrow culture and phenotypic identification confirmed Nocardia farcinica. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 182. `PMC11832390_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (69-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BALF culture showed Gram-positive weakly acid-fast colonies and VITEK MS identified Nocardia otitidiscaviarum.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BALF culture showed Gram-positive weakly acid-fast colonies and VITEK MS identified Nocardia otitidiscaviarum. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 183. `PMC11825202_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (69-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Drainage cultures from two patient abscesses and repeated MALDI-TOF identified Nocardia kroppenstedtii.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Drainage cultures from two patient abscesses and repeated MALDI-TOF identified Nocardia kroppenstedtii. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 184. `PMC11703450_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (19-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Bronchoscopy testing for Nocardia species was negative; the clinical diagnosis was EVALI.
- **Contradiction resolution:** C1_NEGATIVE_TEST: bronchoscopic Nocardia species testing was negative; clinical diagnosis was EVALI.
- **Adjudication rationale:** Bronchoscopy testing for Nocardia species was negative; the clinical diagnosis was EVALI. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 185. `PMC11787046_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (33-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia-directed Kinyoun testing was part of the workup, but bacterial stains/cultures did not identify Nocardia; Pneumocystis and Histoplasma were established.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: bacterial staining/molecular workup did not identify Nocardia; Pneumocystis and Histoplasma confirmed.
- **Adjudication rationale:** Nocardia-directed Kinyoun testing was part of the workup, but bacterial stains/cultures did not identify Nocardia; Pneumocystis and Histoplasma were established. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 186. `PMC13034707_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (64-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Intraoperative tissue culture identified Nocardia paucivorans in the forearm abscess; pulmonary and cerebral lesions were compatible with dissemination.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Intraoperative tissue culture identified Nocardia paucivorans in the forearm abscess; pulmonary and cerebral lesions were compatible with dissemination. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 187. `PMC12515561_01::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (43-year-old male index patient)
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The index case is disseminated Kaposi sarcoma/HIV; Nocardia is not a patient-level diagnosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The index case is disseminated Kaposi sarcoma/HIV; Nocardia is not a patient-level diagnosis. HIV/Kaposi sarcoma case; no Nocardia diagnosis in the index patient narrative. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** HIV/Kaposi sarcoma case; no Nocardia diagnosis in the index patient narrative.

### 188. `PMC12587269_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (77-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** PROBABLE / E2_HIGHLY_SPECIFIC
- **Evidence assessment:** BAL culture identified Nocardia wallacei in a patient with weight loss and structural lung disease; the organism was treated according to susceptibility.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL culture identified Nocardia wallacei in a patient with weight loss and structural lung disease; the organism was treated according to susceptibility. The minimum evidence threshold is met (E2_HIGHLY_SPECIFIC); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 189. `PMC12275057_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_SERIES | **CCU:** MULTI_PATIENT_CASE_SERIES
- **Patient anchor:** Multiple patient narratives / aggregate case-series context; no single anchor for the whole record
- **Assertion / temporality / role:** NEGATED / HISTORICAL_RESOLVED / PAST_HISTORY
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** The Nocardia episode is historical in one Scedosporium case-series patient; current evaluation identified Scedosporium and did not detect Nocardia.
- **Contradiction resolution:** HISTORICAL_ONLY: previous pulmonary Nocardiosis was treated; in the current Scedosporium episode, Nocardia was not detected.
- **Adjudication rationale:** The Nocardia episode is historical in one Scedosporium case-series patient; current evaluation identified Scedosporium and did not detect Nocardia. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 190. `PMC13168027_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (8-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Histology and 16S/culture established Aggregatibacter actinomycetemcomitans; Nocardia was only a differential and morphology favored Actinomyces.
- **Contradiction resolution:** C2_COMPETING_DIAGNOSIS: Actinomyces/ Aggregatibacter actinomycetemcomitans confirmed; morphology favored the alternative.
- **Adjudication rationale:** Histology and 16S/culture established Aggregatibacter actinomycetemcomitans; Nocardia was only a differential and morphology favored Actinomyces. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 191. `PMC12488295_01::Nocardiosis`
- **Decision:** INCONCLUSIVE_DATA | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (43-year-old male index patient)
- **Assertion / temporality / role:** UNCERTAIN / HISTORICAL_RESOLVED / PAST_HISTORY
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The prior cerebral Nocardia diagnosis was suspected, not microbiologically confirmed; current biopsy was nonspecific and no active Nocardiosis is established.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The prior cerebral Nocardia diagnosis was suspected, not microbiologically confirmed; current biopsy was nonspecific and no active Nocardiosis is established. The evidence is insufficient to assign a strict positive or a definitive ruled-out label; final label INCONCLUSIVE_DATA.
- **Audit note:** No patient-anchored Nocardia evidence span was recorded from the supplied case_text.

### 192. `PMC13092237_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Blood/CSF NGS identified Nocardia brevicatena in multiple intracranial abscesses, with improvement on targeted treatment.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Blood/CSF NGS identified Nocardia brevicatena in multiple intracranial abscesses, with improvement on targeted treatment. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 193. `PMC12667243_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (55-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** BAL mNGS and bacterial culture identified Nocardia cyriacigeorgica and the case explicitly diagnosed pulmonary Nocardiosis.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** BAL mNGS and bacterial culture identified Nocardia cyriacigeorgica and the case explicitly diagnosed pulmonary Nocardiosis. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 194. `PMC12646876_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (52-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Brain-abscess aspirate mNGS and culture/MALDI identified Nocardia asiatica; Torque teno virus was a concurrent detection.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Brain-abscess aspirate mNGS and culture/MALDI identified Nocardia asiatica; Torque teno virus was a concurrent detection. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 195. `PMC13138953_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (60-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia cultures from BAL were negative and the cavitary lesions regressed after DLBCL chemotherapy, supporting lymphoma rather than nocardiosis.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: BAL Nocardia cultures negative; DLBCL diagnosis and response to R-CHOP explain lesions.
- **Adjudication rationale:** Nocardia cultures from BAL were negative and the cavitary lesions regressed after DLBCL chemotherapy, supporting lymphoma rather than nocardiosis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 196. `PMC12681903_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (30-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Sputum and BAL cultures detected Nocardia and 16S sequencing identified Nocardia pneumoniae in a symptomatic patient.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Sputum and BAL cultures detected Nocardia and 16S sequencing identified Nocardia pneumoniae in a symptomatic patient. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 197. `PMC12681903_05::Nocardiosis`
- **Decision:** EXCLUDED_NON_TARGET_CASE | **Document:** CASE_REPORT | **CCU:** AGGREGATE_STUDY_UNIT
- **Patient anchor:** Multiple patient narratives / aggregate case-series context; no single anchor for the whole record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / EPIDEMIOLOGICAL_CONTEXT
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** The supplied segment summarizes a previously published N. pneumoniae case from the literature, not the index patient in this candidate row.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The supplied segment summarizes a previously published N. pneumoniae case from the literature, not the index patient in this candidate row. The supplied text is a literature summary of a previously published N. pneumoniae case; it is not the index patient from the main case report. The mention does not form an eligible patient-centered Nocardiosis claim; excluded as EXCLUDED_NON_TARGET_CASE.
- **Audit note:** The supplied text is a literature summary of a previously published N. pneumoniae case; it is not the index patient from the main case report.

### 198. `PMC13043398_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (50-year-old female index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Bronchoscopic testing for Nocardia species was negative and the clinical course supported immune-checkpoint-inhibitor pneumonitis.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia PCR negative; immune-checkpoint pneumonitis was diagnosed.
- **Adjudication rationale:** Bronchoscopic testing for Nocardia species was negative and the clinical course supported immune-checkpoint-inhibitor pneumonitis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 199. `PMC12870019_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (79-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Splenic-aspirate and brain-biopsy cultures grew branching Nocardia ignorata, with species-level MALDI-TOF identification.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** Splenic-aspirate and brain-biopsy cultures grew branching Nocardia ignorata, with species-level MALDI-TOF identification. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 200. `PMC13161159_02::Nocardiosis`
- **Decision:** EXCLUDED_NON_CASE_REPORT | **Document:** SYSTEMATIC_REVIEW | **CCU:** NON_CLINICAL_DOCUMENT
- **Patient anchor:** No eligible single-human patient anchor in this record
- **Assertion / temporality / role:** UNMENTIONED / UNKNOWN / BACKGROUND_LITERATURE_REFERENCE
- **Case definition / evidence:** NOT_MET / E4_CONTEXT
- **Evidence assessment:** This is a narrative review of the nasal-oral microbiome in allergic rhinitis, not a patient-level Nocardiosis case.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** This is a narrative review of the nasal-oral microbiome in allergic rhinitis, not a patient-level Nocardiosis case. Narrative review of the nasal-oral microbiome and allergic rhinitis; no patient-level Nocardiosis CCU. The document/unit is outside the eligible single-human-patient case-report target; excluded as EXCLUDED_NON_CASE_REPORT.
- **Audit note:** Narrative review of the nasal-oral microbiome and allergic rhinitis; no patient-level Nocardiosis CCU.

### 201. `PMC12863413_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (86-year-old female index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / ACTIVE_COMORBIDITY
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** Gluteal-abscess microscopy/culture identified Nocardia farcinica in a patient with chorioretinitis, endophthalmitis and CNS disease.
- **Contradiction resolution:** C0_RESOLVED_COINFECTION: concurrent infection(s) do not invalidate the independent Nocardia claim.
- **Adjudication rationale:** Gluteal-abscess microscopy/culture identified Nocardia farcinica in a patient with chorioretinitis, endophthalmitis and CNS disease. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 202. `PMC12854188_01::Nocardiosis`
- **Decision:** NEGATIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (56-year-old male index patient)
- **Assertion / temporality / role:** NEGATED / CURRENT_ACTIVE / RULED_OUT_DIAGNOSIS
- **Case definition / evidence:** NOT_MET / E0_CONTRADICTED
- **Evidence assessment:** Nocardia-directed staining/cultures were negative and Mycobacterium tuberculosis was confirmed as the cause of disseminated pyomyositis.
- **Contradiction resolution:** C1_NEGATIVE_TEST + C2_COMPETING_DIAGNOSIS: Nocardia-directed stains/cultures negative; tuberculosis confirmed.
- **Adjudication rationale:** Nocardia-directed staining/cultures were negative and Mycobacterium tuberculosis was confirmed as the cause of disseminated pyomyositis. The strict active-disease threshold is not met; the final label is NEGATIVE.
- **Audit note:** No separate limitations recorded.

### 203. `PMC12375495_01::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (67-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** CSF mNGS detected Nocardia otitidiscaviarum above the stated sequencing threshold in a compatible purulent meningitis episode.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** CSF mNGS detected Nocardia otitidiscaviarum above the stated sequencing threshold in a compatible purulent meningitis episode. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

### 204. `PMC12375495_02::Nocardiosis`
- **Decision:** POSITIVE | **Document:** CASE_REPORT | **CCU:** SINGLE_HUMAN_PATIENT
- **Patient anchor:** patient_1 (67-year-old male index patient)
- **Assertion / temporality / role:** AFFIRMED / CURRENT_ACTIVE / PRIMARY_DIAGNOSIS
- **Case definition / evidence:** CONFIRMED / E1_CONFIRMATORY
- **Evidence assessment:** The case segment explicitly documents the definitive diagnosis of Nocardia otitidiscaviarum meningitis and clinical response to targeted treatment.
- **Contradiction resolution:** NONE_IDENTIFIED: no material contradiction to the adjudicated target-disease status is reported in the supplied narrative.
- **Adjudication rationale:** The case segment explicitly documents the definitive diagnosis of Nocardia otitidiscaviarum meningitis and clinical response to targeted treatment. The minimum evidence threshold is met (E1_CONFIRMATORY); the final label is POSITIVE.
- **Audit note:** No separate limitations recorded.

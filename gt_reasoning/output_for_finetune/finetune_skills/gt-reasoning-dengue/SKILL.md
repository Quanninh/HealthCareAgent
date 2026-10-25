---
name: gt-reasoning-dengue-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Dengue cases in selected_case_ft_pofs/output_dengue.jsonl across POSITIVE (active Dengue virus infection) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE).
---

# Dengue — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_dengue.jsonl`)

- **Disease Key:** `"Dengue"`
- **Input File:** `selected_case_ft_pofs/output_dengue.jsonl` (`33` total rows)
  - **`POSITIVE` (`19` rows):** Active Dengue virus (`DENV-1` to `DENV-4`) infection — including classic dengue fever, dengue with warning signs, severe dengue, dengue hemorrhagic fever (`DHF`), dengue shock syndrome (`DSS`), or expanded dengue syndrome (myocarditis, encephalitis, hepatitis, HLH) — confirmed by serum/blood `NS1 antigen assay`, `DENV RT-PCR`, viral isolation, or `anti-dengue IgM/IgG seroconversion / MAC-ELISA`.
  - **`OUT_OF_SCOPE` (`14` rows, rewritten from `5` `NEGATIVE` + `9` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out + Alternative Diagnosis (`5` `NEGATIVE` rows):**
       - `PMC5771939_01` & `PMC5771939_02`: Initial clinical misdiagnosis of dengue refuted by hospital exclusion / lack of improvement and definitive PCR/serologic confirmation of *Rickettsia rickettsii* (Rocky Mountain spotted fever).
       - Other `NEGATIVE` rows: Febrile thrombocytopenia or systemic illness where dengue `NS1 antigen`, `RT-PCR`, and `IgM/IgG serology` were explicitly **negative**, and an out-of-scope etiology was diagnosed.
    2. **Resolved Historical Past Infection Presenting with Delayed Non-Infectious / Post-Infectious Sequelae or Unrelated Illness (`9` `EXCLUDED_NON_TARGET_CASE` rows, `HISTORICAL_PAST`, `F4_ASSERTION_TEMPORAL`):**
       - `PMC6341935_01` & `PMC6341935_02`: Organic mood disorder (post-infectious mania) presenting 5–7 days after resolution of dengue fever, with no active viral infection or acute laboratory testing in the current psychiatric episode.
       - Other `EXCLUDED_NON_TARGET_CASE` rows: Remote historical dengue fever (`1 month` to `1 year` prior) noted in past medical history when presenting for ophthalmic sequelae, unrelated surgical/medical conditions, or background vector/epidemiological discourse.

---

## 2. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Dengue (<DENV serotype and/or clinical severity classification>)."`
  - Examples:
    - `"Dengue (Dengue virus infection — severe dengue shock syndrome)."`
    - `"Dengue (Dengue virus infection — mild dengue fever in a hematopoietic stem cell transplant recipient)."`
    - `"Dengue (Dengue hemorrhagic fever with plasma leakage and severe thrombocytopenia)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Diagnosis or Post-Infectious/Historical Context> — Not Active Dengue)."`
  - Examples:
    - `"OUT_OF_SCOPE (Rickettsia rickettsii infection / Rocky Mountain spotted fever — Not Dengue)."`
    - `"OUT_OF_SCOPE (Organic mania following resolved prior dengue fever — Not Active Dengue)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogens & Serotypes:** Keep `Dengue virus (DENV-1, DENV-2, DENV-3, DENV-4)` and confirmed alternative pathogens in `OUT_OF_SCOPE` cases (`Rickettsia rickettsii`, `Rickettsia typhi`, `Plasmodium`, `Leptospira`).
2. **Diagnostic Assays:** Keep `dengue NS1 antigen assay`, `DENV RT-PCR`, `anti-dengue IgM MAC-ELISA`, `IgG capture ELISA (primary vs. secondary infection ratio)`, `tourniquet test`, and alternative confirmatory tests (`Rickettsia rickettsii PCR and IgM serology`).
3. **Pathophysiological Hallmarks:** Keep `severe thrombocytopenia`, `hemoconcentration (rising hematocrit)`, `plasma leakage (pleural effusion, ascites, gallbladder wall edema)`, `hemorrhagic manifestations (petechiae, epistaxis, gastrointestinal bleeding)`, and `dengue shock syndrome (DSS) / multi-organ failure`.
4. **Lab Value & Titer Conversion:**
   - Convert raw platelet counts (`"16 x 10^9/L"`) to `"severe thrombocytopenia"`.
   - Convert raw hematocrit percentages, transaminase numbers (`AST`, `ALT`), and rickettsial serologic titers (`"1:128"`, `"1:64"`) to qualitative descriptions (`"hemoconcentration"`, `"markedly elevated hepatic transaminases"`, `"positive Rickettsia rickettsii IgM titer"`).

### Strip (Log in `dropped_specifics`)
- Patient age, sex, and occupation (`"10-year-old male"`, `"2-year-old boy"`, `"19-year-old male photographer"`).
- Post-transplant day numbers (`"on day +130"`, `"on day +103"`), exact post-resolution day counts (`"5 days after"`, `"after a week"` → convert to `"shortly after clinical resolution of a prior episode"`), and case numbers (`"case report 1"`).
- Pipeline tokens (`"E1_CONFIRMATORY_LAB"`, `"E0 contradicted"`, `"Assertion ABSENT_NEGATIVE"`, `"clinical role RULED_OUT_DIAGNOSIS"`, `"VPD not satisfied -> NEGATIVE"`, `"Excluded as past history"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_dengue.jsonl`)

### Example 1 — `POSITIVE` (`PMC11378234_03::Dengue`)
**Input Record:**
- `step12_dataset_label`: `"POSITIVE"`, `step5_concept_grounding`: `"Severe dengue shock syndrome post-stem cell transplant confirmed by NS1 antigen"`
- `rationale`: `"A 10-year-old male post-HSCT recipient presented with fever, severe thrombocytopenia (16 x 10^9/L), and multi-organ failure progressing to shock and death. Dengue NS1 antigen was detected (E1_CONFIRMATORY_LAB), confirming fatal severe dengue. VPD satisfied -> POSITIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"Dengue NS1 antigen was detected."`

**Target Output:**
```json
{
  "pair_id": "PMC11378234_03::Dengue",
  "case_id": "PMC11378234_03",
  "target_disease": "Dengue",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "Dengue (Dengue virus infection — severe dengue shock syndrome). Reasoning: (1) Clinical presentation in a hematopoietic stem cell transplant recipient includes acute fever, severe thrombocytopenia, and progressive multi-organ failure culminating in refractory shock. (2) Detection of dengue NS1 antigen in blood provides definitive laboratory confirmation of acute Dengue virus infection. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation in a hematopoietic stem cell transplant recipient includes acute fever, severe thrombocytopenia, and progressive multi-organ failure culminating in refractory shock.",
      "source": "rationale"
    },
    {
      "text": "Detection of dengue NS1 antigen in blood provides definitive laboratory confirmation of acute Dengue virus infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "10-year-old male — demographics",
    "on day +130 — post-transplant timeline",
    "16 x 10^9/L — converted to severe thrombocytopenia",
    "E1_CONFIRMATORY_LAB, VPD satisfied -> POSITIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC5771939_01::Dengue`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Dengue was an initial clinical misdiagnosis explicitly discarded during hospitalization; patient had fatal Rocky Mountain spotted fever (Rickettsia rickettsii)"`
- `rationale`: `"A 2-year-old boy presented with fever, vomiting, and a maculopapular rash, initially diagnosed with dengue exclusively on clinical criteria. During hospitalization, dengue was explicitly discarded, and the patient was confirmed to have Rickettsia rickettsii infection (titer 1:128) resulting in fatal multi-organ failure. The candidate diagnosis of dengue was explicitly ruled out (E0 contradicted). Assertion ABSENT_NEGATIVE, clinical role RULED_OUT_DIAGNOSIS. VPD not satisfied -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC5771939_01::Dengue",
  "case_id": "PMC5771939_01",
  "target_disease": "Dengue",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Rickettsia rickettsii infection / Rocky Mountain spotted fever — Not Dengue). Reasoning: (1) Acute febrile illness with vomiting and maculopapular rash was initially misdiagnosed clinically as dengue, but dengue virus infection is explicitly excluded during inpatient diagnostic evaluation. (2) Serological testing confirms positive Rickettsia rickettsii IgM antibodies complicated by multi-organ failure, establishing Rocky Mountain spotted fever rather than dengue. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute febrile illness with vomiting and maculopapular rash was initially misdiagnosed clinically as dengue, but dengue virus infection is explicitly excluded during inpatient diagnostic evaluation.",
      "source": "both"
    },
    {
      "text": "Serological testing confirms positive Rickettsia rickettsii IgM antibodies complicated by multi-organ failure, establishing Rocky Mountain spotted fever rather than dengue.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "2-year-old boy, case report 1 — demographics and case label",
    "1:128 — converted to positive Rickettsia rickettsii IgM antibodies",
    "E0 contradicted, Assertion ABSENT_NEGATIVE, clinical role RULED_OUT_DIAGNOSIS, VPD not satisfied -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC6341935_01::Dengue`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step7_temporality`: `"HISTORICAL_PAST"`, `step8_clinical_role`: `"PAST_HISTORY"`
- `rationale`: `"An 18-year-old female presented to psychiatric OPD with mania (decreased sleep, irritability, grandiose delusions) developing one week after resolution of dengue fever. Dengue infection is explicitly a resolved past infection with no active disease and no confirmatory or serologic laboratory test documented in the narrative. The active presenting condition being treated is organic mood disorder mania. Excluded as past history / non-target acute episode."`

**Target Output:**
```json
{
  "pair_id": "PMC6341935_01::Dengue",
  "case_id": "PMC6341935_01",
  "target_disease": "Dengue",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Post-infectious organic mania following resolved dengue — Not Active Dengue). Reasoning: (1) Psychiatric presentation with decreased need for sleep, irritability, and grandiose delusions establishes an active diagnosis of organic mania developing after clinical resolution of an antecedent febrile episode. (2) Prior dengue fever is a resolved historical event with no ongoing acute viral infection or laboratory confirmation of active Dengue virus during the current presentation. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Psychiatric presentation with decreased need for sleep, irritability, and grandiose delusions establishes an active diagnosis of organic mania developing after clinical resolution of an antecedent febrile episode.",
      "source": "both"
    },
    {
      "text": "Prior dengue fever is a resolved historical event with no ongoing acute viral infection or laboratory confirmation of active Dengue virus during the current presentation.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "18-year-old female — demographics",
    "one week after — exact timeline converted to after clinical resolution",
    "Excluded as past history / non-target acute episode — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Dengue`)
- Verify all `33` rows are emitted (`19` `"POSITIVE"`, `14` `"OUT_OF_SCOPE"`).
- Confirm all raw platelet counts and serologic titers are converted to qualitative/threshold terms and logged in `dropped_specifics`.
- Ensure zero pipeline tokens and zero deictic pronouns remain in `ground_truth_reasoning` or `claims`.


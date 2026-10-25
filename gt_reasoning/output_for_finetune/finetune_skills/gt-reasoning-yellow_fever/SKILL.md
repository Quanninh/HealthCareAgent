---
name: gt-reasoning-yellow_fever-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Yellow Fever cases in selected_case_ft_pofs/output_yellow_fever.jsonl across OUT_OF_SCOPE (17D/17DD/Stamaril yellow fever vaccination and vaccine-associated neurotropic/viscerotropic adverse events rewritten from EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Yellow Fever — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_yellow_fever.jsonl`)

- **Disease Key:** `"Yellow_Fever"`
- **Input File:** `selected_case_ft_pofs/output_yellow_fever.jsonl` (`4` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active wild-type Yellow fever virus (`YFV`, *Orthoflavivirus flavi*) infection confirmed by blood/serum/CSF/visceral tissue `YFV RT-PCR`, viral isolation, liver histopathology showing midzonal hepatocyte necrosis with eosinophilic Councilman bodies and Torres bodies (without recent YF vaccination), or `anti-YFV IgM ELISA` / `PRNT90` in an unvaccinated patient with acute febrile hepatorenal hemorrhagic syndrome.
  - **`OUT_OF_SCOPE` (`4` rows, rewritten from `0` `NEGATIVE` + `4` `EXCLUDED_NON_TARGET_CASE`):**
    Every row in `selected_case_ft_pofs/output_yellow_fever.jsonl` involves **live attenuated yellow fever vaccination (`17D`, `17DD`, `Stamaril`)** rather than wild-type yellow fever virus infection (`PREVENTION_VACCINATION`, `F5_DISCOURSE_CONTEXT`):
    1. `PMC4978951_01`: Narcolepsy type 1 with cataplexy where yellow fever appears solely as prior pre-travel vaccination with live attenuated `Stamaril` yellow fever vaccine explored as a hypothetical autoimmune trigger, with no wild-type yellow fever infection.
    2. `PMC8931735_01`: Status epilepticus and encephalopathy following pre-travel `17D` yellow fever vaccination, confirmed by CSF and serum YFV IgM and `PRNT90` as **yellow fever vaccine-associated neurotropic disease (`YEL-AND`)** — a vaccine adverse event rather than wild-type yellow fever infection.
    3. `PMC6519039_01` & `PMC7114308_01`: Live attenuated `17D`/`17DD` yellow fever vaccination context or yellow fever vaccine-associated viscerotropic/neurotropic adverse event (`YEL-AVD` / `YEL-AND`), not wild-type yellow fever.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Primary Clinical Condition or Yellow Fever Vaccine Adverse Event> — Not Wild-Type Yellow Fever)."`
  - Examples:
    - `"OUT_OF_SCOPE (Narcolepsy type 1 following pre-travel Stamaril yellow fever vaccination — Not Yellow Fever)."`
    - `"OUT_OF_SCOPE (Yellow fever vaccine-associated neurotropic disease [YEL-AND] following 17D vaccination — Not Wild-Type Yellow Fever)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Yellow Fever (wild-type Yellow fever virus infection)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Vaccine Strains & Vaccine-Associated Syndromes:**
   - Keep `17D` / `17DD` / `Stamaril live attenuated yellow fever vaccine`, `yellow fever vaccine-associated neurotropic disease (YEL-AND)`, `yellow fever vaccine-associated viscerotropic disease (YEL-AVD)`, `CSF and serum YFV IgM`, and `90% plaque reduction neutralization test (PRNT90)`.
   - State clearly in the second claim that the clinical presentation represents a post-vaccination adverse event or pre-travel immunization history rather than wild-type Yellow fever virus infection.
2. **Presenting Non-Target Conditions:** Keep `narcolepsy type 1 with cataplexy`, `status epilepticus and autoimmune/post-vaccinal encephalopathy`, and `molecular mimicry hypothesis`.

### Strip (Log in `dropped_specifics`)
- Patient age and sex (`"13-year-old boy"`, `"67-year-old woman"`).
- Specific travel destinations (`"family trip to Africa"`, `"traveling to Guyana, South America"` → convert to `"pre-travel immunization"`), exact pre-presentation intervals (`"~2 weeks prior"`, `"Two months prior"`), and institutional names (`"CDC"`).
- Pipeline tokens (`"clinical_role = PREVENTION_VACCINATION"`, `"VPD = false -> EXCLUDED_NON_TARGET_CASE"`, `"E4_CONTEXT"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_yellow_fever.jsonl`)

### Example 1 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC4978951_01::Yellow_Fever`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step8_clinical_role`: `"PREVENTION_VACCINATION"`
- `rationale`: `"A 13-year-old boy presented with cataplexy and daytime sleepiness, and was diagnosed with narcolepsy type 1. Yellow fever appears exclusively as historical receipt of the Stamaril live, attenuated yellow fever vaccine ~2 weeks prior to symptom onset, explored as a hypothetical autoimmune trigger via molecular mimicry. The patient had no active or confirmed yellow fever infection. Per protocol, vaccination context cannot establish an infection claim. VPD = false -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC4978951_01::Yellow_Fever",
  "case_id": "PMC4978951_01",
  "target_disease": "Yellow_Fever",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Narcolepsy type 1 with cataplexy following Stamaril yellow fever vaccination — Not Yellow Fever). Reasoning: (1) Presentation with excessive daytime sleepiness and cataplexy establishes a neurological diagnosis of narcolepsy type 1. (2) Yellow fever is referenced solely as recent pre-travel immunization with the Stamaril live attenuated yellow fever vaccine explored as a hypothetical autoimmune trigger, with no active or wild-type Yellow fever virus infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Presentation with excessive daytime sleepiness and cataplexy establishes a neurological diagnosis of narcolepsy type 1.",
      "source": "rationale"
    },
    {
      "text": "Yellow fever is referenced solely as recent pre-travel immunization with the Stamaril live attenuated yellow fever vaccine explored as a hypothetical autoimmune trigger, with no active or wild-type Yellow fever virus infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "13-year-old boy — demographics",
    "~2 weeks prior, family trip to Africa — exact timeline and geographic destination",
    "Per protocol, vaccination context cannot establish an infection claim. VPD = false -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC8931735_01::Yellow_Fever`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step8_clinical_role`: `"PREVENTION_VACCINATION"`
- `rationale`: `"A 67-year-old woman developed status epilepticus and encephalopathy following receipt of the 17D yellow fever vaccine, with CSF and serum YFV IgM and PRNT90 confirming yellow fever vaccine-associated neurotropic disease (YEL-AND). The MultiCaRe protocol explicitly establishes that vaccine-associated adverse events are categorized under clinical_role = PREVENTION_VACCINATION and do not represent wild-type yellow fever infection. Because wild-type infection is not present, VPD = false -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC8931735_01::Yellow_Fever",
  "case_id": "PMC8931735_01",
  "target_disease": "Yellow_Fever",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Yellow fever vaccine-associated neurotropic disease [YEL-AND] — Not Wild-Type Yellow Fever). Reasoning: (1) Encephalopathy and status epilepticus developing after pre-travel immunization with the live attenuated 17D yellow fever vaccine are accompanied by positive cerebrospinal fluid and serum yellow fever virus IgM and plaque reduction neutralization testing (PRNT90), confirming yellow fever vaccine-associated neurotropic disease (YEL-AND). (2) The condition represents an adverse neurological complication of live attenuated 17D vaccination rather than wild-type Yellow fever virus infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Encephalopathy and status epilepticus developing after pre-travel immunization with the live attenuated 17D yellow fever vaccine are accompanied by positive cerebrospinal fluid and serum yellow fever virus IgM and plaque reduction neutralization testing (PRNT90), confirming yellow fever vaccine-associated neurotropic disease (YEL-AND).",
      "source": "both"
    },
    {
      "text": "The condition represents an adverse neurological complication of live attenuated 17D vaccination rather than wild-type Yellow fever virus infection.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "67-year-old woman — demographics",
    "Two months prior, CDC, Guyana, South America — timeline, agency name, and geographic destination",
    "MultiCaRe protocol, clinical_role = PREVENTION_VACCINATION, VPD = false -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Yellow_Fever`)
- Verify all `4` rows in `output_yellow_fever.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Ensure every row clearly distinguishes live attenuated `17D`/`17DD`/`Stamaril` vaccination or `YEL-AND`/`YEL-AVD` from wild-type Yellow fever virus infection without emitting `MultiCaRe protocol`, `PREVENTION_VACCINATION`, or `VPD = false`.


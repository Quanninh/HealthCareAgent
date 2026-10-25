---
name: gt-reasoning-malaria-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Malaria cases in selected_case_ft_pofs/output_malaria.jsonl across POSITIVE (active Plasmodium infection) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE, including ovale anatomical homonyms).
---

# Malaria — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_malaria.jsonl`)

- **Disease Key:** `"Malaria"`
- **Input File:** `selected_case_ft_pofs/output_malaria.jsonl` (`114` total rows)
  - **`POSITIVE` (`18` rows):** Active human malaria caused by *Plasmodium* species (`Plasmodium falciparum`, `Plasmodium vivax`, `Plasmodium ovale`, `Plasmodium malariae`, `Plasmodium knowlesi`, or mixed *Plasmodium* infection) confirmed by thick/thin peripheral blood smear microscopy (intraerythrocytic ring-form trophozoites, schizonts, gametocytes, Maurer's clefts, Schüffner's stippling), malaria rapid diagnostic antigen test (`RDT`: `HRP2`, `pLDH`, `aldolase`, `Malaria Protein Antigen`), or species-specific *Plasmodium* `PCR`.
  - **`OUT_OF_SCOPE` (`96` rows, rewritten from `6` `NEGATIVE` + `90` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out + Alternative Diagnosis (`6` `NEGATIVE` rows):**
       - `PMC5288520_01`: Febrile pregnant immigrant with remote prior history of treated malaria; maternal blood *Plasmodium* PCR and smear/antigen were negative, and blood cultures confirmed *Salmonella enterica* serovar Typhi bacteremia.
       - `PMC4395950_01`: Acute disseminated encephalomyelitis (`ADEM` / delayed cerebellar ataxia and bilateral optic neuritis) presenting after prior resolved *P. vivax* treatment; repeat peripheral blood smear, blood malaria antigen test, and CSF malaria antigen test were all explicitly negative.
       - Other `NEGATIVE` rows: Febrile/hemolytic presentations where peripheral blood smears, RDTs, and/or *Plasmodium* PCR tested negative and an alternative diagnosis was established.
    2. **Anatomical Homonym Collision with `"ovale"` / `"PFO"` (`75` of `90` `EXCLUDED_NON_TARGET_CASE` rows, `F1_LEXICAL_HOMONYM`):**
       - Candidate retrieval triggered by anatomical structures containing the word `"ovale"` or acronym `"PFO"` colliding with *Plasmodium ovale*:
         - **Cardiac:** `patent foramen ovale (PFO)` or `fossa ovalis` on echocardiography / transcranial Doppler (e.g., `PMC9124883_01`: migraine and lower-extremity dystonia with PFO; cryptogenic stroke; paradoxical embolism; platypnea-orthodeoxia).
         - **Neuroanatomical / Cranial:** cerebral `centrum semiovale` / `centrum ovale` on brain MRI, or skull base `foramen ovale` (trigeminal neuralgia rhizotomy, perineural tumor spread).
       - *Note:* `1` `OUT_OF_SCOPE` row has empty `evidence_items` (`[]`) — extract claims from `rationale` and `step5_concept_grounding`.
    3. **Malaria Chemoprophylaxis Adverse Event or Historical/Contextual Mention (`15` `EXCLUDED_NON_TARGET_CASE` rows):**
       - `PMC6798169_01`: Acute cholestatic hepatitis induced by *Artemisia annua* herbal tea ingested as malaria chemoprophylaxis, with liver biopsy showing no parasitic material and no malaria infection.
       - Mefloquine/chloroquine/doxycycline prophylaxis side effects, hydroxychloroquine (antimalarial class drug) used for SLE/rheumatoid arthritis, or empirical antimalarial therapy in a patient with confirmed Lassa fever (`PMC5748105_02`).

---

## 2. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Malaria (<Plasmodium species and severity/complication>)."`
  - Examples:
    - `"Malaria (severe Plasmodium falciparum infection with hyperparasitemia and malarial retinopathy)."`
    - `"Malaria (Plasmodium malariae infection)."`
    - `"Malaria (Plasmodium vivax infection)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Diagnosis or Anatomical/Prophylaxis Context> — Not Malaria)."`
  - *Rule-out examples:*
    - `"OUT_OF_SCOPE (Salmonella Typhi bacteremia with negative malaria PCR — Not Malaria)."`
    - `"OUT_OF_SCOPE (Post-infectious acute disseminated encephalomyelitis with negative malaria smear and antigen testing — Not Active Malaria)."`
  - *Homonym / Chemoprophylaxis examples:*
    - `"OUT_OF_SCOPE (Migraine-associated dystonia with cardiac patent foramen ovale — Not Malaria)."`
    - `"OUT_OF_SCOPE (Artemisia annua herbal chemoprophylaxis-induced cholestatic hepatitis — Not Malaria)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogen Species & Morphological Forms:** Keep `Plasmodium falciparum`, `Plasmodium vivax`, `Plasmodium ovale`, `Plasmodium malariae`, `Plasmodium knowlesi`, intraerythrocytic `ring-form trophozoites`, `schizonts`, `banana-shaped gametocytes`, and `malarial retinopathy`.
2. **Diagnostic Assays:** Keep `Giemsa-stained thick and thin peripheral blood smears`, `rapid diagnostic antigen test (HRP2 / pLDH / Malaria Protein Antigen)`, and `Plasmodium species-specific PCR`.
3. **Parasitemia Threshold Conversion:**
   - When raw parasitemia is high (e.g., `"39.3%"`), convert to `"severe hyperparasitemia (> 10% infected erythrocytes)"` (WHO severe *P. falciparum* threshold) and log the exact percentage (`"39.3%"`, `"<1%"`) in `dropped_specifics`.
4. **Anatomical Homonyms & Prophylaxis Agents (in `OUT_OF_SCOPE` rows):**
   - Explicitly name the anatomical structure (`cardiac patent foramen ovale [PFO]`, `cerebral centrum semiovale`, `cranial base foramen ovale`) and state that no *Plasmodium* infection is present.

### Strip (Log in `dropped_specifics`)
- Patient age, sex, occupation, and gestational week (`"52-year-old female"`, `"78-year-old female missionary"`, `"26-year-old pregnant patient at 31 weeks gestation"` — keep `"pregnancy"` if relevant, strip `"26-year-old"` and `"31 weeks"`).
- Geographic names (`"Sierra Leone"`, `"Nigeria"`, `"Ethiopia"` → convert to `"endemic region"`).
- Raw temperatures (`"103.7 F"`), exact parasitemia percentages (`"39.3%"`, `"<1%"`), herbal tea gram weights (`"1.25 g"`), and figure citations (`"Fig. 1"`, `"[Figure 1]"`).
- Pipeline tokens (`"E1_CONFIRMATORY"`, `"E0_NONE"`, `"E0_CONTRADICTED"`, `"F1_LEXICAL_HOMONYM"`, `"VPD satisfied -> POSITIVE"`, `"VPD = false -> NEGATIVE"`, `"-> EXCLUDED_NON_TARGET_CASE"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_malaria.jsonl`)

### Example 1 — `POSITIVE` (`PMC10932508_01::Malaria`)
**Input Record:**
- `step12_dataset_label`: `"POSITIVE"`, `step5_concept_grounding`: `"Severe Plasmodium falciparum malaria confirmed by blood smear microscopy (39.3% parasitemia) and positive antigen test"`
- `rationale`: `"A 52-year-old female returned from Sierra Leone presenting with severe fatigue, scleral icterus, anemia, and thrombocytopenia. Peripheral blood smear examination demonstrated numerous ring trophozoites and schizonts with hyperparasitemia of 39.3%, and rapid antigen testing was positive for Plasmodium falciparum antigen. Dilated ophthalmic examination confirmed malaria retinopathy. She was successfully treated with intravenous artesunate followed by artemether/lumefantrine, reducing parasitemia to <1%. E1 confirmatory lab evidence present for primary patient in current episode. VPD satisfied -> POSITIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC10932508_01::Malaria",
  "case_id": "PMC10932508_01",
  "target_disease": "Malaria",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "Malaria (severe Plasmodium falciparum infection). Reasoning: (1) Clinical presentation after travel to an endemic region includes severe fatigue, scleral icterus, hemolytic anemia, thrombocytopenia, and malarial retinopathy on dilated ophthalmic examination. (2) Peripheral blood smear microscopy demonstrates numerous intraerythrocytic ring-form trophozoites and schizonts with severe hyperparasitemia (> 10% infected erythrocytes), and rapid antigen testing is positive for Plasmodium falciparum antigen, with parasitemia clearance following intravenous artesunate and artemether-lumefantrine therapy. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation after travel to an endemic region includes severe fatigue, scleral icterus, hemolytic anemia, thrombocytopenia, and malarial retinopathy on dilated ophthalmic examination.",
      "source": "rationale"
    },
    {
      "text": "Peripheral blood smear microscopy demonstrates numerous intraerythrocytic ring-form trophozoites and schizonts with severe hyperparasitemia (> 10% infected erythrocytes), and rapid antigen testing is positive for Plasmodium falciparum antigen, with parasitemia clearance following intravenous artesunate and artemether-lumefantrine therapy.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "52-year-old female — demographics",
    "Sierra Leone — converted to endemic region",
    "39.3%, <1% — converted to severe hyperparasitemia (> 10% infected erythrocytes) and parasitemia clearance",
    "Fig. 1, Figs. 2 and 3, E1 confirmatory lab evidence, VPD satisfied -> POSITIVE — figure citations and pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC5288520_01::Malaria`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Evaluation and rule-out of malaria in a febrile pregnant immigrant; confirmed Salmonella Typhi bacteremia"`
- `rationale`: `"A 26-year-old pregnant female who immigrated from Nigeria two weeks prior presented with fever and abdominal pain. Although she had a remote history of treated malaria in her first trimester, acute malaria was evaluated as part of the differential diagnosis for her current febrile illness. Maternal blood PCR testing for malaria was explicitly negative, and blood cultures subsequently confirmed Salmonella enterica serotype Typhi bacteremia. Because active malaria was suspected and conclusively ruled out by negative molecular PCR testing in the current episode, the dataset label is NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC5288520_01::Malaria",
  "case_id": "PMC5288520_01",
  "target_disease": "Malaria",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Salmonella enterica serovar Typhi bacteremia with negative malaria PCR — Not Malaria). Reasoning: (1) Acute febrile illness with abdominal pain during pregnancy following recent immigration from an endemic region and a remote history of treated malaria prompts diagnostic evaluation for active malaria, including peripheral smear, Plasmodium antigen immunochromatography, and blood PCR. (2) Maternal blood PCR testing for Plasmodium DNA is negative, ruling out active malaria, while blood cultures confirm Salmonella enterica serovar Typhi bacteremia. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute febrile illness with abdominal pain during pregnancy following recent immigration from an endemic region and a remote history of treated malaria prompts diagnostic evaluation for active malaria, including peripheral smear, Plasmodium antigen immunochromatography, and blood PCR.",
      "source": "both"
    },
    {
      "text": "Maternal blood PCR testing for Plasmodium DNA is negative, ruling out active malaria, while blood cultures confirm Salmonella enterica serovar Typhi bacteremia.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "26-year-old female, 31 weeks gestation, first trimester — demographics and exact gestational timelines",
    "Nigeria, two weeks prior — geographic location and exact timeline",
    "the dataset label is NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC9124883_01::Malaria`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F1_LEXICAL_HOMONYM"]`
- `rationale`: `"The case involves a 52-year-old woman evaluated for migraine and lower limb dystonia, found to have a patent foramen ovale (PFO) on contrast echocardiography. Malaria is completely unmentioned in the clinical case; candidate retrieval was caused by the lexical homonym/acronym PFO (patent foramen ovale vs Plasmodium ovale). As this is a non-target cardiac condition, the case is excluded -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC9124883_01::Malaria",
  "case_id": "PMC9124883_01",
  "target_disease": "Malaria",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Migraine-associated lower-extremity dystonia with cardiac patent foramen ovale — Not Malaria). Reasoning: (1) Neurological evaluation of intractable migraine and lower-extremity dystonia demonstrates a cardiac patent foramen ovale (PFO) on contrast transcranial Doppler and right-heart contrast echocardiography. (2) The anatomical term patent foramen ovale (PFO) refers to an interatrial cardiac shunt rather than Plasmodium ovale infection, and no malaria is present. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Neurological evaluation of intractable migraine and lower-extremity dystonia demonstrates a cardiac patent foramen ovale (PFO) on contrast transcranial Doppler and right-heart contrast echocardiography.",
      "source": "both"
    },
    {
      "text": "The anatomical term patent foramen ovale (PFO) refers to an interatrial cardiac shunt rather than Plasmodium ovale infection, and no malaria is present.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "52-year-old female — demographics",
    "lexical homonym/acronym, -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Malaria`)
- Verify all `114` rows are emitted (`18` `"POSITIVE"`, `96` `"OUT_OF_SCOPE"`).
- Confirm that all `75` anatomical `"ovale"` / `"PFO"` homonym rows clearly state the actual cardiac/neurological condition and disambiguate the anatomical structure from *Plasmodium ovale* without emitting `F1_LEXICAL_HOMONYM`.
- Ensure raw parasitemia percentages are converted to WHO hyperparasitemia thresholds (`> 10%`) or qualitative descriptions and logged in `dropped_specifics`.


---
name: gt-reasoning-leptospirosis-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Leptospirosis cases in selected_case_ft_pofs/output_leptospirosis.jsonl across OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Leptospirosis — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_leptospirosis.jsonl`)

- **Disease Key:** `"Leptospirosis"`
- **Input File:** `selected_case_ft_pofs/output_leptospirosis.jsonl` (`8` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active human leptospirosis / Weil's disease caused by pathogenic *Leptospira* species (*L. interrogans* serovars Icterohaemorrhagiae, Copenhageni, Canicola, Grippotyphosa, Pomona, Hardjo; *L. kirschneri*; *L. borgpetersenii*) confirmed by blood/CSF/urine `PCR` or `mNGS`, dark-field microscopy / EMJH culture, `microscopic agglutination test (MAT)` (`>= 1:400` single titer or `>= 4-fold rise` in paired sera), or acute `anti-Leptospira IgM ELISA` in a compatible clinical syndrome (fever, conjunctival suffusion, calf myalgia, jaundice, acute kidney injury, pulmonary hemorrhage).
  - **`OUT_OF_SCOPE` (`8` rows, rewritten from `7` `NEGATIVE` + `1` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out + Alternative Out-of-Scope Diagnosis (`7` `NEGATIVE` rows):**
       - `PMC5933029_01`: Paddy field worker with acute febrile illness, acute kidney injury, and pulmonary edema initially suspected of leptospirosis, ruled out by negative paired *Leptospira* IgM/IgG ELISA on days 7 and 18 and confirmed as **hantavirus infection** (positive hantavirus IgM).
       - `PMC5933029_02`: Acute febrile illness, myalgia, oliguria, and pulmonary edema evaluated for Weil's disease, ruled out by negative *Leptospira* microscopic agglutination test (`MAT`) and confirmed as **hantavirus infection**.
       - `PMC11282534_01`, `PMC6023903_01`, `PMC6102819_01`, `PMC6474635_01`, `PMC8604646_01`: Suspected leptospirosis / Weil's disease ruled out by negative *Leptospira* PCR, MAT, or IgM serology, with confirmation of an alternative out-of-scope etiology (e.g., G6PD-deficiency oxidative hemolysis, autoimmune/vasculitic disease, rickettsiosis, or other non-target pathology).
    2. **Historical Biographical Speculation (`1` `EXCLUDED_NON_TARGET_CASE` row, `PMC10369008_01`):**
       - Retrospective historical biography speculating whether a 1930 fatal illness recorded on the death certificate as cholangitis and hepatitis could have been Weil's disease, without contemporaneous clinical or laboratory confirmation of leptospirosis.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Confirmed Alternative Diagnosis or Historical Context> — Not Leptospirosis)."`
  - Examples:
    - `"OUT_OF_SCOPE (Hantavirus pulmonary-renal syndrome with negative Leptospira ELISA — Not Leptospirosis)."`
    - `"OUT_OF_SCOPE (Hantavirus infection with negative Leptospira microscopic agglutination test — Not Leptospirosis)."`
    - `"OUT_OF_SCOPE (Historical cholangitis and hepatitis with unverified retrospective speculation of Weil's disease — Not Leptospirosis)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Leptospirosis (Leptospira interrogans infection / Weil's disease)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogens & Alternative Etiologies:** Keep `Leptospira`, clinical eponym `Weil's disease`, and confirmed out-of-scope diagnoses (`hantavirus infection`, `G6PD deficiency oxidative hemolysis`, `cholangitis and hepatitis`).
2. **Diagnostic Assays:** Keep `microscopic agglutination test (MAT)`, `paired anti-Leptospira IgM and IgG ELISA`, `Leptospira PCR`, and `hantavirus IgM serology`.
3. **Clinical Features & Exposures:** Keep `acute febrile illness`, `acute kidney injury / oliguria`, `pulmonary edema / hemorrhage`, `jaundice`, `myalgia`, and generalized environmental exposure (`agricultural paddy field exposure`).

### Strip (Log in `dropped_specifics`)
- Patient age, sex, and historical personal names (`"46-year-old male"`, `"57-year-old male"`, `"Philosopher Frank Ramsey, who died in 1930 aged 26"`).
- Illness day numbers (`"on day 7 and repeated on day 18"`, `"on day 10"`) and historical dates (`"mid-November 1929"`, `"1930"`).
- Pipeline tokens (`"E0_CONTRADICTED"`, `"F4_ASSERTION_TEMPORAL"`, `"F5_DISCOURSE_CONTEXT"`, `"-> NEGATIVE"`, `"Excluded as non-target case"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_leptospirosis.jsonl`)

### Example 1 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC5933029_01::Leptospirosis`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Leptospirosis evaluated as provisional working diagnosis and ruled out by negative paired ELISA"`
- `rationale`: `"A 46-year-old rice paddy worker presented with fever, acute kidney injury, and pulmonary edema. Leptospirosis was suspected as the provisional diagnosis, but paired ELISA testing for Leptospira IgM and IgG on days 7 and 18 was negative, while hantavirus IgM was confirmed positive. Target disease was explicitly tested and ruled out -> NEGATIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"An ELISA test done for IgM and IgG against leptospira on day 7 and repeated on day 18 delivered negative results."`

**Target Output:**
```json
{
  "pair_id": "PMC5933029_01::Leptospirosis",
  "case_id": "PMC5933029_01",
  "target_disease": "Leptospirosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Hantavirus infection with negative paired Leptospira ELISA — Not Leptospirosis). Reasoning: (1) Acute febrile illness complicated by acute kidney injury and pulmonary edema following agricultural paddy field exposure initially raises provisional suspicion of leptospirosis, but paired acute and convalescent serum IgM and IgG ELISA tests for Leptospira are negative. (2) Serological testing confirms positive hantavirus IgM antibodies, establishing hantavirus infection and ruling out leptospirosis. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute febrile illness complicated by acute kidney injury and pulmonary edema following agricultural paddy field exposure initially raises provisional suspicion of leptospirosis, but paired acute and convalescent serum IgM and IgG ELISA tests for Leptospira are negative.",
      "source": "both"
    },
    {
      "text": "Serological testing confirms positive hantavirus IgM antibodies, establishing hantavirus infection and ruling out leptospirosis.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "46-year-old male — demographics",
    "on day 7 and repeated on day 18 — illness day timeline converted to paired acute and convalescent",
    "Target disease was explicitly tested and ruled out -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC5933029_02::Leptospirosis`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Leptospirosis evaluated as working diagnosis and ruled out by negative MAT"`
- `rationale`: `"A 57-year-old male presented with fever, myalgias, oliguria, and pulmonary edema with a working diagnosis of Weil's disease. Blood taken on day 10 for MAT (IgM and IgG) was negative, whereas hantavirus IgM serology was positive. Leptospirosis was evaluated and ruled out -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC5933029_02::Leptospirosis",
  "case_id": "PMC5933029_02",
  "target_disease": "Leptospirosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Hantavirus infection with negative Leptospira microscopic agglutination test — Not Leptospirosis). Reasoning: (1) Presentation with fever, myalgias, oliguric renal dysfunction, and pulmonary edema prompts a working diagnosis of severe leptospirosis (Weil's disease), but serum microscopic agglutination testing (MAT) for Leptospira IgM and IgG is negative. (2) Positive hantavirus IgM serology establishes acute hantavirus infection and excludes leptospirosis. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Presentation with fever, myalgias, oliguric renal dysfunction, and pulmonary edema prompts a working diagnosis of severe leptospirosis (Weil's disease), but serum microscopic agglutination testing (MAT) for Leptospira IgM and IgG is negative.",
      "source": "both"
    },
    {
      "text": "Positive hantavirus IgM serology establishes acute hantavirus infection and excludes leptospirosis.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "57-year-old male — demographics",
    "on day 10 — illness timeline",
    "Leptospirosis was evaluated and ruled out -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC10369008_01::Leptospirosis`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F5_DISCOURSE_CONTEXT"]`
- `rationale`: `"A historical biographical case report exploring speculative retrospective causes of death for philosopher Frank Ramsey, who died in 1930. The final contemporaneous death certificate recorded cholangitis and hepatitis. Leptospirosis (Weil's disease) is mentioned solely as a modern retrospective hypothesis in the abstract and discussion, without clinical or diagnostic verification in the patient during life. Excluded as non-target case."`

**Target Output:**
```json
{
  "pair_id": "PMC10369008_01::Leptospirosis",
  "case_id": "PMC10369008_01",
  "target_disease": "Leptospirosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Historical cholangitis and hepatitis with unverified retrospective hypothesis of Weil's disease — Not Leptospirosis). Reasoning: (1) Contemporaneous medical records of a fatal febrile hepatobiliary illness establish a documented diagnosis of cholangitis and hepatitis. (2) Leptospirosis (Weil's disease) is discussed solely as an unverified retrospective historical hypothesis without clinical or microbiological confirmation of Leptospira infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Contemporaneous medical records of a fatal febrile hepatobiliary illness establish a documented diagnosis of cholangitis and hepatitis.",
      "source": "rationale"
    },
    {
      "text": "Leptospirosis (Weil's disease) is discussed solely as an unverified retrospective historical hypothesis without clinical or microbiological confirmation of Leptospira infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "Philosopher Frank Ramsey, 26, male — personal name and demographics",
    "mid-November 1929, 1930, College feast — historical dates and biographical trivia",
    "Excluded as non-target case — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Leptospirosis`)
- Verify all `8` rows in `output_leptospirosis.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Ensure zero personal names, dates, illness day numbers, or pipeline tokens remain in `ground_truth_reasoning` or `claims`.


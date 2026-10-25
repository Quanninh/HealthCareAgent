---
name: gt-reasoning-chikungunya-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Chikungunya cases in selected_case_ft_pofs/output_chikungunya.jsonl across OUT_OF_SCOPE (rewritten from NEGATIVE) and POSITIVE reference rules.
---

# Chikungunya — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_chikungunya.jsonl`)

- **Disease Key:** `"Chikungunya"`
- **Input File:** `selected_case_ft_pofs/output_chikungunya.jsonl` (`2` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active Chikungunya virus (`CHIKV`) infection confirmed by serum/CSF/tissue RT-PCR, viral isolation, IgM/IgG seroconversion or rising titer, or acute anti-CHIKV IgM ELISA in a compatible clinical syndrome (acute fever, severe debilitating polyarthralgia/arthritis, maculopapular rash).
  - **`OUT_OF_SCOPE` (`2` rows, rewritten from `2` `NEGATIVE` + `0` `EXCLUDED_NON_TARGET_CASE`):**
    1. `PMC3931215_01` (`NEGATIVE` → `OUT_OF_SCOPE`): Painful cervical necrotizing lymphadenitis, fever, and subsequent polyarthralgia where clinical suspicion of chikungunya was explicitly refuted by a negative chikungunya serum IgM ELISA (`"The chikungunya IgM antibody was not detected by serum IgM ELISA"`).
    2. `PMC5771939_04` (`NEGATIVE` → `OUT_OF_SCOPE`): Acute febrile illness with rash initially suspected clinically as chikungunya, but laboratory testing for chikungunya was negative and definitive testing confirmed *Rickettsia typhi* (murine typhus) infection.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Diagnosis or Syndrome with Negative CHIKV Testing> — Not Chikungunya)."`
  - `PMC3931215_01`: `"OUT_OF_SCOPE (Febrile necrotizing cervical lymphadenitis with negative Chikungunya IgM ELISA — Not Chikungunya)."`
  - `PMC5771939_04`: `"OUT_OF_SCOPE (Rickettsia typhi infection — Not Chikungunya)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Chikungunya (Chikungunya virus infection)."` (or specify focal manifestation such as `"Chikungunya (Chikungunya virus encephalitis)."`).
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogens & Alternative Etiologies:** Keep `Chikungunya virus (CHIKV)` and confirmed alternative pathogens such as `Rickettsia typhi` (murine typhus).
2. **Diagnostic Assays:** Keep `chikungunya serum IgM ELISA`, `CHIKV RT-PCR`, `plaque reduction neutralization test (PRNT)`, and rickettsial confirmatory testing.
3. **Clinical Features:** Keep `painful cervical necrotizing lymphadenitis`, `symmetrical polyarthralgia`, `acute febrile illness`, and `maculopapular rash`.

### Strip (Log in `dropped_specifics`)
- Patient age and sex (`"41-year-old male"`, `"12-year-old male"`).
- Hospital/illness timeline markers (`"on day 10"`), case numbers (`"case 4"`), and pipeline jargon (`"E0 refuting/contradicted evidence"`, `"fail VPD criteria"`, `"Assigned NEGATIVE"`).

---

## 4. Worked Examples (All `2` Cases in `selected_case_ft_pofs/output_chikungunya.jsonl`)

### Example 1 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC3931215_01::Chikungunya`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Suspected diagnosis of Chikungunya evaluated in patient with necrotizing lymphadenitis and arthralgia"`
- `rationale`: `"A 41-year-old male with painful cervical lymphadenopathy, fever, and later polyarthralgia. While clinicians posited a clinical diagnosis based on symptoms, specific laboratory testing was explicitly negative: 'The chikungunya IgM antibody was not detected by serum IgM ELISA' (E0 refuting/contradicted evidence). Under strict gold-standard curation rules, supportive symptoms (E3) in the presence of a negative specific assay fail VPD criteria. Assigned NEGATIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"The chikungunya IgM antibody was not detected by serum IgM ELISA."`

**Target Output:**
```json
{
  "pair_id": "PMC3931215_01::Chikungunya",
  "case_id": "PMC3931215_01",
  "target_disease": "Chikungunya",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Febrile necrotizing cervical lymphadenitis with negative Chikungunya IgM ELISA — Not Chikungunya). Reasoning: (1) Clinical presentation includes fever, painful cervical necrotizing lymphadenitis, and subsequent polyarthralgia raising initial syndromic suspicion of chikungunya. (2) Specific serological testing by chikungunya serum IgM ELISA does not detect anti-chikungunya IgM antibodies, refuting acute Chikungunya virus infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation includes fever, painful cervical necrotizing lymphadenitis, and subsequent polyarthralgia raising initial syndromic suspicion of chikungunya.",
      "source": "rationale"
    },
    {
      "text": "Specific serological testing by chikungunya serum IgM ELISA does not detect anti-chikungunya IgM antibodies, refuting acute Chikungunya virus infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "41-year-old male — demographics",
    "E0 refuting/contradicted evidence, E3, fail VPD criteria, Assigned NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC5771939_04::Chikungunya`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Initial clinical diagnosis of Chikungunya evaluated and contradicted by negative testing"`
- `rationale`: `"A 12-year-old male was initially presumptively diagnosed with chikungunya clinically without testing. Upon re-evaluation on day 10, laboratory testing was performed to confirm chikungunya and yielded negative results (E0 contradictory evidence). The patient was subsequently confirmed to have Rickettsia typhi infection. Assigned NEGATIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"On this occasion, samples were taken to confirm chikungunya, yielding negative results."`

**Target Output:**
```json
{
  "pair_id": "PMC5771939_04::Chikungunya",
  "case_id": "PMC5771939_04",
  "target_disease": "Chikungunya",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Rickettsia typhi infection — Not Chikungunya). Reasoning: (1) Acute febrile illness with rash initially received a presumptive clinical diagnosis of chikungunya without laboratory verification, but subsequent chikungunya confirmatory laboratory testing yields negative results. (2) Further diagnostic evaluation confirms Rickettsia typhi infection as the true etiology of the febrile exanthem, ruling out Chikungunya virus infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute febrile illness with rash initially received a presumptive clinical diagnosis of chikungunya without laboratory verification, but subsequent chikungunya confirmatory laboratory testing yields negative results.",
      "source": "both"
    },
    {
      "text": "Further diagnostic evaluation confirms Rickettsia typhi infection as the true etiology of the febrile exanthem, ruling out Chikungunya virus infection.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "12-year-old male, case 4 — demographics and case label",
    "on day 10 — illness timeline",
    "E0 contradictory evidence, Assigned NEGATIVE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Chikungunya`)
- Verify both rows in `output_chikungunya.jsonl` (`PMC3931215_01` and `PMC5771939_04`) are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Ensure zero pipeline tokens (`E0`, `E3`, `VPD`, `Assigned NEGATIVE`) and zero demographic/timeline specifics remain in `ground_truth_reasoning` or `claims`.


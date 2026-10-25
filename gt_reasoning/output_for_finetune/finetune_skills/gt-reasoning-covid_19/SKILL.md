---
name: gt-reasoning-covid_19-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for COVID-19 cases in selected_case_ft_pofs/output_covid_19.jsonl across POSITIVE (active SARS-CoV-2 infection) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE).
---

# COVID-19 — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_covid_19.jsonl`)

- **Disease Key:** `"COVID-19"`
- **Input File:** `selected_case_ft_pofs/output_covid_19.jsonl` (`2,649` total rows — largest file in `selected_case_ft_pofs/`)
  - **`POSITIVE` (`1,777` rows):** Active `SARS-CoV-2` infection (including acute COVID-19 pneumonia, ARDS, multisystem inflammatory syndrome `MIS-C`/`MIS-A`, COVID-19-associated coagulopathy/neurological complications, or confirmed active nosocomial/concurrent SARS-CoV-2 comorbidity) verified by RT-PCR/NAAT, rapid antigen test, viral sequencing/IHC, or acute SARS-CoV-2 serology with typical bilateral ground-glass opacities (`GGO`).
    - *Empty `evidence_items` Note:* `218` `POSITIVE` rows have `step9_key_evidence.evidence_items == []`. For these rows, extract claims from `rationale` and `step5_concept_grounding` (with `source: "rationale"` or `"step5"`).
  - **`OUT_OF_SCOPE` (`872` rows, rewritten from `332` `NEGATIVE` + `540` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out (`332` `NEGATIVE` rows):**
       - Suspected COVID-19 pneumonia/myocarditis or mandatory pre-operative/admission pandemic SARS-CoV-2 RT-PCR/antigen screening that tested explicitly **negative**, while an out-of-scope diagnosis was established (e.g., congenital left main coronary artery atresia in `PMC9634233_01`, anaplastic/papillary thyroid collision tumor in `PMC8717010_01`, bacterial/fungal pneumonia, autoimmune pneumonitis, heart failure, malignancy).
    2. **Resolved Historical Past Infection (`EXCLUDED_NON_TARGET_CASE`, `HISTORICAL_PAST`, `F4_ASSERTION_TEMPORAL`):**
       - Prior COVID-19 episode that had fully resolved weeks or months before the current presentation for an unrelated active condition (e.g., oncologic management in `PMC8107669_01` and `PMC8107669_02`, elective surgery, post-infectious sequelae with negative active viral testing).
    3. **COVID-19 Vaccination / Pandemic Context / Prophylaxis (`EXCLUDED_NON_TARGET_CASE`, `PREVENTION_VACCINATION`, `F5_DISCOURSE_CONTEXT`):**
       - Post-vaccination adverse events (mRNA/adenoviral vector vaccine-associated myocarditis, VITT/TTS, Guillain-Barré syndrome, cutaneous reactions) without SARS-CoV-2 viral infection, or pandemic lockdown/telemedicine healthcare delivery context.
    4. **Non-Target Coronavirus Species (`EXCLUDED_NON_TARGET_CASE`, `F6_EVIDENCE_SPECIFICITY`):**
       - Infection by Middle East respiratory syndrome coronavirus (`MERS-CoV`) or seasonal human coronaviruses (`HCoV-OC43`, `HCoV-229E`, `HCoV-NL63`, `HCoV-HKU1`), not `SARS-CoV-2`.
    - *Empty `evidence_items` Note:* `331` `OUT_OF_SCOPE` rows have `step9_key_evidence.evidence_items == []` and/or concise template rationales (e.g., `"COVID-19 infection occurred in the past and is fully resolved/historical; patient presented for cancer management."`). Combine `rationale`, `step5_concept_grounding`, and the non-target clinical condition in `step3_patient_anchor` (stripping age/sex) to produce complete, self-contained `OUT_OF_SCOPE` claims.

---

## 2. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"COVID-19 (SARS-CoV-2 infection)."` or specify the focal syndrome / comorbidity context when prominent:
  - `"COVID-19 (SARS-CoV-2 pneumonia and acute respiratory distress syndrome)."`
  - `"COVID-19 (nosocomial SARS-CoV-2 pneumonia complicating herpes simplex encephalitis)."`
  - `"COVID-19 (acute transverse myelitis with concurrent SARS-CoV-2 infection)."`
  - `"COVID-19 (multisystem inflammatory syndrome associated with SARS-CoV-2)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Condition or Non-Target Context> — Not COVID-19)."`
  - *Rule-out examples:*
    - `"OUT_OF_SCOPE (Congenital left main coronary artery atresia with negative SARS-CoV-2 RT-PCR — Not COVID-19)."`
    - `"OUT_OF_SCOPE (Thyroid collision carcinoma with negative pre-operative SARS-CoV-2 RT-PCR screening — Not COVID-19)."`
  - *Historical / Vaccine / Non-target coronavirus examples:*
    - `"OUT_OF_SCOPE (Oncologic management with resolved prior SARS-CoV-2 infection — Not Active COVID-19)."`
    - `"OUT_OF_SCOPE (Post-COVID-19 vaccination adverse reaction without SARS-CoV-2 infection — Not COVID-19)."`
    - `"OUT_OF_SCOPE (MERS-CoV / seasonal human coronavirus infection — Not COVID-19)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogen & Variant/Gene Targets:** Keep `SARS-CoV-2`, target genes (`N`, `E`, `RdRp`, `ORF1ab`, `S`), Variants of Concern (`Alpha`, `Delta`, `Omicron`), and non-target coronaviruses (`MERS-CoV`, `HCoV-OC43`, `HCoV-229E`, `HCoV-NL63`).
2. **Diagnostic Assays & Specimens:** Keep `reverse transcription-polymerase chain reaction (RT-PCR)`, `nucleic acid amplification test (NAAT)`, `rapid SARS-CoV-2 antigen test`, `anti-SARS-CoV-2 IgM/IgG serology`, and specimen source (`nasopharyngeal swab`, `oropharyngeal swab`, `tracheal aspirate`, `bronchoalveolar lavage fluid`).
3. **Imaging & Clinical Syndromes:** Keep `bilateral ground-glass opacities (GGO)`, `crazy-paving pattern`, `acute respiratory distress syndrome (ARDS)`, `multisystem inflammatory syndrome (MIS-C / MIS-A)`, `cytokine release syndrome`, and `anosmia/dysgeusia`.
4. **Cycle Threshold (`Ct`) Values & Biomarkers:** Convert raw `Ct` numbers (`"Ct = 18.4"`) to `"low cycle threshold (high viral load) on RT-PCR"`. Convert raw `SpO2`, `PaO2/FiO2`, `D-dimer`, `ferritin`, `CRP`, `IL-6`, `ProBNP`, and `LVEF` values to qualitative clinical descriptions (`"severe hypoxemia"`, `"markedly elevated D-dimer and inflammatory markers"`, `"elevated natriuretic peptide"`, `"severely reduced left ventricular ejection fraction"`).

### Strip (Log in `dropped_specifics`)
- Patient age, sex, and pregnancy week/gravida counts.
- Calendar dates (`"September 2020"`, `"November 2020"`), hospital day numbers (`"on day 8 of hospitalization"`), and drug dosages (`"remdesivir 200 mg followed by 100 mg once daily for 4 days"`, `"dexamethasone 8 mg once daily for 6 days"` — keep drug names `"remdesivir and dexamethasone"` without dosages).
- Raw `Ct` numbers, raw `SpO2` percentages, raw `LVEF` percentages (`"20-25%"`), raw `ProBNP` (`"1,950 pg/ml"`), and `CO-RADS` scores (convert to `"chest CT findings typical of viral pneumonia"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_covid_19.jsonl`)

### Example 1 — `POSITIVE` (`PMC9702593_03::COVID-19`)
**Input Record:**
- `step12_dataset_label`: `"POSITIVE"`, `step5_concept_grounding`: `"Hospital-acquired acute COVID-19 pneumonia complicating HSV-1 encephalitis confirmed by tracheal aspirate RT-PCR"`
- `rationale`: `"A 79-year-old female hospitalized for HSV-1 encephalitis developed clinical, biochemical, and radiological pneumonia on day 8 of admission. Diagnostic RT-PCR of a tracheal aspirate confirmed the detection of SARS-CoV-2 RNA, and she was treated with remdesivir and dexamethasone. E1 confirmatory lab evidence satisfies all criteria for active COVID-19 pneumonia as an active comorbidity in the current episode -> POSITIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC9702593_03::COVID-19",
  "case_id": "PMC9702593_03",
  "target_disease": "COVID-19",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "COVID-19 (nosocomial SARS-CoV-2 pneumonia complicating herpes simplex virus encephalitis). Reasoning: (1) Hospitalization for herpes simplex virus type 1 (HSV-1) encephalitis is complicated by the development of clinical, biochemical, and radiological signs of acute pneumonia. (2) Tracheal aspirate reverse transcription-polymerase chain reaction (RT-PCR) detects SARS-CoV-2 RNA, confirming active COVID-19 pneumonia managed with antiviral therapy (remdesivir) and systemic corticosteroids (dexamethasone). -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Hospitalization for herpes simplex virus type 1 (HSV-1) encephalitis is complicated by the development of clinical, biochemical, and radiological signs of acute pneumonia.",
      "source": "both"
    },
    {
      "text": "Tracheal aspirate reverse transcription-polymerase chain reaction (RT-PCR) detects SARS-CoV-2 RNA, confirming active COVID-19 pneumonia managed with antiviral therapy (remdesivir) and systemic corticosteroids (dexamethasone).",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "79-year-old female — demographics",
    "on day 8 of hospitalization — hospital timeline",
    "200 mg followed by 100 mg once daily for 4 days, 8 mg once daily for 6 days — medication dosages and durations",
    "E1 confirmatory lab evidence ... -> POSITIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC9634233_01::COVID-19`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Suspected COVID-19 in a toddler with acute heart failure ruled out by negative RT-PCR"`
- `rationale`: `"A 2-year-old toddler presented with de novo heart failure with severely reduced LVEF (20-25%). Prior flu-like illness raised initial suspicion of COVID-19-related myocarditis, but COVID-19 PCR tested negative (E0 contradicted). Subsequent coronary angiography confirmed congenital left main coronary artery atresia as the cause of ischemic heart disease. The target disease was specifically investigated and ruled out -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC9634233_01::COVID-19",
  "case_id": "PMC9634233_01",
  "target_disease": "COVID-19",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Congenital left main coronary artery atresia with negative SARS-CoV-2 RT-PCR — Not COVID-19). Reasoning: (1) De novo heart failure with severely reduced left ventricular ejection fraction and elevated natriuretic peptide following an antecedent flu-like illness raises initial suspicion of SARS-CoV-2 myocarditis, but respiratory SARS-CoV-2 RT-PCR testing is negative. (2) Coronary angiography establishes congenital left main coronary artery atresia causing ischemic cardiomyopathy as the definitive diagnosis, ruling out COVID-19. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "De novo heart failure with severely reduced left ventricular ejection fraction and elevated natriuretic peptide following an antecedent flu-like illness raises initial suspicion of SARS-CoV-2 myocarditis, but respiratory SARS-CoV-2 RT-PCR testing is negative.",
      "source": "both"
    },
    {
      "text": "Coronary angiography establishes congenital left main coronary artery atresia causing ischemic cardiomyopathy as the definitive diagnosis, ruling out COVID-19.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "2-year-old toddler — demographics",
    "LVEF (20-25%) — converted to severely reduced left ventricular ejection fraction",
    "ProBNP 1,950 pg/ml — converted to elevated natriuretic peptide",
    "(E0 contradicted), -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC8107669_01::COVID-19`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step7_temporality`: `"HISTORICAL_PAST"`, `step8_clinical_role`: `"PAST_HISTORY"`
- `rationale`: `"COVID-19 infection occurred in the past and is fully resolved/historical; patient presented for cancer management."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"he developed severe COVID-19, from which he recovered in November 2020"`

**Target Output:**
```json
{
  "pair_id": "PMC8107669_01::COVID-19",
  "case_id": "PMC8107669_01",
  "target_disease": "COVID-19",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Active oncologic management following resolved prior COVID-19 — Not Active COVID-19). Reasoning: (1) Clinical presentation is solely for active malignancy management, while documented severe SARS-CoV-2 infection represents a prior historical episode from which full clinical recovery occurred before the current admission. (2) There is no active SARS-CoV-2 infection during the current clinical episode. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation is solely for active malignancy management, while documented severe SARS-CoV-2 infection represents a prior historical episode from which full clinical recovery occurred before the current admission.",
      "source": "both"
    },
    {
      "text": "There is no active SARS-CoV-2 infection during the current clinical episode.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "65.0 male — demographics",
    "in November 2020 — calendar date"
  ]
}
```

---

## 5. Pre-Emission Checklist (`COVID-19`)
- Verify all `2,649` rows are emitted (`1,777` `"POSITIVE"`, `872` `"OUT_OF_SCOPE"`).
- Verify that all `218` `POSITIVE` rows and `331` `OUT_OF_SCOPE` rows with empty `evidence_items` (`[]`) have non-empty, self-contained `claims[]` derived from `rationale` and `step5_concept_grounding`.
- Confirm zero raw `Ct` numbers, `SpO2` percentages, drug dosages, dates, or pipeline codes remain in `ground_truth_reasoning` or `claims`.


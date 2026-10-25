---
name: gt-reasoning-hiv_aids-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for HIV/AIDS cases in selected_case_ft_pofs/output_hiv_aids.jsonl across POSITIVE (active HIV infection / AIDS) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE).
---

# HIV/AIDS — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_hiv_aids.jsonl`)

- **Disease Key:** `"HIV_AIDS"`
- **Input File:** `selected_case_ft_pofs/output_hiv_aids.jsonl` (`1,134` total rows)
  - **`POSITIVE` (`828` rows):** Active Human Immunodeficiency Virus (`HIV-1` or `HIV-2`) infection or Acquired Immunodeficiency Syndrome (`AIDS`) — whether newly diagnosed or established/chronic comorbidity on antiretroviral therapy (`ART`/`HAART`) — confirmed by 4th-generation HIV-1/2 Ag/Ab immunoassay, Western blot, HIV-1/2 differentiation assay, plasma HIV RNA viral load (`RT-PCR`), or documented HIV infection with CD4+ T-lymphocyte depletion (`CD4 < 200 cells/mm3` or `< 200 cells/uL` defining AIDS, or inverted `CD4/CD8` ratio) and/or AIDS-defining opportunistic infections or malignancies.
  - **`OUT_OF_SCOPE` (`306` rows, rewritten from `224` `NEGATIVE` + `82` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out (`224` `NEGATIVE` rows):**
       - Routine or targeted HIV serology / Ag-Ab screening / HIV RNA PCR performed during evaluation of an opportunistic-like malignancy, infection, or immunodeficiency syndrome that tested explicitly **negative / nonreactive** (e.g., sinonasal plasmablastic lymphoma with nonreactive HIV serology in `PMC9170507_01`; ocular syphilis with negative HIV titers in `PMC5015792_01`; cryptococcosis, Kaposi sarcoma, lymphoma, tuberculosis, or HLH in HIV-negative hosts).
    2. **Maternal / Partner / Donor HIV Exposure Without Patient Infection (`EXCLUDED_NON_TARGET_CASE`, `F3_SUBJECT_COREFERENCE`):**
       - HIV-exposed uninfected (`HEU`) neonates or infants born to HIV-positive mothers (e.g., `PMC8560288_01`: neonate with alobar holoprosencephaly and cebocephaly born to an HIV-positive mother on HAART, without infant HIV diagnosis), or occupational/sexual post-exposure prophylaxis (`PEP`/`PrEP`) without seroconversion.
    3. **Lexical Homonym Collision (`EXCLUDED_NON_TARGET_CASE`, `F1_LEXICAL_HOMONYM`):**
       - English noun `"aids"` referring to assistive medical devices rather than Acquired Immunodeficiency Syndrome (e.g., `"walking aids"` in orthopedic rehabilitation in `PMC8438790_01`, `"hearing aids"`, `"visual aids"`).
    4. **Non-Human Immunodeficiency Virus or Background Discourse (`EXCLUDED_NON_TARGET_CASE`, `F5_DISCOURSE_CONTEXT`, `F6_EVIDENCE_SPECIFICITY`):**
       - Feline immunodeficiency virus (`FIV`), simian immunodeficiency virus (`SIV`), or general epidemiological/literature mentions without patient HIV infection.
    - *Empty `evidence_items` Note:* `40` `OUT_OF_SCOPE` rows have `step9_key_evidence.evidence_items == []`. Extract their claims from `rationale`, `step5_concept_grounding`, and the clinical condition in `step3_patient_anchor`.

---

## 2. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:**
  - When `CD4 < 200 cells/mm3` (`< 200 cells/uL`) or an AIDS-defining illness is present: `"HIV/AIDS (advanced Human Immunodeficiency Virus infection with <Opportunistic Infection / Malignancy / profound CD4 lymphopenia>)."`
  - When chronic/newly diagnosed HIV without AIDS-defining criteria: `"HIV/AIDS (Human Immunodeficiency Virus infection)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Diagnosis or Non-Target Context> — Not HIV/AIDS)."`
  - *Rule-out examples:*
    - `"OUT_OF_SCOPE (Sinonasal plasmablastic lymphoma with nonreactive HIV serology — Not HIV/AIDS)."`
    - `"OUT_OF_SCOPE (Acute syphilitic posterior placoid chorioretinitis with negative HIV serology — Not HIV/AIDS)."`
  - *Maternal exposure / Lexical homonym examples:*
    - `"OUT_OF_SCOPE (Neonatal alobar holoprosencephaly with maternal HIV history but no infant HIV infection — Not HIV/AIDS)."`
    - `"OUT_OF_SCOPE (Orthopedic foot fracture rehabilitation using walking aids — Not HIV/AIDS)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Virological & Immunological Markers:**
   - Keep `HIV-1`, `HIV-2`, `HIV-1/2 antigen/antibody combination immunoassay`, `Western blot`, `plasma HIV-1 RNA viral load`, `CD4+ T-lymphocyte count`, and `CD4/CD8 ratio inversion`.
   - **CD4 Threshold Conversion:**
     - If raw `CD4 < 200 cells/uL` (e.g., `82 cells/microL`, `14 cells/uL`), convert to `"profound CD4+ T-lymphocyte depletion (< 200 cells/mm3, AIDS-defining threshold)"` and log the exact count in `dropped_specifics`.
     - If raw `CD4` is `200–499 cells/uL` (e.g., `324 cells/uL`), convert to `"reduced CD4+ T-lymphocyte count (< 500 cells/mm3)"` and log the exact number in `dropped_specifics`.
   - **Viral Load Conversion:** Convert raw HIV RNA copy numbers (`"450,000 copies/mL"`, `"< 20 copies/mL"`) to `"markedly elevated plasma HIV-1 RNA viremia"` or `"virological suppression (undetectable plasma HIV-1 RNA) on antiretroviral therapy"`.
2. **Co-Infections & Opportunistic Conditions:** Keep `Pneumocystis jirovecii pneumonia (PJP)`, `cryptococcal meningitis`, `cerebral toxoplasmosis`, `cytomegalovirus (CMV) retinitis`, `Kaposi sarcoma`, `plasmablastic lymphoma`, `hemophagocytic lymphohistiocytosis (HLH)`, `parvovirus B19 aplastic crisis`, and `antiretroviral therapy (ART / HAART)` status.

### Strip (Log in `dropped_specifics`)
- Patient age, sex, race/ethnicity (`"23-year-old African American female"`), birth weight (`"2600 g"`), and gravida/para counts (`"gravida 3, para 2, 38 year-old"`).
- Raw CBC/chemistry values (`"WBC 1.67 x 10^3/L"`, `"Hb 6.2 g/dL"` → `"neutropenia and severe anemia"`), exact CD4 numbers/percentages/ratios (`"324/mul"`, `"14.2%"`, `"0.2"` → convert to qualitative/threshold descriptions), and specific rehabilitation distances/days (`"On the 30th day"`, `"walk 300 m outdoors"`).
- Pipeline tokens (`"E1_CONFIRMATORY_LAB"`, `"E2_HIGHLY_SPECIFIC"`, `"E0_CONTRADICTED"`, `"F1_LEXICAL_HOMONYM"`, `"F3_SUBJECT_COREFERENCE"`, `"-> NEGATIVE"`, `"-> EXCLUDED_NON_TARGET_CASE"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_hiv_aids.jsonl`)

### Example 1 — `POSITIVE` (`PMC6806112_01::HIV_AIDS`)
**Input Record:**
- `step12_dataset_label`: `"POSITIVE"`, `step5_concept_grounding`: `"Perinatally acquired human immunodeficiency virus (HIV) infection with CD4 lymphopenia (82 cells/microL) complicated by acute parvovirus B19 aplastic anemia and secondary HLH"`
- `rationale`: `"A 23-year-old African American female with documented vertically acquired HIV infection managed with antiretroviral therapy presented with septic shock, pancytopenia, acute parvovirus B19 viremia, and severe immunosuppression (CD4 count 82 cells/microL). She developed secondary hemophagocytic lymphohistiocytosis (HLH) confirmed on bone marrow biopsy and elevated soluble CD25, treated with etoposide, dexamethasone, and IVIG while maintaining antiretroviral therapy. Established perinatally acquired HIV with profound CD4 lymphopenia satisfies diagnostic criteria -> POSITIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC6806112_01::HIV_AIDS",
  "case_id": "PMC6806112_01",
  "target_disease": "HIV_AIDS",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "HIV/AIDS (perinatally acquired Human Immunodeficiency Virus infection with profound CD4 lymphopenia). Reasoning: (1) Established vertically acquired HIV infection managed with antiretroviral therapy is accompanied by profound CD4+ T-lymphocyte depletion (< 200 cells/mm3, AIDS-defining threshold). (2) Severe HIV-associated immunosuppression is complicated by acute parvovirus B19 viremia, pancytopenia, and secondary hemophagocytic lymphohistiocytosis (HLH) confirmed on bone marrow biopsy. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Established vertically acquired HIV infection managed with antiretroviral therapy is accompanied by profound CD4+ T-lymphocyte depletion (< 200 cells/mm3, AIDS-defining threshold).",
      "source": "both"
    },
    {
      "text": "Severe HIV-associated immunosuppression is complicated by acute parvovirus B19 viremia, pancytopenia, and secondary hemophagocytic lymphohistiocytosis (HLH) confirmed on bone marrow biopsy.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "23-year-old African American female — demographics",
    "3-day history — illness duration",
    "white blood cell count 1.67 x 103/L, hemoglobin 6.2 g/dL — converted to pancytopenia",
    "CD4 count 82 cells/microL — converted to < 200 cells/mm3 AIDS-defining threshold"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC9170507_01::HIV_AIDS`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Evaluation for underlying HIV infection in a patient presenting with plasmablastic lymphoma; serology was nonreactive"`
- `rationale`: `"A 61-year-old male presented with epistaxis and nasal obstruction and was diagnosed with plasmablastic lymphoma of the paranasal sinuses. Because plasmablastic lymphoma is strongly associated with HIV-induced immunosuppression, HIV serology was tested; it was nonreactive. Target disease is ruled out -> NEGATIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"Hepatitis B, hepatitis C, and HIV serologies were nonreactive."`

**Target Output:**
```json
{
  "pair_id": "PMC9170507_01::HIV_AIDS",
  "case_id": "PMC9170507_01",
  "target_disease": "HIV_AIDS",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Sinonasal plasmablastic lymphoma with nonreactive HIV serology — Not HIV/AIDS). Reasoning: (1) Presentation with epistaxis and nasal obstruction leads to a diagnosis of sinonasal plasmablastic lymphoma, prompting evaluation for underlying HIV-associated immunosuppression. (2) Diagnostic HIV serology is nonreactive alongside negative hepatitis B and hepatitis C serologies, ruling out HIV infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Presentation with epistaxis and nasal obstruction leads to a diagnosis of sinonasal plasmablastic lymphoma, prompting evaluation for underlying HIV-associated immunosuppression.",
      "source": "rationale"
    },
    {
      "text": "Diagnostic HIV serology is nonreactive alongside negative hepatitis B and hepatitis C serologies, ruling out HIV infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "61-year-old male — demographics",
    "Target disease is ruled out -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC8438790_01::HIV_AIDS`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F1_LEXICAL_HOMONYM"]`
- `rationale`: `"A 37-year-old female nurse was rehabilitated after an acute left foot fracture. The candidate disease match 'aids' arose entirely from the lexical homonym 'walking aids' ('able to walk 300 m outdoors without walking aids'), denoting physical assistive devices. The clinical narrative has zero connection to HIV infection or acquired immunodeficiency syndrome. Excluded due to lexical homonym collision -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC8438790_01::HIV_AIDS",
  "case_id": "PMC8438790_01",
  "target_disease": "HIV_AIDS",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Orthopedic foot fracture rehabilitation — Not HIV/AIDS). Reasoning: (1) Clinical management involves orthopedic rehabilitation and functional mobility recovery following an acute foot fracture, achieving independent ambulation without assistive walking aids. (2) The term walking aids refers exclusively to physical mobility devices, with no clinical or laboratory evidence of Human Immunodeficiency Virus (HIV) infection or acquired immunodeficiency syndrome (AIDS). -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical management involves orthopedic rehabilitation and functional mobility recovery following an acute foot fracture, achieving independent ambulation without assistive walking aids.",
      "source": "both"
    },
    {
      "text": "The term walking aids refers exclusively to physical mobility devices, with no clinical or laboratory evidence of Human Immunodeficiency Virus (HIV) infection or acquired immunodeficiency syndrome (AIDS).",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "37-year-old female nurse, left — demographics, occupation, and laterality",
    "On the 30th day, 300 m — rehabilitation timeline and distance",
    "Excluded due to lexical homonym collision -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`HIV_AIDS`)
- Verify all `1,134` rows are emitted (`828` `"POSITIVE"`, `306` `"OUT_OF_SCOPE"`).
- Confirm that all `40` `OUT_OF_SCOPE` rows with empty `evidence_items` (`[]`) have complete, self-contained `claims[]`.
- Verify all raw CD4 counts and viral load copy numbers are converted to threshold/qualitative terms and logged in `dropped_specifics`.


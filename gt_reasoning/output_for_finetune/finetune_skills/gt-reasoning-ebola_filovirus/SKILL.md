---
name: gt-reasoning-ebola_filovirus-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Ebola/Filovirus cases in selected_case_ft_pofs/output_ebola_filovirus.jsonl across OUT_OF_SCOPE (neurosurgical EVD homonyms and Lassa fever rewritten from EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Ebola & Filovirus Disease — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_ebola_filovirus.jsonl`)

- **Disease Key:** `"Ebola_Filovirus"`
- **Input File:** `selected_case_ft_pofs/output_ebola_filovirus.jsonl` (`22` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active Filovirus infection — *Orthoebolavirus* (`Zaire ebolavirus` / `EBOV`, `Sudan ebolavirus` / `SUDV`, `Bundibugyo ebolavirus` / `BDBV`, `Tai Forest ebolavirus`) or *Orthomarburgvirus* (`Marburg virus` / `MARV`, `Ravn virus`) — confirmed by blood/oral swab/body fluid `RT-PCR`, `viral antigen capture ELISA`, `filovirus-specific IgM ELISA`, or viral isolation.
  - **`OUT_OF_SCOPE` (`22` rows, rewritten from `0` `NEGATIVE` + `22` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Neurosurgical Acronym Homonym Collision — External Ventricular Drain (`EVD`) (`21` rows, `F1_LEXICAL_HOMONYM`):**
       - In `21` of `22` rows (e.g., `PMC9215869_01`, `PMC2876252_01`), the abbreviation `"EVD"` or phrase `"external ventricular drain / drainage"` refers to a neurosurgical cerebrospinal fluid (`CSF`) diversion catheter placed for obstructive hydrocephalus, intraventricular hemorrhage, subarachnoid hemorrhage, pineocytoma, neurocysticercosis, or traumatic brain injury — **not** Ebola Virus Disease (`EVD`).
    2. **Non-Target Viral Hemorrhagic Fever Differential / Lassa Fever (`1` row, `PMC5748105_02`):**
       - `PMC5748105_02`: Maternal/peripartum viral hemorrhagic fever in an endemic West African setting caused by **Lassa fever** (*Arenaviridae*), where Ebola virus disease is mentioned only as epidemiological outbreak context, with no filovirus infection in the patient.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Primary Neurosurgical/Clinical Condition with External Ventricular Drain or Alternative Disease> — Not Ebola or Filovirus Disease)."`
  - *EVD homonym examples:*
    - `"OUT_OF_SCOPE (Pineocytoma with neurosurgical external ventricular drain placement — Not Ebola Virus Disease)."`
    - `"OUT_OF_SCOPE (Third-ventricular neurocysticercosis with obstructive hydrocephalus requiring external ventricular drainage — Not Ebola Virus Disease)."`
  - *Lassa fever example (`PMC5748105_02`):*
    - `"OUT_OF_SCOPE (Lassa fever — Not Ebola or Filovirus Disease)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Ebola Virus Disease (Zaire ebolavirus infection)."` or `"Marburg Virus Disease (Marburg virus infection)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Neurosurgical / Clinical Condition & Procedure (in `OUT_OF_SCOPE` EVD rows):**
   - Keep the actual primary neurological pathology (`pineocytoma`, `third-ventricular neurocysticercosis`, `intraventricular hemorrhage`, `aneurysmal subarachnoid hemorrhage`, `obstructive hydrocephalus`, `ventriculitis`, `bacterial meningitis`) and the neurosurgical procedure (`external ventricular drain [EVD] placement for cerebrospinal fluid diversion`).
   - State clearly in the second claim that `"EVD"` denotes a neurosurgical `external ventricular drain` catheter rather than `Ebola virus disease`, and that no filovirus infection is present.
2. **Alternative Hemorrhagic Fever Pathogens:** Keep `Lassa virus / Lassa fever` in `PMC5748105_02`.

### Strip (Log in `dropped_specifics`)
- Patient age and sex (`"51-year-old woman"`, `"24-year-old male"`).
- Intracranial pressure numbers (`"25 cmH2O"`), drain output volumes, catheter French sizes, and calendar dates.
- Pipeline jargon (`"Lexical collision:"`, `"F1_LEXICAL_HOMONYM"`, `"Excluded as a non-target case"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_ebola_filovirus.jsonl`)

### Example 1 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC9215869_01::Ebola_Filovirus`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F1_LEXICAL_HOMONYM"]`
- `rationale`: `"A 51-year-old woman with a pineal tumor diagnosed as pineocytoma underwent endoscopic biopsy and external ventricular drain implantation. The mention of 'external ventricular drain' (EVD) is an acronym/lexical collision with Ebola virus disease. There is no filovirus infection or Ebola clinical claim. Excluded as a non-target case."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"Thus, the patient underwent an endoscopic biopsy and external ventricular drain implantation."`

**Target Output:**
```json
{
  "pair_id": "PMC9215869_01::Ebola_Filovirus",
  "case_id": "PMC9215869_01",
  "target_disease": "Ebola_Filovirus",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Pineocytoma managed with endoscopic biopsy and external ventricular drain — Not Ebola Virus Disease). Reasoning: (1) Intracranial pineal region tumor diagnosed histopathologically as pineocytoma is managed neurosurgically with endoscopic biopsy and external ventricular drain (EVD) implantation for cerebrospinal fluid diversion. (2) The abbreviation EVD refers exclusively to a neurosurgical external ventricular drain procedure, with no clinical or laboratory evidence of Ebola virus or filovirus infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Intracranial pineal region tumor diagnosed histopathologically as pineocytoma is managed neurosurgically with endoscopic biopsy and external ventricular drain (EVD) implantation for cerebrospinal fluid diversion.",
      "source": "both"
    },
    {
      "text": "The abbreviation EVD refers exclusively to a neurosurgical external ventricular drain procedure, with no clinical or laboratory evidence of Ebola virus or filovirus infection.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "51-year-old woman — demographics",
    "Lexical collision / Excluded as a non-target case — pipeline jargon stripped"
  ]
}
```

### Example 2 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC2876252_01::Ebola_Filovirus`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F1_LEXICAL_HOMONYM"]`
- `rationale`: `"A 24-year-old male presented with obstructive hydrocephalus due to a third ventricular neurocysticercosis cyst. An EVD (external ventricular drain) was placed urgently for CSF diversion. The term 'EVD' represents neurosurgical drainage, not Ebola virus disease. Excluded as a non-target case."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"An EVD was placed urgently to treat the obstructive hydrocephalus."`

**Target Output:**
```json
{
  "pair_id": "PMC2876252_01::Ebola_Filovirus",
  "case_id": "PMC2876252_01",
  "target_disease": "Ebola_Filovirus",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Third-ventricular neurocysticercosis with obstructive hydrocephalus requiring external ventricular drainage — Not Ebola Virus Disease). Reasoning: (1) Acute obstructive hydrocephalus secondary to a third-ventricular neurocysticercosis cyst requires urgent placement of a neurosurgical external ventricular drain (EVD) for cerebrospinal fluid diversion. (2) The acronym EVD denotes external ventricular drainage rather than Ebola virus disease, and no filovirus infection is present. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute obstructive hydrocephalus secondary to a third-ventricular neurocysticercosis cyst requires urgent placement of a neurosurgical external ventricular drain (EVD) for cerebrospinal fluid diversion.",
      "source": "both"
    },
    {
      "text": "The acronym EVD denotes external ventricular drainage rather than Ebola virus disease, and no filovirus infection is present.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "24-year-old male — demographics",
    "Excluded as a non-target case — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Ebola_Filovirus`)
- Verify all `22` rows in `output_ebola_filovirus.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Confirm every row clearly states the actual neurosurgical/clinical pathology and disambiguates `"EVD"` (or Lassa fever) in clean clinical prose without `F1_LEXICAL_HOMONYM` or `EXCLUDED_NON_TARGET_CASE` tokens.


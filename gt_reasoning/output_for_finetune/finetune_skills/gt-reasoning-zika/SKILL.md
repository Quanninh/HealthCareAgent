---
name: gt-reasoning-zika-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Zika cases in selected_case_ft_pofs/output_zika.jsonl across OUT_OF_SCOPE (negative ZIKV RT-PCR/serology rule-outs and historical congenital Zika background comorbidities rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Zika Virus Disease — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_zika.jsonl`)

- **Disease Key:** `"Zika"`
- **Input File:** `selected_case_ft_pofs/output_zika.jsonl` (`6` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active Zika virus (`ZIKV`, *Orthoflavivirus zikaense*) infection or laboratory-confirmed acute congenital Zika syndrome evaluated during the active diagnostic episode, confirmed by serum, whole blood, urine, CSF, amniotic fluid, or placental tissue `ZIKV RT-PCR` / `qRT-PCR`, viral isolation, or `anti-ZIKV IgM MAC-ELISA` confirmed by plaque reduction neutralization testing (`PRNT90` with `>= 4-fold` higher titer than dengue/flaviviruses).
  - **`OUT_OF_SCOPE` (`6` rows, rewritten from `2` `NEGATIVE` + `4` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out (`2` `NEGATIVE` rows):**
       - `PMC5177614_03`: Bilateral peripheral facial nerve palsy and Guillain-Barré syndrome (`GBS`) presenting during a Zika outbreak, where urine real-time `ZIKV qRT-PCR` was negative and no active Zika virus infection was confirmed.
       - `PMC6415467_02`: Breastfed infant monitored after ingesting breast milk containing detectable ZIKV RNA from an infected mother; serial infant urine `ZIKV RT-PCR` (7 samples) and infant blood `Zika IgM and IgG serology` were all explicitly negative, confirming absence of ZIKV transmission to the infant.
    2. **Historical Congenital Zika Syndrome Comorbidity in Unrelated Procedural/Surgical Cases (`2` `EXCLUDED_NON_TARGET_CASE` rows, `HISTORICAL_PAST`, `INCIDENTAL_FINDING`):**
       - `PMC9339746_01`: Pediatric dental clinic presentation for CAD/CAM crown restoration of a malformed deciduous incisor causing hand self-injury in a child with historical congenital Zika virus syndrome (`ZVCS`), with no active Zika infection or diagnostic laboratory testing in the current dental episode.
       - `PMC8280763_01`: Massive hemorrhage from a **tracheoinnominate fistula** following tracheostomy managed by endovascular stenting, where congenital Zika syndrome is noted only as a chronic baseline neurological comorbidity without active ZIKV workup.
    3. **Maternal/Epidemiological Discourse or Non-Zika Condition (`2` `EXCLUDED_NON_TARGET_CASE` rows):**
       - `PMC5660769_01` & `PMC6415467_01`: Non-target clinical presentation or epidemiological/maternal breast-milk surveillance context where the evaluated patient record does not represent an active target Zika case in `selected_case_ft_pofs/`.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Primary Clinical Condition or Surveillance Context> — Not Active Zika Virus Infection)."`
  - Examples:
    - `"OUT_OF_SCOPE (Guillain-Barré syndrome with negative urine Zika virus qRT-PCR — Not Zika)."`
    - `"OUT_OF_SCOPE (Uninfected breastfed infant with negative serial Zika RT-PCR and serology despite maternal breast-milk ZIKV RNA — Not Zika)."`
    - `"OUT_OF_SCOPE (Pediatric dental malformation restoration with historical congenital Zika syndrome comorbidity — Not Active Zika)."`
    - `"OUT_OF_SCOPE (Tracheoinnominate fistula hemorrhage with baseline chronic neurological Zika comorbidity — Not Active Zika)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Zika Virus Disease (acute Zika virus infection)."` or `"Congenital Zika Syndrome (congenital Zika virus infection)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Virological & Serological Assays:** Keep `urine and serum ZIKV qRT-PCR / RT-PCR`, `anti-Zika IgM and IgG serology`, and `plaque reduction neutralization test (PRNT)`.
2. **Clinical Syndromes & Procedures:** Keep `Guillain-Barré syndrome (GBS) with bilateral peripheral facial nerve palsy`, `maternal breast-milk ZIKV RNA exposure without infant transmission`, `restorative dental crown rehabilitation for a malformed deciduous incisor`, and `tracheoinnominate fistula hemorrhage managed with endovascular stenting` in the setting of `historical congenital Zika syndrome (microcephaly and arthrogryposis)`.

### Strip (Log in `dropped_specifics`)
- Patient age and sex (`"Male in his 60s"`, `"10-month-old infant"` → keep `"breastfed infant"`, strip `"10-month-old"`, `"20-month-old female"`, `"3-year-old girl"`).
- Geographic names and institutions (`"Suriname"`, `"School of Dentistry Clinic"`), exact calendar dates and sample counts (`"collected 7 times between December 12, 2017 and January 5, 2018"`, `"January 5 and 30, 2018"`, `"at day four after admission"`), and figure citations (`"(Figures 1A and 1B)"`).
- Pipeline tokens (`"E0 non-confirmatory/refuting evidence"`, `"E0_CONTRADICTED"`, `"F4_ASSERTION_TEMPORAL"`, `"F5_DISCOURSE_CONTEXT"`, `"Assigned NEGATIVE"`, `"Excluded as non-target case"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_zika.jsonl`)

### Example 1 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC5177614_03::Zika`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Evaluation of suspected acute Zika virus infection in patient with GBS"`
- `rationale`: `"A male in his 60s presenting with bilateral peripheral facial nerve palsy and Guillain-Barré syndrome during a Zika outbreak in Suriname. Local real-time RT-PCR on urine was negative for ZIKV (E0 non-confirmatory/refuting evidence). No active confirmed Zika infection was documented in the clinical case presentation. Assigned NEGATIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"ZIKV qRT-PCR was performed locally on urine taken at day four after admission and was negative."`

**Target Output:**
```json
{
  "pair_id": "PMC5177614_03::Zika",
  "case_id": "PMC5177614_03",
  "target_disease": "Zika",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Guillain-Barré syndrome with negative urine Zika virus qRT-PCR — Not Zika). Reasoning: (1) Neurological presentation with bilateral peripheral facial nerve paralysis and Guillain-Barré syndrome (GBS) during an arboviral outbreak prompts diagnostic evaluation for Zika virus infection. (2) Urine quantitative reverse transcription-polymerase chain reaction (qRT-PCR) testing for Zika virus is negative, and no confirmatory evidence of active Zika virus infection is established. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Neurological presentation with bilateral peripheral facial nerve paralysis and Guillain-Barré syndrome (GBS) during an arboviral outbreak prompts diagnostic evaluation for Zika virus infection.",
      "source": "rationale"
    },
    {
      "text": "Urine quantitative reverse transcription-polymerase chain reaction (qRT-PCR) testing for Zika virus is negative, and no confirmatory evidence of active Zika virus infection is established.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "Male in his 60s — demographics",
    "in Suriname, at day four after admission — geographic location and hospital timeline",
    "E0 non-confirmatory/refuting evidence, Assigned NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC6415467_02::Zika`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Surveillance and laboratory exclusion of Zika virus transmission in breastfed infant"`
- `rationale`: `"A 10-month-old infant monitored following daily ingestion of breast milk containing ZIKV RNA from an infected mother. Serial urine RT-PCR tests (collected 7 times) and serum IgM/IgG serology were negative (E0 refuting evidence), definitively confirming lack of transmission. Assigned NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC6415467_02::Zika",
  "case_id": "PMC6415467_02",
  "target_disease": "Zika",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Uninfected breastfed infant with negative serial Zika RT-PCR and serology — Not Zika). Reasoning: (1) Diagnostic surveillance is performed on a breastfed infant following ingestion of breast milk containing detectable Zika virus (ZIKV) RNA from an infected mother. (2) Serial infant urine ZIKV RT-PCR assays and infant serum Zika IgM and IgG serology tests are consistently negative, confirming the absence of Zika virus transmission. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Diagnostic surveillance is performed on a breastfed infant following ingestion of breast milk containing detectable Zika virus (ZIKV) RNA from an infected mother.",
      "source": "both"
    },
    {
      "text": "Serial infant urine ZIKV RT-PCR assays and infant serum Zika IgM and IgG serology tests are consistently negative, confirming the absence of Zika virus transmission.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "10-month-old — exact infant age",
    "collected 7 times between December 12, 2017 and January 5, 2018; January 5 and 30, 2018 — exact sample count and calendar dates",
    "E0 refuting evidence, Assigned NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC9339746_01::Zika`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step7_temporality`: `"HISTORICAL_PAST"`, `step8_clinical_role`: `"INCIDENTAL_FINDING"`
- `rationale`: `"A 20-month-old female presenting to a pediatric dental clinic for CAD/CAM restoration of a pointed deciduous incisor. Although noted to have congenital Zika virus syndrome with microcephaly and arthrogryposis, no diagnostic laboratory confirmation (PCR or serology) is reported in the case narrative. The primary subject of the report is restorative dental technique, and Zika is a historical congenital background comorbidity without active infection or E1/E2 evidence in the current episode. Excluded as non-target case."`

**Target Output:**
```json
{
  "pair_id": "PMC9339746_01::Zika",
  "case_id": "PMC9339746_01",
  "target_disease": "Zika",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Dental crown restoration for a malformed deciduous incisor with historical congenital Zika syndrome comorbidity — Not Active Zika). Reasoning: (1) Clinical presentation is for restorative dental crown rehabilitation of a pointed deciduous incisor causing hand self-injury. (2) Congenital Zika virus syndrome with microcephaly and arthrogryposis is noted solely as a chronic historical baseline comorbidity, with no active Zika virus infection or virological testing during the dental episode. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation is for restorative dental crown rehabilitation of a pointed deciduous incisor causing hand self-injury.",
      "source": "both"
    },
    {
      "text": "Congenital Zika virus syndrome with microcephaly and arthrogryposis is noted solely as a chronic historical baseline comorbidity, with no active Zika virus infection or virological testing during the dental episode.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "20-month-old female — demographics",
    "School of Dentistry Clinic, (Figures 1A and 1B) — institution name and figure citations",
    "E1/E2 evidence, Excluded as non-target case — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Zika`)
- Verify all `6` rows in `output_zika.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Ensure zero calendar dates, exact sample counts, patient demographics, or pipeline tokens (`E0`, `E1/E2`, `Assigned NEGATIVE`, `Excluded as non-target case`) remain in `ground_truth_reasoning` or `claims`.


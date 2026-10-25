---
name: gt-reasoning-rabies-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Rabies cases in selected_case_ft_pofs/output_rabies.jsonl across OUT_OF_SCOPE (rabies post-exposure prophylaxis, vaccine adverse events, and forensic putrefaction rewritten from EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Rabies — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_rabies.jsonl`)

- **Disease Key:** `"Rabies"`
- **Input File:** `selected_case_ft_pofs/output_rabies.jsonl` (`12` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active human rabies encephalomyelitis (furious or paralytic form) caused by *Rabies lyssavirus* (`RABV`) or related *Lyssavirus* species, confirmed by saliva/nuchal skin biopsy/CSF/brain tissue `RT-PCR` or `mNGS`, direct fluorescent antibody (`DFA`) testing, Negri bodies on brain histopathology, or rabies-specific neutralizing antibodies (`RFFIT` / `FAVN`) in CSF or in serum of an unvaccinated patient.
  - **`OUT_OF_SCOPE` (`12` rows, rewritten from `0` `NEGATIVE` + `12` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Rabies Post-Exposure Prophylaxis (`PEP`) for Animal Bite Trauma or Non-Rabies Wound Infections (`8` rows, `PREVENTION_VACCINATION`, `F5_DISCOURSE_CONTEXT`):**
       - Patients presenting with animal bite/scratch injuries (horse bite crush injury in `PMC6374822_01`, dog/cat/monkey/wild animal bites, or *Capnocytophaga* / *Pasteurella* / bacterial wound infections) who received precautionary **rabies vaccine and/or rabies immunoglobulin (`RIG` / `ERIG`)** as post-exposure prophylaxis (`PEP`), with **zero rabies viral infection**.
    2. **Rabies Vaccine or Immunoglobulin Adverse Events (`3` rows, `PREVENTION_VACCINATION`, `F5_DISCOURSE_CONTEXT`):**
       - Adverse immunological or hematological reactions triggered by rabies immunization rather than rabies virus infection:
         - `PMC9085745_01`: Rabies vaccination-induced **thrombotic thrombocytopenic purpura (`TTP`)** with `ADAMTS13` inhibitory autoantibodies after a cat scratch.
         - Post-vaccination acute disseminated encephalomyelitis (`ADEM`) / neuroparalytic reaction or equine rabies immunoglobulin (`ERIG`) **serum sickness**.
    3. **Non-Rabies Forensic / Postmortem Context (`1` row, `PMC10869617_01`):**
       - Postmortem forensic decomposition / putrefaction artifact or dog scavenging where rabies is mentioned only in background context without antemortem rabies encephalomyelitis.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Primary Clinical Condition / Rabies PEP or Vaccine Adverse Event> — Not Rabies)."`
  - Examples:
    - `"OUT_OF_SCOPE (Rabies vaccine-associated thrombotic thrombocytopenic purpura — Not Rabies)."`
    - `"OUT_OF_SCOPE (Traumatic animal-bite finger fracture-dislocation managed with rabies post-exposure prophylaxis — Not Rabies)."`
    - `"OUT_OF_SCOPE (Equine rabies immunoglobulin-induced serum sickness — Not Rabies)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Rabies (Rabies lyssavirus encephalomyelitis)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Presenting Non-Target Pathology & Immunological Markers:** Keep `thrombotic thrombocytopenic purpura (TTP)`, `ADAMTS13 inhibitory autoantibodies`, `serum sickness`, `post-vaccination acute disseminated encephalomyelitis (ADEM)`, `traumatic animal-bite crush injury and fracture-dislocation`, and bacterial wound pathogens (`Pasteurella`, `Capnocytophaga`).
2. **Prophylaxis & Immunization Context:** Keep `rabies post-exposure prophylaxis (PEP)`, `inactivated human rabies vaccine`, and `human or equine rabies immunoglobulin (RIG / ERIG) wound infiltration`. Explicitly state that rabies immunization was administered prophylactically or caused an immune-mediated adverse reaction, and that no active *Rabies lyssavirus* infection is present.

### Strip (Log in `dropped_specifics`)
- Patient age, sex, and anatomical laterality (`"49-year-old female"`, `"left foot"`, `"23-year-old male"`).
- Calendar dates (`"March 28, April 4, April 6, and April 12"`), vaccine manufacturer and batch numbers (`"Ningbo Rongan Biological Manufacturing Co., Ltd., drug batch number: National Medicine Standard S20073014"`), and immunoglobulin dosages (`"20 IU/kg"`).
- Pipeline tokens (`"PREVENTION_VACCINATION"`, `"F5_DISCOURSE_CONTEXT"`, `"E4_CONTEXT"`, `"-> EXCLUDED_NON_TARGET_CASE"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_rabies.jsonl`)

### Example 1 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC9085745_01::Rabies`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step8_clinical_role`: `"PREVENTION_VACCINATION"`
- `rationale`: `"A 49-year-old woman received rabies vaccination after a cat scratch and developed thrombotic thrombocytopenic purpura (TTP) confirmed by positive ADAMTS13 inhibitory autoantibodies. Rabies is involved solely as a vaccination/immunization event causing an adverse reaction, not active viral infection. Under protocol rules, vaccine adverse event cases are non-target → EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC9085745_01::Rabies",
  "case_id": "PMC9085745_01",
  "target_disease": "Rabies",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Rabies vaccine-associated thrombotic thrombocytopenic purpura — Not Rabies). Reasoning: (1) Following post-exposure immunization with freeze-dried human rabies vaccine after a cat scratch, clinical manifestations and positive ADAMTS13 inhibitory autoantibodies establish a diagnosis of vaccine-related thrombotic thrombocytopenic purpura (TTP). (2) Rabies involvement is limited to an adverse hematological reaction following prophylactic vaccination, with no active Rabies lyssavirus infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Following post-exposure immunization with freeze-dried human rabies vaccine after a cat scratch, clinical manifestations and positive ADAMTS13 inhibitory autoantibodies establish a diagnosis of vaccine-related thrombotic thrombocytopenic purpura (TTP).",
      "source": "both"
    },
    {
      "text": "Rabies involvement is limited to an adverse hematological reaction following prophylactic vaccination, with no active Rabies lyssavirus infection.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "49-year-old female, left foot — demographics and laterality",
    "March 28, April 4, April 6, and April 12, a total of 4 times — vaccination dates and dose count",
    "Ningbo Rongan Biological Manufacturing Co., Ltd., drug batch number: National Medicine Standard S20073014 — manufacturer and batch number",
    "Under protocol rules, vaccine adverse event cases are non-target -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC6374822_01::Rabies`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step8_clinical_role`: `"PREVENTION_VACCINATION"`
- `rationale`: `"A 23-year-old male sustained a traumatic crush injury and fracture dislocation of his finger from a domestic horse bite. Rabies immune globulin and rabies vaccine were administered purely as post-exposure prophylaxis (PEP). The patient never had rabies infection. Clinical role is PREVENTION_VACCINATION → EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC6374822_01::Rabies",
  "case_id": "PMC6374822_01",
  "target_disease": "Rabies",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Traumatic horse-bite finger crush injury and fracture-dislocation managed with rabies post-exposure prophylaxis — Not Rabies). Reasoning: (1) Acute presentation involves a traumatic digital crush injury and fracture-dislocation sustained from a domestic horse bite. (2) Human rabies immune globulin and rabies vaccine are administered strictly as routine post-exposure prophylaxis (PEP) for an animal bite wound, with no clinical or laboratory evidence of rabies viral infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute presentation involves a traumatic digital crush injury and fracture-dislocation sustained from a domestic horse bite.",
      "source": "rationale"
    },
    {
      "text": "Human rabies immune globulin and rabies vaccine are administered strictly as routine post-exposure prophylaxis (PEP) for an animal bite wound, with no clinical or laboratory evidence of rabies viral infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "23-year-old male — demographics",
    "20 IU/kg — immunoglobulin dosage",
    "Clinical role is PREVENTION_VACCINATION -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Rabies`)
- Verify all `12` rows in `output_rabies.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Confirm all vaccine batch numbers, manufacturer names, vaccination dates, and IU/kg dosages are stripped and logged in `dropped_specifics`.
- Ensure zero pipeline tokens (`PREVENTION_VACCINATION`, `EXCLUDED_NON_TARGET_CASE`, `E4_CONTEXT`) remain in `ground_truth_reasoning` or `claims`.


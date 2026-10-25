---
name: gt-reasoning-extractor
description: Master coordinator skill for extracting generalized ground_truth_reasoning, atomic RAGAS evaluation claims, and dropped_specifics from step9_key_evidence and rationale across all 15 diseases in selected_case/output_*.jsonl.
---

# Ground Truth Reasoning Extractor — Master Coordinator

## 1. Objective
Transform case-specific annotation fields (`step9_key_evidence` and `rationale`, supplemented by `step5_concept_grounding` when `rationale` is a template) in `/Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/reasoning_extract/selected_case/output_{disease}.jsonl` into a generalized, case-de-identified JSON object for evaluating `<Disease Name> + <Reasoning>` in the **RAGAS** evaluation framework.

---

## 2. Per-Disease Skill Routing Table

Route each record by its `disease_key` / source file to the corresponding disease-specific skill:

| Disease Key | Input JSONL File | Disease GT Reasoning Skill |
| :--- | :--- | :--- |
| `Brucellosis` | `selected_case/output_brucellosis.jsonl` | `skills/gt-reasoning-brucellosis/SKILL.md` |
| `Chikungunya` | `selected_case/output_chikungunya.jsonl` | `skills/gt-reasoning-chikungunya/SKILL.md` |
| `Cholera` | `selected_case/output_cholera.jsonl` | `skills/gt-reasoning-cholera/SKILL.md` |
| `COVID-19` | `selected_case/output_covid_19.jsonl` | `skills/gt-reasoning-covid_19/SKILL.md` |
| `Dengue` | `selected_case/output_dengue.jsonl` | `skills/gt-reasoning-dengue/SKILL.md` |
| `Ebola_Filovirus` | `selected_case/output_ebola_filovirus.jsonl` | `skills/gt-reasoning-ebola_filovirus/SKILL.md` |
| `HIV_AIDS` | `selected_case/output_hiv_aids.jsonl` | `skills/gt-reasoning-hiv_aids/SKILL.md` |
| `Leishmaniasis` | `selected_case/output_leishmaniasis.jsonl` | `skills/gt-reasoning-leishmaniasis/SKILL.md` |
| `Leptospirosis` | `selected_case/output_leptospirosis.jsonl` | `skills/gt-reasoning-leptospirosis/SKILL.md` |
| `Malaria` | `selected_case/output_malaria.jsonl` | `skills/gt-reasoning-malaria/SKILL.md` |
| `Rabies` | `selected_case/output_rabies.jsonl` | `skills/gt-reasoning-rabies/SKILL.md` |
| `Tuberculosis` | `selected_case/output_tuberculosis.jsonl` | `skills/gt-reasoning-tuberculosis/SKILL.md` |
| `Typhoid_Fever` | `selected_case/output_typhoid_fever.jsonl` | `skills/gt-reasoning-typhoid_fever/SKILL.md` |
| `Yellow_Fever` | `selected_case/output_yellow_fever.jsonl` | `skills/gt-reasoning-yellow_fever/SKILL.md` |
| `Zika` | `selected_case/output_zika.jsonl` | `skills/gt-reasoning-zika/SKILL.md` |

---

## 3. Target Output Schema

Every case must output a valid JSON object matching `/Users/Me/Desktop/Khailambaitest/final_year/chatbot/project/reasoning_extract/reference_gt_reasoning/` (without `requires` tags):

```json
{
  "ground_truth_reasoning": "<Disease Name> (<pathogen/clinical entity>). Reasoning: (1) <Claim 1>. (2) <Claim 2>. (3) <Claim 3>. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "<Claim 1>", "source": "rationale | step9"},
    {"text": "<Claim 2>", "source": "rationale | step9"},
    {"text": "<Claim 3>", "source": "rationale | step9"}
  ],
  "dropped_specifics": [
    "<Exact patient age, sex, occupation, or location>",
    "<Exact patient-specific lab measurements, titers, doses, dates, and excluded follow-up clearance tests>"
  ]
}
```

---

## 4. Universal Transformation Rules Across All 15 Diseases

### 4.1 Map Evidence Tiers (`E1`, `E2`, `E3`, `E0`) to Natural Diagnostic Roles
- Replace `E1_CONFIRMATORY` / `E1` with *"definitive confirmation by..."*, *"confirmatory pathogen detection via..."*, or *"definitive microbiological/molecular identification..."*.
- Replace `E2_HIGHLY_SPECIFIC` / `E2` with *"highly specific serological/antigen evidence..."* or *"presumptive confirmation by..."*.
- Replace `E3_SUPPORTIVE` / `E3` with *"supported by characteristic clinical, laboratory, or imaging findings..."*.
- Never emit raw `E1`, `E2`, `E3`, `E0`, `E1_CONFIRMATORY`, `E2_HIGHLY_SPECIFIC`, `E3_SUPPORTIVE`, `E0_CONTRADICTED`, or `E4_CONTEXT` in `ground_truth_reasoning` or `claims`.

### 4.2 Strip Pipeline Metadata & `VPD` Keywords
- Strip all occurrences of `VPD`, `Valid Positive Diagnosis`, `qualifies as a VPD`, `making it a VPD`, `CONFIRMED_PRESENT`, `CURRENT_EPISODE`, `PRIOR_HISTORY`, `FOLLOW_UP`, `PRIMARY_DIAGNOSIS`, `SECONDARY_CONDITION`, `COMPLICATION`, `INCIDENTAL`, `Historical/Baseline`, `patient_1`, and `S0`–`S9`.

### 4.3 Standardize `POSITIVE` Keywords
- Convert `result: "POSITIVE"` in `step9_key_evidence` into descriptive diagnostic prose inside the reasoning body.
- Standardize the trailing suffix of `ground_truth_reasoning` to:
  `-> POSITIVE diagnosis confirmed.`

### 4.4 Values and Numbers Rule (`STRIP` vs. `KEEP` vs. `CONVERT`)
Apply this rule to every number or designation encountered in `rationale` and `step9_key_evidence`:

1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`74-year-old`), sex (`male`/`female`)
   - Specific country, city, or institution
   - Hospitalization day (`"on day 3"`), time since exposure (`"50 days ago"`)
   - Exact titer in this patient (`"1:160"`, `"1:100 (++)"`)
   - Exact lab value in this patient (`"ESR 58 mm/hr"`, `"CRP 165.08"`, `"WBC 11,200"`)
   - Exact drug dose for this patient (`"0.6 g Qd"`, `"0.1 g BID"`)
   - Incubation time (`"72 h incubation"`)
   - Specific serovar/strain designations when used as patient-specific findings (keep them only if they generalize, e.g., `"Leptospira interrogans serovars"`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Diagnostic thresholds (`"titer ≥1:160 or ≥1:400 is significant"`, `"PRNT90%"`)
   - Seroconversion rules (`"≥4-fold rise in paired sera is diagnostic"`)
   - Standard duration rules (`"6-week doxycycline-based regimen"`, `"6-month standard anti-tuberculosis regimen"`)
   - Cutoffs (`"troponin above the 99th percentile upper reference limit"`)
   - Clinical definitions (`"fever >38.3°C"`, `"thrombocytopenia <150,000/µL"`, `"CD4 count <200 cells/µL defining AIDS"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation:**
   - `"CRP 165.08"` → `"markedly elevated CRP indicates systemic inflammation"`
   - `"ESR 58"` → `"elevated ESR supports an inflammatory process"`
   - `"1:160"` → `"positive at a significant titer"` OR `"positive at a titer consistent with the diagnostic threshold, depending on the assay"`
   - `"0.6 g Qd doxycycline"` → `"doxycycline-based regimen"`
   - **Never drop the clinical *interpretation* just because the patient-specific number was stripped.**

### 4.5 Handle Dataset-Specific Edge Cases
- **Boilerplate/Template `rationale`s** (prominent in `Tuberculosis` [91/100 rows], `COVID-19` [14/100 rows], and `Brucellosis` [rows 46–100]): Reconstruct clinical presentation and test specifics directly from `step9_key_evidence.evidence_items[].source_quote`, `test_name`, `specimen`, and `step5_concept_grounding`.
- **Follow-Up / Post-Treatment Clearance Items** (`FOLLOW_UP` temporality, `NEGATIVE` / `PARASITE_CLEARANCE` results in `COVID-19`, `Malaria`, `Leishmaniasis`, `Cholera`, `Typhoid_Fever`): Exclude from diagnostic GT claims and log in `dropped_specifics`.
- **Compound `test_name` Items** (e.g., `Rapid antigen test and RT-PCR`, `rK39 and bone marrow examination`, `Blood culture and SAT`): Unpack into separate atomic claims.
- **Discordant / Negative Screening Items** (`E0_CONTRADICTED` / `REFUTES` / `INCONCLUSIVE`): Express as a generalized diagnostic caveat (e.g., *"a negative initial smear/screening test or routine culture does not exclude the diagnosis when definitive testing is positive"*).
- **Non-Patient / Unrelated Context Items** (e.g., family member screening in `Tuberculosis`, grandmother labs in `HIV_AIDS`, unrelated malignancy/Lassa fever): Exclude and record in `dropped_specifics`.

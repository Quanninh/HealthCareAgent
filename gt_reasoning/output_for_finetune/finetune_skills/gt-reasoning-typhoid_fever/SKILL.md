---
name: gt-reasoning-typhoid_fever-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Typhoid Fever cases in selected_case_ft_pofs/output_typhoid_fever.jsonl across OUT_OF_SCOPE (non-typhoidal Salmonella infections, Kawasaki disease, and historical Widal-only mentions rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Typhoid & Enteric Fever — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_typhoid_fever.jsonl`)

- **Disease Key:** `"Typhoid_Fever"`
- **Input File:** `selected_case_ft_pofs/output_typhoid_fever.jsonl` (`10` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Active enteric fever (typhoid or paratyphoid fever) caused by *Salmonella enterica* subspecies *enterica* serovar `Typhi` (`S. Typhi`) or serovar `Paratyphi A`, `B`, or `C`, confirmed by blood, bone marrow, stool, urine, or rose-spot culture, or serovar-specific `PCR` / `mNGS`.
  - **`OUT_OF_SCOPE` (`10` rows, rewritten from `2` `NEGATIVE` + `8` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out + Alternative Diagnosis (`2` `NEGATIVE` rows):**
       - `PMC7470353_01`: Returned traveler presenting with bacteremia initially suspected clinically as typhoid fever, where antigenic serotyping of the blood culture isolate identified *Salmonella enterica* serovar **Corvallis** (a non-typhoidal *Salmonella*), ruling out typhoid fever.
       - `PMC8337161_01`: Prolonged fever and abdominal pain initially treated empirically for suspected typhoid fever with ceftriaxone without improvement; blood cultures were negative, typhoid serology was normal, and the patient was definitively diagnosed with **atypical Kawasaki disease** with coronary artery dilatation.
    2. **Non-Typhoidal *Salmonella* (`NTS`) Infections (`6` `EXCLUDED_NON_TARGET_CASE` rows, `F6_EVIDENCE_SPECIFICITY`):**
       - Invasive or localized infections caused by non-typhoidal *Salmonella* serovars rather than `S. Typhi` or `S. Paratyphi`:
         - `PMC6016173_01`: *Salmonella enteritidis* recurrent bacteremia and pancreatic/stool isolation in systemic lupus erythematosus (`SLE`).
         - Other rows: *Salmonella enteritidis*, *Salmonella* group D (non-typhoidal), or *Salmonella enterica* subsp. *arizonae* causing enteritis, bacteremia, mycotic aneurysm, or focal abscess.
    3. **Historical Widal-Only Presumed Episode Presenting with Delayed Post-Infectious Retinitis or Background Context (`2` `EXCLUDED_NON_TARGET_CASE` rows):**
       - `PMC5385597_01`: Immune-mediated retinitis presenting 4 weeks after a resolved febrile illness that had been presumptively attributed to typhoid fever based solely on non-confirmatory Widal serology without culture confirmation.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Non-Typhoidal Salmonella Serovar or Alternative Diagnosis> — Not Typhoid Fever)."`
  - Examples:
    - `"OUT_OF_SCOPE (Salmonella enterica serovar Corvallis bacteremia — Not Typhoid Fever)."`
    - `"OUT_OF_SCOPE (Atypical Kawasaki disease with coronary artery dilatation — Not Typhoid Fever)."`
    - `"OUT_OF_SCOPE (Non-typhoidal Salmonella enteritidis bacteremia — Not Typhoid Fever)."`
    - `"OUT_OF_SCOPE (Post-infectious immune-mediated retinitis following a historical Widal-only febrile illness — Not Active Typhoid Fever)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Typhoid Fever (Salmonella enterica serovar Typhi infection)."` or `"Paratyphoid Fever (Salmonella enterica serovar Paratyphi A/B/C infection)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogen Serovar Specificity (Critical for `Typhoid_Fever` vs. `OUT_OF_SCOPE`):**
   - Explicitly distinguish typhoidal serovars (`Salmonella enterica serovar Typhi`, `S. Paratyphi A/B/C`) from **non-typhoidal *Salmonella* (`NTS`)** serovars (`Salmonella enterica serovar Corvallis`, `Salmonella enteritidis`, `Salmonella enterica subsp. arizonae`, `Salmonella Typhimurium`).
2. **Diagnostic Assays & Limitations:**
   - Keep `blood, stool, and fluid culture`, `Kauffmann-White antigenic serotyping`, and `Widal tube/slide agglutination test (O and H antigens)`.
   - When Widal serology is cited in an `OUT_OF_SCOPE` historical case (`PMC5385597_01`), convert raw titers (`>1:80`, `>1:160`) to `"elevated historical Widal O and H agglutination titers"` and note that standalone Widal serology without culture/PCR confirmation is non-confirmatory and the episode is historical.
3. **Alternative Diagnoses:** Keep `atypical Kawasaki disease with coronary artery dilatation`, `systemic lupus erythematosus (SLE)`, and `immune-mediated retinitis`.

### Strip (Log in `dropped_specifics`)
- Patient age and sex (`"24-year-old male"`, `"11-year-old boy"`, `"56-year-old female"`, `"59-year-old male"`).
- Geographic names and reference labs (`"Hokkaido Institute of Public Health, Sapporo, Japan"`), antibiotic dosages (`"ceftriaxone 100 mg/kg/day"`), exact timeline counts (`"4 weeks prior"`), and raw Widal titer numbers (`">1:80"`, `">1:160"`).
- Pipeline tokens (`"Assertion ABSENT_NEGATIVE"`, `"clinical role RULED_OUT_DIAGNOSIS"`, `"VPD not satisfied -> NEGATIVE"`, `"-> EXCLUDED_NON_TARGET_CASE"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_typhoid_fever.jsonl`)

### Example 1 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC7470353_01::Typhoid_Fever`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Differential diagnosis of Typhoid_Fever evaluated in case report"`
- `rationale`: `"A 24-year-old male returning traveler presented with bacteremia. Typhoid fever was suspected clinically on admission, but definitive serological typing of the blood culture isolate identified Salmonella enterica serovar Corvallis (a non-typhoidal Salmonella), ruling out typhoid fever. Assertion ABSENT_NEGATIVE, clinical role RULED_OUT_DIAGNOSIS. VPD not satisfied -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC7470353_01::Typhoid_Fever",
  "case_id": "PMC7470353_01",
  "target_disease": "Typhoid_Fever",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Salmonella enterica serovar Corvallis bacteremia — Not Typhoid Fever). Reasoning: (1) Travel-associated febrile bacteremia initially raises clinical suspicion of primary enteric (typhoid) fever. (2) Definitive antigenic serotyping of the blood culture isolate identifies Salmonella enterica serovar Corvallis, a non-typhoidal Salmonella serovar, ruling out Salmonella Typhi or Paratyphi infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Travel-associated febrile bacteremia initially raises clinical suspicion of primary enteric (typhoid) fever.",
      "source": "both"
    },
    {
      "text": "Definitive antigenic serotyping of the blood culture isolate identifies Salmonella enterica serovar Corvallis, a non-typhoidal Salmonella serovar, ruling out Salmonella Typhi or Paratyphi infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "24-year-old male — demographics",
    "at Hokkaido Institute of Public Health, Sapporo, Japan — institution and geographic location",
    "Assertion ABSENT_NEGATIVE, clinical role RULED_OUT_DIAGNOSIS, VPD not satisfied -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC8337161_01::Typhoid_Fever`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Differential diagnosis of Typhoid_Fever evaluated in case report"`
- `rationale`: `"An 11-year-old male presented with prolonged fever and abdominal pain. Typhoid fever was initially considered and treated empirically with ceftriaxone without improvement. Blood cultures were negative and serology for typhoid was normal. He was definitively diagnosed with atypical Kawasaki disease with coronary dilatation. Assertion ABSENT_NEGATIVE, clinical role RULED_OUT_DIAGNOSIS. VPD not satisfied -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC8337161_01::Typhoid_Fever",
  "case_id": "PMC8337161_01",
  "target_disease": "Typhoid_Fever",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Atypical Kawasaki disease with coronary artery dilatation — Not Typhoid Fever). Reasoning: (1) Prolonged fever and abdominal pain initially prompt empirical intravenous ceftriaxone therapy for suspected typhoid fever without clinical improvement, while blood cultures and typhoid fever serology are negative. (2) Subsequent diagnostic evaluation establishes atypical Kawasaki disease with coronary artery dilatation, ruling out typhoid fever. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Prolonged fever and abdominal pain initially prompt empirical intravenous ceftriaxone therapy for suspected typhoid fever without clinical improvement, while blood cultures and typhoid fever serology are negative.",
      "source": "both"
    },
    {
      "text": "Subsequent diagnostic evaluation establishes atypical Kawasaki disease with coronary artery dilatation, ruling out typhoid fever.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "11-year-old boy / male — demographics",
    "100 mg/kg/day — antibiotic dosage",
    "Assertion ABSENT_NEGATIVE, clinical role RULED_OUT_DIAGNOSIS, VPD not satisfied -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC6016173_01::Typhoid_Fever`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step5_concept_grounding`: `"Non-target Salmonella enteritidis infection evaluated"`
- `rationale`: `"A 56-year-old female with SLE and recurrent bacteremia. All cultures (blood, stool, and pancreatic drainage fluid) isolated Salmonella enteritidis, a non-typhoidal Salmonella (NTS) serotype. The patient did not have typhoid fever (S. Typhi or S. Paratyphi). This is an infection caused by a non-target salmonella pathogen. VPD not satisfied -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC6016173_01::Typhoid_Fever",
  "case_id": "PMC6016173_01",
  "target_disease": "Typhoid_Fever",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Non-typhoidal Salmonella enteritidis bacteremia — Not Typhoid Fever). Reasoning: (1) Recurrent bacteremia in the setting of systemic lupus erythematosus (SLE) yields Salmonella enteritidis across blood, stool, and pancreatic drainage fluid cultures. (2) Salmonella enteritidis is a non-typhoidal Salmonella (NTS) serovar rather than Salmonella Typhi or Paratyphi, excluding typhoid or paratyphoid fever. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Recurrent bacteremia in the setting of systemic lupus erythematosus (SLE) yields Salmonella enteritidis across blood, stool, and pancreatic drainage fluid cultures.",
      "source": "both"
    },
    {
      "text": "Salmonella enteritidis is a non-typhoidal Salmonella (NTS) serovar rather than Salmonella Typhi or Paratyphi, excluding typhoid or paratyphoid fever.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "56-year-old female — demographics",
    "VPD not satisfied -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Typhoid_Fever`)
- Verify all `10` rows in `output_typhoid_fever.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Ensure every non-typhoidal *Salmonella* row explicitly states the specific NTS serovar and explains why it is not typhoid/paratyphoid fever (`S. Typhi` / `S. Paratyphi`).
- Confirm zero pipeline tokens and zero demographics/dosages remain.


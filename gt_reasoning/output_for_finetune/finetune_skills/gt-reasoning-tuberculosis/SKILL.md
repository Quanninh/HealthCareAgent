---
name: gt-reasoning-tuberculosis-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Tuberculosis cases in selected_case_ft_pofs/output_tuberculosis.jsonl across POSITIVE (active Mycobacterium tuberculosis complex infection) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE, including template rationale reconstruction).
---

# Tuberculosis — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_tuberculosis.jsonl`)

- **Disease Key:** `"Tuberculosis"`
- **Input File:** `selected_case_ft_pofs/output_tuberculosis.jsonl` (`1,227` total rows — second largest file in `selected_case_ft_pofs/`)
  - **`POSITIVE` (`942` rows):** Active pulmonary, extrapulmonary, or disseminated/miliary tuberculosis caused by *Mycobacterium tuberculosis* complex (`M. tuberculosis`, `M. bovis` wild-type, `M. africanum`) confirmed by liquid/solid mycobacterial culture (`MGIT`, `Löwenstein-Jensen`), nucleic acid amplification (`Xpert MTB/RIF`, `IS6110 PCR`, `mNGS`), Ziehl-Neelsen / auramine-rhodamine acid-fast bacilli (`AFB`) staining, or necrotizing/caseating granulomatous inflammation with Langhans giant cells and clinical/radiological response to standard multi-drug anti-tuberculosis therapy (`ATT`: isoniazid `H`, rifampicin `R`, pyrazinamide `Z`, ethambutol `E`, streptomycin `S`).
  - **`OUT_OF_SCOPE` (`285` rows, rewritten from `78` `NEGATIVE` + `207` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out + Alternative Out-of-Scope Diagnosis (`78` `NEGATIVE` rows):**
       - **Nontuberculous Mycobacteria (`NTM`) or *M. leprae* (`F6_EVIDENCE_SPECIFICITY`):** Positive AFB stain or granulomatous inflammation where `M. tuberculosis` PCR/culture was negative or speciation identified an NTM species (*M. avium* complex, *M. abscessus*, *M. marinum*, *M. chelonae*, *M. kansasii*) or *M. leprae* (e.g., `PMC4531616_01`).
       - **Explicit Negative TB Workup (`RULED_OUT_DIAGNOSIS`):** Suspected TB evaluated and ruled out via negative AFB smears, negative mycobacterial cultures, negative `Xpert MTB/RIF` / PCR, or negative `IGRA` (`QuantiFERON-TB Gold`, `T-SPOT.TB`) / tuberculin skin test (`Mantoux`), while establishing an alternative diagnosis (malignancy, sarcoidosis, fungal infection, lymphoma, autoimmune disease; e.g., `PMC3736967_01`).
    2. **Abbreviation Homonym Collision — `"TB"` = Total Bilirubin (`EXCLUDED_NON_TARGET_CASE`, `F1_LEXICAL_HOMONYM` / `F5_DISCOURSE_CONTEXT`):**
       - Laboratory liver function panels reporting `"total bilirubin (TB)"` alongside `"direct bilirubin (DB)"` and `"total bile acid (TBA)"` (e.g., `PMC8081048_01`, `PMC8081048_02` in infants with cystic fibrosis / cholestasis), with zero connection to *Mycobacterium tuberculosis*.
    3. **BCG Vaccination or Intravesical BCG Immunotherapy Complication (`EXCLUDED_NON_TARGET_CASE`, `PREVENTION_VACCINATION`):**
       - Routine neonatal Bacillus Calmette-Guérin (`BCG`) vaccination context or attenuated *M. bovis* BCG strain complications following intravesical immunotherapy for bladder cancer (`BCGitis`), not wild-type *M. tuberculosis* infection.
    4. **Remote Historical / Treated Past TB, Latent TB Screening Before Biologics, or Family/Background Mention (`EXCLUDED_NON_TARGET_CASE`):**
       - Remote history of cured tuberculosis decades earlier, negative latent TB screening prior to biologic therapy, or family/epidemiological background mention while treating an unrelated active disease.
    - *Empty `evidence_items` Note:* `9` `OUT_OF_SCOPE` rows have `step9_key_evidence.evidence_items == []`. Use `rationale`, `step5_concept_grounding`, and `step3_patient_anchor` to construct self-contained claims.

---

## 2. CRITICAL RULE: Reconstructing Generic Template Rationales in `output_tuberculosis.jsonl`

Unlike other disease files, **`output_tuberculosis.jsonl` frequently uses standardized boilerplate strings in `rationale`** across `POSITIVE`, `NEGATIVE`, and `EXCLUDED_NON_TARGET_CASE` records:
- *Boilerplate `POSITIVE` E2 rationale:* `"Patient diagnosed with active Tuberculosis based on highly specific histopathological features (e.g., caseating granulomas/Langhans giant cells) and/or positive acid-fast bacilli staining with consistent response to standard anti-tuberculosis therapy (E2 strong clinical evidence). VPD criteria fully satisfied."`
- *Boilerplate `NEGATIVE` rationale:* `"The patient presented with symptoms for which tuberculosis was explicitly investigated or noted as absent/ruled out (e.g., negative smears, negative PCR, or explicit negation in past/family history) while another primary pathology was diagnosed. Assigned NEGATIVE."`
- *Boilerplate `EXCLUDED_NON_TARGET_CASE` rationale:* `"The case focuses on an unrelated clinical condition. Tuberculosis is mentioned only in passing (e.g., differential diagnosis, family history, or background literature) without diagnostic evidence or clinical treatment of active TB in this patient. Classified as EXCLUDED_NON_TARGET_CASE."`

### Mandatory Reconstruction Procedure
1. **Never copy `"e.g., ..."` parenthetical lists from a template `rationale` into `ground_truth_reasoning` or `claims`!**
2. Always inspect `step9_key_evidence.evidence_items[].source_quote`, `test_name`, `target_concept`, and `step5_concept_grounding` first.
3. Extract the **actual case-specific clinical findings, anatomical site, imaging features, laboratory assays, and treatment response** directly from `evidence_items[].source_quote` (tagging `source: "step9"` or `"both"`).
   - For example, in `PMC6329029_06`, the boilerplate `rationale` mentions `"e.g., caseating granulomas/Langhans giant cells"`, whereas `evidence_items` actually shows `"CT brain revealed multiple tuberculomas, and Mantoux test was positive"` and `"anti-tuberculosis therapy"`. You MUST ground the reasoning in the **intracranial tuberculomas, positive Mantoux tuberculin skin test, and anti-tuberculosis therapy**, NOT the boilerplate `"e.g."` examples.
   - Similarly, in `PMC8081048_01`, the boilerplate `rationale` says `"mentioned only in passing (e.g., differential diagnosis...)"`, whereas `evidence_items[0].source_quote` shows `"total bilirubin (TB) 35.2 mumol/l, direct bilirubin (DB) 27.7 mumol/l"`. You MUST explain the **Total Bilirubin (`TB`) laboratory abbreviation collision** grounded in `step9`.

---

## 3. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Tuberculosis (Mycobacterium tuberculosis — <anatomical site / syndrome>)."`
  - Examples:
    - `"Tuberculosis (Mycobacterium tuberculosis — central nervous system tuberculoma and tuberculous meningitis)."`
    - `"Tuberculosis (pulmonary Mycobacterium tuberculosis infection)."`
    - `"Tuberculosis (extrapulmonary Mycobacterium tuberculosis spondylodiscitis / Pott disease)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Diagnosis or Non-Target Context> — Not Tuberculosis)."`
  - Examples:
    - `"OUT_OF_SCOPE (Nontuberculous mycobacterial synovial cyst infection with negative Mycobacterium tuberculosis PCR — Not Tuberculosis)."`
    - `"OUT_OF_SCOPE (Hepatic cholestasis with total bilirubin [TB] laboratory abbreviation — Not Tuberculosis)."`
    - `"OUT_OF_SCOPE (Non-tuberculous presentation with negative history and workup for tuberculosis — Not Tuberculosis)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 4. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogens & Non-Target Mycobacteria:** Keep `Mycobacterium tuberculosis`, `M. tuberculosis complex`, `nontuberculous mycobacteria (NTM)`, `Mycobacterium avium complex (MAC)`, `M. abscessus`, `M. marinum`, `M. leprae`, and `M. bovis BCG`.
2. **Diagnostic Assays & Histopathology:** Keep `Ziehl-Neelsen / auramine-rhodamine acid-fast bacilli (AFB) staining`, `MGIT / Löwenstein-Jensen mycobacterial culture`, `Xpert MTB/RIF`, `IS6110 PCR`, `Mantoux tuberculin skin test (TST)`, `interferon-gamma release assay (IGRA / QuantiFERON-TB Gold)`, `caseating (necrotizing) granulomatous inflammation with Langhans giant cells`, `elevated pleural/CSF adenosine deaminase (ADA)`, and `multi-drug anti-tuberculosis therapy (ATT: isoniazid, rifampicin, pyrazinamide, ethambutol)`.

### Strip (Log in `dropped_specifics`)
- Patient age and sex (`"4.0 male"`, `"8.0 female"`, `"57.0 male"`, `"0.0 male"`).
- Calendar dates (`"January 2012"`), regimen durations (`"for the past 6 months"`), steroid dosages (`"prednisolone 2 mg/kg/day"`), raw liver function numbers (`"albumin 16.5 g/L, total bilirubin 35.2 mumol/l, direct bilirubin 27.7 mumol/l, total bile acid 63.0 mumol/l"`), and table citations (`"(shown in Table 1)"`).
- All template parentheticals (`"(e.g., caseating granulomas/Langhans giant cells)"`, `"(e.g., negative smears, negative PCR...)"`, `"(e.g., differential diagnosis, family history...)"`) and pipeline tokens (`"E2 strong clinical evidence"`, `"VPD criteria fully satisfied"`, `"Assigned NEGATIVE"`, `"Classified as EXCLUDED_NON_TARGET_CASE"`).

---

## 5. Worked Examples (Directly from `selected_case_ft_pofs/output_tuberculosis.jsonl`)

### Example 1 — `POSITIVE` (`PMC6329029_06::Tuberculosis`)
**Input Record:**
- `step12_dataset_label`: `"POSITIVE"`, `step9_evidence_strength`: `"E2_HIGHLY_SPECIFIC_CLINICAL"`
- `rationale`: `"Patient diagnosed with active Tuberculosis based on highly specific histopathological features (e.g., caseating granulomas/Langhans giant cells) and/or positive acid-fast bacilli staining with consistent response to standard anti-tuberculosis therapy (E2 strong clinical evidence). VPD criteria fully satisfied."`
- `step9_key_evidence.evidence_items`:
  - `[0]`: `"CT brain revealed multiple tuberculomas, and Mantoux test was positive."`
  - `[1]`: `"Her ATT was changed to Ofx and E."`
  - `[2]`: `"On presentation to us in January 2012, she was symptomatic and ATT was shifted to HR."`

**Target Output:**
```json
{
  "pair_id": "PMC6329029_06::Tuberculosis",
  "case_id": "PMC6329029_06",
  "target_disease": "Tuberculosis",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "Tuberculosis (Mycobacterium tuberculosis — central nervous system tuberculomas). Reasoning: (1) Cranial computed tomography (CT) demonstrates multiple intracranial tuberculomas accompanied by a positive Mantoux tuberculin skin test. (2) Active central nervous system tuberculosis is managed with multi-drug anti-tuberculosis therapy (including isoniazid, rifampicin, ethambutol, and ofloxacin). -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Cranial computed tomography (CT) demonstrates multiple intracranial tuberculomas accompanied by a positive Mantoux tuberculin skin test.",
      "source": "step9"
    },
    {
      "text": "Active central nervous system tuberculosis is managed with multi-drug anti-tuberculosis therapy (including isoniazid, rifampicin, ethambutol, and ofloxacin).",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "8.0 female — demographics",
    "January 2012 — calendar date",
    "Boilerplate e.g. parentheticals and E2/VPD pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC4531616_01::Tuberculosis`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Acid-fast organism identified as nontuberculous mycobacteria (NTM) or M. leprae, not Mycobacterium tuberculosis"`
- `rationale`: `"Microbiological and clinical findings definitively established infection caused by a nontuberculous mycobacterium (NTM) or M. leprae rather than Mycobacterium tuberculosis. Per protocol Step 5 and the Evidence Specificity Matrix, AFB positivity due to non-TB mycobacteria constitutes a rule-out of target TB, yielding NEGATIVE."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"Acid fast bacillus (AFB) stain showed strong positive but polymerase chain reaction (PCR) for mycobacterium tuberculosis was organisms negative."`

**Target Output:**
```json
{
  "pair_id": "PMC4531616_01::Tuberculosis",
  "case_id": "PMC4531616_01",
  "target_disease": "Tuberculosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Nontuberculous mycobacterial synovial infection — Not Tuberculosis). Reasoning: (1) Evaluation of a multiloculated cystic mass communicating with the knee synovial cavity demonstrates a strongly positive acid-fast bacillus (AFB) stain, but specific polymerase chain reaction (PCR) testing for Mycobacterium tuberculosis is negative. (2) Positive AFB staining in the presence of a negative Mycobacterium tuberculosis PCR establishes nontuberculous mycobacterial infection and rules out tuberculosis. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Evaluation of a multiloculated cystic mass communicating with the knee synovial cavity demonstrates a strongly positive acid-fast bacillus (AFB) stain, but specific polymerase chain reaction (PCR) testing for Mycobacterium tuberculosis is negative.",
      "source": "step9"
    },
    {
      "text": "Positive AFB staining in the presence of a negative Mycobacterium tuberculosis PCR establishes nontuberculous mycobacterial infection and rules out tuberculosis.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "female — demographics",
    "Per protocol Step 5 and the Evidence Specificity Matrix ... yielding NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC8081048_01::Tuberculosis`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F5_DISCOURSE_CONTEXT"]`
- `rationale`: `"The case focuses on an unrelated clinical condition. Tuberculosis is mentioned only in passing (e.g., differential diagnosis, family history, or background literature) without diagnostic evidence or clinical treatment of active TB in this patient. Classified as EXCLUDED_NON_TARGET_CASE."`
- `step9_key_evidence.evidence_items[0]`: `target_concept`: `"Total bilirubin (TB abbreviation collision)"`, `source_quote`: `"The test results of the infant's liver function were: albumin 16.5 g/L, total bilirubin (TB) 35.2 mumol/l, direct bilirubin (DB) 27.7 mumol/l, and total bile acid (TBA) 63.0 mumol/l."`

**Target Output:**
```json
{
  "pair_id": "PMC8081048_01::Tuberculosis",
  "case_id": "PMC8081048_01",
  "target_disease": "Tuberculosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Infantile hepatic dysfunction with total bilirubin [TB] laboratory abbreviation — Not Tuberculosis). Reasoning: (1) Biochemical liver function testing demonstrates hypoalbuminemia, elevated total bilirubin (abbreviated as TB), elevated direct bilirubin (DB), and elevated total bile acids (TBA). (2) The abbreviation TB in the laboratory panel refers exclusively to serum total bilirubin rather than Mycobacterium tuberculosis infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Biochemical liver function testing demonstrates hypoalbuminemia, elevated total bilirubin (abbreviated as TB), elevated direct bilirubin (DB), and elevated total bile acids (TBA).",
      "source": "step9"
    },
    {
      "text": "The abbreviation TB in the laboratory panel refers exclusively to serum total bilirubin rather than Mycobacterium tuberculosis infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "0.0 male, infant — demographics",
    "albumin 16.5 g/L, total bilirubin 35.2 mumol/l, direct bilirubin 27.7 mumol/l, total bile acid 63.0 mumol/l — converted to qualitative biochemical descriptions",
    "Boilerplate rationale e.g. parentheticals and Classified as EXCLUDED_NON_TARGET_CASE — stripped"
  ]
}
```

---

## 6. Pre-Emission Checklist (`Tuberculosis`)
- Verify all `1,227` rows are emitted (`942` `"POSITIVE"`, `285` `"OUT_OF_SCOPE"`).
- **Template Leak Gate:** Scan all `1,227` output lines for `"e.g.,"` — there must be **zero** occurrences of `"e.g.,"` in `ground_truth_reasoning` or `claims`. Every claim must be reconstructed from the case-specific `step9_key_evidence.evidence_items` and `step5_concept_grounding`.
- Confirm zero pipeline codes and zero patient demographics/dates remain.


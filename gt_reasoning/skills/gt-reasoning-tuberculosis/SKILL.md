---
name: gt-reasoning-tuberculosis
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Tuberculosis cases in selected_case/output_tuberculosis.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, reconstructing clinical details
  when rationale is a generic template, stripping VPD/schema boilerplate, normalizing
  POSITIVE keywords, and generalizing case-specific details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Tuberculosis

## Target Disease & Data Scope
- **Target Disease:** `Tuberculosis` (*Mycobacterium tuberculosis* complex infection, including pulmonary, extrapulmonary, and disseminated/miliary tuberculosis)
- **Source File:** `selected_case/output_tuberculosis.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-tuberculosis/SKILL.md` (`03_evidence_specificity_matrix.md` §5.2)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_tuberculosis.jsonl`

| Tier in `skills/disease-agent-tuberculosis` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_tuberculosis.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive pathogen-specific microbiological or molecular confirmation of *Mycobacterium tuberculosis* complex via WHO-recommended rapid molecular diagnostics (GeneXpert MTB/RIF / Xpert Ultra, line-probe assay [LPA], or MTB-specific PCR) or mycobacterial culture isolation (e.g., Löwenstein-Jensen or MGIT liquid culture) from sputum, BAL, gastric aspirate, urine, CSF, or tissue biopsy | `GeneXpert MTB/RIF assay`, `Polymerase chain reaction (PCR) assay`, `Mycobacterial culture` | **Target:** `Mycobacterium tuberculosis`<br>**Specimen:** `sputum`, `bronchoalveolar lavage`, `gastric aspirate`, `tissue biopsy`, `bone/synovial tissue`, `synovial fluid`, `peritoneal fluid/tissue`, `urine`, `blood/serum`, `CSF` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly characteristic histopathological findings (caseating / necrotizing granulomatous inflammation with epithelioid histiocytes and Langhans giant cells) on tissue biopsy, integrated with clinical/radiological presentation, AFB staining, and clinical response to anti-tuberculosis therapy (ATT) | `Histopathological examination` (where `result: "CASEATING_GRANULOMATOUS_INFLAMMATION"` or `POSITIVE` and `target_concept: "Mycobacterium tuberculosis"`) | **Target:** `Mycobacterium tuberculosis`<br>**Specimen:** `tissue biopsy`, `lymph node tissue`, `peritoneal fluid/tissue`, `caecal biopsy tissue`, `pleural/bone biopsy` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Supportive, non-species-specific diagnostic evidence:<br>• **AFB smear microscopy** (Ziehl-Neelsen / auramine stain detects acid-fast bacilli but cannot alone distinguish *M. tuberculosis* from nontuberculous mycobacteria [NTM] without molecular/culture/histopathologic correlation)<br>• **Immunological sensitization tests** (Tuberculin Skin Test [TST / Mantoux] or Interferon-Gamma Release Assay [IGRA / QuantiFERON / T-SPOT.TB], which indicate *M. tuberculosis* sensitization/infection but do not alone differentiate latent from active TB)<br>• **Diagnostic imaging** (cavitary upper-lobe infiltrates, miliary nodules, pleural/peritoneal effusion, or spondylodiscitis/Pott's disease on CXR/CT/MRI)<br>• **Response to standard four-drug anti-tuberculosis therapy (ATT: HRZE)** | `Acid-fast bacilli (AFB) smear microscopy`, `Tuberculin skin test (Mantoux)`, `Interferon-gamma release assay (IGRA)`, `Chest/body diagnostic imaging (CT/X-ray/MRI)`, `Anti-tuberculosis therapy`, `Clinical diagnostic finding` | **Target:** `Mycobacterium tuberculosis`<br>**Specimen:** `sputum`, `gastric aspirate`, `pleural fluid/tissue`, `blood/serum`, `tissue biopsy` |
| **DISCORDANT — Negative Screening / Paucibacillary Test (`E0_CONTRADICTED` / `REFUTES`)** | Negative sputum AFB smear, negative TST/IGRA (e.g., anergy in disseminated/immunocompromised TB), or negative initial specimen when tissue biopsy histopathology, PCR/GeneXpert, or culture from the disease site is positive. Generalize as: *"A negative AFB smear (or negative TST/IGRA) does not exclude tuberculosis—particularly in paucibacillary or extrapulmonary disease—when tissue histopathology, molecular testing (GeneXpert/PCR), or culture is positive."* | `Acid-fast bacilli (AFB) smear microscopy` (`result: "NEGATIVE"`, `relation: "REFUTES"`), `Tuberculin skin test (Mantoux)` (`REFUTES`), `Interferon-gamma release assay (IGRA)` (`REFUTES`), `GeneXpert MTB/RIF assay` / `Mycobacterial culture` (`REFUTES` on non-lesional specimen when another E1/E2 test is positive) | **Target:** `Mycobacterium tuberculosis` |

---

## 2. Special Data Quality & Extraction Anomalies in `output_tuberculosis.jsonl`

> **CRITICAL INVESTIGATION FINDING:** Unlike other diseases in `selected_case/`, **91 out of 100 rows in `output_tuberculosis.jsonl` have an automated template `rationale`**, and several `step9_key_evidence` items were generated by a heuristic sentence splitter. You **MUST** apply the following verification rules when reading `output_tuberculosis.jsonl`:

### 2.1 Rule 1 — Reconstruct Specifics from `source_quote` When `rationale` is a Generic Template (91/100 rows)
In 91/100 rows of `output_tuberculosis.jsonl`, `rationale` is one of three generic templates:
1. `"A <age>-year-old <gender> presented with clinical illness confirmed as active Tuberculosis during the current clinical episode. Diagnostic workup demonstrated disease-defining evidence (E1_CONFIRMATORY_LAB), with clinical role PRIMARY_DIAGNOSIS. All Valid Positive Diagnosis (VPD) criteria fully satisfied -> POSITIVE."` (33 rows)
2. `"Patient diagnosed with active Tuberculosis based on highly specific histopathological features (e.g., caseating granulomas/Langhans giant cells) and/or positive acid-fast bacilli staining with consistent response to standard anti-tuberculosis therapy (E2 strong clinical evidence). VPD criteria fully satisfied."` (48 rows)
3. `"Patient presented with active clinical disease confirmed as Tuberculosis by molecular/microbiological assays (E1 confirmatory evidence). All Valid Positive Diagnosis (VPD) criteria satisfied -> POSITIVE."` (10 rows)

**Mandatory Action:** Never generate a vague GT reasoning just from the template! Read every `source_quote`, `test_name`, `specimen`, and `result` in `step9_key_evidence.evidence_items` (plus `step5_concept_grounding`) to identify:
- The actual anatomical site / clinical form of TB (e.g., pulmonary TB, tuberculous peritonitis, intestinal/ileocaecal TB, lymph node TB / scrofula, skeletal/synovial TB, genitourinary TB, CNS tuberculoma, or multidrug-resistant TB [MDR-TB]).
- The actual confirmatory or histopathological tests performed in `source_quote` (e.g., CT-guided biopsy showing caseous necrosis with epithelioid and Langhans giant cells, GeneXpert MTB/RIF detecting *M. tuberculosis* and rifampicin susceptibility/resistance, mycobacterial culture, AFB smear, Mantoux/IGRA, and HRZE anti-tubercular therapy).

### 2.2 Rule 2 — Verify `source_quote` Against Mis-tagged `test_name` or `result`
Because `step9_key_evidence` in `output_tuberculosis.jsonl` was partially populated by automated regex rules, always trust the literal text of `source_quote` over a mismatched `test_name` or `result` enum:
- **Split sentence trap (`PMC8605226_01`):** Item 1 has `source_quote: "...X-pert MTB/RIF on gastric aspirate was positive for M."` with `result: "COMPATIBLE_IMAGING_FINDINGS"` (because the same sentence mentioned chest radiograph infiltrate), and Item 2 has `source_quote: "tuberculosis complex with resistance to rifampicin."` mislabeled as `test_name: "Anti-tuberculosis therapy"`. Read them together as: positive TST, perihilar infiltrate on chest radiograph, and gastric aspirate Xpert MTB/RIF positive for rifampicin-resistant *M. tuberculosis* complex.
- **Family member negative screening trap (`PMC8605226_02`):** Item 1 has `source_quote: "Her parents showed negative for TB screening."` tagged as `patient_anchor_id: "patient_1"`, `strength: "E0_CONTRADICTED"`, `relation: "REFUTES"`. **Exclude** family member screening results (`dropped_specifics`) and retain the neighbour MDR-TB contact history and positive Xpert MTB/RIF with rifampicin resistance.
- **Adverse drug reaction / cessation quote trap (`PMC5648305_01`, `PMC6329029_04`):** If `source_quote` describes an adverse reaction to rifampicin or restarting/stopping ATT for tuberculomas, combine the anatomical site/clinical history from `source_quote` with the histopathological/microbiological diagnostic basis stated in `rationale`.
- **Non-TB target concept trap (`PMC9076999_01` / `Histopathological examination` with `target_concept: "Malignant neoplasm"` or `Tuberculin skin test` with `target_concept: "Leishmania species"`):** Exclude any `evidence_item` whose `source_quote` describes a ruled-out malignancy or non-TB test, and log it in `dropped_specifics`.

---

## 3. Decoding `rationale`, Stripping `VPD`, Handling `POSITIVE`, and Values/Numbers Rules

### 3.1 Replace Encoded Tier Keywords (`E1`, `E2`, `E3`) & Strip `VPD`
- Replace `(E1_CONFIRMATORY_LAB)` / `(E1 confirmatory evidence)` / `(E1)` with **`definitive microbiological or molecular confirmation`**.
- Replace `(E2 strong clinical evidence)` / `(E2_HIGHLY_SPECIFIC_CLINICAL)` / `(E2)` with **`highly specific histopathological and clinical evidence`**.
- Strip all variants of `VPD`, `Valid Positive Diagnosis`, `clinical role PRIMARY_DIAGNOSIS / COMORBIDITY`, and `VPD criteria fully satisfied`.
- Always conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.`

### 3.2 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`25.0-year-old`, `14.0-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution
   - Exact Mantoux induration size in this patient (`"18 mm induration"` → convert to `"positive Mantoux/TST induration exceeding the diagnostic threshold"`)
   - Exact lab values (`"ESR 84 mm/hr"`, `"CRP 92 mg/L"`, `"ADA 78 U/L"`) or individual milligram drug doses for this patient
   - Patient-specific non-standard treatment durations if modified due to toxicity (`"ATT for the first 4 months"`, unless referring to a standard phase rule)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Standard regimen rules (`"standard four-drug first-line anti-tuberculosis regimen (HRZE: isoniazid, rifampicin, pyrazinamide, and ethambutol)"`, `"2-month intensive HRZE phase followed by 4-month continuation HR phase [6-month standard regimen]"`)
   - Diagnostic cutoffs (`"Mantoux/TST induration ≥5 mm, ≥10 mm, or ≥15 mm depending on risk group"`, `"pleural/peritoneal/CSF adenosine deaminase [ADA] elevation above diagnostic cutoffs [e.g., >40 U/L in pleural/ascitic fluid]"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"ADA 78 U/L in ascitic/pleural fluid"` → `"markedly elevated fluid adenosine deaminase (ADA) supporting tuberculous serositis"`
   - `"ESR 84 mm/hr"` → `"elevated ESR supporting a chronic inflammatory process"`

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Template `rationale` Reconstructed from `step9_key_evidence` (`PMC9282816_01::Tuberculosis`)

**INPUT (from `selected_case/output_tuberculosis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Histopathological examination", result: "CASEATING_GRANULOMATOUS_INFLAMMATION", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Mycobacterium tuberculosis", specimen: "tissue biopsy", source_quote: "A CT-guided biopsy was diagnostic for TB; it demonstrated caseous necrosis with epithelioid and Langerhans giant cells [Figure 3]."}`
  - `{test_name: "GeneXpert MTB/RIF assay", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Mycobacterium tuberculosis", specimen: null, source_quote: "In addition, GeneXpert detected Mycobacterium tuberculosis that showed sensitivity to both isoniazid and rifampicin."}`
  - `{test_name: "Anti-tuberculosis therapy", result: "POSITIVE", strength: "E3_SUPPORTIVE", target_concept: "Mycobacterium tuberculosis", specimen: null, source_quote: "ATT for the first 4 months included rifampicin, isoniazid, pyrazinamide, and ethambutol (HRZE) (intensive phase)."}`
- `rationale`:
  `"A 25.0-year-old female presented with clinical illness confirmed as active Tuberculosis during the current clinical episode. Diagnostic workup demonstrated disease-defining evidence (E1_CONFIRMATORY_LAB), with clinical role PRIMARY_DIAGNOSIS. All Valid Positive Diagnosis (VPD) criteria fully satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Tuberculosis (Mycobacterium tuberculosis infection). Reasoning: (1) Definitive diagnosis of active tuberculosis is established by molecular detection of Mycobacterium tuberculosis complex using the GeneXpert MTB/RIF nucleic acid amplification assay, along with drug susceptibility testing confirming sensitivity to isoniazid and rifampicin. (2) Histopathological demonstration of caseous necrosis with epithelioid cells and Langhans giant cells on CT-guided tissue biopsy provides highly specific pathological evidence of tuberculosis. (3) Standard first-line intensive-phase anti-tuberculosis therapy (ATT) consists of a four-drug combination regimen with isoniazid, rifampicin, pyrazinamide, and ethambutol (HRZE). -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Definitive diagnosis of active tuberculosis is established by molecular detection of Mycobacterium tuberculosis complex using the GeneXpert MTB/RIF nucleic acid amplification assay, along with drug susceptibility testing confirming sensitivity to isoniazid and rifampicin.", "source": "step9"},
    {"text": "Histopathological demonstration of caseous necrosis with epithelioid cells and Langhans giant cells on CT-guided tissue biopsy provides highly specific pathological evidence of tuberculosis.", "source": "step9"},
    {"text": "Standard first-line intensive-phase anti-tuberculosis therapy (ATT) consists of a four-drug combination regimen with isoniazid, rifampicin, pyrazinamide, and ethambutol (HRZE).", "source": "step9"}
  ],
  "dropped_specifics": ["25.0-year-old female", "patient-specific 4-month intensive phase duration (kept standard four-drug HRZE intensive-phase rule)", "[Figure 3] reference", "generic template rationale boilerplate"]
}
```

### 4.2 Worked Example 2 — Rifampicin-Resistant / MDR Tuberculosis with Excluded Parent Screening (`PMC8605226_02::Tuberculosis`)

**INPUT (from `selected_case/output_tuberculosis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Clinical diagnostic finding", result: "NEGATIVE", strength: "E0_CONTRADICTED", relation: "REFUTES", target_concept: "Mycobacterium tuberculosis", source_quote: "Her parents showed negative for TB screening."}` ← **EXCLUDE** (family member screening, not patient)
  - `{test_name: "Clinical diagnostic finding", result: "ADMINISTERED", strength: "E3_SUPPORTIVE", relation: "SUPPORTS", target_concept: "Mycobacterium tuberculosis", source_quote: "History of tuberculosis contact is her neighbour identified MDR-TB and received treatment in our hospital."}`
  - `{test_name: "GeneXpert MTB/RIF assay", result: "POSITIVE", strength: "E1_CONFIRMATORY", relation: "SUPPORTS", target_concept: "Mycobacterium tuberculosis", source_quote: "Her X-pert MTB/RIF revealed positive Mycobacterium tuberculosis with Rifampicin resistant."}`
- `rationale`:
  `"Patient presented with active clinical disease confirmed as Tuberculosis by molecular/microbiological assays (E1 confirmatory evidence). All Valid Positive Diagnosis (VPD) criteria satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Rifampicin-resistant / Multidrug-resistant Tuberculosis (Mycobacterium tuberculosis infection). Reasoning: (1) Epidemiological contact with a known multidrug-resistant tuberculosis (MDR-TB) case is a significant risk factor for acquiring drug-resistant tuberculosis. (2) Definitive diagnosis of rifampicin-resistant tuberculosis is established by rapid molecular testing with the GeneXpert MTB/RIF assay detecting Mycobacterium tuberculosis complex and rifampicin resistance mutations. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Epidemiological contact with a known multidrug-resistant tuberculosis (MDR-TB) case is a significant risk factor for acquiring drug-resistant tuberculosis.", "source": "step9"},
    {"text": "Definitive diagnosis of rifampicin-resistant tuberculosis is established by rapid molecular testing with the GeneXpert MTB/RIF assay detecting Mycobacterium tuberculosis complex and rifampicin resistance mutations.", "source": "step9"}
  ],
  "dropped_specifics": ["14.0-year-old female", "negative TB screening in parents (excluded: family member subject, not primary patient)", "specific neighbour/hospital contact context"]
}
```

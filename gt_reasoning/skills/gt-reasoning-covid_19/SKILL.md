---
name: gt-reasoning-covid_19
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for COVID-19 cases in selected_case/output_covid_19.jsonl by decoding E1/E2/E3
  evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate from
  rationale, normalizing POSITIVE keywords, and generalizing case-specific details
  for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — COVID-19

## Target Disease & Data Scope
- **Target Disease:** `COVID-19` (*SARS-CoV-2 infection*)
- **Source File:** `selected_case/output_covid_19.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-covid_19/SKILL.md` (`03_evidence_specificity_matrix.md` §5.1)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_covid_19.jsonl`

| Tier in `skills/disease-agent-covid_19` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_covid_19.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive molecular laboratory confirmation of current SARS-CoV-2 infection | `SARS-CoV-2 RT-PCR`, `SARS-CoV-2 RT-PCR / NAAT`, `RT-PCR`, `SARS-CoV-2 PCR`, `SARS-CoV-2 RT-PCR assay`, `Repeat SARS-CoV-2 PCR`, `COVID-19 RT-PCR`, `SARS-CoV-2 nasopharyngeal swab test`, `SARS-CoV-2 diagnostic test`, `COVID-19 diagnostic test`, `Rapid antigen test and laryngopharyngeal swab RT-PCR (E and S genes)` | **Target:** `SARS-CoV-2`, `SARS-CoV-2 RNA`<br>**Specimen:** `nasopharyngeal swab`, `oropharyngeal swab`, `throat swab`, `laryngopharyngeal swab`, `nasal and throat swabs`, `respiratory swab`, `endotracheal aspirate`, `BAL` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly specific rapid antigen screening or seroconversion supporting acute/recent infection (requires RT-PCR/NAAT confirmation or clinical correlation) | `Antigen test`, `Rapid antigen test`, `SARS-CoV-2 test` (when `strength = E2_HIGHLY_SPECIFIC`), `Rapid nasopharyngeal swab for SARS-CoV-2`, `SARS-CoV-2 serology (IgG, IgM)`, `SARS-CoV-2 IgM serology`, `Clinical diagnosis and treatment` (`RECENT_EPISODIC` readmission) | **Target:** `SARS-CoV-2`, `SARS-CoV-2 antibodies`, `SARS-CoV-2 IgM antibody`<br>**Specimen:** `nasopharyngeal/throat swab`, `serum` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Supportive pulmonary imaging, histopathology, or clinical syndrome compatible with COVID-19 pneumonia/ARDS | `High-resolution chest CT`, `Chest CT`, `Thorax CT`, `Thoracic CT scan`, `Chest computed tomography (CT)`, `Abdominal/Chest CT`, `Chest X-ray`, `Lung autopsy histopathology`, `Clinical presentation and hospitalization for COVID-19`, `Clinical diagnosis of severe COVID-19 with MIS-C` | **Target:** `COVID-19-associated pneumonia`, `Patchy ground glass opacities`, `Lung basal consolidations / ground-glass attenuations`, `Viral pneumonia (COVID-19)`, `Diffuse alveolar damage`, `COVID-19 ARDS`, `Severe COVID-19 with MIS-C` |
| **EXCLUDE — Clearance / Follow-up Negative** | Viral clearance / recovery monitoring (**NOT** diagnostic of infection). **EXCLUDE** from `claims` and log in `dropped_specifics`. | `Follow-up RT-PCR`, `Follow-up SARS-CoV-2 RT-PCR`, `Follow-up RT-PCR test for COVID-19`, `Follow-up SARS-CoV-2 RT-PCR control test`, `SARS-CoV-2 viral nucleic acid resolution test` (where `result = NEGATIVE` and `strength = E1_CONFIRMATORY`) | **Target:** `SARS-CoV-2 clearance`, `SARS-CoV-2 RNA clearance`, or `SARS-CoV-2` with `result = NEGATIVE` after prior positive test |
| **DISCORDANT — Initial False Negative (`E0_CONTRADICTED` / `REFUTES`)** | Early/single negative swab superseded by subsequent positive RT-PCR or BAL/repeat testing. Generalize as: *"A single negative initial swab does not exclude COVID-19 when repeat or lower-respiratory RT-PCR is positive."* | `Initial nasopharyngeal aspirate PCR`, `Repeat nasopharyngeal aspirate PCR`, `Initial COVID-19 PCR` (`result = NEGATIVE`, `relation = REFUTES`, `strength = E0_CONTRADICTED`) | **Target:** `SARS-CoV-2 RNA` (`result = NEGATIVE`) |

### 1.2 Compound `test_name` Splitting Rule
In `output_covid_19.jsonl`, several records bundle a screening test (E2) and a confirmatory molecular test (E1) into a single `evidence_item` or `source_quote`, such as:
- `test_name: "Rapid antigen test and laryngopharyngeal swab RT-PCR (E and S genes)"` (`PMC8342944_01`)
- `source_quote: "PCR and quick antigen tests for SARS-CoV-2 from the throat swab were positive."` (`PMC10196249_02`)

**Rule:** Always split compound antigen + RT-PCR evidence into **two distinct generalized claims**:
1. **E1 Claim:** Definitive diagnosis requires molecular detection of SARS-CoV-2 RNA by RT-PCR/NAAT from a respiratory specimen (e.g., nasopharyngeal, oropharyngeal, or laryngopharyngeal swab).
2. **E2 Claim:** Rapid antigen testing is a highly specific but less sensitive screening method that supports acute infection and is confirmed by RT-PCR.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`, `E3`) in `rationale`
Never copy raw tier codes (`E1`, `E2`, `E3`, `E1_CONFIRMATORY_LAB`, `E2_HIGHLY_SPECIFIC_CLINICAL`) into `ground_truth_reasoning`. Replace them according to context:
- `(E1)`, `(E1 confirmatory evidence)`, `(E1 confirmatory viral test)`, `providing E1 confirmatory lab evidence`, `E1 confirmatory lab evidence` → **`definitive molecular laboratory confirmation`**
- `(E2)`, `(E2 evidence)`, `subsequent seroconversion on day 19 (E2)` → **`highly specific supportive screening/serological evidence`**
- `(E3)`, `(E3 supportive)` → **`supportive clinical or radiological evidence`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Remove all annotation-pipeline judgment clauses from `rationale`. Specifically strip:
- `Confirmatory testing during an active infection episode satisfies the Valid Positive Diagnosis criteria.`
- `VPD satisfied -> POSITIVE.` / `VPD criteria are satisfied -> POSITIVE.` / `VPD criteria are met -> POSITIVE.` / `VPD criteria satisfied -> POSITIVE.`
- `Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS.`
- `Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role ACTIVE_COMORBIDITY.`
- `Primary diagnosis in active current episode.` / `Primary diagnosis in active episode with E1 confirmatory testing.`
- `Single patient, active infection, primary diagnosis confirmed.` / `Single patient, active current episode, primary diagnosis confirmed.`
- `E1 confirmatory lab evidence satisfies all criteria for acute primary COVID-19 infection -> POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords
1. **In `step9_key_evidence` (`result: "POSITIVE"`, `"PRESENT"`, `"DIFFUSE_ALVEOLAR_DAMAGE"`):**
   - Do **not** write `"result is POSITIVE"` in the reasoning. Translate `result: "POSITIVE"` on an E1/E2 test into a medical principle describing what confirms or supports the diagnosis (e.g., *"Definitive diagnosis requires molecular detection of SARS-CoV-2 RNA by RT-PCR from a respiratory specimen"*).
   - If `result: "NEGATIVE"` has `target_concept: "SARS-CoV-2 clearance"` (or is a follow-up test on day 10+), **exclude it** from `ground_truth_reasoning` and record it in `dropped_specifics`.
2. **At the end of `ground_truth_reasoning`:**
   - Replace the raw `-> POSITIVE.` suffix from `rationale` with the standardized concluding token:
     `-> POSITIVE diagnosis confirmed.`

### 2.4 Fallback Rule for Boilerplate `rationale` Rows (14/100 rows in `output_covid_19.jsonl`)
In `output_covid_19.jsonl`, 14 rows have a generic template `rationale` such as:
- `"Patient diagnosed with active COVID-19 confirmed by positive SARS-CoV-2 RT-PCR or NAAT/antigen testing in current episode."` (`PMC10196249_01`–`04`, `PMC8168796_01`, `PMC8531932_01`, `PMC8097002_01`, `PMC7687474_02`, `PMC8013978_01`, `PMC7269521_01`, `PMC7248319_01`–`03`)
- `"Confirmed acute COVID-19 infection with confirmatory PCR/antigen test."` (`PMC7481472_08`)

**Rule when `rationale` is a generic template:**
- Do **not** hallucinate "or NAAT/antigen testing" if `step9_key_evidence` only shows RT-PCR.
- Inspect `step9_key_evidence.evidence_items[].source_quote`, `test_name`, `specimen`, and `step5_concept_grounding` to extract the actual assay (e.g., RT-PCR vs. RT-PCR + quick antigen test) and specimen type (throat swab, nasopharyngeal swab, oronasopharyngeal swab).

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`42-year-old`, `81-year-old`, `preterm newborn born at 28 weeks 5 days`), sex (`male`, `female`), occupation (`healthcare worker`)
   - Specific country, city, or hospital (`Khorshid Hospital`)
   - Exact day/timeline in this patient (`"49 days after second dose"`, `"on day 4"`, `"DOL 19"`, `"day 10 negative test"`)
   - Exact viral load or Ct value in this patient (`"7x10^6 copies/ml"`)
   - Exact inflammatory lab values or drug doses for this patient
   - Specific Pango lineage/clade or vaccine brand name when used as patient-specific findings (`"variant B.1.525"`, `"BNT162b2"`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Standard clinical definitions (`"hypoxemia with SpO2 <94%"`, `"fever >38.0°C"`, `"ARDS PaO2/FiO2 ≤300 mmHg"`)
   - Standard assay gene targets (`"RT-PCR targeting E, N, RdRp, or S genes"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"7x10^6 copies/ml"` → `"high viral load demonstrating active viral replication"`
   - `"49 days after completing two doses of BNT162b2 mRNA vaccine"` → `"breakthrough infection in a fully vaccinated individual (after completing an mRNA vaccine series)"`
   - `"variant B.1.525"` → `"emerging SARS-CoV-2 variants"`

### 3.2 Generalize Clinical Presentation, Comorbidities & Complications
- Frame atypical presentations or complications mentioned in `rationale` as recognized clinical manifestations/associations of COVID-19:
  - *Respiratory/Imaging:* bilateral ground-glass opacities and crazy-paving pattern on chest CT are characteristic radiological features of COVID-19 pneumonia.
  - *Atypical/Extrapulmonary:* acute abdominal pain mimicking appendicitis with basal lung consolidations, secondary thrombotic thrombocytopenic purpura (TTP), neuromyelitis optica spectrum disorder (NMOSD), HELLP syndrome in pregnancy, or severe respiratory failure in myasthenia gravis.
  - *Treatment:* standard antiviral and anti-inflammatory therapy (e.g., remdesivir, corticosteroids such as dexamethasone) when mentioned in `rationale`.

---

## 4. Output Format & Worked Examples

### 4.1 Required JSON Schema
```json
{
  "ground_truth_reasoning": "<Disease Name> (<pathogen/clinical entity>). Reasoning: (1) <Claim 1>. (2) <Claim 2>. (3) <Claim 3>. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "<Claim 1>", "source": "rationale | step9"}
  ],
  "dropped_specifics": ["<dropped item 1>", "<dropped item 2>"]
}
```

### 4.2 Reference Example 1 — Breakthrough Infection with Antigen + RT-PCR & Follow-up Clearance (`PMC8342944_01::COVID-19`)

**INPUT (from `selected_case/output_covid_19.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Rapid antigen test and laryngopharyngeal swab RT-PCR (E and S genes)", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "SARS-CoV-2", specimen: "laryngopharyngeal swab"}`
  - `{test_name: "Follow-up RT-PCR", result: "NEGATIVE", strength: "E1_CONFIRMATORY", target_concept: "SARS-CoV-2 clearance", specimen: "laryngopharyngeal swab"}` ← **EXCLUDE** (`target_concept = clearance`)
- `rationale`:
  `"A 42-year-old male healthcare worker experienced a breakthrough SARS-CoV-2 infection (variant B.1.525) 49 days after completing two doses of the BNT162b2 mRNA vaccine. The infection was initially detected by a positive rapid antigen test (E2) and definitively confirmed by RT-PCR targeting E and S genes from a laryngopharyngeal swab (E1), demonstrating viral replication and transmission. Confirmatory testing during an active infection episode satisfies the Valid Positive Diagnosis criteria. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "COVID-19 (SARS-CoV-2 infection). Reasoning: (1) COVID-19 can present as a breakthrough infection in fully vaccinated individuals, particularly with emerging SARS-CoV-2 variants. (2) Definitive diagnosis requires molecular detection of SARS-CoV-2 RNA by RT-PCR (e.g., targeting E and S genes) from a respiratory specimen such as a laryngopharyngeal or nasopharyngeal swab. (3) Rapid antigen testing is a highly specific but less sensitive screening method that requires confirmation by RT-PCR. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "COVID-19 can present as a breakthrough infection in fully vaccinated individuals, particularly with emerging SARS-CoV-2 variants.", "source": "rationale"},
    {"text": "Definitive diagnosis requires molecular detection of SARS-CoV-2 RNA by RT-PCR (e.g., targeting E and S genes) from a respiratory specimen such as a laryngopharyngeal or nasopharyngeal swab.", "source": "step9"},
    {"text": "Rapid antigen testing is a highly specific but less sensitive screening method that requires confirmation by RT-PCR.", "source": "step9"}
  ],
  "dropped_specifics": ["42-year-old male", "healthcare worker", "49 days after second dose", "BNT162b2 brand name (kept general 'mRNA vaccine')", "variant B.1.525", "day 10 negative follow-up test (excluded: target_concept = clearance, not diagnosis)"]
}
```

### 4.3 Worked Example 2 — Severe COVID-19 Pneumonia with Chest CT (`E3`) & Repeat PCR (`E1`) (`PMC8012864_01::COVID-19`)

**INPUT (from `selected_case/output_covid_19.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "SARS-CoV-2 PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "SARS-CoV-2 RNA", specimen: "nasopharyngeal swab"}`
  - `{test_name: "Repeat SARS-CoV-2 PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "SARS-CoV-2 RNA", specimen: "nasopharyngeal swab"}`
  - `{test_name: "High-resolution chest CT", result: "POSITIVE", strength: "E3_SUPPORTIVE", target_concept: "COVID-19-associated pneumonia", specimen: null}`
- `rationale`:
  `"An 81-year-old female presented with fever, cough, dyspnea, and loss of consciousness. She had two positive PCR tests for COVID-19 (before and after hospital admission), providing E1 confirmatory lab evidence. High-resolution chest CT showed bilateral ground-glass and crazy paving opacities typical of COVID-19 pneumonia. Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "COVID-19 (SARS-CoV-2 infection). Reasoning: (1) Fever, cough, and dyspnea are characteristic respiratory symptoms of acute COVID-19, which can be complicated by neurological manifestations and secondary thrombotic thrombocytopenic purpura (TTP). (2) Definitive diagnosis requires molecular detection of SARS-CoV-2 RNA by PCR from a respiratory specimen such as a nasopharyngeal swab. (3) Diffuse bilateral ground-glass and crazy-paving opacities with peripheral distribution on high-resolution chest CT are supportive radiological features typical of COVID-19-associated pneumonia. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Fever, cough, and dyspnea are characteristic respiratory symptoms of acute COVID-19, which can be complicated by neurological manifestations and secondary thrombotic thrombocytopenic purpura (TTP).", "source": "rationale"},
    {"text": "Definitive diagnosis requires molecular detection of SARS-CoV-2 RNA by PCR from a respiratory specimen such as a nasopharyngeal swab.", "source": "step9"},
    {"text": "Diffuse bilateral ground-glass and crazy-paving opacities with peripheral distribution on high-resolution chest CT are supportive radiological features typical of COVID-19-associated pneumonia.", "source": "step9"}
  ],
  "dropped_specifics": ["81-year-old female", "Khorshid Hospital", "pre- and post-admission test timing", "[Figure 1]"]
}
```

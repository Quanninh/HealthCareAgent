---
name: gt-reasoning-chikungunya
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Chikungunya cases in selected_case/output_chikungunya.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate
  from rationale, normalizing POSITIVE keywords, and generalizing case-specific
  details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Chikungunya

## Target Disease & Data Scope
- **Target Disease:** `Chikungunya` (*Chikungunya virus [CHIKV] infection*)
- **Source File:** `selected_case/output_chikungunya.jsonl` (20 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-chikungunya/SKILL.md` (`03_evidence_specificity_matrix.md` §5.14)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_chikungunya.jsonl`

| Tier in `skills/disease-agent-chikungunya` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_chikungunya.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive molecular detection of Chikungunya virus (CHIKV) RNA by RT-PCR during the acute viremic phase (typically days 1–7 of illness), or viral isolation in cell culture | `Chikungunya RT-PCR`, `Serum chikungunya real-time RT-PCR`, `Real-time reverse transcription PCR for CHIKV`, `Real-time RT-PCR for CHIKV`, `Combined congenital arbovirus PCR`, `CHIKV-PCR and convalescent serology` | **Target:** `Chikungunya virus`<br>**Specimen:** `serum`, `blood`, `cell culture supernatant / serum` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly specific serological detection of anti-CHIKV IgM (or ≥4-fold paired IgM/IgG titer rise / seroconversion) by ELISA, MAC-ELISA, or IFA in serum or CSF (especially after the first week of illness when viremia has cleared), with exclusion of cross-reactive/co-circulating arboviruses (dengue, Zika) | `Chikungunya IgM serology`, `Chikungunya serology`, `Chikungunya serum IgM test`, `Chikungunya MAC-ELISA`, `Chikungunya EIA serology`, `Chikungunya IgM and IgG ELISA`, `CHIK IgM and IgG serology`, `CHIKV indirect immunofluorescence assay (IFA)`, `CSF and serum CHIKV IgM ELISA`, `CSF CHIKV IgM antibody test`, `Chikungunya IgM antibody assay`, `Neonatal chikungunya IgM antibody test` | **Target:** `Chikungunya virus`<br>**Specimen:** `serum`, `blood / serum`, `CSF`, `CSF and serum` |
| **E3 — Supportive (in `rationale`)** | Characteristic clinical triad of abrupt high-grade fever, severe debilitating polyarthralgia/polyarthritis, and maculopapular/vesiculobullous rash, plus travel/residence in an endemic/epidemic region | Mentioned in `rationale` and `source_quote` | Clinical syndrome, epidemiological exposure |

### 1.2 Special Diagnostic Timing & Compound Rules in `output_chikungunya.jsonl`
1. **Post-Viremic RT-PCR Negativity + IgM Positivity (`PMC5388347_01`, `PMC12399548_01`):**
   - Several cases note that RT-PCR was negative in the second or third week of illness (e.g., day 20 or during post-acute neurological complications like transverse myelitis) while CHIKV IgM/IgG serology was strongly positive.
   - **Rule:** State the general diagnostic principle (keeping the general 1-week viremic window rule): *"During the post-viremic phase (typically after the first 5–7 days of illness), molecular testing (RT-PCR) may be negative while CHIKV-specific IgM/IgG serology in serum or CSF establishes the diagnosis."*
2. **Compound `CHIKV-PCR and convalescent serology` (`PMC5376920_01`):**
   - Inspect `source_quote` and `rationale`: if acute PCR was positive or convalescent IgM/polyvalent antibody titer rose significantly, separate the acute molecular detection role from the convalescent seroconversion (≥4-fold antibody titer rise) role.
3. **Differential Exclusion of Co-circulating Arboviruses:**
   - When `rationale` notes negative testing for Dengue, Zika, Mayaro, Yellow Fever, or Malaria, generalize this as: *"Exclusion of clinically overlapping arboviral and tropical infections (such as dengue and Zika) strengthens the serological diagnosis of chikungunya."*

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
All 20 rows in `output_chikungunya.jsonl` contain explicit `E1` or `E2` markers in `rationale`. Replace them as follows:
- `(E1)` / `(E1 confirmatory)` / `(E1 confirmatory evidence)` → **`definitive molecular laboratory confirmation`**
- `(E2)` / `(E2 evidence)` / `(E2 highly specific evidence)` / `(E2 intrathecal evidence of neuro-chikungunya)` → **`highly specific serological (or intrathecal antibody) evidence`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Remove all trailing annotation protocol sentences from `rationale`:
- `Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS.`
- `Primary diagnosis confirmed.` / `Single patient anchor (neonate), current episode, primary diagnosis confirmed.`
- `VPD satisfied -> POSITIVE.` / `Primary diagnosis confirmed, VPD satisfied -> POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords
- Convert `result: "POSITIVE"` or `result: "DETECTED"` in `step9_key_evidence` into generalized diagnostic statements.
- Replace trailing `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`56-year-old`, `27-year-old`, `31-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution (`Costa Rica`)
   - Exact illness/hospitalization day in this patient (`"on day 16"`, `"on day 20"`)
   - Exact titer in this patient (`"1:100"`, `"1:10,000"`, `"1:<10 to 1:160"`)
   - Exact lab value or drug dose for this patient
   - Specific strain designations when used as patient-specific findings

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Diagnostic window rules (`"acute viremic phase during the first 5–7 days of illness"`)
   - Seroconversion rules (`"≥4-fold rise in antibody titer between acute and convalescent sera is diagnostic"`)
   - Clinical definitions (`"fever >38.5°C"`, `"thrombocytopenia <150,000/µL"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"IgM 1:100 and IgG 1:10,000"` → `"positive at a high/significant antibody titer"`
   - `"titer rose from 1:<10 to 1:160"` → `"demonstrated seroconversion (≥4-fold antibody titer rise) in paired sera"`
   - `"day 20 negative RT-PCR"` → `"negative RT-PCR during the post-viremic phase (after the first week of illness)"`

### 3.2 Generalize Atypical & Severe Manifestations
- Chikungunya cases in `output_chikungunya.jsonl` frequently feature severe or atypical complications: neuro-chikungunya (longitudinally extensive transverse myelitis, encephalitis, Guillain-Barré syndrome, optic neuritis), vesiculobullous/hemorrhagic dermatosis, deep vein thrombosis, myocarditis, maternal-fetal (congenital/neonatal) transmission, or secondary opportunistic infections from transient CD4 lymphopenia. Frame these as recognized severe or atypical complications of chikungunya fever.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Post-Viremic Chikungunya Confirmed by IFA Serology (`E2`) (`PMC5388347_01::Chikungunya`)

**INPUT (from `selected_case/output_chikungunya.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "CHIKV indirect immunofluorescence assay (IFA)", result: "POSITIVE", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Chikungunya virus", specimen: "serum", source_quote: "CHIKV IgM and IgG antibodies were detected with titre 1:100 and 1:10,000, respectively (Figure 2)."}`
- `rationale`:
  `"A 27-year-old female returning from Costa Rica developed acute fever, rash, and persistent polyarthralgias. Serology on day 20 revealed high-titer CHIKV IgM (1:100) and IgG (1:10,000) by IFA (E2 evidence) with exclusion of cross-reactivity against Zika, dengue, West Nile, Usutu, and yellow fever. RT-PCR negativity at day 20 reflects expected post-viremic timing. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Chikungunya (Chikungunya virus [CHIKV] infection). Reasoning: (1) Acute fever, rash, and persistent debilitating polyarthralgia after travel to an endemic region are classic clinical features of chikungunya fever. (2) Detection of CHIKV-specific IgM and IgG antibodies at significant/high titers by indirect immunofluorescence assay (IFA) provides highly specific serological evidence of infection, particularly when cross-reactive arboviruses (such as dengue, Zika, and yellow fever) are excluded. (3) Molecular testing (RT-PCR) is typically negative after the acute viremic window (the first 5–7 days of illness), making serology the primary diagnostic modality in the post-viremic phase. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Acute fever, rash, and persistent debilitating polyarthralgia after travel to an endemic region are classic clinical features of chikungunya fever.", "source": "rationale"},
    {"text": "Detection of CHIKV-specific IgM and IgG antibodies at significant/high titers by indirect immunofluorescence assay (IFA) provides highly specific serological evidence of infection, particularly when cross-reactive arboviruses (such as dengue, Zika, and yellow fever) are excluded.", "source": "step9"},
    {"text": "Molecular testing (RT-PCR) is typically negative after the acute viremic window (the first 5–7 days of illness), making serology the primary diagnostic modality in the post-viremic phase.", "source": "rationale"}
  ],
  "dropped_specifics": ["27-year-old female", "Costa Rica", "exact day 20 sampling day (converted to post-viremic phase after first week)", "exact patient titers IgM 1:100 and IgG 1:10,000 (converted to significant/high titers)", "Figure 2 reference"]
}
```

### 4.2 Worked Example 2 — Neuro-Chikungunya with Intrathecal CSF IgM (`E2`) (`PMC12399548_01::Chikungunya`)

**INPUT (from `selected_case/output_chikungunya.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "CSF CHIKV IgM antibody test", result: "DETECTED", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Chikungunya virus", specimen: "CSF", source_quote: "Antibodies to CHIKV IgM were detected in the CSF by enzyme-linked immunosorbent assay (ELISA)."}`
- `rationale`:
  `"A 31-year-old female with SLE developed acute ascending tetraparesis, fever, arthritis, and longitudinally extensive transverse myelitis. CSF analysis revealed detected CHIKV IgM antibodies (E2 intrathecal evidence of neuro-chikungunya) with dengue and Zika ruled out. Negative CSF RT-PCR resolved as expected given post-acute myelitic presentation. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Chikungunya (Neuro-chikungunya with longitudinally extensive transverse myelitis). Reasoning: (1) Chikungunya virus infection typically presents with fever and arthritis and can be complicated by severe neurological manifestations such as longitudinally extensive transverse myelitis (LETM) with acute tetraparesis. (2) Detection of CHIKV-specific IgM antibodies in cerebrospinal fluid (CSF) by ELISA provides highly specific intrathecal serological evidence of central nervous system chikungunya infection, particularly when co-circulating arboviruses (dengue and Zika) are excluded. (3) Negative CSF RT-PCR does not exclude neuro-chikungunya when sampling occurs during the post-acute parainfectious myelitic phase. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Chikungunya virus infection typically presents with fever and arthritis and can be complicated by severe neurological manifestations such as longitudinally extensive transverse myelitis (LETM) with acute tetraparesis.", "source": "rationale"},
    {"text": "Detection of CHIKV-specific IgM antibodies in cerebrospinal fluid (CSF) by ELISA provides highly specific intrathecal serological evidence of central nervous system chikungunya infection, particularly when co-circulating arboviruses (dengue and Zika) are excluded.", "source": "step9"},
    {"text": "Negative CSF RT-PCR does not exclude neuro-chikungunya when sampling occurs during the post-acute parainfectious myelitic phase.", "source": "rationale"}
  ],
  "dropped_specifics": ["31-year-old female", "SLE comorbidity"]
}
```

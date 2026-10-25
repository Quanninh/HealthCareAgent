---
name: gt-reasoning-ebola_filovirus
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Ebola / Filovirus cases in selected_case/output_ebola_filovirus.jsonl by
  decoding E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema
  boilerplate from rationale, normalizing POSITIVE keywords, and generalizing
  case-specific details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Ebola / Filovirus Disease

## Target Disease & Data Scope
- **Target Disease:** `Ebola_Filovirus` (*Ebola virus disease [EVD] caused by Zaire ebolavirus [EBOV] or related filoviruses*)
- **Source File:** `selected_case/output_ebola_filovirus.jsonl` (3 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-ebola_filovirus/SKILL.md` (`03_evidence_specificity_matrix.md` §5.10)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_ebola_filovirus.jsonl`

| Tier in `skills/disease-agent-ebola_filovirus` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_ebola_filovirus.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive reference-laboratory confirmation of orthoebolavirus/filovirus infection via RT-PCR amplification of viral RNA, viral gene sequencing (e.g., L-gene Sanger sequencing), antigen-capture ELISA, or viral isolation in appropriate specimens (blood/plasma, CSF, or urine) | `Blood EBOV RT-PCR`, `CSF EBOV RT-PCR (Trombley assay)`, `Filovirus RT-PCR`, `L-gene Sanger sequencing and phylogenetic analysis`, `Zaire Ebola virus diagnostic testing` | **Target:** `Zaire ebolavirus`, `Ebola virus (EBOV)`, `Filovirus / Ebola virus`, `Zaire ebolavirus (KM251803.1)`<br>**Specimen:** `blood`, `plasma`, `cerebrospinal fluid`, `blood and urine` |
| **E2 — Strong / Highly Specific** | Validated antigen detection or phase-appropriate IgM/IgG serology within a reference diagnostic framework | (None standalone in the 3 selected cases; all 3 cases have E1 molecular confirmation) | **Target:** `Ebola virus` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Acute febrile gastrointestinal/hemorrhagic syndrome (high fever, sore throat, vomiting, diarrhea, hematuria), epidemiological travel/exposure in an active West/Central African outbreak zone, or late-onset neurological/viral persistence complications | `Clinical presentation of acute febrile illness` (`result: "FEVER_VOMITING_DIARRHEA"`) | **Target:** `Ebola virus disease` |

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E3`) in `rationale`
All 3 rows in `output_ebola_filovirus.jsonl` contain explicit `E1` markers in `rationale`. Replace them as follows:
- `(E1 confirmatory evidence)` → **`(definitive laboratory confirmation)`**
- `E1 confirmatory laboratory evidence is present for the primary human patient in the current active episode.` → **Strip completely** (already covered by the decoded RT-PCR claim)
- `Confirmatory E1 molecular laboratory evidence is documented in the current active episode for the primary human patient.` → **Strip completely**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Remove all trailing schema/protocol sentences from `rationale`:
- `The assertion is CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS.`
- `VPD criteria are fully satisfied -> POSITIVE.`
- `VPD satisfied -> POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords & Special `result` Values
- Convert `result: "POSITIVE"`, `"FEVER_VOMITING_DIARRHEA"`, and `"ZAIRE_EBOLAVIRUS_CONFIRMED"` in `step9_key_evidence` into generalized medical and diagnostic statements.
- Replace trailing `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`21-year-old`, `30-year-old`, `40-year-old`), sex (`male`, `female`)
   - Specific country, city, or reference laboratory (`Guinea to Senegal`, `Sierra Leone`, `Liberian traveler in Lagos, Nigeria`, `Dakar Pasteur Institute`, `Public Health England`)
   - Exact day of illness in this patient (`"on day 8 of illness"`)
   - Exact cycle threshold (Ct) in this patient (`"Ct 23.5"`, `"Ct 37.6"`) and amplicon size (`"300 bp"`)
   - Exact supportive fluid volumes and drug doses for this patient (`"ceftriaxone 2 g"`, `"artesunate 180 mg"`, `"Ringer's lactate 4-6 L"`)
   - Patient-specific GenBank accession numbers and isolate IDs (`"KM251803.1"`, `"EBOV/Hsap/NGA/2014/LIB-NIG 01072014"`), while **keeping** the species designation (*Zaire ebolavirus*)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Standard clinical definitions (`"fever >38.0°C"`) or general assay cutoffs if stated as a general rule

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"plasma Ct 23.5"` → `"positive plasma RT-PCR with high viral load (low cycle threshold) during acute viremia"`
   - `"CSF Ct 37.6"` → `"positive CSF RT-PCR confirming central nervous system viral invasion/persistence"`
   - `"Ringer's lactate 4-6 L"` → `"aggressive intravenous fluid and electrolyte resuscitation"`

### 3.2 Preserve Viral Persistence & Complication Concepts
- In `PMC4696703_01`, the patient developed late-onset encephalopathy/meningoencephalitis with EBOV RNA detected in CSF and intermittent viral shedding in urine after plasma viremia improved. Generalize this into a clinical principle: *"Ebola virus can persist in immunologically privileged sites such as the central nervous system (causing late-onset meningoencephalitis with CSF RT-PCR positivity) and be shed intermittently in urine during convalescence."*

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Ebola Virus Disease with Late-Onset Encephalopathy & CSF/Plasma RT-PCR (`E1`) (`PMC4696703_01::Ebola_Filovirus`)

**INPUT (from `selected_case/output_ebola_filovirus.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Blood EBOV RT-PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Ebola virus (EBOV)", specimen: "blood", source_quote: "On day 8 of illness, after testing EBOV PCR-positive (cycle threshold [Ct] value of 23.5)..."}`
  - `{test_name: "CSF EBOV RT-PCR (Trombley assay)", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Ebola virus (EBOV)", specimen: "cerebrospinal fluid", source_quote: "cerebrospinal fluid (CSF) was EBOV PCR-positive (Ct value 37.6)..."}`
- `rationale`:
  `"A 30-year-old female in Sierra Leone was diagnosed with acute Ebola virus disease confirmed by plasma RT-PCR (Ct 23.5). Following initial improvement, she developed late-onset encephalopathy with EBOV PCR positivity in cerebrospinal fluid (Ct 37.6) and subsequent intermittent PCR positivity in urine. E1 confirmatory laboratory evidence is present for the primary human patient in the current active episode. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Ebola virus disease (Zaire ebolavirus [EBOV] infection). Reasoning: (1) Definitive diagnosis of acute Ebola virus disease requires molecular detection of Ebola virus RNA by RT-PCR in blood or plasma during acute viremia. (2) Ebola virus can invade and persist in immunologically privileged sites such as the central nervous system, causing late-onset encephalopathy/encephalitis confirmed by detection of EBOV RNA in cerebrospinal fluid (CSF) by RT-PCR, as well as intermittent viral RNA shedding in urine during recovery. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Definitive diagnosis of acute Ebola virus disease requires molecular detection of Ebola virus RNA by RT-PCR in blood or plasma during acute viremia.", "source": "step9"},
    {"text": "Ebola virus can invade and persist in immunologically privileged sites such as the central nervous system, causing late-onset encephalopathy/encephalitis confirmed by detection of EBOV RNA in cerebrospinal fluid (CSF) by RT-PCR, as well as intermittent viral RNA shedding in urine during recovery.", "source": "rationale"}
  ],
  "dropped_specifics": ["30-year-old female", "Sierra Leone", "day 8 of illness", "exact patient Ct values: plasma Ct 23.5 and CSF Ct 37.6 (kept clinical interpretation of acute viremia and CNS persistence)", "Public Health England Trombley assay specifics", "empiric ceftriaxone, artesunate, and Ringer's lactate doses"]
}
```

### 4.2 Worked Example 2 — Ebola Virus Disease Confirmed by Filovirus RT-PCR & L-Gene Sequencing (`E1`) (`PMC5436409_01::Ebola_Filovirus`)

**INPUT (from `selected_case/output_ebola_filovirus.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Filovirus RT-PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Filovirus / Ebola virus", specimen: "blood and urine"}`
  - `{test_name: "L-gene Sanger sequencing and phylogenetic analysis", result: "ZAIRE_EBOLAVIRUS_CONFIRMED", strength: "E1_CONFIRMATORY", target_concept: "Zaire ebolavirus (KM251803.1)", specimen: "blood"}`
- `rationale`:
  `"A 40-year-old Liberian male traveler arrived in Lagos, Nigeria and presented with high fever, sore throat, vomiting, diarrhea, and hematuria. RT-PCR on blood and urine specimens amplified the expected 300 bp filovirus product, and Sanger sequencing of the L-gene confirmed Zaire ebolavirus (GenBank KM251803.1). Confirmatory E1 molecular laboratory evidence is documented in the current active episode for the primary human patient. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Ebola virus disease (Zaire ebolavirus infection). Reasoning: (1) Ebola virus disease typically presents after exposure in an outbreak region with acute high fever, sore throat, gastrointestinal symptoms (vomiting and diarrhea), and hemorrhagic manifestations such as hematuria. (2) Definitive diagnosis requires molecular detection of filovirus RNA by RT-PCR from blood or urine specimens. (3) Sanger sequencing and phylogenetic analysis of the viral RNA-dependent RNA polymerase (L) gene provide definitive species-level identification of Zaire ebolavirus. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Ebola virus disease typically presents after exposure in an outbreak region with acute high fever, sore throat, gastrointestinal symptoms (vomiting and diarrhea), and hemorrhagic manifestations such as hematuria.", "source": "rationale"},
    {"text": "Definitive diagnosis requires molecular detection of filovirus RNA by RT-PCR from blood or urine specimens.", "source": "step9"},
    {"text": "Sanger sequencing and phylogenetic analysis of the viral RNA-dependent RNA polymerase (L) gene provide definitive species-level identification of Zaire ebolavirus.", "source": "step9"}
  ],
  "dropped_specifics": ["40-year-old Liberian male", "travel to Lagos, Nigeria", "300 bp amplicon size", "patient-specific GenBank accession KM251803.1 and strain ID EBOV/Hsap/NGA/2014/LIB-NIG 01072014 (kept species Zaire ebolavirus)"]
}
```

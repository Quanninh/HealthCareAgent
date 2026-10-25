---
name: gt-reasoning-dengue
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Dengue cases in selected_case/output_dengue.jsonl by decoding E1/E2/E3
  evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate from
  rationale, normalizing POSITIVE keywords, and generalizing case-specific details
  for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Dengue

## Target Disease & Data Scope
- **Target Disease:** `Dengue` (*Dengue virus [DENV-1, DENV-2, DENV-3, DENV-4] infection, including Dengue Fever, Dengue Hemorrhagic Fever [DHF], Dengue Shock Syndrome [DSS], and Expanded Dengue Syndrome*)
- **Source File:** `selected_case/output_dengue.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-dengue/SKILL.md` (`03_evidence_specificity_matrix.md` §5.5)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_dengue.jsonl`

| Tier in `skills/disease-agent-dengue` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_dengue.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive acute-phase laboratory confirmation by detection of dengue viral RNA via NAAT/RT-PCR (with optional serotype identification DENV-1–4) or detection of dengue NS1 viral antigen by ELISA/immunochromatographic assay during the early febrile phase (days 1–7 of illness) | **NS1 Antigen:** `Dengue NS1 antigen test`, `Dengue NS1 ELISA`, `Dengue NS1 antigen assay`, `Dengue NS1 antigen`, `Dengue NS1 antigen ELISA`, `Dengue NS-1 antigen assay`<br>**Molecular (RT-PCR):** `Light Cycler RT-PCR`, `Real-time RNA PCR panel`, `DENV serotyping RT-PCR`, `Multiplex quantitative RT-PCR (qRT-PCR)`, `Dengue RT-PCR`<br>**Compound NS1 + Serology:** `Dengue NS1 antigen and IgM serology`, `Dengue NS1 antigen and IgM antibody`, `Dengue NS1 and IgM/IgG test` | **Target:** `Dengue virus`, `Dengue virus NS1 antigen`, `Dengue virus RNA`, `Dengue virus serotype 1 RNA`, `Dengue virus serotype 2 (DENV2)`<br>**Specimen:** `serum`, `blood`, `blood / serum`, `CSF and serum` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly specific serological evidence of acute/recent dengue infection via anti-DENV IgM detection (ELISA, MAC-ELISA, rapid immunochromatographic test) or paired IgM/IgG seroconversion, especially after day 5 of illness when NS1/viremia may decline; requires clinical correlation due to potential flavivirus cross-reactivity | `Dengue IgM ELISA`, `Dengue IgM serology`, `Dengue IgM and IgG serology`, `Dengue IgM chromatographic immunoassay`, `Anti-DENV-1 IgM ELISA`, `Dengue ELISA-IgM`, `Anti-DENV IgM and IgG ELISA`, `Dengue IgM antibody assay`, `Dengue serology (IgM/IgG) and NS1 antigen` (`result: "POSITIVE_IGM_IGG_NEGATIVE_NS1"`), `Clinical diagnosis of dengue hemorrhagic fever`, `Clinical and neuroimaging diagnosis of dengue meningoencephalitis (cohort inclusion criteria: dengue IgM positivity)` | **Target:** `Dengue virus`, `Dengue virus IgM`, `Dengue virus IgM and IgG`, `Dengue virus antibodies`, `Dengue virus serotype 1 IgM`<br>**Specimen:** `serum`, `blood`, `CSF` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Supportive clinical, hematologic, or imaging findings (acute febrile illness with myalgia/retro-orbital headache/rash, thrombocytopenia `<100,000–150,000/µL`, leukopenia, hemoconcentration with `≥20%` hematocrit rise, plasma leakage [ascites, pleural effusion, gallbladder wall thickening], or exclusion of malaria/typhoid) | `Complete blood count`, `Complete blood count and hemoconcentration`, `Hematocrit and abdominal ultrasound`, `Ophthalmologic fundoscopy and OCT examination`, `Clinical presentation of severe dengue shock`, `Clinical diagnosis of severe dengue with coagulopathy`, `Clinical management of dengue haemorrhagic fever`, `Malaria and typhoid serological tests` (`result: "NEGATIVE"`) | **Target:** `Dengue thrombocytopenia`, `Severe dengue`, `Dengue haemorrhagic fever`, `Dengue fever-associated maculopathy and panuveitis`, `Plasmodium / Salmonella Typhi` |
| **DISCORDANT — Negative Screening / Post-Acute NS1 (`E0_CONTRADICTED` / `NEGATIVE_NS1`)** | Negative NS1 antigen in the late febrile/defervescence phase when IgM/IgG is positive, or negative initial rapid test superseded by confirmatory testing. Generalize as: *"A negative NS1 antigen or rapid screening test later in the illness course does not exclude dengue when DENV-specific IgM/IgG serology or RT-PCR is positive."* | `Dengue serology (IgM/IgG) and NS1 antigen` (`result: "POSITIVE_IGM_IGG_NEGATIVE_NS1"`, `PMC9767721_01`), `Panbio Dengue immunochromatography assay` (`result: "NEGATIVE"`, `strength: "E0_CONTRADICTED"`, `PMC10750506_01`) | **Target:** `Dengue virus` |

### 1.2 Compound `test_name` Splitting Rule
In `output_dengue.jsonl`, many records combine **Dengue NS1 antigen (E1)** and **Dengue IgM/IgG serology (E2)** into a single `evidence_item` (e.g., `test_name: "Dengue NS1 antigen and IgM serology"` or `"Dengue NS1 antigen and IgM antibody"`):
- **Rule:** Unpack into **two distinct claims**:
  1. **E1 Claim:** Detection of dengue viral NS1 antigen (or viral RNA by RT-PCR) in serum/blood during the acute febrile phase (days 1–7) provides definitive laboratory confirmation of acute dengue infection.
  2. **E2 Claim:** Detection of anti-dengue IgM antibodies (or IgG seroconversion) by ELISA/immunoassay provides highly specific serological confirmation of acute or recent infection.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
In `output_dengue.jsonl`, 89/100 rows contain explicit tier markers in `rationale`. Replace them as follows:
- `(E1 confirmatory evidence)` / `(E1_CONFIRMATORY_LAB)` / `(E1)` → **`definitive acute laboratory confirmation`**
- `(E2 highly specific evidence)` / `(E2_HIGHLY_SPECIFIC_CLINICAL)` / `(E2 evidence)` / `(E2)` → **`highly specific serological (or clinical) evidence`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Remove all trailing schema/protocol sentences from `rationale`:
- `Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS.` (62 rows)
- `Single patient, current episode, primary diagnosis confirmed.` / `Single patient, acute episode, primary diagnosis confirmed.` / `Single patient, active current episode, primary diagnosis confirmed.` / `Single patient, acute infection, co-primary diagnosis confirmed.`
- `VPD satisfied -> POSITIVE.` / `VPD criteria -> POSITIVE.` / `VPD criteria satisfied -> POSITIVE.` / `VPD criteria are satisfied -> POSITIVE.` / `VPD criteria are met -> POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords & Special `result` Values
- Convert `result: "POSITIVE"`, `"DETECTED"`, `"REACTIVE"`, `"CONFIRMED"`, and `"POSITIVE_IGM_IGG_NEGATIVE_NS1"` into generalized diagnostic claims.
- Replace trailing `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`41-year-old`, `34-year-old`, `7-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution (`Cambodia and Thailand`)
   - Exact hospitalization or illness day in this patient (`"on day 3"`, `"day 2 and day 6"`)
   - Exact lab value in this patient (`"AST 5162 U/L, ALT 3964 U/L"`, `"platelets 14,000/µL"`)
   - Commercial assay brand names (`Light Cycler (Roche Diagnostics)`, `Panbio`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Standard dengue serotypes (`DENV-1`, `DENV-2`, `DENV-3`, `DENV-4` — these are canonical viral serotypes, not patient-specific strain codes)
   - Diagnostic window rules (`"early febrile phase (days 1–7 of illness) for NS1 antigen/RT-PCR"`, `"IgM seroconversion typically after day 5 of illness"`)
   - Clinical definitions (`"thrombocytopenia <100,000/µL or <150,000/µL"`, `"hemoconcentration defined as ≥20% rise in hematocrit"`, `"severe transaminitis ≥1000 U/L in severe dengue"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"AST 5162 U/L, ALT 3964 U/L"` → `"markedly elevated transaminases (severe acute transaminitis/hepatitis) indicating hepatic involvement"`
   - `"platelets 14,000/µL"` → `"severe thrombocytopenia"`
   - `"positive Dengue NS1 antigen on day 3"` → `"positive Dengue NS1 antigen during the early febrile phase (days 1–7)"`

### 3.2 Specify Clinical Severity & Expanded Dengue Manifestations
- **Classic features:** Acute high-grade fever, myalgia, arthralgia, retro-orbital headache, maculopapular rash, leukopenia, and thrombocytopenia.
- **Severe / DHF / DSS:** Plasma leakage (hemoconcentration, pleural effusion, ascites, gallbladder wall edema), hemorrhagic manifestations (petechiae, epistaxis, gastrointestinal bleeding, subarachnoid hemorrhage), and hypovolemic shock.
- **Expanded Dengue Syndrome (organ-specific complications):** Severe hepatitis/transaminitis, myocarditis, meningoencephalitis, Guillain-Barré syndrome, maculopathy/panuveitis, hemophagocytic lymphohistiocytosis (HLH), acute kidney injury, or coinfections.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Dengue with NS1 Antigen (`E1`) & Expanded Dengue Syndrome (`PMC8572612_01::Dengue`)

**INPUT (from `selected_case/output_dengue.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Dengue NS1 antigen test", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Dengue virus", specimen: "serum", source_quote: "She was diagnosed as DF with a positive Dengue NS 1 antigen test on day 3."}`
- `rationale`:
  `"A 41-year-old female presented with acute fever, myalgia, and headache, diagnosed with dengue fever via a positive Dengue NS1 antigen test on day 3 (E1 confirmatory evidence). The disease progressed into expanded dengue syndrome with severe plasma leakage, subarachnoid hemorrhage, dengue myocarditis, hemophagocytic lymphohistiocytosis (HLH), and cranial diabetes insipidus. Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Dengue fever / Expanded dengue syndrome (Dengue virus infection). Reasoning: (1) Acute fever, myalgia, and headache are classic febrile-phase clinical features of dengue virus infection. (2) Detection of dengue NS1 viral antigen in serum during the early febrile phase (days 1–7 of illness) provides definitive laboratory confirmation of acute dengue infection. (3) Severe dengue can progress to plasma leakage and expanded dengue syndrome involving life-threatening multiorgan complications, including myocarditis, intracranial/subarachnoid hemorrhage, secondary hemophagocytic lymphohistiocytosis (HLH), and central endocrine dysfunction. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Acute fever, myalgia, and headache are classic febrile-phase clinical features of dengue virus infection.", "source": "rationale"},
    {"text": "Detection of dengue NS1 viral antigen in serum during the early febrile phase (days 1–7 of illness) provides definitive laboratory confirmation of acute dengue infection.", "source": "step9"},
    {"text": "Severe dengue can progress to plasma leakage and expanded dengue syndrome involving life-threatening multiorgan complications, including myocarditis, intracranial/subarachnoid hemorrhage, secondary hemophagocytic lymphohistiocytosis (HLH), and central endocrine dysfunction.", "source": "rationale"}
  ],
  "dropped_specifics": ["41-year-old female", "patient-specific day 3 of illness (converted to general early febrile phase days 1–7)"]
}
```

### 4.2 Worked Example 2 — Dengue Encephalitis with CSF/Serum RT-PCR (`E1`) & IgM/IgG Seroconversion (`E2`) (`PMC8312185_01::Dengue`)

**INPUT (from `selected_case/output_dengue.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "DENV serotyping RT-PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Dengue virus serotype 1 RNA", specimen: "CSF and serum"}`
  - `{test_name: "Anti-DENV IgM and IgG ELISA", result: "POSITIVE", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Dengue virus", specimen: "serum"}`
- `rationale`:
  `"A 7-year-old boy presented with acute encephalopathy, fever, coffee ground vomiting, leukopenia, and thrombocytopenia. Molecular testing confirmed DENV serotype 1 RNA in both CSF and serum by RT-PCR (E1 confirmatory evidence), with subsequent sequencing and positive anti-DENV IgM/IgG seroconversion (E2 evidence). Classical neurotropic pathogens (JEV, CHIK, HSV) tested negative. Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Dengue encephalitis (Dengue virus serotype 1 [DENV-1] infection). Reasoning: (1) Fever, leukopenia, thrombocytopenia, gastrointestinal mucosal bleeding, and acute encephalopathy are characteristic features of severe dengue with central nervous system involvement (dengue encephalitis). (2) Molecular detection of dengue viral RNA (e.g., DENV-1) by RT-PCR in cerebrospinal fluid (CSF) and serum provides definitive laboratory confirmation of acute neuroinvasive dengue infection. (3) Detection of anti-dengue IgM antibodies and subsequent IgG seroconversion by ELISA in paired serum samples provides highly specific serological confirmation, strengthened by the exclusion of other neurotropic viruses (such as Japanese encephalitis virus, chikungunya, and HSV). -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Fever, leukopenia, thrombocytopenia, gastrointestinal mucosal bleeding, and acute encephalopathy are characteristic features of severe dengue with central nervous system involvement (dengue encephalitis).", "source": "rationale"},
    {"text": "Molecular detection of dengue viral RNA (e.g., DENV-1) by RT-PCR in cerebrospinal fluid (CSF) and serum provides definitive laboratory confirmation of acute neuroinvasive dengue infection.", "source": "step9"},
    {"text": "Detection of anti-dengue IgM antibodies and subsequent IgG seroconversion by ELISA in paired serum samples provides highly specific serological confirmation, strengthened by the exclusion of other neurotropic viruses (such as Japanese encephalitis virus, chikungunya, and HSV).", "source": "step9"}
  ],
  "dropped_specifics": ["7-year-old boy", "admission day, day 2, and day 6 hospitalization sampling timeline"]
}
```

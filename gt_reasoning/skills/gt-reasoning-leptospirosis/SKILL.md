---
name: gt-reasoning-leptospirosis
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Leptospirosis cases in selected_case/output_leptospirosis.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate
  from rationale, normalizing POSITIVE keywords, and generalizing case-specific
  details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Leptospirosis

## Target Disease & Data Scope
- **Target Disease:** `Leptospirosis` (*Leptospira interrogans*, *Leptospira borgpetersenii*, *Leptospira kirschneri*, *Leptospira fainei*, or *Leptospira* spp. infection, including Weil's disease and Leptospiral Pulmonary Hemorrhage Syndrome [LPHS])
- **Source File:** `selected_case/output_leptospirosis.jsonl` (49 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-leptospirosis/SKILL.md` (`03_evidence_specificity_matrix.md` §5.8)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_leptospirosis.jsonl`

| Tier in `skills/disease-agent-leptospirosis` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_leptospirosis.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive confirmation via molecular detection of *Leptospira* DNA (PCR, 16S rRNA / *lipL32* real-time PCR, or metagenomic next-generation sequencing [mNGS]) in blood, BAL, CSF, or urine; reference Microscopic Agglutination Test (MAT) demonstrating seroconversion, `≥4-fold` titer rise in paired sera, or a significant confirmatory single titer (`≥1:400` or `≥1:800` depending on endemicity) against pathogenic serovars; culture isolation; or tissue immunohistochemistry (IHC) | **Molecular (PCR / mNGS):** `Metagenomic next-generation sequencing (mNGS)`, `Next generation sequencing (NGS)`, `Urine PCR for leptospiral DNA`, `PCR and Microscopic agglutination test (MAT)`, `dual-target real-time 16SrRNA/Lipl32 PCR and Panbio IgM ELISA`, `Real-time PCR`<br>**Reference Serology (MAT):** `Microscopic agglutination test (MAT)`, `Microagglutination test (MAT)`, `Leptospira IgM and Microscopic agglutination test (MAT)`<br>**Tissue IHC / Culture:** `Immunohistochemical assay for leptospira`, `Blood/urine culture` | **Target:** `Leptospira interrogans`, `Leptospira borgpetersenii`, `Leptospira icterohaemorrhagiae`, `Leptospira interrogans serovar Mankarso`, `Leptospira interrogans serovar Bratislava`, `Leptospira interrogans serovar Bataviae`, `Leptospira`<br>**Specimen:** `blood`, `serum`, `urine`, `bronchoalveolar lavage fluid`, `cerebrospinal fluid`, `autopsy tissue` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly specific serological evidence (anti-*Leptospira* IgM/IgG ELISA, Indirect Hemagglutination Assay [IHA], single-sample or *Leptospira biflexa* Patoc-strain screening MAT, or dark-field microscopy of CSF/body fluid) supporting acute leptospirosis in a compatible clinical and epidemiological setting | `Indirect hemagglutination assay (IHA)`, `Indirect hemagglutination (IHA)`, `anti-Leptospira IgM and IgG serology`, `Leptospira IgM antibody`, `ELISA for Leptospira IgM antibodies`, `Serum IgM-ELISA`, `Leptospirosis serology panel`, `Serology for Leptospira icterohaemorrhagiae`, `Martin and Pettit's (MAT) serology` (Patoc strain), `Microscopic agglutination test (MAT)` (single-titer E2), `Dark-field microscopy of cerebrospinal fluid` | **Target:** `Leptospira`, `Leptospira interrogans`, `Leptospira icterohaemorrhagiae`, `Leptospira serogroups Bataviae and Canicola`, `Leptospira biflexa (Patoc strain)`, `Leptospira fainei spirochetes`<br>**Specimen:** `serum`, `blood`, `cerebrospinal fluid` |
| **E3 — Supportive (in `rationale`)** | Classic clinical syndrome (abrupt fever, severe myalgia especially of the calves/gastrocnemius, headache, conjunctival suffusion, thrombocytopenia), severe icteric/Weil's disease triad (jaundice/hyperbilirubinemia, acute kidney injury, hemorrhage) or pulmonary hemorrhage/ARDS, environmental exposure (rat urine, floodwater, river water, farming/sewage), and response to penicillin/ceftriaxone/doxycycline | Mentioned in `rationale` and `source_quote` | Clinical syndrome, zoonotic/water exposure, antibiotic response |

### 1.2 Compound `test_name` Splitting Rule
In `output_leptospirosis.jsonl`, several records combine an **acute molecular test (PCR)** with **serology (MAT or IgM ELISA)**, or combine **IgM ELISA screening (E2)** with **reference MAT confirmation (E1)**:
- `test_name: "PCR and Microscopic agglutination test (MAT)"` (`PMC5928731_02`, `PMC5928731_03`)
- `test_name: "dual-target real-time 16SrRNA/Lipl32 PCR and Panbio IgM ELISA"` (`PMC6831015_01`)
- `test_name: "Leptospira IgM and Microscopic agglutination test (MAT)"` (`PMC8896608_01`)

**Rule:** Unpack compound diagnostic evidence into distinct claims:
1. **Acute Molecular Detection:** Detection of *Leptospira* DNA by PCR (e.g., targeting 16S rRNA or *lipL32*) or metagenomic next-generation sequencing (mNGS) in blood, BAL fluid, CSF, or urine provides definitive confirmation during the acute bacteremic/leptospiruric phase.
2. **Serological Confirmation:** The Microscopic Agglutination Test (MAT) is the reference serological standard (confirming diagnosis via seroconversion, a `≥4-fold` rise in paired sera, or a significant single titer `≥1:400`), while anti-*Leptospira* IgM ELISA or IHA provides rapid serological support.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
All 49 rows in `output_leptospirosis.jsonl` contain explicit `E1` or `E2` markers in `rationale`. Replace them as follows:
- `fulfilling E1 confirmatory criteria` / `confirming acute leptospirosis (E1)` / `(E1)` / `(E1 confirmatory)` → **`providing definitive laboratory confirmation of acute leptospirosis`**
- `(E2)` / `(E2 serologic evidence)` / `(E2 highly specific)` → **`providing highly specific serological evidence supporting the diagnosis`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
All 49 rows in `output_leptospirosis.jsonl` end with `VPD satisfied -> POSITIVE.`. Strip `VPD satisfied` completely.

### 2.3 Handle `POSITIVE` Keywords
- Convert `result: "POSITIVE"` in `step9_key_evidence` into generalized diagnostic statements.
- Replace trailing `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number or designation describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`25-year-old`, `54-year-old`, `73-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution
   - Exact sampling day in this patient (`"on day 5 of illness"`, `"upon discharge 8 days after illness onset"`)
   - Exact titer or fold-change in this patient (`"from 1:100 to 1:3,200"`, `"32-fold titer rise"`)
   - Exact lab values or drug doses for this patient
   - Specific local serovar/strain designations when used as patient-specific findings (e.g., strip `"serovar Mankarso"` and generalize to `"pathogenic Leptospira interrogans serovars"`, while keeping major clinically recognized species/serogroups when they generalize, such as *Leptospira interrogans* serogroup Icterohaemorrhagiae)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Diagnostic thresholds (`"MAT titer ≥1:400 or ≥1:800 is considered significant in a single specimen"`)
   - Seroconversion rules (`"≥4-fold rise in MAT titer between paired acute and convalescent sera is diagnostic"`)
   - Canonical gene targets (`"16S rRNA"`, `"lipL32"`)
   - Clinical definitions (`"thrombocytopenia <150,000/µL"`, `"fever >38.3°C"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"32-fold titer rise from 1:100 to 1:3200"` → `"a ≥4-fold rise in MAT antibody titer between paired acute and convalescent sera"`
   - `"single MAT titer 1:800"` → `"positive MAT at a significant titer consistent with the diagnostic threshold (≥1:400)"`

### 3.2 Highlight Classic Clinical Syndromes & Complications
- Highlight classic clinical syndromes and complications: calf (gastrocnemius) myalgia, conjunctival suffusion, Weil's disease (jaundice, acute kidney injury, hemorrhage), severe pulmonary hemorrhage syndrome (LPHS) / diffuse alveolar hemorrhage with ARDS, aseptic meningitis, myocarditis, or Jarisch-Herxheimer reaction following beta-lactam initiation.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Leptospirosis Confirmed by Paired MAT Titer Rise (`E1`) (`PMC5928731_01::Leptospirosis`)

**INPUT (from `selected_case/output_leptospirosis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Microscopic agglutination test (MAT)", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Leptospira interrogans serovar Mankarso", specimen: "serum", source_quote: "A serum specimen collected on day 5 of illness was positive by MAT with a reciprocal titer of 100 against serogroup Icterohaemorrhagiae (serovar Mankarso). Serum collected upon discharge 8 days after illness onset had a reciprocal MAT titer of 3,200 against serovar Mankarso."}`
- `rationale`:
  `"A 25-year-old male presented with fever, myalgia, bone pain, headache, and thrombocytopenia. Paired MAT testing showed a 32-fold titer rise against Leptospira interrogans serogroup Icterohaemorrhagiae (serovar Mankarso) from 1:100 to 1:3200, fulfilling E1 confirmatory criteria. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Leptospirosis (Leptospira interrogans infection). Reasoning: (1) Acute fever, myalgia, headache, and thrombocytopenia are characteristic early clinical and hematologic features of leptospirosis. (2) The Microscopic Agglutination Test (MAT) against pathogenic Leptospira interrogans serovars is the reference serological method for leptospirosis; demonstration of a ≥4-fold rise in MAT antibody titer between paired acute and convalescent serum specimens provides definitive confirmation of acute infection. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Acute fever, myalgia, headache, and thrombocytopenia are characteristic early clinical and hematologic features of leptospirosis.", "source": "rationale"},
    {"text": "The Microscopic Agglutination Test (MAT) against pathogenic Leptospira interrogans serovars is the reference serological method for leptospirosis; demonstration of a ≥4-fold rise in MAT antibody titer between paired acute and convalescent serum specimens provides definitive confirmation of acute infection.", "source": "step9"}
  ],
  "dropped_specifics": ["25-year-old male", "day 5 and day 8 exact sampling timeline", "exact patient 32-fold titer values (1:100 to 1:3,200; converted to general ≥4-fold rise rule)", "patient-specific serovar Mankarso designation (generalized to pathogenic Leptospira interrogans serovars)"]
}
```

### 4.2 Worked Example 2 — Severe Pulmonary Hemorrhage Leptospirosis Confirmed by BAL mNGS (`E1`) (`PMC9950387_01::Leptospirosis`)

**INPUT (from `selected_case/output_leptospirosis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Metagenomic next-generation sequencing (mNGS)", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Leptospira interrogans", specimen: "bronchoalveolar lavage fluid"}`
- `rationale`:
  `"A 73-year-old farmer who drank raw river water developed fever, gastrocnemius pain, and severe pulmonary hemorrhage complicated by a Jarisch-Herxheimer reaction after piperacillin-tazobactam. Bronchoalveolar lavage mNGS confirmed Leptospira interrogans (E1). VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Leptospirosis (Leptospira interrogans infection with pulmonary hemorrhage syndrome). Reasoning: (1) Fever and calf (gastrocnemius) myalgia following exposure to contaminated freshwater or agricultural environments are classic clinical and epidemiological features of leptospirosis. (2) Severe leptospirosis can be complicated by alveolar hemorrhage (leptospiral pulmonary hemorrhage syndrome) and a Jarisch-Herxheimer reaction following initiation of bactericidal beta-lactam antibiotics. (3) Molecular detection of Leptospira interrogans DNA in bronchoalveolar lavage fluid by metagenomic next-generation sequencing (mNGS) provides definitive pathogen confirmation. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Fever and calf (gastrocnemius) myalgia following exposure to contaminated freshwater or agricultural environments are classic clinical and epidemiological features of leptospirosis.", "source": "rationale"},
    {"text": "Severe leptospirosis can be complicated by alveolar hemorrhage (leptospiral pulmonary hemorrhage syndrome) and a Jarisch-Herxheimer reaction following initiation of bactericidal beta-lactam antibiotics.", "source": "rationale"},
    {"text": "Molecular detection of Leptospira interrogans DNA in bronchoalveolar lavage fluid by metagenomic next-generation sequencing (mNGS) provides definitive pathogen confirmation.", "source": "step9"}
  ],
  "dropped_specifics": ["73-year-old farmer", "specific piperacillin-tazobactam agent (generalized to bactericidal beta-lactam antibiotics)"]
}
```

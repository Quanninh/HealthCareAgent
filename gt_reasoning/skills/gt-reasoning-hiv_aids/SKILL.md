---
name: gt-reasoning-hiv_aids
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for HIV/AIDS cases in selected_case/output_hiv_aids.jsonl by decoding E1/E2/E3
  evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate from
  rationale, normalizing POSITIVE keywords, and generalizing case-specific details
  for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — HIV / AIDS

## Target Disease & Data Scope
- **Target Disease:** `HIV_AIDS` (*Human immunodeficiency virus [HIV-1 / HIV-2] infection and Acquired Immunodeficiency Syndrome [AIDS]*)
- **Source File:** `selected_case/output_hiv_aids.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-hiv_aids/SKILL.md` (`03_evidence_specificity_matrix.md` §5.3)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_hiv_aids.jsonl`

| Tier in `skills/disease-agent-hiv_aids` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_hiv_aids.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive virological/laboratory confirmation via quantitative plasma HIV-1/2 RNA viral load (NAT/RT-PCR), completed multi-step HIV diagnostic algorithm (4th-generation Ag/Ab combination screening + supplemental differentiation assay / Western blot + NAT), or HIV proviral DNA / genotypic resistance sequencing | `HIV-1 RNA quantitative viral load`, `HIV viral load quantification`, `HIV-1 RNA quantitative PCR and CD4 count`, `Plasma HIV-1 RNA quantitative RT-PCR and CD4 count`, `HIV antigen/antibody combination test and HIV RNA quantitative viral load`, `HIV serology, CD4 count, and quantitative viral load`, `HIV antibody test and plasma HIV RNA viral load`, `Multi-assay HIV serologic and chemiluminescent confirmation`, `HIV-1 pol gene amplification and sequencing`, `HIV genotypic resistance testing (reverse transcriptase sequencing)`, `HIV viral load and CD4 count` | **Target:** `HIV-1`, `HIV-1 RNA`, `HIV-1 viral load`, `HIV-1 RNA viral load and CD4 T-lymphocyte count`, `HIV-1 pol gene sequencing`, `HIV-1 RT genotypic resistance`<br>**Specimen:** `plasma`, `blood`, `serum` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Reactive HIV-1/2 serology combined with documented CD4 T-lymphocyte depletion and/or established chronic HIV clinical diagnosis managed with combination antiretroviral therapy (ART/HAART) | `HIV-1 serology and CD4 count`, `HIV-1 diagnostic workup and CD4 count`, `HIV screening/diagnostic testing`, `HIV viral load monitoring and ongoing ART`, `HAART initiation and CD4 cell count`, `Clinical documentation of HIV and HAART history`, `Documented history of HIV seropositivity`, `Clinical history of HIV and antiretroviral therapy`, `CD4 cell count`, `HIV history and ART regimen` | **Target:** `HIV-1`, `HIV`, `HIV infection`, `HIV infection on HAART and CD4 count`, `CD4 T-lymphocyte count`, `Antiretroviral therapy`<br>**Specimen:** `serum`, `blood`, `plasma` |
| **E3 — Supportive (`E3_CLINICAL_DIAGNOSIS` / in `rationale`)** | Severe CD4 T-cell lymphopenia (`<200 cells/mm³` defining AIDS) and AIDS-defining opportunistic infections or malignancies (e.g., *Pneumocystis jirovecii* pneumonia [PJP], cerebral toxoplasmosis, cryptococcal meningitis, Kaposi sarcoma, disseminated mycobacterial or fungal infection, oral/esophageal candidiasis) | `CD4 cell count` (as an immunologic staging marker), opportunistic infection workup in `rationale` | **Target:** `CD4 T-lymphocyte count`, opportunistic pathogens |
| **EXCLUDE — Family Member / Demographic Context (`E4_CONTEXT` / Non-Patient Anchor)** | Non-patient family member labs or pure demographic anchor (**NOT** patient diagnostic evidence). **EXCLUDE** from patient diagnostic claims and log in `dropped_specifics`. | `Grandmother CD4 and viral load` (`PMC9076999_01` — belongs to grandmother, not primary patient), `Patient demographic anchor` (`target_concept: "Patient identity"`, `strength: "E4_CONTEXT"`) | **Target:** Family member HIV status or patient demographics |

### 1.2 Special Anomalies & Compound `test_name` Rules in `output_hiv_aids.jsonl`
1. **Compound `HIV serology, CD4 count, and quantitative viral load` Items:**
   - Many `evidence_items` in `output_hiv_aids.jsonl` bundle three distinct clinical concepts into one `test_name` and `result` (e.g., `result: "POSITIVE; CD4 <5 cells/cc; viral load 1,180,000 copies"`):
     - **HIV Serology / Ag-Ab + HIV-1 RNA Viral Load:** Reactive HIV serology confirmed by quantitative plasma HIV-1 RNA viral load (NAT/RT-PCR) definitively establishes active HIV-1 infection.
     - **CD4 T-Lymphocyte Depletion:** Severe CD4 T-cell depletion below the clinical threshold of `<200 cells/mm³` (or `<200 cells/µL`) defines advanced HIV-induced cellular immunodeficiency (AIDS) and predisposes to opportunistic infections.
2. **`HISTORICAL_PAST` Temporality in Chronic HIV Cases (39 items in `output_hiv_aids.jsonl`):**
   - Unlike acute self-limited infections, HIV is a **chronic lifelong infection**. An initial HIV diagnosis or nadir CD4 count labeled `temporality: "HISTORICAL_PAST"` remains valid diagnostic grounding for active chronic HIV/AIDS in the current episode, especially when paired with ongoing ART/HAART or current viral load/CD4 monitoring.
3. **Undetectable Viral Load on ART (`result: "UNDETECTED"` or `"<40 copies/mL"`):**
   - In patients with known HIV on suppressive HAART/ART, an undetectable plasma HIV RNA viral load (below the assay lower limit of detection, e.g., `<20–50 copies/mL`) reflects **virologic suppression under antiretroviral therapy**, **not** absence of HIV infection.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
In `output_hiv_aids.jsonl`, 30/100 rows contain explicit `E1` or `E2` markers in `rationale`. Replace them as follows:
- `provides E1 confirmatory laboratory evidence of active HIV infection` → **`provides definitive virological confirmation of active HIV infection`**
- `satisfy E2 criteria` / `(E2)` / `(E1)` → **`establish confirmed HIV infection`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
All 100 rows in `output_hiv_aids.jsonl` end with a concluding classification phrase. Strip:
- `Case is positive -> POSITIVE.`
- `VPD satisfied -> POSITIVE.`
- `Conclusive genotypic and virologic confirmation establishes HIV infection -> POSITIVE.` (keep the clinical confirmation meaning, strip `-> POSITIVE.`)

### 2.3 Handle `POSITIVE` Keywords & Rich `result` Strings
- In `output_hiv_aids.jsonl`, `result` contains rich composite strings (`"POSITIVE; CD4 <5 cells/cc; viral load 1,180,000 copies"`, `"REACTIVE; CD4 160 cells/mm3"`, `"KNOWN_HIV_POSITIVE_ON_ART"`, `"CONFIRMED_ON_HAART"`, `"INITIATED"`).
- Always conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`31-year-old`, `46-year-old`), sex (`male`, `female`), exact weight loss in this patient (`"50-pound weight loss"`)
   - Specific country, city, or institution
   - Exact CD4 count in this patient (`"CD4 <5 cells/cc"`, `"CD4 160 cells/mm3"`, `"CD4 94 cells/mm3"`)
   - Exact viral load in this patient (`"1,180,000 copies/mL"`, `"185,976 copies/mL"`)
   - Exact drug doses for this patient

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Virus type designations (`HIV-1`, `HIV-2`) and assay generation (`4th-generation HIV-1/2 antigen/antibody combination immunoassay`)
   - Immunologic staging cutoffs (`"CD4 T-lymphocyte count <200 cells/mm³ (or <200 cells/µL) defines AIDS"`, `"severe immunosuppression with CD4 <50 or <100 cells/mm³ predisposing to specific opportunistic infections"`)
   - Standard virologic suppression thresholds (`"plasma HIV RNA below the lower limit of detection, typically <20–50 copies/mL"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"CD4 <5 cells/cc"` or `"CD4 160 cells/mm3"` → `"profound/severe CD4 T-lymphocyte depletion (<200 cells/mm³, consistent with AIDS)"`
   - `"viral load 1,180,000 copies/mL"` → `"markedly elevated quantitative plasma HIV-1 RNA viral load indicating high-level active viral replication"`
   - `"50-pound weight loss"` → `"severe constitutional weight loss (HIV wasting)"`

### 3.2 Generalize Opportunistic Infections, Co-infections & ART Concepts
- Clearly link the opportunistic disease (e.g., *Pneumocystis jirovecii* pneumonia, cryptococcosis, toxoplasmosis, Kaposi sarcoma, CMV retinitis, tuberculosis, visceral leishmaniasis, HIV-associated distal symmetric polyneuropathy, or immune reconstitution inflammatory syndrome [IRIS]) to HIV-induced CD4 T-cell immunosuppression.
- Generalize specific drug combinations (`tenofovir/lamivudine/efavirenz`, `biktarvy`) to `"combination antiretroviral therapy (ART/HAART)"`.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Newly Diagnosed Advanced HIV/AIDS with Viral Load (`E1`) & PJP (`PMC3722985_01::HIV_AIDS`)

**INPUT (from `selected_case/output_hiv_aids.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "HIV serology, CD4 count, and quantitative viral load", result: "POSITIVE; CD4 <5 cells/cc; viral load 1,180,000 copies", strength: "E1_CONFIRMATORY", target_concept: "HIV-1", specimen: "plasma"}`
- `rationale`:
  `"A 31-year-old male presented with progressive dyspnea, 50-pound weight loss, and oral candidiasis. Diagnostic testing confirmed he was HIV positive with profound CD4 T-cell depletion (<5 cells/cc) and an elevated plasma viral load of 1,180,000 copies/mL. Grocott's methenamine silver staining of bronchoalveolar lavage demonstrated Pneumocystis jiroveci pneumonia, and he subsequently developed Wernicke's encephalopathy. The quantitative viral load provides E1 confirmatory laboratory evidence of active HIV infection. Case is positive -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "HIV/AIDS (Advanced HIV-1 infection with Pneumocystis jirovecii pneumonia). Reasoning: (1) Severe constitutional weight loss, oral candidiasis, and progressive dyspnea with opportunistic Pneumocystis jirovecii pneumonia (PJP) are classic clinical manifestations of advanced HIV-induced immunodeficiency (AIDS). (2) Definitive laboratory diagnosis of active HIV-1 infection is established by reactive HIV serology confirmed by a markedly elevated quantitative plasma HIV-1 RNA viral load. (3) Profound CD4 T-lymphocyte depletion below the AIDS-defining threshold (<200 cells/mm³) confirms severe cellular immunodeficiency and high susceptibility to opportunistic infections. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Severe constitutional weight loss, oral candidiasis, and progressive dyspnea with opportunistic Pneumocystis jirovecii pneumonia (PJP) are classic clinical manifestations of advanced HIV-induced immunodeficiency (AIDS).", "source": "rationale"},
    {"text": "Definitive laboratory diagnosis of active HIV-1 infection is established by reactive HIV serology confirmed by a markedly elevated quantitative plasma HIV-1 RNA viral load.", "source": "step9"},
    {"text": "Profound CD4 T-lymphocyte depletion below the AIDS-defining threshold (<200 cells/mm³) confirms severe cellular immunodeficiency and high susceptibility to opportunistic infections.", "source": "step9"}
  ],
  "dropped_specifics": ["31-year-old male", "exact 50-pound weight loss (converted to severe constitutional weight loss)", "exact patient CD4 count <5 cells/cc (converted to profound CD4 depletion <200 cells/mm³)", "exact patient viral load 1,180,000 copies/mL (converted to markedly elevated viral load)", "Wernicke's encephalopathy secondary nutritional complication"]
}
```

### 4.2 Worked Example 2 — HIV Distal Symmetric Polyneuropathy with Serology & CD4 (`E2`) (`PMC6111644_01::HIV_AIDS`)

**INPUT (from `selected_case/output_hiv_aids.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "HIV-1 serology and CD4 count", result: "REACTIVE; CD4 160 cells/mm3", strength: "E2_HIGHLY_SPECIFIC", target_concept: "HIV-1", specimen: "serum"}`
  - `{test_name: "Clinical diagnosis of HIV neuropathy and ART initiation", result: "INITIATED", strength: "E2_HIGHLY_SPECIFIC", target_concept: "HIV-1 neuropathy", specimen: null}`
- `rationale`:
  `"A 46-year-old male presented with bilateral distal lower leg sensory loss initially evaluated for leprosy. Neurological workup excluded Hansen's disease, and HIV serology revealed reactive antibodies for HIV-1 with a CD4 count of 160 cells/mm3. He was definitively diagnosed with HIV distal symmetric polyneuropathy and initiated on antiretroviral therapy (ART). Reactive HIV-1 serology, CD4 immunosuppression, and establishment of ART satisfy E2 criteria. Case is positive -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "HIV/AIDS (HIV-1 infection complicated by HIV-associated distal symmetric polyneuropathy). Reasoning: (1) HIV-1 infection can present with bilateral distal symmetric sensory polyneuropathy and CD4 T-lymphocyte depletion (<200 cells/mm³). (2) Reactive HIV-1 serology combined with documented CD4 T-cell lymphopenia provides strong laboratory evidence of HIV-1 infection. (3) Initiation of combination antiretroviral therapy (ART) is the standard management for HIV infection and its neurological complications. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "HIV-1 infection can present with bilateral distal symmetric sensory polyneuropathy and CD4 T-lymphocyte depletion (<200 cells/mm³).", "source": "rationale"},
    {"text": "Reactive HIV-1 serology combined with documented CD4 T-cell lymphopenia provides strong laboratory evidence of HIV-1 infection.", "source": "step9"},
    {"text": "Initiation of combination antiretroviral therapy (ART) is the standard management for HIV infection and its neurological complications.", "source": "step9"}
  ],
  "dropped_specifics": ["46-year-old male", "initial leprosy / Hansen's disease evaluation", "exact patient CD4 count 160 cells/mm3 (kept general AIDS threshold <200 cells/mm³)"]
}
```

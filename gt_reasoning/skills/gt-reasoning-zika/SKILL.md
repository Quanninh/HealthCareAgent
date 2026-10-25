---
name: gt-reasoning-zika
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Zika cases in selected_case/output_zika.jsonl by decoding E1/E2/E3 evidence
  tiers from step9_key_evidence, stripping VPD/schema boilerplate from rationale,
  normalizing POSITIVE keywords, and generalizing case-specific details for RAGAS
  evaluation.
---

# Ground Truth Reasoning Extraction Skill — Zika Virus Disease

## Target Disease & Data Scope
- **Target Disease:** `Zika` (*Zika virus [ZIKV] infection, including acute Zika fever, neurological complications [Guillain-Barré syndrome, meningoencephalitis], and Maternal-Fetal / Congenital Zika Syndrome [CZS]*)
- **Source File:** `selected_case/output_zika.jsonl` (20 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-zika/SKILL.md` (`03_evidence_specificity_matrix.md` §5.11)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_zika.jsonl`

| Tier in `skills/disease-agent-zika` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_zika.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive molecular or tissue-level confirmation of Zika virus (ZIKV) infection via NAAT / RT-PCR / qRT-PCR detection of ZIKV RNA in blood/serum, urine (where viral shedding persists longer than in serum), CSF, amniotic fluid, or placental/fetal tissue; viral isolation in cell culture; or ZIKV-specific immunohistochemistry (IHC) / in situ hybridization (ISH) in placental/fetal tissue | **Molecular (RT-PCR / qPCR):** `Zika virus RT-PCR`, `ZIKV real-time RT-PCR`, `qPCR for Zika`, `Polymerase chain reaction (PCR)`, `Zika virus PCR test`, `CSF RT-PCR for ZIKV`, `Real-time reverse transcription PCR (RT-PCR)`, `Amniotic fluid RT-PCR`, `ZIKV RT-PCR`, `Specific ZIKV quantitative RT-PCR`, `Zika virus reverse transcription PCR (RT-PCR)`<br>**Culture + Molecular:** `RT-qPCR and viral culture isolation`<br>**Tissue IHC/ISH:** `Specific staining (IHC/ISH) for ZIKV in placental and fetal tissues` | **Target:** `Zika virus`<br>**Specimen:** `blood`, `serum`, `urine`, `serum and urine`, `cerebrospinal fluid`, `amniotic fluid`, `placenta`, `placenta and fetal tissue` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Zika-specific serology (anti-ZIKV IgM ELISA) confirmed by Plaque Reduction Neutralization Test (`PRNT90%`) to rule out flavivirus cross-reactivity (e.g., dengue) and TORCH pathogens, or ZIKV-specific IgG serology in the appropriate congenital/neurological diagnostic setting | `Zika IgM serology and PRNT90%`, `ZIKV IgM serology and PRNT90%`, `Zika virus serology (IgG antibodies)` | **Target:** `Zika virus`<br>**Specimen:** `serum` |
| **E3 — Supportive (in `rationale`)** | Classic acute clinical features (maculopapular rash, pruritus, low-grade fever, nonpurulent conjunctivitis, arthralgia/myalgia), congenital Zika syndrome hallmarks (microcephaly, ventriculomegaly, intracranial calcifications, arthrogryposis, chorioretinal atrophy), neurological complications (Guillain-Barré syndrome, meningoencephalitis), or vector/travel/sexual transmission history | Mentioned in `rationale` and `source_quote` | Clinical syndrome, congenital/neurological complications, epidemiological/sexual exposure |

### 1.2 Compound `test_name` Splitting Rules (`output_zika.jsonl`)
1. **Compound `Zika IgM serology and PRNT90%` (`PMC7490298_03`, `PMC7490298_06`, `PMC7490298_09`):**
   - Explicitly explain why both assays are used together: *"Because anti-Zika IgM antibodies can cross-react with other flaviviruses (such as dengue), a positive Zika IgM screening assay confirmed by a Plaque Reduction Neutralization Test (PRNT90%) demonstrating ZIKV-specific neutralizing antibodies (along with exclusion of dengue, chikungunya, and TORCH infections) provides highly specific serological confirmation."*
2. **Compound `RT-qPCR and viral culture isolation` (`PMC5962088_01`):**
   - State that RT-qPCR detection of ZIKV RNA in urine combined with viral isolation in cell culture provides definitive virological and molecular confirmation.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
All 20 rows in `output_zika.jsonl` contain explicit `(E1 confirmatory evidence)` or `(E2 ...)` markers in `rationale`. Replace them as follows:
- `(E1 confirmatory evidence)` / `(E1 confirmatory)` → **`(definitive molecular/virological confirmation)`**
- `(E2 highly specific evidence)` / `(E2 evidence)` → **`(highly specific serological confirmation with neutralization testing)`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
All 20 rows in `output_zika.jsonl` end with two protocol validation sentences. Strip **both** sentences completely:
- `Single patient, current episode, primary diagnosis confirmed.` (14 rows)
- `Single patient dyad, current episode, primary diagnosis confirmed.` (3 rows)
- `Single patient dyad, current active gestational episode, primary diagnosis confirmed.` (1 row)
- `Single patient dyad, current gestational episode, primary diagnosis confirmed.` (1 row)
- `Single patient, current active episode, primary diagnosis confirmed.` (1 row)
- `VPD satisfied -> POSITIVE.` (20 rows)

### 2.3 Handle `POSITIVE` Keywords
- Convert `result: "POSITIVE"` in `step9_key_evidence` into generalized diagnostic statements.
- Replace trailing `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`32-year-old`, `24-year-old`, `50-year-old`), sex (`male`, `female`)
   - Specific country, city, or reference laboratory (`Haiti`, `Colombia`, `CDC`, `National Health Institute`)
   - Exact gestational week numbers in this patient (`"at 31 and 36 weeks gestation"` → convert to `"third-trimester prenatal ultrasound"` or `"first-trimester maternal infection"`)
   - Exact head circumference measurement in cm or patient-specific viral load/Ct values
   - Specific cell line names (`SIRC cell culture`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Neutralization assay threshold (`"PRNT90% [90% plaque reduction neutralization test]"` or `"PRNT titer ≥4-fold higher than dengue"`)
   - Clinical definitions (`"severe microcephaly defined as head circumference <3rd or <1st percentile / >2–3 standard deviations below the mean for gestational age and sex"`, `"first-trimester maternal Zika infection carries the highest risk of congenital Zika syndrome"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"head circumference <1st percentile"` → `"severe microcephaly (head circumference below the 1st percentile for gestational age)"`
   - `"ultrasound at 31 and 36 weeks gestation"` → `"third-trimester prenatal neuroimaging"`

### 3.2 Domain-Specific Clinical Generalizations
- **Distinguish Acute Zika Fever vs. Congenital Zika Syndrome in the Header:**
  - Maternal-fetal / congenital cases (`Single patient dyad`): `"Congenital Zika syndrome / Vertical Zika virus infection (Zika virus [ZIKV] infection). Reasoning: ..."`
  - Acute / adult neurological cases: `"Zika virus disease (Zika virus [ZIKV] infection). Reasoning: ..."`
- **Preserve Transmission Route & Specimen Selection Principles:**
  - *Transmission:* Vector-borne (*Aedes* mosquito bite in endemic areas), vertical/transplacental maternal-fetal transmission during pregnancy (causing microcephaly, ventriculomegaly, cerebral calcifications, fetal demise), and sexual transmission from a traveler returning from an endemic area (`PMC6317256_01`).
  - *Specimen selection:* ZIKV RNA can be detected by RT-PCR in blood/serum during the early acute phase, in urine for a prolonged window, in CSF during neuroinvasive disease, and in amniotic fluid or placental/fetal tissues (by RT-PCR or IHC/ISH) in congenital infection.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Congenital Zika Syndrome via Sexual Transmission Confirmed by Placental RT-PCR (`E1`) (`PMC6317256_01::Zika`)

**INPUT (from `selected_case/output_zika.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Zika virus RT-PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Zika virus", specimen: "placenta", source_quote: "confirmation was received from the CDC that all placental samples were positive for Zika RNA, thus supporting the diagnosis of congenital Zika syndrome."}`
- `rationale`:
  `"A 32-year-old woman whose infant had microcephaly (<1st percentile) following paternal travel to Haiti and sexual transmission during pregnancy. CDC evaluation confirmed that all placental samples were positive for Zika RNA by RT-PCR (E1 confirmatory evidence), establishing congenital Zika syndrome. Single patient dyad, current active gestational episode, primary diagnosis confirmed. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Congenital Zika syndrome (Zika virus [ZIKV] infection). Reasoning: (1) Zika virus can be transmitted sexually from an infected partner returning from an endemic region and vertically across the placenta during pregnancy, causing congenital Zika syndrome characterized by severe fetal/neonatal microcephaly (head circumference <1st percentile). (2) Definitive diagnosis of vertical Zika virus infection and congenital Zika syndrome is established by molecular detection of Zika viral RNA in placental tissue by RT-PCR. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Zika virus can be transmitted sexually from an infected partner returning from an endemic region and vertically across the placenta during pregnancy, causing congenital Zika syndrome characterized by severe fetal/neonatal microcephaly (head circumference <1st percentile).", "source": "rationale"},
    {"text": "Definitive diagnosis of vertical Zika virus infection and congenital Zika syndrome is established by molecular detection of Zika viral RNA in placental tissue by RT-PCR.", "source": "step9"}
  ],
  "dropped_specifics": ["32-year-old woman", "paternal travel to Haiti", "CDC reference lab name"]
}
```

### 4.2 Worked Example 2 — Congenital Zika Infection Confirmed by ZIKV IgM & PRNT90% (`E2`) (`PMC7490298_03::Zika`)

**INPUT (from `selected_case/output_zika.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "ZIKV IgM serology and PRNT90%", result: "POSITIVE", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Zika virus", specimen: "serum", source_quote: "Her IgM serology for ZIKV was positive and non-reactive for dengue, chikungunya, rubella, toxoplasmosis, cytomegalovirus, herpes, and syphilis, and the plaque reduction neutralization test (PRNT90%) was positive for ZIKV."}`
- `rationale`:
  `"An infant with microcephaly and cerebral calcifications born to a mother who had a Zika-like rash illness in the first trimester. Serology was positive for ZIKV IgM and confirmed by a positive ZIKV plaque reduction neutralization test (PRNT90%) with negative dengue, chikungunya, and TORCH serologies (E2 highly specific evidence). Single patient dyad, current episode, primary diagnosis confirmed. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Congenital Zika syndrome (Zika virus [ZIKV] infection). Reasoning: (1) Maternal exanthematous illness during the first trimester of pregnancy followed by fetal/neonatal microcephaly and intracranial calcifications is characteristic of congenital Zika syndrome. (2) Positive ZIKV-specific IgM serology confirmed by a Plaque Reduction Neutralization Test (PRNT90%) demonstrating neutralizing antibodies against Zika virus—along with negative serology for cross-reactive arboviruses (dengue, chikungunya) and TORCH pathogens—provides highly specific serological confirmation of Zika virus infection. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Maternal exanthematous illness during the first trimester of pregnancy followed by fetal/neonatal microcephaly and intracranial calcifications is characteristic of congenital Zika syndrome.", "source": "rationale"},
    {"text": "Positive ZIKV-specific IgM serology confirmed by a Plaque Reduction Neutralization Test (PRNT90%) demonstrating neutralizing antibodies against Zika virus—along with negative serology for cross-reactive arboviruses (dengue, chikungunya) and TORCH pathogens—provides highly specific serological confirmation of Zika virus infection.", "source": "step9"}
  ],
  "dropped_specifics": ["single patient dyad annotation boilerplate"]
}
```

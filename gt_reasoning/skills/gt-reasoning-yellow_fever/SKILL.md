---
name: gt-reasoning-yellow_fever
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Yellow Fever cases in selected_case/output_yellow_fever.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate
  from rationale, normalizing POSITIVE keywords, and generalizing case-specific
  details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Yellow Fever

## Target Disease & Data Scope
- **Target Disease:** `Yellow_Fever` (*Yellow fever virus [YFV] infection*)
- **Source File:** `selected_case/output_yellow_fever.jsonl` (3 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-yellow_fever/SKILL.md` (`03_evidence_specificity_matrix.md` §5.15)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_yellow_fever.jsonl`

| Tier in `skills/disease-agent-yellow_fever` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_yellow_fever.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive virological/molecular confirmation of yellow fever virus (YFV) infection via RT-PCR / qRT-PCR (or multiplex arbovirus qRT-PCR) in serum, blood, urine, or semen; viral isolation in cell culture; or whole-genome sequencing | `Yellow fever virus RT-PCR`, `multiplex qRT-PCR for arboviruses`, `YFV qRT-PCR and IgM-capture ELISA`, `Yellow fever virus isolation in cell culture` | **Target:** `Yellow fever virus`, `Yellow fever virus RNA and IgM`<br>**Specimen:** `serum`, `urine`, `urine and serum`, `semen` |
| **E2 — Strong / Highly Specific** | Specific YFV IgM-capture ELISA (MAC-ELISA) or plaque reduction neutralization test (PRNT) interpreted alongside confirmed absence of recent yellow fever vaccination and exclusion of cross-reactive flaviviruses (such as dengue or Zika) | Bundled inside `YFV qRT-PCR and IgM-capture ELISA` (`PMC5749440_01` — unvaccinated patient with positive specific IgM-capture ELISA alongside urine qRT-PCR and viral isolation) | **Target:** `Yellow fever virus IgM`<br>**Specimen:** `serum` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Characteristic biphasic clinical syndrome (acute high-grade fever, malaise, myalgia, headache, thrombocytopenia, hemorrhagic features such as ecchymosis, and severe icteric hepatitis with marked transaminitis and jaundice, or late-onset relapsing hepatitis) and exposure/travel in a sylvatic/endemic transmission zone in an unvaccinated individual | `Clinical presentation and hepatic enzyme panel` | **Target:** `Acute hepatitis due to Yellow fever`<br>**Specimen:** `serum` |
| **DISCORDANT — Inconclusive Rapid Serology (`INCONCLUSIVE`)** | Early or inconclusive rapid antibody test superseded by confirmatory molecular detection (qRT-PCR). Generalize as: *"An inconclusive rapid IgM antibody screening test during the acute viremic phase does not exclude yellow fever when viral RNA is definitively detected by qRT-PCR."* | `Rapid antibody test for YFV IgM` (`result: "INCONCLUSIVE"`, `relation: "INCONCLUSIVE"`, `strength: "E3_SUPPORTIVE"`, in `PMC8749146_01`) | **Target:** `Yellow fever virus IgM`<br>**Specimen:** `serum` |

### 1.2 Compound `test_name` Splitting Rule (`PMC5749440_01`)
In `PMC5749440_01`, `test_name: "YFV qRT-PCR and IgM-capture ELISA"` bundles molecular detection in urine (`E1`) and specific IgM-capture ELISA in serum (`E2`):
- **Rule:** Split into two distinct diagnostic claims:
  1. **E1 Claim:** Definitive diagnosis is established by molecular detection of yellow fever virus RNA by qRT-PCR (including prolonged viral shedding in urine and semen) and viral isolation in cell culture.
  2. **E2 Claim:** Positive YFV-specific IgM-capture ELISA in an unvaccinated patient provides highly specific serological confirmation of wild-type yellow fever virus infection.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E3`) in `rationale`
All 3 rows in `output_yellow_fever.jsonl` contain explicit `E1` markers in `rationale`. Replace them as follows:
- `E1 confirmatory lab evidence is present for the primary human patient in the current episode.` → **Strip completely** (already covered by the RT-PCR claim)
- `confirming a true coinfection. Inconclusive rapid IgM testing does not contradict the confirmatory E1 molecular result.` → Replace `the confirmatory E1 molecular result` with **`definitive molecular confirmation by qRT-PCR`**
- `E1 confirmatory lab criteria are fully satisfied.` → **Strip completely**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Remove `VPD satisfied -> POSITIVE.` from all 3 rows.

### 2.3 Handle `POSITIVE` Keywords & `DETECTED` / `INCONCLUSIVE` Results
- Convert `result: "POSITIVE"` and `result: "DETECTED"` on RT-PCR / cell culture items into generalized molecular and virological diagnostic claims.
- Handle `result: "INCONCLUSIVE"` on rapid IgM testing (`PMC8749146_01`) by stating that inconclusive rapid serology in the acute phase is superseded by definitive molecular qRT-PCR detection.
- Conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`42-year-old`, `65-year-old`), sex (`male`)
   - Specific dates or patient timelines (`July 2018`, `10 days after initial symptoms`, `21 days after symptom onset`)
   - Specific state/city names (`Minas Gerais, Brazil`)
   - Exact liver enzyme levels in this patient (`"AST 2216 U/L, ALT 1611 U/L"`)
   - Exact cycle threshold, viral load, or ELISA optical density in this patient (`"Ct 17.42, 9.3 x 10^6 RNA copies/mL"`, `"Ct 24.35, 6.7 x 10^4 RNA copies/mL"`, `"OD 1.19"`)
   - Patient-specific genome strain IDs (`"BRMG-2017"`), while keeping general co-infecting serotype designations (`"dengue virus serotype 2 [DENV-2]"`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Standard clinical definitions (`"marked transaminitis >1000 U/L with AST typically exceeding ALT in yellow fever hepatitis"`, `"acute viremic window during days 1–5 of illness"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"AST 2216 U/L, ALT 1611 U/L"` → `"markedly elevated serum transaminases (severe acute hepatocellular injury/transaminitis, characteristically with AST exceeding ALT)"`
   - `"Ct 17.42 (9.3 x 10^6 RNA copies/mL) in urine and Ct 24.35 in semen"` → `"high viral RNA load in urine and persistent viral RNA shedding in semen"`

### 3.2 Preserve Important Clinical & Virological Concepts
- *Relapsing hepatitis (`PMC7310355_01`):* Yellow fever typically causes acute febrile hepatitis with marked transaminitis and jaundice, and can occasionally be followed by late-onset relapsing hepatitis after initial recovery.
- *Arboviral co-infection (`PMC8749146_01`):* In regions where *Aedes* / sylvatic vectors and multiple flaviviruses co-circulate, multiplex qRT-PCR can simultaneously detect yellow fever virus and dengue virus (e.g., DENV-2) co-infection.
- *Unvaccinated status (`PMC5749440_01`):* Confirming that the patient is unvaccinated against yellow fever is critical when interpreting serological assays (IgM-capture ELISA), as yellow fever vaccine can induce cross-reactive IgM antibodies.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Yellow Fever with Acute Hepatitis & Late-Onset Relapse Confirmed by RT-PCR (`E1`) (`PMC7310355_01::Yellow_Fever`)

**INPUT (from `selected_case/output_yellow_fever.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Yellow fever virus RT-PCR", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Yellow fever virus", specimen: "serum"}`
  - `{test_name: "Clinical presentation and hepatic enzyme panel", result: "POSITIVE", strength: "E3_SUPPORTIVE", target_concept: "Acute hepatitis due to Yellow fever", specimen: "serum"}`
- `rationale`:
  `"A 42-year-old male was admitted with high-grade fever, malaise, myalgia, severe transaminitis (AST 2216 U/L, ALT 1611 U/L), and subsequent jaundice. Yellow fever virus PCR performed during the acute episode was confirmed positive, establishing acute yellow fever infection and explaining subsequent late-onset hepatitis relapse. E1 confirmatory lab evidence is present for the primary human patient in the current episode. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Yellow fever (Yellow fever virus [YFV] infection). Reasoning: (1) High-grade fever, malaise, myalgia, markedly elevated serum transaminases (severe acute transaminitis with AST exceeding ALT), and jaundice are classic clinical and biochemical manifestations of icteric yellow fever hepatitis, which can occasionally be complicated by late-onset relapsing hepatitis. (2) Definitive diagnosis of acute yellow fever is established by molecular detection of yellow fever virus RNA in serum by RT-PCR during the acute viremic phase. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "High-grade fever, malaise, myalgia, markedly elevated serum transaminases (severe acute transaminitis with AST exceeding ALT), and jaundice are classic clinical and biochemical manifestations of icteric yellow fever hepatitis, which can occasionally be complicated by late-onset relapsing hepatitis.", "source": "rationale"},
    {"text": "Definitive diagnosis of acute yellow fever is established by molecular detection of yellow fever virus RNA in serum by RT-PCR during the acute viremic phase.", "source": "step9"}
  ],
  "dropped_specifics": ["42-year-old male", "4-day symptom duration", "exact patient transaminase values AST 2216 U/L and ALT 1611 U/L (kept clinical interpretation of severe transaminitis with AST > ALT)"]
}
```

### 4.2 Worked Example 2 — Yellow Fever & Dengue Co-Infection Confirmed by Multiplex qRT-PCR (`E1`) (`PMC8749146_01::Yellow_Fever`)

**INPUT (from `selected_case/output_yellow_fever.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "multiplex qRT-PCR for arboviruses", result: "DETECTED", strength: "E1_CONFIRMATORY", target_concept: "Yellow fever virus", specimen: "serum"}`
  - `{test_name: "Rapid antibody test for YFV IgM", result: "INCONCLUSIVE", strength: "E3_SUPPORTIVE", relation: "INCONCLUSIVE", target_concept: "Yellow fever virus IgM", specimen: "serum"}`
- `rationale`:
  `"A patient presented in July 2018 with acute symptoms of fever, myalgia, and headache during co-circulation of arboviruses in Brazil. Serum multiplex qRT-PCR definitively detected genetic material of both yellow fever virus (YFV) and dengue serotype 2 (DENV2), confirming a true coinfection. Inconclusive rapid IgM testing does not contradict the confirmatory E1 molecular result. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Yellow fever (Yellow fever virus [YFV] infection, with Dengue virus serotype 2 co-infection). Reasoning: (1) Acute fever, myalgia, and headache in a region with co-circulating arboviruses are compatible with acute flavivirus infection. (2) Definitive diagnosis of yellow fever (and concurrent arboviral co-infection such as dengue serotype 2) is established by molecular detection of viral RNA in serum using multiplex quantitative RT-PCR (qRT-PCR). (3) An inconclusive rapid IgM antibody test during the acute viremic window does not exclude yellow fever when viral RNA is confirmed by qRT-PCR. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Acute fever, myalgia, and headache in a region with co-circulating arboviruses are compatible with acute flavivirus infection.", "source": "rationale"},
    {"text": "Definitive diagnosis of yellow fever (and concurrent arboviral co-infection such as dengue serotype 2) is established by molecular detection of viral RNA in serum using multiplex quantitative RT-PCR (qRT-PCR).", "source": "step9"},
    {"text": "An inconclusive rapid IgM antibody test during the acute viremic window does not exclude yellow fever when viral RNA is confirmed by qRT-PCR.", "source": "step9"}
  ],
  "dropped_specifics": ["July 2018 date", "Brazil location"]
}
```

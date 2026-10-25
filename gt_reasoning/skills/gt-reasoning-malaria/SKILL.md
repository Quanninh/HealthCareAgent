---
name: gt-reasoning-malaria
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Malaria cases in selected_case/output_malaria.jsonl by decoding E1/E2/E3
  evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate from
  rationale, normalizing POSITIVE keywords, and generalizing case-specific details
  for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Malaria

## Target Disease & Data Scope
- **Target Disease:** `Malaria` (*Plasmodium falciparum*, *Plasmodium vivax*, *Plasmodium ovale*, *Plasmodium malariae*, *Plasmodium knowlesi*, or mixed *Plasmodium* infection)
- **Source File:** `selected_case/output_malaria.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-malaria/SKILL.md` (`03_evidence_specificity_matrix.md` §5.4)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_malaria.jsonl`

| Tier in `skills/disease-agent-malaria` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_malaria.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive parasitological demonstration of *Plasmodium* parasites (ring forms, trophozoites, schizonts, or gametocytes) on thick and thin peripheral blood smears (or bone marrow aspirate), detection of malarial antigen (HRP2 / pLDH / aldolase) by rapid diagnostic test (RDT), or species-specific molecular detection by PCR / qPCR / LAMP | **Microscopy:** `Peripheral blood smear microscopy`, `Peripheral blood smear examination`, `Peripheral blood smear`, `Blood smear microscopy`, `Peripheral blood microscopy`, `Thick and thin blood smear microscopy`, `Peripheral blood film examination`, `Thick blood smear`, `Repeat peripheral blood smear`, `Bone marrow aspirate microscopy`, `Alcoholic ammonium hydroxide bleaching of trephine biopsy pigment` (hemozoin)<br>**Antigen RDT:** `Malaria rapid diagnostic test (RDT)`, `Malaria rapid diagnostic test (MRDT)`, `Rapid malarial antigen test`<br>**Molecular:** `Plasmodium species-specific PCR`, `Real-time PCR`, `Nested PCR`<br>**Compound:** `Malaria rapid diagnostic test and thin blood smear`, `Rapid malaria test, microscopy, and qPCR` | **Target:** `Plasmodium falciparum`, `Plasmodium vivax`, `Plasmodium ovale`, `Plasmodium malariae`, `Plasmodium knowlesi`, `Plasmodium species`, `malarial pigment (hemozoin)`<br>**Specimen:** `peripheral blood`, `blood`, `bone marrow` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_STRONG`)** | Characteristic clinical/ophthalmologic diagnosis of severe malaria (e.g., malarial retinopathy on indirect ophthalmoscopy in cerebral malaria, or confirmed clinical/parasitological evaluation with response to antimalarial therapy when raw smear details are summarized at the clinical level) | `Indirect ophthalmoscopy (retinography)`, `Clinical diagnosis of cerebral malaria`, `Clinical diagnosis and antimalarial therapy`, `Diagnostic malaria blood test`, `Clinical and species-specific diagnostic evaluation`, `clinical confirmation of congenital P. ovale malaria` | **Target:** `Malarial retinopathy`, `Plasmodium falciparum cerebral malaria`, `Severe malaria`, `Severe Plasmodium falciparum malaria`, `Plasmodium vivax`, `Plasmodium ovale` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Antimalarial treatment response (intravenous artesunate, artemisinin-based combination therapy [ACT], chloroquine + 14-day primaquine for radical cure of *P. vivax*/*P. ovale* hypnozoites, or quinine), classic malarial paroxysms (cyclical fever, chills, rigors), hemolytic anemia, thrombocytopenia, splenomegaly, and endemic travel/residence | `Antimalarial treatment`, `Specific antimalarial therapy`, `Antimalarial regimen`, `Antimalarial treatment regimen`, `Response to intravenous quinine therapy`, `Antimalarial therapeutic response`, `Clinical physical examination`, `Clinical presentation and history` | **Target:** `Plasmodium falciparum`, `Plasmodium vivax`, `Acute febrile malaria syndrome`, `Acute malaria paroxysm syndrome` (`result: "ADMINISTERED"`, `"TREATED"`, `"RESPONSIVE"`) |
| **EXCLUDE — Post-Treatment Parasite Clearance (`result = NEGATIVE` / `PARASITE_CLEARANCE`)** | Follow-up smear confirming parasite clearance after antimalarial therapy (**NOT** diagnostic of malaria infection). **EXCLUDE** negative follow-up clearance smears from diagnostic claims and log in `dropped_specifics`. | `Follow-up peripheral blood smear`, `Follow-up peripheral blood malaria smear`, `Follow-up hemoscopy (blood smear examination)`, `Follow-up peripheral blood smear evaluation`, `Follow-up blood smear parasitemia control` (where `result = NEGATIVE` or `PARASITE_CLEARANCE` and `target_concept` is `Plasmodium ... clearance`) | **Target:** `Plasmodium falciparum clearance`, `Plasmodium vivax clearance`, `Plasmodium clearance` |
| **EXCLUDE — Unrelated Co-Infection Context (`E4_CONTEXT`)** | Diagnostic test for a separate co-infecting pathogen. **EXCLUDE** from malaria diagnostic claims and log in `dropped_specifics`. | `Polymerase chain reaction (PCR)` with `target_concept: "Lassa virus"` (`strength: "E4_CONTEXT"`, in `PMC8976985_01`) | **Target:** `Lassa virus` |
| **DISCORDANT — Initial Negative Smear (`E0_CONTRADICTED` / `REFUTES` / `INCONCLUSIVE`)** | Initial negative thick/thin smear or RDT due to low parasitemia/sequestration, later confirmed by repeat smear, bone marrow exam, or PCR. Generalize as: *"A single negative initial blood smear or RDT does not exclude malaria (particularly during low parasitemia or deep vascular sequestration); serial blood film examination or molecular testing by PCR is required."* | `Thick peripheral blood smear` (`result: "NEGATIVE"`, `relation: "REFUTES"`), `malaria thick and thin blood films and rapid diagnostic test` (`relation: "INCONCLUSIVE"`) | **Target:** `Plasmodium falciparum`, `Plasmodium species` |

### 1.2 Compound `test_name` Splitting Rule
In `output_malaria.jsonl`, many records combine **Malaria RDT**, **Blood Smear Microscopy**, and/or **PCR** into a single `evidence_item` (e.g., `test_name: "Malaria rapid diagnostic test and thin blood smear"` or `"Rapid malaria test, microscopy, and qPCR"`):
- **Rule:** Clearly articulate their complementary diagnostic roles:
  1. **Thick and Thin Blood Smear Microscopy:** Microscopic examination of thick and thin peripheral blood smears is the gold-standard method for detecting *Plasmodium* parasites (trophozoites, schizonts, gametocytes), quantifying parasitemia, and identifying the causative species.
  2. **Rapid Diagnostic Test (RDT):** Malaria antigen RDTs (detecting *P. falciparum*-specific HRP2 or pan-malarial pLDH/aldolase) provide rapid antigen-based confirmation, complemented by microscopy for species identification and parasite density assessment.
  3. **Molecular PCR:** Species-specific PCR / qPCR provides highly sensitive confirmation and definitive speciation, especially in low-density, submicroscopic, or mixed *Plasmodium* infections (or to distinguish *P. knowlesi* from *P. malariae*/*P. falciparum*).

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`, `E3`) in `rationale`
In `output_malaria.jsonl`, 88/100 rows contain explicit tier markers in `rationale`. Replace them as follows:
- `(E1 confirmatory)` / `(E1 confirmatory lab)` / `E1 confirmatory lab evidence` / `E1 confirmatory lab criteria` → **`definitive parasitological/laboratory confirmation`**
- `(E2)` / `(E2 strong)` → **`highly specific clinical/diagnostic evidence`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Remove all trailing schema/protocol sentences from `rationale`:
- `E1 confirmatory lab evidence is established for the primary patient in the current active episode.`
- `E1 confirmatory lab criteria are met for the neonate during the current episode.`
- `Single patient, current episode, primary diagnosis confirmed.` / `Single patient, current episode, comorbidity confirmed.`
- `VPD satisfied -> POSITIVE.` / `VPD -> POSITIVE.` / `VPD = true -> POSITIVE.` / `VPD is satisfied -> POSITIVE.` / `VPD fully satisfied -> POSITIVE.`
- `All criteria for a Valid Positive Diagnosis of Malaria are satisfied -> POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords & Non-Diagnostic `result` Values
- Convert `result: "POSITIVE"` or `"CONFIRMED"` on diagnostic tests into generalized diagnostic principles.
- Exclude `result: "NEGATIVE"` / `"PARASITE_CLEARANCE"` on follow-up smears from diagnostic claims and record them in `dropped_specifics`.
- Convert `result: "ADMINISTERED"` / `"TREATED"` / `"RESPONSIVE"` on antimalarial therapy items (`strength: "E3_SUPPORTIVE"`) into a generalized treatment claim.
- Always conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`2-day-old`, `7-year-old`, `71-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution (`Togo`, `Colombia`)
   - Exact dates or patient timeline (`"36 hours after delivery"`, `"December 13, 2019"`, `"day 5 negative smear"`)
   - Exact parasitemia count or percentage in this patient (`"1.846*10^3 infected RBCs"`, `"3.2% parasitemia"`)
   - Exact lab values or individual drug doses in this patient (`"12 hr / 24 hr dosing schedule"`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - WHO hyperparasitemia / severe malaria thresholds (`"hyperparasitemia >5% or >10% in Plasmodium falciparum malaria defines severe malaria"`, `"severe malarial anemia with hemoglobin <5 g/dL in children or <7 g/dL in adults"`)
   - Standard fever periodicity rules (`"48-hour tertian fever cycle in P. falciparum, P. vivax, and P. ovale; 72-hour quartan cycle in P. malariae; 24-hour quotidian cycle in P. knowlesi"`)
   - Standard radical cure duration rules (`"14-day primaquine course for radical cure of P. vivax/P. ovale hypnozoites"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"15% parasitemia"` → `"marked hyperparasitemia (>5–10% infected erythrocytes, a criterion for severe falciparum malaria)"`
   - `"1.846*10^3 infected RBCs"` → `"patent Plasmodium falciparum parasitemia on peripheral blood smear"`
   - `"Hb 4.2 g/dL"` → `"severe malarial anemia"`

### 3.2 Domain-Specific Clinical Generalizations
- **Always Specify the Causative *Plasmodium* Species in the Header:** e.g., `"Malaria (Plasmodium falciparum infection)"`, `"Malaria (Plasmodium vivax infection)"`, `"Mixed malaria (Plasmodium falciparum and Plasmodium vivax co-infection)"`, or `"Congenital malaria (Plasmodium falciparum infection)"`.
- **Generalize Severe Malaria Syndromes & Complications:** Link recognized complications to the species: cerebral malaria, blackwater fever (intravascular hemolysis with hemoglobinuria), acute kidney injury, metabolic acidosis, severe malarial anemia, splenic infarction/rupture (especially in *P. vivax*), secondary hemophagocytic lymphohistiocytosis (HLH), post-artemisinin delayed hemolysis (PADH), or congenital/placental transmission.
- **Generalize Species-Appropriate Antimalarial Therapy:** Parenteral artesunate (or quinine) followed by artemisinin-based combination therapy (ACT) is standard for severe *P. falciparum* malaria; chloroquine (or ACT) combined with primaquine (to eradicate hepatic hypnozoites and prevent relapse) is standard for *P. vivax* and *P. ovale* malaria.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — *Plasmodium vivax* Malaria with HLH & Hemozoin Pigment (`E1`) (`PMC7365499_01::Malaria`)

**INPUT (from `selected_case/output_malaria.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Peripheral blood smear examination", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Plasmodium vivax", specimen: "peripheral blood", source_quote: "The peripheral smear revealed fragmented red blood cells and on careful examination, schizonts of P. vivax [Figure 5a]."}`
  - `{test_name: "Alcoholic ammonium hydroxide bleaching of trephine biopsy pigment", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "malarial pigment (hemozoin)", specimen: "bone marrow trephine biopsy"}`
- `rationale`:
  `"A 7-year-old girl presented with 3 weeks of fever, abdominal distension, hepatosplenomegaly, and pancytopenia. Bone marrow trephine biopsy revealed hemophagocytic lymphohistiocytosis (HLH) with histiocytes containing brown pigment confirmed to be malarial pigment (hemozoin) via ammonium hydroxide bleaching. Peripheral blood smear confirmed schizonts of Plasmodium vivax. She was successfully treated with chloroquine and primaquine with complete recovery. E1 confirmatory lab evidence is established for the primary patient in the current active episode. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Malaria (Plasmodium vivax infection). Reasoning: (1) Prolonged fever, hepatosplenomegaly, and pancytopenia are characteristic clinical features of malaria, which can be complicated by secondary hemophagocytic lymphohistiocytosis (HLH). (2) Definitive diagnosis of Plasmodium vivax malaria is established by direct identification of parasite forms (such as P. vivax schizonts) on peripheral blood smear microscopy. (3) Demonstration of intracellular malarial pigment (hemozoin, confirmed by alcoholic ammonium hydroxide bleaching) within bone marrow histiocytes provides additional confirmatory histopathological evidence of malaria. (4) Standard radical cure of Plasmodium vivax malaria consists of schizonticidal therapy with chloroquine combined with primaquine to eradicate hepatic hypnozoites. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Prolonged fever, hepatosplenomegaly, and pancytopenia are characteristic clinical features of malaria, which can be complicated by secondary hemophagocytic lymphohistiocytosis (HLH).", "source": "rationale"},
    {"text": "Definitive diagnosis of Plasmodium vivax malaria is established by direct identification of parasite forms (such as P. vivax schizonts) on peripheral blood smear microscopy.", "source": "step9"},
    {"text": "Demonstration of intracellular malarial pigment (hemozoin, confirmed by alcoholic ammonium hydroxide bleaching) within bone marrow histiocytes provides additional confirmatory histopathological evidence of malaria.", "source": "step9"},
    {"text": "Standard radical cure of Plasmodium vivax malaria consists of schizonticidal therapy with chloroquine combined with primaquine to eradicate hepatic hypnozoites.", "source": "rationale"}
  ],
  "dropped_specifics": ["7-year-old girl", "3-week fever duration", "[Figure 5a] and [Figure 5b] references"]
}
```

### 4.2 Worked Example 2 — Congenital *Plasmodium falciparum* Malaria with RDT + Blood Smear (`E1`) & Excluded Clearance Smear (`PMC8282370_01::Malaria`)

**INPUT (from `selected_case/output_malaria.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Malaria rapid diagnostic test and thin blood smear", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Plasmodium falciparum", specimen: "peripheral blood"}`
  - `{test_name: "Antimalarial treatment", result: "ADMINISTERED", strength: "E3_SUPPORTIVE", target_concept: "Plasmodium falciparum", specimen: "not applicable"}`
  - `{test_name: "Follow-up peripheral blood smear", result: "NEGATIVE", strength: "E1_CONFIRMATORY", target_concept: "Plasmodium falciparum clearance", specimen: "peripheral blood"}` ← **EXCLUDE** (`target_concept = clearance`)
- `rationale`:
  `"A 2-day-old neonate developed high-grade fever, irritability, and jaundice 36 hours after delivery. Malaria rapid diagnostic test (MRDT) for P. falciparum was positive, and thin blood smear demonstrated P. falciparum infection with 1.846*10^3 infected RBCs. Maternal blood smear and rapid test were negative, confirming congenital malaria in the newborn. Intravenous artesunate resulted in complete parasite clearance on day 5. E1 confirmatory lab criteria are met for the neonate during the current episode. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Congenital malaria (Plasmodium falciparum infection). Reasoning: (1) Congenital malaria can present in neonates with early-onset fever, irritability, and jaundice, even when maternal peripheral blood smears are negative at delivery due to placental sequestration. (2) Definitive diagnosis requires parasite-based confirmation by thin peripheral blood smear microscopy demonstrating Plasmodium falciparum parasitemia and a positive P. falciparum malaria rapid diagnostic test (RDT). (3) Parenteral artesunate is the standard treatment for neonatal/severe Plasmodium falciparum malaria. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Congenital malaria can present in neonates with early-onset fever, irritability, and jaundice, even when maternal peripheral blood smears are negative at delivery due to placental sequestration.", "source": "rationale"},
    {"text": "Definitive diagnosis requires parasite-based confirmation by thin peripheral blood smear microscopy demonstrating Plasmodium falciparum parasitemia and a positive P. falciparum malaria rapid diagnostic test (RDT).", "source": "step9"},
    {"text": "Parenteral artesunate is the standard treatment for neonatal/severe Plasmodium falciparum malaria.", "source": "step9"}
  ],
  "dropped_specifics": ["2-day-old neonate", "36 hours after delivery", "exact patient parasite density 1.846*10^3 infected RBCs (converted to patent P. falciparum parasitemia)", "12 hr / 24 hr dosing schedule", "day 5 negative follow-up blood smear (excluded: target_concept = clearance, not diagnosis)"]
}
```

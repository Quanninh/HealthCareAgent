---
name: gt-reasoning-leishmaniasis
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Leishmaniasis cases in selected_case/output_leishmaniasis.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate
  from rationale, normalizing POSITIVE keywords, and generalizing case-specific
  details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Leishmaniasis

## Target Disease & Data Scope
- **Target Disease:** `Leishmaniasis` (*Visceral [kala-azar], Cutaneous, Mucocutaneous / Tegumentary, and Post-kala-azar dermal leishmaniasis [PKDL]*)
- **Source File:** `selected_case/output_leishmaniasis.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-leishmaniasis/SKILL.md` (`03_evidence_specificity_matrix.md` §5.7)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Leishmaniasis in `output_leishmaniasis.jsonl` spans distinct clinical syndromes (**Visceral leishmaniasis** caused by *L. donovani* complex / *L. infantum* / *L. chagasi*, **Cutaneous leishmaniasis** caused by *L. major*, *L. tropica*, *L. mexicana*, *L. amazonensis*, etc., and **Mucocutaneous / Tegumentary leishmaniasis** caused by *L. (Viannia) braziliensis*, *L. panamensis*, *L. guyanensis*). Always specify the clinical form and causative *Leishmania* species/complex in the header of `ground_truth_reasoning` when known.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_leishmaniasis.jsonl`

| Tier in `skills/disease-agent-leishmaniasis` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_leishmaniasis.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY`)** | Definitive parasitological demonstration of *Leishmania* amastigotes (Leishman-Donovan bodies) in tissue/smear, parasite isolation in culture (e.g., NNN/RPMI medium), or molecular detection/speciation by PCR / sequencing | **Microscopy/Histopathology:** `Bone marrow aspirate microscopy`, `Bone marrow biopsy histopathology`, `Bone marrow smear microscopy`, `Splenic aspirate microscopy`, `Skin biopsy histopathological evaluation`, `Punch biopsy histopathological examination`, `Giemsa stain microscopic examination of skin lesion smear`, `Direct parasite search on lesion scraping`, `Fine needle aspiration cytology of lymph node`, `Liver and bone marrow biopsy histopathology`<br>**Culture:** `Culture in NNN medium`, `Blood culture`<br>**Molecular:** `PCR for Leishmania species identification`, `Blood Leishmania quantitative PCR`, `kDNA PCR for Leishmania (Viannia) subgenus`, `ITS1 PCR-RFLP`, `ITS1 rRNA gene sequence analysis`, `Mini-exon PCR-RFLP`, `mNGS` | **Target:** `Leishmania amastigotes`, `Leishmania LD bodies`, `Leishmania donovani`, `Leishmania infantum`, `Leishmania major`, `Leishmania tropica`, `Leishmania (Viannia) braziliensis`, `Leishmania amazonensis`, `Leishmania mexicana`, `Leishmania DNA`<br>**Specimen:** `bone marrow`, `spleen`, `skin biopsy`, `skin scraping smear`, `lymph node aspirate`, `liver biopsy`, `mucosal/lip lesion`, `peripheral blood` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC`)** | Highly specific serological testing (e.g., rK39 immunochromatographic/ELISA assay, IIF, DAT) for visceral leishmaniasis, or delayed-type hypersensitivity skin test (Montenegro test, typically positive at `≥5 mm` induration) supporting tegumentary leishmaniasis; requires clinical/parasitological correlation | `rK39 ELISA serology`, `rK39 immunochromatographic rapid test`, `rK39 rapid antibody test`, `CDC rK39 antibody test`, `rK39 antigen immunochromatography`, `Anti-Leishmania serology (IIF and rK39 rapid test)`, `Anti-Leishmania indirect immunofluorescence serology`, `Anti-Leishmania antibody ELISA`, `Montenegro intradermal test (MIT)`, `Montenegro skin test` | **Target:** `Leishmania antibodies`, `Leishmania rK39 antigen antibodies`, `Leishmania infantum`, `Delayed-type hypersensitivity to Leishmania`<br>**Specimen:** `serum`, `intradermal skin test` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Therapeutic response to standard anti-leishmanial agents or compatible clinical features (fever, hepatosplenomegaly, pancytopenia, chronic cutaneous/mucosal ulceration) | `Intralesional meglumine antimoniate (Glucantime) treatment response`, `Intravenous meglumine antimoniate treatment response`, `Amphotericin B treatment response`, `Response to liposomal amphotericin B therapy`, `Specific anti-leishmanial therapy response` | **Target:** `Cutaneous leishmaniasis`, `Visceral leishmaniasis`, `Mucosal leishmaniasis` (`result: "CLINICAL_IMPROVEMENT"`) |
| **EXCLUDE — Post-Treatment Clearance & Remote Past** | Post-treatment parasite clearance or remote historical episode (`HISTORICAL_PAST`). **EXCLUDE** clearance tests from diagnostic claims (or mention generally under treatment response) and log in `dropped_specifics`. | `Blood PCR post-treatment` (`result: "PARASITE_CLEARANCE"`), `Post-treatment bone marrow examination` (`result: "NEGATIVE (PARASITE_CLEARANCE)"`), `temporality: "HISTORICAL_PAST"` items when a `CURRENT_EPISODE` relapse item is present | **Target:** `Leishmania DNA`, `Leishmania amastigotes` (post-treatment clearance) |
| **EXCLUDE — Unrelated Context (`E4_CONTEXT`)** | Concurrent unrelated pathology. **EXCLUDE** from Leishmaniasis diagnostic claims and log in `dropped_specifics`. | `Surgical excision histopathology` (`target_concept: "Basal cell carcinoma"`, `relation: "CONTEXTUALIZES"`) | **Target:** `Basal cell carcinoma` |
| **DISCORDANT — Negative Aspirate/Culture (`E0_CONTRADICTED` / `REFUTES`)** | Negative initial bone marrow smear or negative culture when biopsy/PCR/repeat aspirate is positive. Generalize as: *"A negative culture or single negative aspirate does not exclude leishmaniasis when tissue histopathology or PCR demonstrates the parasite."* | `Bone marrow aspiration microscopy` (`result: "NEGATIVE"`, `relation: "REFUTES"`), or negative culture noted in `source_quote` (`"Cultures were negative, but..."`) | **Target:** `LD bodies in bone marrow` |

### 1.2 Compound `test_name` Splitting Rule
In `output_leishmaniasis.jsonl`, several records combine an **E2 serological/skin test** and an **E1 parasitological/PCR test** inside a single `evidence_item`:
- `test_name: "rK39 rapid antigen test and bone marrow examination"` (`PMC5430503_01`)
- `test_name: "rK39 immunochromatography test and bone marrow examination"` (`PMC6850740_02`)
- `test_name: "Anti-Leishmania antibody test and Leishmania PCR"` (`PMC10150918_01`, `PMC9198207_01`)
- `test_name: "Direct parasite search on lesion scraping and Montenegro skin test"` (`PMC5813666_01`)

**Rule:** Unpack compound evidence items into separate generalized claims:
1. **E1 Claim:** Direct visualization of *Leishmania* amastigotes (LD bodies) in tissue/smear (e.g., bone marrow, spleen, lymph node, or skin biopsy), parasite isolation in culture, or species-specific PCR is the definitive gold standard.
2. **E2 Claim:** rK39 rapid immunochromatographic/ELISA testing or IIF serology (for visceral leishmaniasis) or Montenegro intradermal testing (for tegumentary leishmaniasis) provides highly specific supportive evidence that requires clinical/parasitological correlation.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`, `E3`) in `rationale`
In `output_leishmaniasis.jsonl`, all 100 rationales contain parenthetical tier markers. Replace them as follows:
- `(E1 confirmatory)` / `(E1 confirmatory evidence)` / `(E1)` → **`definitive laboratory confirmation`**
- `(E2)` / `(E2 highly specific)` → **`highly specific serological/immunological evidence`**
- `(E3 supportive)` → **`supportive clinical/therapeutic evidence`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Strip all trailing annotation protocol sentences from `rationale`:
- `VPD satisfied -> POSITIVE.`
- `Primary diagnosis confirmed, current episode, primary patient, no contradictions.`

### 2.3 Handle `POSITIVE` Keywords
1. **In `step9_key_evidence` (`result: "POSITIVE"`, `"POSITIVE (1:100)"`, `"POSITIVE (Leishmania major)"`, `"POSITIVE (amastigotes seen; 213,000 Leishmania/ml)"`):**
   - Strip patient-specific quantitative titers (`1:100`, `1:640`), parasite densities (`213,000 Leishmania/ml`, `5+ LD bodies/field`), and exact induration measurements (`6 mm`) from the generalized claim and log them in `dropped_specifics`, while keeping general clinical interpretations (`positive at a significant titer`, `reactive delayed-type hypersensitivity induration ≥5 mm`).
   - Keep species identifications (`Leishmania major`, `Leishmania infantum`, `Leishmania tropica`, `Leishmania braziliensis`, `Leishmania amazonensis`) as part of the generalized pathogen/diagnostic claim.
2. **At the end of `ground_truth_reasoning`:**
   - Replace `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`15-year-old`, `71-year-old`), sex (`male`, `female`), occupation (`farmer`, `agricultural worker`)
   - Specific country, city, or region (`Margarita Island, Venezuela`, `Georgia`, `Algeria`, `Amazon`)
   - Exact antibody titer in this patient (`"1:100"`, `"1:80"`, `"1:640"`)
   - Exact qPCR parasite load or amastigote count in this patient (`"29.8 Leishmania/ml"`, `"213,000 Leishmania/ml"`, `"6723 parasites/microg"`)
   - Exact lesion count or organ measurement in this patient (`"25 lesions"`, `"20 cm spleen"`)
   - Exact reagent percentages in laboratory preparation (`"10% Giemsa"`, `"10% FBS"`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Standard diagnostic cutoffs (`"Montenegro skin test induration ≥5 mm is considered positive"`, `"DAT titer ≥1:1600 or ≥1:3200 threshold"`)
   - Canonical gene targets (`"ITS1 rRNA"`, `"kDNA"`, `"18S rRNA"`) and standard culture media (`"RPMI-1640"`, `"NNN medium"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"1:100 rK39 / IIF titer"` → `"positive at a significant titer"`
   - `"20 cm spleen"` → `"massive splenomegaly"`
   - `"25 ulcerative/crusted lesions"` → `"multiple disseminated ulcerative and crusted cutaneous lesions"`

### 3.2 Domain-Specific Clinical Generalizations
- **Specify the Clinical Form in the Disease Header:**
  - Visceral leishmaniasis: `"Visceral leishmaniasis (kala-azar), caused by Leishmania donovani complex / Leishmania infantum. Reasoning: ..."`
  - Cutaneous leishmaniasis: `"Cutaneous leishmaniasis, caused by Leishmania <species>. Reasoning: ..."`
  - Mucocutaneous / Tegumentary leishmaniasis: `"Mucocutaneous (or American tegumentary) leishmaniasis, caused by Leishmania (Viannia) <species>. Reasoning: ..."`
  - Post-kala-azar dermal leishmaniasis: `"Post-kala-azar dermal leishmaniasis (PKDL). Reasoning: ..."`
- **Preserve Immunocompromised Host Context & Standard Treatments:**
  - If the patient is an **HIV co-infected** patient or **solid-organ transplant recipient** with relapsing visceral leishmaniasis, generalize this as a recognized host risk factor (`"Visceral leishmaniasis frequently presents as an opportunistic or relapsing infection in immunocompromised hosts, such as patients with HIV coinfection or organ transplant recipients"`).
  - If anti-leishmanial therapy is stated (`meglumine antimoniate [Glucantime]`, `liposomal amphotericin B`, `miltefosine`, `sodium stibogluconate`), include a generalized treatment claim.

---

## 4. Output Format & Worked Examples

### 4.1 Reference Example 1 — Visceral Leishmaniasis with rK39 (`E2`) & Bone Marrow Biopsy (`E1`) (`PMC8320547_01::Leishmaniasis`)

**INPUT (from `selected_case/output_leishmaniasis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "rK39 ELISA serology", result: "POSITIVE (1:100)", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Leishmania antibodies", specimen: "serum", source_quote: "Cultures were negative, but the K-39 ELISA Leishmania titers were positive at 1:100."}`
  - `{test_name: "Bone marrow biopsy histopathology", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Leishmania donovani amastigotes", specimen: "bone marrow"}`
- `rationale`:
  `"A 15-year-old female presented with prolonged fever, pancytopenia, and massive hepatosplenomegaly. rK39 ELISA was positive (1:100) and bone marrow biopsy showed intracellular colonization by Leishmania donovani amastigotes (E1 confirmatory). Successfully treated with meglumine antimoniate. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Visceral leishmaniasis (kala-azar), caused by Leishmania donovani complex. Reasoning: (1) Prolonged fever, pancytopenia, and massive hepatosplenomegaly are characteristic clinical features of visceral leishmaniasis. (2) Definitive diagnosis requires demonstration of Leishmania amastigotes in tissue (e.g., bone marrow aspirate or biopsy) or culture of the organism; a negative culture does not exclude the diagnosis. (3) rK39 ELISA is a highly specific serological test that supports the diagnosis when positive at a significant titer, though it requires clinical correlation. (4) Treatment with anti-leishmanial agents such as meglumine antimoniate is standard. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Prolonged fever, pancytopenia, and massive hepatosplenomegaly are characteristic clinical features of visceral leishmaniasis.", "source": "rationale"},
    {"text": "Definitive diagnosis requires demonstration of Leishmania amastigotes in tissue (e.g., bone marrow aspirate or biopsy) or culture of the organism; a negative culture does not exclude the diagnosis.", "source": "step9"},
    {"text": "rK39 ELISA is a highly specific serological test that supports the diagnosis when positive at a significant titer, though it requires clinical correlation.", "source": "step9"},
    {"text": "Treatment with anti-leishmanial agents such as meglumine antimoniate is standard.", "source": "rationale"}
  ],
  "dropped_specifics": ["15-year-old female", "Margarita Island, Venezuela", "exact patient 1:100 titer (converted to positive at a significant titer)", "specific amastigote count", "negative culture (kept as general 'negative culture does not exclude')"]
}
```

### 4.2 Worked Example 2 — Cutaneous Leishmaniasis with Smear Microscopy (`E1`) & Species PCR (`E1`) (`PMC5292196_01::Leishmaniasis`)

**INPUT (from `selected_case/output_leishmaniasis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Giemsa stain microscopic examination of skin lesion smear", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Leishmania amastigotes", specimen: "skin scraping smear"}`
  - `{test_name: "PCR for Leishmania species identification", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Leishmania major", specimen: "skin lesion culture"}`
- `rationale`:
  `"A 75-year-old male farmer presented with multiple ulcerative and nodular cutaneous lesions including the upper eyelid. Giemsa staining of direct smears demonstrated Leishmania amastigotes, and culture-extracted DNA PCR was positive for Leishmania major (E1 confirmatory). VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Cutaneous leishmaniasis, caused by Leishmania major. Reasoning: (1) Cutaneous leishmaniasis typically presents with chronic ulcerative, crusted, or nodular skin lesions, which can occasionally involve ocular/periocular structures such as the eyelid. (2) Direct parasitological demonstration of Leishmania amastigotes on Giemsa-stained smears of skin lesion scrapings provides definitive diagnostic confirmation. (3) Parasite culture (e.g., in RPMI-1640 medium) and molecular testing by PCR enable definitive species-level identification of Leishmania major. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Cutaneous leishmaniasis typically presents with chronic ulcerative, crusted, or nodular skin lesions, which can occasionally involve ocular/periocular structures such as the eyelid.", "source": "rationale"},
    {"text": "Direct parasitological demonstration of Leishmania amastigotes on Giemsa-stained smears of skin lesion scrapings provides definitive diagnostic confirmation.", "source": "step9"},
    {"text": "Parasite culture (e.g., in RPMI-1640 medium) and molecular testing by PCR enable definitive species-level identification of Leishmania major.", "source": "step9"}
  ],
  "dropped_specifics": ["75-year-old male farmer", "exact count of 25 ulcerative/crusted skin lesions (kept 'multiple ulcerative and nodular lesions')", "10% Giemsa and 10% FBS laboratory preparation concentrations", "Figure 2 and Figure 3 references"]
}
```

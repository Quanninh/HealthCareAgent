---
name: gt-reasoning-brucellosis
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Brucellosis cases in selected_case/output_brucellosis.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate
  from rationale, normalizing POSITIVE keywords, and generalizing case-specific
  details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Brucellosis

## Target Disease & Data Scope
- **Target Disease:** `Brucellosis` (*Brucella melitensis*, *Brucella abortus*, *Brucella suis*, *Brucella canis*, or *Brucella* spp. infection)
- **Source File:** `selected_case/output_brucellosis.jsonl` (100 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-brucellosis/SKILL.md` (`03_evidence_specificity_matrix.md` §5.6)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_brucellosis.jsonl`

| Tier in `skills/disease-agent-brucellosis` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_brucellosis.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY`)** | Definitive microbiological isolation/culture of *Brucella* spp. from blood, bone marrow, or sterile tissue/fluid, or validated pathogen-specific molecular detection (PCR / 16S rRNA / MALDI-TOF / mNGS) | **Culture:** `Blood culture`, `Bone marrow culture`, `Culture of blood and bursa aspirates`, `Vertebral tissue aspirate culture`, `Tissue culture and reference laboratory confirmation`, `Pus/curettage culture`, `Synovial fluid culture`, `CSF culture`<br>**Molecular:** `Real-time PCR`, `Real-time PCR for Brucella`, `Bone marrow RNA 16S molecular test`, `Blood/bone marrow culture and real-time PCR`<br>**Compound Culture + Serology:** `Blood culture and Serum Agglutination Test`, `Blood microbial culture and agglutination test`, `Blood culture and tube agglutination test`, `Blood culture and tube agglutination` | **Target:** `Brucella melitensis`, `Brucella abortus`, `Brucella suis`, `Brucella canis`, `Brucella spp.`, `Brucella species`, `Brucella`<br>**Specimen:** `blood`, `bone marrow`, `CSF`, `vertebral tissue aspirate`, `periprosthetic hip tissue`, `olecranon bursa aspirate`, `canalicular discharge/curettage`, `synovial fluid` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly specific serological evidence (Standard Tube Agglutination / SAT / Wright test, 2-mercaptoethanol [2ME] test, Coombs anti-Brucella test, Rose Bengal Plate Test [RBPT], or Brucella-specific ELISA IgM/IgG/IgA) interpreted in a compatible clinical and epidemiological context | `Brucella serology`, `Brucella agglutination titers`, `Serum Agglutination Test (SAT)`, `Standard tube agglutination (STA)`, `Wright's agglutination test`, `Wright and 2ME agglutination tests`, `Direct Coombs / Brucella micro agglutination test`, `Brucella tube agglutination (Coombs/capt test)`, `Rose Bengal Plate Test and Serum Agglutination Test`, `Rose Bengal test (RBT) and Serum Agglutination Test (SAT)`, `Rose Bengal test and Wright agglutination test`, `Wright agglutination reaction and Brucella melitensis IgM/IgA`, `Brucella serology (ELISA IgG and Coombs Wright)`, `Serum agglutination test and CSF agglutinin`, `Tiger red plate agglutination and test tube agglutination`, `Brucella antibody titers (Abortus and Melitensis)` | **Target:** `Brucella`, `Brucella sp.`, `Brucella melitensis`, `Brucella abortus and Brucella melitensis`<br>**Specimen:** `serum`, `plasma`, `CSF`, `blood and CSF` |
| **E3 — Supportive (in `rationale`)** | Characteristic clinical syndrome (undulating fever, night sweats, arthralgia/sacroiliitis/spondylodiscitis, hepatosplenomegaly, epididymo-orchitis), elevated inflammatory markers (ESR, CRP), zoonotic/dietary exposure (unpasteurized milk/cheese, livestock/farming contact), and response to prolonged combination anti-Brucella antibiotic therapy | Mentioned in `rationale` and `source_quote` (e.g., unpasteurized goat/camel/cow milk consumption, animal husbandry, doxycycline + rifampicin/streptomycin/gentamicin response) | Clinical syndrome, zoonotic exposure, targeted therapy response |

### 1.2 Compound `test_name` Splitting Rule
In `output_brucellosis.jsonl`, several records bundle a **confirmatory culture (E1)** and a **serological agglutination assay (E2)** into one `evidence_item`, or bundle a **rapid screening agglutination test (Rose Bengal / RBPT)** with a **quantitative tube agglutination test (SAT / Wright / Coombs)**:
- `test_name: "Blood culture and Serum Agglutination Test"` (`PMC6387729_01`)
- `test_name: "Blood microbial culture and agglutination test"` (`PMC9643386_01`)
- `test_name: "Blood culture and tube agglutination test"` (`PMC8710768_01`)
- `test_name: "Rose Bengal Plate Test and Serum Agglutination Test"` (`PMC9969863_01`, `PMC9389076_01`, `PMC5081455_01`)

**Rule:**
1. When **Culture (E1) + Serology (E2)** are bundled together, generate **two separate diagnostic claims**:
   - **E1 Claim:** Isolation of *Brucella* spp. (e.g., *B. melitensis* or *B. abortus*) from blood, bone marrow, or tissue/fluid culture is the definitive gold-standard diagnostic method.
   - **E2 Claim:** Brucella serology (such as the serum/standard tube agglutination test [SAT/Wright] at a significant diagnostic titer or Rose Bengal screening test) provides highly specific serological support for the diagnosis.
2. When **Rose Bengal Plate Test (RBPT) + Tube Agglutination (SAT / Wright / 2ME / Coombs)** are paired (all E2), explain their complementary serological role: RBPT serves as a rapid screening agglutination assay, while quantitative tube agglutination (SAT/Wright, 2ME, or Coombs) confirms anti-*Brucella* antibodies at a significant diagnostic titer.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Two Distinct `rationale` Styles in `output_brucellosis.jsonl`
Investigation of `output_brucellosis.jsonl` shows two distinct formats across the 100 rows:
- **Rows 1–45:** Multi-sentence rationales ending with `E1/E2 evidence ... satisfies VPD -> POSITIVE.` (e.g., `"E2 evidence in a current primary episode satisfies VPD -> POSITIVE."`, `"E1 confirmatory culture evidence satisfies VPD -> POSITIVE."`, `"E2 serologic evidence satisfies VPD -> POSITIVE."`).
- **Rows 46–100:** Concise single-sentence rationales without `VPD` or `POSITIVE` (e.g., `"58-year-old male farmer with suppurative canaliculitis whose curettage material isolated Brucella melitensis."`, `"32-year-old male presenting with paraparesis and acute transverse myelitis whose real-time PCR for Brucella was positive."`).

### 2.2 Replace Encoded Tier Keywords (`E1`, `E2`) & Strip `VPD`
- Strip all trailing VPD validation sentences:
  - `E1 evidence satisfies VPD -> POSITIVE.`
  - `E2 evidence in a current primary episode satisfies VPD -> POSITIVE.`
  - `E2 serologic evidence satisfies VPD -> POSITIVE.`
  - `E1 confirmatory culture/lab evidence satisfies VPD -> POSITIVE.`
- Replace any inline `E1` with **`definitive microbiological/molecular confirmation`** and `E2` with **`highly specific serological evidence`**.

### 2.3 Expand Concise Single-Sentence Rationales (Rows 46–100)
For rows where `rationale` is a single brief sentence (e.g., `"58-year-old male farmer with suppurative canaliculitis whose curettage material isolated Brucella melitensis"`), inspect `step9_key_evidence.evidence_items[].source_quote`, `test_name`, `specimen`, and `target_concept` to construct a complete set of generalized claims:
1. Etiology / focal presentation or complication claim
2. Definitive E1 or E2 diagnostic method claim
3. Epidemiological exposure (e.g., farming/livestock contact or unpasteurized dairy) or treatment claim if present in `rationale` or `source_quote`.

### 2.4 Handle `POSITIVE` Keywords
- Convert `result: "POSITIVE"` in `step9_key_evidence` into generalized diagnostic principles.
- Always conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.` (even for rows 46–100 where `-> POSITIVE.` was omitted from the raw `rationale`).

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`74-year-old`, `9-year-old`, `58-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution (`local Centers for Disease Control`)
   - Hospitalization day (`"on day 3"`), time since exposure (`"50 days ago"`), culture incubation time (`"after 8 days of blood culture"`, `"72 h incubation"`)
   - Exact titer in this patient (`"1:160"`, `"1:100 (++)"`, `"1:320"`, `"1:640"`, `"1:1280"`, `"1:5,120"`, `"1:20,480"`)
   - Exact lab value in this patient (`"ESR 58 mm/hr"`, `"CRP 165.08 mg/dl"`, `"WBC 11,200"`, `"leukocytosis 23.32x10^3/muL"`)
   - Exact drug dose for this patient (`"0.6 g Qd"`, `"0.1 g BID"`)
   - Specific strain/biovar designations when used as patient-specific findings (keep species that generalize, e.g., *Brucella melitensis*, *Brucella abortus*)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Diagnostic thresholds (`"SAT titer ≥1:160 in non-endemic areas or ≥1:320 in endemic areas is considered diagnostic"`, `"titer ≥1:400 is significant"`)
   - Seroconversion rules (`"≥4-fold rise in paired sera is diagnostic"`)
   - Duration rules (`"6-week doxycycline-based combination regimen"`)
   - Clinical definitions (`"fever >38.3°C"`, `"thrombocytopenia <150,000/µL"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"CRP 165.08 mg/dl"` → `"markedly elevated CRP indicates systemic inflammation"`
   - `"ESR 58 mm/hr"` → `"elevated ESR supports an inflammatory process"`
   - `"1:160"` / `"1:320"` → `"positive at a significant titer"` OR `"positive at a titer consistent with the diagnostic threshold"`
   - `"0.6 g Qd rifampin and 0.1 g BID doxycycline"` → `"doxycycline- and rifampin-based combination regimen"`

### 3.2 Domain-Specific Clinical Generalizations
- **Epidemiological Exposure:** Generalize specific animal/food mentions (`drinking unpasteurized goat milk`, `farmer`, `shepherd`) into: *"Brucellosis is a zoonotic infection commonly transmitted through consumption of unpasteurized dairy products or direct contact with infected livestock."*
- **Focal Organ Involvement & Complications:** State focal osteoarticular (spondylodiscitis, sacroiliitis, septic arthritis/bursitis), neurological (neurobrucellosis, transverse myelitis, meningoencephalitis), genitourinary (epididymo-orchitis), cardiovascular (endocarditis), or autoimmune/hematologic manifestations (P-ANCA vasculitis, secondary ITP/TTP) as recognized manifestations or complications of brucellosis.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Serologically Confirmed Brucellosis (`E2`) with Inflammatory Markers (`PMC8639279_01::Brucellosis`)

**INPUT (from `selected_case/output_brucellosis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Brucella serology", result: "POSITIVE", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Brucella abortus and Brucella melitensis", specimen: "serum", source_quote: "Laboratory investigations revealed positive serology for Brucella abortus and Brucella melitensis, elevated erythrocyte sedimentation rate (ESR) (58 mm/hr), C-reactive protein (CRP) (165.08 mg/dl), and leukocytosis (23.32x103/muL)."}`
- `rationale`:
  `"A 74-year-old male presented with fever, night sweats, fatigability, and history of unpasteurized milk consumption. Serology was positive for Brucella abortus and Brucella melitensis, leading to treatment with doxycycline and rifampin, followed by secondary P-ANCA vasculitis. E2 evidence in a current primary episode satisfies VPD -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Brucellosis (Brucella abortus / Brucella melitensis infection). Reasoning: (1) Prolonged fever, night sweats, and constitutional fatigue in a patient with a history of unpasteurized dairy consumption are classic clinical and epidemiological features of brucellosis, supported by elevated inflammatory markers (elevated ESR, markedly elevated CRP, and leukocytosis indicating systemic inflammation). (2) Positive Brucella-specific serology (detecting antibodies against Brucella abortus and Brucella melitensis) provides highly specific diagnostic evidence in a compatible clinical setting. (3) Secondary autoimmune phenomena such as P-ANCA vasculitis are recognized complications of brucellosis. (4) Standard antimicrobial treatment consists of a combination regimen with doxycycline and rifampin (typically a 6-week doxycycline-based regimen). -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Prolonged fever, night sweats, and constitutional fatigue in a patient with a history of unpasteurized dairy consumption are classic clinical and epidemiological features of brucellosis, supported by elevated inflammatory markers (elevated ESR, markedly elevated CRP, and leukocytosis indicating systemic inflammation).", "source": "rationale"},
    {"text": "Positive Brucella-specific serology (detecting antibodies against Brucella abortus and Brucella melitensis) provides highly specific diagnostic evidence in a compatible clinical setting.", "source": "step9"},
    {"text": "Secondary autoimmune phenomena such as P-ANCA vasculitis are recognized complications of brucellosis.", "source": "rationale"},
    {"text": "Standard antimicrobial treatment consists of a combination regimen with doxycycline and rifampin (typically a 6-week doxycycline-based regimen).", "source": "rationale"}
  ],
  "dropped_specifics": ["74-year-old male", "exact patient lab values: ESR 58 mm/hr, CRP 165.08 mg/dl, leukocytosis 23.32x10^3/muL (kept clinical interpretation of elevated ESR, CRP, and leukocytosis)"]
}
```

### 4.2 Worked Example 2 — Compound Blood Culture (`E1`) + Serum Agglutination (`E2`) (`PMC6387729_01::Brucellosis`)

**INPUT (from `selected_case/output_brucellosis.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Blood culture and Serum Agglutination Test", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Brucella melitensis", specimen: "blood", source_quote: "On day 3 of hospitalization, Brucella melitensis was isolated from two consecutive blood cultures. The serum agglutination test (SAT) for Brucella was positive at a titer of 1:320."}`
- `rationale`:
  `"A 45-year-old male shepherd presented with undulating fever, arthralgias, and hepatosplenomegaly. Two consecutive blood cultures isolated Brucella melitensis (E1) and serum agglutination test was positive at 1:320 (E2). Treated successfully with doxycycline and streptomycin. E1 evidence satisfies VPD -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Brucellosis (Brucella melitensis infection). Reasoning: (1) Undulating fever, arthralgias, and hepatosplenomegaly in an individual with occupational livestock exposure are characteristic clinical and epidemiological features of brucellosis. (2) Isolation of Brucella melitensis from blood culture provides definitive microbiological confirmation of brucellosis. (3) A positive Serum Agglutination Test (SAT) at a significant titer consistent with the diagnostic threshold (≥1:160) provides highly specific serological evidence supporting the diagnosis. (4) A doxycycline-based combination antibiotic regimen (e.g., doxycycline with an aminoglycoside such as streptomycin) is standard treatment and typically leads to clinical recovery. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Undulating fever, arthralgias, and hepatosplenomegaly in an individual with occupational livestock exposure are characteristic clinical and epidemiological features of brucellosis.", "source": "rationale"},
    {"text": "Isolation of Brucella melitensis from blood culture provides definitive microbiological confirmation of brucellosis.", "source": "step9"},
    {"text": "A positive Serum Agglutination Test (SAT) at a significant titer consistent with the diagnostic threshold (≥1:160) provides highly specific serological evidence supporting the diagnosis.", "source": "step9"},
    {"text": "A doxycycline-based combination antibiotic regimen (e.g., doxycycline with an aminoglycoside such as streptomycin) is standard treatment and typically leads to clinical recovery.", "source": "rationale"}
  ],
  "dropped_specifics": ["45-year-old male shepherd", "day 3 of hospitalization", "two consecutive cultures count", "exact patient SAT titer 1:320 (converted to significant diagnostic titer)"]
}
```

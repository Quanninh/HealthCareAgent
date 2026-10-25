---
name: gt-reasoning-cholera
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Cholera cases in selected_case/output_cholera.jsonl by decoding E1/E2/E3
  evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate from
  rationale, normalizing POSITIVE keywords, and generalizing case-specific details
  for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Cholera

## Target Disease & Data Scope
- **Target Disease:** `Cholera` (*Vibrio cholerae* infection, particularly toxigenic serogroups O1 [biovar El Tor / Classical; serotypes Inaba / Ogawa] and O139)
- **Source File:** `selected_case/output_cholera.jsonl` (6 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-cholera/SKILL.md` (`03_evidence_specificity_matrix.md` §5.12)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_cholera.jsonl`

| Tier in `skills/disease-agent-cholera` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_cholera.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive microbiological isolation of *Vibrio cholerae* by stool culture (e.g., on TCBS agar), serogrouping/serotyping (O1/O139, El Tor, Inaba/Ogawa) by slide agglutination, or validated molecular detection by PCR (e.g., species-specific PCR or multiplex gastrointestinal PCR panel) | `Stool culture`, `Stool culture and serotyping`, `Stool culture, species-specific PCR, and slide agglutination serotyping`, `BioFire GI PCR panel` | **Target:** `Vibrio cholerae`, `V. cholerae O1 El Tor, subtype Inaba`, `V. cholerae serogroup O1, biovar El Tor, serotype Ogawa`, `Vibrio cholerae DNA`<br>**Specimen:** `stool` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC`)** | Presumptive / rapid diagnostic evidence supporting cholera (immunochromatographic rapid diagnostic test [RDT] detecting *V. cholerae* O1/O139 lipopolysaccharide antigen, or characteristic darting motility on hanging-drop / dark-field stool microscopy); requires confirmation by culture or PCR | `Rapid Diagnostic Test (Crystal VC dipstick)`, `Hanging drop stool microscopy`, `Clinical and infectious disease diagnostic assessment` | **Target:** `Vibrio cholerae lipopolysaccharide antigen`, `Darting motility characteristic of Vibrio cholerae`, `Non-diarrheal cholera masked by bowel obstruction`<br>**Specimen:** `stool` |
| **E3 — Supportive (`E3_SUPPORTIVE`)** | Classic clinical syndrome of profuse secretory ("rice-water") diarrhea, rapid dehydration, hypovolemic shock, metabolic acidosis, acute kidney injury, travel/epidemiological exposure, and response to fluid resuscitation and targeted antibiotics | `Clinical presentation and history`, `Clinical presentation and diarrhea severity`, `Antibiotic therapy completion and clinical outcome` | **Target:** `Acute watery diarrhea and dehydration after Bangladesh travel`, `Profuse watery diarrhea exceeding 40 episodes in 24 hours`, `Completion of antibiotic therapy for cholera with diarrheal resolution` |
| **EXCLUDE — Post-Treatment Clearance (`result = NEGATIVE`)** | Post-treatment microbiological clearance test (**NOT** diagnostic of infection). **EXCLUDE** negative follow-up PCR from diagnostic claims (retain only the positive initial GI PCR and antibiotic treatment response) and log clearance test in `dropped_specifics`. | `Targeted antibiotic therapy and repeat GI PCR clearance` (`result: "NEGATIVE"`, `strength: "E1_CONFIRMATORY"`, `target_concept: "Microbiological clearance of V. cholerae following ciprofloxacin"`, in `PMC10885837_01`) | **Target:** `Microbiological clearance of V. cholerae following ciprofloxacin` |

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`, `E3`) in `rationale`
All 6 rows in `output_cholera.jsonl` contain explicit `E1` markers in `rationale`. Replace them as follows:
- `— providing E1 disease-defining confirmatory laboratory evidence` → **`— providing definitive microbiological confirmation`**
- `establishing E1 laboratory-confirmed cholera` → **`establishing definitive laboratory confirmation of cholera`**
- `(E1 confirmatory evidence)` / `(E1 confirmatory)` → **`(definitive laboratory confirmation)`**
- `(E2)` → **`(rapid presumptive diagnostic evidence)`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
Strip all trailing VPD validation sentences from `rationale`:
- `All criteria for Valid Positive Diagnosis are fully satisfied -> POSITIVE.`
- `VPD criteria are fully satisfied -> POSITIVE.`
- `All criteria for a Valid Positive Diagnosis are met -> POSITIVE.`
- `VPD criteria are satisfied -> POSITIVE.`
- `VPD is fully satisfied -> POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords & Non-Standard `result` Values
- In `output_cholera.jsonl`, `step9_key_evidence` contains `result` values such as `"POSITIVE"`, `"PRESENT"`, `"DIAGNOSED_CHOLERA"`, `"SEVERE_SECRETORY_DIARRHEA"`, `"COMPLETED_TREATMENT"`, and `"NEGATIVE"` (for post-ciprofloxacin clearance in `PMC10885837_01`).
- Translate positive/present diagnostic items into generalized medical principles, exclude the negative post-treatment clearance test from diagnostic claims, and conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`58-year-old`, `31-year-old`, `47-year-old`), sex (`male`, `female`)
   - Specific country, city, or institution (`Pakistan`, `Bangladesh`, `India`, `Doha, Qatar`, `May 2024`)
   - Exact stool episode count or volume in this patient (`"exceeding 40 episodes in 24 hours"` → convert to `"profuse high-frequency secretory watery diarrhea"`)
   - Exact lab values or drug doses for this patient
   - Patient-specific isolate strain codes (`"VF4E2"`), while **keeping** general epidemic serogroup/biovar/serotype classifications (*Vibrio cholerae* serogroup O1 or O139, biovar El Tor, serotype Inaba or Ogawa)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Epidemic serogroup designations (`"Vibrio cholerae serogroup O1 or O139"`)
   - Standard clinical definitions or treatment duration rules

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `">40 episodes of watery diarrhea in 24 hours"` → `"profuse, high-volume secretory ('rice-water') diarrhea leading to rapid severe dehydration"`

### 3.2 Distinguish Screening (RDT / Motility) from Confirmatory (Culture / PCR) Testing
- When both stool RDT (e.g., Crystal VC dipstick) or hanging-drop microscopy (E2) and stool culture/PCR (E1) are present (`PMC6713851_01`, `PMC6713851_02`, `PMC9946370_01`), state that rapid dipstick antigen testing or hanging-drop microscopy provides rapid presumptive screening evidence, while stool culture with serotyping or PCR provides definitive confirmation.

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Cholera with Stool RDT (`E2`) & Stool Culture/Serotyping (`E1`) (`PMC6713851_01::Cholera`)

**INPUT (from `selected_case/output_cholera.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Rapid Diagnostic Test (Crystal VC dipstick)", result: "POSITIVE", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Vibrio cholerae lipopolysaccharide antigen", specimen: "stool"}`
  - `{test_name: "Stool culture and serotyping", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "V. cholerae O1 El Tor, subtype Inaba", specimen: "stool"}`
- `rationale`:
  `"A 58-year-old male returned from Pakistan presenting with classic acute rice-water diarrhea, hypovolemic shock, and acute renal failure. Stool RDT was positive and stool culture confirmed Vibrio cholerae O1 El Tor, subtype Inaba — providing E1 disease-defining confirmatory laboratory evidence. All criteria for Valid Positive Diagnosis are fully satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Cholera (Vibrio cholerae serogroup O1, biovar El Tor, serotype Inaba infection). Reasoning: (1) Classic cholera presents with profuse acute watery ('rice-water') diarrhea following travel to an endemic area, which can rapidly progress to severe dehydration, hypovolemic shock, and acute kidney injury. (2) Stool culture isolating Vibrio cholerae with serogrouping and serotyping (identifying epidemic serogroup O1, biovar El Tor, serotype Inaba) is the definitive gold standard for laboratory confirmation. (3) Rapid immunochromatographic dipstick testing (detecting V. cholerae lipopolysaccharide antigen in stool) provides rapid presumptive evidence that requires confirmation by stool culture or PCR. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Classic cholera presents with profuse acute watery ('rice-water') diarrhea following travel to an endemic area, which can rapidly progress to severe dehydration, hypovolemic shock, and acute kidney injury.", "source": "rationale"},
    {"text": "Stool culture isolating Vibrio cholerae with serogrouping and serotyping (identifying epidemic serogroup O1, biovar El Tor, serotype Inaba) is the definitive gold standard for laboratory confirmation.", "source": "step9"},
    {"text": "Rapid immunochromatographic dipstick testing (detecting V. cholerae lipopolysaccharide antigen in stool) provides rapid presumptive evidence that requires confirmation by stool culture or PCR.", "source": "step9"}
  ],
  "dropped_specifics": ["58-year-old male", "Pakistan travel location", "Crystal VC brand name (generalized to immunochromatographic dipstick RDT)"]
}
```

### 4.2 Worked Example 2 — Cholera Detected by Multiplex GI PCR (`E1`) with Excluded Clearance Test (`PMC10885837_01::Cholera`)

**INPUT (from `selected_case/output_cholera.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "BioFire GI PCR panel", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Vibrio cholerae DNA", specimen: "stool"}`
  - `{test_name: "Clinical and infectious disease diagnostic assessment", result: "DIAGNOSED_CHOLERA", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Non-diarrheal cholera masked by bowel obstruction", specimen: null}`
  - `{test_name: "Targeted antibiotic therapy and repeat GI PCR clearance", result: "NEGATIVE", strength: "E1_CONFIRMATORY", target_concept: "Microbiological clearance of V. cholerae following ciprofloxacin", specimen: "stool"}` ← **EXCLUDE** negative follow-up clearance test
- `rationale`:
  `"A 60-year-old female with metastatic ovarian cancer and malignant bowel obstruction tested positive for Vibrio cholerae on a stool gastrointestinal PCR panel (E1 confirmatory). Although bowel obstruction masked typical watery diarrhea, infectious disease consultation confirmed cholera and treated her with ciprofloxacin, achieving microbiological clearance on repeat testing. VPD criteria are satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Cholera (Vibrio cholerae infection). Reasoning: (1) Definitive diagnosis of cholera can be established by molecular detection of Vibrio cholerae DNA in stool using a multiplex gastrointestinal PCR panel. (2) Mechanical bowel obstruction can mask the classic secretory watery diarrhea of cholera, resulting in an atypical non-diarrheal presentation. (3) Targeted fluoroquinolone-based antimicrobial therapy (e.g., ciprofloxacin) is effective in eradicating Vibrio cholerae infection. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Definitive diagnosis of cholera can be established by molecular detection of Vibrio cholerae DNA in stool using a multiplex gastrointestinal PCR panel.", "source": "step9"},
    {"text": "Mechanical bowel obstruction can mask the classic secretory watery diarrhea of cholera, resulting in an atypical non-diarrheal presentation.", "source": "rationale"},
    {"text": "Targeted fluoroquinolone-based antimicrobial therapy (e.g., ciprofloxacin) is effective in eradicating Vibrio cholerae infection.", "source": "rationale"}
  ],
  "dropped_specifics": ["60-year-old female", "metastatic ovarian cancer", "BioFire brand name (generalized to multiplex GI PCR panel)", "negative repeat GI PCR clearance test (excluded: target_concept = clearance, not diagnosis)"]
}
```

---
name: gt-reasoning-typhoid_fever
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Typhoid Fever cases in selected_case/output_typhoid_fever.jsonl by decoding
  E1/E2/E3 evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate
  from rationale, normalizing POSITIVE keywords, and generalizing case-specific
  details for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Typhoid Fever

## Target Disease & Data Scope
- **Target Disease:** `Typhoid_Fever` (*Typhoid fever / Enteric fever caused by Salmonella enterica serovar Typhi*)
- **Source File:** `selected_case/output_typhoid_fever.jsonl` (31 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-typhoid_fever/SKILL.md` (`03_evidence_specificity_matrix.md` §5.9)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`, `E3`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_typhoid_fever.jsonl`

| Tier in `skills/disease-agent-typhoid_fever` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_typhoid_fever.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | Definitive microbiological confirmation by isolation/culture of *Salmonella enterica* serovar Typhi from blood, bone marrow, or other sterile/clinical sites (bone marrow culture is more sensitive than blood culture, especially after antibiotic exposure) | `Blood culture`, `Aerobic and anaerobic blood culture`, `Blood and bone marrow culture`, `Blood and stool culture`, `Stool culture`, `Quantitative urine culture`, `Hip joint pus aspiration culture and serological typing`, `Neck lymph node cystic fluid culture`, `Pleural fluid culture and serotyping`, `Blood and liver abscess drainage fluid culture / MALDI-TOF MS`, `Blood culture and eviscerated tissue culture / 16S rRNA PCR`, `Blood culture and Widal test` | **Target:** `Salmonella enterica serovar Typhi`<br>**Specimen:** `blood`, `bone marrow`, `stool / feces`, `urine`, `synovial fluid / pus`, `pleural fluid / pus`, `liver abscess fluid`, `cystic fluid from cervical lymph node mass`, `ocular eviscerated tissue` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC` / `E2_HIGHLY_SPECIFIC_CLINICAL`)** | Highly specific surgical/histopathological hallmark of typhoid intestinal perforation (antimesenteric terminal ileal/jejunal perforation with Peyer's patch inflammation and erythrophagocytic Mallory histiocytes) or targeted molecular/NGS identification | `Exploratory laparotomy`, `Emergency exploratory laparotomy`, `Histopathology of resected ileum`, `Next-generation sequencing and PCR verification` | **Target:** `Perforated typhoid enteritis`, `Typhoid bowel perforation`, `Typhoid ileal perforation with Peyer patch phagocytic histiocytes`, `Salmonella enterica serovar Typhi`<br>**Specimen:** `terminal ileum`, `jejunum / bowel`, `ileum / Peyer patches`, `vertebral abscess tissue` |
| **E3 / E0 — Weak / Supportive Serology (`E3_SUPPORTIVE`)** | Nonspecific/supportive serological evidence (Widal test / Gruber-Widal agglutination has high false-positive rates and cannot confirm typhoid fever alone without culture or surgical/clinical confirmation) | `Salmonella serology`, `Widal test` (when bundled in `Blood culture and Widal test` or mentioned in `rationale` as `Gruber-Widal serology`) | **Target:** `Salmonella enterica serovar Typhi`<br>**Specimen:** `serum` |

### 1.2 Special Anomalies & Compound `test_name` Rules in `output_typhoid_fever.jsonl`
1. **Compound `Blood culture and Widal test` (`PMC10233606_01`) or Widal mentioned in `rationale` (`PMC4137699_01`):**
   - Separate the roles clearly: Blood/urine culture isolation of *S. Typhi* is the **definitive diagnostic confirmation (E1)**, whereas the Widal/Gruber-Widal serological test is **supportive/nonspecific (E3/E0)** due to limited specificity.
2. **Compound `Blood and bone marrow culture` (`PMC6282142_01`):**
   - State the clinical diagnostic principle: *"Isolation of S. typhi from blood or bone marrow culture is the definitive diagnostic method; bone marrow culture is more sensitive than blood culture."*
3. **Discharge Clearance Quote Anomaly (`PMC5832104_01`):**
   - In `PMC5832104_01`, `test_name` is `"Blood and stool culture"` (`result: "POSITIVE"`, `strength: "E1_CONFIRMATORY"`), but `source_quote` captured the discharge sentence (`"A repeat blood and faeces culture performed on discharge was negative for Salmonella enterica serovar Typhi."`).
   - **Rule:** Use the `rationale` (`"Culture yielded extended-spectrum beta-lactamase-producing Salmonella enterica serovar Typhi"`) and `test_name` to formulate the positive diagnostic culture claim, and **exclude** the negative discharge clearance culture (logging it in `dropped_specifics`).
4. **Serovar Typhimurium vs. Typhi in `source_quote` (`PMC11362080_01`):**
   - In `PMC11362080_01`, `target_concept` is normalized to `Salmonella enterica serovar Typhi` while `rationale` and `source_quote` describe vertebral osteomyelitis confirmed by metagenomic next-generation sequencing (mNGS) and PCR verification. Frame the claim around molecular/mNGS and PCR identification of *Salmonella enterica* in vertebral abscess tissue.

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
In `output_typhoid_fever.jsonl`, 27/31 rows contain `— E1 confirmatory lab evidence`, `— E1 confirmatory lab finding`, or `— E1 confirmatory`. Replace them as follows:
- `— E1 confirmatory lab evidence` / `— E1 confirmatory lab finding` / `— E1 confirmatory` → **`— definitive laboratory confirmation`**
- `E2_HIGHLY_SPECIFIC_CLINICAL` → **`characteristic surgical/histopathological confirmation`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
All 31 rows in `output_typhoid_fever.jsonl` end with a two-sentence schema dump. Strip **both** sentences completely:
- `Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS.` (29 rows)
- `Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role COMORBIDITY.` (2 rows)
- `VPD satisfied -> POSITIVE.` (31 rows)

### 2.3 Handle `POSITIVE` Keywords
1. **In `step9_key_evidence` (`result: "POSITIVE"`):**
   - Translate `result: "POSITIVE"` into a generalized statement of microbiological isolation (`"Isolation of S. typhi from blood/bone marrow/sterile-site culture is the definitive diagnostic method"`) or surgical pathology confirmation (`"Antimesenteric perforation of the terminal ileum or jejunum with Peyer's patch inflammation is a classic surgical and histopathological hallmark of complicated typhoid enteritis"`).
2. **At the end of `ground_truth_reasoning`:**
   - Replace `-> POSITIVE.` with `-> POSITIVE diagnosis confirmed.`

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`8-year-old`, `4-year-old`, `86-year-old`), sex (`male`, `female`)
   - Specific country, city, or hospital (`Colombia`, `Benin`, `Nigeria`, `Pakistan`, `Cameroon`, `Yuhuangding Hospital`)
   - Hospitalization day or incubation time in this patient (`"fourth day of hospitalization"`, `"72 hours later"`)
   - Exact colony count, fluid volume, or perforation count in this patient (`"10^3 - 10^4 CFU/mL"`, `"600 ml peritoneal fluid"`, `"15 ileal perforations"`)
   - Exact lab values or individual drug doses in this patient

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - Disease-defining serovar (`Salmonella enterica serovar Typhi` — this defines typhoid fever itself)
   - Canonical gene targets (`16S rRNA`) or antibiotic classes (`third-generation cephalosporins`)
   - Standard clinical definitions (`"stepwise fever >39–40°C"`, `"intestinal perforation typically occurring in the 2nd–3rd week of untreated illness"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"15 ileal perforations"` → `"single or multiple antimesenteric perforations of the terminal ileum causing acute peritonitis"`
   - `"10^3 - 10^4 CFU/mL in urine culture"` → `"significant Salmonella Typhi bacteriuria on quantitative urine culture"`

### 3.2 Domain-Specific Clinical Generalizations
- **Always Include Pathogen Etiology Claim:** Start with `"Typhoid fever (Salmonella enterica serovar Typhi infection). Reasoning: (1) Typhoid fever is caused by Salmonella enterica serovar Typhi..."`
- **Generalize Recognized Complications & Extraintestinal Focal Infections:**
  - *Hematologic:* Secondary hemophagocytic lymphohistiocytosis (HLH), pancytopenia, leukopenia.
  - *Gastrointestinal/Surgical:* Antimesenteric ileal or jejunal perforation with peritonitis, acute acalculous cholecystitis, lower gastrointestinal bleeding, acute pancreatitis and hepatitis, hepatic/splenic abscess.
  - *Cardiovascular/Neurologic/Sensory:* Relative bradycardia or marked sinus bradycardia, acute sensorineural hearing loss, endophthalmitis.
  - *Musculoskeletal/Other:* Septic arthritis (e.g., hip joint in SLE), pyomyositis and osteomyelitis, infected branchial/cervical cystic mass.
- **Generalize Antibiotic Therapy & Resistance Patterns:** *"Treatment with appropriate antibiotics (such as third-generation cephalosporins like ceftriaxone, fluoroquinolones like ciprofloxacin, azithromycin, or carbapenems such as meropenem/imipenem for multidrug-resistant or ESBL-producing strains) typically results in clinical resolution."*

---

## 4. Output Format & Worked Examples

### 4.1 Reference Example 1 — Typhoid Fever with Blood & Bone Marrow Culture (`E1`) and HLH (`PMC6282142_01::Typhoid_Fever`)

**INPUT (from `selected_case/output_typhoid_fever.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Blood and bone marrow culture", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Salmonella enterica serovar Typhi", specimen: "blood and bone marrow", source_quote: "On the fourth day of hospitalization, both blood and bone marrow cultures were positive for Salmonella typhi"}`
- `rationale`:
  `"An 8-year-old female presented with fever, pancytopenia, and hemophagocytic lymphohistiocytosis. Both blood and bone marrow cultures isolated Salmonella typhi — E1 confirmatory lab evidence. Following ciprofloxacin therapy, typhoid fever and HLH completely resolved. Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Typhoid fever (Salmonella enterica serovar Typhi infection). Reasoning: (1) Typhoid fever is caused by Salmonella enterica serovar Typhi. (2) Isolation of S. typhi from blood or bone marrow culture is the definitive diagnostic method; bone marrow culture is more sensitive than blood culture. (3) Secondary hemophagocytic lymphohistiocytosis (HLH) is a recognized complication of typhoid fever. (4) Treatment with appropriate antibiotics (e.g., ciprofloxacin) typically results in resolution. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Typhoid fever is caused by Salmonella enterica serovar Typhi.", "source": "step9"},
    {"text": "Isolation of S. typhi from blood or bone marrow culture is the definitive diagnostic method; bone marrow culture is more sensitive than blood culture.", "source": "step9"},
    {"text": "Secondary hemophagocytic lymphohistiocytosis (HLH) is a recognized complication of typhoid fever.", "source": "rationale"},
    {"text": "Treatment with appropriate antibiotics (e.g., ciprofloxacin) typically results in resolution.", "source": "rationale"}
  ],
  "dropped_specifics": ["8-year-old female", "Colombia", "day 4 of hospitalization", "specific pancytopenia values", "complete resolution timeline"]
}
```

### 4.2 Worked Example 2 — Surgical/Histopathological Typhoid Ileal Perforation (`E2`) (`PMC5753017_01::Typhoid_Fever`)

**INPUT (from `selected_case/output_typhoid_fever.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Histopathology of resected ileum", result: "POSITIVE", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Typhoid ileal perforation with Peyer patch phagocytic histiocytes", specimen: "ileum / Peyer patches"}`
- `rationale`:
  `"An 86-year-old male presented with peritonitis due to 15 ileal perforations. Histopathological analysis of the resected ileum confirmed chronic inflammation of Peyer's patches with diffuse aggregates of pale histiocytes exhibiting phagocytic characteristics (Mallory cells), confirming typhoid fever perforation. Assertion CONFIRMED_PRESENT, temporality CURRENT_EPISODE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied -> POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Typhoid fever (Salmonella enterica serovar Typhi enteritis with ileal perforation). Reasoning: (1) Single or multiple intestinal perforations of the terminal ileum resulting in acute peritonitis are a severe surgical complication of typhoid fever. (2) Histopathological demonstration of chronic inflammation of Peyer's patches with aggregates of enlarged phagocytic histiocytes (Mallory cells) in resected ileal tissue provides highly specific pathological confirmation of typhoid enteritis perforation. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Single or multiple intestinal perforations of the terminal ileum resulting in acute peritonitis are a severe surgical complication of typhoid fever.", "source": "rationale"},
    {"text": "Histopathological demonstration of chronic inflammation of Peyer's patches with aggregates of enlarged phagocytic histiocytes (Mallory cells) in resected ileal tissue provides highly specific pathological confirmation of typhoid enteritis perforation.", "source": "step9"}
  ],
  "dropped_specifics": ["86-year-old male", "exact count of 15 ileal perforations (converted to single or multiple terminal ileal perforations)"]
}
```

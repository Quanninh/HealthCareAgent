---
name: gt-reasoning-extractor-finetune
description: Master coordinator and universal rulebook for transforming clinical annotation JSONL records in selected_case_ft_pofs/ into clean, self-contained, generalized ground-truth clinical reasoning JSONL outputs for LLM fine-tuning across two target classes: POSITIVE (one of the 15 target diseases) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE).
---

# Ground-Truth Clinical Reasoning Extractor — Fine-Tuning Coordinator (`selected_case_ft_pofs/`)

## 1. Objective & Fine-Tuning Task Framing

This skill defines the universal transformation rules, output schema, label-normalization logic, and validation gates for converting clinical annotation records in `selected_case_ft_pofs/output_{disease}.jsonl` into structured ground-truth clinical reasoning targets (`output/gt_reasoning_{disease}.jsonl` or fine-tuning target files).

### Fine-Tuning Question–Answer Paradigm
- **Input Question (at training/inference time):** Given the patient's symptoms, clinical history, physical examination, imaging, and laboratory test results, which disease does this patient have?
- **Desired Target Output (`ground_truth_reasoning`):** `<Disease Name or OUT_OF_SCOPE> + <Step-by-step clinical reasoning>`.
- **Dual Case Types in `selected_case_ft_pofs/` (`5,308` total cases across 15 files):**
  1. **`POSITIVE` (`3,617` cases):** Raw `step12_dataset_label == "POSITIVE"` (and `_provenance.validated_label == "POSITIVE"`, `step11_vpd_satisfied == true`). The patient has an active, verified case of the target disease within the 15 selected infectious diseases.
     - **Target `dataset_label`:** `"POSITIVE"`
     - **Target Header:** `"<Disease Name> (<pathogen or specific clinical entity>)."`
     - **Target Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`
  2. **`NEGATIVE` (`664` cases) and `EXCLUDED_NON_TARGET_CASE` (`1,027` cases) → Rewritten into `OUT_OF_SCOPE` (`1,691` cases):** Raw `step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` (and `_provenance.validated_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}`, `step11_vpd_satisfied == false`). In `selected_case_ft_pofs/`, the dataset has been pre-filtered such that every `NEGATIVE` and `EXCLUDED_NON_TARGET_CASE` record represents a patient who does **not** have the target disease (nor any of the 15 target diseases), but instead has a condition or clinical context **outside the 15 selected diseases (`OUT_OF_SCOPE`)**.
     - **Target `dataset_label`:** `"OUT_OF_SCOPE"` *(both `NEGATIVE` and `EXCLUDED_NON_TARGET_CASE` MUST be rewritten to `"OUT_OF_SCOPE"`)*
     - **Target Header:** `"OUT_OF_SCOPE (<Alternative/Non-Target Condition or Clinical Context — Not <Target Disease>>)."`
     - **Target Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### Design Principles
1. **Self-Contained:** The reader never sees the source JSONL or raw PMC article. Every claim must stand alone as complete medical prose without deictic references (`"the patient"`, `"this test"`, `"the above"`, `"in this case"`).
2. **Generalized (The "Guideline Test"):** Strip patient-specific noise (ages, sex, dates, geographic locations, vital signs, raw lab numbers, drug dosages) while preserving disease-defining clinical reasoning, qualitative interpretations (`"elevated"`, `"severely reduced"`), diagnostic thresholds (`"SAT titer >= 1:160"`, `"CD4 count < 200 cells/mm3"`), and definitive microbiological/diagnostic test results.
3. **Zero Pipeline Jargon:** Strip all internal annotation codes (`VPD`, `E0`–`E4`, `C1_DEFINITIVE_REFUTING`, `F1`–`F6` failure flags, `CONFIRMED_PRESENT`, `ABSENT_NEGATIVE`, `RULED_OUT_DIAGNOSIS`, `EXCLUDED_NON_TARGET_CASE`, `Assigned NEGATIVE`, etc.).
4. **Zero Hallucination:** Derive all claims strictly from the record's `rationale`, `step9_key_evidence.evidence_items`, `step5_concept_grounding`, and `step3_patient_anchor`. Never invent clinical findings, assays, or alternative diagnoses not grounded in the record.

---

## 2. Per-Disease Skill Routing Table (`selected_case_ft_pofs/`)

When processing a specific disease file `selected_case_ft_pofs/output_{disease}.jsonl`, load **both** this master coordinator skill and the corresponding disease-specific skill in `skills/finetune/`:

| Target Disease Key | Input JSONL (`selected_case_ft_pofs/`) | Total | `POSITIVE` | `OUT_OF_SCOPE` (Total) | Raw `NEGATIVE` | Raw `EXCLUDED_NON_TARGET_CASE` | Disease Skill Directory (`skills/finetune/`) |
| :--- | :--- | ---: | ---: | ---: | ---: | ---: | :--- |
| `Brucellosis` | `output_brucellosis.jsonl` | 45 | 13 | 32 | 3 | 29 | `gt-reasoning-brucellosis` |
| `Chikungunya` | `output_chikungunya.jsonl` | 2 | 0 | 2 | 2 | 0 | `gt-reasoning-chikungunya` |
| `Cholera` | `output_cholera.jsonl` | 12 | 0 | 12 | 1 | 11 | `gt-reasoning-cholera` |
| `COVID-19` | `output_covid_19.jsonl` | 2,649 | 1,777 | 872 | 332 | 540 | `gt-reasoning-covid_19` |
| `Dengue` | `output_dengue.jsonl` | 33 | 19 | 14 | 5 | 9 | `gt-reasoning-dengue` |
| `Ebola_Filovirus` | `output_ebola_filovirus.jsonl` | 22 | 0 | 22 | 0 | 22 | `gt-reasoning-ebola_filovirus` |
| `HIV_AIDS` | `output_hiv_aids.jsonl` | 1,134 | 828 | 306 | 224 | 82 | `gt-reasoning-hiv_aids` |
| `Leishmaniasis` | `output_leishmaniasis.jsonl` | 30 | 20 | 10 | 2 | 8 | `gt-reasoning-leishmaniasis` |
| `Leptospirosis` | `output_leptospirosis.jsonl` | 8 | 0 | 8 | 7 | 1 | `gt-reasoning-leptospirosis` |
| `Malaria` | `output_malaria.jsonl` | 114 | 18 | 96 | 6 | 90 | `gt-reasoning-malaria` |
| `Rabies` | `output_rabies.jsonl` | 12 | 0 | 12 | 0 | 12 | `gt-reasoning-rabies` |
| `Tuberculosis` | `output_tuberculosis.jsonl` | 1,227 | 942 | 285 | 78 | 207 | `gt-reasoning-tuberculosis` |
| `Typhoid_Fever` | `output_typhoid_fever.jsonl` | 10 | 0 | 10 | 2 | 8 | `gt-reasoning-typhoid_fever` |
| `Yellow_Fever` | `output_yellow_fever.jsonl` | 4 | 0 | 4 | 0 | 4 | `gt-reasoning-yellow_fever` |
| `Zika` | `output_zika.jsonl` | 6 | 0 | 6 | 2 | 4 | `gt-reasoning-zika` |
| **TOTAL** | **15 JSONL files** | **5,308** | **3,617** | **1,691** | **664** | **1,027** | **15 Per-Disease Skills** |

---

## 3. Target Output Schema (`output/gt_reasoning_{disease}.jsonl`)

Every record in `selected_case_ft_pofs/output_{disease}.jsonl` produces **one JSON object per line** in the output JSONL file:

```json
{
  "pair_id": "PMC11835056_01::Brucellosis",
  "case_id": "PMC11835056_01",
  "target_disease": "Brucellosis",
  "dataset_label": "POSITIVE | OUT_OF_SCOPE",
  "ground_truth_reasoning": "<Header>. Reasoning: (1) <claims[0].text> (2) <claims[1].text> ... -> <POSITIVE | OUT_OF_SCOPE> diagnosis confirmed.",
  "claims": [
    {"text": "<Self-contained clinical claim — ends with period, never starts with (N)>", "source": "rationale | step9 | both | step5"}
  ],
  "dropped_specifics": [
    "<raw_value> — <category or conversion/exclusion note>"
  ]
}
```

### Mechanical Assembly Contract (`ground_truth_reasoning` ↔ `claims`)
`ground_truth_reasoning` is **mechanically assembled** from the header, `claims[]`, and the label-specific concluding suffix:

1. **For `POSITIVE` cases (`dataset_label == "POSITIVE"`):**
   ```text
   <Disease Name> (<pathogen/clinical entity>). Reasoning: (1) <claims[0].text> (2) <claims[1].text> ... -> POSITIVE diagnosis confirmed.
   ```
2. **For `OUT_OF_SCOPE` cases (`dataset_label == "OUT_OF_SCOPE"`, rewritten from raw `NEGATIVE` or `EXCLUDED_NON_TARGET_CASE`):**
   ```text
   OUT_OF_SCOPE (<Alternative/Non-Target Condition or Clinical Context — Not <Target Disease>>). Reasoning: (1) <claims[0].text> (2) <claims[1].text> ... -> OUT_OF_SCOPE diagnosis confirmed.
   ```
3. **Strict Synchronization:**
   - Every `claims[i].text` must appear **verbatim** inside `ground_truth_reasoning` immediately after `(i+1) `.
   - `claims[i].text` **never** starts with a number prefix `(1)` and **always** ends with a single period `.`.
   - `source` for each claim must be one of `{"rationale", "step9", "both", "step5"}` (when patient-anchor context from `step3_patient_anchor` is folded in to disambiguate a template rationale, record `"step5"` or `"rationale"`).

---

## 4. Universal Input Schema & Field Inspection (`selected_case_ft_pofs/`)

In `selected_case_ft_pofs/output_{disease}.jsonl`, every line is a JSON object with the following structure:
- `pair_id`: `"<case_id>::<target_disease>"`
- `case_id`: `"<PMC_ID_NN>"`
- `target_disease`: One of the 15 disease keys
- `_provenance.validated_label` and `step12_dataset_label`: Always identical in `selected_case_ft_pofs/` (`"POSITIVE"`, `"NEGATIVE"`, or `"EXCLUDED_NON_TARGET_CASE"`).
- `step11_vpd_satisfied`: `true` for all `POSITIVE` rows; `false` for all `NEGATIVE` and `EXCLUDED_NON_TARGET_CASE` rows.
- `rationale`: Narrative explanation of the clinical case and diagnostic conclusion.
  - *Caveat 1 (`Tuberculosis` template rationales):* In `output_tuberculosis.jsonl`, many `POSITIVE`, `NEGATIVE`, and `EXCLUDED_NON_TARGET_CASE` rows use standardized template strings in `rationale`. You **must** extract the case-specific clinical findings and assays from `step9_key_evidence.evidence_items[].source_quote` and `step5_concept_grounding`.
  - *Caveat 2 (Short/template `EXCLUDED_NON_TARGET_CASE` rationales in `COVID-19` and `HIV_AIDS`):* Combine `rationale` with `step5_concept_grounding`, `step3_patient_anchor` (clinical condition only, stripping age/sex), and `step9_key_evidence.evidence_items` to name the actual non-target condition or clinical context.
- `step9_key_evidence`: Always a `dict` with key `{"evidence_items": [...]}` in `selected_case_ft_pofs/`.
  - Note that `evidence_items` can be empty (`[]`) in several files (`218` `POSITIVE` and `331` `OUT_OF_SCOPE` rows in `COVID-19`; `17` `OUT_OF_SCOPE` rows in `Brucellosis`; `40` `OUT_OF_SCOPE` rows in `HIV_AIDS`; `9` `OUT_OF_SCOPE` rows in `Tuberculosis`; `1` `OUT_OF_SCOPE` row in `Malaria`). When `evidence_items` is empty, extract claims from `rationale`, `step5_concept_grounding`, and the clinical diagnosis in `step3_patient_anchor` (with `source: "rationale"` or `"step5"`).
- `step5_concept_grounding`: Crucial for identifying exact pathogen species, clinical syndromes, non-target species, lexical homonyms, or vaccination/historical contexts.
- `step6_assertion_type`, `step7_temporality`, `step8_clinical_role`, `step9_evidence_strength`, `failure_flags`: Use these to understand *why* a case is `POSITIVE` or `OUT_OF_SCOPE`, then **strip the raw codes** from the output text.

---

## 5. Step-by-Step Transformation Pipeline

### Step 1: Determine Target `dataset_label` and Header Format

Check `step12_dataset_label` (and `_provenance.validated_label`):

#### Branch A — `POSITIVE` (`step12_dataset_label == "POSITIVE"`)
- Set `"dataset_label": "POSITIVE"`.
- Construct the header using the disease-specific header rule:
  - Format: `"<Disease Name> (<specific pathogen species and/or clinical syndrome>)."`
  - Examples:
    - `"Brucellosis (Brucella abortus neurobrucellosis)."`
    - `"COVID-19 (SARS-CoV-2 infection — acute nosocomial pneumonia)."`
    - `"Dengue (Dengue virus infection — severe dengue shock syndrome)."`
    - `"HIV/AIDS (Human Immunodeficiency Virus infection)."`
    - `"Leishmaniasis (mucocutaneous leishmaniasis)."`
    - `"Malaria (severe Plasmodium falciparum infection)."`
    - `"Tuberculosis (Mycobacterium tuberculosis — central nervous system tuberculoma)."`

#### Branch B — `OUT_OF_SCOPE` (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}`)
- Rewrite both `"NEGATIVE"` and `"EXCLUDED_NON_TARGET_CASE"` into `"dataset_label": "OUT_OF_SCOPE"`.
- Construct the header to explicitly state `OUT_OF_SCOPE`, followed in parentheses by the actual non-target diagnosis/clinical context and `Not <Target Disease>`:
  - Format: `"OUT_OF_SCOPE (<Alternative/Non-Target Condition or Clinical Context — Not <Target Disease>>)."`
  - Identify which of the **5 Canonical `OUT_OF_SCOPE` Subtypes** applies:

| Subtype | Raw Source Pattern | Header Pattern & Reasoning Focus |
| :--- | :--- | :--- |
| **1. Explicit Diagnostic Rule-Out + Alternative Out-of-Scope Diagnosis** | `NEGATIVE` (`RULED_OUT_DIAGNOSIS`, `E0_CONTRADICTED`, `C1_DEFINITIVE_REFUTING`) | `OUT_OF_SCOPE (<Confirmed Alternative Diagnosis> — Not <Target Disease>).` State the presenting clinical syndrome, the specific negative diagnostic assays that ruled out `<Target Disease>`, and the confirmed out-of-scope diagnosis (e.g., *Ochrobactrum anthropi* bacteremia, Felty syndrome, *Rickettsia rickettsii*, *Rickettsia typhi*, hantavirus infection, leukemia cutis, plasmablastic lymphoma, nontuberculous mycobacterial infection, Kawasaki disease). |
| **2. Non-Target Pathogen Species / Serogroup / Strain** | `EXCLUDED_NON_TARGET_CASE` or `NEGATIVE` (`F6_EVIDENCE_SPECIFICITY`) | `OUT_OF_SCOPE (<Non-Target Pathogen Infection> — Not <Target Disease>).` State why the isolated organism is outside the target disease definition (e.g., non-O1/non-O139 non-toxigenic *Vibrio cholerae* lacking *ctxA*/*ctxB* or *Vibrio albensis* in `Cholera`; non-typhoidal *Salmonella enteritidis* or *S. Corvallis* in `Typhoid_Fever`; MERS-CoV or HCoV-OC43 in `COVID-19`; *Trypanosoma cruzi* Chagas disease in `Leishmaniasis`; *M. bovis* BCG strain in `Tuberculosis`). |
| **3. Lexical / Acronym Homonym Collision** | `EXCLUDED_NON_TARGET_CASE` (`F1_LEXICAL_HOMONYM`) | `OUT_OF_SCOPE (<Actual Clinical Condition / Procedure> — Not <Target Disease>).` State the actual clinical condition/procedure and clarify the terminology distinction in plain clinical language without pipeline jargon (e.g., Familial Mediterranean Fever with `MEFV` mutation vs. brucellosis; neurosurgical External Ventricular Drain [`EVD`] for hydrocephalus vs. Ebola virus disease; cardiac Patent Foramen Ovale [`PFO`] or cerebral *centrum ovale* vs. *Plasmodium ovale* malaria; orthopedic walking aids vs. HIV/AIDS; serum total bilirubin [`TB`] lab abbreviation vs. tuberculosis). |
| **4. Vaccination, Prophylaxis, or Vaccine-Associated Adverse Event** | `EXCLUDED_NON_TARGET_CASE` (`PREVENTION_VACCINATION`, `F5_DISCOURSE_CONTEXT`) | `OUT_OF_SCOPE (<Vaccine Adverse Event or Prophylaxis Context> — Not Active <Target Disease>).` State the presenting clinical condition and clarify that exposure was solely vaccination, post-exposure prophylaxis (PEP), or chemoprophylaxis rather than wild-type infection (e.g., 17D/Stamaril yellow fever vaccination and YEL-AND/YEL-AVD in `Yellow_Fever`; animal-bite rabies PEP or rabies vaccine-induced TTP in `Rabies`; *Artemisia annua* herbal malaria chemoprophylaxis hepatotoxicity in `Malaria`; SARS-CoV-2 vaccination reaction in `COVID-19`; intravesical BCG immunotherapy in `Tuberculosis`). |
| **5. Remote Historical / Resolved Infection, Maternal Exposure Without Transmission, or Non-Patient Context** | `EXCLUDED_NON_TARGET_CASE` (`HISTORICAL_PAST`, `F4_ASSERTION_TEMPORAL`, `F3_SUBJECT_COREFERENCE`, `F5_DISCOURSE_CONTEXT`) | `OUT_OF_SCOPE (<Current Active Non-Target Condition; Resolved Historical / Non-Patient Context> — Not Active <Target Disease>).` State the active presenting condition being managed (e.g., post-infectious organic mania, oncologic surgery, restorative dental care, neonatal holoprosencephaly without infant HIV transmission, cryptococcal meningitis) and explain why `<Target Disease>` is not an active diagnosis in the patient during the current episode. |

---

### Step 2: Apply the "Guideline Test" (`STRIP` vs. `KEEP` vs. `CONVERT`)

Ask of every detail in `rationale`, `step9_key_evidence`, `step5_concept_grounding`, and `step3_patient_anchor`:
> *"Would this detail appear in a medical textbook or diagnostic guideline explaining why this presentation confirms `<Target Disease>` (or why it is `OUT_OF_SCOPE`)?"*

#### Mandatory `STRIP` List (Record in `dropped_specifics`)
1. **Demographics & Personal Identifiers:** Exact age (`"35-year-old"`, `"2-year-old toddler"`, `"in his 60s"`), sex/gender (`"male"`, `"female"`, `"boy"`, `"woman"`), race/ethnicity, occupation (`"navy marine"`, `"shrimp farm worker"`, `"paddy field worker"`), pregnancy/gravida/para counts (`"gravida 3, para 2"`, `"31 weeks gestation"`), birth weight (`"2600 g"`).
   - *Exception:* When neonatal/perinatal transmission or congenital syndrome is central to the reasoning, use generalized clinical terms (`"neonate"`, `"infant"`, `"perinatally acquired HIV infection"`, `"maternal-fetal exposure"`).
2. **Dates, Timestamps & Case Numbers:** Calendar dates (`"March 28"`, `"November 2020"`, `"1930"`), hospital day numbers (`"on day 8 of hospitalization"`, `"day +130"`, `"on the 5th day"`), duration counts (`"3-day history"`, `"for 6 months"`), and case labels (`"Case 1"`, `"Patient 2"`). Convert durations to qualitative terms (`"prolonged"`, `"acute"`, `"recent"`, `"prior"`).
3. **Geographic Locations, Institutions & Brand/Batch Names:** Countries, cities, states, hospitals, reference labs (`"Senegal"`, `"Suriname"`, `"Tunisia"`, `"Sierra Leone"`, `"Hokkaido Institute of Public Health"`, `"BACT/ALERT VIRTUO"`, `"drug batch number S20073014"`).
   - *Convert:* If travel or endemicity is diagnostically relevant, convert to `"travel to an endemic region"` or `"residence in an endemic area"`.
4. **Raw Vital Signs & Routine Non-Diagnostic Lab Numbers:** Exact temperatures (`"103.7 F"`, `"39.2°C"` → `"high-grade fever"`), blood pressures, heart rates, LVEF percentages (`"20-25%"` → `"severely reduced left ventricular ejection fraction"`), raw CBC/chemistry numbers (`"WBC 1.67 x 10^3/L"`, `"Hb 6.2 g/dL"`, `"platelets 16 x 10^9/L"`, `"ProBNP 1,950 pg/ml"`, `"albumin 16.5 g/L"`, `"total bilirubin 35.2 umol/L"` → convert to `"neutropenia"`, `"severe anemia"`, `"severe thrombocytopenia"`, `"elevated natriuretic peptide"`, `"hypoalbuminemia"`, `"conjugated hyperbilirubinemia"`), and mNGS read ratios (`"(2/19353)"`).
5. **Treatment Dosages, Regimen Durations & Procedural Mechanics:** Drug doses (`"remdesivir 200 mg followed by 100 mg"`, `"dexamethasone 8 mg"`, `"ceftriaxone 100 mg/kg/day"`, `"colchicine 0.25 mg/day"`), catheter sizes, and figure/table citations (`"(Fig. 2)"`, `"(Table 1)"`). Keep the therapeutic class or agent name *only* when treatment response or prophylaxis context is diagnostically relevant (e.g., `"favorable clinical response to doxycycline"`, `"treated with standard anti-tuberculosis therapy"`, `"receiving antiretroviral therapy"`).

#### Mandatory `KEEP` / `CONVERT` List
1. **Pathogen Names, Gene Targets & Serotypes:** Keep exact species, serogroups, and genetic markers (`Brucella abortus`, `Vibrio cholerae non-O1/non-O139`, `ctxA`/`ctxB`, `tcpA`, `SARS-CoV-2`, `Rickettsia rickettsii`, `Salmonella enterica serovar Corvallis`, `MEFV` gene mutation `M680I/M680I`, `ADAMTS13` autoantibodies).
2. **Diagnostic Assays & Specimens:** Keep specific assay methodologies and anatomical specimens (`CSF metagenomic next-generation sequencing (mNGS)`, `Rose Bengal plate agglutination test`, `standard tube agglutination test (SAT)`, `tracheal aspirate RT-PCR`, `NS1 antigen assay`, `Giemsa-stained skin smear`, `microscopic agglutination test (MAT)`, `Montenegro intradermal test`).
3. **Disease-Defining Diagnostic Thresholds (Convert Raw Value → Guideline Threshold):**
   - **Brucellosis:** SAT titer `>= 1:160` (or `>= 1:320` in endemic areas).
   - **HIV/AIDS:** `CD4+ T-lymphocyte count < 200 cells/mm3 (or < 200 cells/uL)` defining AIDS / profound immunosuppression; `inverted CD4/CD8 ratio`.
   - **Malaria:** `P. falciparum hyperparasitemia (> 10% infected erythrocytes)` when raw parasitemia is high (e.g., `39.3%` → `"severe hyperparasitemia"`).
   - **Leptospirosis:** MAT titer `>= 1:400` or `>= 4-fold rise in paired sera`.
   - **Typhoid / Rickettsia:** Convert raw serologic titers (`1:128`, `1:64`, `>1:80`) to `"positive serologic titer"` or `"elevated agglutination titer"`.

---

### Step 3: Decode & Strip All Pipeline Jargon

Never emit internal annotation codes in `ground_truth_reasoning` or `claims[].text`. Translate them into clinical prose:

| Raw Pipeline Token / Code | Clinical Prose Translation (`POSITIVE` or `OUT_OF_SCOPE`) |
| :--- | :--- |
| `E1_CONFIRMATORY_LAB`, `E1_CONFIRMATORY`, `E1` | `"definitive laboratory confirmation"`, `"molecular/microbiological confirmation"` |
| `E2_HIGHLY_SPECIFIC_CLINICAL`, `E2_HIGHLY_SPECIFIC`, `E2` | `"characteristic histopathologic/clinical findings"` |
| `E3_SUPPORTIVE_CLINICAL`, `E3_SUPPORTIVE`, `E3` | `"supportive clinical and laboratory features"` |
| `E0_CONTRADICTED`, `E0_NO_EVIDENCE`, `C1_DEFINITIVE_REFUTING` | `"definitively ruled out by negative diagnostic testing"` |
| `E4_CONTEXT`, `EPIDEMIOLOGICAL_CONTEXT`, `BACKGROUND_CONTEXT` | Explain the specific clinical, epidemiological, or procedural context directly |
| `VPD satisfied -> POSITIVE`, `-> POSITIVE` | Strip from claim text; the suffix `-> POSITIVE diagnosis confirmed.` is appended mechanically |
| `VPD not satisfied -> NEGATIVE`, `Assigned NEGATIVE`, `-> EXCLUDED_NON_TARGET_CASE`, `Excluded as non-target case` | Strip completely; the suffix `-> OUT_OF_SCOPE diagnosis confirmed.` is appended mechanically |
| `F1_LEXICAL_HOMONYM`, `F2_SCOPE_COHORT`, `F3_SUBJECT_COREFERENCE`, `F4_ASSERTION_TEMPORAL`, `F5_DISCOURSE_CONTEXT`, `F6_EVIDENCE_SPECIFICITY` | Strip the flag code; express the underlying clinical reason in plain medical English |

---

### Step 4: Eliminate All Deictic References (Self-Containment Check)

Every claim in `claims[]` must read as standalone medical prose. Replace all deictic pronouns and article-relative phrases:

| Forbidden Deictic Phrase | Required Self-Contained Replacement |
| :--- | :--- |
| `"The patient presented with..."` / `"He/She developed..."` | `"Clinical presentation includes..."` / `"Disease course is complicated by..."` / `"Clinical evaluation demonstrates..."` |
| `"His/Her blood culture grew..."` | `"Blood culture isolates..."` / `"Microbiological culture of blood yields..."` |
| `"This test was negative"` / `"The results of this test..."` | `"Brucella-specific multiplex PCR on the blood isolate is negative"` |
| `"In this case"` / `"In the present report"` / `"Our patient"` | Omit or rewrite as `"Clinical evaluation reveals..."` |

---

## 6. Worked Examples (Directly from `selected_case_ft_pofs/`)

### Worked Example 1 — `POSITIVE` Case (`PMC11835056_01::Brucellosis`)
**Input Record (`selected_case_ft_pofs/output_brucellosis.jsonl`):**
- `step12_dataset_label`: `"POSITIVE"`, `step5_concept_grounding`: `"Brucella abortus"`
- `rationale`: `"35-year-old female presenting with headache whose CSF mNGS identified Brucella abortus and serum Rose Bengal test and SAT (1:160) were positive."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"mNGS of the CSF identified Brucella abortus (2/19353). Given the limited number of sequences, serum brucellosis antibody testing was conducted. By the 5th day, the Rose Bengal plate test was positive,"`

**Target Output:**
```json
{
  "pair_id": "PMC11835056_01::Brucellosis",
  "case_id": "PMC11835056_01",
  "target_disease": "Brucellosis",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "Brucellosis (Brucella abortus neurobrucellosis). Reasoning: (1) Neurological presentation with headache and fever is accompanied by identification of Brucella abortus in cerebrospinal fluid via metagenomic next-generation sequencing (mNGS). (2) Systemic brucellosis is serologically confirmed by a positive serum Rose Bengal plate agglutination test and a positive standard tube agglutination test (SAT) meeting the diagnostic threshold (>= 1:160). -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Neurological presentation with headache and fever is accompanied by identification of Brucella abortus in cerebrospinal fluid via metagenomic next-generation sequencing (mNGS).",
      "source": "both"
    },
    {
      "text": "Systemic brucellosis is serologically confirmed by a positive serum Rose Bengal plate agglutination test and a positive standard tube agglutination test (SAT) meeting the diagnostic threshold (>= 1:160).",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "35-year-old female — demographics",
    "2/19353 — mNGS raw sequence read ratio",
    "By the 5th day — hospital timeline",
    "1:160 — converted to SAT diagnostic threshold (>= 1:160)"
  ]
}
```

### Worked Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC6062634_01::Brucellosis`)
**Input Record (`selected_case_ft_pofs/output_brucellosis.jsonl`):**
- `step12_dataset_label`: `"NEGATIVE"`, `step8_clinical_role`: `"RULED_OUT_DIAGNOSIS"`
- `rationale`: `"32-year-old female whose blood isolate showed polyvalent agglutination with Brucella antisera, but definitive multiplex PCR was negative and 16S rRNA gene sequencing proved Ochrobactrum anthropi bacteremia, ruling out brucellosis."`
- `step9_key_evidence.evidence_items[0].source_quote`: `"The results of this test were negative, indicating that the isolated bacterium did not belong to the Brucella species."`

**Target Output:**
```json
{
  "pair_id": "PMC6062634_01::Brucellosis",
  "case_id": "PMC6062634_01",
  "target_disease": "Brucellosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Ochrobactrum anthropi bacteremia — Not Brucellosis). Reasoning: (1) Evaluation of fever of unknown origin in an immunocompromised hematologic transplant recipient shows initial cross-reactive polyvalent agglutination of a blood culture isolate with Brucella antisera, but definitive Brucella-specific multiplex PCR is negative, excluding Brucella species. (2) Confirmatory 16S rRNA gene sequencing identifies the causative bloodstream pathogen as Ochrobactrum anthropi rather than Brucella. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Evaluation of fever of unknown origin in an immunocompromised hematologic transplant recipient shows initial cross-reactive polyvalent agglutination of a blood culture isolate with Brucella antisera, but definitive Brucella-specific multiplex PCR is negative, excluding Brucella species.",
      "source": "both"
    },
    {
      "text": "Confirmatory 16S rRNA gene sequencing identifies the causative bloodstream pathogen as Ochrobactrum anthropi rather than Brucella.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "32-year-old female — demographics"
  ]
}
```

### Worked Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC9883795_01::Brucellosis`)
**Input Record (`selected_case_ft_pofs/output_brucellosis.jsonl`):**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F1_LEXICAL_HOMONYM"]`
- `rationale`: `"Lexical homonym collision: the case report describes Familial Mediterranean Fever (FMF), a hereditary autoinflammatory disorder confirmed by MEFV gene mutation (M680I/M680I). It does not describe Brucellosis (infectious Mediterranean fever). Excluded as non-target case."`

**Target Output:**
```json
{
  "pair_id": "PMC9883795_01::Brucellosis",
  "case_id": "PMC9883795_01",
  "target_disease": "Brucellosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Familial Mediterranean Fever — Not Brucellosis). Reasoning: (1) Recurrent febrile pleurisy is caused by Familial Mediterranean Fever (FMF), a hereditary autoinflammatory disorder confirmed by homozygous MEFV gene mutation (M680I/M680I) on genetic testing. (2) There is no clinical or microbiological evidence of Brucella infection, as the term Mediterranean fever refers to genetic Familial Mediterranean Fever rather than infectious brucellosis. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Recurrent febrile pleurisy is caused by Familial Mediterranean Fever (FMF), a hereditary autoinflammatory disorder confirmed by homozygous MEFV gene mutation (M680I/M680I) on genetic testing.",
      "source": "both"
    },
    {
      "text": "There is no clinical or microbiological evidence of Brucella infection, as the term Mediterranean fever refers to genetic Familial Mediterranean Fever rather than infectious brucellosis.",
      "source": "rationale"
    }
  ],
  "dropped_specifics": [
    "30-year-old male navy marine — demographics and occupation",
    "Lexical homonym collision / Excluded as non-target case — pipeline jargon stripped"
  ]
}
```

---

## 7. Pre-Emission Validation Checklist (Definition of Done)

Before writing any record to the output JSONL file, verify **all 10 gates**:

1. **Row Count & Pair ID Parity:** The output JSONL has the exact same number of lines and identical `pair_id`, `case_id`, and `target_disease` values as `selected_case_ft_pofs/output_{disease}.jsonl`.
2. **Strict Dual-Label Mapping:**
   - If raw `step12_dataset_label == "POSITIVE"` → output `dataset_label` is `"POSITIVE"`.
   - If raw `step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → output `dataset_label` is `"OUT_OF_SCOPE"`. Never emit `"NEGATIVE"` or `"EXCLUDED_NON_TARGET_CASE"` in `dataset_label`.
3. **Header & Suffix Match `dataset_label`:**
   - `POSITIVE` rows start with `<Disease Name> (...). Reasoning: (1) ...` and end with `-> POSITIVE diagnosis confirmed.`.
   - `OUT_OF_SCOPE` rows start with `OUT_OF_SCOPE (... — Not <Target Disease>). Reasoning: (1) ...` and end with `-> OUT_OF_SCOPE diagnosis confirmed.`.
4. **Verbatim Mechanical Assembly:** Joining `(1) claims[0].text (2) claims[1].text ...` reproduces the body of `ground_truth_reasoning` character-for-character.
5. **Claim Formatting:** Every `claims[i].text` is non-empty, ends with `.`, does not start with `(1)` or `(2)`, and has `source in {"rationale", "step9", "both", "step5"}`.
6. **Zero Forbidden Pipeline Jargon (Regex Gate):** Neither `ground_truth_reasoning` nor `claims[].text` matches any of:
   `\b(VPD|E0|E1|E2|E3|E4|E0_NO_EVIDENCE|E0_CONTRADICTED|E0_NONE|E1_CONFIRMATORY|E1_CONFIRMATORY_LAB|E2_HIGHLY_SPECIFIC|E2_HIGHLY_SPECIFIC_CLINICAL|E3_SUPPORTIVE|E3_SUPPORTIVE_CLINICAL|E4_CONTEXT|C1_DEFINITIVE_REFUTING|CONFIRMED_PRESENT|ABSENT_NEGATIVE|RULED_OUT_DIAGNOSIS|EXCLUDED_NON_TARGET_CASE|PREVENTION_VACCINATION|HISTORICAL_PAST|CURRENT_EPISODE|CAUSATIVE_PATHOGEN|PRIMARY_DIAGNOSIS|EPIDEMIOLOGICAL_CONTEXT|BACKGROUND_CONTEXT|F1_LEXICAL_HOMONYM|F2_SCOPE_COHORT|F3_SUBJECT_COREFERENCE|F4_ASSERTION_TEMPORAL|F5_DISCOURSE_CONTEXT|F6_EVIDENCE_SPECIFICITY|Assigned NEGATIVE|Excluded as non-target case)\b`
7. **Zero Deictic Leaks (Regex Gate):** Case-insensitive scan confirms no occurrences of `\b(the patient|this patient|our patient|he was|she was|his |her |who presented|in this case|in the present case|this report|the above)\b`.
8. **Zero Demographic / Date / Vital-Sign Leaks:** No age patterns (`\b\d+-year-old\b`, `\baged \d+\b`), no gender nouns (`\b(male|female|man|woman|boy|girl)\b`), no calendar dates/months, and no raw vital signs.
9. **Audit Trail Completeness:** Every stripped age, sex, date, location, raw lab number, or threshold conversion is documented in `dropped_specifics[]`.
10. **Valid UTF-8 JSONL:** Every line parses cleanly via `json.loads()` with all 7 required top-level keys (`pair_id`, `case_id`, `target_disease`, `dataset_label`, `ground_truth_reasoning`, `claims`, `dropped_specifics`).


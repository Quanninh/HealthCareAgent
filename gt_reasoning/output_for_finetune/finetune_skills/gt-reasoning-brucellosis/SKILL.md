---
name: gt-reasoning-brucellosis-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Brucellosis cases in selected_case_ft_pofs/output_brucellosis.jsonl across POSITIVE (active Brucella infection) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE).
---

# Brucellosis — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_brucellosis.jsonl`)

- **Disease Key:** `"Brucellosis"`
- **Input File:** `selected_case_ft_pofs/output_brucellosis.jsonl` (`45` total rows)
  - **`POSITIVE` (`13` rows):** Active human brucellosis (`Brucella melitensis`, `Brucella abortus`, `Brucella suis`, or unspeciated `Brucella species`) confirmed via blood/bone marrow/CSF/tissue culture, mNGS/PCR, or standard tube agglutination test (`SAT >= 1:160` or `>= 1:320`) / Coombs test.
  - **`OUT_OF_SCOPE` (`32` rows, rewritten from `3` `NEGATIVE` + `29` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out (`3` `NEGATIVE` rows):**
       - `PMC9449881_01`: Rheumatoid arthritis and Felty syndrome with ecthyma gangrenosum; remote history of treated brucellosis, screened negative for *Brucella* during current admission.
       - `PMC6062634_01`: Blood isolate cross-reacted with *Brucella* antisera, but *Brucella* multiplex PCR was negative and 16S rRNA sequencing confirmed *Ochrobactrum anthropi* bacteremia.
       - `PMC10690546_01`: Pediatric hepatic brucelloma mentioned only in introduction literature while the primary patient had non-brucellar hepatic lesion / negative workup.
    2. **Lexical Homonym Collision (`25` `EXCLUDED_NON_TARGET_CASE` rows, `F1_LEXICAL_HOMONYM`):**
       - **Familial Mediterranean Fever (`FMF`):** Hereditary autoinflammatory disorder caused by `MEFV` gene mutations (`M680I`, `M694V`, `R202Q`, `V726A`, `E148Q`) managed with colchicine or anti-IL-1 therapy, colliding lexically with "Mediterranean fever" (historical synonym for brucellosis). Note: `17` of these rows have empty `step9_key_evidence.evidence_items` (`[]`) — extract claims directly from `rationale`, `step5_concept_grounding`, and clinical presentation in `step3_patient_anchor`.
       - **Microbiological Culture Medium Homonym:** Mention of `"Brucella agar"` or `"Brucella broth"` used as an anaerobic culture medium to grow unrelated bacteria (e.g., *Campylobacter*, *Clostridioides*, anaerobes), not *Brucella* infection.
    3. **Background / Differential / Historical Mention (`4` `EXCLUDED_NON_TARGET_CASE` rows):** Passing mention of brucellosis in epidemiological background, differential list, or unverified remote history while treating an unrelated primary disease.

---

## 2. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Brucellosis (<Brucella species and/or focal syndrome>)."`
  - Specify species when grounded in `step5_concept_grounding` or `rationale` (`Brucella melitensis`, `Brucella abortus`, `Brucella suis`, or `Brucella species`) and focal organ involvement when present (e.g., `"Brucellosis (Brucella abortus neurobrucellosis)."`, `"Brucellosis (Brucella melitensis spondylodiscitis)."`, `"Brucellosis (Brucella species bacteremia and endocarditis)."`).
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Condition or Non-Target Context> — Not Brucellosis)."`
  - *Rule-out examples:*
    - `"OUT_OF_SCOPE (Ochrobactrum anthropi bacteremia — Not Brucellosis)."`
    - `"OUT_OF_SCOPE (Felty syndrome and ecthyma gangrenosum with negative Brucella screening — Not Brucellosis)."`
  - *Lexical homonym examples:*
    - `"OUT_OF_SCOPE (Familial Mediterranean Fever — Not Brucellosis)."`
    - `"OUT_OF_SCOPE (<Anaerobic Infection> cultured on Brucella agar medium — Not Brucellosis)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogen & Cross-Reactive Species:** Keep `Brucella melitensis`, `Brucella abortus`, `Brucella suis`, `Brucella species`, and cross-reactive non-target organisms such as `Ochrobactrum anthropi`.
2. **Diagnostic Assays:** Keep blood/bone marrow/CSF/synovial fluid culture, `metagenomic next-generation sequencing (mNGS)`, `16S rRNA gene sequencing`, `Brucella multiplex PCR`, `Rose Bengal plate agglutination test (RBPT)`, `standard tube agglutination test (SAT)`, `Brucella Coombs test`, and `ELISA (IgM/IgG)`.
3. **Serologic Threshold Conversion:**
   - Convert raw SAT titers (`1:160`, `1:320`, `1:640`, `1:1280`) to the diagnostic threshold: `"positive standard tube agglutination test (SAT) meeting the diagnostic threshold (>= 1:160)"` (or `(>= 1:320)` when an endemic cutoff is cited) and log the raw titer in `dropped_specifics`.
   - Convert Coombs titers (`>= 1:320`) to `"positive Brucella Coombs test meeting diagnostic threshold (>= 1:320)"`.
4. **Focal Syndromes & Zoonotic Exposure:** Keep focal manifestations (`neurobrucellosis`, `spondylodiscitis`, `sacroiliitis`, `epididymo-orchitis`, `endocarditis`, `hepatic/splenic abscess`) and generalized zoonotic exposure (`consumption of unpasteurized dairy products`, `occupational livestock contact`).
5. **FMF Genetic Markers (in `OUT_OF_SCOPE` rows):** Keep `Familial Mediterranean Fever (FMF)`, `MEFV gene mutation` (including specific variants like `M680I`, `M694V`, `R202Q`), `autoinflammatory serositis/pleurisy/peritonitis`, and `response to colchicine`.

### Strip (Log in `dropped_specifics`)
- Exact patient age, sex, nationality/ethnicity (`"Turkish girl"`, `"navy marine"`).
- Raw mNGS sequence read counts (`"2/19353"`), routine CBC/CRP/ESR numbers, and antibiotic/colchicine dosages (`"0.25 mg/day"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_brucellosis.jsonl`)

### Example 1 — `POSITIVE` (`PMC11835056_01::Brucellosis`)
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

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC9449881_01::Brucellosis`)
**Input Summary:** 67-year-old female with rheumatoid arthritis and Felty syndrome presenting with fever and ecthyma gangrenosum; remote history of treated brucellosis in 2020; screened negative for *Brucella* during current admission.
```json
{
  "pair_id": "PMC9449881_01::Brucellosis",
  "case_id": "PMC9449881_01",
  "target_disease": "Brucellosis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Felty syndrome and ecthyma gangrenosum — Not Brucellosis). Reasoning: (1) Acute presentation with fever and ecthyma gangrenosum occurs in the setting of rheumatoid arthritis complicated by Felty syndrome. (2) Despite a remote history of previously treated brucellosis, diagnostic screening for Brucella during the active episode is negative, ruling out active or relapsed brucellosis. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute presentation with fever and ecthyma gangrenosum occurs in the setting of rheumatoid arthritis complicated by Felty syndrome.",
      "source": "rationale"
    },
    {
      "text": "Despite a remote history of previously treated brucellosis, diagnostic screening for Brucella during the active episode is negative, ruling out active or relapsed brucellosis.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "67-year-old female — demographics",
    "in 2020 — calendar year stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC9883795_01::Brucellosis`)
**Input Summary:** 30-year-old male navy marine with recurrent febrile pleurisy diagnosed with Familial Mediterranean Fever (`MEFV` homozygous mutation `M680I/M680I`).
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

## 5. Pre-Emission Checklist (`Brucellosis`)
- Verify all `45` rows are emitted (`13` `"POSITIVE"`, `32` `"OUT_OF_SCOPE"`).
- Confirm that the `17` FMF rows with empty `evidence_items` (`[]`) have complete, self-contained `claims[]` extracted from `rationale` and `step5_concept_grounding` (`source: "rationale"` or `"step5"`).
- Ensure all raw SAT/Coombs titers are converted to diagnostic threshold statements (`>= 1:160` or `>= 1:320`) and logged in `dropped_specifics`.
- Run the master coordinator regex gates to confirm zero pipeline codes (`E0_CONTRADICTED`, `F1_LEXICAL_HOMONYM`, `RULED_OUT_DIAGNOSIS`, `EXCLUDED_NON_TARGET_CASE`) and zero deictic pronouns.


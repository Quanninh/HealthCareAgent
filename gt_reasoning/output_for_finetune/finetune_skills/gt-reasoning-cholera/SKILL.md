---
name: gt-reasoning-cholera-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Cholera cases in selected_case_ft_pofs/output_cholera.jsonl across OUT_OF_SCOPE (non-O1/non-O139 non-toxigenic Vibrio cholerae and Vibrio albensis infections rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE) and POSITIVE reference rules.
---

# Cholera — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_cholera.jsonl`)

- **Disease Key:** `"Cholera"`
- **Input File:** `selected_case_ft_pofs/output_cholera.jsonl` (`12` total rows)
  - **`POSITIVE` (`0` rows in `selected_case_ft_pofs/`, reference rules retained below):** Epidemic/toxigenic cholera caused by *Vibrio cholerae* serogroup `O1` (Inaba, Ogawa, Hikojima; classical or El Tor biotype) or `O139`, or cholera toxin (`ctxA`/`ctxB`) positive *V. cholerae* causing acute secretory diarrheal illness, confirmed by stool culture on TCBS agar with O1/O139 slide agglutination or PCR.
  - **`OUT_OF_SCOPE` (`12` rows, rewritten from `1` `NEGATIVE` + `11` `EXCLUDED_NON_TARGET_CASE`):**
    Every single case in `selected_case_ft_pofs/output_cholera.jsonl` represents a **non-target *Vibrio* infection** (Subtype 2: Non-Target Pathogen Serogroup/Species) where true epidemic/toxigenic cholera (serogroup O1/O139) is absent or explicitly refuted:
    1. **Non-O1 / Non-O139 *Vibrio cholerae* (`NOVC`) Extraintestinal or Non-Toxigenic Infections (`11` rows):**
       - `PMC4627963_01` (raw `NEGATIVE`): Returned traveler with watery diarrhea, fever, pyogenic liver abscesses, and *V. cholerae* bacteremia; stool cultures were negative, isolate did not agglutinate with O1/O139 antisera, and PCR confirmed absence of `ctxA`, `ctxB`, `tcpA`, and `stn` virulence genes.
       - `PMC6491804_01` (raw `EXCLUDED_NON_TARGET_CASE`): Acute gastroenteritis after raw mollusc ingestion; stool culture on TCBS grew *V. cholerae*, but slide agglutination was non-O1/non-O139 and whole-genome/PCR profiling was negative for `ctxA`, `zot`, `hlyA`, `tcpA`, `tcpI`, and `ompU` (positive only for species-housekeeping `toxR`).
       - `PMC6796756_01`, `PMC4961881_01`, `PMC6360190_01`, `PMC5490655_01`, `PMC8896959_01`, `PMC9380259_01`, `PMC10695424_01`, `PMC5013514_01`, `PMC9015075_01` (raw `EXCLUDED_NON_TARGET_CASE`): Non-O1/non-O139 *V. cholerae* causing bacteremic cellulitis/gangrene, necrotizing fasciitis, bullous skin lesions in cirrhosis, chronic otitis media/mastoiditis, acute cholecystitis, or non-toxigenic bacteremia/UTI.
    2. **Non-Target *Vibrio* Species (`1` row):**
       - `PMC5360940_01` (raw `EXCLUDED_NON_TARGET_CASE`): *Vibrio albensis* urinary tract infection / bacteremia, not toxigenic *V. cholerae* O1/O139 cholera.

---

## 2. Header & Concluding Suffix Rules

### A. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Non-O1/non-O139 Vibrio cholerae or Vibrio albensis Syndrome> — Not Cholera)."`
  - Examples:
    - `"OUT_OF_SCOPE (Non-O1/non-O139 non-toxigenic Vibrio cholerae bacteremia and pyogenic liver abscesses — Not Cholera)."`
    - `"OUT_OF_SCOPE (Non-O1/non-O139 non-toxigenic Vibrio cholerae gastroenteritis — Not Cholera)."`
    - `"OUT_OF_SCOPE (Non-O1/non-O139 Vibrio cholerae bacteremic lower-extremity cellulitis and gangrene — Not Cholera)."`
    - `"OUT_OF_SCOPE (Vibrio albensis infection — Not Cholera)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

### B. For `POSITIVE` Cases (Reference Pattern when `step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Cholera (Vibrio cholerae O1/O139 infection)."` (specify biotype/serotype e.g., `O1 El Tor Ogawa` when available).
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Serogroup & Virulence Gene Specificity (Critical for `Cholera` vs. `OUT_OF_SCOPE`):**
   - Always keep serogrouping results: `non-O1/non-O139 Vibrio cholerae (NOVC)`, negative slide agglutination with `O1 and O139 antisera`, or `Vibrio albensis`.
   - Always keep virulence gene PCR/genomic profiling results: absence of cholera toxin genes (`ctxA`, `ctxB`), toxin-coregulated pilus (`tcpA`, `tcpI`), zonula occludens toxin (`zot`), hemolysin (`hlyA`), outer membrane protein (`ompU`), and heat-stable enterotoxin (`stn`), alongside presence of species-regulatory gene `toxR`.
2. **Selective Culture Media & Identification Assays:**
   - Keep `thiosulfate-citrate-bile salts-sucrose (TCBS) agar`, `MacConkey agar`, `MALDI-TOF mass spectrometry`, `16S rRNA sequencing`, and `O1/O139 polyvalent antisera slide agglutination`.
3. **Clinical Syndrome & Exposure Context:**
   - Keep extraintestinal syndromes (`pyogenic liver abscess`, `bacteremic cellulitis`, `necrotizing fasciitis`, `otitis media`, `cholecystitis`) and marine/dietary exposures (`raw mollusc/seafood ingestion`, `seawater exposure to open wound`, `underlying hepatic cirrhosis or diabetes mellitus`).

### Strip (Log in `dropped_specifics`)
- Patient age, sex, and occupation (`"70-year-old male"`, `"25-year-old male shrimp farm worker"`, `"54-year-old diabetic male"` — keep `"diabetes mellitus"` as a clinical comorbidity, strip `"54-year-old"` and `"male"`).
- Geographic names and reference center names (`"Senegal"`, `"National Reference Center"`, `"bioMerieux, US"`), automated blood culture incubation hours (`"after 8.5 h of incubation in the BACT/ALERT VIRTUO"`), and calendar dates (`"27/07/2018"`).
- Pipeline tokens (`"VPD not satisfied -> NEGATIVE"`, `"-> EXCLUDED_NON_TARGET_CASE"`, `"E0_CONTRADICTED"`, `"F6_EVIDENCE_SPECIFICITY"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_cholera.jsonl`)

### Example 1 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC4627963_01::Cholera`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Non-O1, non-O139 Vibrio cholerae bacteremia with hepatic abscesses; toxigenic cholera ruled out"`
- `rationale`: `"A 70-year-old male returned from Senegal with watery diarrhea, fever, and liver abscesses. Blood culture grew Vibrio cholerae, but evaluation at the National Reference Center proved negative for O1 and O139 antisera, negative for cholera toxin genes (ctxA/ctxB), and stool cultures were negative. Cholera was definitively tested and ruled out, and the patient was diagnosed with non-O1/non-O139 pyogenic liver abscess and bacteremia. VPD not satisfied -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC4627963_01::Cholera",
  "case_id": "PMC4627963_01",
  "target_disease": "Cholera",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Non-O1/non-O139 non-toxigenic Vibrio cholerae bacteremia and pyogenic liver abscesses — Not Cholera). Reasoning: (1) Clinical presentation with fever, watery diarrhea, and pyogenic hepatic abscesses is accompanied by blood cultures yielding a Gram-negative rod identified as Vibrio cholerae, whereas stool cultures are negative. (2) Reference seroagglutination of the blood isolate is negative for O1 and O139 antisera, and virulence PCR demonstrates the absence of cholera toxin genes (ctxA and ctxB), toxin-coregulated pilus gene (tcpA), and heat-stable enterotoxin gene (stn), ruling out toxigenic cholera and confirming invasive non-O1/non-O139 Vibrio cholerae infection. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation with fever, watery diarrhea, and pyogenic hepatic abscesses is accompanied by blood cultures yielding a Gram-negative rod identified as Vibrio cholerae, whereas stool cultures are negative.",
      "source": "both"
    },
    {
      "text": "Reference seroagglutination of the blood isolate is negative for O1 and O139 antisera, and virulence PCR demonstrates the absence of cholera toxin genes (ctxA and ctxB), toxin-coregulated pilus gene (tcpA), and heat-stable enterotoxin gene (stn), ruling out toxigenic cholera and confirming invasive non-O1/non-O139 Vibrio cholerae infection.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "70-year-old male — demographics",
    "returned from Senegal — geographic location",
    "National Reference Center, (Fig. 2) — institution name and figure reference",
    "VPD not satisfied -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC6491804_01::Cholera`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step5_concept_grounding`: `"Non-O1/non-O139 Vibrio cholerae gastroenteritis; non-toxigenic isolate lacking cholera toxin genes"`
- `rationale`: `"A 25-year-old male presented with watery diarrhea and vomiting following raw mollusc ingestion. Stool culture on TCBS isolated Vibrio cholerae, but slide agglutination with O1 and O139 antisera was negative, and genomic analysis confirmed absence of cholera toxin genes (ctxA, zot, tcpA). Non-O1/non-O139 V. cholerae intestinal infection represents non-target vibriosis rather than epidemic cholera. VPD not satisfied -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC6491804_01::Cholera",
  "case_id": "PMC6491804_01",
  "target_disease": "Cholera",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Non-O1/non-O139 non-toxigenic Vibrio cholerae gastroenteritis — Not Cholera). Reasoning: (1) Acute watery diarrhea and vomiting following raw mollusc ingestion yield Vibrio cholerae on thiosulfate-citrate-bile salts-sucrose (TCBS) and MacConkey agar stool cultures. (2) Slide agglutination with O1 and O139 antisera is negative, and genomic virulence profiling confirms that the isolate carries the species-specific toxR gene but lacks cholera toxin and virulence genes (ctxA, zot, hlyA, tcpA, tcpI, and ompU), establishing non-O1/non-O139 non-toxigenic vibriosis rather than epidemic cholera. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Acute watery diarrhea and vomiting following raw mollusc ingestion yield Vibrio cholerae on thiosulfate-citrate-bile salts-sucrose (TCBS) and MacConkey agar stool cultures.",
      "source": "both"
    },
    {
      "text": "Slide agglutination with O1 and O139 antisera is negative, and genomic virulence profiling confirms that the isolate carries the species-specific toxR gene but lacks cholera toxin and virulence genes (ctxA, zot, hlyA, tcpA, tcpI, and ompU), establishing non-O1/non-O139 non-toxigenic vibriosis rather than epidemic cholera.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "25-year-old male shrimp farm worker — demographics and occupation",
    "VPD not satisfied -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC6796756_01::Cholera`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `step5_concept_grounding`: `"Non-O1/non-O139 Vibrio cholerae soft tissue infection and bacteremia, not clinical cholera"`
- `rationale`: `"A 54-year-old diabetic male presented with right lower extremity cellulitis and impending sepsis. Blood culture isolated non-O1, non-O139 Vibrio cholerae. The patient had bacteremic soft tissue infection/gangrene rather than clinical cholera (acute diarrheal illness caused by toxigenic V. cholerae). VPD not satisfied -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC6796756_01::Cholera",
  "case_id": "PMC6796756_01",
  "target_disease": "Cholera",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Non-O1/non-O139 Vibrio cholerae bacteremic lower-extremity cellulitis and gangrene — Not Cholera). Reasoning: (1) Severe lower-extremity cellulitis and gangrene with impending sepsis in the setting of diabetes mellitus are accompanied by blood cultures isolating Vibrio cholerae. (2) Serotyping agglutination confirms a non-O1, non-O139 Vibrio cholerae strain causing invasive extraintestinal soft-tissue infection rather than toxigenic O1/O139 diarrheal cholera. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Severe lower-extremity cellulitis and gangrene with impending sepsis in the setting of diabetes mellitus are accompanied by blood cultures isolating Vibrio cholerae.",
      "source": "both"
    },
    {
      "text": "Serotyping agglutination confirms a non-O1, non-O139 Vibrio cholerae strain causing invasive extraintestinal soft-tissue infection rather than toxigenic O1/O139 diarrheal cholera.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "54-year-old male, right — demographics and laterality",
    "27/07/2018, after 8.5 h of incubation in the BACT/ALERT VIRTUO (bioMerieux, US) — date, incubation hours, and instrument brand",
    "VPD not satisfied -> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Cholera`)
- Verify all `12` rows in `output_cholera.jsonl` are emitted with `"dataset_label": "OUT_OF_SCOPE"`.
- Ensure every row explicitly explains why the *Vibrio* isolate does not constitute cholera (non-O1/non-O139 serogroup, absence of `ctxA`/`ctxB` cholera toxin genes, extraintestinal wound/biliary/ear/bloodstream infection, or *Vibrio albensis*).
- Confirm zero pipeline codes and zero patient demographics/dates remain in `ground_truth_reasoning` or `claims`.


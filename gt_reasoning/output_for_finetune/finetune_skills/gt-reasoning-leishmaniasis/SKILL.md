---
name: gt-reasoning-leishmaniasis-finetune
description: Extract generalized, self-contained ground-truth clinical reasoning for Leishmaniasis cases in selected_case_ft_pofs/output_leishmaniasis.jsonl across POSITIVE (active visceral, cutaneous, or mucocutaneous Leishmania infection) and OUT_OF_SCOPE (rewritten from NEGATIVE and EXCLUDED_NON_TARGET_CASE).
---

# Leishmaniasis — Fine-Tuning Ground-Truth Reasoning Extraction Skill

## 1. Quick Reference & Dataset Profile (`selected_case_ft_pofs/output_leishmaniasis.jsonl`)

- **Disease Key:** `"Leishmaniasis"`
- **Input File:** `selected_case_ft_pofs/output_leishmaniasis.jsonl` (`30` total rows)
  - **`POSITIVE` (`20` rows):** Active visceral leishmaniasis (`VL` / kala-azar), cutaneous leishmaniasis (`CL`), mucocutaneous leishmaniasis (`MCL`), or post-kala-azar dermal leishmaniasis (`PKDL`) caused by *Leishmania* species (`L. infantum`, `L. donovani`, `L. braziliensis`, `L. panamensis`, `L. guyanensis`, `L. major`, `L. tropica`), confirmed by Giemsa-stained bone marrow/splenic/skin smear microscopy (intracellular amastigotes / Leishman-Donovan bodies), NNN culture, *Leishmania* PCR/mNGS, `rK39` immunochromatographic strip test / DAT / IFA serology, or Montenegro intradermal skin test (`leishmanin skin test`) with characteristic clinical/histopathological findings and antileishmanial treatment response.
  - **`OUT_OF_SCOPE` (`10` rows, rewritten from `2` `NEGATIVE` + `8` `EXCLUDED_NON_TARGET_CASE`):**
    1. **Explicit Diagnostic Rule-Out + Alternative Histopathological Diagnosis (`2` `NEGATIVE` rows):**
       - `PMC3898666_01`: Ulcerated finger dermal nodule clinically suspected to be cutaneous leishmaniasis, where punch biopsy histopathology ruled out *Leishmania* and established a definitive diagnosis of **fibro-osseous pseudotumor of the digit**.
       - `PMC10699217_01`: Ulcerative forearm nodule clinically suspected of cutaneous leishmaniasis, where Giemsa-stained smears and skin biopsy histopathology were negative for *Leishmania* (`C1_DEFINITIVE_REFUTING`) and immunohistochemistry established **leukemia cutis (small lymphocytic lymphoma / chronic lymphocytic leukemia)** responsive to rituximab.
    2. **Non-Target Kinetoplastid Pathogen (`1` `EXCLUDED_NON_TARGET_CASE` row, `PMC9812266_01`):**
       - Acute **Chagas myocarditis** caused by *Trypanosoma cruzi* (non-target kinetoplastid protozoan), not *Leishmania*.
    3. **Remote Historical / Childhood Scar Comorbidity (`2` `EXCLUDED_NON_TARGET_CASE` rows, `PMC7481585_01`, `PMC10864015_01`):**
       - Basal cell carcinoma (`BCC`) arising in a 52-year-old leishmanization scar or remote resolved childhood cutaneous leishmaniasis scar with no active *Leishmania* infection.
    4. **Non-Patient Epidemiological / Policy / Veterinary Context (`5` `EXCLUDED_NON_TARGET_CASE` rows):**
       - `PMC6600853_01`: Cryptococcal meningitis case where visceral leishmaniasis is mentioned solely because clinicians sought liposomal amphotericin B from a government VL drug program.
       - `PMC6850740_01` & `PMC7527865_01`: Article introduction/epidemiological background segments without an individual patient clinical presentation.
       - `PMC4719184_01`: Epidemiological discussion of HIV/VL co-infection in an unrelated case.

---

## 2. Header & Concluding Suffix Rules

### A. For `POSITIVE` Cases (`step12_dataset_label == "POSITIVE"` → `dataset_label: "POSITIVE"`)
- **Header Pattern:** `"Leishmaniasis (<clinical form: visceral / cutaneous / mucocutaneous leishmaniasis and Leishmania species if specified>)."`
  - Examples:
    - `"Leishmaniasis (mucocutaneous leishmaniasis)."`
    - `"Leishmaniasis (visceral leishmaniasis due to Leishmania infantum)."`
    - `"Leishmaniasis (cutaneous leishmaniasis)."`
- **Concluding Suffix:** `"-> POSITIVE diagnosis confirmed."`

### B. For `OUT_OF_SCOPE` Cases (`step12_dataset_label in {"NEGATIVE", "EXCLUDED_NON_TARGET_CASE"}` → `dataset_label: "OUT_OF_SCOPE"`)
- **Header Pattern:** `"OUT_OF_SCOPE (<Alternative Diagnosis or Non-Target Context> — Not Leishmaniasis)."`
  - Examples:
    - `"OUT_OF_SCOPE (Fibro-osseous pseudotumor of the digit — Not Leishmaniasis)."`
    - `"OUT_OF_SCOPE (Leukemia cutis / small lymphocytic lymphoma — Not Leishmaniasis)."`
    - `"OUT_OF_SCOPE (Cryptococcal meningitis with contextual reference to a visceral leishmaniasis drug program — Not Leishmaniasis)."`
    - `"OUT_OF_SCOPE (Epidemiological background discussion without individual patient case — Not Active Leishmaniasis)."`
- **Concluding Suffix:** `"-> OUT_OF_SCOPE diagnosis confirmed."`

---

## 3. Disease-Specific Keep / Convert / Strip Rules

### Keep / Convert
1. **Pathogens & Clinical Forms:** Keep `Leishmania infantum`, `L. donovani`, `L. braziliensis`, `L. panamensis`, `L. major`, `L. tropica`, clinical forms (`visceral`, `cutaneous`, `mucocutaneous`, `post-kala-azar dermal leishmaniasis`), and non-target pathogens/conditions (`Trypanosoma cruzi`, `fibro-osseous pseudotumor`, `leukemia cutis / SLL-CLL`, `cryptococcal meningitis`, `basal cell carcinoma`).
2. **Diagnostic Assays & Histopathology:** Keep `Giemsa-stained smear microscopy`, `amastigotes (Leishman-Donovan bodies) within macrophages`, `promastigotes on Novy-MacNeal-Nicolle (NNN) medium`, `Leishmania PCR / kDNA PCR`, `rK39 immunochromatographic test`, `Montenegro intradermal skin test`, and biopsy histopathology (`biphasic fibro-osseous dermal lesion`, `monomorphous dermal lymphocytic infiltrate`).
3. **Therapeutic Agents:** Keep `liposomal amphotericin B`, `meglumine antimoniate`, `sodium stibogluconate`, `miltefosine`, and `rituximab` (for leukemia cutis), while stripping all mg/kg dosages and day counts.

### Strip (Log in `dropped_specifics`)
- Patient age, sex, and occupation (`"59-year-old male"`, `"32-year-old male laborer"`, `"52-year-old female"`).
- Geographic names and institutions (`"Tunisia"`, `"Nepal"`, `"University Hospital"`), calendar dates (`"September 2012"`, `"December 2018"`), and drug dosages (`"50 mg at the dose of 200 mg/kg/day for 15 days"`).
- Pipeline tokens (`"E1 confirmatory evidence"`, `"E2 specific evidence"`, `"C1_DEFINITIVE_REFUTING"`, `"F5_DISCOURSE_CONTEXT"`, `"VPD satisfied -> POSITIVE"`, `"-> NEGATIVE"`, `"-> EXCLUDED_NON_TARGET_CASE"`).

---

## 4. Worked Examples (Directly from `selected_case_ft_pofs/output_leishmaniasis.jsonl`)

### Example 1 — `POSITIVE` (`PMC7527865_07::Leishmaniasis`)
**Input Record:**
- `step12_dataset_label`: `"POSITIVE"`, `step5_concept_grounding`: `"Mucocutaneous leishmaniasis concurrent with melanoma"`
- `rationale`: `"A 59-year-old male presented with mucosal ulcers and cutaneous lesions with confirmed positive Montenegro test and positive PCR for Leishmania (E1 confirmatory evidence), concurrent with a diagnosed plantar melanoma. VPD satisfied -> POSITIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC7527865_07::Leishmaniasis",
  "case_id": "PMC7527865_07",
  "target_disease": "Leishmaniasis",
  "dataset_label": "POSITIVE",
  "ground_truth_reasoning": "Leishmaniasis (mucocutaneous leishmaniasis). Reasoning: (1) Clinical presentation with ulcerative cutaneous lesions and oral mucosal ulceration is accompanied by a positive Montenegro intradermal skin test demonstrating delayed-type hypersensitivity to Leishmania antigens. (2) Molecular testing by polymerase chain reaction (PCR) on lesion tissue confirms Leishmania DNA, establishing active mucocutaneous leishmaniasis managed with intravenous liposomal amphotericin B alongside concurrent plantar melanoma. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {
      "text": "Clinical presentation with ulcerative cutaneous lesions and oral mucosal ulceration is accompanied by a positive Montenegro intradermal skin test demonstrating delayed-type hypersensitivity to Leishmania antigens.",
      "source": "both"
    },
    {
      "text": "Molecular testing by polymerase chain reaction (PCR) on lesion tissue confirms Leishmania DNA, establishing active mucocutaneous leishmaniasis managed with intravenous liposomal amphotericin B alongside concurrent plantar melanoma.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "59-year-old male — demographics",
    "University Hospital, December 2018, After seven days — institution and timeline",
    "50 mg at the dose of 200 mg/kg/day for 15 days, (Figure 4) — dosage, duration, and figure citation",
    "E1 confirmatory evidence, VPD satisfied -> POSITIVE — pipeline jargon stripped"
  ]
}
```

### Example 2 — `NEGATIVE` Rewritten to `OUT_OF_SCOPE` (`PMC10699217_01::Leishmaniasis`)
**Input Record:**
- `step12_dataset_label`: `"NEGATIVE"`, `step5_concept_grounding`: `"Cutaneous leishmaniasis (ruled out) in favor of small lymphocytic lymphoma / leukemia cutis"`
- `rationale`: `"A 52-year-old female had an ulcerative forearm nodule clinically suspected of cutaneous leishmaniasis. Giemsa-stained smears and histopathological examination were negative and rejected CL, establishing an alternative diagnosis of leukemia cutis (SLL/CLL stage I) responsive to rituximab. Leishmaniasis is explicitly ruled out -> NEGATIVE."`

**Target Output:**
```json
{
  "pair_id": "PMC10699217_01::Leishmaniasis",
  "case_id": "PMC10699217_01",
  "target_disease": "Leishmaniasis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Leukemia cutis / small lymphocytic lymphoma — Not Leishmaniasis). Reasoning: (1) An ulcerative cutaneous forearm nodule in an endemic setting initially raises clinical suspicion of cutaneous leishmaniasis, but Giemsa-stained skin smear microscopy is negative for Leishmania amastigotes. (2) Incisional skin biopsy histopathology and immunohistochemistry reveal a dense monomorphous dermal lymphocytic infiltration diagnostic of leukemia cutis (small lymphocytic lymphoma / chronic lymphocytic leukemia) rather than cutaneous leishmaniasis. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "An ulcerative cutaneous forearm nodule in an endemic setting initially raises clinical suspicion of cutaneous leishmaniasis, but Giemsa-stained skin smear microscopy is negative for Leishmania amastigotes.",
      "source": "both"
    },
    {
      "text": "Incisional skin biopsy histopathology and immunohistochemistry reveal a dense monomorphous dermal lymphocytic infiltration diagnostic of leukemia cutis (small lymphocytic lymphoma / chronic lymphocytic leukemia) rather than cutaneous leishmaniasis.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "52-year-old female — demographics",
    "C1_DEFINITIVE_REFUTING, -> NEGATIVE — pipeline jargon stripped"
  ]
}
```

### Example 3 — `EXCLUDED_NON_TARGET_CASE` Rewritten to `OUT_OF_SCOPE` (`PMC6600853_01::Leishmaniasis`)
**Input Record:**
- `step12_dataset_label`: `"EXCLUDED_NON_TARGET_CASE"`, `failure_flags`: `["F5_DISCOURSE_CONTEXT"]`
- `rationale`: `"A 50-year-old female presented with cryptococcal meningitis. Visceral leishmaniasis is mentioned solely as institutional administrative context because the hospital sought liposomal amphotericin B from Nepal's government VL program. The patient did not have leishmaniasis -> EXCLUDED_NON_TARGET_CASE."`

**Target Output:**
```json
{
  "pair_id": "PMC6600853_01::Leishmaniasis",
  "case_id": "PMC6600853_01",
  "target_disease": "Leishmaniasis",
  "dataset_label": "OUT_OF_SCOPE",
  "ground_truth_reasoning": "OUT_OF_SCOPE (Cryptococcal meningitis — Not Leishmaniasis). Reasoning: (1) Active central nervous system infection is diagnosed as cryptococcal meningitis requiring antifungal therapy with liposomal amphotericin B. (2) Visceral leishmaniasis is mentioned solely as administrative drug-procurement context regarding a public visceral leishmaniasis treatment program, with no Leishmania infection present. -> OUT_OF_SCOPE diagnosis confirmed.",
  "claims": [
    {
      "text": "Active central nervous system infection is diagnosed as cryptococcal meningitis requiring antifungal therapy with liposomal amphotericin B.",
      "source": "rationale"
    },
    {
      "text": "Visceral leishmaniasis is mentioned solely as administrative drug-procurement context regarding a public visceral leishmaniasis treatment program, with no Leishmania infection present.",
      "source": "both"
    }
  ],
  "dropped_specifics": [
    "50-year-old female — demographics",
    "government of Nepal, single dose of 10 mg/kg — geographic location and drug dosage",
    "-> EXCLUDED_NON_TARGET_CASE — pipeline jargon stripped"
  ]
}
```

---

## 5. Pre-Emission Checklist (`Leishmaniasis`)
- Verify all `30` rows are emitted (`20` `"POSITIVE"`, `10` `"OUT_OF_SCOPE"`).
- Confirm that non-single-patient introduction segments (`PMC6850740_01`, `PMC7527865_01`) are emitted as `"OUT_OF_SCOPE"` with self-contained explanations that the text segment contains only general epidemiological background without an active patient diagnosis.
- Ensure zero pipeline codes (`C1_DEFINITIVE_REFUTING`, `E1`, `E2`, `F5_DISCOURSE_CONTEXT`) and zero deictic pronouns remain.


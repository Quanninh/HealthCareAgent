---
name: gt-reasoning-rabies
description: >
  Constructs generalized ground_truth_reasoning, atomic claims, and dropped_specifics
  for Rabies cases in selected_case/output_rabies.jsonl by decoding E1/E2/E3
  evidence tiers from step9_key_evidence, stripping VPD/schema boilerplate from
  rationale, normalizing POSITIVE keywords, and generalizing case-specific details
  for RAGAS evaluation.
---

# Ground Truth Reasoning Extraction Skill — Rabies

## Target Disease & Data Scope
- **Target Disease:** `Rabies` (*Rabies virus [Lyssavirus] infection, including furious/encephalitic rabies and paralytic [dumb] rabies*)
- **Source File:** `selected_case/output_rabies.jsonl` (3 positive cases)
- **Reference Evidence Matrix:** `skills/disease-agent-rabies/SKILL.md` (`03_evidence_specificity_matrix.md` §5.13)
- **Goal:** Transform instance-specific `step9_key_evidence` and `rationale` into a generalized, schema-free `ground_truth_reasoning` string and atomic `claims` list suitable for evaluating `<Disease Name> + <Reasoning>` in the RAGAS framework.

---

## 1. Entity-to-Tier Mapping (`step9_key_evidence` → Diagnostic Tier)

Use the table below to classify every `evidence_item` in `step9_key_evidence.evidence_items` and to replace encoded tier references (`E1`, `E2`) in `rationale`.

### 1.1 Tier Definitions & Observed `step9_key_evidence` Entities in `output_rabies.jsonl`

| Tier in `skills/disease-agent-rabies` | Diagnostic Role (Decoded Phrase) | Matching `test_name` Entities in `output_rabies.jsonl` | Matching `target_concept` & `specimen` |
|---|---|---|---|
| **E1 — Confirmatory (`E1_CONFIRMATORY` / `E1_CONFIRMATORY_LAB`)** | **Post-mortem gold standard:** Detection of rabies virus antigen by fluorescent antibody test (FAT) or pathognomonic intracytoplasmic eosinophilic inclusions (Negri bodies) in brain/neural axis tissue on autopsy histopathology.<br>**Antemortem confirmatory:** Detection of rabies virus antigen in cutaneous nerve twigs of a nuchal (nape of the neck) skin biopsy, corneal impression, or CSF; molecular amplification of rabies virus RNA in saliva (RT-PCR or NASBA); or detection of rabies virus neutralizing antibodies in CSF (and serum) by Rapid Fluorescent Focus Inhibition Test (RFFIT) | `Post-mortem histopathology (Autopsy)`, `Rabies antigen detection` (nuchal skin/corneal biopsy or CSF), `Rabies virus RNA NASBA` (saliva), `Rapid Fluorescent Focus Inhibition Test (RFFIT)` (CSF and serum) | **Target:** `Negri bodies (Rabies virus)`, `Rabies virus`, `Rabies virus RNA`, `Rabies virus neutralizing antibodies`<br>**Specimen:** `brain and neural axis`, `nape of the neck and cornea biopsy`, `CSF`, `saliva`, `serum and CSF` |
| **E2 — Strong / Highly Specific (`E2_HIGHLY_SPECIFIC`)** | Markedly elevated or rising rabies virus antibody titers in paired serum samples integrated with a classic encephalitic or paralytic clinical syndrome (note: serum antibodies after rabies post-exposure vaccination must be interpreted alongside a significant titer rise, CSF antibodies, or direct antigen detection) | `Rabies virus antibody titer (paired sera)` | **Target:** `Rabies virus`<br>**Specimen:** `serum` (`result: "POSITIVE (> 1:60,000 dilution)"`) |
| **E3 — Supportive (in `rationale`)** | Acute progressive encephalomyelitis (furious encephalopathy with hydrophobia/aerophobia/autonomic instability or acute ascending flaccid paralysis mimicking Guillain-Barré syndrome in paralytic rabies) following a bite or scratch from a rabid animal (e.g., dog bite) | Mentioned in `rationale` and `source_quote` | Clinical syndrome, animal bite exposure |

### 1.2 Special Diagnostic Rules for Rabies (`output_rabies.jsonl`)
1. **Multi-Modal Antemortem Testing Principle (`PMC4947331_01`, `PMC3162835_02`, `PMC1282576_01`):**
   - Per WHO and CDC guidance (`03_evidence_specificity_matrix.md` §5.13), no single antemortem test is universally sensitive in humans because viral shedding in saliva/urine is intermittent (e.g., in `PMC1282576_01`, rabies virus RNA was detected by NASBA in saliva *but not in urine*).
   - **Rule:** When antemortem tests are used, state the general principle: *"Antemortem diagnosis of human rabies relies on a combination of specialized assays, including detection of rabies virus antigen in cutaneous nerve twigs from a nuchal skin biopsy, corneal impressions, or CSF; molecular amplification of viral RNA (e.g., by RT-PCR or NASBA) in saliva (as viral shedding in fluids such as urine is intermittent); and detection of rabies virus neutralizing antibodies in CSF and serum (e.g., by RFFIT)."*
2. **CSF Neutralizing Antibodies (`PMC3162835_02`):**
   - In `PMC3162835_02`, `step9_key_evidence` labels `Rapid Fluorescent Focus Inhibition Test (RFFIT)` on `serum and CSF` as `E1_CONFIRMATORY`, while `rationale` refers to it as `(E2 strong evidence)`. In clinical neurology/virology, rabies neutralizing antibodies in **CSF** are diagnostic of CNS rabies infection (even in vaccinated individuals, since vaccine alone does not produce high CSF neutralizing titers). Decode this cleanly without `E1`/`E2` tags as *"Detection of rabies virus neutralizing antibodies in both serum and CSF by the Rapid Fluorescent Focus Inhibition Test (RFFIT) provides strong immunological confirmation of central nervous system rabies infection."*

---

## 2. Rules for Decoding `rationale`, Stripping `VPD`, and Handling `POSITIVE`

### 2.1 Replace Encoded Tier Keywords (`E1`, `E2`) in `rationale`
All 3 rows in `output_rabies.jsonl` contain explicit `E1` and `E2` markers in `rationale`. Replace them as follows:
- `(E1 confirmatory)` → **`(definitive antemortem laboratory confirmation)`**
- `(E1 confirmatory gold standard)` → **`(the post-mortem histopathological gold standard)`**
- `(E2 strong evidence)` → **`(strong serological/immunological confirmation)`**

### 2.2 Strip `VPD` and Annotation Pipeline Boilerplate
All 3 rows in `output_rabies.jsonl` end with two protocol validation sentences (note the Unicode arrow `→`). Strip **both** sentences completely:
- `Primary diagnosis of rabies encephalitis affirmed, current episode, primary patient, no contradictions.`
- `Primary diagnosis confirmed, current episode, primary patient, no contradiction.`
- `Primary diagnosis affirmed in current episode of primary patient.`
- `VPD fully satisfied → POSITIVE.`

### 2.3 Handle `POSITIVE` Keywords
- Conclude `ground_truth_reasoning` with `-> POSITIVE diagnosis confirmed.` (using standard ASCII `->`).

---

## 3. Generalization & Values/Numbers Rules (`dropped_specifics`)

### 3.1 VALUES AND NUMBERS — Apply This Rule to Every Number Encountered
1. **STRIP if the number describes THIS PATIENT's measurement or circumstance** (log in `dropped_specifics`):
   - Age (`13-year-old boy`, `6-year-old girl`, `18-year-old male`)
   - Specific country, city, or reference laboratory (`AFMC Pune`, `NIMHANS Bengaluru`)
   - Exact patient dilution titer (`"> 1:60,000 dilution"`)
   - Exact hospitalization or post-bite timeline in this patient (`"after 45 days of vaccine treatment"`, `"died after 12 days of hospitalization / 15 days after first clinical onset"`)

2. **KEEP if the number is a GENERAL CLINICAL THRESHOLD or RULE that a guideline would state verbatim:**
   - WHO protective/neutralizing antibody cutoff if stated (`"RFFIT neutralizing antibody ≥0.5 IU/mL"`, `"≥4-fold titer rise in paired sera"`)

3. **WHEN IN DOUBT: convert the patient value into its general clinical interpretation (NEVER drop the clinical interpretation just because the number was stripped):**
   - `"paired sera titer > 1:60,000 dilution"` → `"markedly elevated anti-rabies virus antibody titers in paired serum samples (far exceeding post-vaccination levels)"`

### 3.2 Specify the Clinical Phenotype in the Header
- Encephalitic rabies: `"Rabies encephalitis (Rabies virus infection). Reasoning: ..."`
- Paralytic rabies: `"Paralytic rabies (Rabies virus infection). Reasoning: ..."`

---

## 4. Output Format & Worked Examples

### 4.1 Worked Example 1 — Rabies Encephalitis Confirmed by Nuchal/Corneal Biopsy Antigen (`E1`) & Paired Sera (`E2`) (`PMC4947331_01::Rabies`)

**INPUT (from `selected_case/output_rabies.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Rabies virus antibody titer (paired sera)", result: "POSITIVE (> 1:60,000 dilution)", strength: "E2_HIGHLY_SPECIFIC", target_concept: "Rabies virus", specimen: "serum"}`
  - `{test_name: "Rabies antigen detection", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Rabies virus", specimen: "nape of the neck and cornea biopsy"}`
- `rationale`:
  `"A 13-year-old boy presented with encephalopathy following a dog bite. Rabies virus antigen was detected in nerve twigs from a nape of neck/corneal biopsy (E1 confirmatory), and paired sera showed antibody titers > 1:60,000 (E2 strong evidence). Primary diagnosis of rabies encephalitis affirmed, current episode, primary patient, no contradictions. VPD fully satisfied → POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Rabies encephalitis (Rabies virus infection). Reasoning: (1) Acute progressive encephalopathy following a dog bite is the classic clinical and epidemiological presentation of encephalitic rabies. (2) Antemortem detection of rabies virus antigen in peripheral nerve twigs from a nuchal (nape of the neck) skin biopsy and corneal impression provides definitive laboratory confirmation of rabies encephalitis. (3) Markedly elevated anti-rabies virus antibody titers in paired serum samples provide strong serological evidence supporting the diagnosis. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Acute progressive encephalopathy following a dog bite is the classic clinical and epidemiological presentation of encephalitic rabies.", "source": "rationale"},
    {"text": "Antemortem detection of rabies virus antigen in peripheral nerve twigs from a nuchal (nape of the neck) skin biopsy and corneal impression provides definitive laboratory confirmation of rabies encephalitis.", "source": "step9"},
    {"text": "Markedly elevated anti-rabies virus antibody titers in paired serum samples provide strong serological evidence supporting the diagnosis.", "source": "step9"}
  ],
  "dropped_specifics": ["13-year-old boy", "exact patient antibody titer > 1:60,000 dilution (converted to markedly elevated titers in paired sera)", "45 days post-vaccine timing", "AFMC Pune and NIMHANS Bengaluru reference laboratory names"]
}
```

### 4.2 Worked Example 2 — Paralytic Rabies Confirmed by Saliva NASBA (`E1`) & Autopsy Negri Bodies (`E1`) (`PMC1282576_01::Rabies`)

**INPUT (from `selected_case/output_rabies.jsonl`):**
- `step9_key_evidence`:
  - `{test_name: "Rabies virus RNA NASBA", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Rabies virus RNA", specimen: "saliva", source_quote: "Paralytic rabies was then suspected and rabies virus RNA was demonstrable in saliva but not in the urine by nucleic acid sequence based amplification technique (3)."}`
  - `{test_name: "Post-mortem histopathology (Autopsy)", result: "POSITIVE", strength: "E1_CONFIRMATORY", target_concept: "Negri bodies (Rabies virus)", specimen: "brain and neural axis"}`
- `rationale`:
  `"An 18-year-old male presented with pneumomediastinum and paralytic rabies. Antemortem testing demonstrated rabies virus RNA in saliva by NASBA (E1 confirmatory), and autopsy revealed widespread Negri bodies throughout the whole neural axis (E1 confirmatory gold standard). Primary diagnosis affirmed in current episode of primary patient. VPD fully satisfied → POSITIVE."`

**OUTPUT:**
```json
{
  "ground_truth_reasoning": "Paralytic rabies (Rabies virus infection). Reasoning: (1) Rabies can present in the paralytic form with ascending flaccid paralysis and autonomic or respiratory complications such as spontaneous pneumomediastinum. (2) Antemortem molecular detection of rabies virus RNA in saliva by nucleic acid sequence-based amplification (NASBA) provides definitive virological confirmation; negative urine testing does not exclude rabies due to intermittent site-specific viral shedding. (3) Post-mortem histopathological demonstration of widespread Negri bodies throughout the brain and neural axis on autopsy is a classic gold-standard pathological confirmation of rabies. -> POSITIVE diagnosis confirmed.",
  "claims": [
    {"text": "Rabies can present in the paralytic form with ascending flaccid paralysis and autonomic or respiratory complications such as spontaneous pneumomediastinum.", "source": "rationale"},
    {"text": "Antemortem molecular detection of rabies virus RNA in saliva by nucleic acid sequence-based amplification (NASBA) provides definitive virological confirmation; negative urine testing does not exclude rabies due to intermittent site-specific viral shedding.", "source": "step9"},
    {"text": "Post-mortem histopathological demonstration of widespread Negri bodies throughout the brain and neural axis on autopsy is a classic gold-standard pathological confirmation of rabies.", "source": "step9"}
  ],
  "dropped_specifics": ["18-year-old male", "death after 12 days of hospitalization (15 days after clinical onset)", "citation (3)"]
}
```

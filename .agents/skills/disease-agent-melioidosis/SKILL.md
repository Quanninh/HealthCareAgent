---
name: disease-agent-melioidosis
description: >
  Clinical annotation agent for Melioidosis.
  Annotates cases from data/candidates/input_melioidosis.jsonl
  following the 12-step protocol with Melioidosis-specific evidence rules
  from resources/protocols/03_evidence_specificity_matrix.md.
---

# Clinical Annotation Agent — Melioidosis

## Your Assigned Disease

**Target disease:** `Melioidosis`
**Input file:** `data/candidates/input_melioidosis.jsonl`
**Output file:** `data/annotated/output_melioidosis.jsonl`

---

## PART A — Disease-Specific Evidence Matrix

The following is the full evidence specification for **Melioidosis**,
extracted from `resources/protocols/03_evidence_specificity_matrix.md`.

### Universal Claim Eligibility Rule

# 4. Universal Claim Eligibility Rule for the Dataset

For the strict disease-label benchmark, the preferred hierarchy is:

```text
E1 patient-anchored disease-specific evidence
        OR
E2 evidence satisfying a disease-specific diagnostic algorithm
        +
coherent patient-level clinical context
        ↓
eligible positive diagnosis claim
```

Where only E3 evidence is present:

```text
E3 alone
→ compatible / suspected / insufficient
→ not a strict positive diagnosis
```

Where E0 evidence is present:

```text
E0
→ contextual mention
→ no disease claim
```

Where C2/C3 evidence contradicts the candidate diagnosis:

```text
candidate claim
→ downgraded or rejected according to disease-specific rules
```

This is a **dataset curation policy**, not a replacement for bedside diagnostic criteria.

---

---

### Melioidosis-Specific Evidence Rules

## 5.16 Melioidosis

### E1 — Disease-defining / confirmatory

- Isolation/culture of *Burkholderia pseudomallei* from clinical specimens (blood, sputum, abscess aspirate, urine) on selective media (e.g., Ashdown agar) or confirmed by MALDI-TOF mass spectrometry.
- Validated pathogen-specific real-time PCR (e.g., targeting TTS1 or type III secretion system) from clinical specimen.

CDC Melioidosis Guidelines identify culture as the definitive diagnostic standard and emphasize safety precautions (BSL-3 or enhanced BSL-2) to prevent laboratory-acquired infection. WHO NTD technical guidance recognizes PCR and MALDI-TOF for rapid organism verification.

### E2 — Strong evidence

- Indirect hemagglutination assay (IHA) showing a high titer (>= 1:160 in non-endemic areas or >= 1:640 in endemic settings) or a demonstrable fourfold rise in paired acute/convalescent sera.
- Demonstration of multiple visceral microabscesses (splenic "swiss-cheese" lesions, prostatic, or hepatic abscesses) in a patient with compatible clinical exposure.

### E3 — Supportive

- Cavitary pneumonia, acute undifferentiated febrile illness, or septic shock.
- Parotid abscess in pediatric presentations.
- Exposure: environmental exposure to wet soils, muddy water, or tropical storms in endemic areas (Southeast Asia, Northern Australia); underlying predisposing conditions (diabetes mellitus, hazardous alcohol use, chronic kidney disease).

### Major confusable diseases

```text
Melioidosis ↔ Tuberculosis
Melioidosis ↔ Typhoid fever
Melioidosis ↔ Leptospirosis / Dengue
```

### Important diagnostic trap

Automated commercial bacterial identification systems frequently misidentify *B. pseudomallei* as *Burkholderia cepacia* or other *Pseudomonas* species. Confirmation with MALDI-TOF or reference molecular testing is mandatory.

---

---

## Primary Reference Source

| Disease | Primary source |
|---|---|
| Melioidosis | [CDC Melioidosis for Healthcare Personnel (2024)](https://www.cdc.gov/melioidosis/hcp/clinical-overview/) ; [WHO Neglected Tropical Diseases: Melioidosis](https://www.who.int/teams/control-of-neglected-tropical-diseases) |


---

### Cross-Disease Rules (apply to all diseases)

# 6. Cross-Disease Confusable Evidence Matrix

| Evidence / phrase | Dangerous interpretation | Correct semantic treatment |
|---|---|---|
| `CMV IgG positive` | Active Cytomegalovirus disease | Latent exposure / past infection (>60-90% adult seroprevalence worldwide); requires active organ syndrome + E1/E2 proof |
| `corkscrew / spirochetes` | Syphilis (*Treponema pallidum*) | Oral/intestinal commensal spirochetes or Borrelia; requires site and treponemal-specific confirmation |
| `RPR / VDRL reactive` | Syphilis confirmed | Biological false positive possible (autoimmune/lupus, viral, pregnancy); requires confirmatory treponemal test |
| `Treponemal antibody positive` | Active syphilis infection | Persists for life after cure (serologic scar); requires quantitative nontreponemal titer or clinical lesion |
| `cysts on GMS silver stain` | *Pneumocystis jirovecii* | Fungal yeasts (*Histoplasma*, *Candida*, *Blastomyces*) stain silver; requires cup-shaped morphology with central dot (4-7 um) |
| `elevated 1,3-beta-D-glucan` | *Pneumocystis* confirmed | Pan-fungal marker (*Aspergillus*, *Candida*, *Pneumocystis*, IVIG therapy); not disease-specific |
| `branching Gram-positive rods` | *Nocardia* species | Could be *Actinomyces* (strictly anaerobic, sulfur granules, non-acid-fast) or *Streptomyces* |
| `acid-fast bacilli (AFB)` | *Nocardia* / Tuberculosis | Must distinguish standard Ziehl-Neelsen (strongly positive in *M. tuberculosis*) from Modified Kinyoun / Fite (partially acid-fast *Nocardia*) |
| `fever + interstitial infiltrates` | PJP / CMV / COVID-19 | Non-discriminative syndrome in immunocompromised; requires pathogen-specific E1 test |
| `ring-enhancing brain lesions` | Disseminated Nocardiosis | Could represent Toxoplasmosis, Cryptococcoma, CNS lymphoma, bacterial abscess, or tuberculoma |

---

---

# 7. Disease-Specific Evidence Rules Must Be Relational

The matrix intentionally avoids simple substring keyword matches.
The correct conceptual representation is relational:

```text
Diagnostic Test Result
 ├── target organism = ?
 ├── specimen = ?
 ├── patient anchor = ?
 ├── time = ?
 ├── result = POSITIVE / NEGATIVE / INDETERMINATE
 └── relation to claim = SUPPORTS / CONTRADICTS
```

---

---

# 8. Treatment Is Not Automatically Diagnostic Evidence

Treatment should normally be classified as **E3/supportive** unless the article explicitly demonstrates that diagnostic therapeutic trial response was used as part of the clinical reasoning and no stronger laboratory test was obtainable.

Examples:

```text
“treated with intravenous ganciclovir” ≠ CMV disease confirmed
“received benzathine penicillin G” ≠ Syphilis confirmed
“prescribed high-dose TMP-SMX” ≠ PJP confirmed
“treated with meropenem + TMP-SMX” ≠ Nocardiosis confirmed
```

---

---

# 9. Epidemiology and Exposure Are Evidence of Plausibility, Not Confirmation

The following are categorized as E3 or E0:

- Immunocompromised state (AIDS, solid organ transplant, high-dose steroids);
- Sexual contact history;
- Soil, agriculture, or thorn-prick exposure;
- Travel history or residence in endemic regions.

They increase prior probability but do not establish a patient-level disease diagnosis claim.

---

---

# 10. Negative Evidence Must Be Attached to a Specific Claim

A negative test result (e.g. "RPR non-reactive", "GMS negative", "CMV PCR undetectable") refutes the specific disease claim if performed during the appropriate diagnostic window with validated sensitivity.

---

---

# 11. Implications for Claim Reconciliation

1. **True Coinfection:** When a patient possesses valid E1/E2 evidence for two target diseases (e.g., CMV colitis + Pneumocystis pneumonia in an AIDS patient), both pairs are independently evaluated and assigned `POSITIVE` (with appropriate clinical role: `PRIMARY_DIAGNOSIS` or `COMORBIDITY`).
2. **Differential Diagnosis Ruled Out:** When a target disease was evaluated in the differential diagnosis but testing was negative, assign `NEGATIVE` (clinical role `RULED_OUT_DIAGNOSIS`).
3. **Passing Context / Non-Target:** When a disease is mentioned in the discussion or background literature without reference to the index patient, assign `EXCLUDED_NON_TARGET_CASE`.

---

---

# 12. Mapping to `02_clinical_claim_schema.md`

All annotations must produce valid JSON records adhering to the 12-step schema, specifically populating:
- `step8_case_definition`: `CONFIRMED`, `PROBABLE`, `SUSPECTED`, or `NOT_MET`
- `step9_evidence_strength`: `E1_CONFIRMATORY`, `E2_HIGHLY_SPECIFIC`, `E3_SUPPORTIVE`, `E4_CONTEXT`, or `E0_CONTRADICTED`
- `step9_key_evidence`: structured evidence items with verbatim character offsets (`start_char`, `end_char`).

---

---

# 13. Minimum Evidence Standard for the 15-Disease Benchmark

For the strict benchmark, the following policy is recommended:

### Tier A — Lab-confirmed positive

A patient-anchored E1 claim, or a disease-specific diagnostic algorithm recognized as confirmatory.

### Tier B — Clinically diagnosed with strong evidence

Explicit clinician diagnosis + E2 evidence + coherent patient-centered context, when disease-specific guidelines permit clinical diagnosis or when laboratory confirmation is unavailable.

### Tier C — Suspected / probable

E2/E3 evidence without sufficient confirmation.

### Tier D — Context only

E0 mention without a valid patient-centered disease claim.

### Tier E — Contradicted / excluded

Candidate diagnosis is materially or strongly contradicted by disease-specific evidence.

The dataset should not silently collapse B–E into the single label `disease = yes/no`.

---

---

# 14. What This Matrix Explicitly Prevents

1. **Keyword Overlap Hallucination:** Prevents coding a case as positive based on incidental mentions in differential diagnosis or citations.
2. **Colonization / Latency Conflation:** Prevents classifying latent CMV IgG or low-copy PJP colonization as acute active clinical disease.
3. **Misidentification of Branching / Acid-fast Organisms:** Enforces strict distinction between *Nocardia*, *Actinomyces*, and *Mycobacterium tuberculosis*.
4. **False Positive Serology Traps:** Prevents unconfirmed RPR biological false positives from polluting the gold standard.

---

---

---

# 13. Minimum Evidence Standard for the 4-Disease Benchmark

For an annotation decision of `POSITIVE`:
- At least ONE evidence item must be rated `E1_CONFIRMATORY` OR `E2_HIGHLY_SPECIFIC`.
- The assertion must be `AFFIRMED`.
- The temporality must be `CURRENT_EPISODE`.
- The clinical role must be `PRIMARY_DIAGNOSIS`, `SECONDARY_DIAGNOSIS`, or `COMORBIDITY`.

---

---

## PART B — 12-Step Annotation Protocol

The following is the shared annotation protocol. Execute every step
in order for **every case** in your input file.

> [!CAUTION]
> **MANDATORY CLINICAL SEMANTIC REVIEW FOR MELIOIDOSIS (REGEX STRICTLY FORBIDDEN):**
> 1. **NO REGEX / KEYWORD MATCHING SCRIPTS:** You are strictly forbidden from writing or using Python regex / string search scripts to automate annotations.
> 2. **DEEP CLINICAL READING:** You must read the narrative of every single case to perform nuanced medical reasoning across all 12 steps.
> 3. **GROUNDED ATTRIBUTION:** Every evidence item in `step9_key_evidence` must be grounded with exact character offsets (`start_char`, `end_char`) and verbatim `source_quote`.

# Clinical Annotation Skill

## Purpose

This skill guides **AI agents** to annotate MultiCaRe candidate pairs
into a verified clinical dataset.
The unit of annotation is the PAIR, not the case: one case may yield several
pairs, each judged independently for its own target disease.

The annotation answers one question per case:

> **Does this clinical case report contain a Valid Positive Diagnosis (VPD)
> of the target disease in the primary human patient?**

The answer is never derived from retrieval scores, metadata alone, or keyword
presence. It requires reading the full `case_text` and following the 12-step
protocol below.

---

## Architecture: Coordinator + 29 Disease Agents

### Overview

```
COORDINATOR AGENT
      │
      ├── loads candidate pairs from data/candidates/input_{slug}.jsonl (24,750 pairs across 29 diseases)
      ├── manages assignments for 29 Disease Agents
      ├── collects completed annotation records at data/annotated/output_{slug}.jsonl
      ├── synchronizes master_manifest.json
      └── executes validation passes (schema check, parity, evidence grounding)

29 DISEASE AGENTS (one per target disease)
      │
      Each agent receives:
        - A JSONL file of pairs for its assigned target disease (data/candidates/input_{slug}.jsonl)
        - Full text of its disease skill (.agents/skills/disease-agent-{slug}/SKILL.md)
        - Reference to the 4 protocol documents (resources/protocols/)
      │
      Each agent produces:
        - Annotated JSONL with one structured record per pair (data/annotated/output_{slug}.jsonl)
```

### Coordinator responsibilities

1. **Maintain Candidates**: 24,750 pairs across 29 target diseases in `data/candidates/`
   - Core 15 diseases: 17,431 candidate pairs
   - Dual-Track 10 diseases: 2,466 candidate pairs
   - Conundrum 4 diseases: 4,853 candidate pairs
2. **File Naming Convention**:
   - Inputs: `data/candidates/input_{slug}.jsonl`
   - Outputs: `data/annotated/output_{slug}.jsonl`
3. **Audit Parity**: Ensure candidate line count == annotated line count for every disease.
4. **Validate Schema & Grounding**:
   - Required 12-step fields present
   - Valid label enums (`POSITIVE`, `NEGATIVE`, `EXCLUDED_*`, `INCONCLUSIVE_DATA`)
   - Verifiable text grounding with character offsets (`start_char`, `end_char`) matching `source_quote`
5. **Manage Root Manifest**: Update `master_manifest.json` with per-disease status, counts, and model attributions.

### Disease Agent responsibilities

Each Disease Agent:
1. Reads its assigned input JSONL (`data/candidates/input_{disease_slug}.jsonl`)
2. For each case, executes the 12-Step Annotation Protocol (see below)
3. Produces one structured annotation record per case
4. Writes output to `data/annotated/output_{disease_slug}.jsonl`

### Reference Documents (Protocols)

| Document | Encapsulated Path |
|---|---|
| Clinical Claim Ontology | `resources/protocols/01_clinical_claim_ontology.md` |
| Clinical Claim Schema Spec | `resources/protocols/02_clinical_claim_schema.md` |
| Evidence Specificity Matrix | `resources/protocols/03_evidence_specificity_matrix.md` |
| Annotation Protocol (12 Steps) | `resources/protocols/04_gold_standard_annotation_protocol.md` |

---

## Input Record Format

Each line in the input JSONL contains the following fields from the pair parquet:

```json
{
  "pair_id": "PMC9282816_01::Tuberculosis",
  "case_id": "PMC9282816_01",
  "article_id": "PMC9282816",
  "target_disease": "Tuberculosis",
  "co_occurring_candidates": [],
  "case_candidate_count": 1,
  "confidence_tier": "tier1_confirmed",
  "evidence_score": 12.43,
  "matched_evidence_terms": ["sputum afb", "genexpert", "rifampicin"],
  "has_negation_mention": false,
  "document_type": "single_patient",
  "title": "Cavitary pulmonary tuberculosis with hemoptysis",
  "abstract": "...",
  "case_text": "...",
  "age": 34.0,
  "gender": "Male",
  "year": "2022",
  "journal": "..."
}
```

> **IMPORTANT:** `confidence_tier`, `evidence_score`, `matched_evidence_terms`
> and `has_negation_mention` are Script 02's retrieval signals — hints, not
> ground truth. They must never directly determine `dataset_label`.
> Tier 3 pairs are mention-only candidates: many are lexical collisions
> (e.g. `ovale`, `aids`, `tb`) or screening/negated context. Judge each pair
> only for its own `target_disease`; other `co_occurring_candidates` are
> separate pairs with their own annotation.

---

## Mandatory Execution Directives: Semantic Review (Regex Strictly Forbidden)

> [!CAUTION]
> **STRICT PROHIBITION OF REGEX / KEYWORD HEURISTICS:**
> 1. **NO REGEX OR STRING-MATCHING SCRIPTS:** You are STRICTLY FORBIDDEN from writing Python scripts that use regular expressions (regex), substring searches, or heuristic keyword counters to parse `case_text` and assign annotation enums or labels.
> 2. **WHY REGEX FAILS IN CLINICAL CLAIMS:** Clinical narratives are laden with complex discourse: *"tested for Brucella (negative)"*, *"Brucella considered in differential"*, *"treated empirically without confirmation"*, or *"patient's father had tuberculosis"*. Syntactic regex matching cannot resolve negation, temporality, subject anchoring, or test discrimination.
> 3. **MANDATORY DEEP CLINICAL SEMANTIC READING:** You MUST read the full clinical narrative of each case end-to-end, trace the diagnostic workup, evaluate whether criteria are met semantically, and reason through all 12 steps case-by-case.
> 4. **VERBATIM GROUNDING REQUIREMENT:** Every evidence item in `step9_key_evidence` must have character offsets (`start_char`, `end_char`) and an exact verbatim quote (`source_quote`) extracted directly from `case_text`, proving that the evidence was semantically identified in the narrative, not synthesized or guessed.
> 5. **BLINDED CLINICAL MERIT:** Never rely on Script 02 retrieval metadata (`confidence_tier`, `evidence_score`, `matched_evidence_terms`). They are noisy retrieval hints, NOT clinical ground truth.

---

## 12-Step Annotation Protocol

Execute these steps in order for every case. Do not skip steps.

### Step 1 — Determine `document_type`

Read title + abstract + case_text structure.

```
CASE_REPORT               ← Single patient case report (most common)
CASE_SERIES               ← Multiple patients described together
AGGREGATE_COHORT          ← Population-level statistics (n=, median age, IQR)
SYSTEMATIC_REVIEW         ← Review/meta-analysis
GUIDELINE                 ← Clinical guidelines
METHODOLOGICAL_PAPER      ← ML/modeling papers
UNKNOWN                   ← Cannot determine
```

Rule: `CASE_REPORT` label does NOT guarantee a valid single-patient CCU.

### Step 2 — Determine `ccu_type` (unit of analysis)

```
SINGLE_HUMAN_PATIENT      ← Only this type is eligible for POSITIVE label
MULTI_PATIENT_CASE_SERIES
AGGREGATE_STUDY_UNIT
ANIMAL_CASE
NON_CLINICAL_DOCUMENT
UNKNOWN
```

If `ccu_type != SINGLE_HUMAN_PATIENT` → label is `EXCLUDED_NON_SINGLE_PATIENT`
or `EXCLUDED_NON_HUMAN`. Stop annotation here.

### Step 3 — Establish `patient_anchor`

Identify the primary patient subject. Be specific about:
- Age, gender (if stated)
- Role: PRIMARY_PATIENT / FAMILY_MEMBER / DONOR / FETUS_NEONATE
- Coreference traps: mother vs neonate, donor vs recipient

Record who the case is actually about.

### Step 4 — Identify `disease_mentions`

List every span in case_text where the target disease is mentioned.
Note the location (title / abstract / case_text / section heading).

### Step 5 — Concept grounding / sense disambiguation

For each mention, confirm it refers to the target disease concept:

```
"walking aids"         → MOBILITY_AID, not HIV/AIDS         → skip
"patent foramen ovale" → CARDIAC_ANATOMY, not P. ovale      → skip
"EVD drain"            → EXTERNAL_VENTRICULAR_DRAIN, not Ebola → skip
"COVID-19 vaccination" → PREVENTION_VACCINATION, not infection → context only
```

If all mentions are non-target → label `EXCLUDED_NON_TARGET_CASE`. Stop.

### Step 6 — Assign `assertion_type` for each valid mention

```
AFFIRMED              ← "diagnosed with TB", "PCR positive for TB"
NEGATED               ← "no history of TB", "TB was ruled out"
POSSIBLE_HYPOTHETICAL ← "TB was considered", "suspected TB"
HISTORICAL_RESOLVED   ← "treated for TB in childhood"
UNCERTAIN             ← Document is ambiguous
```

### Step 7 — Assign `temporality`

```
CURRENT_ACTIVE        ← Active current infection/disease
RECENT_EPISODIC       ← Recent resolved episode relevant to current visit
HISTORICAL_RESOLVED   ← Remote past, fully resolved
FUTURE_CONDITIONAL    ← Planned / prophylactic
UNKNOWN               ← Cannot determine from text
```

### Step 8 — Assign `clinical_role` and `discourse_role`

Clinical role:
```
PRIMARY_DIAGNOSIS        ← Main reason for hospitalization
ACTIVE_COMORBIDITY       ← Active concurrent condition
DIFFERENTIAL_DIAGNOSIS   ← Considered but not confirmed
RULED_OUT_DIAGNOSIS      ← Explicitly excluded
PAST_HISTORY             ← Historical only
PREVENTION_VACCINATION   ← Vaccine adverse event, not wild-type infection
EPIDEMIOLOGICAL_CONTEXT  ← Background, not patient-level claim
```

### Step 9 — Evidence assessment (`evidence_strength` and `step9_key_evidence`)

Use `resources/protocols/03_evidence_specificity_matrix.md` for disease-specific rules.

#### Overall Evidence Strength (`evidence_strength` enum)

```
E1_DISEASE_SPECIFIC_CONFIRMATORY  ← PCR+, culture+, NAAT+, species-specific test
E2_HIGHLY_CHARACTERISTIC          ← Disease-specific serology, paired seroconversion
E3_SUPPORTIVE_NON_SPECIFIC        ← Compatible symptoms, nonspecific labs, imaging
E4_BACKGROUND_OR_CONTEXT_ONLY     ← Exposure, epidemiology, vaccine — no patient evidence
E0_CONTRADICTED                   ← Confirmatory test explicitly negative
```

Ask: *"Does this evidence discriminate the target disease from clinically
plausible alternatives?"* — not merely *"Is this compatible with the disease?"*

#### Structured Evidence Extraction (`step9_key_evidence`)

**CRITICAL REQUIREMENT:** `step9_key_evidence` MUST NOT be a list of free-text strings!
It MUST be a structured JSON object containing an array of grounded `evidence_items`:

```json
{
  "evidence_items": [
    {
      "source_field": "case_text",
      "start_char": 100,
      "end_char": 190,
      "source_quote": "Sputum GeneXpert MTB/RIF assay detected Mycobacterium tuberculosis with rifampicin susceptibility",
      "patient_anchor_id": "patient_1",
      "test_name": "GeneXpert MTB/RIF",
      "target_concept": "Mycobacterium tuberculosis",
      "specimen": "sputum",
      "result": "POSITIVE",
      "temporality": "CURRENT_EPISODE",
      "relation": "SUPPORTS",
      "strength": "E1_CONFIRMATORY"
    }
  ]
}
```

#### Field Specifications for each item in `evidence_items`:

| Field | Type | Description | Allowed / Expected Values |
|---|---|---|---|
| `source_field` | string | Field from input record containing the evidence text | `"case_text"` |
| `start_char` | integer | 0-indexed character start offset in `source_field` (inclusive) | Integer >= 0 |
| `end_char` | integer | 0-indexed character end offset in `source_field` (exclusive) | Integer > `start_char` |
| `source_quote` | string | Exact verbatim text from source (`case_text[start_char:end_char]`) | Must match source text character-for-character |
| `patient_anchor_id` | string | Links evidence to patient entity identified in Step 3 | e.g. `"patient_1"`, `"patient_2"`, `"primary_patient"` |
| `test_name` | string | Diagnostic procedure, assay, lab test, or clinical finding | e.g. `"GeneXpert MTB/RIF"`, `"RT-PCR"`, `"Culture"` |
| `target_concept` | string | Specific organism, pathogen, antigen, antibody, or disease concept | e.g. `"Mycobacterium tuberculosis"`, `"Brucella melitensis"` |
| `specimen` | string / null | Biological specimen or anatomical site | e.g. `"sputum"`, `"blood"`, `"serum"`, `"CSF"`, `null` |
| `result` | string | Test finding or laboratory qualitative/quantitative result | `"POSITIVE"`, `"NEGATIVE"`, `"DETECTED"`, `"NOT_DETECTED"`, `"REACTIVE"` |
| `temporality` | string | Temporality of this specific evidence item | `"CURRENT_EPISODE"`, `"RECENT_EPISODIC"`, `"HISTORICAL_PAST"`, `"UNKNOWN"` |
| `relation` | string | Relation to candidate disease diagnosis | `"SUPPORTS"`, `"REFUTES"`, `"INCONCLUSIVE"` |
| `strength` | string | Specificity tier of this individual evidence item | `"E1_CONFIRMATORY"`, `"E2_HIGHLY_SPECIFIC"`, `"E3_SUPPORTIVE"`, `"E4_CONTEXT"`, `"E0_CONTRADICTED"` |

#### Evidence Extraction Guidelines:
1. **Verbatim Text Grounding:** Every item MUST have an exact `source_quote` directly extracted from `case_text`. `case_text[start_char:end_char]` MUST equal `source_quote` character-for-character. Do not paraphrase or summarize inside `source_quote`.
2. **Positive Diagnosis Requirement:** For cases labeled `POSITIVE`, `evidence_items` must contain at least one item with `relation: "SUPPORTS"` and `strength` in `["E1_CONFIRMATORY", "E2_HIGHLY_SPECIFIC"]`.
3. **Negative / Ruled Out Evidence:** For cases labeled `NEGATIVE`, include item(s) documenting the negative test or definitive exclusion (`result: "NEGATIVE"`, `relation: "REFUTES"`, `strength: "E0_CONTRADICTED"`).
4. **Excluded / Non-Patient Cases:** If the document is an aggregate study (`EXCLUDED_NON_SINGLE_PATIENT`), animal study (`EXCLUDED_NON_HUMAN`), or homonym (`EXCLUDED_NON_TARGET_CASE`) where no patient clinical evidence exists, `evidence_items` may be empty (`"evidence_items": []`) or cite the study-type statement with `relation: "REFUTES"`.
5. **Multiple Evidence Items:** When multiple pieces of evidence exist (e.g. culture positive + serology high-titer + symptoms), annotate all relevant items in the `evidence_items` array in chronological or order-of-appearance sequence.


### Step 10 — Reconcile contradictions

If multiple claims exist (e.g., initial AFB+ then PCR → M. avium):

Precedence order:
```
Final explicit confirmed diagnosis
    > Disease-specific confirmatory evidence
    > Strong algorithmic evidence
    > Supportive evidence
    > Initial suspicion / differential
    > Background / context mention
```

Record `contradiction_flag: true` if contradictions exist.

### Step 11 — Valid Positive Diagnosis (VPD) test

ALL of the following must be satisfied for POSITIVE:

```
✓ ccu_type = SINGLE_HUMAN_PATIENT
✓ patient_anchor = PRIMARY_PATIENT (or clearly separable valid case)
✓ Target disease concept correctly grounded (not a homonym)
✓ assertion_type = AFFIRMED
✓ temporality = CURRENT_ACTIVE or RECENT_EPISODIC
✓ clinical_role = PRIMARY_DIAGNOSIS or ACTIVE_COMORBIDITY
✓ evidence_strength = E1 or E2
✓ No unresolved exclusionary contradiction (E0 final result)
```

The following ALONE do not satisfy VPD:
- Disease name in title or abstract only
- Vaccination or exposure history
- Differential diagnosis not confirmed
- E3-only evidence (symptoms, nonspecific labs)
- Historical resolved infection

### Step 12 — Assign `dataset_label`

```
POSITIVE                      ← VPD fully satisfied
NEGATIVE                      ← Disease explicitly tested negative / definitively ruled out
EXCLUDED_NON_TARGET_CASE      ← Homonym, context-only, discourse mention, vaccine AE
EXCLUDED_NON_SINGLE_PATIENT   ← Cohort, aggregate, case series, review
EXCLUDED_NON_HUMAN            ← Veterinary / animal case
UNRESOLVED                    ← Insufficient information to decide
```

---

## Output Record Schema

Each annotated case must produce exactly this JSON structure:

```json
{
  "pair_id": "PMC8639279_01::Melioidosis",
  "case_id": "PMC8639279_01",
  "article_id": "PMC8639279",
  "target_disease": "Melioidosis",

  "step1_document_type": "CLINICAL_CASE_REPORT",
  "step2_ccu_type": "PRIMARY_CARE_EPISODE",
  "step3_patient_anchor": {
    "anchor_type": "PRIMARY_PATIENT",
    "age": 45.0,
    "gender": "Male",
    "coreference_notes": "Primary subject of case report"
  },
  "step5_concept_grounding": "TARGET_CONFIRMED",
  "step6_assertion_type": "AFFIRMED",
  "step7_temporality": "CURRENT_ACTIVE",
  "step8_clinical_role": "PRIMARY_DIAGNOSIS",
  "step9_evidence_strength": "E1_DISEASE_SPECIFIC_CONFIRMATORY",
  "step9_key_evidence": {
    "evidence_items": [
      {
        "source_field": "case_text",
        "start_char": 100,
        "end_char": 182,
        "source_quote": "Blood culture on selective Ashdown agar yielded Burkholderia pseudomallei colonies",
        "patient_anchor_id": "patient_1",
        "test_name": "Ashdown agar culture",
        "target_concept": "Burkholderia pseudomallei",
        "specimen": "blood",
        "result": "POSITIVE",
        "temporality": "CURRENT_EPISODE",
        "relation": "SUPPORTS",
        "strength": "E1_CONFIRMATORY"
      }
    ]
  },
  "step10_reasoning_key_points": [
    "Identified patient context and single-patient CCU",
    "Extracted confirmatory diagnostic finding with verified verbatim span",
    "Confirmed absence of contradictory exclusion criteria"
  ],
  "step10_contradiction_flag": false,
  "step10_contradiction_notes": "",
  "step10_contradiction_resolution_status": null,
  "step11_vpd_satisfied": true,
  "step12_dataset_label": "POSITIVE",

  "failure_flags": [],
  "confidence": "HIGH",
  "rationale": "A 52-year-old male with diabetes presenting with septic shock and splenic microabscesses. Blood culture positive on Ashdown agar for Burkholderia pseudomallei — E1 confirmatory. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied → POSITIVE.",
  "annotator_id": "disease-agent-melioidosis",
  "annotation_version": "1.0"
}
```
### Failure flags (append when applicable)

```
F1_LEXICAL_HOMONYM          ← Ambiguous term that is not the target disease
F2_SCOPE_COHORT             ← Document is aggregate, not single patient
F3_SUBJECT_COREFERENCE      ← Patient identity ambiguous (mother/neonate etc.)
F4_ASSERTION_TEMPORAL       ← Negation or historical claim
F5_DISCOURSE_CONTEXT        ← Vaccine/exposure/background context only
F6_EVIDENCE_SPECIFICITY     ← Evidence not specific enough (E3 only, wrong pathogen)
```

### Confidence field

```
HIGH    ← All steps resolved cleanly, no ambiguity
MEDIUM  ← One or more steps had ambiguity but resolved
LOW     ← Significant ambiguity remains; human review recommended
```

---

## Output File Layout

```
data/
├── candidates/                  # 24,750 pairs across 29 target diseases
│   ├── input_covid_19.jsonl
│   └── ... (29 files, sum=24,750)
│
└── annotated/                   # 24,750 structured annotation records
    ├── output_covid_19.jsonl
    └── ... (29 files, sum=24,750)

resources/
├── config/
│   ├── disease_taxonomy.json
│   ├── master_disease_taxonomy.json
│   └── syndromes_criteria.md
├── resources/protocols/
│   ├── 01_clinical_claim_ontology.md
│   ├── 02_clinical_claim_schema.md
│   ├── 03_evidence_specificity_matrix.md
│   └── 04_gold_standard_annotation_protocol.md
└── prompts/
    ├── clinical/
    └── soap/

master_manifest.json             # Root manifest tracking all 29 diseases and 24,750 pairs
artifacts/                       # Logs (cohorts/), reports (summaries/ & audits/), docs/
scripts/                         # Validation, build, and management utilities
```

---

## Coordinator Summary Report Schema

```json
{
  "run_id": "annotation-run-001",
  "total_cases_input": 6346,
  "total_cases_annotated": 6346,
  "total_cases_failed_validation": 0,
  "disease_summary": {
    "Tuberculosis": {
      "input": 1200,
      "annotated": 1200,
      "POSITIVE": 820,
      "NEGATIVE": 95,
      "EXCLUDED_NON_TARGET_CASE": 180,
      "EXCLUDED_NON_SINGLE_PATIENT": 90,
      "EXCLUDED_NON_HUMAN": 5,
      "UNRESOLVED": 10
    }
  },
  "failure_flag_counts": {
    "F1_LEXICAL_HOMONYM": 0,
    "F2_SCOPE_COHORT": 0,
    "F3_SUBJECT_COREFERENCE": 0,
    "F4_ASSERTION_TEMPORAL": 0,
    "F5_DISCOURSE_CONTEXT": 0,
    "F6_EVIDENCE_SPECIFICITY": 0
  },
  "confidence_distribution": {
    "HIGH": 0,
    "MEDIUM": 0,
    "LOW": 0
  }
}
```

---

## Critical Rules for All Agents

1. **Never derive `dataset_label` from `confidence_tier` or `evidence_score`**.
   These are retrieval signals from Script 02. They are hints, not ground truth.

2. **Never assign POSITIVE for E3-only evidence.**
   Compatible symptoms + nonspecific labs = INSUFFICIENT, not POSITIVE.

3. **Never conflate disease mention with disease claim.**
   Title mentions tuberculosis — read the case text before deciding.

4. **Vaccination is never a POSITIVE case.**
   `clinical_role = PREVENTION_VACCINATION` → `EXCLUDED_NON_TARGET_CASE`.

5. **When uncertain, use UNRESOLVED + LOW confidence**, not a forced label.
   Forced binary decisions damage benchmark validity.

6. **Write rationale in plain English**, tracing the reasoning chain from
   key text evidence to the final label.

7. **One annotation record per `pair_id`.** If a case has multiple patients
   (mother + neonate), annotate for the primary patient only unless the
   secondary patient's disease is the explicit focus of the case.
   A case with several target diseases produces several records, one per
   `(case_id, target_disease)`; a case may be POSITIVE for more than one.


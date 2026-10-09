---
name: clinical-annotator
description: >
  Full annotation plan for the MultiCaRe Clinical Gold Standard.
  Annotates every (case_id, target_disease) candidate pair from the Script 02
  unified generator output (pair-level, ~17,431 pairs) using a
  Coordinator + 15 Disease-Agent hybrid architecture.
  Produces structured JSON annotations following the 12-step protocol
  defined in code/milestone3-5/04_gold_standard_annotation_protocol.md.
  THIS SKILL IS A PLAN — read and internalize it before executing any work.
---

# Clinical Gold Standard Annotation Skill

## Purpose

This skill guides **AI agents** to annotate the MultiCaRe candidate pairs
(`tropical_infectious_candidate_pairs.parquet`, one row per
`(case_id, target_disease)`) into a **Clinical Gold Standard** dataset.
The unit of annotation is the PAIR, not the case: one case may yield several
pairs, each judged independently for its own target disease.

The annotation answers one question per case:

> **Does this clinical case report contain a Valid Positive Diagnosis (VPD)
> of the target disease in the primary human patient?**

The answer is never derived from retrieval scores, metadata alone, or keyword
presence. It requires reading the full `case_text` and following the 12-step
protocol below.

---

## Architecture: Coordinator + 15 Disease Agents

### Overview

```
COORDINATOR AGENT
      │
      ├── reads tropical_infectious_candidate_pairs.parquet
      ├── groups pairs by target_disease
      ├── assigns batches to 15 Disease Agents
      ├── collects completed annotation JSONs
      ├── merges into gold_standard_annotations.jsonl
      └── runs validation pass (schema check, missing fields, conflicts)

15 DISEASE AGENTS (one per disease)
      │
      Each agent receives:
        - A JSONL file of pairs for its assigned target disease
        - Full text of this SKILL.md
        - Reference to the 4 protocol documents (paths below)
      │
      Each agent produces:
        - Annotated JSONL with one structured record per pair
```

### Coordinator responsibilities

1. **Load** `code/data/raw_filtered/tropical_infectious_candidate_pairs.parquet` (17,431 candidate pairs)
2. **Select Target Pool**:
   - `tier3_pool/` (10,388 pairs): pending clinical annotation (mostly Tier 3 mentions).
   - `labeled_pool/` (7,043 pairs): already annotated and validated.
3. **Group** pairs by `target_disease` column (15 disease buckets)
4. **Input JSONL files** at `code/data/annotation_workdir/{pool}/input/`
   - File naming: `input_{disease_slug}.jsonl`
   - Each line: one pair record (see Input Record Format below)
5. **Spawn** 15 Disease Agents, one per input file
6. **Collect** 15 output JSONL files from `code/data/annotation_workdir/{pool}/output/`
7. **Validate** each output:
   - Required fields present
   - `dataset_label` is a valid enum value
   - `evidence_strength` is a valid enum value
   - `rationale` is non-empty
8. **Merge** all validated outputs into:
   `code/data/gold_standard/pair_annotations_02b_unified.jsonl`
9. **Write** a coordinator summary report:
   `code/data/gold_standard/annotation_coordinator_report.json`

### Disease Agent responsibilities

Each Disease Agent:
1. Reads its assigned input JSONL (one case per line)
2. For each case, executes the 12-Step Annotation Protocol (see below)
3. Produces one structured annotation record per case
4. Writes output to `code/data/annotation_workdir/output/output_{disease_slug}.jsonl`

### Reference Documents (agents must read these)

| Document | Path |
|---|---|
| Clinical Claim Ontology | `code/milestone3-5/01_clinical_claim_ontology.md` |
| Clinical Claim Schema | `code/milestone3-5/02_clinical_claim_schema.md` |
| Evidence Specificity Matrix | `code/milestone3-5/03_evidence_specificity_matrix.md` |
| Annotation Protocol (12 Steps) | `code/milestone3-5/04_gold_standard_annotation_protocol.md` |

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

### Step 9 — Evidence assessment (`evidence_strength`)

Use `code/milestone3-5/03_evidence_specificity_matrix.md` for disease-specific rules.

```
E1_DISEASE_SPECIFIC_CONFIRMATORY  ← PCR+, culture+, NAAT+, species-specific test
E2_HIGHLY_CHARACTERISTIC          ← Disease-specific serology, paired seroconversion
E3_SUPPORTIVE_NON_SPECIFIC        ← Compatible symptoms, nonspecific labs, imaging
E4_BACKGROUND_OR_CONTEXT_ONLY     ← Exposure, epidemiology, vaccine — no patient evidence
E0_CONTRADICTED                   ← Confirmatory test explicitly negative
```

Ask: *"Does this evidence discriminate the target disease from clinically
plausible alternatives?"* — not merely *"Is this compatible with the disease?"*

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
  "pair_id": "PMC9282816_01::Tuberculosis",
  "case_id": "PMC9282816_01",
  "article_id": "PMC9282816",
  "target_disease": "Tuberculosis",

  "step1_document_type": "CASE_REPORT",
  "step2_ccu_type": "SINGLE_HUMAN_PATIENT",
  "step3_patient_anchor": {
    "anchor_type": "PRIMARY_PATIENT",
    "age": 34.0,
    "gender": "Male",
    "coreference_notes": ""
  },
  "step5_concept_grounding": "TARGET_CONFIRMED",
  "step6_assertion_type": "AFFIRMED",
  "step7_temporality": "CURRENT_ACTIVE",
  "step8_clinical_role": "PRIMARY_DIAGNOSIS",
  "step9_evidence_strength": "E1_DISEASE_SPECIFIC_CONFIRMATORY",
  "step9_key_evidence": [
    "Sputum AFB smear 3+",
    "GeneXpert MTB/RIF positive"
  ],
  "step10_contradiction_flag": false,
  "step10_contradiction_notes": "",
  "step11_vpd_satisfied": true,
  "step12_dataset_label": "POSITIVE",

  "failure_flags": [],
  "confidence": "HIGH",
  "rationale": "34M with cavitary pulmonary lesion. Sputum AFB 3+, GeneXpert MTB/RIF positive — E1 confirmatory evidence. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied → POSITIVE.",
  "annotator_id": "disease-agent-tuberculosis",
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
code/data/annotation_workdir/
├── labeled_pool/                # 7,043 pairs (already labeled & validated)
│   ├── input/
│   │   ├── input_covid_19.jsonl
│   │   └── ... (15 files, sum=7,043)
│   ├── output/
│   │   ├── output_covid_19.jsonl
│   │   └── ... (15 files, sum=7,043)
│   ├── coordinator_manifest.json
│   └── pair_provenance.json
│
└── tier3_pool/                  # 10,388 pairs (delta candidates, pending annotation)
    ├── input/
    │   ├── input_covid_19.jsonl
    │   └── ... (15 files, sum=10,388)
    ├── output/
    │   └── (ready for agent execution)
    ├── prompts/
    │   ├── prompt_covid_19.md
    │   └── ... (15 files + master batch prompt)
    ├── coordinator_manifest.json
    ├── pair_retrieval_provenance.json
    └── logs/

code/data/gold_standard/
└── pair_annotations_02b_unified.jsonl   ← Unified pair-level annotations
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

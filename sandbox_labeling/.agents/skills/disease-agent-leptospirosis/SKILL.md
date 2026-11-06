---
name: disease-agent-leptospirosis
description: >
  Clinical annotation agent for Leptospirosis.
  Annotates cases from annotation_workdir/labeled_pool/input/input_leptospirosis.jsonl
  following the 12-step protocol with Leptospirosis-specific evidence rules
  from 03_evidence_specificity_matrix.md.
---

# Clinical Annotation Agent — Leptospirosis

## Your Assigned Disease

**Target disease:** `Leptospirosis`
**Input file:** `sandbox/workspace/labeled_pool/input/input_leptospirosis.jsonl`
**Output file:** `sandbox/workspace/labeled_pool/output/output_leptospirosis.jsonl`

---

## PART A — Disease-Specific Evidence Matrix

The following is the full evidence specification for **Leptospirosis**,
extracted from `sandbox/protocols/03_evidence_specificity_matrix.md`.

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

### Leptospirosis-Specific Evidence Rules

## 5.8 Leptospirosis

### E1 — Disease-defining / confirmatory

- Detection of *Leptospira* DNA by a suitable molecular assay in an appropriate specimen and disease phase.
- Serological evidence of infection using an accepted diagnostic strategy, particularly demonstration of the expected antibody response.
- MAT-based confirmation where appropriately interpreted.

CDC states that diagnosis is based on detection of *Leptospira* DNA or antibody response, with test choice dependent on illness duration. WHO identifies MAT as the reference serologic method and emphasizes sequential specimens. citeturn550161search11turn877452search165

### E2 — Strong evidence

- Positive MAT with appropriate titer/paired-serum interpretation.
- Appropriate serologic conversion or rising titer.

### E3 — Supportive

- Fever.
- Myalgia.
- Headache.
- Conjunctival suffusion.
- Jaundice.
- Renal failure.
- Exposure to contaminated water/animals.

### Major confusable diseases

```text
Leptospirosis ↔ dengue
Leptospirosis ↔ malaria
Leptospirosis ↔ viral hepatitis
Leptospirosis ↔ hantavirus
```

### Contradiction notes

Timing matters strongly. Early serology may be negative before the antibody response develops.

---

---

## Primary Reference Source

| Disease | Primary source |
|---|---|
| Leptospirosis | [CDC Clinical Overview of Leptospirosis](https://www.cdc.gov/leptospirosis/hcp/clinical-overview/index.html) ; [WHO Human Leptospirosis](https://iris.who.int/bitstream/handle/10665/42667/WHO_CDS_CSR_EPH_2002.23.pdf) |


---

### Cross-Disease Rules (apply to all diseases)

# 6. Cross-Disease Confusable Evidence Matrix

| Evidence / phrase | Dangerous interpretation | Correct semantic treatment |
|---|---|---|
| `AFB positive` | Tuberculosis | Generic mycobacterial evidence; organism identity required for disease-specific claim |
| `mycobacteria` | Tuberculosis | Could represent NTM, *M. leprae*, BCG, etc. |
| `ovale` | Malaria | Lexical ambiguity; require *Plasmodium ovale* context |
| `walking aids` | HIV/AIDS | Mobility aid, not HIV disease |
| `COVID-19 vaccination` | COVID-19 infection | Prevention/vaccination role |
| `COVID-19 exposure precautions` | COVID-19 infection | Epidemiological/infection-control context |
| `COVID-19 considered` | COVID-19 diagnosis | Differential/hypothetical role |
| `fever + thrombocytopenia` | Dengue/malaria | Non-discriminative syndrome |
| `polyarthralgia + fever` | Chikungunya | Supportive only; laboratory differentiation needed |
| `IgM positive` | Zika/dengue/chikungunya confirmed | Disease-specific assay + cross-reactivity handling required |
| `animal exposure` | Rabies | Exposure, not infection |
| `history of TB` | Active TB | Temporality = historical unless current disease evidence exists |
| `mother has HIV` | Patient has HIV | Experiencer/subject = family member |
| `29-year-old mother` | Patient age 29 | Demographic anchor belongs to mother, not neonate |
| `case series, median age` | Single patient | Aggregate unit, not individual patient evidence |

---

---

# 7. Disease-Specific Evidence Rules Must Be Relational

The matrix intentionally avoids a rule such as:

```text
if matched_evidence_term == "PCR":
    evidence = E1
```

The correct conceptual representation is:

```text
PCR
 ├── target organism = ?
 ├── specimen = ?
 ├── patient anchor = ?
 ├── time = ?
 ├── result = POSITIVE / NEGATIVE / INDETERMINATE
 └── relation to claim = SUPPORTS / CONTRADICTS
```

For example:

```text
PCR
 ├── target = M. tuberculosis
 ├── result = NEGATIVE
```

is fundamentally different from:

```text
PCR
 ├── target = M. avium
 ├── result = POSITIVE
```

even though both contain:

```text
mycobacterium + PCR
```

The same principle applies to:

```text
SARS-CoV-2 NAAT
Dengue RT-PCR
Zika NAAT
Chikungunya RT-PCR
Yellow-fever RT-PCR
```

The analyte must be part of the evidence representation.

---

---

# 8. Treatment Is Not Automatically Diagnostic Evidence

Treatment should normally be classified as **E3/supportive** unless the article explicitly states that treatment response was used as part of the diagnostic reasoning and no stronger evidence is available.

Examples:

```text
“treated with anti-TB drugs”
    ≠
TB confirmed

“received antimalarial treatment”
    ≠
malaria confirmed

“received broad-spectrum antibiotics”
    ≠
Typhoid/Brucellosis confirmed
```

Otherwise the curation system risks a circular inference:

```text
clinician suspected disease
→ treated for disease
→ treatment appears in case text
→ model infers disease
→ model labels same original suspicion as confirmed diagnosis
```

That violates the project's **Retrieval ≠ Verification** invariant.

---

---

# 9. Epidemiology and Exposure Are Evidence of Plausibility, Not Confirmation

The following should normally be E3 or E0:

- residence in an endemic region;
- mosquito exposure;
- travel history;
- animal contact;
- unpasteurized dairy exposure;
- floodwater exposure;
- household contact with TB;
- outbreak membership.

They increase prior probability but do not establish a patient-level disease claim.

Formally:

```text
Exposure → raises plausibility
Exposure ↛ diagnosis
```

---

---

# 10. Negative Evidence Must Be Attached to a Specific Claim

A generic sentence such as:

> “The test was negative.”

is not enough for semantic contradiction.

The evidence object must resolve:

```text
negative what?
for whom?
from what specimen?
when?
using which assay?
relative to which disease claim?
```

The desired graph is:

```text
Patient_1
   │
   ├── ClinicalClaim_1 ──► Tuberculosis = AFFIRMED
   │
   └── Evidence_9
          ├── test = MTB PCR
          ├── target = M. tuberculosis
          ├── result = NEGATIVE
          ├── specimen = synovial fluid
          └── relation = CONTRADICTS Claim_1
```

This is fundamentally richer than:

```text
sentence contains “negative”
```

---

---

# 11. Implications for Claim Reconciliation

Claim reconciliation should operate in the following conceptual order:

```text
1. Establish patient / subject anchor
2. Normalize the disease/pathogen concept
3. Assign assertion / temporality / experiencer / clinical role
4. Attach evidence objects
5. Determine evidence specificity
6. Resolve supporting vs contradictory evidence
7. Prefer later explicit diagnostic conclusions over early hypotheses
8. Preserve unresolved contradiction rather than forcing a label
```

A later, specific result should normally outrank an earlier nonspecific suspicion, but this must remain **claim-aware** rather than a simple chronological or frequency rule.

Example:

```text
Initial differential:
    tuberculosis

AFB smear:
    positive

MTB-specific PCR:
    negative

Culture:
    M. avium positive

Final reconciled claim:
    non-TB mycobacterial infection

Tuberculosis label:
    REJECTED / CONTRADICTED
```

The representation should preserve all intermediate claims rather than deleting them after reconciliation.

---

---

# 12. Mapping to `02_clinical_claim_schema.md`

| Matrix concept | Schema representation |
|---|---|
| Disease target | `target_disease` / `normalized_concept` |
| Evidence level | `evidence_category`, `evidence_strength` |
| Patient relationship | `patient_anchor_id`, `subject_class`, `experiencer` |
| Test result | `EvidenceObject.result` |
| Pathogen/analyte | `EvidenceObject.target_concept` |
| Specimen | `EvidenceObject.specimen` |
| Timing | `EvidenceObject.temporality` / claim temporality |
| Supports diagnosis | `evidence_relation = SUPPORTS` |
| Contradicts diagnosis | `evidence_relation = CONTRADICTS` |
| Background context | `clinical_role`, `discourse_role` |
| Differential diagnosis | `clinical_role = DIFFERENTIAL_DIAGNOSIS` |
| Vaccination | `clinical_role = PREVENTION_VACCINATION` |
| Final diagnosis | `final_claim_status` |

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

The matrix is designed to eliminate the following failure patterns without case-specific exceptions:

```text
LEXICAL
“aids” → HIV/AIDS
“ovale” → malaria

ASSERTION
“no history of TB” → TB
“both HIV tests negative” → HIV

SUBJECT
mother's age → neonate's age
family member's disease → patient disease

DOCUMENT SCOPE
case series → single patient
animal case → human patient
mathematical model → clinical case

CLINICAL ROLE
vaccination → infection
infection-control → infection
hypothesis → confirmed diagnosis

EVIDENCE SPECIFICITY
AFB → tuberculosis
fever → dengue
polyarthralgia → chikungunya
IgM → any flavivirus

CONTRADICTION
single negative test → universal exclusion
```

---

---

## PART B — 12-Step Annotation Protocol

The following is the shared annotation protocol. Execute every step
in order for **every case** in your input file.

> [!CAUTION]
> **MANDATORY CLINICAL SEMANTIC REVIEW FOR LEPTOSPIROSIS (REGEX STRICTLY FORBIDDEN):**
> 1. **NO REGEX / KEYWORD MATCHING SCRIPTS:** You are strictly forbidden from writing or using Python regex / string search scripts to automate annotations.
> 2. **DEEP CLINICAL READING:** You must read the narrative of every single case to perform nuanced medical reasoning across all 12 steps.
> 3. **GROUNDED ATTRIBUTION:** Every evidence item in `step9_key_evidence` must be grounded with exact character offsets (`start_char`, `end_char`) and verbatim `source_quote`.

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
4. Writes output to `data/annotation_workdir/{pool}/output/output_{disease_slug}.jsonl`

### Reference Documents (Sandboxed Protocols)

| Document | Encapsulated Path |
|---|---|
| Clinical Claim Ontology | `sandbox/protocols/01_clinical_claim_ontology.md` |
| Clinical Claim Schema Spec | `sandbox/protocols/02_clinical_claim_schema.md` |
| Evidence Specificity Matrix | `sandbox/protocols/03_evidence_specificity_matrix.md` |
| Annotation Protocol (12 Steps) | `sandbox/protocols/04_gold_standard_annotation_protocol.md` |

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

Use `sandbox/protocols/03_evidence_specificity_matrix.md` for disease-specific rules.

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
      "end_char": 185,
      "source_quote": "Microscopic agglutination test demonstrated a diagnostic titer of 1:1600 against Leptospira interrogans",
      "patient_anchor_id": "patient_1",
      "test_name": "Microscopic agglutination test (MAT)",
      "target_concept": "Leptospira interrogans",
      "specimen": "serum",
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
| `test_name` | string | Diagnostic procedure, assay, lab test, or clinical finding | e.g. `"Microscopic agglutination test (MAT)"`, `"RT-PCR"`, `"Culture"`, `"Serology"` |
| `target_concept` | string | Specific organism, pathogen, antigen, antibody, or disease concept | e.g. `"Leptospira interrogans"` |
| `specimen` | string / null | Biological specimen or anatomical site | e.g. `"serum"`, `"blood"`, `"serum"`, `"sputum"`, `"CSF"`, `null` |
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
  "pair_id": "PMC8639279_01::Leptospirosis",
  "case_id": "PMC8639279_01",
  "article_id": "PMC8639279",
  "target_disease": "Leptospirosis",

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
        "end_char": 185,
        "source_quote": "Microscopic agglutination test demonstrated a diagnostic titer of 1:1600 against Leptospira interrogans",
        "patient_anchor_id": "patient_1",
        "test_name": "Microscopic agglutination test (MAT)",
        "target_concept": "Leptospira interrogans",
        "specimen": "serum",
        "result": "POSITIVE",
        "temporality": "CURRENT_EPISODE",
        "relation": "SUPPORTS",
        "strength": "E1_CONFIRMATORY"
      }
    ]
  },
  "step10_contradiction_flag": false,
  "step10_contradiction_notes": "",
  "step10_contradiction_resolution_status": null,
  "step11_vpd_satisfied": true,
  "step12_dataset_label": "POSITIVE",

  "failure_flags": [],
  "confidence": "HIGH",
  "rationale": "A 42-year-old farmer presenting with fever, conjunctival suffusion, and jaundice following flood immersion. MAT titer 1:1600 confirms leptospirosis — E1 confirmatory. Assertion AFFIRMED, temporality CURRENT_ACTIVE, clinical role PRIMARY_DIAGNOSIS. VPD satisfied → POSITIVE.",
  "annotator_id": "disease-agent-leptospirosis",
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


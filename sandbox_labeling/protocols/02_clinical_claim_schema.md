# Clinical Claim Representation — Formal Schema Specification

**Milestone 3 — Phase C / Task 1**  
**Status:** Research specification — code remains frozen  
**Date:** 2026-10-02  
**Depends on:** `01_clinical_claim_ontology.md`  
**Scope:** MultiCaRe single-patient clinical case curation for the 15 target diseases

---

## 0. Purpose

This document translates the ontology defined in `01_clinical_claim_ontology.md` into a **formal, machine-readable representation**.

The goal is not to prescribe an implementation. The goal is to define a stable information model so that different future implementations — rules, classical NLP, learned models, retrieval systems, LLMs, or hybrids — must produce outputs that are semantically comparable and auditable.

The core representation remains:

```text
DOCUMENT
   ↓
UNIT OF ANALYSIS
   ↓
PATIENT / SUBJECT ANCHOR
   ↓
CLINICAL CONCEPT MENTION
   ↓
CONTEXT
   ├── assertion
   ├── temporality
   ├── experiencer
   ├── clinical role
   └── discourse / section role
   ↓
EVIDENCE + RELATIONS
   ↓
CLINICAL CLAIM
   ↓
DATASET LABEL
```

The fundamental modeling decision is:

```text
DiseaseMention ≠ DiseaseClaim ≠ DatasetLabel
```

A disease mention is an observed textual/semantic object. A disease claim is a proposition about a clinical subject. A dataset label is a downstream decision derived from reconciled claims and evidence.

---

# 1. Schema Design Principles

## 1.1 Separation of observed facts and derived decisions

The schema distinguishes:

```text
OBSERVED
- text spans
- document metadata
- subject anchors
- mentions
- contextual attributes
- evidence

DERIVED
- normalized disease concept
- claim status
- evidence sufficiency
- final dataset label
```

This prevents a model's final label from being mistaken for an original observation.

## 1.2 Explicit subject anchoring

Every patient-level clinical claim must point to an explicit `PatientAnchor` or subject entity. The system must not infer that the first person or first demographic expression in a document is the patient.

## 1.3 Assertion, temporality, experiencer, and clinical role are independent dimensions

The representation deliberately avoids a single overloaded field such as `is_positive`.

For example:

```text
"COVID-19 vaccination was administered."

assertion       = AFFIRMED
experiencer     = PATIENT
clinical_role   = PREVENTION_VACCINATION
final_claim     = NON_DIAGNOSTIC_CONTEXT
```

The assertion is affirmed, but the statement is not a diagnosis of COVID-19.

## 1.4 Evidence is relational

Evidence is not just a list of keywords. Each evidence object must record whether it:

```text
SUPPORTS
CONTRADICTS
CONTEXTUALIZES
```

a particular claim.

## 1.5 JSON Schema is necessary but not sufficient

JSON Schema can validate:

- field presence;
- primitive types;
- enums;
- local structural constraints;
- conditional field combinations.

It cannot by itself reliably enforce graph-level constraints such as:

```text
claim.subject_anchor_id exists in the same CCU
claim.evidence_ref exists
claim.object_concept is compatible with the target disease
an evidence object belongs to the referenced patient
```

Those are defined below as **semantic validation invariants** and are part of the specification even though they require validation outside pure JSON Schema.

---

# 2. Top-Level Representation

A single serialized record represents one document and all case units that have been identified within that document.

Conceptually:

```text
ClinicalDocument
├── document_metadata
├── case_units[]
└── dataset_label_summary
```

The top-level record must preserve the distinction between:

1. the article/document;
2. the case unit extracted from it;
3. the patient anchor inside that unit;
4. disease mentions;
5. evidence objects;
6. reconciled clinical claims;
7. the resulting dataset label.

---

# 3. Controlled Vocabularies

The values below are the canonical serialization vocabulary for Phase C. They are derived from the conceptual vocabulary in Phase A/B; machine-safe names use uppercase snake case.

## 3.1 `document_type`

```text
CASE_REPORT
CASE_SERIES
AGGREGATE_COHORT
CASE_CONTROL
CROSS_SECTIONAL_STUDY
CLINICAL_TRIAL
SYSTEMATIC_REVIEW
META_ANALYSIS
GUIDELINE
EDITORIAL
PUBLIC_HEALTH_REPORT
MATHEMATICAL_MODEL
MACHINE_LEARNING_FRAMEWORK
METHODOLOGICAL_PAPER
UNKNOWN
```

`CASE_REPORT` is a publication/document classification only. It does **not** imply the existence of a valid single-human-patient case unit.

## 3.2 `ccu_type`

```text
SINGLE_HUMAN_PATIENT
MULTI_PATIENT_CASE_SERIES
AGGREGATE_STUDY_UNIT
ANIMAL_CASE
NON_HUMAN_SUBJECT
LABORATORY_SPECIMEN
NON_CLINICAL_DOCUMENT
UNKNOWN
```

For the target dataset, only `SINGLE_HUMAN_PATIENT` is eligible for the primary positive-diagnosis benchmark.

## 3.3 `subject_class`

```text
PATIENT_HUMAN
FAMILY_MEMBER
OTHER_HUMAN
POPULATION
ANIMAL
IN_VITRO_SPECIMEN
CAREGIVER_OR_STAFF
UNKNOWN
```

## 3.4 `assertion_type`

```text
AFFIRMED
NEGATED
POSSIBLE_HYPOTHETICAL
CONDITIONAL
UNCERTAIN
UNMENTIONED
```

## 3.5 `temporality`

```text
CURRENT_ACTIVE
RECENT_EPISODIC
HISTORICAL_RESOLVED
FUTURE_CONDITIONAL
CASE_RELEVANT_UNKNOWN_TIME
UNKNOWN
```

## 3.6 `experiencer`

```text
PATIENT
FAMILY_MEMBER
OTHER_PERSON
POPULATION
ANIMAL
UNKNOWN
```

`experiencer` describes who experiences the clinical condition or event referred to by the mention/claim. It is intentionally separate from the anchor identity.

## 3.7 `clinical_role`

```text
PRIMARY_DIAGNOSIS
ACTIVE_COMORBIDITY
DIFFERENTIAL_DIAGNOSIS
RULED_OUT_DIAGNOSIS
PAST_HISTORY
SYMPTOM_FINDING
TEST_TARGET
TEST_RESULT
TREATMENT_TARGET
ADVERSE_EVENT_EXPOSURE
PREVENTION_VACCINATION
EPIDEMIOLOGICAL_CONTEXT
BACKGROUND_LITERATURE_REFERENCE
UNKNOWN
```

## 3.8 `discourse_role`

```text
CASE_PRESENTATION
PATIENT_INFORMATION
DIAGNOSTIC_WORKUP
TREATMENT
OUTCOME
DISCUSSION
INTRODUCTION
LITERATURE_REVIEW
PUBLIC_HEALTH_CONTEXT
METHODS
RESULTS
UNKNOWN
```

## 3.9 `evidence_category`

Derived directly from the ontology:

```text
DIRECT_DIAGNOSIS
DISEASE_SPECIFIC_TEST
PATHOGEN_IDENTIFICATION
PATHOGNOMONIC_FINDING
CLINICAL_PATTERN
TREATMENT_RESPONSE
EXPOSURE_HISTORY
NEGATIVE_TEST
NON_SPECIFIC_FINDING
BACKGROUND_REFERENCE
```

## 3.10 `evidence_relation`

```text
SUPPORTS
CONTRADICTS
CONTEXTUALIZES
```

## 3.11 `evidence_strength`

The ontology defines the following conceptual hierarchy:

```text
E0_DIRECT_PATIENT_DIAGNOSIS
E1_DISEASE_SPECIFIC_CONFIRMATORY_EVIDENCE
E2_HIGHLY_CHARACTERISTIC_EVIDENCE
E3_SUPPORTIVE_NON_SPECIFIC_EVIDENCE
E4_BACKGROUND_OR_CONTEXT_ONLY
```

This is **not** a probability scale and must not be interpreted as one.

## 3.12 `final_claim_status`

This is a derived field, not an observed textual attribute.

```text
POSITIVE_DIAGNOSIS
NEGATED
HISTORICAL
POSSIBLE_OR_HYPOTHETICAL
NON_DIAGNOSTIC_CONTEXT
INSUFFICIENT_EVIDENCE
CONTRADICTED
UNRESOLVED
```

## 3.13 `dataset_label`

```text
POSITIVE
NEGATIVE
EXCLUDED_NON_TARGET_CASE
EXCLUDED_NON_HUMAN
EXCLUDED_NON_SINGLE_PATIENT
UNRESOLVED
```

The label is always downstream from claim reconciliation.

---

# 4. Core Object: `ClinicalCaseUnit`

## 4.1 Definition

A `ClinicalCaseUnit` is the document-grounded unit whose subject(s), observations, diagnostic reasoning, intervention, or outcome are being analyzed.

For the target benchmark:

```text
ccu_type = SINGLE_HUMAN_PATIENT
subject_anchor_id → PatientAnchor(subject_class = PATIENT_HUMAN)
```

## 4.2 Required fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `ccu_id` | string | yes | Stable identifier within the document |
| `ccu_type` | enum | yes | Unit of analysis |
| `subject_anchor_id` | string | yes | Primary subject anchor |
| `clinical_narrative_present` | boolean | yes | Whether patient-level narrative exists |
| `patient_level_observations_present` | boolean | yes | Whether patient-level observations are present |
| `source_sections` | array[string] | yes | Sections supplying the CCU |
| `disease_mentions` | array[ref] | yes | Candidate disease mentions |
| `evidence_objects` | array[ref] | yes | Evidence objects |
| `clinical_claims` | array[ref] | yes | Reconciled claims |
| `dataset_label` | enum | yes | Derived case-level label |

## 4.3 Target-case structural invariant

A CCU may be retained as an internal representation even when it is not eligible for the target dataset. The representation must therefore support both:

```text
represented case unit
```

and:

```text
target dataset eligibility
```

This avoids losing information merely because a document is eventually excluded.

---

# 5. Core Object: `PatientAnchor`

## 5.1 Definition

A `PatientAnchor` identifies the subject that acts as the target patient for a `ClinicalCaseUnit`.

## 5.2 Required fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `anchor_id` | string | yes | Stable ID |
| `subject_class` | enum | yes | Subject category |
| `mention_refs` | array[string] | yes | Mentions that establish this anchor |
| `anchor_confidence` | number 0–1 | yes | Confidence in identity resolution |
| `is_primary_subject` | boolean | yes | Whether this is the CCU's main subject |
| `demographics` | object/null | no | Patient demographics attributable to this anchor |
| `role_description` | string | no | Human-readable role if not self-evident |

## 5.3 Demographics object

The schema deliberately stores demographics *under the anchor* rather than at document root.

```text
PatientAnchor
└── demographics
    ├── age_value
    ├── age_unit
    ├── sex
    └── source_mention_refs
```

This prevents a mother's age from becoming the neonate's age simply because it appeared first in the text.

## 5.4 Subject invariant

If:

```text
ccu.ccu_type = SINGLE_HUMAN_PATIENT
```

then:

```text
patient_anchor.subject_class = PATIENT_HUMAN
patient_anchor.is_primary_subject = true
```

---

# 6. Core Object: `DiseaseMention`

## 6.1 Definition

A `DiseaseMention` is a candidate textual/semantic reference to a disease or disease-related concept.

It is intentionally weaker than a disease claim.

## 6.2 Required fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `mention_id` | string | yes | Stable ID |
| `text` | string | yes | Exact observed text span |
| `normalized_concept` | string | yes | Canonical clinical concept after grounding |
| `target_disease` | string/null | yes | One of the 15 target diseases if applicable |
| `source_section` | enum | yes | Discourse location |
| `anchor_id` | string | yes | Subject associated with mention interpretation |
| `assertion` | enum | yes | Assertion dimension |
| `temporality` | enum | yes | Temporal dimension |
| `experiencer` | enum | yes | Experiencer dimension |
| `clinical_role` | enum | yes | Clinical function |
| `discourse_role` | enum | yes | Discourse function |
| `evidence_refs` | array[string] | yes | Evidence objects associated with the mention |

## 6.3 Concept grounding invariant

The `normalized_concept` must refer to the semantic concept represented by the span, not simply to the lexical substring that matched it.

Examples:

```text
"walking aids"
    normalized_concept = MOBILITY_AID
    target_disease = null

"patent foramen ovale"
    normalized_concept = PATENT_FORAMEN_OVALE
    target_disease = null

"Plasmodium ovale"
    normalized_concept = PLASMODIUM_OVALE
    target_disease = MALARIA
```

The schema therefore has no field whose semantics are “matched keyword”.

---

# 7. Core Object: `EvidenceObject`

## 7.1 Definition

An `EvidenceObject` is an observation or statement that can support, contradict, or contextualize a clinical claim.

## 7.2 Required fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `evidence_id` | string | yes | Stable ID |
| `text` | string | yes | Exact evidence span/sentence |
| `anchor_id` | string | yes | Subject to whom evidence belongs |
| `category` | enum | yes | Evidence category |
| `relation` | enum | yes | Relation to a claim |
| `strength` | enum | yes | E0–E4 conceptual evidence level |
| `source_section` | enum | yes | Discourse location |
| `specificity_note` | string | yes | Why evidence is or is not disease-discriminative |
| `source_mention_refs` | array[string] | yes | Mentions that generated this evidence object |

## 7.3 Evidence specificity invariant

An evidence object may support a claim only if its specificity is compatible with that claim.

For example:

```text
AFB-positive
strength = E3_SUPPORTIVE_NON_SPECIFIC_EVIDENCE
```

must not be promoted automatically into:

```text
Tuberculosis = POSITIVE_DIAGNOSIS
```

unless additional patient-specific, disease-discriminative evidence or an explicit established diagnosis exists.

---

# 8. Core Object: `ClinicalClaim`

## 8.1 Definition

A `ClinicalClaim` is a structured proposition asserting that a target disease condition applies to a subject within a CCU.

Canonical form:

```text
(subject, predicate, object, context, evidence)
```

For the disease-label task:

```text
subject   = PatientAnchor
predicate = HAS_DISEASE
object    = TargetDisease
```

## 8.2 Required fields

| Field | Type | Required | Meaning |
|---|---|---:|---|
| `claim_id` | string | yes | Stable ID |
| `subject_anchor_id` | string | yes | Patient/subject reference |
| `predicate` | enum | yes | Currently `HAS_DISEASE` |
| `object_concept` | string | yes | Canonical disease concept |
| `target_disease` | string/null | yes | Target disease if applicable |
| `assertion` | enum | yes | Assertion status |
| `temporality` | enum | yes | Temporal status |
| `experiencer` | enum | yes | Experiencer |
| `clinical_role` | enum | yes | Clinical role |
| `discourse_role` | enum | yes | Discourse role |
| `evidence_refs` | array[string] | yes | Supporting/contradicting evidence |
| `final_claim_status` | enum | yes | Derived reconciled status |
| `claim_confidence` | number 0–1 | yes | Confidence in the structured claim |
| `rationale` | string | yes | Audit explanation |

## 8.3 Predicate vocabulary

Current Phase C schema:

```text
HAS_DISEASE
```

Additional predicates may be introduced later for evidence graphs, but they are deliberately not added here until Phase C Task 2 establishes the evidence-relation model.

---

# 9. Core Object: `ClinicalDocument`

## 9.1 Structure

```text
ClinicalDocument
├── document_metadata
├── patient_anchors[]
├── case_units[]
├── disease_mentions[]
├── evidence_objects[]
├── clinical_claims[]
└── dataset_label_summary
```

The object collections are normalized at document scope so that references remain stable and auditable.

## 9.2 Document metadata

| Field | Type | Required |
|---|---|---:|
| `document_id` | string | yes |
| `title` | string | yes |
| `document_type` | enum | yes |
| `source` | string | no |
| `publication_identifier` | string | no |
| `metadata_only_evidence` | boolean | yes |

`metadata_only_evidence = true` means the disease signal originates only from title/metadata/abstract-level content and must not be treated as patient-level confirmation under the VPD rules.

---

# 10. Dataset-Level Label Derivation

`dataset_label` is not a manually equivalent synonym for `final_claim_status`.

It is a document/CCU-level result derived after claim reconciliation.

Conceptual mapping:

```text
POSITIVE
    ⇐ at least one reconciled Valid Positive Diagnosis

NEGATIVE
    ⇐ target disease is explicitly ruled out / negated and no stronger
       positive claim remains

EXCLUDED_NON_TARGET_CASE
    ⇐ document/unit does not satisfy target single-patient disease task

EXCLUDED_NON_HUMAN
    ⇐ primary subject is not human

EXCLUDED_NON_SINGLE_PATIENT
    ⇐ unit is aggregate / cohort / multi-subject without separable patient CCU

UNRESOLVED
    ⇐ available claims and evidence cannot support a defensible final status
```

The exact operational policy for `NEGATIVE` versus `UNRESOLVED` must be finalized during Gold-Standard annotation, not inferred from the schema alone.

---

# 11. Valid Positive Diagnosis — Machine-Checkable Conditions

A claim is eligible to produce `POSITIVE_DIAGNOSIS` only when all mandatory conditions are satisfied.

## 11.1 Mandatory conditions

```text
C1  Case unit is eligible for target dataset
C2  Subject anchor is PATIENT_HUMAN and primary subject
C3  Target disease concept is correctly grounded
C4  Assertion is AFFIRMED
C5  Temporality is CURRENT_ACTIVE or CASE_RELEVANT_UNKNOWN_TIME
C6  Experiencer is PATIENT
C7  Clinical role is diagnostic/active clinical disease
C8  At least one evidence item is DIRECT_DIAGNOSIS or E1/E2-level
    disease-relevant evidence, OR an explicit established case-level diagnosis
C9  No stronger patient-specific contradictory evidence overrides the claim
C10 Mention is not merely background, vaccination, epidemiology, exposure,
    literature reference, or differential diagnosis
```

## 11.2 Diagnostic clinical roles

For Phase C, the roles that can directly support a positive disease label are:

```text
PRIMARY_DIAGNOSIS
ACTIVE_COMORBIDITY
```

`SYMPTOM_FINDING` and `TEST_RESULT` can provide evidence, but do not by themselves become positive diagnoses.

`DIFFERENTIAL_DIAGNOSIS`, `RULED_OUT_DIAGNOSIS`, `PAST_HISTORY`, `PREVENTION_VACCINATION`, `EPIDEMIOLOGICAL_CONTEXT`, and `BACKGROUND_LITERATURE_REFERENCE` cannot independently produce a positive active-disease label.

---

# 12. Semantic Validation Invariants

These rules are part of the formal specification even where pure JSON Schema cannot express them.

## V1 — CCU subject integrity

```text
case_unit.subject_anchor_id
    must resolve to an existing PatientAnchor/subject anchor
```

## V2 — Human-patient eligibility

```text
ccu_type = SINGLE_HUMAN_PATIENT
    ⇒ subject_class = PATIENT_HUMAN
```

## V3 — Primary-subject integrity

```text
A claim used for dataset labeling
    ⇒ claim.subject_anchor_id = ccu.subject_anchor_id
```

## V4 — Experiencer consistency

A claim may only contribute to the patient label when:

```text
claim.experiencer = PATIENT
```

A family member's disease is not the patient's disease.

## V5 — Assertion consistency

```text
assertion = NEGATED
    ⇒ final_claim_status != POSITIVE_DIAGNOSIS
```

```text
assertion = POSSIBLE_HYPOTHETICAL
    ⇒ final_claim_status != POSITIVE_DIAGNOSIS
```

unless a separate affirmed claim exists and is independently supported. The possible mention itself cannot create the positive label.

## V6 — Clinical-role consistency

```text
clinical_role = PREVENTION_VACCINATION
    ⇒ final_claim_status != POSITIVE_DIAGNOSIS
```

```text
clinical_role = EPIDEMIOLOGICAL_CONTEXT
    ⇒ final_claim_status != POSITIVE_DIAGNOSIS
```

```text
clinical_role = BACKGROUND_LITERATURE_REFERENCE
    ⇒ final_claim_status != POSITIVE_DIAGNOSIS
```

## V7 — Evidence requirement

A positive disease label must have at least one linked evidence item or explicit patient-level diagnosis statement.

```text
len(evidence_refs) > 0 OR explicit_diagnosis = true
```

## V8 — Evidence anchoring

For an evidence item linked as `SUPPORTS`, the evidence's `anchor_id` must resolve to the same patient/subject as the claim unless the evidence is explicitly an indirect contextual relation.

## V9 — Metadata non-equivalence

The following cannot independently satisfy VPD:

```text
article title
MeSH term
publication type
abstract-only disease mention
BM25 score
retrieval rank
keyword count
```

## V10 — Background non-equivalence

A disease mention located exclusively in `DISCUSSION`, `INTRODUCTION`, `LITERATURE_REVIEW`, or `PUBLIC_HEALTH_CONTEXT` cannot independently produce a positive patient diagnosis.

## V11 — Specificity requirement

`E3_SUPPORTIVE_NON_SPECIFIC_EVIDENCE` and `E4_BACKGROUND_OR_CONTEXT_ONLY` are insufficient as sole evidence for a positive label.

## V12 — Contradiction precedence

If a claim has both supporting and contradicting evidence, the final status must be reconciled using the strongest patient-specific disease-discriminative evidence and the established/final diagnosis where available.

The schema does not encode an arbitrary numeric weighting formula at this stage.

## V13 — Entity-grounding requirement

A lexical substring match must not be sufficient to establish `target_disease`.

Example:

```text
"aids"
```

must be semantically grounded before it can map to HIV/AIDS.

## V14 — Single-patient scope

An aggregate statistic may not be attributed to the target patient unless the text explicitly links that statistic to that patient.

Example:

```text
"median age was 62 years"
```

cannot become:

```text
Patient.age = 62
```

## V15 — Demographic anchoring

Demographic attributes must be attached to the anchor whose identity the text explicitly establishes.

---

# 13. JSON Schema — Draft 2020-12

The following is the normative structural schema for Phase C Task 1.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://clinicians-multimodel.local/schema/clinical-claim-document.schema.json",
  "title": "Clinical Claim Document",
  "type": "object",
  "required": [
    "document_metadata",
    "patient_anchors",
    "case_units",
    "disease_mentions",
    "evidence_objects",
    "clinical_claims"
  ],
  "properties": {
    "document_metadata": { "$ref": "#/$defs/documentMetadata" },
    "patient_anchors": {
      "type": "array",
      "items": { "$ref": "#/$defs/patientAnchor" }
    },
    "case_units": {
      "type": "array",
      "items": { "$ref": "#/$defs/clinicalCaseUnit" }
    },
    "disease_mentions": {
      "type": "array",
      "items": { "$ref": "#/$defs/diseaseMention" }
    },
    "evidence_objects": {
      "type": "array",
      "items": { "$ref": "#/$defs/evidenceObject" }
    },
    "clinical_claims": {
      "type": "array",
      "items": { "$ref": "#/$defs/clinicalClaim" }
    }
  },
  "$defs": {
    "documentType": {
      "type": "string",
      "enum": [
        "CASE_REPORT",
        "CASE_SERIES",
        "AGGREGATE_COHORT",
        "CASE_CONTROL",
        "CROSS_SECTIONAL_STUDY",
        "CLINICAL_TRIAL",
        "SYSTEMATIC_REVIEW",
        "META_ANALYSIS",
        "GUIDELINE",
        "EDITORIAL",
        "PUBLIC_HEALTH_REPORT",
        "MATHEMATICAL_MODEL",
        "MACHINE_LEARNING_FRAMEWORK",
        "METHODOLOGICAL_PAPER",
        "UNKNOWN"
      ]
    },
    "ccuType": {
      "type": "string",
      "enum": [
        "SINGLE_HUMAN_PATIENT",
        "MULTI_PATIENT_CASE_SERIES",
        "AGGREGATE_STUDY_UNIT",
        "ANIMAL_CASE",
        "NON_HUMAN_SUBJECT",
        "LABORATORY_SPECIMEN",
        "NON_CLINICAL_DOCUMENT",
        "UNKNOWN"
      ]
    },
    "subjectClass": {
      "type": "string",
      "enum": [
        "PATIENT_HUMAN",
        "FAMILY_MEMBER",
        "OTHER_HUMAN",
        "POPULATION",
        "ANIMAL",
        "IN_VITRO_SPECIMEN",
        "CAREGIVER_OR_STAFF",
        "UNKNOWN"
      ]
    },
    "assertionType": {
      "type": "string",
      "enum": [
        "AFFIRMED",
        "NEGATED",
        "POSSIBLE_HYPOTHETICAL",
        "CONDITIONAL",
        "UNCERTAIN",
        "UNMENTIONED"
      ]
    },
    "temporality": {
      "type": "string",
      "enum": [
        "CURRENT_ACTIVE",
        "RECENT_EPISODIC",
        "HISTORICAL_RESOLVED",
        "FUTURE_CONDITIONAL",
        "CASE_RELEVANT_UNKNOWN_TIME",
        "UNKNOWN"
      ]
    },
    "experiencer": {
      "type": "string",
      "enum": [
        "PATIENT",
        "FAMILY_MEMBER",
        "OTHER_PERSON",
        "POPULATION",
        "ANIMAL",
        "UNKNOWN"
      ]
    },
    "clinicalRole": {
      "type": "string",
      "enum": [
        "PRIMARY_DIAGNOSIS",
        "ACTIVE_COMORBIDITY",
        "DIFFERENTIAL_DIAGNOSIS",
        "RULED_OUT_DIAGNOSIS",
        "PAST_HISTORY",
        "SYMPTOM_FINDING",
        "TEST_TARGET",
        "TEST_RESULT",
        "TREATMENT_TARGET",
        "ADVERSE_EVENT_EXPOSURE",
        "PREVENTION_VACCINATION",
        "EPIDEMIOLOGICAL_CONTEXT",
        "BACKGROUND_LITERATURE_REFERENCE",
        "UNKNOWN"
      ]
    },
    "discourseRole": {
      "type": "string",
      "enum": [
        "CASE_PRESENTATION",
        "PATIENT_INFORMATION",
        "DIAGNOSTIC_WORKUP",
        "TREATMENT",
        "OUTCOME",
        "DISCUSSION",
        "INTRODUCTION",
        "LITERATURE_REVIEW",
        "PUBLIC_HEALTH_CONTEXT",
        "METHODS",
        "RESULTS",
        "UNKNOWN"
      ]
    },
    "evidenceCategory": {
      "type": "string",
      "enum": [
        "DIRECT_DIAGNOSIS",
        "DISEASE_SPECIFIC_TEST",
        "PATHOGEN_IDENTIFICATION",
        "PATHOGNOMONIC_FINDING",
        "CLINICAL_PATTERN",
        "TREATMENT_RESPONSE",
        "EXPOSURE_HISTORY",
        "NEGATIVE_TEST",
        "NON_SPECIFIC_FINDING",
        "BACKGROUND_REFERENCE"
      ]
    },
    "evidenceRelation": {
      "type": "string",
      "enum": ["SUPPORTS", "CONTRADICTS", "CONTEXTUALIZES"]
    },
    "evidenceStrength": {
      "type": "string",
      "enum": [
        "E0_DIRECT_PATIENT_DIAGNOSIS",
        "E1_DISEASE_SPECIFIC_CONFIRMATORY_EVIDENCE",
        "E2_HIGHLY_CHARACTERISTIC_EVIDENCE",
        "E3_SUPPORTIVE_NON_SPECIFIC_EVIDENCE",
        "E4_BACKGROUND_OR_CONTEXT_ONLY"
      ]
    },
    "sourceSection": {
      "$ref": "#/$defs/discourseRole"
    },
    "finalClaimStatus": {
      "type": "string",
      "enum": [
        "POSITIVE_DIAGNOSIS",
        "NEGATED",
        "HISTORICAL",
        "POSSIBLE_OR_HYPOTHETICAL",
        "NON_DIAGNOSTIC_CONTEXT",
        "INSUFFICIENT_EVIDENCE",
        "CONTRADICTED",
        "UNRESOLVED"
      ]
    },
    "datasetLabel": {
      "type": "string",
      "enum": [
        "POSITIVE",
        "NEGATIVE",
        "EXCLUDED_NON_TARGET_CASE",
        "EXCLUDED_NON_HUMAN",
        "EXCLUDED_NON_SINGLE_PATIENT",
        "UNRESOLVED"
      ]
    },
    "demographics": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "age_value": { "type": ["number", "null"] },
        "age_unit": {
          "type": ["string", "null"],
          "enum": ["years", "months", "weeks", "days", "unknown", null]
        },
        "sex": {
          "type": ["string", "null"],
          "enum": ["male", "female", "intersex", "unknown", null]
        },
        "source_mention_refs": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "documentMetadata": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "document_id",
        "title",
        "document_type",
        "metadata_only_evidence"
      ],
      "properties": {
        "document_id": { "type": "string", "minLength": 1 },
        "title": { "type": "string", "minLength": 1 },
        "document_type": { "$ref": "#/$defs/documentType" },
        "source": { "type": ["string", "null"] },
        "publication_identifier": { "type": ["string", "null"] },
        "metadata_only_evidence": { "type": "boolean" }
      }
    },
    "patientAnchor": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "anchor_id",
        "subject_class",
        "mention_refs",
        "anchor_confidence",
        "is_primary_subject"
      ],
      "properties": {
        "anchor_id": { "type": "string", "minLength": 1 },
        "subject_class": { "$ref": "#/$defs/subjectClass" },
        "mention_refs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "anchor_confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "is_primary_subject": { "type": "boolean" },
        "demographics": {
          "anyOf": [
            { "$ref": "#/$defs/demographics" },
            { "type": "null" }
          ]
        },
        "role_description": { "type": ["string", "null"] }
      }
    },
    "clinicalCaseUnit": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "ccu_id",
        "ccu_type",
        "subject_anchor_id",
        "clinical_narrative_present",
        "patient_level_observations_present",
        "source_sections",
        "disease_mentions",
        "evidence_objects",
        "clinical_claims",
        "dataset_label"
      ],
      "properties": {
        "ccu_id": { "type": "string", "minLength": 1 },
        "ccu_type": { "$ref": "#/$defs/ccuType" },
        "subject_anchor_id": { "type": "string", "minLength": 1 },
        "clinical_narrative_present": { "type": "boolean" },
        "patient_level_observations_present": { "type": "boolean" },
        "source_sections": {
          "type": "array",
          "items": { "$ref": "#/$defs/discourseRole" }
        },
        "disease_mentions": {
          "type": "array",
          "items": { "type": "string" }
        },
        "evidence_objects": {
          "type": "array",
          "items": { "type": "string" }
        },
        "clinical_claims": {
          "type": "array",
          "items": { "type": "string" }
        },
        "dataset_label": { "$ref": "#/$defs/datasetLabel" }
      }
    },
    "diseaseMention": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "mention_id",
        "text",
        "normalized_concept",
        "target_disease",
        "source_section",
        "anchor_id",
        "assertion",
        "temporality",
        "experiencer",
        "clinical_role",
        "discourse_role",
        "evidence_refs"
      ],
      "properties": {
        "mention_id": { "type": "string", "minLength": 1 },
        "text": { "type": "string", "minLength": 1 },
        "normalized_concept": { "type": "string", "minLength": 1 },
        "target_disease": { "type": ["string", "null"] },
        "source_section": { "$ref": "#/$defs/discourseRole" },
        "anchor_id": { "type": "string", "minLength": 1 },
        "assertion": { "$ref": "#/$defs/assertionType" },
        "temporality": { "$ref": "#/$defs/temporality" },
        "experiencer": { "$ref": "#/$defs/experiencer" },
        "clinical_role": { "$ref": "#/$defs/clinicalRole" },
        "discourse_role": { "$ref": "#/$defs/discourseRole" },
        "evidence_refs": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "evidenceObject": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "evidence_id",
        "text",
        "anchor_id",
        "category",
        "relation",
        "strength",
        "source_section",
        "specificity_note",
        "source_mention_refs"
      ],
      "properties": {
        "evidence_id": { "type": "string", "minLength": 1 },
        "text": { "type": "string", "minLength": 1 },
        "anchor_id": { "type": "string", "minLength": 1 },
        "category": { "$ref": "#/$defs/evidenceCategory" },
        "relation": { "$ref": "#/$defs/evidenceRelation" },
        "strength": { "$ref": "#/$defs/evidenceStrength" },
        "source_section": { "$ref": "#/$defs/discourseRole" },
        "specificity_note": { "type": "string", "minLength": 1 },
        "source_mention_refs": {
          "type": "array",
          "items": { "type": "string" }
        }
      }
    },
    "clinicalClaim": {
      "type": "object",
      "additionalProperties": false,
      "required": [
        "claim_id",
        "subject_anchor_id",
        "predicate",
        "object_concept",
        "target_disease",
        "assertion",
        "temporality",
        "experiencer",
        "clinical_role",
        "discourse_role",
        "evidence_refs",
        "final_claim_status",
        "claim_confidence",
        "rationale"
      ],
      "properties": {
        "claim_id": { "type": "string", "minLength": 1 },
        "subject_anchor_id": { "type": "string", "minLength": 1 },
        "predicate": {
          "type": "string",
          "enum": ["HAS_DISEASE"]
        },
        "object_concept": { "type": "string", "minLength": 1 },
        "target_disease": { "type": ["string", "null"] },
        "assertion": { "$ref": "#/$defs/assertionType" },
        "temporality": { "$ref": "#/$defs/temporality" },
        "experiencer": { "$ref": "#/$defs/experiencer" },
        "clinical_role": { "$ref": "#/$defs/clinicalRole" },
        "discourse_role": { "$ref": "#/$defs/discourseRole" },
        "evidence_refs": {
          "type": "array",
          "items": { "type": "string" }
        },
        "final_claim_status": { "$ref": "#/$defs/finalClaimStatus" },
        "claim_confidence": {
          "type": "number",
          "minimum": 0,
          "maximum": 1
        },
        "rationale": { "type": "string", "minLength": 1 }
      },
      "allOf": [
        {
          "if": {
            "properties": {
              "assertion": { "enum": ["NEGATED", "POSSIBLE_HYPOTHETICAL"] }
            }
          },
          "then": {
            "properties": {
              "final_claim_status": {
                "not": { "const": "POSITIVE_DIAGNOSIS" }
              }
            }
          }
        },
        {
          "if": {
            "properties": {
              "clinical_role": {
                "enum": [
                  "PREVENTION_VACCINATION",
                  "EPIDEMIOLOGICAL_CONTEXT",
                  "BACKGROUND_LITERATURE_REFERENCE",
                  "DIFFERENTIAL_DIAGNOSIS",
                  "RULED_OUT_DIAGNOSIS"
                ]
              }
            }
          },
          "then": {
            "properties": {
              "final_claim_status": {
                "not": { "const": "POSITIVE_DIAGNOSIS" }
              }
            }
          }
        }
      ]
    }
  }
}
```

---

# 14. JSON Schema vs Semantic Validator

The specification intentionally separates two validation layers.

## Layer 1 — Structural JSON Schema validation

Checks:

```text
Field exists
Type is correct
Enum is valid
Confidence is within [0,1]
Object structure is valid
Simple local conditionals hold
```

## Layer 2 — Semantic graph validation

Checks:

```text
Reference integrity
Subject identity
Experiencer identity
Evidence ownership
Claim/evidence compatibility
CCU eligibility
Disease concept correctness
Contradiction reconciliation
Final positive-diagnosis criteria
```

This distinction is fundamental.

For example, the following JSON object can be perfectly valid JSON Schema while still being clinically wrong:

```json
{
  "subject_anchor_id": "PATIENT_01",
  "experiencer": "PATIENT",
  "object_concept": "Tuberculosis",
  "assertion": "AFFIRMED",
  "clinical_role": "PRIMARY_DIAGNOSIS"
}
```

if `PATIENT_01` actually points to the wrong person.

Therefore:

```text
Schema validity ≠ Clinical validity
```

---

# 15. Canonical Minimal Examples

## 15.1 Positive tuberculosis case

```json
{
  "claim_id": "CLAIM_001",
  "subject_anchor_id": "PATIENT_01",
  "predicate": "HAS_DISEASE",
  "object_concept": "Tuberculosis",
  "target_disease": "Tuberculosis",
  "assertion": "AFFIRMED",
  "temporality": "CURRENT_ACTIVE",
  "experiencer": "PATIENT",
  "clinical_role": "PRIMARY_DIAGNOSIS",
  "discourse_role": "CASE_PRESENTATION",
  "evidence_refs": ["EV_001"],
  "final_claim_status": "POSITIVE_DIAGNOSIS",
  "claim_confidence": 0.98,
  "rationale": "Patient-level diagnosis is explicitly established and supported by disease-specific evidence."
}
```

## 15.2 Negated tuberculosis

```json
{
  "claim_id": "CLAIM_002",
  "subject_anchor_id": "PATIENT_01",
  "predicate": "HAS_DISEASE",
  "object_concept": "Tuberculosis",
  "target_disease": "Tuberculosis",
  "assertion": "NEGATED",
  "temporality": "CURRENT_ACTIVE",
  "experiencer": "PATIENT",
  "clinical_role": "RULED_OUT_DIAGNOSIS",
  "discourse_role": "DIAGNOSTIC_WORKUP",
  "evidence_refs": ["EV_002"],
  "final_claim_status": "NEGATED",
  "claim_confidence": 0.97,
  "rationale": "Tuberculosis was explicitly ruled out for the patient."
}
```

## 15.3 COVID-19 vaccination

```json
{
  "claim_id": "CLAIM_003",
  "subject_anchor_id": "PATIENT_01",
  "predicate": "HAS_DISEASE",
  "object_concept": "COVID-19",
  "target_disease": "COVID-19",
  "assertion": "AFFIRMED",
  "temporality": "RECENT_EPISODIC",
  "experiencer": "PATIENT",
  "clinical_role": "PREVENTION_VACCINATION",
  "discourse_role": "CASE_PRESENTATION",
  "evidence_refs": ["EV_003"],
  "final_claim_status": "NON_DIAGNOSTIC_CONTEXT",
  "claim_confidence": 0.99,
  "rationale": "COVID-19 is referenced as the target of vaccination, not as an active patient diagnosis."
}
```

## 15.4 Family-member disease

```json
{
  "claim_id": "CLAIM_004",
  "subject_anchor_id": "MOTHER_01",
  "predicate": "HAS_DISEASE",
  "object_concept": "Tuberculosis",
  "target_disease": "Tuberculosis",
  "assertion": "AFFIRMED",
  "temporality": "HISTORICAL_RESOLVED",
  "experiencer": "FAMILY_MEMBER",
  "clinical_role": "PAST_HISTORY",
  "discourse_role": "PATIENT_INFORMATION",
  "evidence_refs": ["EV_004"],
  "final_claim_status": "HISTORICAL",
  "claim_confidence": 0.94,
  "rationale": "Disease belongs to the patient's mother rather than the target patient."
}
```

This claim may be clinically true while still contributing **zero positive evidence** to the patient's tuberculosis label.

---

# 16. Canonical Representation of the 17 Observed Failure Modes

The schema is intended to represent failures without special-case exceptions.

| Observed phenomenon | Representation-level resolution |
|---|---|
| `walking aids` → AIDS | `normalized_concept` disambiguation before `target_disease` assignment |
| `ovale` → malaria | semantic concept grounding |
| HIV serology nonreactive | `assertion = NEGATED` + `clinical_role = TEST_RESULT` |
| both HIV tests returned negative | evidence object `NEGATIVE_TEST` contradicts positive diagnosis |
| TB PCR negative, M. avium present | competing disease claims + `CONTRADICTS` evidence |
| no tuberculosis contact | contextual/history statement, not diagnosis |
| AFB positive in leprosy | `E3_SUPPORTIVE_NON_SPECIFIC_EVIDENCE` |
| COVID vaccination | affirmed mention + `PREVENTION_VACCINATION` |
| COVID exposure-control context | `EPIDEMIOLOGICAL_CONTEXT` / `ADVERSE_EVENT_EXPOSURE` |
| COVID pandemic background | `EPIDEMIOLOGICAL_CONTEXT` |
| COVID differential hypothesis | `POSSIBLE_HYPOTHETICAL` + `DIFFERENTIAL_DIAGNOSIS` |
| cat/tiger case | `subject_class = ANIMAL` |
| mathematical model | non-target `ccu_type` / `document_type` |
| ML framework | non-target document/unit |
| cohort summary | `AGGREGATE_COHORT` / `AGGREGATE_STUDY_UNIT` |
| review/case-control | non-target document/unit |
| mother's demographics extracted for neonate | separate anchors + demographic ownership |

No case above requires a disease-specific exception in the representation itself.

---

# 17. What the Schema Deliberately Does Not Encode Yet

The following remain intentionally unresolved until later Phase C work:

## 17.1 Disease-specific evidence matrix

The schema knows that evidence must be disease-discriminative, but it does not yet say exactly which test, pathogen, specimen, clinical pattern, or treatment response is sufficient for each of the 15 diseases.

That belongs to:

```text
03_evidence_specificity_matrix.md
```

## 17.2 Numerical evidence scoring

No numeric formula such as:

```text
score = 0.7 * PCR + 0.2 * symptoms + ...
```

is specified.

Doing so before the disease-specific evidence study would reintroduce the same premature assumptions that the ontology was designed to avoid.

## 17.3 Model choice

The schema does not favor:

```text
rules
BM25
MedCPT
Cross-Encoder
LLM
hybrid model
```

All must be evaluated as candidate mechanisms for producing the same representation.

## 17.4 Automatic claim reconciliation algorithm

The ontology requires reconciliation, but does not yet define a learned or deterministic resolver. That is a later experimental question.

---

# 18. Gold-Standard Annotation Implication

This schema implies that a future annotator should not be asked simply:

```text
"Is this article about tuberculosis?"
```

The annotation task should instead be decomposed:

```text
1. What is the document type?
2. What is the unit of analysis?
3. Who is the primary patient/subject?
4. Which disease concepts are mentioned?
5. Who/what does each mention refer to?
6. What is its assertion status?
7. What is its temporal status?
8. What clinical role does it play?
9. What evidence supports or contradicts it?
10. What clinical claim remains after reconciliation?
11. Does that claim satisfy VPD?
12. What is the final dataset label?
```

This decomposition is essential for Phase D because otherwise annotation disagreement will be hidden inside one binary diagnosis label.

---

# 19. Required Invariants for All Future Systems

Any future implementation evaluated against this schema must satisfy the following project-level invariants:

```text
I1  Disease mention is not sufficient for disease label.
I2  Retrieval score is not sufficient for disease verification.
I3  Metadata is not sufficient for patient-level diagnosis.
I4  Assertion, temporality, experiencer, and clinical role are distinct.
I5  Patient anchoring precedes dataset labeling.
I6  Evidence specificity must discriminate the target disease.
I7  Document scope precedes case scope.
I8  Multiple claims must be reconciled before final labeling.
I9  Contradictory patient-specific evidence cannot be ignored merely because
    a lexical disease mention exists.
I10 The representation must remain auditable back to source text.
```

These are research invariants, not software implementation preferences.

---

# 20. Phase C Exit Criteria for Task 1

Task 1 is considered complete when:

```text
[✓] ClinicalCaseUnit formally represented
[✓] PatientAnchor formally represented
[✓] DiseaseMention formally represented
[✓] EvidenceObject formally represented
[✓] ClinicalClaim formally represented
[✓] Controlled vocabularies frozen for Phase C
[✓] Positive-diagnosis conditions specified
[✓] Structural JSON Schema defined
[✓] Semantic validation invariants defined
[✓] Observed failure modes expressible without case-specific patches
[ ] Disease-specific evidence matrix completed
[ ] Gold-standard annotation guide completed
```

The final two items belong to the subsequent Phase C/D artifacts and are intentionally not solved here.

---

# 21. Research Position

The schema establishes the following formal distinction:

```text
LEXICAL OBSERVATION
        ↓
SEMANTIC MENTION
        ↓
PATIENT-ANCHORED CONTEXT
        ↓
CLINICAL EVIDENCE
        ↓
DISEASE CLAIM
        ↓
RECONCILED CLAIM STATUS
        ↓
DATASET LABEL
```

The central hypothesis for the next research phase is therefore:

> **A clinically defensible disease dataset requires a representation in which disease labels are derived from reconciled patient-centered claims rather than directly from lexical mentions or retrieval scores.**

Phase C Task 2 will test how far this representation can be grounded in a disease-specific **Evidence Specificity Matrix** for the 15 target diseases.

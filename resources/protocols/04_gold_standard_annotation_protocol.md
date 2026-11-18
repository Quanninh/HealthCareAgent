# Gold-Standard Annotation Protocol

**Milestone 3 — Phase D / Task 1**  
**Status:** Research specification — code remains frozen  
**Date:** 2026-10-02  
**Depends on:** `01_clinical_claim_ontology.md`, `02_clinical_claim_schema.md`, `03_evidence_specificity_matrix.md`  
**Scope:** Gold-standard annotation of patient-centric clinical claims for the 15 target diseases in the MultiCaRe project

---

## 0. Purpose

This document defines the annotation protocol used to construct a **Gold-Standard Clinical Claim Dataset** against which all future retrieval, verification, rule-based, machine-learning, or LLM-based systems will be evaluated.

The protocol follows the project invariant:

```text
MENTION ≠ EVIDENCE ≠ CLAIM ≠ LABEL
```

The annotation task is therefore **not**:

```text
"Does the disease name appear in the article?"
```

and not:

```text
"Does this case look medically compatible with the disease?"
```

The annotation task is:

> **Given a biomedical document, identify the valid clinical case unit, identify the patient/subject being described, interpret disease mentions in context, attach the relevant evidence to that subject, reconcile competing claims, and determine whether the patient satisfies the project's strict dataset-level positive-diagnosis standard.**

This protocol is deliberately separated from implementation. No regex, model, retrieval score, or current pipeline output is authoritative for annotation.

---

# 1. Gold-Standard Objectives

The gold standard must answer five independent questions:

```text
Q1. What is this document / unit of analysis?
Q2. Who is the clinical subject?
Q3. What disease-related claims are actually made about that subject?
Q4. What evidence supports or contradicts each claim?
Q5. Does the reconciled claim satisfy the dataset-level positive label standard?
```

These questions must be answered in order because later judgments depend on earlier scope decisions.

### 1.1 Primary outputs

For every annotated item, the gold set should contain:

- `document_type`
- one or more `ClinicalCaseUnit` objects as applicable
- `PatientAnchor` objects
- `DiseaseMention` objects for target-disease-relevant mentions
- `EvidenceObject` objects
- `ClinicalClaim` objects
- reconciled `final_claim_status`
- `dataset_label`
- evidence and rationale traceability
- annotator confidence / uncertainty flags
- adjudication status

### 1.2 Secondary outputs

The gold set should also preserve disagreement-relevant information, including:

- ambiguous subject references;
- unresolved disease terminology;
- conflicting evidence;
- insufficient information;
- competing interpretations considered by annotators;
- failure-family tags (`F1`–`F6`) when a failure mode is present.

The gold set must therefore support both **benchmarking** and **error analysis**.

---

# 2. Annotation Philosophy

## 2.1 Observed facts before derived decisions

Annotators must first record what the document actually states before assigning a derived claim or label.

```text
Observed text
    ↓
Structured interpretation
    ↓
Claim
    ↓
Dataset label
```

Do not infer an unreported diagnostic fact merely because it would be clinically plausible.

## 2.2 Patient anchoring precedes disease interpretation

The same disease mention can have different meanings depending on its subject:

```text
patient has TB
mother has TB
history of TB in father
possible TB in differential
TB mentioned in discussion
TB infection in animal
```

These are not equivalent claims.

## 2.3 Disease-specific evidence is not interchangeable

Annotators must use `03_evidence_specificity_matrix.md` when deciding whether evidence is E1/E2/E3/E0 or contradictory.

The protocol explicitly prohibits the shortcut:

```text
"medical-sounding" evidence → positive diagnosis
```

## 2.4 Uncertainty must be represented, not hidden

When the document does not provide enough information to establish a judgment, annotators should use the schema's uncertainty/insufficient-evidence mechanisms rather than inventing certainty.

---

# 3. Annotation Unit and Sampling Frame

## 3.1 Fundamental annotation unit

The primary sampling unit is a **document entry** from the MultiCaRe-derived candidate corpus.

Within each sampled document, annotation proceeds over one or more `ClinicalCaseUnit` objects.

Therefore:

```text
1 document
    may contain
0, 1, or multiple CCUs
```

A document must not be forced into a single-patient interpretation merely because the dataset contains one row for it.

## 3.2 Target population

The gold-standard set is intended to evaluate curation of **human patient-centered clinical cases** for the project's 15 target diseases.

The benchmark must deliberately include non-target and exclusionary documents because the principal scientific problem is not disease recognition alone; it is distinguishing valid patient-level claims from misleading lexical or contextual signals.

## 3.3 Recommended sample size

Target range:

```text
100–200 document-level cases
```

A practical operational target is approximately **150 cases**, subject to availability and annotation burden.

The final sample size should be reported explicitly and should not be inflated by counting multiple claims from one document as independent documents.

---

# 4. Sampling Strategy

## 4.1 Principle: stratified purposive sampling

Random sampling alone is insufficient for this milestone because many critical failure modes are rare.

The sample should therefore deliberately cover:

1. all 15 target diseases;
2. valid positive cases;
3. true negatives / irrelevant mentions;
4. ambiguous and confusable cases;
5. all six failure families;
6. heterogeneous document types;
7. cases with contradictory evidence.

## 4.2 Required strata

### Stratum A — Disease coverage

Every target disease must appear in the gold set.

Where corpus prevalence differs greatly across diseases, disease-balanced sampling should be used for the benchmark analysis rather than allowing common diseases to dominate the final metric.

### Stratum B — Failure coverage

The sample must include representatives of:

| Code | Failure family | Required coverage examples |
|---|---|---|
| F1 | Lexical ambiguity / entity disambiguation | `walking aids` vs AIDS; `patent foramen ovale` vs *P. ovale* |
| F2 | Unit-of-analysis / document scope | cohort; case series; veterinary; mathematical model; review |
| F3 | Patient anchoring / coreference | mother vs neonate; family member vs patient |
| F4 | Assertion / temporality | no history; negative test; historical disease; resolved disease |
| F5 | Discourse role vs active diagnosis | vaccination; infection-control context; pandemic background; differential diagnosis |
| F6 | Evidence specificity / pathogen discrimination | AFB vs TB; *M. avium* vs *M. tuberculosis*; non-specific serology |

### Stratum C — Claim status

Include cases that contain:

```text
AFFIRMED
NEGATED
HISTORICAL
POSSIBLE / SUSPECTED
CONTEXT_ONLY
INSUFFICIENT
CONTRADICTORY / DISCORDANT
```

### Stratum D — Evidence strength

Include examples spanning:

```text
E1
E2
E3
E0
C1
C2
C3
```

Not every document must contain every class, but the final gold set should cover all classes used in the schema.

## 4.3 Known high-value seed cases

The benchmark should deliberately include the previously identified MultiCaRe cases that motivated the ontology, including examples analogous to:

- `PMC8438790_01` — `walking aids` lexical ambiguity;
- `PMC9124883_01` — `ovale` / patent foramen ovale ambiguity;
- `PMC3736967_01` — explicit absence/history of tuberculosis;
- `PMC9170507_01` — nonreactive HIV serology;
- `PMC3090653_01` — HIV tests returned negative;
- `PMC4531616_01` — AFB with negative *M. tuberculosis* PCR / alternative mycobacterium;
- `PMC8184239_01` — AFB evidence in leprosy;
- `PMC9062907_01–03` — COVID-19 vaccination context;
- `PMC9149410_02` — COVID-19 infection-control context;
- `PMC9195123_01` — COVID-19 as pandemic background;
- `PMC10321783_01` — COVID-19 in differential/hypothesis;
- `PMC7074520_01` and `PMC7652926_04/_05` — veterinary/non-human subjects;
- `PMC9137965_01` / `PMC8434904_01` — mathematical/ML non-case documents;
- `PMC8282370_01` — neonate/mother demographic anchoring.

These cases are **seed examples, not the complete benchmark**. Additional cases must be selected to avoid a benchmark that simply memorizes the currently known errors.

---

# 5. Annotator Roles and Independence

## 5.1 Recommended annotation team

A minimum robust setup is:

```text
Annotator A — clinical annotation
Annotator B — independent clinical annotation
Adjudicator — senior clinical reviewer / consensus authority
Research lead — protocol and dataset quality control
```

The adjudicator should be independent of the initial annotation whenever possible.

## 5.2 Blinding requirement

Primary annotators must be **blind to the current pipeline's predicted label** and preferably blind to retrieval/evidence scores.

They may use the document, article metadata, the annotation ontology, the evidence matrix, and authorized clinical references, but they must not see:

- current dataset labels;
- current confidence tiers;
- BM25 scores;
- current pipeline assertion outputs;
- model predictions.

This prevents incorporation of the system's existing errors into the gold standard.

## 5.3 Independent first-pass annotation

Annotators A and B must perform their first-pass annotations independently.

They must not discuss individual cases until the independent annotation pass is complete.

---

# 6. Twelve-Step Decomposed Annotation Workflow

The following twelve steps are mandatory and ordered.

---

## Step 1 — Determine `document_type`

Question:

> What kind of document is this at the publication/document level?

Use the controlled vocabulary from the schema.

Annotator should consider:

- metadata/publication type;
- title;
- abstract;
- full-text structure;
- article purpose.

Important rule:

```text
Publication Type ≠ Clinical Case Unit
```

Do not infer a human single-patient case merely from a label such as `Case Reports`.

### Record

- `document_type`
- supporting evidence location
- confidence / uncertainty flag

---

## Step 2 — Determine `ccu_type` and unit of analysis

Question:

> What is the actual unit being described?

Possible interpretations include:

```text
SINGLE_HUMAN_PATIENT
MULTIPLE_HUMAN_PATIENTS / CASE_SERIES
COHORT / POPULATION
ANIMAL SUBJECT
NON_CLINICAL_MODEL
REVIEW / COMMENTARY / GUIDELINE
OTHER / UNSUITABLE
```

A document can contain multiple units. Create separate CCUs when the article genuinely describes separable patient-level cases.

### Reject the false shortcut

```text
one row in dataset → one patient
```

That assumption is explicitly prohibited.

---

## Step 3 — Establish `PatientAnchor` objects

Question:

> Who are the subjects to whom clinical statements refer?

Create one anchor per clinically relevant subject.

Minimum distinction:

```text
PRIMARY_PATIENT
OTHER_HUMAN
FAMILY_MEMBER
CLINICIAN / HEALTHCARE_WORKER
POPULATION / COHORT
ANIMAL
UNKNOWN / UNRESOLVED
```

For target-case curation, identify the primary patient only when the document supports that role.

### Demographic rule

Age, sex, pregnancy status, and related demographics must be attached to the correct subject anchor.

Never assign:

```text
first age mentioned in document → patient age
```

---

## Step 4 — Identify disease-relevant `DiseaseMention` objects

Annotate mentions that could plausibly affect the target disease claim.

For each mention record:

- text span;
- normalized concept;
- disease target if applicable;
- subject anchor if locally resolvable;
- document/section location.

### Critical rule

A text span is only a **mention** at this stage.

Do not assign disease diagnosis merely because the concept is present.

---

## Step 5 — Perform concept grounding / sense disambiguation

Question:

> What clinical concept does the mention actually denote in this context?

Examples:

```text
"walking aids"
    → MOBILITY_AID
    → not HIV/AIDS

"patent foramen ovale"
    → CARDIAC_ANATOMICAL_FINDING
    → not Plasmodium ovale
```

When ambiguity remains, record the ambiguity rather than forcing a target-disease normalization.

---

## Step 6 — Assign `assertion_type`

For each disease-relevant claim candidate, determine whether the disease is:

```text
AFFIRMED
NEGATED
HISTORICAL
POSSIBLE / SUSPECTED
UNKNOWN / UNRESOLVED
```

Use surrounding syntax and clinical meaning, not keyword presence.

Examples:

```text
"has tuberculosis"
→ AFFIRMED

"no history of tuberculosis"
→ NEGATED

"treated for tuberculosis in childhood"
→ HISTORICAL

"tuberculosis was considered"
→ POSSIBLE
```

---

## Step 7 — Assign `temporality`

Determine when the statement applies relative to the clinical case.

At minimum distinguish:

```text
CURRENT
HISTORICAL / REMOTE
FUTURE / PLANNED
UNKNOWN
```

Temporality is independent of assertion.

For example:

```text
Current disease + AFFIRMED
Historical disease + AFFIRMED
Current disease + NEGATED
```

are all distinct states.

---

## Step 8 — Assign `clinical_role` and `discourse_role`

These fields must be annotated independently from assertion.

### Clinical role examples

```text
DIAGNOSIS
SYMPTOM / SIGN
TESTING
TREATMENT
PREVENTION / VACCINATION
EXPOSURE
DIFFERENTIAL_DIAGNOSIS
FAMILY_HISTORY
COMORBIDITY
OTHER
```

### Discourse role examples

```text
PATIENT_PRESENTATION
DIAGNOSTIC_WORKUP
ASSESSMENT
TREATMENT
FOLLOW_UP
BACKGROUND
DISCUSSION
LITERATURE_REVIEW
PUBLIC_HEALTH_CONTEXT
OTHER
```

Example:

> “The patient received COVID-19 vaccination.”

may be:

```text
assertion = AFFIRMED
clinical_role = PREVENTION / VACCINATION
```

It must **not** become a COVID-19 infection claim.

---

## Step 9 — Create and classify `EvidenceObject` objects

For every candidate disease claim, identify evidence explicitly supporting, weakening, or contextualizing it.

Record:

- evidence span;
- evidence category;
- relation to claim;
- evidence strength (`E1`–`E3`, `E0`, `C1`–`C3`);
- subject anchor;
- specimen/test details when stated;
- timing when stated.

### Evidence rule

The annotator must ask:

> “Does this evidence discriminate the target disease from clinically plausible alternatives?”

not merely:

> “Is this evidence compatible with the disease?”

---

## Step 10 — Reconcile contradictory or competing claims

When more than one claim exists for the same patient and disease, annotate all relevant claims first. Then reconcile them.

Recommended evidence precedence:

```text
Final explicit diagnosis
        >
Disease-specific confirmatory evidence
        >
Strong algorithmic evidence
        >
Supportive evidence
        >
Initial suspicion / differential
        >
Background/context mention
```

This is a **clinical evidence hierarchy for dataset curation**, not a universal bedside decision rule.

### Example pattern

```text
Initial suspicion: TB
      ↓
AFB positive
      ↓
TB PCR negative
      ↓
M. avium identified
```

The annotator must not count disease mentions. The final claim must reflect the reconciled evidence.

### Contradiction rule

Do not classify a negative result as C3 solely because the result is negative. Consider:

- target organism;
- specimen;
- timing;
- assay;
- disease site;
- known limitations;
- subsequent evidence.

---

## Step 11 — Apply the Valid Positive Diagnosis (VPD) test

A strict positive diagnosis requires all mandatory conditions defined by the ontology and schema.

Conceptually:

```text
Correct patient/subject
        AND
Correct disease concept
        AND
AFFIRMED current/appropriate claim
        AND
Disease-relevant clinical role
        AND
Adequate patient-level evidence
        AND
No unresolved exclusionary contradiction
        ↓
VALID POSITIVE DIAGNOSIS
```

The following do **not** satisfy VPD by themselves:

- disease mention;
- metadata-only disease label;
- exposure history;
- vaccination;
- disease in differential diagnosis;
- empirical therapy;
- non-specific symptom;
- generic imaging finding;
- generic inflammatory finding;
- E3-only evidence.

Annotators must use the disease-specific matrix for the target disease before declaring VPD.

---

## Step 12 — Assign final dataset label and audit record

After all prior steps are complete, assign the final dataset label.

The final label must be traceable to the chain:

```text
Document
  ↓
CCU
  ↓
PatientAnchor
  ↓
DiseaseMention
  ↓
ClinicalContext
  ↓
Evidence
  ↓
Reconciliation
  ↓
VPD
  ↓
DatasetLabel
```

Every positive or exclusionary decision must therefore have an auditable explanation.

---

# 7. Final Dataset Label Policy

The exact controlled vocabulary is inherited from `02_clinical_claim_schema.md`.

At annotation time, the semantic decision should distinguish at least:

```text
POSITIVE_DIAGNOSIS
NEGATIVE / EXCLUDED
HISTORICAL_ONLY
POSSIBLE / SUSPECTED
CONTEXT_ONLY
INSUFFICIENT_EVIDENCE
NON_TARGET / WRONG_ENTITY
NON_CASE / OUT_OF_SCOPE
```

The final dataset encoding must use the exact schema enum rather than inventing a second vocabulary.

---

# 8. Annotation Evidence Requirements

## 8.1 Positive labels

Every `POSITIVE_DIAGNOSIS` annotation must cite at least one patient-anchored disease-discriminative evidence object.

The annotation record should store:

```text
claim_id
patient_anchor_id
disease_mention_id
evidence_id(s)
reconciliation_rationale
```

## 8.2 Negative / excluded labels

A negative or exclusionary decision must state whether it is based on:

- explicit clinical negation;
- definitive alternative diagnosis;
- exclusionary test evidence;
- wrong subject;
- wrong entity/sense;
- context-only mention;
- non-case document type;
- insufficient case evidence.

## 8.3 Insufficient evidence

`INSUFFICIENT_EVIDENCE` must be used when the document does not permit a defensible decision under the project's VPD standard.

This category is important because forced binary labels create artificial certainty and damage benchmark validity.

---

# 9. Evidence Traceability Standard

Every dataset-level decision must be traceable to exact document evidence.

For each final claim, retain:

```text
source_document_id
section / location
exact evidence sentence or text span
patient_anchor_id
concept id / normalized concept
assertion
temporality
clinical_role
evidence_category
evidence_strength
contradiction status
final rationale
```

### 9.1 No unsupported annotation

An annotator may not record:

```text
POSITIVE_DIAGNOSIS
```

without a retrievable supporting evidence span.

### 9.2 No evidence laundering

Do not cite a treatment, exposure, title, abstract, or metadata field as “evidence” if it only provides context and not patient-level disease support.

---

# 10. Handling Difficult / Ambiguous Cases

## 10.1 Ambiguous lexical mention

Use:

```text
normalized_concept = unresolved / non-target
```

rather than selecting the target disease by string similarity.

## 10.2 Ambiguous patient reference

Use `UNKNOWN / UNRESOLVED` when the document does not allow reliable subject assignment.

Do not borrow the demographic attributes of a nearby subject.

## 10.3 Contradictory evidence

Annotate every material claim and evidence object first. Reconciliation occurs only afterward.

## 10.4 Multiple patients in one article

Each patient-level case should receive its own CCU and PatientAnchor structure when separable.

Do not collapse a case series into one synthetic patient.

## 10.5 Veterinary / non-human material

A veterinary case must not be converted into a human patient case merely because the disease term is a target disease.

## 10.6 Review / discussion material

Disease mentions occurring only in review/discussion/background sections are not patient-level evidence unless the article explicitly relates them to the patient being reported.

---

# 11. Adjudication Protocol

## 11.1 First-pass disagreement

After independent annotation, compare:

```text
document_type
ccu_type
primary patient anchor
disease concept
assertion
temporality
clinical_role
evidence strength
claim status
final dataset label
```

## 11.2 Disagreement classes

Each disagreement should be categorized before resolution:

```text
D1 — Scope disagreement
D2 — Subject anchoring disagreement
D3 — Concept normalization disagreement
D4 — Assertion/temporality disagreement
D5 — Clinical-role/discourse disagreement
D6 — Evidence-strength disagreement
D7 — Reconciliation disagreement
D8 — VPD / final-label disagreement
```

This enables measurement of **where the ontology is difficult**, rather than merely reporting one overall agreement number.

## 11.3 Adjudication rule

The adjudicator reviews:

1. the source text;
2. both independent annotations;
3. the ontology;
4. the evidence matrix;
5. the documented rationale.

The adjudicator must issue a final structured decision and record the reason for overriding either annotator.

### 11.4 Protocol revision trigger

If disagreement reveals that:

- an ontology category is missing;
- two labels are not operationally distinguishable;
- a disease-specific evidence rule is ambiguous;
- an annotation instruction is interpreted consistently in incompatible ways;

then **the protocol is revised before continued large-scale annotation**.

Changes must be versioned.

---

# 12. Inter-Annotator Agreement (IAA)

IAA is measured **per annotation layer**, not only on the final disease label.

## 12.1 Required agreement layers

At minimum report:

| Layer | Example variable | Why measure it separately? |
|---|---|---|
| Document scope | `document_type` | Detect publication/document ambiguity |
| Unit of analysis | `ccu_type` | Detect case-vs-cohort ambiguity |
| Subject | primary patient anchor | Detect patient-linking errors |
| Concept | normalized disease concept | Detect lexical/grounding errors |
| Assertion | `assertion_type` | Detect negation/hypothesis errors |
| Temporality | `temporality` | Detect historical/current errors |
| Clinical role | `clinical_role` | Detect vaccine/exposure/differential errors |
| Evidence | `evidence_strength` | Detect medical evidence disagreement |
| Claim | `final_claim_status` | Detect claim-level disagreement |
| Dataset label | `dataset_label` | Benchmark endpoint |

## 12.2 Recommended statistics

For two primary annotators and categorical variables:

- **Cohen's kappa** may be reported for nominal categories.

For three or more annotators:

- **Fleiss' kappa** may be used for nominal categorical agreement.

For annotation schemes with missing values, ordinal structure, or more complex disagreement patterns, an additional reliability statistic such as **Krippendorff's alpha** may be reported where appropriate.

Raw agreement must also be reported because kappa can be affected by class prevalence.

## 12.3 Span-level agreement

For text spans such as disease mentions or evidence spans, categorical kappa alone is insufficient.

Report a span-level metric such as:

- exact-match precision/recall/F1;
- overlap-based agreement where scientifically justified.

The metric and overlap definition must be fixed before seeing the final results.

## 12.4 Claim-level agreement

The highest-value agreement endpoint is:

```text
Does the same patient-centered disease claim exist?
```

A system should not be considered successful merely because two annotators agree that the string “tuberculosis” appears.

---

# 13. Agreement Interpretation Policy

IAA values must not be interpreted as a universal quality grade detached from the task.

The report should distinguish:

```text
high agreement on obvious lexical cases
vs.
low agreement caused by genuine clinical ambiguity
vs.
low agreement caused by a defective guideline
```

A low agreement rate is therefore a signal for protocol review, not automatically annotator failure.

### 13.1 Required reporting

For each layer report:

```text
N annotated units
raw agreement
agreement statistic
95% confidence interval where feasible
number of adjudicated cases
number of unresolved cases
major disagreement categories
```

---

# 14. Annotator Training and Calibration

## 14.1 Training sequence

Before independent annotation, annotators should complete a calibration batch containing:

- straightforward positive cases;
- straightforward negative/context cases;
- one or more examples from each F1–F6 family;
- contradictory evidence cases;
- ambiguous subject cases.

Calibration examples should be reviewed jointly.

## 14.2 No protocol tuning on the final benchmark

The benchmark set must not be repeatedly re-labeled until agreement looks high.

The recommended separation is:

```text
Calibration set
    ↓
Protocol refinement
    ↓
Freeze protocol
    ↓
Independent gold annotation
    ↓
Adjudication
```

## 14.3 Frozen benchmark principle

Once the final benchmark annotation begins, changes to ontology or labeling rules require explicit versioning and documentation.

---

# 15. Quality-Control Gates

The gold dataset cannot be declared complete unless all gates pass.

## Gate 1 — Structural completeness

Every record contains all mandatory schema fields.

## Gate 2 — Patient anchoring completeness

Every positive claim has a valid patient/subject anchor.

## Gate 3 — Evidence traceability

Every positive diagnosis has at least one cited supporting evidence object.

## Gate 4 — Contradiction review

Cases containing material contradictory evidence have a reconciliation record.

## Gate 5 — Failure-mode coverage

All six failure families are represented.

## Gate 6 — Disease coverage

All 15 target diseases are represented.

## Gate 7 — IAA reporting

Layer-level agreement statistics are computed and documented.

## Gate 8 — Adjudication completeness

All disagreements affecting final labels are resolved or explicitly marked unresolved.

## Gate 9 — Provenance integrity

Every final label can be traced to source text and annotation decisions.

## Gate 10 — No model leakage

The final gold label does not depend on hidden/current pipeline output.

---

# 16. Gold Record Minimal Example

A positive case should conceptually contain:

```json
{
  "document": {
    "document_id": "CASE_001",
    "document_type": "CASE_REPORT"
  },
  "case_unit": {
    "ccu_id": "CCU_001",
    "ccu_type": "SINGLE_HUMAN_PATIENT"
  },
  "patient_anchor": {
    "patient_id": "PATIENT_001",
    "subject_class": "PRIMARY_PATIENT",
    "demographics": {
      "age": 34,
      "age_unit": "years",
      "sex": "female"
    }
  },
  "disease_mention": {
    "mention_id": "M_001",
    "normalized_concept": "Tuberculosis"
  },
  "evidence": [
    {
      "evidence_id": "E_001",
      "evidence_strength": "E1",
      "evidence_relation": "SUPPORTS",
      "patient_anchor_id": "PATIENT_001"
    }
  ],
  "claim": {
    "claim_id": "CLM_001",
    "patient_anchor_id": "PATIENT_001",
    "assertion_type": "AFFIRMED",
    "temporality": "CURRENT",
    "clinical_role": "DIAGNOSIS"
  },
  "final_claim_status": "POSITIVE_DIAGNOSIS",
  "dataset_label": "POSITIVE"
}
```

This example is intentionally structural. Disease-specific evidence admissibility comes from `03_evidence_specificity_matrix.md` and the actual source text.

---

# 17. Canonical Negative / Contextual Examples

## 17.1 Negated disease

```text
"There was no history of tuberculosis."
```

Expected semantic structure:

```text
mention = Tuberculosis
assertion = NEGATED
clinical_role = HISTORY / DIAGNOSTIC_CONTEXT
final_claim_status ≠ POSITIVE_DIAGNOSIS
```

## 17.2 Historical disease

```text
"The patient had tuberculosis in childhood."
```

```text
assertion = AFFIRMED
temporality = HISTORICAL
final label ≠ current positive diagnosis unless the dataset definition explicitly targets historical disease
```

## 17.3 Vaccination

```text
"The patient received COVID-19 vaccination."
```

```text
assertion = AFFIRMED
clinical_role = PREVENTION / VACCINATION
```

This is not a COVID-19 infection claim.

## 17.4 Family member disease

```text
"The patient's mother had tuberculosis."
```

```text
experiencer / subject = MOTHER
primary patient claim = absent
```

## 17.5 Veterinary case

```text
"An 11-year-old domestic cat was diagnosed ..."
```

```text
subject_class = ANIMAL
ccu_type ≠ SINGLE_HUMAN_PATIENT
```

---

# 18. Failure Annotation Overlay

Failure labels are not substitutes for clinical labels. They are a **secondary error-analysis layer**.

A single case may have multiple failure families.

Example:

```text
Mother's age extracted as neonate age
        ↓
F3 — Patient Anchoring

COVID-19 mentioned because of vaccination
        ↓
F5 — Discourse Role

Article summarizes 43 cases
        ↓
F2 — Unit of Analysis
```

This overlay allows future experiments to report:

```text
overall label accuracy
        +
accuracy by failure family
```

rather than hiding all errors inside one aggregate metric.

---

# 19. Benchmark Leakage Prevention

Because the gold set is intended to evaluate the entire future pipeline, the following must be avoided:

1. Using current model predictions to make gold decisions.
2. Repeatedly tuning rules on the held-out benchmark.
3. Allowing benchmark-specific lexical exceptions into the production system before evaluation is frozen.
4. Selecting only cases already known to be problematic.

The benchmark should contain both:

```text
known failure cases
+
unseen cases from the same failure families
```

to distinguish genuine generalization from memorization.

---

# 20. Versioning and Provenance

Every gold annotation release must include:

```text
ontology_version
schema_version
evidence_matrix_version
annotation_protocol_version
annotator_ids (pseudonymized)
adjudication_version
annotation_date
source_document_version / identifier
```

Any change affecting annotation semantics requires a new protocol version.

Previous gold releases must remain reproducible.

---

# 21. Definition of a Completed Gold-Standard Case

A case is considered **gold-complete** only when all of the following are true:

```text
Document scope resolved
        AND
CCU type resolved
        AND
Patient anchor resolved (or explicitly unresolved)
        AND
Target disease mentions grounded
        AND
Assertion / temporality / experiencer / role annotated
        AND
Evidence objects annotated
        AND
Contradictions reconciled
        AND
VPD evaluated
        AND
Dataset label assigned
        AND
Source evidence traceable
        AND
Independent disagreement resolved/adjudicated
```

A record missing the evidence chain is not a complete positive gold case, even if both annotators happen to agree on its label.

---

# 22. Recommended Gold-Standard Release Structure

The final release should be separated into logically independent layers:

```text
01_raw_source_manifest
02_document_annotations
03_case_unit_annotations
04_patient_anchor_annotations
05_disease_mention_annotations
06_evidence_annotations
07_clinical_claim_annotations
08_reconciliation_annotations
09_final_labels
10_annotator_agreement
11_adjudication_log
12_failure_taxonomy_annotations
```

This structure permits later researchers to evaluate intermediate tasks independently.

---

# 23. Phase D Exit Criteria

Phase D / Task 1 is complete when:

- the 12-step annotation workflow is frozen;
- controlled vocabularies are mapped to the schema;
- annotator instructions cover F1–F6;
- sampling strata are defined;
- blinding rules are documented;
- IAA metrics are pre-specified;
- adjudication rules are documented;
- quality-control gates are defined;
- no benchmark decision depends on pipeline predictions.

The next artifact is:

```text
05_gold_standard_benchmark_cases.md
```

Its purpose is to define the actual 100–200 case benchmark roster and its sampling allocation.

---

# 24. Research Position

The Gold Standard is not merely a list of labels.

It is a **structured record of clinical reasoning made explicit and auditable**.

The project therefore treats the gold annotation as:

```text
Document understanding
      ↓
Patient anchoring
      ↓
Clinical concept grounding
      ↓
Assertion / temporality / role
      ↓
Evidence discrimination
      ↓
Claim reconciliation
      ↓
Dataset-level diagnosis label
```

The benchmark should ultimately allow the project to answer not only:

> “How accurate is the final classifier?”

but also:

> **“At which semantic layer does the system diverge from the clinical ground truth?”**

That is the central purpose of Phase D.

---

# 25. References / Governing Artifacts

1. `01_clinical_claim_ontology.md` — Clinical Claim Ontology & Failure Taxonomy.
2. `02_clinical_claim_schema.md` — Clinical Claim Representation / Formal Schema Specification.
3. `03_evidence_specificity_matrix.md` — Evidence Specificity Matrix for the 15 target diseases.
4. Project Research Invariants: Mention ≠ Diagnosis; Retrieval ≠ Verification; Metadata ≠ Patient Evidence; Patient Anchoring Precedes Labeling; Evidence must be disease-discriminative; Document scope precedes case scope.
5. Clinical assertion / context concepts derived from the project foundation's ConText / NegEx framing.

---

# 26. Final Annotation Checklist

Before submitting a case, annotator must be able to answer **yes** to all applicable questions:

```text
[ ] Did I identify the actual document type?
[ ] Did I determine the true unit of analysis?
[ ] Did I identify the correct patient/subject?
[ ] Did I attach demographics to that subject rather than the first person mentioned?
[ ] Did I distinguish disease mention from disease claim?
[ ] Did I resolve lexical ambiguity?
[ ] Did I annotate assertion?
[ ] Did I annotate temporality?
[ ] Did I annotate experiencer / subject correctly?
[ ] Did I distinguish diagnosis from vaccine / exposure / differential / background?
[ ] Did I attach evidence to the correct patient?
[ ] Did I assess evidence specificity using the disease matrix?
[ ] Did I identify contradictory evidence?
[ ] Did I reconcile competing claims?
[ ] Did I apply VPD rather than clinical intuition alone?
[ ] Can another reviewer trace my final label back to exact source text?
```

If any answer is **no**, the case is not ready for gold-release status.

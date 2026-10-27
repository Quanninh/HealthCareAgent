# Clinical Claim Ontology & Failure Taxonomy

**Milestone 3 — Phase A & Phase B**  
**Status:** Research specification — code frozen  
**Date:** 2026-10-02  
**Scope:** MultiCaRe single-patient clinical case curation for 15 target diseases

---

## 0. Purpose

This document defines the **research object** that the project is trying to curate.

The central change is ontological:

> A disease label is not equivalent to a disease mention.

The project must determine whether a biomedical document contains a **patient-centered clinical claim** that supports the presence of a target disease in the patient represented by the case unit.

The intended reasoning chain is:

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

This specification deliberately does **not** define an implementation. Regexes, retrieval models, LLMs, classifiers, embeddings, and rule engines are implementation choices that must be evaluated only after these objects and decision criteria are fixed.

---

# Phase A — Clinical Object Ontology

## A1. Core Ontological Principle

The smallest unit of meaning relevant to the dataset is not a token, sentence, or disease entity. It is a **claim about a clinical subject**.

Formally:

```text
DiseaseMention
    ≠
DiseaseClaim
```

A disease mention becomes a disease claim only when the system can establish sufficient context about:

1. **what concept** is being mentioned;
2. **who/what** the concept applies to;
3. **what assertion** is being made;
4. **when** the assertion applies;
5. **what clinical role** the mention plays;
6. **what evidence** supports or contradicts the claim;
7. **where in the document's discourse** the statement occurs.

This principle explains the previously observed errors:

- `walking aids` contains the lexical string `aids`, but the clinical concept is not HIV/AIDS.
- `no history of tuberculosis` mentions tuberculosis but explicitly denies the target condition for the patient.
- `patent foramen ovale` contains `ovale`, but the concept is cardiac anatomy rather than *Plasmodium ovale*.
- `COVID-19 vaccination` references COVID-19 without asserting that the patient has COVID-19.
- `mother was 29-year-old` contains demographics that belong to another person, not necessarily the patient.
- a tiger or cat case can be a genuine case report while still being outside a human-patient dataset.

---

## A2. Clinical Case Unit (CCU)

### Definition

A **Clinical Case Unit** is the smallest document-grounded unit that represents a coherent clinical subject or group of subjects for whom the article reports clinical observations, diagnostic reasoning, intervention, or outcome.

For this project, the target CCU is:

> **One human patient represented as the primary subject of a single-patient case narrative.**

A document may contain more than one CCU. A case-report article may contain multiple patients; each patient must be treated as a separate unit only when the article provides sufficiently separable patient-level narratives.

### Required properties

A valid target CCU must have:

```text
ccu_type = SINGLE_HUMAN_PATIENT
subject = identifiable patient anchor in the narrative
clinical_narrative = present
patient-level observations = present
```

### Explicit exclusions from the target CCU

The following are not target single-patient CCUs:

- aggregate cohort summaries;
- case-control populations;
- cross-sectional populations;
- clinical trials treated only as a study population;
- systematic reviews and meta-analyses;
- guidelines and recommendations;
- mathematical models;
- machine-learning frameworks or methodological papers;
- editorial/background/public-health commentary;
- animal or veterinary cases;
- laboratory-only specimens with no patient-level narrative;
- population-level surveillance reports.

### Important distinction

`Case report` as a publication label is evidence about document type, not proof that a single human patient is the target unit. The project therefore treats **document-level metadata and narrative-level unit identification as separate evidence sources**.

CARE case-report guidance itself emphasizes patient-specific information, the patient's concerns and findings, diagnoses, interventions, and outcomes as core content of a case report. citeturn772233search3turn772233search1

---

## A3. Subject / Patient Anchor

### Definition

A **Patient Anchor** is the document-level entity representing the subject whose clinical state is being described by the target case unit.

The anchor is not automatically the first person, first demographic expression, or first named individual in the document.

### Subject classes

```text
PATIENT_HUMAN
FAMILY_MEMBER
CAREGIVER / STAFF
OTHER_HUMAN
POPULATION
ANIMAL
IN_VITRO / SPECIMEN
UNKNOWN
```

The target dataset requires:

```text
subject_class = PATIENT_HUMAN
```

### Patient anchoring rule

A clinical fact may contribute to the disease claim only when it is attributable to the target patient anchor, unless the fact is explicitly used as indirect evidence in a clinically valid relation.

Examples:

```text
"The neonate was born to a 29-year-old mother."

29-year-old → FAMILY_MEMBER / MOTHER
neonate → PATIENT_HUMAN
```

Therefore the mother's age must not become the patient's demographic age.

### Key principle

> **Mention ownership precedes clinical interpretation.**

Before deciding whether `Tuberculosis` is positive, the system must know whose tuberculosis is being discussed.

ConText explicitly models the `experiencer` dimension because a disease can be mentioned as belonging to someone other than the patient, such as a family member. citeturn772233search0

---

## A4. Clinical Concept Mention

A **Clinical Concept Mention** is a textual span or semantically grounded phrase that refers to a clinical entity, condition, finding, symptom, test, pathogen, treatment, anatomical structure, or related biomedical concept.

Important distinction:

```text
Mention ≠ diagnosis
Mention ≠ patient condition
Mention ≠ evidence of disease
```

Examples:

| Mention | Actual interpretation | Disease claim? |
|---|---|---:|
| `tuberculosis` in “no history of tuberculosis” | negated history | No |
| `HIV` in “serologies were nonreactive” | negative test target | No |
| `COVID-19` in “COVID-19 vaccination” | vaccine/context object | No |
| `COVID-19` in “COVID-19 pneumonia was confirmed” | active diagnosis | Potentially yes |
| `AFB` | non-specific microbiological finding | Not sufficient alone for TB |
| `M. tuberculosis PCR positive` | disease-specific evidence | Potentially yes |

---

## A5. Context Layer

Each clinically relevant mention is interpreted through a context vector rather than a binary presence/absence flag.

### A5.1 Assertion

The assertion state answers:

> Is the condition stated to exist for the subject?

Recommended conceptual values:

```text
AFFIRMED
NEGATED
POSSIBLE / HYPOTHETICAL
CONDITIONAL
UNCERTAIN
UNMENTIONED
```

### A5.2 Temporality

The temporal state answers:

> When does the condition apply relative to the case being reported?

Recommended conceptual values:

```text
CURRENT / ACTIVE
RECENT / EPISODIC
HISTORICAL / RESOLVED
FUTURE / CONDITIONAL
UNKNOWN
```

ConText separates negation, temporality, and experiencer because these dimensions affect whether a mention should be interpreted as a patient condition. citeturn772233search0

### A5.3 Experiencer

```text
PATIENT
FAMILY_MEMBER
OTHER_PERSON
POPULATION
ANIMAL
UNKNOWN
```

### A5.4 Clinical Role

Clinical role answers:

> What function does the mention play in the clinical narrative?

Recommended values:

```text
PRIMARY_DIAGNOSIS
ACTIVE_COMORBIDITY
DIFFERENTIAL_DIAGNOSIS
RULED_OUT_DIAGNOSIS
PAST_HISTORY
SYMPTOM / FINDING
TEST_TARGET
TEST_RESULT
TREATMENT_TARGET
ADVERSE_EVENT / EXPOSURE
PREVENTION / VACCINATION
EPIDEMIOLOGICAL_CONTEXT
BACKGROUND / LITERATURE_REFERENCE
```

This dimension is deliberately separate from assertion. For example:

```text
"COVID-19 was considered in the differential."

assertion = POSSIBLE
clinical_role = DIFFERENTIAL_DIAGNOSIS
```

while:

```text
"COVID-19 vaccination was administered."

assertion = AFFIRMED
clinical_role = PREVENTION / VACCINATION
```

The entity is real in both statements, but neither is an active COVID-19 diagnosis.

### A5.5 Discourse / Section Role

Recommended values:

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

A disease mention inside a discussion paragraph should not automatically carry the same evidentiary weight as a disease statement in the patient presentation or diagnostic workup.

MACCR is particularly relevant here: its curators explicitly select a primary case-presentation section and associate text spans with high-level clinical concepts while retaining context, rather than treating the document as a flat collection of biomedical entities. citeturn295062search0turn295062search1

---

## A6. Evidence Object

An **Evidence Object** is a patient-anchored observation that can support, weaken, or contradict a clinical claim.

Evidence categories:

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

### Evidence specificity principle

Evidence must be evaluated for **specificity to the target disease**.

For example:

```text
AFB-positive
```

is evidence of a mycobacterial/acid-fast process, but is not by itself equivalent to:

```text
M. tuberculosis-positive
```

This prevents shared findings from leaking across diseases.

---

## A7. Disease Claim

### Definition

A **Disease Claim** is a structured proposition asserting that a target disease condition applies to the target patient within the target case unit.

Canonical form:

```text
CLAIM(
    subject = Patient_X,
    predicate = HAS_DISEASE,
    object = Disease_Y,
    assertion = AFFIRMED,
    temporality = CURRENT_OR_RELEVANT,
    experiencer = PATIENT,
    clinical_role = PRIMARY_DIAGNOSIS_OR_ACTIVE_DISEASE,
    evidence = E
)
```

A disease claim can be represented even when its final truth value is negative or uncertain; however, the positive dataset label requires an **affirmed patient-centered disease claim** under the criteria below.

---

## A8. Valid Positive Diagnosis (VPD)

### Definition

A **Valid Positive Diagnosis** is a disease claim that satisfies all mandatory conditions:

```text
1. Correct target disease concept
2. Correct human-patient subject
3. Positive / affirmed assertion
4. Relevant temporal status
5. Disease is playing a diagnostic or active clinical role
6. Evidence is located in patient-centered clinical narrative OR an explicit patient diagnosis is stated
7. Evidence is not contradicted by stronger patient-specific evidence
```

### Strong exclusion conditions

A candidate is **not** a Valid Positive Diagnosis if the target disease is mentioned only as:

- negated disease;
- ruled-out disease;
- family history;
- another person's condition;
- differential diagnosis with no confirmation;
- hypothetical/conditional condition;
- vaccine/prevention context;
- epidemiological background;
- exposure concern without disease diagnosis;
- literature discussion;
- study-level population attribute when the target CCU is a single patient;
- animal/veterinary condition;
- a nonspecific finding that cannot identify the target disease;
- lexical substring or ambiguous homonym.

### Evidence sufficiency hierarchy

For dataset curation, evidence should be interpreted in descending strength:

```text
E0  Direct patient diagnosis explicitly established in the case
E1  Disease-specific confirmatory evidence attributable to patient
E2  Highly characteristic clinical/diagnostic evidence with coherent patient context
E3  Supportive clinical findings only
E4  Generic/background/contextual mention
```

For a **high-precision positive dataset**, E0 or E1 is preferred. E2 may qualify only when the diagnosis is explicitly established by the clinical narrative and no stronger contradictory evidence exists. E3 and E4 are insufficient on their own.

### Non-sufficient evidence examples

```text
MeSH disease descriptor                   → insufficient alone
article title disease word               → insufficient alone
abstract disease word                    → insufficient alone
BM25 evidence score                      → insufficient alone
single symptom                           → insufficient alone
non-specific laboratory finding          → insufficient alone
mention in Discussion                    → insufficient alone
mention in differential diagnosis        → insufficient alone
mention in vaccination/exposure context  → insufficient alone
```

---

## A9. Minimum VPD Standard for the 15 Target Diseases

The project currently contains the following target disease classes:

```text
1.  COVID-19
2.  Tuberculosis
3.  HIV/AIDS
4.  Malaria
5.  Dengue
6.  Brucellosis
7.  Leishmaniasis
8.  Leptospirosis
9.  Typhoid Fever
10. Ebola Virus Disease
11. Zika Virus Infection
12. Cholera
13. Rabies
14. Chikungunya
15. Yellow Fever
```

A single universal **semantic rule** applies to all 15:

> The minimum positive label requires an affirmed, patient-anchored diagnosis of the target disease, supported either by an explicit case-level diagnosis or by disease-specific confirmatory/diagnostic evidence attributable to that patient.

Disease-specific laboratory and clinical evidence will be formalized separately as an **Evidence Matrix** in Phase C. This prevents the ontology from prematurely encoding test-specific assumptions that may vary by disease, setting, specimen, or diagnostic practice.

### Rules that apply across all 15 diseases

| Rule | Required? |
|---|---:|
| Human patient anchor | Yes |
| Correct disease concept | Yes |
| Affirmed / positive assertion | Yes |
| Active or case-relevant temporal relation | Yes |
| Disease is the patient's clinical condition, not merely context | Yes |
| Patient-level clinical evidence or explicit diagnosis | Yes |
| Metadata/MeSH alone | No |
| BM25/evidence score alone | No |
| Symptoms alone | Generally no |
| Nonspecific findings alone | No |
| Differential diagnosis alone | No |
| Family history / other experiencer | No |
| Animal case | No |

This is intentionally conservative. The dataset is a **curation benchmark**, so precision of the final label has priority over maximizing lexical coverage at this stage.

---

## A10. Claim Reconciliation

A case may contain multiple mentions of the same disease with different statuses.

Example:

```text
"Tuberculosis was initially suspected, but PCR was negative.
The final diagnosis was Mycobacterium avium infection."
```

The correct representation is not simply:

```text
Tuberculosis = mentioned
```

but:

```text
Claim_1: TB → POSSIBLE / DIFFERENTIAL
Claim_2: TB → NEGATED / RULED_OUT
Final patient disease → M. avium infection
```

Therefore, case-level labeling must reconcile **multiple claims**, not count disease mentions.

Priority is conceptually based on clinical resolution, not lexical frequency:

```text
Final / established diagnosis
        >
confirmed patient-specific evidence
        >
active diagnosis / presentation
        >
supportive findings
        >
differential / possible
        >
background mention
```

This is a research ordering for evidence interpretation, not an implementation recipe.

---

# Phase B — Failure Ontology

## B0. Purpose

The Failure Ontology converts observed false positives into reusable research categories.

A failure is not defined by the particular word that caused it. It is defined by the **semantic contract that was violated**.

The current project has six principal failure families.

---

## F1 — Lexical Ambiguity & Entity Disambiguation

### Definition

A lexical form is mapped to the wrong clinical concept because surface similarity is mistaken for semantic identity.

### Typical mechanism

```text
string match
   ↓
wrong concept
```

### Canonical MultiCaRe examples

1. `aids` in `without walking aids` → incorrectly interpreted as HIV/AIDS.
2. `ovale` in `patent foramen ovale` → incorrectly interpreted as *Plasmodium ovale*.

### Diagnostic signature

```text
entity string = matched
concept identity = wrong
```

### Why keyword expansion does not solve it

The problem is not vocabulary coverage. It is **sense disambiguation** and often requires surrounding lexical/syntactic/clinical context.

### Research question

> How should a biomedical mention be grounded to the correct clinical concept before disease-level reasoning begins?

---

## F2 — Unit-of-Analysis & Document Scope

### Definition

The system interprets a document as a single-patient clinical case when the document actually represents a different unit of analysis.

### Subtypes

```text
F2.1 Aggregate cohort
F2.2 Case series / multiple patients
F2.3 Case-control study
F2.4 Review / guideline / editorial
F2.5 Mathematical / computational model
F2.6 Public-health / epidemiological report
F2.7 Non-clinical framework / methodology paper
F2.8 Veterinary / animal report
```

### Canonical MultiCaRe examples

- COVID-19 article describing 43 patients with aggregate statistics.
- mathematical COVID-19 vaccination model.
- smart-city / ML framework paper.
- WHO or surveillance summaries.
- veterinary cat/tiger reports.

### Research question

> What is the unit of analysis represented by the document, and does it contain an eligible human single-patient case unit?

### Core distinction

```text
Publication Type
        ≠
Unit of Analysis
```

A `Case Reports` publication type does not by itself guarantee that the desired human single-patient unit has been correctly identified.

---

## F3 — Patient Entity Anchoring & Coreference

### Definition

A clinical attribute, finding, diagnosis, or demographic statement is assigned to the wrong subject.

### Subtypes

```text
F3.1 Mother/father ↔ infant
F3.2 Family member ↔ patient
F3.3 Staff/caregiver ↔ patient
F3.4 Population ↔ individual
F3.5 Animal ↔ human
F3.6 Multiple patients ↔ wrong patient
```

### Canonical MultiCaRe example

```text
"The neonate was born to a 29-year-old mother."
```

Incorrect:

```text
patient age = 29
```

Correct:

```text
patient = neonate
mother.age = 29
```

### Research question

> For each clinical statement, who is its experiencer/subject, and how is that subject linked to the target case unit?

---

## F4 — Clinical Assertion & Temporality

### Definition

A disease mention is interpreted as an active positive diagnosis even though the statement is negated, historical, hypothetical, or otherwise non-current.

### Subtypes

```text
F4.1 NEGATED
F4.2 HISTORICAL
F4.3 POSSIBLE / HYPOTHETICAL
F4.4 RULED OUT
F4.5 CONDITIONAL / FUTURE
F4.6 RESOLVED
```

### Canonical MultiCaRe examples

```text
"HIV serologies were nonreactive."
"both tests returned negative."
"No tuberculosis contact was noted."
"without a history of tuberculosis."
```

ConText demonstrates why these properties need explicit modeling: the same disease mention can mean very different things depending on negation, temporality, and experiencer. citeturn772233search0turn772233search2

### Research question

> What is the assertion state and temporal status of the disease claim for the target patient?

---

## F5 — Discourse Role vs Active Diagnosis

### Definition

A target disease appears in a clinically meaningful sentence, but the mention serves a role other than reporting that disease as the patient's active diagnosis.

### Subtypes

```text
F5.1 Vaccination / prevention
F5.2 Exposure-control context
F5.3 Pandemic / historical background
F5.4 Differential diagnosis
F5.5 Clinical hypothesis
F5.6 Literature discussion
F5.7 Epidemiological context
F5.8 Adverse-event / exposure relationship
```

### Canonical MultiCaRe examples

- `COVID-19 vaccination` in an aneurysm case.
- `minimize personnel exposure to COVID-19` in device management.
- `onset of the COVID-19 pandemic` in an internet-gaming-disorder case.
- `COVID-19-related lesions` as an initial clinical hypothesis before biopsy.

### Research question

> Does the disease mention function as a statement about the patient's disease state, or does it play another discourse/clinical role?

This category is deliberately separated from negation because:

```text
"COVID-19 vaccination"
```

can be perfectly **affirmed**, while still being irrelevant to a COVID-19 disease label.

---

## F6 — Evidence Specificity & Pathogen Discrimination

### Definition

A finding is real and patient-specific, but it is not sufficiently specific to establish the target disease.

### Subtypes

```text
F6.1 Shared organism class
F6.2 Non-specific laboratory finding
F6.3 Non-specific symptom/sign
F6.4 Shared diagnostic modality
F6.5 Wrong pathogen within same family/genus
F6.6 Contradictory disease-specific test
```

### Canonical MultiCaRe examples

```text
AFB-positive
```

can occur in more than one mycobacterial disease.

Likewise:

```text
M. avium identified
```

should not be converted into:

```text
M. tuberculosis disease
```

when the disease-specific evidence contradicts that mapping.

### Research question

> How specific is the observed evidence to the target disease, and does it discriminate the target from clinically similar conditions?

---

# B7. Cross-Failure Composition

Real errors can involve multiple failure families simultaneously.

Example:

```text
"COVID-19-related lesions were considered..."
```

may involve:

```text
F4  POSSIBLE / HYPOTHETICAL
+
F5  DIFFERENTIAL DIAGNOSIS
```

Another example:

```text
"AFB positive, PCR for M. tuberculosis negative"
```

may involve:

```text
F6  evidence specificity
+
F4  contradictory evidence
```

Another:

```text
29-year-old mother of a neonate
```

may involve:

```text
F3  patient anchoring
```

The taxonomy therefore permits **multi-label failure annotation**.

---

# B8. Failure Taxonomy Summary

| ID | Failure family | Core question violated |
|---|---|---|
| F1 | Lexical ambiguity & entity disambiguation | “What concept does this mention actually denote?” |
| F2 | Unit-of-analysis & document scope | “What kind of study/case is this?” |
| F3 | Patient anchoring & coreference | “Whose clinical state is being described?” |
| F4 | Assertion & temporality | “Is the disease actually asserted for this patient, and when?” |
| F5 | Discourse role vs active diagnosis | “Why is the disease mentioned?” |
| F6 | Evidence specificity & pathogen discrimination | “Does the evidence specifically support this disease?” |

---

# B9. From Failure Taxonomy to Gold Annotation

The failure ontology implies that a future gold-standard annotation must not record only:

```text
primary_disease = Tuberculosis
```

Instead, each candidate disease mention should be annotatable as:

```text
Document
 ├── document_type
 ├── unit_of_analysis
 │
 └── CaseUnit
      ├── patient_anchor
      ├── subject_type
      │
      └── DiseaseMention
           ├── concept
           ├── assertion
           ├── temporality
           ├── experiencer
           ├── clinical_role
           ├── discourse_role
           ├── evidence_type
           ├── evidence_specificity
           ├── contradiction_status
           └── final_claim_status
```

This is the conceptual bridge from Phase B to Phase C/D.

---

# B10. What Counts as a Dataset-Level Positive?

The final dataset label should be generated from the claim ontology, not from lexical counts.

Conceptually:

```text
DatasetPositive(case, disease)
    iff
        EligibleCaseUnit(case)
    AND PatientAnchor(case) is HUMAN
    AND ∃ ClinicalClaim
        such that
            claim.subject = target patient
            claim.concept = target disease
            claim.assertion = AFFIRMED
            claim.temporality ∈ {CURRENT, CASE_RELEVANT}
            claim.clinical_role ∈ {PRIMARY_DIAGNOSIS, ACTIVE_DISEASE}
            claim.evidence ≥ minimum acceptable specificity
            claim is not overridden by stronger contradictory evidence
```

This definition intentionally makes **final labeling downstream of semantic verification**.

---

# 11. Research Invariants

The following invariants should remain true regardless of future implementation:

### Invariant 1 — Mention is not diagnosis

```text
DiseaseMention → candidate evidence
DiseaseClaim → diagnostic proposition
```

### Invariant 2 — Retrieval is not verification

```text
BM25 / Dense Retrieval → candidate evidence
not → final diagnosis
```

### Invariant 3 — Metadata is not patient evidence

```text
MeSH / title / abstract metadata
        ≠
patient-level clinical confirmation
```

### Invariant 4 — Assertion is multidimensional

At minimum:

```text
assertion + temporality + experiencer
```

should be conceptually separate.

### Invariant 5 — Patient anchoring precedes label assignment

A disease statement cannot count toward the patient label until the subject of the statement is resolved.

### Invariant 6 — Evidence must be disease-discriminative

A shared or non-specific finding cannot automatically establish a specific disease.

### Invariant 7 — Document scope precedes case scope

Before asking “does the patient have X?”, establish that the document contains the intended kind of patient-level case.

---

# 12. Research Boundaries for Phase A/B

This document does **not** yet decide:

- which NLP model should perform each task;
- whether rules or learned models are superior;
- exact token windows or trigger lists;
- disease-specific laboratory thresholds;
- the final evidence-weighting formula;
- retrieval architecture;
- calibration parameters;
- production filtering logic.

Those questions belong to Phase C onward.

The purpose of Phase A/B is to make those later decisions **answerable and falsifiable**.

---

# 13. Immediate Research Consequences

The current implementation should therefore be considered a **baseline / historical artifact**, not the object to be incrementally patched.

The next artifacts should be:

```text
Phase C
01_clinical_claim_schema.md
02_evidence_specificity_matrix.md

Phase D
03_gold_standard_annotation_guideline.md
04_gold_standard_100_200_cases.md

Phase E
05_model_comparison_protocol.md
06_error_analysis_protocol.md
```

No implementation should be considered a solution merely because it increases the number of retained cases or removes previously observed false positives. It must demonstrate that it recovers the ontology defined here.

---

# 14. References

1. Harkema H, Dowling JN, Thornblade T, Chapman WW. **ConText: An Algorithm for Determining Negation, Experiencer, and Temporal Status from Clinical Reports.** Journal of Biomedical Informatics. 2009;42(5):839–851. citeturn772233search0
2. ConText / NegEx contextual modeling discussion: negation, temporality, experiencer, trigger scope, termination, and pseudo-trigger concepts. citeturn772233search0turn772233search2
3. CARE Checklist. **CARE Case Report Guidelines** — patient information, concerns, clinical findings, diagnoses, interventions, and outcomes as core case-report content. citeturn772233search3turn772233search1
4. **A reference set of curated biomedical data and metadata from clinical case reports.** MACCR; 3,100 curated clinical case reports with concept-level metadata and retained textual context. citeturn295062search0turn295062search4
5. **A Metadata Extraction Approach for Clinical Case Reports to Enable Advanced Understanding of Biomedical Concepts.** MACCR annotation methodology and concept-level contextual structure. citeturn295062search1

---

# 15. Project-Level Thesis

The project is no longer primarily a keyword-filtering problem.

It is a **patient-centered clinical claim curation problem**.

The core transformation is:

```text
BEFORE

mention → evidence score → label

AFTER

 document
    ↓
 unit of analysis
    ↓
 patient anchor
    ↓
 clinical concept
    ↓
 context
    ↓
 evidence + relations
    ↓
 clinical claim
    ↓
 label
```

The purpose of the next research phases is to determine whether this representation can be made reproducible, clinically defensible, and measurable — before deciding how it should be implemented.

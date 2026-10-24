# Evidence Specificity Matrix — 15 Target Diseases

**Milestone 3 — Phase C / Task 2**  
**Status:** Research specification — code remains frozen  
**Date:** 2026-10-02  
**Depends on:** `01_clinical_claim_ontology.md`, `02_clinical_claim_schema.md`  
**Scope:** Patient-centric clinical claim curation for the 15 target diseases in the MultiCaRe project

---

## 0. Purpose

This document defines the **disease-specific evidence semantics** that sit beneath the generic Clinical Claim Schema.

The purpose is not to create another keyword taxonomy. It is to answer a narrower clinical question:

> **When does a piece of evidence materially support a patient-level claim that the patient has the target disease, and when does apparently related evidence fail to distinguish that disease from plausible alternatives?**

The matrix is therefore designed around **disease discrimination**, not lexical overlap.

The core principle is:

```text
Disease mention
      ↓
Evidence object
      ↓
Evidence specificity
      ↓
Relation to patient-centered claim
      ↓
Claim reconciliation
      ↓
Dataset label
```

A disease term, pathogen family, symptom, treatment, or epidemiological context is **not** automatically diagnostic evidence.

---

# 1. A Critical Correction: E1 Is Not “≥99% Specificity”

A universal numerical rule such as:

```text
E1 = specificity ≥ 99%
```

is **not adopted**.

Diagnostic performance varies with:

- assay and platform;
- specimen type;
- timing relative to symptom onset;
- disease phenotype and stage;
- prior treatment;
- patient population;
- pre-test probability;
- reference standard;
- laboratory quality.

For example, a positive dengue NAAT or NS1 result can provide confirmed acute dengue evidence, but a negative NAAT/NS1 does not by itself rule out dengue. Similarly, WHO's current TB guidance uses different molecular tests and sampling strategies by age, HIV status, disease site and specimen type. citeturn550161search0turn550161search5turn877452search1turn877452search12

Therefore **E1/E2/E3 are semantic evidence classes, not numerical sensitivity/specificity bins**.

---

# 2. Evidence Classes

## E1 — Disease-defining / confirmatory evidence

Evidence that, when correctly identified, sampled, and interpreted in the appropriate clinical setting, can directly establish or strongly establish the target infection/disease.

Typical examples:

- detection of a target pathogen by an accepted molecular assay;
- isolation/culture of the target pathogen;
- direct demonstration of the pathogen in the appropriate specimen;
- a disease-specific diagnostic algorithm whose endpoint is a confirmed diagnosis.

**Important:** E1 means **diagnostically decisive in the stated context**. It does not mean that every E1 test is perfect or universally sufficient.

## E2 — Strong disease-discriminative / algorithm-dependent evidence

Evidence that substantially increases confidence and may support diagnosis when combined with timing, specimen, clinical context, or another test.

Examples:

- disease-specific antigen tests;
- serologic confirmation according to a disease-specific algorithm;
- paired-serum seroconversion;
- species-level microscopy when the morphology is sufficiently diagnostic;
- validated molecular evidence when the assay/specimen is not itself the final reference standard.

## E3 — Supportive / non-discriminative evidence

Evidence compatible with the disease but also compatible with important alternatives.

Examples:

- fever;
- thrombocytopenia;
- pulmonary infiltrates;
- AFB staining without organism identification;
- generic inflammatory markers;
- exposure history alone;
- empirical treatment alone.

E3 may strengthen a claim but **cannot by itself create a strict positive diagnosis label** in this project.

## E0 — Contextual / non-diagnostic

A mention can be clinically meaningful without being evidence that the patient has the disease.

Examples:

- vaccination;
- infection-control precautions;
- epidemiological background;
- public-health discussion;
- differential diagnosis;
- family history;
- disease mentioned in a literature review or discussion section.

## C — Contradictory evidence

Contradictory evidence is evidence that materially opposes a candidate claim.

It is divided conceptually into:

```text
C1 = discordant / weak contradiction
C2 = material contradiction
C3 = exclusionary contradiction in the stated context
```

The level cannot be assigned from the word “negative” alone. It depends on whether the test had adequate sensitivity for the disease, site, specimen and time point.

---

# 3. Contradiction Hierarchy

The project must **not** implement the following false rule:

```text
negative test → disease impossible
```

Instead:

```text
negative result
      ↓
Was the correct disease target tested?
      ↓
Was the correct specimen used?
      ↓
Was the timing appropriate?
      ↓
Was the assay sufficiently sensitive for this setting?
      ↓
Was repeat / alternative testing required?
      ↓
contradiction strength
```

### 3.1 C1 — Discordant

Example:

> One negative early NAAT, while symptoms and another independent test remain positive.

Interpretation:

```text
claim weakened
≠ claim disproved
```

### 3.2 C2 — Material contradiction

A well-targeted negative result on an appropriate specimen substantially conflicts with the proposed diagnosis, but false-negative disease remains plausible.

### 3.3 C3 — Exclusionary contradiction

Only when the diagnostic context makes the negative result sufficiently sensitive and appropriately timed to make the proposed diagnosis incompatible with the observed evidence.

### 3.4 Why this matters for MultiCaRe

The current case examples show exactly why a hierarchy is required. In the `PMC4531616_01` case, AFB positivity was not equivalent to *M. tuberculosis* because the article subsequently reported a negative PCR for *M. tuberculosis* and identified a different mycobacterial organism. Therefore:

```text
AFB positive
    ≠
Tuberculosis confirmed
```

The negative disease-specific result and the alternative organism must be represented as **claim-specific contradictory and discriminative evidence**, not as a regex negation event.

---

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

# 5. Disease-by-Disease Matrix

## 5.1 COVID-19

### E1 — Disease-defining / confirmatory

- Positive SARS-CoV-2 NAAT/RT-PCR from an appropriate respiratory specimen.
- A validated positive viral diagnostic test identifying current SARS-CoV-2 infection.

WHO's current clinical management guidance recommends respiratory-specimen NAAT as the minimum molecular diagnostic approach for suspected cases; CDC describes NAAT as highly sensitive and highly specific for detecting viral RNA. citeturn877452search164turn550161search9

### E2 — Strong evidence

- Positive antigen test in a patient being evaluated for current infection.
- Repeated/confirmatory testing when initial antigen evidence is uncertain.

CDC states that positive antigen results indicate current infection, while negative antigen results are less sensitive and may require repeat testing or NAAT confirmation. citeturn550161search9

### E3 — Supportive

- Fever, cough, dyspnea.
- Ground-glass pulmonary imaging.
- Epidemiological exposure.
- Lymphopenia or other non-specific laboratory changes.

### E0 — Context only

- COVID-19 vaccination.
- Hospital infection-control precautions.
- “COVID-19 pandemic” as a temporal background.
- Staff-exposure minimization.
- COVID-19 listed only in differential diagnosis.

### Major confusable entities

```text
COVID-19 infection
↔ vaccination
↔ exposure-control context
↔ post-COVID history
↔ differential diagnosis
```

### Contradiction notes

A negative antigen result does **not** universally exclude COVID-19. A negative NAAT is materially stronger, but interpretation still depends on specimen, timing and clinical context. citeturn550161search9

### Curation rule

```text
vaccination ≠ infection
exposure-control ≠ infection
pandemic background ≠ infection
```

---

## 5.2 Tuberculosis

### E1 — Disease-defining / confirmatory

- Identification of *Mycobacterium tuberculosis* complex by an accepted molecular test on an appropriate clinical specimen.
- Culture isolation of *M. tuberculosis* complex.
- Other accepted bacteriological confirmation explicitly identifying TB according to the applicable diagnostic algorithm.

WHO's 2025 consolidated diagnostic guidance recommends molecular WHO-recommended rapid diagnostics for initial TB diagnosis in relevant populations and explicitly distinguishes diagnostic technologies by specimen and clinical setting. WHO also defines bacteriologically confirmed TB using positive smear microscopy, culture or a WHO-recommended diagnostic test; however, for this dataset's **pathogen-discriminative evidence matrix**, smear alone is insufficiently specific when nontuberculous mycobacteria remain plausible. citeturn877452search1turn877452search12

### E2 — Strong evidence

- Histopathology compatible with TB when integrated with microbiology and clinical findings.
- Positive molecular evidence that is strong but limited by specimen or assay context.
- Culture showing a mycobacterial organism with additional evidence establishing *M. tuberculosis*.

### E3 — Supportive / non-discriminative

- AFB smear positive without organism identification.
- Granulomatous inflammation.
- Cavitary lesions / compatible imaging.
- Chronic cough, fever, weight loss.
- TB exposure history.

### E0 — Context only

- “History of TB” in a relative.
- TB mentioned as differential diagnosis.
- TB contact investigation without evidence that the patient has TB disease.
- TB vaccination / BCG discussion.

### Major confusable entities

| Apparent evidence | Possible alternative | Interpretation |
|---|---|---|
| AFB-positive smear | *M. avium* complex | Does not identify *M. tuberculosis* |
| AFB-positive smear | *M. leprae* | Does not establish TB |
| “BCG infection” | *M. bovis* BCG | Not equivalent to human TB disease caused by *M. tuberculosis* |
| “tuberculosis” in text | historical/contact/differential | Requires assertion and role analysis |

### Contradiction notes

A negative TB molecular test can be materially contradictory without universally excluding TB, particularly when disease site, specimen quality, or organism burden limits sensitivity. WHO's current guidance explicitly uses specimen- and population-specific algorithms and discusses discordant/negative testing. citeturn877452search5turn877452search12

### Curation rule

```text
AFB positive
   ≠
TB confirmed

M. tuberculosis identified
   → strong disease-specific evidence
```

---

## 5.3 HIV / HIV Infection / AIDS

### E1 — Disease-defining / confirmatory

- A complete laboratory HIV diagnostic algorithm leading to a confirmed HIV infection diagnosis.
- Reactive HIV-1/2 antigen-antibody screening followed by appropriate supplemental differentiation testing and NAT resolution when required.

CDC's current laboratory guidance continues to distinguish the screening, differentiation and NAT stages; a single reactive screening assay should not be treated as the final diagnosis. citeturn235361search2turn235361search3

### E2 — Strong evidence

- HIV-1 RNA/NAT demonstrating infection in an appropriate diagnostic context, including suspected acute infection.
- Concordant confirmatory laboratory results.

### E3 — Supportive

- Opportunistic infection.
- Low CD4 count.
- Weight loss / constitutional symptoms.
- Exposure history.

These may support clinical suspicion but are not equivalent to laboratory confirmation of HIV infection.

### E0 — Context only

- HIV testing performed with a negative result.
- “HIV exposure.”
- Partner/family HIV history.
- AIDS-related disease discussion without patient-level HIV evidence.
- “AIDS” used in a non-HIV phrase such as `walking aids`.

### Major lexical confusable

```text
walking aids
       ≠
AIDS / HIV infection
```

The mention must be normalized semantically before it can become a disease concept.

### Contradiction notes

A negative test result can be decisive within an appropriate completed algorithm, but timing and testing strategy matter for early infection. A raw phrase such as `nonreactive` must therefore be attached to the specific test and patient anchor.

### Curation rule

```text
single reactive screening test
   ≠
final HIV diagnosis

completed diagnostic algorithm
   → diagnostic claim
```

---

## 5.4 Malaria

### E1 — Disease-defining / confirmatory

- Detection of malaria parasites on appropriately performed blood microscopy.
- Positive quality-assured malaria RDT detecting a validated malaria antigen in the correct clinical context.
- Validated molecular detection of malaria parasite DNA/RNA where used as a diagnostic method.

WHO recommends prompt parasite-based diagnosis by microscopy or RDT for suspected malaria; microscopy can detect malaria-causing *Plasmodium* species and requires examination of thick and thin films. citeturn382910search0turn382910search2turn382910search9

### E2 — Strong evidence

- Species-level *Plasmodium* identification by microscopy.
- Molecular confirmation and speciation.
- RDT plus compatible clinical and epidemiological context when microscopy is unavailable.

### E3 — Supportive

- Fever.
- Thrombocytopenia.
- Hemolysis.
- Splenomegaly.
- Travel/residence in endemic region.

### E0 — Context / confounder

- “Malaria” in differential diagnosis.
- Malaria discussed in background literature.
- Treatment with antimalarials without diagnostic evidence.

### Major confusable entities

```text
Plasmodium ovale
      ↔
patent foramen ovale (lexical confounder)

Plasmodium-positive evidence
      ↔
other hemoparasites / non-malarial fever

human malaria
      ↔
Cytauxzoon felis in veterinary text
```

### Contradiction notes

A single negative smear/RDT does not necessarily exclude malaria because parasite density, timing, prior treatment and test characteristics matter. WHO emphasizes parasite-based testing and repeated/appropriate testing strategies rather than a lexical negative rule. citeturn382910search10turn382910search11

### Curation rule

```text
“fever + thrombocytopenia”
   ≠
malaria diagnosis

Plasmodium-specific evidence
   → disease claim
```

---

## 5.5 Dengue

### E1 — Disease-defining / confirmatory

- Positive dengue NAAT/RT-PCR during the acute phase.
- Positive dengue NS1 antigen test in the appropriate diagnostic setting.

CDC explicitly classifies positive NAAT or NS1 antigen results as confirmed acute dengue infection. citeturn550161search0turn550161search1turn550161search5

### E2 — Strong evidence

- Dengue IgM supporting recent infection, especially after the first week.
- Paired-serum seroconversion or other disease-specific confirmatory serologic strategy.
- PRNT when required to discriminate dengue from related flaviviruses.

### E3 — Supportive

- Fever.
- Rash.
- Thrombocytopenia.
- Hemoconcentration.
- Plasma leakage.

### Major confusable diseases

```text
Dengue ↔ Zika
Dengue ↔ chikungunya
Dengue ↔ malaria
Dengue ↔ leptospirosis
```

WHO explicitly notes that dengue cannot be clinically differentiated from several other vector-borne infections during the febrile phase. citeturn382910search4

### Contradiction notes

Negative NAAT or NS1 does not rule out dengue. CDC recommends time-appropriate serology or convalescent testing when initial testing is negative or unavailable. citeturn550161search0turn550161search5

---

## 5.6 Brucellosis

### E1 — Disease-defining / confirmatory

- Isolation/culture of *Brucella* spp. from an appropriate clinical specimen.
- Validated pathogen-specific molecular confirmation when clinically and laboratorily appropriate.

CDC's reference guide identifies culture as the gold-standard test and notes that PCR can provide rapid detection. citeturn235361search48

### E2 — Strong evidence

- Disease-specific serology interpreted according to the appropriate testing strategy.
- Paired sera demonstrating the expected change in antibody response.

CDC notes that some serologic diagnoses require two sera and that single-sample interpretation may only support a probable diagnosis. citeturn235361search1

### E3 — Supportive

- Undulating fever.
- Arthralgia.
- Hepatosplenomegaly.
- Exposure to unpasteurized dairy or infected animals.

### Major confusable diseases

```text
Brucellosis ↔ tuberculosis
Brucellosis ↔ typhoid fever
Brucellosis ↔ Q fever / other zoonoses
```

### Important species-specific trap

Standard serology may fail to detect *B. canis* or Brucella RB51; culture may be required. citeturn235361search1

### Contradiction notes

Negative serology alone should not be encoded as universal exclusion, especially in early or complicated disease.

---

## 5.7 Leishmaniasis

### E1 — Disease-defining / confirmatory

- Direct parasitological identification of *Leishmania* in an appropriate lesion/tissue specimen.
- Validated PCR demonstrating *Leishmania* where appropriate.

WHO states that parasite identification remains the gold standard; diagnostic strategy differs by visceral, cutaneous and mucocutaneous disease. citeturn382910search1turn382910search16

### E2 — Strong evidence

- Visceral leishmaniasis serology / rK39 in an appropriate endemic setting.
- Supportive parasitology + compatible clinical syndrome.

### E3 — Supportive

- Fever.
- Splenomegaly.
- Pancytopenia.
- Chronic skin ulceration.

### Major confusable diseases

Cutaneous lesions can resemble tuberculosis, fungal infection, leprosy, psoriasis and other ulcers. WHO explicitly notes the low specificity of lesion appearance. citeturn382910search1

### Contradiction notes

Serology is less useful in some cutaneous/mucocutaneous presentations; a negative serology result should not be treated as a universal exclusion.

---

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

## 5.9 Typhoid Fever / Paratyphoid Fever

### E1 — Disease-defining / confirmatory

- Isolation of *Salmonella Typhi* or *Salmonella Paratyphi* from an appropriate clinical specimen, especially blood culture.
- Bone-marrow culture is highly sensitive and may remain positive despite prior antibiotics.

CDC describes blood culture as the mainstay of diagnosis and notes that bone-marrow culture can retain substantial sensitivity. citeturn550161search10

### E2 — Strong evidence

- Validated molecular detection of *S. Typhi/Paratyphi* used in an appropriate diagnostic setting.
- Concordant microbiological evidence from repeated specimens.

### E3 — Supportive

- Prolonged fever.
- Abdominal symptoms.
- Relative bradycardia where documented.
- Leukopenia.
- Travel/exposure history.

### E0 / weak evidence

- Widal test.
- “Typhoid treated empirically”.

CDC specifically does not recommend Widal because of false-positive rates. citeturn550161search10

### Major confusable diseases

```text
Typhoid ↔ malaria
Typhoid ↔ dengue
Typhoid ↔ brucellosis
Typhoid ↔ other invasive Salmonella infections
```

### Contradiction notes

A negative blood culture does not universally exclude typhoid because sensitivity is affected by prior antibiotics and number/volume of cultures.

---

## 5.10 Ebola Virus Disease

### E1 — Disease-defining / confirmatory

- RT-PCR identifying an orthoebolavirus infection in an appropriate clinical specimen.
- Antigen-capture detection or virus isolation within a validated diagnostic framework.

WHO states that laboratory confirmation is critical because Ebola can be difficult to distinguish clinically from other infectious diseases; accepted methods include RT-PCR, antigen-capture ELISA, antibody-capture ELISA and culture. citeturn382910search5turn382910search12

### E2 — Strong evidence

- Validated antigen detection.
- Appropriate serologic evidence in the relevant phase.
- Concordant repeated laboratory evidence.

### E3 — Supportive

- Febrile hemorrhagic/viral syndrome.
- Exposure during a recognized outbreak.
- Compatible travel or contact history.

### Major confusable diseases

```text
Ebola ↔ Marburg disease
Ebola ↔ malaria
Ebola ↔ other viral hemorrhagic fevers
Ebola ↔ severe bacterial sepsis
```

### Contradiction notes

A negative early molecular result may need to be interpreted with timing and repeat-testing procedures; a universal “negative RT-PCR = impossible” rule is not justified.

---

## 5.11 Zika Virus Disease

### E1 — Disease-defining / confirmatory

- Detection of Zika viral RNA by NAAT in an appropriate specimen and diagnostic window.

CDC describes NAAT as the preferred method because it can provide confirmed evidence of infection. citeturn550161search3

### E2 — Strong evidence

- Zika-specific serology in the appropriate setting.
- IgM followed by confirmatory neutralization testing when required to address flavivirus cross-reactivity.

WHO states that IgM testing requires differentiation from related flaviviruses such as dengue. citeturn382910search13

### E3 — Supportive

- Rash.
- Fever.
- Conjunctivitis.
- Arthralgia.
- Compatible pregnancy/travel exposure.

### Major confusable diseases

```text
Zika ↔ dengue
Zika ↔ chikungunya
Zika ↔ other flavivirus infection
```

### Contradiction notes

Negative NAAT may be non-definitive if the specimen or timing is inappropriate. IgM alone may remain ambiguous because of flavivirus cross-reactivity.

---

## 5.12 Cholera

### E1 — Disease-defining / confirmatory

- Laboratory confirmation of *Vibrio cholerae* by culture.
- PCR confirmation where an appropriate validated assay is used.
- Serologic confirmation/serogrouping of the isolate where applicable.

WHO states that RDTs are useful for early detection of probable cholera outbreaks, but confirmation requires laboratory testing by culture, seroagglutination or PCR. citeturn382910search15

### E2 — Strong evidence

- Positive RDT in a compatible outbreak/epidemiological setting.
- Concordant stool microbiology.

### E3 — Supportive

- Acute profuse watery diarrhea.
- Rapid dehydration.
- Epidemiological outbreak context.

### Major confusable diseases

```text
Cholera ↔ other acute watery diarrhea
Cholera ↔ enterotoxigenic E. coli
Cholera ↔ viral gastroenteritis
```

### Contradiction notes

Negative RDT does not rule out disease; performance and outbreak context matter.

---

## 5.13 Rabies

### E1 — Disease-defining / confirmatory

**Post-mortem:**

- Detection of rabies virus antigen in appropriate brain tissue by fluorescent antibody testing or equivalent validated methods.

WHO considers brain-tissue antigen detection by FAT the post-mortem gold standard. citeturn235361search0turn877452search7

**Ante-mortem:**

- Concordant laboratory evidence from the appropriate combination of saliva, nuchal skin biopsy, CSF/serum and other validated tests.

CDC states that no single antemortem test is sufficient in humans. citeturn550161search2

### E2 — Strong evidence

- RT-PCR on appropriate serial specimens.
- Positive antigen/serologic evidence integrated with the clinical syndrome.

### E3 — Supportive

- Acute progressive encephalitis.
- Hydrophobia/aerophobia.
- Compatible animal exposure.

### Major confusable diseases

```text
Rabies ↔ other viral encephalitides
Rabies ↔ autoimmune encephalitis
Rabies ↔ severe toxic/metabolic encephalopathy
```

### Contradiction notes

A negative single antemortem RT-PCR or saliva specimen does not necessarily exclude rabies because viral shedding can be intermittent. WHO explicitly cautions that negative RT-PCR results do not always rule out infection. citeturn235361search46

---

## 5.14 Chikungunya

### E1 — Disease-defining / confirmatory

- RT-PCR or other molecular detection during the acute phase.
- Validated virus detection/culture where available.

WHO and CDC both describe molecular testing as the principal early diagnostic approach. citeturn382910search7turn550161search6

### E2 — Strong evidence

- Chikungunya-specific serology after the first week.
- Positive IgM followed by confirmatory neutralizing antibody testing when indicated.

CDC notes that positive IgM can be false-positive and should be confirmed in appropriate cases. citeturn550161search6

### E3 — Supportive

- Abrupt fever.
- Severe polyarthralgia.
- Rash.
- Compatible travel/vector exposure.

### Major confusable diseases

```text
Chikungunya ↔ dengue
Chikungunya ↔ Zika
```

WHO explicitly notes clinical overlap with dengue and Zika. citeturn382910search7

### Contradiction notes

Acute-phase negative molecular testing does not universally exclude infection when timing/sample limitations apply; convalescent serology may be required.

---

## 5.15 Yellow Fever

### E1 — Disease-defining / confirmatory

- RT-PCR / molecular detection in the early phase when viral RNA is detectable.
- Appropriately interpreted serologic confirmation in later disease.

WHO describes early RT-PCR and later antibody testing; CDC emphasizes the importance of distinguishing wild-type infection from vaccine-induced antibodies and using more specific neutralization testing when needed. citeturn382910search8turn550161search8

### E2 — Strong evidence

- Yellow fever IgM with appropriate epidemiological context and confirmatory neutralization testing when flavivirus cross-reactivity is possible.
- Compatible laboratory and clinical findings interpreted together.

### E3 — Supportive

- Fever.
- Jaundice.
- Hemorrhagic features.
- Exposure to endemic area/vector.

### Major confusable diseases

```text
Yellow fever ↔ dengue
Yellow fever ↔ malaria
Yellow fever ↔ leptospirosis
Yellow fever ↔ viral hepatitis
Yellow fever ↔ other flavivirus infections
```

WHO notes that severe yellow fever can resemble malaria, leptospirosis, viral hepatitis and dengue. citeturn382910search8

### Critical vaccination confounder

Yellow-fever vaccine can produce antibodies that are not distinguishable by some routine serologic assays from antibodies generated by wild-type infection. Vaccination history must therefore be part of evidence interpretation. citeturn550161search8

---

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

# 15. Research Questions Left Open

This artifact deliberately does **not** answer several empirical questions yet.

## 15.1 How many E2 pieces are enough?

This should be measured rather than assumed.

For example:

```text
E2 + E3
vs
E2 + E2
vs
E1 alone
```

may have different predictive value by disease.

## 15.2 How should conflicting E1 evidence be resolved?

Examples:

```text
PCR positive + culture negative
PCR negative + culture positive
serology positive + NAAT negative
```

These require disease-specific and time-aware reconciliation rather than a universal priority score.

## 15.3 Should clinical diagnosis without laboratory confirmation be accepted?

The answer may differ by disease and by the intended use of the dataset. This must be decided explicitly before Gold Standard annotation.

## 15.4 What specimen-specific rules are required?

Future work must formalize the relationship:

```text
disease × test × specimen × timing × subject class
```

rather than storing “PCR” as a generic evidence type.

---

# 16. Primary Reference Sources

The matrix was grounded primarily in current official diagnostic guidance and reference material available as of 2026-10-02.

| Disease | Primary source |
|---|---|
| COVID-19 | [WHO Clinical management of COVID-19: living guideline, June 2025](https://www.who.int/publications/i/item/B09467) ; [CDC Overview of Testing for SARS-CoV-2](https://www.cdc.gov/covid/hcp/clinical-care/overview-testing-sars-cov-2.html) |
| Tuberculosis | [WHO consolidated guidelines on tuberculosis: module 3, diagnosis, 2025](https://www.who.int/publications/i/item/9789240107984) |
| HIV | [CDC HIV Laboratory Testing guidance](https://www.cdc.gov/hivpartners/php/guidelines/) |
| Malaria | [WHO Global Malaria Programme — Diagnostic testing](https://www.who.int/activities/diagnostic-testing-for-malaria) |
| Dengue | [CDC Clinical Testing Guidance for Dengue](https://www.cdc.gov/dengue/hcp/diagnosis-testing/) |
| Brucellosis | [CDC Clinical Overview of Brucellosis](https://www.cdc.gov/brucellosis/hcp/clinical-overview/index.html) ; [CDC Brucellosis Reference Guide](https://www.cdc.gov/brucellosis/pdf/brucellosi-reference-guide.pdf) |
| Leishmaniasis | [WHO Leishmaniasis Q&A](https://www.who.int/news-room/questions-and-answers/item/leishmaniasis) |
| Leptospirosis | [CDC Clinical Overview of Leptospirosis](https://www.cdc.gov/leptospirosis/hcp/clinical-overview/index.html) ; [WHO Human Leptospirosis](https://iris.who.int/bitstream/handle/10665/42667/WHO_CDS_CSR_EPH_2002.23.pdf) |
| Typhoid fever | [CDC Clinical Guidance for Typhoid and Paratyphoid Fever](https://www.cdc.gov/typhoid-fever/hcp/clinical-guidance/index.html) |
| Ebola | [WHO Diagnostic testing for Ebola disease and Marburg virus disease, interim guidance, July 2026](https://www.who.int/publications/i/item/B09834) ; [WHO Ebola disease fact sheet](https://www.who.int/news-room/fact-sheets/detail/ebola-disease) |
| Zika | [CDC Clinical Testing and Diagnosis for Zika Virus Disease](https://www.cdc.gov/zika/hcp/diagnosis-testing/) ; [WHO Zika virus fact sheet](https://www.who.int/en/news-room/fact-sheets/detail/zika-virus) |
| Cholera | [WHO Cholera fact sheet](https://www.who.int/en/news-room/fact-sheets/detail/cholera) |
| Rabies | [WHO Rabies diagnosis](https://www.who.int/teams/control-of-neglected-tropical-diseases/rabies/diagnosis) ; [CDC Laboratory Methods for Rabies Testing](https://www.cdc.gov/rabies/php/labs-specimens/testing.html) |
| Chikungunya | [WHO Chikungunya Q&A](https://www.who.int/news-room/questions-and-answers/item/chikungunya) ; [CDC Clinical Testing and Diagnosis for Chikungunya](https://www.cdc.gov/chikungunya/hcp/diagnosis-testing/index.html) |
| Yellow fever | [WHO Yellow fever fact sheet](https://www.who.int/news-room/fact-sheets/detail/yellow-fever) ; [CDC Clinical Features and Diagnosis of Yellow Fever](https://www.cdc.gov/yellow-fever/hcp/clinical-diagnosis/index.html) |

---

# 17. Status and Next Research Dependency

This artifact defines the **disease-specific semantics of evidence**, but it intentionally does not introduce a numerical scoring function.

The next dependency is therefore:

```text
03 Evidence Specificity Matrix
          ↓
04 Gold-Standard Annotation Protocol
          ↓
05 Inter-Annotator Agreement Study
          ↓
06 Baseline Evaluation of Frozen Pipeline
```

The central research hypothesis to test is:

> **Patient-anchored, disease-discriminative evidence representation will reduce false-positive disease labeling more robustly than adding lexical patterns to the existing retrieval pipeline.**

That hypothesis is now falsifiable.

---

## Final Research Invariant

```text
A disease-related observation becomes a valid dataset label
ONLY after it has survived:

1. subject anchoring,
2. concept normalization,
3. assertion/temporality/experiencer analysis,
4. clinical-role analysis,
5. disease-specific evidence discrimination,
6. contradiction-aware reconciliation.
```

Therefore:

```text
MENTION ≠ EVIDENCE
EVIDENCE ≠ CLAIM
CLAIM ≠ LABEL
```

The purpose of the matrix is to make those three boundaries explicit and auditable.

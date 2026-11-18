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

## 5.17 Histoplasmosis

### E1 — Disease-defining / confirmatory

- Isolation of *Histoplasma capsulatum* in fungal culture from blood, bone marrow, BAL, sputum, or tissue biopsy.
- Microscopic visualization of characteristic intracellular narrow-based budding oval yeasts (2–4 μm) within macrophages on Wright-Giemsa stain, or on Gomori methenamine silver (GMS) / PAS tissue histology.
- Validated *Histoplasma*-specific molecular confirmation (PCR) from clinical tissue.

IDSA Practice Guidelines for Histoplasmosis (2015/2023) and CDC Fungal Diseases program highlight direct culture and histopathology as gold-standard evidence, with antigen detection serving as a rapid primary tool in disseminated forms.

### E2 — Strong evidence

- High-titer *Histoplasma* antigen enzyme immunoassay (EIA) in urine or serum (> 0.5 ng/mL or above laboratory reference cutoff).
- Immunodiffusion demonstrating both H and M precipitin bands (H band reflects active infection; M band alone may represent acute or past exposure).
- Complement fixation (CF) antibody titer >= 1:32 or fourfold rise in paired sera.

### E3 — Supportive

- Apical cavitary pulmonary infiltrates, fibrosing mediastinitis, diffuse reticulonodular infiltrates.
- Hepatosplenomegaly, mucosal/oral ulcerative lesions, or bilateral adrenal enlargement in disseminated disease.
- Exposure: exposure to bat guano, cave exploration (spelunking), or bird roosts in endemic river valleys (Ohio/Mississippi) or Latin America.

### Major confusable diseases

```text
Histoplasmosis ↔ Tuberculosis
Histoplasmosis ↔ Aspergillosis / Cryptococcosis
Histoplasmosis ↔ Visceral leishmaniasis
```

### Important diagnostic trap

Histoplasma antigen assays cross-react with other endemic fungal infections (e.g., *Blastomyces*, *Coccidioides*, *Paracoccidioides*). Negative culture does not rule out acute or chronic pulmonary histoplasmosis due to prolonged incubation requirements.

---

## 5.18 Cryptococcosis

### E1 — Disease-defining / confirmatory

- Isolation/culture of *Cryptococcus neoformans* or *Cryptococcus gattii* from CSF, blood, BAL, or sterile tissue biopsy (demonstrating melanin synthesis on birdseed agar).
- Microscopic visualization of encapsulated, narrow-based budding yeast cells with clear halo on India ink examination of CSF.
- Histopathologic demonstration of encapsulated yeasts stained with Mucicarmine or Fontana-Masson stain.

WHO Guidelines on Cryptococcal Infection (2022) and CDC Cryptococcosis guidance identify culture and cryptococcal antigen lateral flow assay (LFA) as standard diagnostic modalities, prioritizing rapid LFA in resource-constrained settings.

### E2 — Strong evidence

- Cryptococcal capsular antigen (CrAg) detected in CSF or serum via lateral flow assay (LFA) or latex agglutination/EIA with significant titer.

### E3 — Supportive

- Subacute or chronic headache, fever, neck stiffness, cranial nerve palsies, significantly elevated CSF opening pressure (> 200 mm H2O).
- Brain MRI/CT showing cryptococcomas, dilated perivascular Virchow-Robin spaces ("soap-bubble" appearance), or basal meningeal enhancement.
- Profound immunosuppression (HIV with CD4 < 100 cells/μL, organ transplantation, prolonged corticosteroid therapy) or *C. gattii* exposure in immunocompetent hosts.

### Major confusable diseases

```text
Cryptococcosis ↔ Tuberculous meningitis
Cryptococcosis ↔ Neurocysticercosis
Cryptococcosis ↔ Bacterial / viral meningoencephalitis
```

### Important diagnostic trap

India ink has only 50–80% sensitivity compared to CrAg LFA (> 98% sensitivity). Isolated serum CrAg positivity in HIV patients reflects cryptococcal antigenemia; lumbar puncture is required to evaluate for central nervous system involvement.

---

## 5.19 Neurocysticercosis

### E1 — Disease-defining / confirmatory

- Definitive neuroimaging demonstration of cystic lesions with an identifiable invaginated scolex ("hole-with-dot" sign) on high-resolution brain MRI or CT.
- Histopathological confirmation of the larval cestode (*Taenia solium* cysticercus) from brain or spinal biopsy.

WHO Guidelines on Taenia solium Neurocysticercosis (2021) and the Del Brutto Revised Diagnostic Criteria designate visualization of a cystic lesion with scolex as absolute confirmatory evidence.

### E2 — Strong evidence

- Positive enzyme-linked immunoelectrotransfer blot (EITB / Western blot) for *Taenia solium* specific antibodies using lentil-lectin purified glycoprotein antigens.
- Neuroimaging showing highly suggestive cystic lesions without visible scolex: ring-enhancing or nodular lesions (colloidal or granular stage) or punctate parenchymal calcifications with concordant serology.

### E3 — Supportive

- New-onset unprovoked seizures, epilepsy, focal neurological signs, progressive hydrocephalus.
- Epidemiological travel or residence in *T. solium* endemic regions (Latin America, Sub-Saharan Africa, South/Southeast Asia), household contact with tapeworm carrier.
- Documented clinical and radiological response following antiparasitic treatment (albendazole or praziquantel).

### Major confusable diseases

```text
Neurocysticercosis ↔ Tuberculoma / CNS Tuberculosis
Neurocysticercosis ↔ Cerebral cryptococcoma / pyogenic brain abscess
Neurocysticercosis ↔ Brain tumor / primary CNS neoplasm
```

### Important diagnostic trap

Standard ELISA serology exhibits cross-reactivity with echinococcosis and other cestodes; EITB Western blot is the reference standard. Completely calcified nodular lesions represent inactive, non-viable remnants.

---

## 5.20 Amoebiasis

### E1 — Disease-defining / confirmatory

- Detection of *Entamoeba histolytica* DNA by real-time PCR in stool, liver abscess pus aspirate, or colonic biopsy.
- Stool or pus antigen detection specific for *E. histolytica* (e.g., Gal/GalNAc lectin ELISA) distinguishing *E. histolytica* from morphologically identical non-pathogenic commensals (*E. dispar*, *E. moshkovskii*).
- Microscopic demonstration of *E. histolytica* trophozoites with ingested erythrocytes (erythrophagocytosis) in stool or tissue specimen.

CDC DPDx and WHO Amebiasis Technical Report emphasize that microscopic identification without erythrophagocytosis cannot differentiate *E. histolytica* from non-pathogenic amoebae, establishing PCR and specific antigen ELISA as definitive tests.

### E2 — Strong evidence

- High-titer amebic serology (IHA >= 1:256 or positive EIA) in a patient presenting with an ultrasound/CT-confirmed hepatic abscess cavity yielding characteristic reddish-brown "anchovy-paste" fluid.
- Colonoscopy demonstrating typical "flask-shaped" mucosal ulcerations with trophozoites on histopathological biopsy.

### E3 — Supportive

- Right upper quadrant pain, tender hepatomegaly, fever; or amebic dysentery with bloody/mucoid diarrhea and tenesmus.
- Hepatic ultrasound/CT showing solitary or dominant liver abscess, predominantly localized in the right lobe.
- Prompt clinical and radiological resolution following metronidazole or tinidazole therapy.

### Major confusable diseases

```text
Amoebiasis ↔ Pyogenic bacterial liver abscess
Amoebiasis ↔ Echinococcosis (hydatid liver cyst)
Amoebiasis ↔ Bacillary dysentery / Inflammatory bowel disease
```

### Important diagnostic trap

Microscopy finding amoebic cysts or non-erythrophagocytic trophozoites must NOT be coded as confirmed *E. histolytica* without molecular or antigen discrimination from *E. dispar*.

---

## 5.21 Echinococcosis

### E1 — Disease-defining / confirmatory

- Microscopic identification of *Echinococcus* protoscolices, free hooklets ("hydatid sand"), or characteristic laminated cyst wall membrane in aspirated hydatid fluid or surgical specimen.
- Pathogen-specific *Echinococcus* PCR from cyst tissue or fluid aspirate.
- Histopathologic demonstration of acellular laminated membrane and nucleated germinal layer.

WHO Informal Working Group on Echinococcosis (WHO-IWGE) and CDC DPDx classify microscopic/histologic finding of protoscolices or laminated cuticular layers as definitive confirmation.

### E2 — Strong evidence

- Ultrasound/CT findings conforming to pathognomonic WHO-IWGE classification criteria:
  - CE1: unilocular simple cyst with double-line sign.
  - CE2: multivesicular / multiseptated cyst with honeycomb appearance or daughter cysts.
  - CE3a/b: detached endocyst membrane floating inside ("water-lily sign") or daughter cysts within solid matrix.
- Specific *Echinococcus* IgG ELISA or Western blot showing characteristic diagnostic bands (e.g., 8 kDa, 18 kDa) with compatible cystic mass.

### E3 — Supportive

- Slow-growing asymptomatic or space-occupying hepatic mass, pulmonary hydatid cyst.
- Complete egg-shell ring calcification of the cyst wall (CE5 - inactive cyst).
- Hypersensitivity reaction or anaphylaxis secondary to cyst fluid leakage.
- Epidemiological exposure in pastoral livestock-raising areas (dogs, sheep, cattle).

### Major confusable diseases

```text
Echinococcosis ↔ Amebic liver abscess
Echinococcosis ↔ Simple hepatic or pulmonary cysts / biliary cystadenoma
Echinococcosis ↔ Cavitary tuberculosis / Pulmonary aspergilloma
```

### Important diagnostic trap

Diagnostic aspiration of suspected hydatid cysts is generally contraindicated due to risk of lethal anaphylaxis and secondary peritoneal seeding; percutaneous procedures must follow WHO PAIR guidelines with anthelmintic coverage.

---

## 5.22 Schistosomiasis

### E1 — Disease-defining / confirmatory

- Microscopic identification of viable *Schistosoma* eggs with characteristic spine morphology:
  - *S. mansoni*: prominent lateral spine in stool (Kato-Katz) or rectal biopsy.
  - *S. haematobium*: terminal spine in urine filtration or bladder biopsy.
  - *S. japonicum*: small rudimentary lateral knob/spine in stool.
- Validated species-specific *Schistosoma* real-time PCR in clinical urine, stool, or serum specimens.
- Histopathological identification of viable schistosome ova in tissue biopsy.

WHO Guideline on Control and Elimination of Human Schistosomiasis (2022) and CDC DPDx establish egg detection by microscopy or molecular PCR as gold-standard proof of active schistosomal infection.

### E2 — Strong evidence

- Detection of circulating schistosome antigens: Point-of-care Circulating Cathodic Antigen (POC-CCA) in urine or Circulating Anodic Antigen (CAA) in serum/urine at diagnostic thresholds.
- Demonstrable seroconversion or high-titer species-specific antibody in non-endemic travelers following fresh-water exposure.

### E3 — Supportive

- Painless terminal hematuria, dysuria, bladder calcification on imaging (*S. haematobium*).
- Hepatosplenomegaly, Symmers' pipestem periportal fibrosis on liver ultrasound, portal hypertension, esophageal varices (*S. mansoni*, *S. japonicum*).
- Katayama fever (acute schistosomiasis): fever, urticaria, dry cough, splenomegaly, marked eosinophilia 2–8 weeks after freshwater contact.
- History of bathing, swimming, or wading in freshwater bodies in endemic African, South American, or Asian habitats.

### Major confusable diseases

```text
Schistosomiasis ↔ Visceral leishmaniasis / Malaria
Schistosomiasis ↔ Urinary tract infection / Bladder carcinoma
Schistosomiasis ↔ Viral or alcoholic liver cirrhosis
```

### Important diagnostic trap

Calcified, non-viable ova seen in old tissue scars in individuals from endemic countries reflect past resolved infection rather than active ovipositing worms.

---

## 5.23 Leprosy

### E1 — Disease-defining / confirmatory

- Demonstration of acid-fast bacilli in clumps or globi on slit-skin smear (SSS) from earlobes, elbows, or active lesion margins (Bacteriological Index > 0).
- Histopathologic examination of skin or peripheral nerve biopsy showing acid-fast bacilli on Fite-Faraco modified stain with characteristic neurovascular granulomatous infiltration.
- Validated *Mycobacterium leprae* / *Mycobacterium lepromatosis* PCR from skin or nerve biopsy.

WHO Guidelines for the Diagnosis, Treatment and Prevention of Leprosy (2018) and CDC Hansen's Disease Clinical Overview recognize slit-skin smear, nerve biopsy with Fite stain, and molecular PCR as definitive confirmation.

### E2 — Strong evidence

- Presence of at least two of the WHO Cardinal Triad signs of leprosy:
  1. Hypopigmented or erythematous skin lesion with definite impairment of sensation (touch, pain, temperature).
  2. Thickened or enlarged peripheral nerve (ulnar, common peroneal, greater auricular) with sensory impairment or motor weakness in corresponding distribution.
  3. Positive slit-skin smear.
- Documented lepromatous reaction: Type 1 reversal reaction or Type 2 Erythema Nodosum Leprosum (ENL) in a patient with neuro-dermal signs.

### E3 — Supportive

- Claw-hand deformity, foot drop, lagophthalmos, trophic neuropathic ulcers, leonine facies, loss of eyebrows/eyelashes (madarosis).
- Elevated anti-PGL-I IgM antibodies (supportive of multibacillary infection).
- Prolonged household or close contact with untreated leprosy patients.

### Major confusable diseases

```text
Leprosy ↔ Cutaneous tuberculosis / NTM infection
Leprosy ↔ Diabetic peripheral neuropathy / Charcot-Marie-Tooth
Leprosy ↔ Cutaneous leishmaniasis / Sarcoidosis / Vitiligo
```

### Important diagnostic trap

Standard Ziehl-Neelsen staining easily decolorizes *M. leprae*; Fite-Faraco stain is essential. Slit-skin smear is characteristically negative in paucibacillary (PB) tuberculoid leprosy; clinical sensory testing is primary.

---

## 5.24 Lymphatic Filariasis

### E1 — Disease-defining / confirmatory

- Microscopic detection of microfilariae in nocturnal thick blood smears, Knott concentration, or membrane filtration collected during peak periodicity (22:00–02:00) with diagnostic morphology (*Wuchereria bancrofti*, *Brugia malayi*).
- Real-time visualization of motile adult worms inside dilated lymphatic vessels on scrotal or breast ultrasound ("filarial dance sign").
- Pathogen-specific molecular confirmation by real-time PCR in clinical blood specimens.

WHO Global Programme to Eliminate Lymphatic Filariasis (GPELF) and CDC DPDx emphasize nocturnal blood examination or daytime filarial antigen testing as primary diagnostic standards.

### E2 — Strong evidence

- Circulating filarial antigen (CFA) positivity by Filarial Test Strip (FTS / Alere) or ICT card for *W. bancrofti*.
- Positive Brugia Rapid antibody test (detecting anti-Bm17/BmR1 antibodies) for *Brugia malayi* / *Brugia timori*.

### E3 — Supportive

- Progressive asymmetrical chronic lymphedema, elephantiasis of legs or genitalia, filarial hydrocele, chyluria.
- Recurrent acute adenolymphangitis (ADL) episodes with retrograde lymphatic tracking and fever.
- Tropical pulmonary eosinophilia (TPE): paroxysmal nocturnal wheezing, marked peripheral eosinophilia (> 3,000/μL), extremely high serum IgE.
- Residence or travel in filariasis-endemic tropical regions with vector mosquito exposure.

### Major confusable diseases

```text
Lymphatic Filariasis ↔ Podoconiosis (geochemical non-filarial elephantiasis)
Lymphatic Filariasis ↔ Recurrent bacterial cellulitis with secondary lymphedema
Lymphatic Filariasis ↔ Congestive heart failure / chronic venous stasis
```

### Important diagnostic trap

Daytime blood examination is usually false-negative for microfilariae in nocturnally periodic infections. In advanced chronic elephantiasis, circulating microfilariae and antigens are often cleared due to lymphatic obstruction and adult worm death.

---

## 5.25 Aspergillosis

### E1 — Disease-defining / confirmatory

- Histopathological demonstration of acute-angle (approximately 45 degree), dichotomously branching, regularly septate hyphae with documented tissue invasion / necrosis on GMS or PAS stain from lung tissue, surgical biopsy, or cavity aspirate.
- Fungal culture positive for *Aspergillus* species (*A. fumigatus*, *A. flavus*, *A. niger*, *A. terreus*) from sterile deep tissue or intraoperative surgical specimen.
- In an immunocompromised host: positive galactomannan antigen in BAL (optical density index >= 1.0) or serum (single index >= 0.7 or two consecutive >= 0.5) with compatible thoracic CT lesions.

IDSA Practice Guidelines for Aspergillosis (2016) and WHO Fungal Priority Pathogens List (2022) establish tissue histopathology, sterile culture, and validated galactomannan assay as gold-standard confirmatory criteria for invasive/chronic pulmonary aspergillosis.

### E2 — Strong evidence

- Thoracic CT demonstrating classic pathognomonic features:
  - Mobile intracavitary mass with surrounding air-crescent sign ("Monod sign") inside a preexisting lung cavity.
  - Dense nodular lesion with surrounding ground-glass attenuation ("halo sign") in neutropenic patients.
- High-titer serum *Aspergillus* precipitin or specific IgG antibodies in chronic pulmonary aspergillosis (CPA) / aspergilloma.
- Positive *Aspergillus* PCR from BAL fluid or sterile specimen with concordant radiological and clinical evidence.

### E3 — Supportive

- Hemoptysis (mild to massive life-threatening hemoptysis), chronic cough, pleuritic chest pain, fever unresponsive to antibacterial agents.
- Underlying cavitary lung defect: prior treated tuberculosis (TB cavity), sarcoidosis, bronchiectasis, COPD.
- Severe immunosuppression: prolonged neutropenia (< 500 cells/μL), hematopoietic stem cell transplant, high-dose corticosteroid therapy.

### Major confusable diseases

```text
Aspergillosis ↔ Tuberculosis
Aspergillosis ↔ Histoplasmosis / Endemic fungal infections
Aspergillosis ↔ Mucormycosis
Aspergillosis ↔ Cavitary lung malignancy / bacterial abscess
```

### Critical Cavitary Pulmonary Rule & TB Anchoring Trap

In patients with suspected or prior tuberculosis, identification of *Aspergillus* hyphae or a mobile intracavitary mass with positive precipitins indicates **Aspergilloma (Chronic Pulmonary Aspergillosis)** colonizing an existing tuberculous cavity, NOT active recurrence of tuberculosis.

### Contradiction notes

Isolation of *Aspergillus* in sputum without radiological lesions, tissue invasion, or elevated biomarkers represents environmental airway colonization (`E4_BACKGROUND_OR_CONTEXT_ONLY`) and must NOT be encoded as active invasive aspergillosis.

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

---

## 5.26 Cytomegalovirus (CMV)

### E1 — Disease-defining / confirmatory
- Histopathologic demonstration of characteristic cytomegaly with pathognomonic basophilic or amphophilic intranuclear inclusion bodies surrounded by a clear halo ("owl's eye" inclusion bodies) in tissue biopsy (e.g., gastrointestinal mucosa, lung transbronchial biopsy, liver, kidney), confirmed by CMV immunohistochemistry (IHC).
- Quantitative CMV DNA real-time PCR / nucleic acid amplification testing (NAT) from end-organ sterile tissue, cerebrospinal fluid (CSF in encephalitis/polyradiculopathy), vitreous/aqueous humor, or amniotic fluid.
- Quantitative plasma/whole-blood CMV DNA PCR exceeding institutionally verified significant viral load thresholds in an immunocompromised host presenting with compatible end-organ dysfunction.
- CMV pp65 antigenemia assay demonstrating significant antigenemia (>10-15 positive nuclei per 200,000 leukocytes) in peripheral blood in the setting of acute clinical disease.

### E2 — Strong evidence
- Characteristic fundoscopic examination revealing CMV retinitis with confluent yellow-white retinal necrosis accompanied by intraretinal hemorrhages along retinal vascular arcades ("pizza-pie" or "scrambled eggs with ketchup" appearance) in an immunocompromised patient (typically AIDS with CD4 < 50 cells/uL).
- Endoscopic demonstration of deep, sharply demarcated, punched-out mucosal ulcers in the esophagus, stomach, or colon, with compatible histopathology pending molecular confirmation.
- High-level systemic CMV viral load in an immunocompromised patient (post-transplant or advanced HIV/AIDS) with compatible end-organ manifestations (interstitial pneumonitis, hepatitis, colitis) and marked clinical response to specific intravenous ganciclovir, foscarnet, or oral valganciclovir.

### E3 — Supportive
- Constitutional "mononucleosis-like syndrome" in an immunocompetent host: persistent fever, fatigue, malaise, atypical lymphocytosis (>10%), and mild-to-moderate transaminitis with negative heterophile antibody (Monospot) test.
- Detection of anti-CMV IgM antibodies in serum (suggestive of acute primary infection, but subject to cross-reactivity and prolonged persistence).
- Qualitative or low-copy quantitative CMV PCR without clear end-organ syndrome.
- Non-specific interstitial ground-glass opacities on chest radiography or HRCT.

### Major confusable diseases
```text
Cytomegalovirus ↔ Epstein-Barr Virus (EBV / Infectious Mononucleosis)
Cytomegalovirus ↔ Herpes Simplex Virus (HSV esophagitis / ulcerations / encephalitis)
Cytomegalovirus ↔ Pneumocystis jirovecii (interstitial lung disease in immunocompromised)
Cytomegalovirus ↔ Ocular Toxoplasmosis (retinochoroiditis vs necrotizing retinitis)
```

### Important diagnostic trap
CMV IgG seropositivity alone reflects past latent exposure (seroprevalence >60-90% in adult populations worldwide) and MUST NEVER be coded as active CMV disease (assign E0_CONTRADICTED / EXCLUDED). Asymptomatic CMV shedding in urine or saliva without organ involvement does not constitute CMV disease.

---

## 5.27 Syphilis (*Treponema pallidum*)

### E1 — Disease-defining / confirmatory
- Direct microscopic visualization of *Treponema pallidum* by Darkfield Microscopy demonstrating characteristic morphology and corkscrew motility in serous exudate from primary chancre, condylomata lata, or cutaneous lesions.
- Positive *Treponema pallidum* nucleic acid amplification test (NAAT / real-time PCR) from lesion exudate, tissue biopsy, or CSF.
- Histopathologic demonstration of spirochetes by silver staining (Warthin-Starry or Steiner stain) or specific *T. pallidum* immunohistochemistry (IHC) in affected tissue.
- Reactive cerebrospinal fluid Venereal Disease Research Laboratory test (CSF-VDRL) in the absence of gross blood contamination (diagnostic of neurosyphilis).
- Dual reactivity on both a quantitative nontreponemal test (RPR or VDRL) AND a confirmatory treponemal test (TP-PA, FTA-ABS, EIA, or CIA), accompanied by a >=4-fold titer increase or documented seroconversion in an active clinical presentation.

### E2 — Strong evidence
- Classic primary syphilis chancre: single, indurated, painless ulcer with clean non-purulent base and regional non-tender painless lymphadenopathy in an active sexual contact, with reactive treponemal serology.
- Secondary syphilis syndrome: generalized non-pruritic maculopapular rash characteristically involving palms and soles, mucous patches, or condylomata lata, with high-titer nontreponemal test (RPR >= 1:16 or VDRL >= 1:8) and reactive confirmatory treponemal assay.
- Late tertiary syphilis presentation: syphilitic aortitis with ascending thoracic aortic aneurysm ("tree-barking" calcification) or gummatous granulomatous lesions responsive to treponemicidal therapy with reactive treponemal antibodies.
- Classic Argyll Robertson pupils (accommodate but do not react to light) in a treponemal-seropositive patient.

### E3 — Supportive
- Generalized painless lymphadenopathy, constitutional symptoms (fever, malaise, weight loss, headache), moth-eaten alopecia.
- Isolated low-titer nontreponemal test (e.g. RPR 1:1 to 1:4) pending confirmatory treponemal testing.
- Rapid clinical and serological response (>=4-fold nontreponemal titer drop at 6-12 months) following intramuscular benzathine penicillin G therapy.

### Major confusable diseases
```text
Syphilis (Primary chancre) ↔ Genital Herpes Simplex Virus (painful clustered vesicles/ulcers)
Syphilis (Primary chancre) ↔ Chancroid (Haemophilus ducreyi; painful soft purulent ulcers)
Syphilis (Secondary rash) ↔ Pityriasis Rosea, Psoriasis, Drug Eruption, Secondary Dengue
Syphilis (Neurosyphilis) ↔ Neuroborreliosis (Lyme disease), Multiple Sclerosis
```

### Important diagnostic trap
Biological false positive (BFP) nontreponemal tests (reactive RPR/VDRL with negative treponemal tests) occur in pregnancy, autoimmune disorders (systemic lupus, antiphospholipid syndrome), malaria, and viral infections. Isolated treponemal test positivity without nontreponemal reactivity often represents successfully treated past syphilis (serological scar) and does not indicate active disease in the absence of treatment history or reinfection.

---

## 5.28 Pneumocystis Pneumonia (PJP / *Pneumocystis jirovecii*)

### E1 — Disease-defining / confirmatory
- Direct microscopic visualization of *Pneumocystis jirovecii* cysts or trophic forms in respiratory specimens (bronchoalveolar lavage [BAL] fluid, induced sputum, or lung transbronchial biopsy) using silver stain (Gomori methenamine silver [GMS] showing characteristic 4-7 um rounded, cup-shaped, or collapsed ping-pong ball cysts with prominent focal dark dots), Toluidine Blue O, Calcofluor White, or Giemsa.
- Direct immunofluorescence assay (DFA) using monoclonal antibodies demonstrating bright apple-green fluorescent *P. jirovecii* cysts in BAL or induced sputum.
- High-copy quantitative real-time PCR (qPCR) in BAL fluid exceeding validated clinical diagnostic thresholds established to differentiate active pneumonia from asymptomatic respiratory colonization.

### E2 — Strong evidence
- Characteristic high-resolution chest CT (HRCT) demonstrating bilateral, symmetrical perihilar ground-glass opacities (GGO) with subpleural or peripheral sparing AND significantly elevated serum (1,3)-beta-D-glucan (BDG > 80 pg/mL) in an immunocompromised host (HIV with CD4 < 200 cells/uL, prolonged glucocorticoid use, hematologic malignancy, or solid organ transplant) presenting with progressive exertional dyspnea, dry cough, hypoxemia out of proportion to exam, and rapid clinical improvement upon therapeutic trimethoprim-sulfamethoxazole (TMP-SMX).
- Typical clinical triad of subacute exertional dyspnea, dry cough, and marked exercise-induced pulse oximetry desaturation with elevated serum lactate dehydrogenase (LDH > 400-500 U/L) and positive qualitative PCR in BAL fluid in high-risk immunocompromised setting.

### E3 — Supportive
- Subacute progressive dyspnea on exertion, fever, non-productive cough, tachypnea in an immunocompromised host.
- Isolated elevated serum lactate dehydrogenase (LDH) or isolated elevated (1,3)-beta-D-glucan without respiratory microbiological confirmation.
- Chest radiograph demonstrating bilateral diffuse interstitial perihilar infiltrates.
- Favorable response to empiric TMP-SMX or intravenous pentamidine.

### Major confusable diseases
```text
Pneumocystis jirovecii pneumonia ↔ COVID-19 Acute Respiratory Distress
Pneumocystis jirovecii pneumonia ↔ Cytomegalovirus (CMV) pneumonitis
Pneumocystis jirovecii pneumonia ↔ Mycoplasma pneumoniae / Chlamydophila pneumonia
Pneumocystis jirovecii pneumonia ↔ Non-cardiogenic Pulmonary Edema / Diffuse Alveolar Hemorrhage
```

### Important diagnostic trap
Low-copy *P. jirovecii* PCR in respiratory secretions can represent asymptomatic colonization (frequently encountered in COPD, mild immunosuppression, or healthy carriers) without invasive pneumonitis. Serum (1,3)-beta-D-glucan is a pan-fungal cell wall marker that is also positive in invasive candidiasis and aspergillosis, and yields false positives after administration of certain intravenous immunoglobulins (IVIG) or albumin.

---

## 5.29 Nocardiosis (*Nocardia* species)

### E1 — Disease-defining / confirmatory
- Isolation and culture of *Nocardia* species (e.g., *N. asteroides*, *N. brasiliensis*, *N. farcinica*, *N. cyriacigeorgica*, *N. nova*) from a normally sterile clinical specimen (bronchoalveolar lavage, lung tissue/biopsy, brain abscess aspirate, blood, skin biopsy, cerebrospinal fluid) with definitive species-level identification by 16S rRNA gene sequencing or MALDI-TOF mass spectrometry.
- Direct microscopic visualization in clinical specimen of Gram-positive, thin, beaded, delicate branching filamentous rods that are **partially acid-fast** on Modified Kinyoun or Fite-Faraco staining (and negative, patchy, or weakly stained on conventional Ziehl-Neelsen staining).

### E2 — Strong evidence
- Characteristic disseminated nocardial syndrome: necrotizing or cavitary pulmonary disease accompanied by single or multiple ring-enhancing brain abscesses in an immunocompromised patient (e.g., solid organ transplant recipient, prolonged corticosteroid therapy, hematologic malignancy), with demonstration of branching Gram-positive beaded bacilli on initial aspirate or smear pending definitive culture confirmation.
- Primary cutaneous/lymphocutaneous (sporotrichoid) nocardiosis or mycetoma presenting with nodular suppurative lesions following soil/thorn trauma, with demonstration of partially acid-fast branching beaded filaments on exudate/biopsy.

### E3 — Supportive
- Subacute to chronic cough, fever, night sweats, weight loss, hemoptysis with chest CT demonstrating nodular or cavitary infiltrates in an immunocompromised host.
- Multiple ring-enhancing brain lesions on contrast MRI/CT in a patient with unexplained pulmonary infiltrates.
- Favorable clinical and radiological resolution following prolonged targeted antimicrobial therapy with sulfonamides/trimethoprim-sulfamethoxazole (TMP-SMX), carbapenems (imipenem), or amikacin.

### Major confusable diseases
```text
Nocardiosis ↔ Tuberculosis (Mycobacterium tuberculosis; standard Ziehl-Neelsen strongly positive, non-branching)
Nocardiosis ↔ Actinomycosis (Actinomyces israelii; strictly anaerobic, non-acid-fast, sulfur granules)
Nocardiosis ↔ Fungal cavitary disease (Aspergillus, Histoplasma, Blastomyces)
Nocardiosis ↔ Pyogenic bacterial brain abscess / metastatic malignancy
```

### Important diagnostic trap
Standard Ziehl-Neelsen staining uses a strong mineral acid decolorizer that typically completely destains *Nocardia*, leading to false-negative acid-fast reporting. Conversely, misinterpreting *Nocardia* as *M. tuberculosis* due to partial acid-fastness leads to inappropriate anti-tubercular regimens. *Actinomyces* species are morphologically similar branching Gram-positive rods but are strictly anaerobic, completely non-acid-fast on modified stains, and produce true macroscopic sulfur granules.

---

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

# 9. Epidemiology and Exposure Are Evidence of Plausibility, Not Confirmation

The following are categorized as E3 or E0:

- Immunocompromised state (AIDS, solid organ transplant, high-dose steroids);
- Sexual contact history;
- Soil, agriculture, or thorn-prick exposure;
- Travel history or residence in endemic regions.

They increase prior probability but do not establish a patient-level disease diagnosis claim.

---

# 10. Negative Evidence Must Be Attached to a Specific Claim

A negative test result (e.g. "RPR non-reactive", "GMS negative", "CMV PCR undetectable") refutes the specific disease claim if performed during the appropriate diagnostic window with validated sensitivity.

---

# 11. Implications for Claim Reconciliation

1. **True Coinfection:** When a patient possesses valid E1/E2 evidence for two target diseases (e.g., CMV colitis + Pneumocystis pneumonia in an AIDS patient), both pairs are independently evaluated and assigned `POSITIVE` (with appropriate clinical role: `PRIMARY_DIAGNOSIS` or `COMORBIDITY`).
2. **Differential Diagnosis Ruled Out:** When a target disease was evaluated in the differential diagnosis but testing was negative, assign `NEGATIVE` (clinical role `RULED_OUT_DIAGNOSIS`).
3. **Passing Context / Non-Target:** When a disease is mentioned in the discussion or background literature without reference to the index patient, assign `EXCLUDED_NON_TARGET_CASE`.

---

# 12. Mapping to `02_clinical_claim_schema.md`

All annotations must produce valid JSON records adhering to the 12-step schema, specifically populating:
- `step8_case_definition`: `CONFIRMED`, `PROBABLE`, `SUSPECTED`, or `NOT_MET`
- `step9_evidence_strength`: `E1_CONFIRMATORY`, `E2_HIGHLY_SPECIFIC`, `E3_SUPPORTIVE`, `E4_CONTEXT`, or `E0_CONTRADICTED`
- `step9_key_evidence`: structured evidence items with verbatim character offsets (`start_char`, `end_char`).

---

# 13. Minimum Evidence Standard for the 4-Disease Benchmark

For an annotation decision of `POSITIVE`:
- At least ONE evidence item must be rated `E1_CONFIRMATORY` OR `E2_HIGHLY_SPECIFIC`.
- The assertion must be `AFFIRMED`.
- The temporality must be `CURRENT_EPISODE`.
- The clinical role must be `PRIMARY_DIAGNOSIS`, `SECONDARY_DIAGNOSIS`, or `COMORBIDITY`.

---

# 14. What This Matrix Explicitly Prevents

1. **Keyword Overlap Hallucination:** Prevents coding a case as positive based on incidental mentions in differential diagnosis or citations.
2. **Colonization / Latency Conflation:** Prevents classifying latent CMV IgG or low-copy PJP colonization as acute active clinical disease.
3. **Misidentification of Branching / Acid-fast Organisms:** Enforces strict distinction between *Nocardia*, *Actinomyces*, and *Mycobacterium tuberculosis*.
4. **False Positive Serology Traps:** Prevents unconfirmed RPR biological false positives from polluting the gold standard.

---

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
| Melioidosis | [CDC Melioidosis for Healthcare Personnel (2024)](https://www.cdc.gov/melioidosis/hcp/clinical-overview/) ; [WHO Neglected Tropical Diseases: Melioidosis](https://www.who.int/teams/control-of-neglected-tropical-diseases) |
| Histoplasmosis | [IDSA Clinical Practice Guidelines for Histoplasmosis](https://academic.oup.com/cid/article/45/7/807/388277) ; [CDC Histoplasmosis Guidelines](https://www.cdc.gov/fungal/diseases/histoplasmosis/index.html) |
| Cryptococcosis | [WHO Guidelines for Diagnosing Cryptococcal Disease (2022)](https://www.who.int/publications/i/item/9789240052178) ; [CDC Cryptococcosis Testing](https://www.cdc.gov/fungal/diseases/cryptococcosis/) |
| Neurocysticercosis | [WHO Guidelines on Management of Taenia solium Neurocysticercosis (2021)](https://www.who.int/publications/i/item/9789240032231) ; [CDC DPDx Cysticercosis](https://www.cdc.gov/dpdx/cysticercosis/) |
| Amoebiasis | [CDC DPDx Amebiasis](https://www.cdc.gov/dpdx/amebiasis/) ; [WHO Amoebiasis Technical Report](https://www.who.int/publications/i/item/WHO-TRS-881) |
| Echinococcosis | [WHO Informal Working Group on Echinococcosis (WHO-IWGE)](https://www.who.int/activities/controlling-echinococcosis) ; [CDC DPDx Echinococcosis](https://www.cdc.gov/dpdx/echinococcosis/) |
| Schistosomiasis | [WHO Guideline on Control and Elimination of Human Schistosomiasis (2022)](https://www.who.int/publications/i/item/9789240041608) ; [CDC DPDx Schistosomiasis](https://www.cdc.gov/dpdx/schistosomiasis/) |
| Leprosy | [WHO Guidelines for Diagnosis, Treatment and Prevention of Leprosy (2018)](https://www.who.int/publications/i/item/9789290226383) ; [CDC Hansen's Disease](https://www.cdc.gov/hansens-disease/) |
| Lymphatic Filariasis | [WHO Global Programme to Eliminate Lymphatic Filariasis (GPELF)](https://www.who.int/teams/control-of-neglected-tropical-diseases/lymphatic-filariasis) ; [CDC DPDx Filariasis](https://www.cdc.gov/dpdx/filariasis/) |
| Aspergillosis | [IDSA Practice Guidelines for Diagnosis and Management of Aspergillosis (2016)](https://academic.oup.com/cid/article/63/4/e1/2565653) ; [WHO Fungal Priority Pathogens List (2022)](https://www.who.int/publications/i/item/9789240060241) |
| Cytomegalovirus | [NIH/CDC/HIVMA Guidelines for the Prevention and Treatment of Opportunistic Infections in Adults and Adolescents with HIV (CMV)](https://clinicalinfo.hiv.gov/en/guidelines/hiv-clinical-guidelines-adult-and-adolescent-opportunistic-infections/cytomegalovirus) ; [IDSA/AST CMV Guidelines](https://academic.oup.com/cid/article/68/7/e1/5285748) |
| Syphilis | [CDC Laboratory Recommendations for Syphilis Testing, United States, 2024 (MMWR Recomm Rep 2024;73(No. RR-1))](https://www.cdc.gov/mmwr/volumes/73/rr/rr7301a1.htm) ; [CDC STI Treatment Guidelines: Syphilis](https://www.cdc.gov/std/treatment-guidelines/syphilis.htm) |
| Pneumocystis | [NIH/CDC/HIVMA Guidelines for Opportunistic Infections in HIV: Pneumocystis Pneumonia](https://clinicalinfo.hiv.gov/en/guidelines/hiv-clinical-guidelines-adult-and-adolescent-opportunistic-infections/pneumocystis-pneumonia) |
| Nocardiosis | [Mayo Clinic Proceedings: Nocardiosis Updates & Clinical Overview (Wilson JW, 2012)](https://www.mayoclinicproceedings.org/article/S0025-6196(12)00262-1/fulltext) ; [CDC Bacterial Infections: Nocardiosis](https://www.cdc.gov/) |

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

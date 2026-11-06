---
name: soap-structuring-agent
description: >
  Transforms raw clinical case reports (raw_case_text) into standard 8-field
  SOAP notes conforming to the Boston University School of Medicine write-up guide
  and LOINC 81218-0. Populates sandbox_soap/workspace/core_positive_1500/*.json files.
---

# Clinical SOAP Note Structuring Skill

## 1. Purpose & Clinical Authority

This skill guides **AI Agents** to transform retrospective, unstructured medical case reports (`raw_case_text`) into standardized, high-fidelity **SOAP notes (8 clinical fields)**.

### Reference Standards
- **SOAP Note Framework:** Subjective, Objective, Assessment, Plan ([Wikipedia: SOAP note](https://en.wikipedia.org/wiki/SOAP_note))
- **BU School of Medicine Write-Up Guide:** [LOINC 81218-0](https://loinc.org/81218-0) (Comprehensive History and Physical Note)
- **Clinical Benchmarks:** DiagnosisArena (ACL 2025), CUPCase / MultiCaRe Structuring (Lecture 3), RareBench (KDD 2024)

---

## 2. Workspace & File Handling

### Target Directory
All case files reside in disease folders under:
`codebases/data_processing/sandbox_soap/workspace/core_positive_1500/<target_disease>/`

### Input Case Schema
Each case file (`{case_id}__{target_disease}.json`) starts with an initialized empty template:
```json
{
  "case_id": "PMC1184073_01",
  "pair_id": "PMC1184073_01::Typhoid_Fever",
  "target_disease": "Typhoid_Fever",
  "raw_case_text": "...",
  "soap_note": {
    "subjective": {
      "chief_complaint": null,
      "history_of_present_illness": null,
      "past_medical_history": null,
      "review_of_systems": null
    },
    "objective": {
      "physical_examination": null,
      "routine_investigations": null,
      "advanced_workup": null
    },
    "assessment_and_plan": {
      "assessment_and_confirmation": null
    }
  }
}
```

### Agent Action
Your task is to:
1. Open and read a target case JSON file.
2. Read `raw_case_text` thoroughly and extract clinical entities according to the **8-Field Specification** below.
3. Update the `soap_note` dictionary in-place with the structured text.
4. Save the file back with the populated `soap_note`.

---

## 3. The 8-Field Clinical Specification

```
                                  SOAP NOTE ARCHITECTURE
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ S - SUBJECTIVE                                                                         │
│   1. chief_complaint             : Age, gender, primary symptom, exact duration.      │
│   2. history_of_present_illness  : Chronological onset, evolution, severity, signs.    │
│   3. past_medical_history        : Past conditions, prior infections, exposures, trips │
│   4. review_of_systems           : Secondary patient-reported symptoms, prior meds.    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ O - OBJECTIVE                                                                          │
│   5. physical_examination        : Vitals, general appearance, systematic exam.        │
│   6. routine_investigations      : CBC, CRP, ESR, LFTs, renal, urinalysis, CXR, smear. │
│   7. advanced_workup             : CT, MRI, endoscopy, lumbar puncture, antibiogram.  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ A & P - ASSESSMENT & PLAN                                                              │
│   8. assessment_and_confirmation : Definitive culture/PCR, ruled-out differentials,    │
│                                    treatment regimen, clinical response and outcome.   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

### Detailed Field Guidance:

#### 1. `chief_complaint` (CC)
- Format: *"A [age]-year-old [gender] presenting with [primary symptom] of [duration] duration."*
- Strictly 1–2 sentences.
- **ANTI-LEAKAGE RULE:** Never include the final diagnosis or confirmed pathogen in the CC.

#### 2. `history_of_present_illness` (HPI)
- Detailed narrative of the presenting illness: when symptoms began, character (e.g. intermittent vs remittent fever), location, severity, progression, and negative review of cardinal symptoms.
- **ANTI-LEAKAGE RULE:** If the author wrote *"Patient presented with confirmed Brucellosis"*, omit the diagnosis and retain only the symptoms (fever, arthralgia).

#### 3. `past_medical_history` (PMH)
- Chronic illnesses (diabetes, cirrhosis, hypertension, malignancy).
- Prior infections (e.g., *"attack of suspected typhoid 2 months prior treated with chloramphenicol"*).
- **Epidemiological Risk Factors:** Raw/unpasteurized dairy intake, animal contact (cattle, goats, camels), endemic region residence, travel history, mosquito/tick bites.
- If completely absent, set to `null`.

#### 4. `review_of_systems` (ROS)
- Secondary constitutional or organ-specific symptoms reported by the patient (headache, myalgias, nausea, anorexia, weight loss).
- Home medications or prior empirical drugs.
- If no secondary symptoms outside HPI are reported, set to `null`.

#### 5. `physical_examination` (PE)
- Vital signs: T, HR, BP, RR, SpO2.
- Clinician's physical examination: General state (pale, jaundiced, acute distress), cardiovascular, pulmonary, abdominal (hepatomegaly, splenomegaly, tenderness, guarding), skin/rashes (petechiae, rose spots), neurological findings.
- If physical examination details are absent, set to `null`.

#### 6. `routine_investigations`
- Baseline non-definitive laboratory tests & bedside imaging:
  - CBC: WBC count, differential, Hemoglobin, Platelet count.
  - Biochemistry: CRP, ESR, AST/ALT, Bilirubin, Creatinine, BUN.
  - Urinalysis, stool routine.
  - Non-specific screening serologies: Widal test, peripheral blood smear for malaria, rapid HIV screening.
  - Baseline imaging: Chest X-ray, bedside abdominal ultrasound.
- Always preserve exact numbers and units (e.g. `WBC 1.7 x 10^9/L`).

#### 7. `advanced_workup`
- Specialized imaging: CT scan (chest/abdomen/brain), MRI, echocardiogram.
- Specialized invasive tests: Lumbar puncture/CSF analysis, bone marrow biopsy/aspirate, endoscopy, bronchoscopy, thoracentesis.
- Antibiogram & susceptibility testing: Disc diffusion, agar dilution MIC values, resistance profiles.
- If none performed, set to `null`.

#### 8. `assessment_and_confirmation`
- **Definitive Microbiological Confirmation:** Blood culture, tissue culture, PCR/NAAT, MALDI-TOF, specific antibody seroconversion confirming the target disease.
- **Clinical Assessment:** Final diagnostic conclusion and differentials definitively excluded.
- **Plan & Outcome:** Targeted antimicrobial regimen (drugs, dosages, route, duration), clinical response (treatment failure, defervescence, recovery), and follow-up status.

---

## 4. Five Golden Rules for the Agent

1. **NO LEAKAGE INTO S & O:** Confirmatory culture, PCR, and final diagnosis belong EXCLUSIVELY in `assessment_and_confirmation`.
2. **ZERO HALLUCINATION:** Extract only what is documented in `raw_case_text`. Never guess or fill in missing vitals or lab values.
3. **EXPLICIT NULL POLICY:** If a field has no information in the text, assign `null` (not `"None"` or `"N/A"`).
4. **PRESERVE CLINICAL MEASUREMENTS:** Keep exact numbers, units, and ranges (`WBC 1.7 x 10^9/L`, `MIC 0.5 mcg/mL`).
5. **PRESERVE JSON INTEGRITY:** Keep `case_id`, `pair_id`, `target_disease`, and `raw_case_text` intact. Only overwrite `soap_note`.

---

## 5. Reference Prompt File

A full system prompt with a few-shot demonstration is available at:
[`codebases/data_processing/sandbox_soap/prompts/soap_structuring_prompt.md`](file:///mnt/DATA/VSCode/Clinicians_MultiModel/codebases/data_processing/sandbox_soap/prompts/soap_structuring_prompt.md)

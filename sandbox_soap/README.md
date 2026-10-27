# Clinical SOAP Structuring Sandbox Environment

> **Purpose:** Isolated execution environment and workspace for transforming unstructured clinical case reports into standardized 8-field SOAP notes adhering to BU School of Medicine Write-Up Guide and LOINC 81218-0.

---

## 1. Directory Layout

```text
sandbox_soap/
├── .agents/                               # Sandboxed Agent Customizations
│   └── skills/
│       └── soap-structuring-agent/        # Skill definition for SOAP note extraction
│           └── SKILL.md
├── prompts/                               # Clinical Structuring Prompts
│   └── soap_structuring_prompt.md         # Full clinical prompt specification (BU Guide & LOINC 81218-0)
├── scripts/                               # Validation & Quality Assurance
│   └── validate_soap.py                   # Automated validator for 8 fields & diagnostic leakage
└── workspace/                             # Structured Clinical Workspace
    └── core_positive_1500/                # 835 Core Positive Cases (15 target diseases)
        ├── manifest.json                  # Dataset metadata & disease breakdown
        ├── Brucellosis/                   # 100 cases
        ├── COVID-19/                      # 100 cases
        ├── Chikungunya/                   # 20 cases
        ├── Cholera/                       # 6 cases
        ├── Dengue/                        # 100 cases
        ├── Ebola_Filovirus/               # 3 cases
        ├── HIV_AIDS/                      # 100 cases
        ├── Leishmaniasis/                 # 100 cases
        ├── Leptospirosis/                 # 49 cases
        ├── Malaria/                       # 100 cases
        ├── Rabies/                        # 3 cases
        ├── Tuberculosis/                  # 100 cases
        ├── Typhoid_Fever/                 # 31 cases
        ├── Yellow_Fever/                  # 3 cases
        └── Zika/                          # 20 cases
```

---

## 2. Agent Execution Workflow

All structuring agents operate strictly within `sandbox_soap/workspace/`:
1. **Inputs:** Loaded from `sandbox_soap/workspace/core_positive_1500/{Disease}/{case_id}__{Disease}.json`
2. **Prompts:** Adhere to definitions in `sandbox_soap/prompts/soap_structuring_prompt.md`
3. **Extraction:** Transform `raw_case_text` into standard 8 clinical fields:
   - **Subjective (S):** `chief_complaint`, `history_of_present_illness`, `past_medical_history`, `review_of_systems`
   - **Objective (O):** `physical_examination`, `routine_investigations`, `advanced_workup`
   - **Assessment & Plan (A/P):** `assessment_and_confirmation`
4. **Anti-Leakage Rule:** Strictly prevent confirmatory diagnostic test results (e.g., blood cultures, PCR, definitive diagnosis) from leaking into Subjective or Objective sections.
5. **Outputs:** Update the `soap_note` structure in-place in each case JSON file.

### Validating Structured SOAP Notes

```bash
# Run automated validation across all 15 disease folders (schema, non-empty, anti-leakage checks):
python3 sandbox_soap/scripts/validate_soap.py
```

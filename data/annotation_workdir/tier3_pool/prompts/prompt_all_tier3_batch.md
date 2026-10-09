# Master Clinical Claim Annotation Task: All 10,388 Tier 3 Candidate Pairs

You are the Master Clinical Annotation Coordinator & Evaluator for the MultiCaRe Clinical Gold Standard project.
Your assignment is to process all **10388 candidate pairs** across **15 target diseases** newly produced by the unified generator (Tier 3 mention-only candidates pending annotation).

---

## Overview Table

| Disease | Slug | Pairs | Primary Skill | Input File | Output File |
| :--- | :--- | :---: | :--- | :--- | :--- |
| HIV_AIDS | `hiv_aids` | 4345 | `code/.agents/skills/disease-agent-hiv_aids/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_hiv_aids.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_hiv_aids.jsonl` |\n| Tuberculosis | `tuberculosis` | 2929 | `code/.agents/skills/disease-agent-tuberculosis/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_tuberculosis.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_tuberculosis.jsonl` |\n| COVID-19 | `covid_19` | 1272 | `code/.agents/skills/disease-agent-covid_19/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_covid_19.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_covid_19.jsonl` |\n| Malaria | `malaria` | 682 | `code/.agents/skills/disease-agent-malaria/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_malaria.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_malaria.jsonl` |\n| Brucellosis | `brucellosis` | 318 | `code/.agents/skills/disease-agent-brucellosis/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_brucellosis.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_brucellosis.jsonl` |\n| Ebola_Filovirus | `ebola_filovirus` | 169 | `code/.agents/skills/disease-agent-ebola_filovirus/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_ebola_filovirus.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_ebola_filovirus.jsonl` |\n| Dengue | `dengue` | 166 | `code/.agents/skills/disease-agent-dengue/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_dengue.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_dengue.jsonl` |\n| Leptospirosis | `leptospirosis` | 152 | `code/.agents/skills/disease-agent-leptospirosis/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_leptospirosis.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_leptospirosis.jsonl` |\n| Typhoid_Fever | `typhoid_fever` | 119 | `code/.agents/skills/disease-agent-typhoid_fever/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_typhoid_fever.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_typhoid_fever.jsonl` |\n| Leishmaniasis | `leishmaniasis` | 95 | `code/.agents/skills/disease-agent-leishmaniasis/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_leishmaniasis.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_leishmaniasis.jsonl` |\n| Rabies | `rabies` | 37 | `code/.agents/skills/disease-agent-rabies/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_rabies.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_rabies.jsonl` |\n| Chikungunya | `chikungunya` | 34 | `code/.agents/skills/disease-agent-chikungunya/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_chikungunya.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_chikungunya.jsonl` |\n| Zika | `zika` | 30 | `code/.agents/skills/disease-agent-zika/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_zika.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_zika.jsonl` |\n| Cholera | `cholera` | 21 | `code/.agents/skills/disease-agent-cholera/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_cholera.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_cholera.jsonl` |\n| Yellow_Fever | `yellow_fever` | 19 | `code/.agents/skills/disease-agent-yellow_fever/SKILL.md` | `code/data/annotation_workdir/tier3_pool/input/input_yellow_fever.jsonl` | `code/data/annotation_workdir/tier3_pool/output/output_yellow_fever.jsonl` |

---

## Methodological Core

1. **Fixed Target Disease Evaluation:**
   Each pair must be evaluated strictly for its assigned `target_disease`.
   The agent does not change the disease; it only determines if a valid clinical claim exists for that specific disease in that case.

2. **Blinded Evaluation:**
   The agent must evaluate purely on clinical evidence in the narrative.

3. **Multi-Label vs. Differential Context:**
   - If target disease is confirmed alongside another disease -> `POSITIVE` (True Coinfection).
   - If target disease was tested and negative / ruled out -> `NEGATIVE` (Differential Diagnosis).
   - If target disease was merely cited as background / context -> `EXCLUDED_NON_TARGET_CASE`.

---

## Batch Execution Flow

For each disease in the table above:
1. Load the corresponding disease skill (`code/.agents/skills/disease-agent-{slug}/SKILL.md`).
2. Read the input file: `code/data/annotation_workdir/tier3_pool/input/input_{slug}.jsonl`.
3. Check existing output in: `code/data/annotation_workdir/tier3_pool/output/output_{slug}.jsonl`.
4. Annotate each pair using the 12-step protocol and append output JSONL lines.
5. Write log summary to: `code/data/annotation_workdir/tier3_pool/logs/agent_{slug}.log`.

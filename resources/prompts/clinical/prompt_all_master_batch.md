# Master Batch Annotation Directive — MultiCaRe Clinical Gold Standard (master)

**Total Candidate Pairs:** 24,750 across 29 target diseases.
**Protocol Specification:** `resources/protocols/04_gold_standard_annotation_protocol.md`
**Evidence Matrix:** `resources/protocols/03_evidence_specificity_matrix.md`
**Schema Specification:** `resources/protocols/02_clinical_claim_schema.md`

## Disease Breakdown & File Mapping

| Disease | Slug | Candidate Pairs | Input File | Output File |
|---|---|---:|---|---|
| HIV/AIDS | `hiv/aids` | 5,735 | `data/candidates/input_hiv/aids.jsonl` | `data/annotated/output_hiv/aids.jsonl` |
| Tuberculosis | `tuberculosis` | 4,468 | `data/candidates/input_tuberculosis.jsonl` | `data/annotated/output_tuberculosis.jsonl` |
| COVID-19 | `covid_19` | 4,359 | `data/candidates/input_covid_19.jsonl` | `data/annotated/output_covid_19.jsonl` |
| Cytomegalovirus | `cytomegalovirus` | 2,585 | `data/candidates/input_cytomegalovirus.jsonl` | `data/annotated/output_cytomegalovirus.jsonl` |
| Syphilis | `syphilis` | 1,399 | `data/candidates/input_syphilis.jsonl` | `data/annotated/output_syphilis.jsonl` |
| Malaria | `malaria` | 938 | `data/candidates/input_malaria.jsonl` | `data/annotated/output_malaria.jsonl` |
| Aspergillosis | `aspergillosis` | 801 | `data/candidates/input_aspergillosis.jsonl` | `data/annotated/output_aspergillosis.jsonl` |
| Pneumocystis | `pneumocystis` | 665 | `data/candidates/input_pneumocystis.jsonl` | `data/annotated/output_pneumocystis.jsonl` |
| Cryptococcosis | `cryptococcosis` | 483 | `data/candidates/input_cryptococcosis.jsonl` | `data/annotated/output_cryptococcosis.jsonl` |
| Brucellosis | `brucellosis` | 473 | `data/candidates/input_brucellosis.jsonl` | `data/annotated/output_brucellosis.jsonl` |
| Echinococcosis | `echinococcosis` | 360 | `data/candidates/input_echinococcosis.jsonl` | `data/annotated/output_echinococcosis.jsonl` |
| Dengue | `dengue` | 356 | `data/candidates/input_dengue.jsonl` | `data/annotated/output_dengue.jsonl` |
| Histoplasmosis | `histoplasmosis` | 293 | `data/candidates/input_histoplasmosis.jsonl` | `data/annotated/output_histoplasmosis.jsonl` |
| Leishmaniasis | `leishmaniasis` | 240 | `data/candidates/input_leishmaniasis.jsonl` | `data/annotated/output_leishmaniasis.jsonl` |
| Leptospirosis | `leptospirosis` | 218 | `data/candidates/input_leptospirosis.jsonl` | `data/annotated/output_leptospirosis.jsonl` |
| Nocardiosis | `nocardiosis` | 204 | `data/candidates/input_nocardiosis.jsonl` | `data/annotated/output_nocardiosis.jsonl` |
| Ebola Filovirus | `ebola_filovirus` | 202 | `data/candidates/input_ebola_filovirus.jsonl` | `data/annotated/output_ebola_filovirus.jsonl` |
| Typhoid Fever | `typhoid_fever` | 166 | `data/candidates/input_typhoid_fever.jsonl` | `data/annotated/output_typhoid_fever.jsonl` |
| Neurocysticercosis | `neurocysticercosis` | 138 | `data/candidates/input_neurocysticercosis.jsonl` | `data/annotated/output_neurocysticercosis.jsonl` |
| Leprosy | `leprosy` | 121 | `data/candidates/input_leprosy.jsonl` | `data/annotated/output_leprosy.jsonl` |
| Schistosomiasis | `schistosomiasis` | 92 | `data/candidates/input_schistosomiasis.jsonl` | `data/annotated/output_schistosomiasis.jsonl` |
| Amoebiasis | `amoebiasis` | 83 | `data/candidates/input_amoebiasis.jsonl` | `data/annotated/output_amoebiasis.jsonl` |
| Zika | `zika` | 76 | `data/candidates/input_zika.jsonl` | `data/annotated/output_zika.jsonl` |
| Chikungunya | `chikungunya` | 62 | `data/candidates/input_chikungunya.jsonl` | `data/annotated/output_chikungunya.jsonl` |
| Rabies | `rabies` | 62 | `data/candidates/input_rabies.jsonl` | `data/annotated/output_rabies.jsonl` |
| Melioidosis | `melioidosis` | 55 | `data/candidates/input_melioidosis.jsonl` | `data/annotated/output_melioidosis.jsonl` |
| Cholera | `cholera` | 49 | `data/candidates/input_cholera.jsonl` | `data/annotated/output_cholera.jsonl` |
| Lymphatic Filariasis | `lymphatic_filariasis` | 40 | `data/candidates/input_lymphatic_filariasis.jsonl` | `data/annotated/output_lymphatic_filariasis.jsonl` |
| Yellow Fever | `yellow_fever` | 27 | `data/candidates/input_yellow_fever.jsonl` | `data/annotated/output_yellow_fever.jsonl` |

## Quality & Validation Invariants
- 100% of cases labeled `POSITIVE` must contain at least one confirmatory (`E1_CONFIRMATORY`) or highly specific (`E2_HIGHLY_SPECIFIC`) evidence item.
- All quotes in `step9_key_evidence` must strictly ground to verbatim text in `case_text` with character offsets.
- Label leakage is prohibited: inputs and prompts must remain decoupled from final target assertions.
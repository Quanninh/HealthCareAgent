# Rabies Clinical Gold Standard Annotation — Master Summary & Index

- **Target Disease:** `Rabies`
- **Total Candidate Pairs Evaluated:** `37`
- **Annotator ID:** `disease-agent-rabies`
- **Protocol:** 12-Step Clinical Claim Annotation Protocol (`03_evidence_specificity_matrix.md` §5.13 Rabies)

## Summary Distribution

| Dataset Label (`SKILL.md`) | Decision (`prompt_rabies.md`) | Count | Clinical Description |
| :--- | :--- | :---: | :--- |
| `POSITIVE` | `POSITIVE` | 0 | Confirmed/probable human rabies cases meeting VPD criteria |
| `NEGATIVE` | `NEGATIVE` | 9 | Human cases where rabies was in the differential diagnosis and explicitly ruled out via laboratory or clinical testing |
| `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | 12 | Human cases mentioning rabies only as post-exposure prophylaxis (PEP), prior vaccination, donor exclusion criteria, negative exposure history, or negated hydrophobia |
| `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | 16 | Veterinary / wildlife animal cases (cheetah, cats, dogs, horse, cattle, white-tailed deer) |
| **Total** | **Total** | **37** | **100% of candidate pairs annotated and verified** |

## Case-by-Case Overview Table

| # | Pair ID | Case ID | Subject / CCU | Evidence Strength | Dataset Label (`SKILL.md`) | Decision (`prompt_rabies.md`) | Reasoning File |
| :-: | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 01 | `PMC6005275_01::Rabies` | `PMC6005275_01` | NON_HUMAN_ANIMAL (Acinonyx jubatus (Namibian cheetah)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_01_PMC6005275_01.md` |
| 02 | `PMC5996657_01::Rabies` | `PMC5996657_01` | PRIMARY_PATIENT (55.0y Unknown) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_02_PMC5996657_01.md` |
| 03 | `PMC6739741_01::Rabies` | `PMC6739741_01` | NON_HUMAN_ANIMAL (Felis catus (domestic shorthair cat)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_03_PMC6739741_01.md` |
| 04 | `PMC7313338_01::Rabies` | `PMC7313338_01` | NON_HUMAN_ANIMAL (Felis catus (domestic shorthair cat)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_04_PMC7313338_01.md` |
| 05 | `PMC10184206_01::Rabies` | `PMC10184206_01` | NON_HUMAN_ANIMAL (Felis catus (domestic shorthair cat)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_05_PMC10184206_01.md` |
| 06 | `PMC9372548_02::Rabies` | `PMC9372548_02` | NON_HUMAN_ANIMAL (Equus caballus (Arabian mare)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_06_PMC9372548_02.md` |
| 07 | `PMC3318216_01::Rabies` | `PMC3318216_01` | PRIMARY_PATIENT (17.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_07_PMC3318216_01.md` |
| 08 | `PMC6196918_01::Rabies` | `PMC6196918_01` | NON_HUMAN_ANIMAL (Canis lupus familiaris (Staffordshire Bull Terrier dog)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_08_PMC6196918_01.md` |
| 09 | `PMC4350224_01::Rabies` | `PMC4350224_01` | PRIMARY_PATIENT (11.0y Male) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_09_PMC4350224_01.md` |
| 10 | `PMC3992778_01::Rabies` | `PMC3992778_01` | PRIMARY_PATIENT (55.0y Male) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_10_PMC3992778_01.md` |
| 11 | `PMC9997573_02::Rabies` | `PMC9997573_02` | PRIMARY_PATIENT (2.0y Female) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_11_PMC9997573_02.md` |
| 12 | `PMC3707323_01::Rabies` | `PMC3707323_01` | PRIMARY_PATIENT (8.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_12_PMC3707323_01.md` |
| 13 | `PMC3199917_01::Rabies` | `PMC3199917_01` | PRIMARY_PATIENT (38.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_13_PMC3199917_01.md` |
| 14 | `PMC9932685_01::Rabies` | `PMC9932685_01` | PRIMARY_PATIENT (33.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_14_PMC9932685_01.md` |
| 15 | `PMC6067776_01::Rabies` | `PMC6067776_01` | NON_HUMAN_ANIMAL (Canis lupus familiaris (Chihuahua dog)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_15_PMC6067776_01.md` |
| 16 | `PMC7267871_01::Rabies` | `PMC7267871_01` | PRIMARY_PATIENT (40.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_16_PMC7267871_01.md` |
| 17 | `PMC6501490_01::Rabies` | `PMC6501490_01` | PRIMARY_PATIENT (20.0y Female) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_17_PMC6501490_01.md` |
| 18 | `PMC6458861_01::Rabies` | `PMC6458861_01` | NON_HUMAN_ANIMAL (Canis lupus familiaris (Jack Russell Terrier dog)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_18_PMC6458861_01.md` |
| 19 | `PMC9382088_01::Rabies` | `PMC9382088_01` | NON_HUMAN_ANIMAL (Canis lupus familiaris (Boxer dog)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_19_PMC9382088_01.md` |
| 20 | `PMC7337170_01::Rabies` | `PMC7337170_01` | NON_HUMAN_ANIMAL (Felis catus (European shorthaired cat)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_20_PMC7337170_01.md` |
| 21 | `PMC3204653_01::Rabies` | `PMC3204653_01` | PRIMARY_PATIENT (76.0y Female) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_21_PMC3204653_01.md` |
| 22 | `PMC9022915_01::Rabies` | `PMC9022915_01` | PRIMARY_PATIENT (28.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_22_PMC9022915_01.md` |
| 23 | `PMC9277426_01::Rabies` | `PMC9277426_01` | DONOR (18.0y Female) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_23_PMC9277426_01.md` |
| 24 | `PMC8242143_01::Rabies` | `PMC8242143_01` | PRIMARY_PATIENT (77.0y Male) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_24_PMC8242143_01.md` |
| 25 | `PMC8164334_01::Rabies` | `PMC8164334_01` | PRIMARY_PATIENT (17.0y Female) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_25_PMC8164334_01.md` |
| 26 | `PMC6629187_01::Rabies` | `PMC6629187_01` | PRIMARY_PATIENT (56.0y Female) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_26_PMC6629187_01.md` |
| 27 | `PMC9477003_01::Rabies` | `PMC9477003_01` | NON_HUMAN_ANIMAL (Canis lupus familiaris (Yorkshire Terrier dog)) | `E0_CONTRADICTED` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_27_PMC9477003_01.md` |
| 28 | `PMC10850352_01::Rabies` | `PMC10850352_01` | PRIMARY_PATIENT (77.0y Female) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_28_PMC10850352_01.md` |
| 29 | `PMC11215014_01::Rabies` | `PMC11215014_01` | PRIMARY_PATIENT (22.0y Male) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_29_PMC11215014_01.md` |
| 30 | `PMC10829934_01::Rabies` | `PMC10829934_01` | NON_HUMAN_ANIMAL (Bos taurus (Aberdeen Angus cattle)) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_30_PMC10829934_01.md` |
| 31 | `PMC10829934_03::Rabies` | `PMC10829934_03` | NON_HUMAN_ANIMAL (Bos taurus (crossbred cattle)) | `E0_CONTRADICTED` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_31_PMC10829934_03.md` |
| 32 | `PMC10705509_01::Rabies` | `PMC10705509_01` | PRIMARY_PATIENT (46.0y Male) | `E0_CONTRADICTED` | `NEGATIVE` | `NEGATIVE` | `reasoning_32_PMC10705509_01.md` |
| 33 | `PMC11810149_01::Rabies` | `PMC11810149_01` | PRIMARY_PATIENT (46.0y Female) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_33_PMC11810149_01.md` |
| 34 | `PMC11816176_01::Rabies` | `PMC11816176_01` | NON_HUMAN_ANIMAL (Odocoileus virginianus (white-tailed deer)) | `E0_CONTRADICTED` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_34_PMC11816176_01.md` |
| 35 | `PMC11816176_02::Rabies` | `PMC11816176_02` | NON_HUMAN_ANIMAL (Odocoileus virginianus (white-tailed deer)) | `E0_CONTRADICTED` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_35_PMC11816176_02.md` |
| 36 | `PMC11816176_04::Rabies` | `PMC11816176_04` | NON_HUMAN_ANIMAL (Odocoileus virginianus (white-tailed deer)) | `E0_CONTRADICTED` | `EXCLUDED_NON_HUMAN` | `EXCLUDED_NON_CASE_REPORT` | `reasoning_36_PMC11816176_04.md` |
| 37 | `PMC12558858_01::Rabies` | `PMC12558858_01` | PRIMARY_PATIENT (4.0y Male) | `E4_BACKGROUND_OR_CONTEXT_ONLY` | `EXCLUDED_NON_TARGET_CASE` | `EXCLUDED_NON_TARGET_CASE` | `reasoning_37_PMC12558858_01.md` |

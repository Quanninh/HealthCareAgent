# This is the branch where I update progress on my reasoning labeling
## `oss_extracted_cases.jsonl` Schema

Each line is a JSON object (2,949 records total) joining the OSS model extraction output (`out_oss_Khoa29/*.md`) with the ground-truth SOAP labels (`model_inputs_soap_21_final.jsonl`):

| Field | Type | Source | Description |
|---|---|---|---|
| `case_id` | `string` | Derived from `sample_id` | Filename-safe case identifier (e.g., `PMC10046697_01__Aspergillosis`), generated via `sanitize_case_id(sample_id)` and matching the `.md` filename stem in `out_oss_Khoa29/`. |
| `sample_id` | `string` | `model_inputs_soap_21_final.jsonl` | Original unique case-disease pair identifier (e.g., `PMC10046697_01::Aspergillosis`). |
| `case_analysis` | `string` | OSS `.md` (`<case_analysis>`) | Model's internal planning notes covering target diagnosis/scope check, breakpoint selection, and key analytic distinctions. |
| `case_prompt` | `string` | OSS `.md` (`<case_prompt>`) | Extracted clinical case presentation truncated at the diagnostic breakpoint so the final diagnosis is not spoiled. |
| `diagnostic_reasoning` | `string` | OSS `.md` (`<diagnostic_reasoning>`) | Numbered step-by-step clinical reasoning points paired with supporting quotes from the original report. |
| `final_diagnosis` | `string` | OSS `.md` (`<final_diagnosis>`) | Diagnosis predicted by the OSS extraction model: either canonical disease name(s) from the 21 `SELECTED_DISEASES` (e.g., `aspergillosis`, or comma-separated for co-infections) or `<disease> -> OUT_OF_SCOPE`. |
| `target_disease` | `string` | `model_inputs_soap_21_final.jsonl` | Target disease folder/category associated with the case in the SOAP dataset (e.g., `Aspergillosis`, `COVID-19`). |
| `clinical_label` | `string` | `model_inputs_soap_21_final.jsonl` | SOAP ground-truth label for `target_disease`: `"POSITIVE"` (1,770 cases) or `"NEGATIVE"` (1,179 cases). |
| `12step` | `string` | `model_inputs_soap_21_final.jsonl` (`final_diagnosis`) | Ground-truth label derived from SOAP: equals `target_disease` when `clinical_label == "POSITIVE"`, or `"OUT_OF_SCOPE"` when `clinical_label == "NEGATIVE"`. |
| `matched` | `boolean` | Computed | `true` if the canonicalized `12step` label matches the OSS model's `final_diagnosis`, `false` otherwise. Resolves `12step` to lowercase canonical form (e.g., `COVID-19` → `covid_19`) before checking against OSS diagnosis tokens, and ensures `OUT_OF_SCOPE` predictions only match `12step == "OUT_OF_SCOPE"` (2,358 / 2,949 matched overall). |
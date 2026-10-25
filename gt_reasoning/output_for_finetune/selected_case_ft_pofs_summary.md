# Selected Cases for Fine-Tuning (Out-of-Scope Filtered) — `selected_case_ft_pofs`

The 15 filtered JSONL files have been generated and saved into the `selected_case_ft_pofs` directory.

---

## 1. Filtering Logic Applied

### Target Labels Kept
Only records with `dataset_label` / `validated_label` equal to:
* **`POSITIVE`**
* **`NEGATIVE`**
* **`EXCLUDED_NON_TARGET_CASE`**

*(All `UNRESOLVED`, `EXCLUDED_NON_SINGLE_PATIENT`, and `EXCLUDED_NON_HUMAN` records were removed).*

### Out-of-Scope Negative/Excluded Isolation
* For **`NEGATIVE`** and **`EXCLUDED_NON_TARGET_CASE`**, each `case_id` was checked across the entire 15-disease corpus.
* Any case evaluated for another target disease among the remaining 14 diseases (e.g., tested negative for Dengue but tested positive/evaluated for Chikungunya) was excluded.
* **Only cases describing patients with conditions out-of-scope** (i.e., not appearing in any other disease file) were kept.

---

## 2. Summary of Resulting Files in `selected_case_ft_pofs`

| File | Kept Lines |
| :--- | :--- |
| `output_brucellosis.jsonl` | 45 |
| `output_chikungunya.jsonl` | 2 |
| `output_cholera.jsonl` | 12 |
| `output_covid_19.jsonl` | 2,649 |
| `output_dengue.jsonl` | 33 |
| `output_ebola_filovirus.jsonl` | 22 |
| `output_hiv_aids.jsonl` | 1,134 |
| `output_leishmaniasis.jsonl` | 30 |
| `output_leptospirosis.jsonl` | 8 |
| `output_malaria.jsonl` | 114 |
| `output_rabies.jsonl` | 12 |
| `output_tuberculosis.jsonl` | 1,227 |
| `output_typhoid_fever.jsonl` | 10 |
| `output_yellow_fever.jsonl` | 4 |
| `output_zika.jsonl` | 6 |
| **Total** | **5,308** |

---

## 3. Breakdown by Label

* **`POSITIVE`**: 3,617 lines
* **`EXCLUDED_NON_TARGET_CASE`**: 1,027 lines
* **`NEGATIVE`**: 664 lines

> **Note on Excluded Records:**  
> A total of 900 records from `selected_case_finetune` were excluded during this filtering pass:
> * 449 `EXCLUDED_NON_SINGLE_PATIENT`
> * 210 `UNRESOLVED`
> * 26 `EXCLUDED_NON_HUMAN`
> * 124 cross-disease `NEGATIVE` (patient evaluated for another target disease)
> * 91 cross-disease `EXCLUDED_NON_TARGET_CASE` (patient evaluated for another target disease)


# Group 2 Audit Statistics (`audit_results/consolidated_audit_results.csv`)

- **Total Audited Cases:** 248 / 248 (100.0% coverage across all 5 splits)
- **Total Batch Files Parsed:** 52 / 52 (DeepSeek: 49 files / 233 cases, Claude: 2 files / 10 cases, Gemini: 1 file / 5 cases)
- **Anomalies:** 0 missing cases, 0 duplicates, 0 score-sum or format mismatches (5 bare `PMC...` IDs in `claude-1795617997025.txt` were automatically normalized to `<case_id>__Aspergillosis` during consolidation).

---

## 1. Overall Adjudicated Verdict (`whos_right`)

| Verdict | Count | Percentage |
| :--- | :---: | :---: |
| **`Both right`** | **213** | **85.9%** |
| **`Method Y`** (MultiCaRe 12-Step) | **18** | **7.3%** |
| **`Method X`** (MedCase GPT-OSS 120B) | **17** | **6.9%** |
| **`Both wrong`** | **0** | **0.0%** |
| **Total** | **248** | **100.0%** |

---

## 2. Diagnostic Primacy Holder ($D_6$, from `notes`)

| Primacy Holder | Count | Percentage |
| :--- | :---: | :---: |
| **`METHOD_X`** | **213** | **85.9%** |
| **`METHOD_Y`** | **29** | **11.7%** |
| **`BOTH`** | **4** | **1.6%** |
| **`NEITHER`** | **2** | **0.8%** |

---

## 3. Mean Scores Across the 6 Rubric Dimensions

| Method | Overall (`/30`) | $D_1$ Accuracy | $D_2$ Rule-Out | $D_3$ Temporality | $D_4$ Grounding | $D_5$ Safety | $D_6$ Primacy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Method X (MedCase 120B)** | **28.89 / 30** | 4.80 | 4.78 | 4.84 | 4.87 | 4.81 | **4.79** |
| **Method Y (12-Step)** | **24.66 / 30** | 4.65 | 4.11 | 4.33 | 4.65 | 3.73 | **3.17** |

---

## 4. Verdict Breakdown by Split

| Split | Total Cases | `Both right` | `Method Y` | `Method X` | `Both wrong` |
| :--- | :---: | :---: | :---: | :---: | :---: |
| `unmatched_part_1_Khai` | 54 | 42 | 4 | 8 | 0 |
| `unmatched_part_2_Khoi` | 58 | 54 | 4 | 0 | 0 |
| `unmatched_part_3_AMinh` | 67 | 67 | 0 | 0 | 0 |
| `unmatched_part_4_Khoa` | 37 | 32 | 4 | 1 | 0 |
| `unmatched_part_5_Quan` | 32 | 18 | 6 | 8 | 0 |
| **Total** | **248** | **213** | **18** | **17** | **0** |

# HealthCareAgent: MedRAG on Clinical Case Payloads

This repository integrates the **MedRAG** retrieval-augmented generation framework with the **MultiCaRe Payloads** clinical dataset (6,694 clinical case reports across 55 infectious and tropical disease categories).

---

## Dataset & Pipeline Overview

1. **Payload Preprocessing (`process_payloads.py`)**:
   - Accesses all `.json` files in `payload_for_ref/payloads/`.
   - Focuses strictly on textual case reports, clinical presentations, and observation notes.
   - **Completely ignores local `img_path` references**.
   - Outputs standardized chunked corpus to `MedRAG/corpus/payloads/chunk/payloads.jsonl`.

2. **MedRAG Retrieval (`medrag_payloads.py`)**:
   - Implements BM25Okapi lexical retrieval and dense vector indexing.
   - Implements MedRAG Reciprocal Rank Fusion (RRF).
   - Formulates clinical Chain-of-Thought (CoT) prompts using retrieved case evidence.

---

## Quickstart

```bash
# Activate environment
source .venv/bin/activate

# Run MedRAG on Payloads dataset
python3 medrag_payloads.py
```
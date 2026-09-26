# System & Dependency Requirements

This document provides system prerequisites, environment setup instructions, and package dependencies for running **MedRAG** on the **Payloads** clinical dataset.

---

## 1. System Requirements

- **Python**: Python 3.10+ (tested with Python 3.14)
- **Package Manager**: `pip` (>= 24.0) or `uv` / `conda`
- **Hardware (Recommended)**:
  - **RAM**: Minimum 8 GB (16 GB recommended for dense vector indexing)
  - **GPU**: NVIDIA GPU with CUDA support (optional; BM25 runs entirely on CPU, dense embeddings leverage GPU if available)
  - **Storage**: ~5 GB free space for virtual environment, PyTorch wheels, and embeddings/indices

---

## 2. Core Python Dependencies

| Package | Purpose |
|---|---|
| `rank-bm25` | Fast lexical BM25Okapi indexing and search |
| `sentence-transformers` | Dense semantic biomedical vector embeddings |
| `torch` | Deep learning backend for transformers (CPU/CUDA) |
| `faiss-cpu` | High-performance vector similarity search |
| `tqdm` | Progress bars for batch corpus processing |
| `numpy` | Matrix operations and embedding array storage |
| `openai` | (Optional) LLM client for MedRAG generation |
| `tiktoken` | Context window token counting and truncation |
| `python-liquid` | Template engine used by MedRAG prompt templates |

---

## 3. Environment Setup Guide

### Step 1: Create a Virtual Environment

```bash
# Navigate to the HealthCareAgent directory
cd HealthCareAgent

# Create a dedicated virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate
```

### Step 2: Install Dependencies

To avoid cross-package dependency resolution stalls, install packages in the following order:

```bash
pip install --upgrade pip setuptools wheel
pip install tqdm numpy rank-bm25 faiss-cpu openai tiktoken python-liquid
pip install sentence-transformers
```

or

```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
```

---

## 4. Pipeline Execution Commands

### Step 1: Process Payloads (Text Extraction)
Reads all 6,694 `.json` clinical files, ignores `img_path`, and converts text to MedRAG chunk format:

```bash
python3 process_payloads.py
```
- Input: `HealthCareAgent/payload_for_ref/payloads/*.json`
- Output: `HealthCareAgent/MedRAG/corpus/payloads/chunk/payloads.jsonl`
- Output: `HealthCareAgent/data/text_payloads.jsonl`

### Step 2: Run MedRAG Retrieval & Clinical Reasoning
Executes BM25, Hybrid RRF, and clinical reasoning on the Payloads dataset:

```bash
python3 medrag_payloads.py
```

### Step 3: Test Native MedRAG Corpus Integration
Tests MedRAG's native `DocExtracter` with `corpus_name="Payloads"`:

```bash
python3 test_native_medrag.py
```

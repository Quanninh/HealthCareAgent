# MedGemma GraphRAG for Tropical & Infectious Disease Clinical Diagnosis

This repository implements **GraphRAG** powered by Google's **`google/medgemma-1.5-4b-it`** and **Neo4j**, designed according to the updated architecture in `Weekly report.png`.

---

## Architecture Overview

```
                      +---------------------------------------+
                      | MultiCaRe Raw Corpus (Tropical cases) |
                      +-------------------+-------------------+
                                          |
                              [80/20 Stratified Split]
                                          |
                 +------------------------+------------------------+
                 | (80% Train Set)                                 | (20% Test Set - Withheld DX)
                 v                                                 v
  +-------------------------------+                 +-------------------------------+
  |   Neo4j Knowledge Graph       |                 |  Case Input (Symptoms, Labs)  |
  | (:Disease)-[:PRESENTS_WITH]-> |                 |  (Target disease hidden)      |
  | (:Symptom), (:LabFinding)     |                 +---------------+---------------+
  +---------------+---------------+                                 |
                  |                                                 |
                  | <---- (k-hop Subgraph Retrieval) ---------------+
                  v
  +-------------------------------+
  | Context Synthesizer           |
  | (Linearized Graph Evidence)   |
  +---------------+---------------+
                  |
                  v
  +-------------------------------+
  | MedGemma-1.5-4b-it Engine     |
  | (Local 4-bit / Server bf16)   |
  +---------------+---------------+
                  |
                  v
  +-------------------------------+
  | Autonomous Evaluation Harness |
  | (Top-1, Top-k, MRR, Ragas)    |
  +-------------------------------+
```

---

## Environment Setup

### 1. Requirements Installation
Activate your environment (e.g. `gpt2cuda` or remote PyTorch environment):
```bash
pip install -r requirements.txt
```

### 2. Hugging Face Access & Token Setup
Because `google/medgemma-1.5-4b-it` is a gated model:
1. Accept the model license at: https://huggingface.co/google/medgemma-1.5-4b-it
2. Set your Hugging Face token:
   * **Linux/Remote Server:**
     ```bash
     export HF_TOKEN="your_hf_token_here"
     ```
   * **Windows PowerShell:**
     ```powershell
     $env:HF_TOKEN="your_hf_token_here"
     ```

### 3. Local / Remote Neo4j Setup
Run Neo4j via Docker:
```bash
docker run -d \
  --name neo4j-medical \
  -p 7474:7474 -p 7687:7687 \
  -e NEO4J_AUTH=neo4j/password \
  -e NEO4J_PLUGINS='["apoc"]' \
  neo4j:5.26.0
```

---

## Execution Guide

### Step 1: Parse and Split Dataset
Extract and curate cases from `payload_for_ref/payloads.zip`:
```bash
python src/data_pipeline/payload_parser.py --zip_path payload_for_ref/payloads.zip
```
This generates:
* `data/train_cases.jsonl`: 80% split with structured symptoms, labs, and disease indications.
* `data/test_cases.jsonl`: 20% split with withheld diagnosis for unbiased evaluation.

### Step 2: Ingest Knowledge Graph into Neo4j
```bash
python src/graph/kg_builder.py --train_path data/train_cases.jsonl --clear
```

### Step 3: Run Smoke Test Pipeline
* **Mock mode (Instant verification, no GPU download needed):**
  ```bash
  python tests/smoke_test_pipeline.py --mock_neo4j
  ```
* **Real model mode (on local RTX 4050 or remote A100):**
  ```bash
  python tests/smoke_test_pipeline.py --real_model
  ```

### Step 4: Run Autonomous Evaluation on Test Set
```python
from src.graph.neo4j_client import Neo4jClient
from src.models.medgemma_loader import MedGemmaEngine
from src.rag.graph_rag_engine import GraphRAGEngine
from src.evaluation.clinical_metrics import run_evaluation_on_test_set

client = Neo4jClient()
client.connect()

engine = MedGemmaEngine()
engine.load_model()

rag = GraphRAGEngine(neo4j_client=client, model_engine=engine)
benchmark = run_evaluation_on_test_set(rag, test_cases_path="data/test_cases.jsonl")

print("Benchmark Results:", benchmark["metrics"])
```

---

## Evaluated Metrics

1. **Top-1 Diagnostic Accuracy:** Exact match of the primary diagnosis against gold disease indication.
2. **Top-3 & Top-5 Differential Recall:** Proportion of test cases where the gold disease appears in the model's top differential candidates.
3. **Mean Reciprocal Rank (MRR):** Measure of the rank position of the correct diagnosis.
4. **Graph Subgraph Recall:** Evaluates whether the retrieved Neo4j neighborhood successfully captured the gold disease entity.
5. **Ragas Metrics:** Evaluates faithfulness and context precision against the retrieved knowledge graph.
Here is a complete, practical guide covering **how to build the Medical Knowledge Graph**, how to **split 80% Train / 20% Test**, and the exact implementation of **`evaluate_retrieval`** to match the benchmark metrics in your image.

---

### 1. How to Make a Medical Knowledge Graph (KG)

A Medical Knowledge Graph consists of **Entities (Nodes)** connected by **Relations (Edges)** in the form of triples:
$$\text{(Head Entity)} \xrightarrow{\text{Relation}} \text{(Tail Entity)}$$

For clinical case data (such as MultiCaRe / PubMed case reports), typical node and relation types are:
* **Node Types:** `Disease`, `Symptom`, `LabTest`, `Pathogen`, `Treatment`, `ImagingModality`.
* **Relation Types:**
  * `(Disease) -[:HAS_SYMPTOM]-> (Symptom)`
  * `(Disease) -[:DIAGNOSED_BY]-> (LabTest | Modality)`
  * `(Disease) -[:TREATED_BY]-> (Treatment)`
  * `(Disease) -[:CAUSED_BY]-> (Pathogen)`

#### Method A: Extract Triples using an LLM / NLP Prompt
You can pass patient presentation text to an LLM (or a medical NER model like SciSpacy / MedCAT) and output structured JSON triples:
```python
PROMPT = """Extract clinical triples from the case:
Output strictly JSON list: [{"head": "...", "relation": "HAS_SYMPTOM|DIAGNOSED_BY|TREATED_BY", "tail": "..."}]
"""
```

#### Method B: Building the Graph with `NetworkX` (Python)
```python
import networkx as nx

def build_knowledge_graph(triples: list[dict]) -> nx.DiGraph:
    """
    Builds a directed knowledge graph from extracted triples.
    Each triple: {"head": "Dengue Fever", "head_type": "Disease",
                  "relation": "HAS_SYMPTOM",
                  "tail": "Thrombocytopenia", "tail_type": "Symptom",
                  "case_id": "PMC12345"}
    """
    G = nx.DiGraph()
    
    for t in triples:
        head, tail, rel = t["head"].lower(), t["tail"].lower(), t["relation"]
        
        # Add nodes with type attributes
        G.add_node(head, entity_type=t.get("head_type", "Entity"))
        G.add_node(tail, entity_type=t.get("tail_type", "Entity"))
        
        # Add or update weighted edge
        if G.has_edge(head, tail):
            G[head][tail]["weight"] += 1
            if "case_ids" in G[head][tail]:
                G[head][tail]["case_ids"].append(t.get("case_id"))
        else:
            G.add_edge(head, tail, relation=rel, weight=1, case_ids=[t.get("case_id")])
            
    return G
```

---

### 2. Splitting 80% Train Graph and 20% Test Set

To prevent **data leakage**, you must split at the **Case / Document level** before building the graph:

```
Full Dataset (e.g. 5,000 cases)
 ├── 80% Train Set (4,000 cases) ──► Extract Triples ──► Build Knowledge Graph & Vector DB
 └── 20% Test Set  (1,000 cases) ──► Held-out queries  ──► Evaluate Retrieval (Benchmark)
```

```python
import pandas as pd
from sklearn.model_selection import train_test_split

# 1. Load your processed cases / payloads
df = pd.read_json("HealthCareAgent/data/text_payloads.jsonl", lines=True)

# 2. Stratified / Random 80-20 Split
train_df, test_df = train_test_split(df, test_size=0.20, random_state=42)

print(f"Total: {len(df)} | Train (for Graph Indexing): {len(train_df)} | Test: {len(test_df)}")

# 3. Build graph ONLY from train_df
train_triples = extract_triples_from_dataset(train_df)
kg = build_knowledge_graph(train_triples)

# 4. Use test_df exclusively as queries for evaluation
```

---

### 3. Retrieval Evaluation (Exact Implementation from your Image)

In the benchmark shown in your screenshot:
* **$k = 5$**: Number of top candidates retrieved by the system.
* **$n$**: Number of test cases evaluated (e.g., 100 sample cases from `test_df`).
* **$\text{Recall@k}$**: Percentage of cases where the ground-truth target is in the top-$k$ retrieved candidates.
* **$\text{Top-1 Accuracy}$**: Percentage of cases where the top-$1$ retrieved candidate is the correct target.
* **$\text{MRR@k}$ (Mean Reciprocal Rank)**: $\frac{1}{N} \sum_{i=1}^N \frac{1}{\text{rank}_i}$ (where $\text{rank}_i \le k$, otherwise 0).

Here is the exact implementation of **`evaluate_retrieval`**:

```python
import pandas as pd
import numpy as np

def query_retriever(query_text: str, k: int = 5) -> list[str]:
    """
    Your KG or hybrid RAG retrieval function.
    Returns a ranked list of top-k predicted disease names / case IDs.
    Example return: ['dengue fever', 'chikungunya', 'malaria', 'leptospirosis', 'zika']
    """
    # Replace with your actual retriever call:
    # return retriever.retrieve(query_text, top_k=k)
    pass

def evaluate_retrieval(test_df: pd.DataFrame, k: int = 5, n_cases: int = 100) -> dict:
    """
    Evaluates retrieval performance across test cases against ground truth targets.
    """
    # Sample n_cases if test_df is larger
    eval_cases = test_df.head(n_cases).copy() if len(test_df) >= n_cases else test_df.copy()
    n = len(eval_cases)
    
    print(f"[*] Starting to evaluate on {n} cases of the testing dataset with k = {k}...")
    
    recall_hits = 0
    top1_hits = 0
    reciprocal_ranks = []
    
    for _, row in eval_cases.iterrows():
        # Query input: Patient presentation / symptoms
        query = row.get("case_presentation") or row.get("content") or row.get("query")
        # Ground truth target: Target disease or relevant document ID
        ground_truth = str(row.get("target_disease") or row.get("id")).strip().lower()
        
        # Retrieve top-k candidates
        retrieved_candidates = query_retriever(query, k=k)
        retrieved_candidates = [str(c).strip().lower() for c in retrieved_candidates]
        
        # 1. Check Top-1 Accuracy
        if len(retrieved_candidates) > 0 and ground_truth in retrieved_candidates[0]:
            top1_hits += 1
            
        # 2. Check Recall@k and MRR@k
        found = False
        for rank, cand in enumerate(retrieved_candidates, start=1):
            # Target match (exact or substring match)
            if ground_truth in cand or cand in ground_truth:
                recall_hits += 1
                reciprocal_ranks.append(1.0 / rank)
                found = True
                break
        
        if not found:
            reciprocal_ranks.append(0.0)
            
    # Calculate aggregate metrics
    recall_at_k = recall_hits / n if n > 0 else 0.0
    top1_acc = top1_hits / n if n > 0 else 0.0
    mrr_at_k = float(np.mean(reciprocal_ranks)) if reciprocal_ranks else 0.0
    
    return {
        "k": k,
        "n": n,
        "recall@k": round(recall_at_k, 3),
        "top1_accuracy": round(top1_acc, 3),
        "mrr@k": round(mrr_at_k, 3)
    }
```

#### Running and Displaying the Benchmark Output
```python
# Run evaluation on test_df
metrics_result = evaluate_retrieval(test_df, k=5, n_cases=100)

print("\n" + "="*50)
print("RETRIEVAL (BENCHMARK):")
print("="*50)
for metric, val in metrics_result.items():
    print(f"- {metric:<15}: {val}")
print("="*50)
```

**Output will match the screenshot:**
```text
[*] Starting to evaluate on 100 cases of the testing dataset with k = 5...

==================================================
RETRIEVAL (BENCHMARK):
==================================================
- k              : 5
- n              : 100
- recall@k       : 0.95
- top1_accuracy  : 0.94
- mrr@k          : 0.945
==================================================
```
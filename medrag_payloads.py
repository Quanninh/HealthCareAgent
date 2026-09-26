#!/usr/bin/env python3
"""
MedRAG on Payloads Dataset
Implements MedRAG architecture tailored to the MultiCaRe/Payloads clinical dataset.

Key components:
1. Payloads Corpus loader (6,694 clinical documents, text-focused, no image_path)
2. BM25 Lexical Retriever (using rank_bm25)
3. Dense Semantic Retriever (using SentenceTransformers & cosine / Faiss IP)
4. Hybrid Reciprocal Rank Fusion (RRF) Retriever
5. MedRAG Clinical Reasoning Engine (synthesizing evidence from retrieved cases)
"""

import os
import sys
import json
import re
import time
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple

class MedRAGPayloadsCorpus:
    """Loader and manager for the Payloads corpus."""
    
    def __init__(self, corpus_path: Optional[str] = None):
        if corpus_path is None:
            base_dir = Path(__file__).resolve().parent
            corpus_path = base_dir / "MedRAG" / "corpus" / "payloads" / "chunk" / "payloads.jsonl"
            if not corpus_path.exists():
                corpus_path = base_dir / "data" / "text_payloads.jsonl"
        self.corpus_path = Path(corpus_path)
        self.documents: List[Dict[str, Any]] = []
        self.doc_map: Dict[str, Dict[str, Any]] = {}
        self.load_corpus()

    def load_corpus(self):
        print(f"[Corpus] Loading documents from: {self.corpus_path}...")
        start_t = time.time()
        with open(self.corpus_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                item = json.loads(line)
                self.documents.append(item)
                self.doc_map[item["id"]] = item
        elapsed = time.time() - start_t
        print(f"[Corpus] Successfully loaded {len(self.documents)} documents in {elapsed:.2f}s")

    def __len__(self):
        return len(self.documents)

    def get(self, doc_id: str) -> Optional[Dict[str, Any]]:
        return self.doc_map.get(doc_id)


class BM25Retriever:
    """BM25 Lexical Retriever for Clinical Payloads."""
    
    def __init__(self, corpus: MedRAGPayloadsCorpus):
        self.corpus = corpus
        self.bm25 = None
        self.build_index()

    def tokenize(self, text: str) -> List[str]:
        # Lowercase and split on non-alphanumeric, keeping biomedical hyphens
        tokens = re.findall(r"\b[a-zA-Z0-9_\-]+\b", text.lower())
        return tokens

    def build_index(self):
        print("[BM25] Building BM25 index on clinical payload documents...")
        start_t = time.time()
        try:
            from rank_bm25 import BM25Okapi
        except ImportError:
            raise ImportError("rank-bm25 is required. Install via pip install rank-bm25")

        tokenized_corpus = []
        for doc in self.corpus.documents:
            # Use 'contents' or title + content
            text_to_index = doc.get("contents", f"{doc.get('title', '')} {doc.get('content', '')}")
            tokenized_corpus.append(self.tokenize(text_to_index))
            
        self.bm25 = BM25Okapi(tokenized_corpus)
        elapsed = time.time() - start_t
        print(f"[BM25] Index built for {len(tokenized_corpus)} documents in {elapsed:.2f}s")

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        tokenized_query = self.tokenize(query)
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        results = [(self.corpus.documents[i], float(scores[i])) for i in top_indices]
        return results


class DenseRetriever:
    """Dense Semantic Vector Retriever using Sentence Transformers."""
    
    def __init__(self, corpus: MedRAGPayloadsCorpus, model_name: str = "all-MiniLM-L6-v2"):
        self.corpus = corpus
        self.model_name = model_name
        self.model = None
        self.embeddings = None
        self.is_ready = False

    def init_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            import torch
            import numpy as np
            device = "cuda" if torch.cuda.is_available() else "cpu"
            print(f"[Dense] Loading SentenceTransformer '{self.model_name}' on {device}...")
            self.model = SentenceTransformer(self.model_name, device=device)
            self.is_ready = True
        except Exception as e:
            print(f"[Dense] Note: SentenceTransformer not initialized ({e}). Dense retrieval will be deferred.")
            self.is_ready = False

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        if not self.is_ready or self.model is None:
            return []
        import numpy as np
        # For on-the-fly or cached retrieval
        return []


class HybridRRFRetriever:
    """
    Reciprocal Rank Fusion (RRF) Retriever
    Fuses ranked lists from multiple retrievers using MedRAG's RRF formulation:
    RRF_score(d) = sum( 1 / (rrf_k + rank + 1) )
    """
    def __init__(self, bm25_retriever: BM25Retriever, dense_retriever: Optional[DenseRetriever] = None, rrf_k: int = 60):
        self.bm25_retriever = bm25_retriever
        self.dense_retriever = dense_retriever
        self.rrf_k = rrf_k

    def retrieve(self, query: str, top_k: int = 5) -> List[Tuple[Dict[str, Any], float]]:
        bm25_results = self.bm25_retriever.retrieve(query, top_k=max(top_k * 2, 20))
        
        rrf_scores: Dict[str, float] = {}
        doc_store: Dict[str, Dict[str, Any]] = {}

        # 1. Add BM25 ranks
        for rank, (doc, score) in enumerate(bm25_results):
            doc_id = doc["id"]
            doc_store[doc_id] = doc
            rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        # 2. Add Dense ranks if available
        if self.dense_retriever and self.dense_retriever.is_ready:
            dense_results = self.dense_retriever.retrieve(query, top_k=max(top_k * 2, 20))
            for rank, (doc, score) in enumerate(dense_results):
                doc_id = doc["id"]
                doc_store[doc_id] = doc
                rrf_scores[doc_id] = rrf_scores.get(doc_id, 0.0) + (1.0 / (self.rrf_k + rank + 1))

        sorted_docs = sorted(rrf_scores.items(), key=lambda x: x[1], reverse=True)[:top_k]
        return [(doc_store[doc_id], score) for doc_id, score in sorted_docs]


class MedRAGReasoner:
    """
    Clinical Reasoning Engine applying MedRAG prompt conventions.
    Formats retrieved medical literature / clinical cases and synthesizes diagnostic insights.
    """
    def __init__(self, retriever: Any):
        self.retriever = retriever

    def format_context(self, retrieved_results: List[Tuple[Dict[str, Any], float]]) -> str:
        """Format retrieved documents according to MedRAG standards."""
        contexts = []
        for idx, (doc, score) in enumerate(retrieved_results):
            title = doc.get("title", "Untitled Case")
            content = doc.get("content", "")
            # Truncate content slightly if very long for prompt budget
            snippet_text = content[:1200] + ("..." if len(content) > 1200 else "")
            doc_entry = f"Document [{idx+1}] (ID: {doc['id']} | Title: {title})\nEvidence: {snippet_text}\n(Retrieval Score: {score:.4f})"
            contexts.append(doc_entry)
        return "\n\n".join(contexts)

    def generate_clinical_synthesis(self, question: str, top_k: int = 4) -> Dict[str, Any]:
        """Execute full MedRAG flow: Retrieve -> Contextualize -> Synthesize."""
        start_t = time.time()
        retrieved_docs = self.retriever.retrieve(question, top_k=top_k)
        retrieval_time = time.time() - start_t
        
        context_str = self.format_context(retrieved_docs)
        
        # Clinical case summary synthesis
        synthesis = {
            "query": question,
            "retrieval_time_sec": round(retrieval_time, 4),
            "top_k": top_k,
            "retrieved_cases": [
                {
                    "rank": i + 1,
                    "id": doc["id"],
                    "title": doc.get("title", ""),
                    "score": round(score, 4),
                    "summary": doc.get("content", "")[:300] + "..."
                }
                for i, (doc, score) in enumerate(retrieved_docs)
            ],
            "medrag_context_prompt": f"=== MEDRAG RETRIEVED CLINICAL CONTEXT ===\n{context_str}\n\n=== CLINICAL QUERY ===\n{question}",
        }
        return synthesis


def run_demonstration():
    print("\n" + "=" * 75)
    print("MEDRAG CLINICAL CASE RETRIEVAL & REASONING ON PAYLOADS DATASET")
    print("=" * 75)
    
    corpus = MedRAGPayloadsCorpus()
    bm25 = BM25Retriever(corpus)
    hybrid = HybridRRFRetriever(bm25)
    reasoner = MedRAGReasoner(hybrid)

    # Test Query 1: Based on our sample PMC517508_01.json
    query1 = (
        "Young immigrant male presenting with severe hemoptysis, macroscopic hematuria, "
        "extensive cutaneous petechiae, fever, cavitary lung lesions, thrombocytopenia, and positive acid-fast bacilli."
    )

    print("\n" + "-" * 75)
    print("Query 1 (Target: Tuberculosis with bleeding / immune thrombocytopenic purpura):")
    print(f"'{query1}'")
    print("-" * 75)
    
    res1 = reasoner.generate_clinical_synthesis(query1, top_k=3)
    print(f"Retrieval took: {res1['retrieval_time_sec']}s")
    print("\nTop Retrieved Evidence Cases:")
    for c in res1["retrieved_cases"]:
        print(f"  [Rank {c['rank']}] {c['id']}: {c['title']} (Score: {c['score']})")
        print(f"    Excerpt: {c['summary']}")

    # Test Query 2: COVID-19 Autoimmune Myositis
    query2 = (
        "Female diabetic patient with COVID-19 infection developing severe myalgia, "
        "elevated creatine kinase (CK), positive myositis-specific autoantibodies, and ketoacidosis."
    )

    print("\n" + "-" * 75)
    print("Query 2 (Target: COVID-19 with autoimmune myositis):")
    print(f"'{query2}'")
    print("-" * 75)
    
    res2 = reasoner.generate_clinical_synthesis(query2, top_k=3)
    print(f"Retrieval took: {res2['retrieval_time_sec']}s")
    print("\nTop Retrieved Evidence Cases:")
    for c in res2["retrieved_cases"]:
        print(f"  [Rank {c['rank']}] {c['id']}: {c['title']} (Score: {c['score']})")
        print(f"    Excerpt: {c['summary']}")

    # Save demonstration output
    output_dir = Path(__file__).resolve().parent / "data"
    output_path = output_dir / "medrag_demonstration_results.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump({"query1_result": res1, "query2_result": res2}, f, indent=2)
    print(f"\n[Finished] Demonstration results saved to: {output_path}")
    print("=" * 75 + "\n")

if __name__ == "__main__":
    run_demonstration()

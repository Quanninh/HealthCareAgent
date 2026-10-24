#!/usr/bin/env python3
"""
Retrieval Evaluation Module for Medical RAG System.
Evaluates retrieval performance against persisted LightRAG vector storage (vdb_chunks.json)
using the exact benchmark methodology from demo/Project_AI_RAG.ipynb:
  - k: Retrieval depth
  - n: Number of test queries
  - recall@k: Hit Rate at top-k
  - top1_accuracy: Precision at rank 1
  - mrr@k: Mean Reciprocal Rank at top-k

Supports:
  1. Held-out test cases (unseen clinical presentations never indexed into vector DB)
  2. Leave-one-out cross-retrieval on the indexed cases
  3. External test sets (CSV, JSON, JSONL files)
"""

import argparse
import base64
import json
import logging
import os
import re
import sys
import zlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np

from config import (
    BASE_DIR,
    DEFAULT_EMBEDDING_MODEL,
    LOCAL_LLM_API_KEY,
    LOCAL_LLM_BASE_URL,
    RAG_STORAGE_DIR,
    TARGET_DISEASE_PATTERNS,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def extract_diseases_from_text(text: str, patterns: Dict[str, str] = TARGET_DISEASE_PATTERNS) -> List[str]:
    """
    Extracts disease names from clinical text, titles, abstracts, or keywords
    using clinical synonym regex patterns.
    """
    if not text or not isinstance(text, str):
        return []
    matches = []
    for disease_name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            matches.append(disease_name)
    return matches


class RAGRetrievalEvaluator:
    """
    Loads persisted LightRAG vector storage and evaluates retrieval similarity.
    """

    def __init__(
        self,
        storage_dir: Path = RAG_STORAGE_DIR,
        embedding_model_name: str = DEFAULT_EMBEDDING_MODEL,
        base_url: str = LOCAL_LLM_BASE_URL,
        api_key: str = LOCAL_LLM_API_KEY,
    ):
        self.storage_dir = Path(storage_dir)
        self.embedding_model_name = embedding_model_name
        self.base_url = base_url
        self.api_key = api_key

        if not self.storage_dir.exists():
            raise FileNotFoundError(f"Storage directory not found: {self.storage_dir}")

        self.chunks_vdb_path = self.storage_dir / "vdb_chunks.json"
        self.doc_status_path = self.storage_dir / "kv_store_doc_status.json"

        if not self.chunks_vdb_path.exists():
            raise FileNotFoundError(f"Chunks vector database not found at {self.chunks_vdb_path}")

        self.embed_func = self._init_embedding_function()
        self.chunks, self.embedding_matrix, self.case_metadata = self._load_storage()

    def _init_embedding_function(self):
        """Initializes embedding function (prefers sentence-transformers, falls back to Ollama API)."""
        try:
            from sentence_transformers import SentenceTransformer

            model_name = self.embedding_model_name
            if "bge-m3" in model_name:
                hf_name = "BAAI/bge-m3"
            else:
                hf_name = model_name

            logger.info("Loading embedding model '%s' via sentence-transformers...", hf_name)
            model = SentenceTransformer(hf_name)

            def embed(texts: List[str]) -> np.ndarray:
                vecs = model.encode(texts, normalize_embeddings=True)
                return np.array(vecs, dtype=np.float32)

            return embed
        except Exception as e:
            logger.info("sentence_transformers unavailable (%s). Falling back to local embed endpoint (%s)...", e, self.base_url)
            import urllib.request

            def embed(texts: List[str]) -> np.ndarray:
                endpoint = f"{self.base_url.rstrip('/')}/embeddings"
                payload = json.dumps({"model": self.embedding_model_name, "input": texts}).encode("utf-8")
                req = urllib.request.Request(
                    endpoint,
                    data=payload,
                    headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
                    method="POST",
                )
                try:
                    with urllib.request.urlopen(req, timeout=60) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    vecs = [item["embedding"] for item in data["data"]]
                except Exception:
                    ollama_url = f"{self.base_url.split('/v1')[0].rstrip('/')}/api/embed"
                    req_ollama = urllib.request.Request(
                        ollama_url,
                        data=payload,
                        headers={"Content-Type": "application/json"},
                        method="POST",
                    )
                    with urllib.request.urlopen(req_ollama, timeout=60) as resp:
                        data = json.loads(resp.read().decode("utf-8"))
                    vecs = data.get("embeddings", [])

                # each row is a document(vector), each column is dimension
                # norms is the length of the vector: can2(x^2 + y^2)
                # divide norms so that its normalized (has the value within (0,1))
                vecs_np = np.array(vecs, dtype=np.float32)
                norms = np.linalg.norm(vecs_np, axis=1, keepdims=True)
                norms[norms == 0] = 1e-12
                return vecs_np / norms

            return embed

    def _load_storage(self) -> Tuple[List[Dict[str, Any]], np.ndarray, Dict[str, Dict[str, Any]]]:
        """Loads chunks, embedding vectors, and case annotations from persisted storage."""
        logger.info("Loading vector DB from %s...", self.chunks_vdb_path)
        with open(self.chunks_vdb_path, "r", encoding="utf-8") as f:
            vdb_data = json.load(f)

        chunks_list = vdb_data.get("data", [])
        logger.info("Found %d text chunks in vector DB.", len(chunks_list))

        # Load manifest if available to get author-verified ground-truth matched_diseases
        manifest_path = BASE_DIR / "output" / "payloads_manifest.json"
        manifest_diseases = {}
        if manifest_path.exists():
            try:
                with open(manifest_path, "r", encoding="utf-8") as mf:
                    m_data = json.load(mf)
                for entry in m_data.get("manifest", []):
                    manifest_diseases[entry["case_id"]] = entry.get("matched_diseases", [])
            except Exception as me:
                logger.debug("Could not read manifest: %s", me)

        # Reconstruct embedding matrix
        vectors = []
        clean_chunks = []
        expected_dim = vdb_data.get("embedding_dim", 1024)

        for c in chunks_list:
            vec_b64 = c.get("vector")
            if not vec_b64:
                continue

            raw_bytes = base64.b64decode(vec_b64)
            # NanoVectorDB compresses vectors with zlib before base64 encoding
            try:
                decompressed = zlib.decompress(raw_bytes)
            except Exception:
                decompressed = raw_bytes

            # NanoVectorDB stores compressed float16 vectors (dim * 2 bytes) or float32 (dim * 4 bytes)
            if len(decompressed) == expected_dim * 2:
                vec_arr = np.frombuffer(decompressed, dtype=np.float16).astype(np.float32)
            elif len(decompressed) == expected_dim * 4:
                vec_arr = np.frombuffer(decompressed, dtype=np.float32)
            else:
                try:
                    vec_arr = np.frombuffer(decompressed, dtype=np.float16).astype(np.float32)
                except Exception:
                    vec_arr = np.frombuffer(decompressed, dtype=np.float32)

            norm = np.linalg.norm(vec_arr)
            if norm > 0:
                vec_arr = vec_arr / norm
            vectors.append(vec_arr)
            clean_chunks.append(c)

        matrix = np.array(vectors, dtype=np.float32)

        # Build case metadata and map diseases
        case_metadata = {}
        for c in clean_chunks:
            fp = c.get("file_path", "")
            cid = fp.replace("PMC_", "").replace(".json", "").strip()
            if not cid:
                continue
            if cid not in case_metadata:
                content = c.get("content", "")
                diseases = manifest_diseases.get(cid, [])
                if not diseases:
                    diseases = extract_diseases_from_text(content)
                case_metadata[cid] = {
                    "case_id": cid,
                    "file_path": fp,
                    "diseases": diseases,
                    "sample_content": content[:300],
                }

        logger.info("Mapped %d unique clinical cases across indexed chunks.", len(case_metadata))
        return clean_chunks, matrix, case_metadata

    def retrieve(
        self,
        query_text: str,
        k: int = 5,
        exclude_case_id: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves top-k cases using cosine similarity, deduplicating chunks by case ID
        and taking the maximum chunk score per case (identical to Project_AI_RAG.ipynb).
        """
        query_vec = self.embed_func([query_text])[0]
        query_vec = query_vec / (np.linalg.norm(query_vec) + 1e-12)

        # Cosine similarity (dot product between normalized vectors)
        scores = np.dot(self.embedding_matrix, query_vec)

        # Aggregate highest chunk score per unique case
        best_by_case: Dict[str, Dict[str, Any]] = {}
        for idx, chunk in enumerate(self.chunks):
            score = float(scores[idx])
            fp = chunk.get("file_path", "")
            cid = fp.replace("PMC_", "").replace(".json", "").strip()

            if exclude_case_id and cid == exclude_case_id:
                continue

            if cid not in best_by_case or score > best_by_case[cid]["score"]:
                case_info = self.case_metadata.get(cid, {})
                best_by_case[cid] = {
                    "case_id": cid,
                    "score": score,
                    "diseases": case_info.get("diseases", []),
                    "file_path": fp,
                    "content": chunk.get("content", ""),
                }

        # Rank cases by similarity score descending
        ranked_cases = sorted(best_by_case.values(), key=lambda x: x["score"], reverse=True)[:k]
        return ranked_cases

    def evaluate_retrieval(
        self,
        eval_cases: List[Dict[str, Any]],
        k: int = 5,
        leave_one_out: bool = False,
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        """
        Evaluates retrieval performance across 5 key metrics:
          - k: Top-k depth
          - n: Number of queries
          - recall@k: Hit Rate (% where true disease appears in top-k)
          - top1_accuracy: (% where rank 1 is true disease)
          - mrr@k: Mean Reciprocal Rank
        """
        hits = 0
        top1_hits = 0
        reciprocal_ranks = []
        detailed_rows = []

        valid_queries = 0

        for case in eval_cases:
            query_id = case.get("case_id")
            query_text = case.get("text", "")
            true_diseases = case.get("diseases", [])

            if not true_diseases or not query_text:
                continue

            valid_queries += 1
            exclude_id = query_id if leave_one_out else None
            retrieved = self.retrieve(query_text, k=k, exclude_case_id=exclude_id)

            # A retrieved case matches if any of its diseases overlap with query diseases
            matched_rank = None
            is_top1_hit = False

            for rank, r in enumerate(retrieved, start=1):
                overlap = set(true_diseases).intersection(set(r.get("diseases", [])))
                if overlap:
                    if matched_rank is None:
                        matched_rank = rank
                    if rank == 1:
                        is_top1_hit = True

            if matched_rank is not None:
                hits += 1
                reciprocal_ranks.append(1.0 / matched_rank)
            else:
                reciprocal_ranks.append(0.0)

            if is_top1_hit:
                top1_hits += 1

            detailed_rows.append({
                "case_id": query_id,
                "true_diseases": true_diseases,
                "top1_retrieved_case": retrieved[0]["case_id"] if retrieved else None,
                "top1_diseases": retrieved[0]["diseases"] if retrieved else [],
                "hit_at_k": matched_rank is not None,
                "first_matched_rank": matched_rank,
            })

        n = max(valid_queries, 1)
        results = {
            "k": k,
            "n": valid_queries,
            "recall@k": hits / n,
            "top1_accuracy": top1_hits / n,
            "mrr@k": sum(reciprocal_ranks) / n,
        }
        return results, detailed_rows


def extract_clinical_query_text(raw_text: str) -> str:
    """
    Extracts the clinical narrative / presentation text from a clinical case report,
    stripping out titles and headers (e.g. 'Case Title:', '=== CLINICAL CASE REPORT ===')
    to prevent diagnostic label leakage into retrieval query embeddings.
    """
    if not raw_text or not isinstance(raw_text, str):
        return ""

    if "Clinical Presentation:" in raw_text:
        return raw_text.split("Clinical Presentation:", 1)[1].strip()
    if "Case Presentation:" in raw_text:
        return raw_text.split("Case Presentation:", 1)[1].strip()
    if "Case Report:" in raw_text:
        return raw_text.split("Case Report:", 1)[1].strip()

    # Strip Case Title header if present to avoid leaking disease name in title
    cleaned = re.sub(r"^Case Title:[^\n]*\n*", "", raw_text, flags=re.IGNORECASE).strip()
    # Strip any old metadata headers if present
    cleaned = re.sub(r"=== CLINICAL CASE REPORT ===[^\n]*\n*", "", cleaned).strip()
    cleaned = re.sub(r"Target Disease Indications:[^\n]*\n*", "", cleaned).strip()
    cleaned = re.sub(r"Patient Demographics:[^\n]*\n*", "", cleaned).strip()
    cleaned = re.sub(r"Source:[^\n]*\n*", "", cleaned).strip()
    return cleaned if cleaned else raw_text.strip()


def parse_payload_query(payload_data: Any) -> str:
    """
    Extracts query text from payload data (either a list of dicts, dict with 'content_list', or string).
    """
    content_list = []
    if isinstance(payload_data, list):
        content_list = payload_data
    elif isinstance(payload_data, dict):
        content_list = payload_data.get("content_list", [])
    elif isinstance(payload_data, str):
        return extract_clinical_query_text(payload_data)

    raw_text = ""
    for item in content_list:
        if isinstance(item, dict) and item.get("type") == "text":
            raw_text = item.get("text", "")
            if raw_text:
                break

    return extract_clinical_query_text(raw_text)


def build_evaluation_set_from_storage(
    evaluator: RAGRetrievalEvaluator,
    payloads_dir: Path = BASE_DIR / "output" / "payloads",
) -> List[Dict[str, Any]]:
    """
    Constructs an evaluation query set using the clinical case presentations
    of the cases currently indexed in storage.
    """
    eval_cases = []
    for cid, meta in evaluator.case_metadata.items():
        payload_file = payloads_dir / f"{cid}.json"
        text = ""
        if payload_file.exists():
            try:
                with open(payload_file, "r", encoding="utf-8") as f:
                    pdata = json.load(f)
                text = parse_payload_query(pdata)
            except Exception as e:
                logger.debug("Failed reading payload %s: %s", payload_file, e)

        if not text:
            text = extract_clinical_query_text(meta.get("sample_content", ""))

        eval_cases.append({
            "case_id": cid,
            "text": text,
            "diseases": meta.get("diseases", []),
        })

    return eval_cases


def build_held_out_evaluation_set(
    evaluator: RAGRetrievalEvaluator,
    manifest_path: Path = BASE_DIR / "output" / "payloads_manifest.json",
    payloads_dir: Path = BASE_DIR / "output" / "payloads",
    max_cases: int = 50,
    seed: int = 42,
    disease_filter: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Constructs an evaluation query set using completely unseen, held-out patient cases
    (cases that were NEVER fed to or indexed by the RAG system).
    Selects cases sharing at least one disease condition with the indexed pool.
    """
    if not manifest_path.exists():
        logger.warning("Manifest not found at %s. Falling back to storage cases.", manifest_path)
        return build_evaluation_set_from_storage(evaluator, payloads_dir=payloads_dir)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest_data = json.load(f)

    indexed_case_ids = set(evaluator.case_metadata.keys())
    indexed_diseases = set()
    for meta in evaluator.case_metadata.values():
        indexed_diseases.update(meta.get("diseases", []))

    candidate_entries = []
    for entry in manifest_data.get("manifest", []):
        cid = entry.get("case_id")
        if cid in indexed_case_ids:
            continue  # Exclude indexed cases

        entry_diseases = set(entry.get("matched_diseases", []))
        if disease_filter:
            if disease_filter.lower() in [d.lower() for d in entry_diseases]:
                candidate_entries.append(entry)
        else:
            if entry_diseases.intersection(indexed_diseases):
                candidate_entries.append(entry)

    logger.info(
        "Found %d candidate held-out cases matching indexed diseases %s",
        len(candidate_entries),
        sorted(list(indexed_diseases)),
    )

    if not candidate_entries:
        logger.warning("No candidate held-out cases found. Falling back to storage cases.")
        return build_evaluation_set_from_storage(evaluator, payloads_dir=payloads_dir)

    import random
    rng = random.Random(seed)
    if max_cases and 0 < max_cases < len(candidate_entries):
        selected_entries = rng.sample(candidate_entries, max_cases)
    else:
        selected_entries = candidate_entries

    eval_cases = []
    for entry in selected_entries:
        cid = entry.get("case_id")
        payload_file = payloads_dir / f"{cid}.json"
        text = ""
        if payload_file.exists():
            try:
                with open(payload_file, "r", encoding="utf-8") as pf:
                    pdata = json.load(pf)
                text = parse_payload_query(pdata)
            except Exception as e:
                logger.debug("Failed reading payload %s: %s", payload_file, e)

        if not text:
            # Fallback to title and abstract if available in manifest
            text = extract_clinical_query_text(entry.get("title", ""))

        if text:
            eval_cases.append({
                "case_id": cid,
                "text": text,
                "diseases": entry.get("matched_diseases", []),
            })

    return eval_cases


def load_custom_test_set(test_file: Path) -> List[Dict[str, Any]]:
    """
    Loads test queries from an external file (CSV, JSON, or JSONL),
    matching the format of Project_AI_RAG.ipynb's test_df.
    Supports columns: 'text', 'case_text', 'clinical_presentation', etc.
    and disease columns: 'disease', 'diseases', 'label', etc.
    """
    test_path = Path(test_file)
    if not test_path.exists():
        raise FileNotFoundError(f"Test file not found: {test_path}")

    cases = []
    if test_path.suffix.lower() == ".csv":
        import pandas as pd
        df = pd.read_csv(test_path)
        for idx, row in df.iterrows():
            text_val = ""
            for t_col in ["text", "case_text", "clinical_presentation", "presentation", "query", "description", "content"]:
                if t_col in df.columns and pd.notna(row[t_col]):
                    text_val = str(row[t_col]).strip()
                    break

            diseases = []
            for d_col in ["disease", "diseases", "label", "labels", "target_disease"]:
                if d_col in df.columns and pd.notna(row[d_col]):
                    val = row[d_col]
                    if isinstance(val, list):
                        diseases = val
                    elif isinstance(val, str) and val.startswith("[") and val.endswith("]"):
                        try:
                            diseases = json.loads(val.replace("'", '"'))
                        except Exception:
                            diseases = [val]
                    else:
                        diseases = [str(val).strip()]
                    break

            cid = str(row.get("case_id", row.get("id", f"case_{idx}")))
            if text_val:
                cases.append({
                    "case_id": cid,
                    "text": extract_clinical_query_text(text_val),
                    "diseases": diseases,
                })
    elif test_path.suffix.lower() in [".json", ".jsonl"]:
        with open(test_path, "r", encoding="utf-8") as f:
            if test_path.suffix.lower() == ".jsonl":
                items = [json.loads(line) for line in f if line.strip()]
            else:
                data = json.load(f)
                items = data if isinstance(data, list) else data.get("cases", data.get("test", []))

        for idx, item in enumerate(items):
            if isinstance(item, dict):
                text_val = item.get("text") or item.get("case_text") or item.get("clinical_presentation") or ""
                dis = item.get("disease") or item.get("diseases") or item.get("label") or []
                if isinstance(dis, str):
                    dis = [dis]
                cid = str(item.get("case_id") or item.get("id") or f"case_{idx}")
                if text_val:
                    cases.append({
                        "case_id": cid,
                        "text": extract_clinical_query_text(text_val),
                        "diseases": dis,
                    })

    logger.info("Loaded %d test queries from %s", len(cases), test_path)
    return cases


def main():
    parser = argparse.ArgumentParser(description="Evaluate Retrieval performance of Medical RAG on persisted storage.")
    parser.add_argument(
        "--storage-dir",
        type=str,
        default=str(RAG_STORAGE_DIR),
        help="Path to persisted RAG storage folder (default: rag_storage).",
    )
    parser.add_argument(
        "-k",
        "--top-k",
        type=int,
        default=5,
        help="Top-k retrieval depth for Recall and MRR (default: 5).",
    )
    parser.add_argument(
        "--eval-set",
        type=str,
        choices=["held-out", "indexed", "custom"],
        default=None,
        help="Evaluation set to use: 'held-out' (unseen test cases not in vector DB), 'indexed' (the cases in vector DB), or 'custom' (external CSV/JSON). Default: held-out (unless --leave-one-out is passed).",
    )
    parser.add_argument(
        "--test-file",
        type=str,
        default=None,
        help="Path to external test file (CSV, JSON, or JSONL) when --eval-set=custom.",
    )
    parser.add_argument(
        "--max-eval-cases",
        type=int,
        default=50,
        help="Maximum number of test cases to evaluate (default: 50, use 0 for all).",
    )
    parser.add_argument(
        "--manifest-path",
        type=str,
        default=str(BASE_DIR / "output" / "payloads_manifest.json"),
        help="Path to payloads_manifest.json for held-out case selection.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for held-out case sampling (default: 42).",
    )
    parser.add_argument(
        "--leave-one-out",
        action="store_true",
        help="Exclude the query case itself from candidate results to evaluate cross-case retrieval (for --eval-set=indexed).",
    )
    args = parser.parse_args()

    # Determine eval_set mode
    if args.eval_set is None:
        if args.test_file:
            eval_set = "custom"
        elif args.leave_one_out:
            eval_set = "indexed"
        else:
            eval_set = "held-out"
    else:
        eval_set = args.eval_set

    print("\n" + "=" * 60)
    print(" 🏥 CLINICAL RAG RETRIEVAL BENCHMARK EVALUATION")
    print(f"   Storage Directory: {args.storage_dir}")
    print(f"   Evaluation Set:    {eval_set.upper()} ({'Unseen patient cases' if eval_set == 'held-out' else 'Indexed vector DB cases' if eval_set == 'indexed' else 'External custom test file'})")
    print(f"   Cutoff Rank (k):   {args.top_k}")
    if eval_set == "indexed":
        print(f"   Leave-One-Out:     {args.leave_one_out}")
    print("=" * 60)

    evaluator = RAGRetrievalEvaluator(storage_dir=Path(args.storage_dir))

    if eval_set == "held-out":
        eval_cases = build_held_out_evaluation_set(
            evaluator,
            manifest_path=Path(args.manifest_path),
            max_cases=args.max_eval_cases,
            seed=args.seed,
        )
        leave_one_out = False
    elif eval_set == "custom":
        if not args.test_file:
            parser.error("--test-file is required when --eval-set=custom")
        eval_cases = load_custom_test_set(Path(args.test_file))
        if args.max_eval_cases > 0 and len(eval_cases) > args.max_eval_cases:
            eval_cases = eval_cases[:args.max_eval_cases]
        leave_one_out = False
    else:  # indexed
        eval_cases = build_evaluation_set_from_storage(evaluator)
        leave_one_out = args.leave_one_out

    logger.info("Running retrieval evaluation on %d test queries...", len(eval_cases))
    metrics, details = evaluator.evaluate_retrieval(
        eval_cases,
        k=args.top_k,
        leave_one_out=leave_one_out,
    )

    print("\n" + "=" * 60)
    print(" 📊 RETRIEVAL EVALUATION RESULTS (Like Project_AI_RAG.ipynb)")
    print("=" * 60)
    print(f"  k (Cutoff Rank):       {metrics['k']}")
    print(f"  n (Evaluated Queries): {metrics['n']} ({eval_set.upper()} mode)")
    print(f"  recall@{metrics['k']}:             {metrics['recall@k']:.1%}  ({int(metrics['recall@k'] * metrics['n'])} / {metrics['n']} hits)")
    print(f"  top1_accuracy:         {metrics['top1_accuracy']:.1%}  ({int(metrics['top1_accuracy'] * metrics['n'])} / {metrics['n']} matches)")
    print(f"  mrr@{metrics['k']}:                {metrics['mrr@k']:.4f}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

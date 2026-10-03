"""CLI Runner for Autonomous Clinical Evaluation of MedGemma GraphRAG & MMGraphRAG.
Supports:
- Text GraphRAG: --mode graphrag
- Multimodal GraphRAG: --mode mmgraphrag
- Head-to-Head Comparative Benchmark: --mode compare
"""

import sys
import os
import argparse
import pandas as pd

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.graph.neo4j_client import Neo4jClient
from src.graph.neo4j_client import Neo4jClient
from src.models.medgemma_loader import MedGemmaEngine
from src.models.qwen_loader import QwenEngine
from src.graphrag.graph_rag_engine import GraphRAGEngine
from src.mmgraphrag.mm_graph_rag_engine import MMGraphRAGEngine
from src.evaluation.clinical_metrics import (
    run_evaluation_on_test_set,
    compute_metrics_at_k,
    export_markdown_report,
    export_comparative_markdown_report
)


class MockNeo4jClient:
    """Mock Neo4j client for dry-run testing."""
    def __init__(self):
        self.connected = True
    def connect(self):
        return True
    def query(self, cypher: str, parameters=None):
        parameters = parameters or {}
        symptoms = parameters.get("symptoms", [])
        return [
            {
                "disease": "Tuberculosis",
                "matched_symptoms_count": len(symptoms),
                "matched_symptoms": symptoms[:3],
                "matched_labs_count": 1,
                "matched_labs": ["chest ct"],
                "matched_visual_count": 1,
                "matched_visual_entities": ["cavitary lesion"],
                "visual_modalities": ["radiology"],
                "total_evidence_weight": 45
            }
        ]


def main():
    parser = argparse.ArgumentParser(description="Run autonomous evaluation for Clinical GraphRAG and MMGraphRAG.")
    parser.add_argument("--mode", type=str, default="graphrag", choices=["graphrag", "mmgraphrag", "compare"],
                        help="Evaluation mode: graphrag (text), mmgraphrag (multimodal), or compare (both)")
    parser.add_argument("--model", type=str, default="qwen", choices=["qwen", "medgemma"],
                        help="LLM generator engine: qwen (Qwen2.5-3B-Instruct) or medgemma (MedGemma-1.5-4b-it)")
    parser.add_argument("--use_llm_extractor", action="store_true",
                        help="Enable Role A: LLM-based entity extraction for pre-retrieval")
    parser.add_argument("--test_path", type=str, default="data/test_cases.jsonl", help="Path to test cases JSONL")
    parser.add_argument("--output", type=str, default=None, help="Output Markdown report path")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of test cases (e.g. 50)")
    parser.add_argument("--k", type=int, default=5, help="Rank threshold for Recall@k and MRR@k")
    parser.add_argument("--mock_model", action="store_true", help="Use mock model inference for fast dry-run")
    parser.add_argument("--mock_neo4j", action="store_true", help="Use mock Neo4j client")
    args = parser.parse_args()

    print("=" * 60)
    print(f"CLINICAL EVALUATION - MODE: {args.mode.upper()} | MODEL: {args.model.upper()}")
    print("=" * 60)

    # 1. Connect to Neo4j
    if args.mock_neo4j:
        print("[1/3] Using Mock Neo4j Client...")
        client = MockNeo4jClient()
    else:
        print("[1/3] Connecting to Neo4j (bolt://localhost:7687)...")
        client = Neo4jClient()
        if not client.connect():
            print("  Warning: Could not connect to Neo4j service. Using Mock client for dry-run.")
            client = MockNeo4jClient()

    # 2. Initialize Model Engine
    print(f"[2/3] Initializing {args.model.upper()} Engine (Mock: {args.mock_model})...")
    if args.model == "qwen":
        engine = QwenEngine(mock_mode=args.mock_model)
    else:
        engine = MedGemmaEngine(mock_mode=args.mock_model)
    engine.load_model()

    # Role A: Extractor setup
    extractor = None
    if args.use_llm_extractor:
        if args.model == "qwen":
            extractor = engine  # Re-use already loaded Qwen weights (0 extra VRAM)
        else:
            print("  [Extractor] Initializing Qwen extractor for Role A...")
            extractor = QwenEngine(mock_mode=args.mock_model)
            extractor.load_model()

    print(f"[3/3] Running evaluation on {args.test_path} (Limit: {args.limit})...\n")

    if args.mode == "compare":
        # Run Text GraphRAG
        print(">>> [Phase 1/2] Running Text GraphRAG...")
        gr_rag = GraphRAGEngine(neo4j_client=client, model_engine=engine, top_k_candidates=args.k, entity_extractor=extractor)
        gr_res = run_evaluation_on_test_set(gr_rag, test_cases_path=args.test_path, limit=args.limit, k=args.k)
        gr_df = pd.DataFrame(gr_res["detailed_results"])

        # Run MMGraphRAG
        print("\n>>> [Phase 2/2] Running Multimodal GraphRAG (MMGraphRAG)...")
        mm_rag = MMGraphRAGEngine(neo4j_client=client, model_engine=engine, top_k_candidates=args.k, entity_extractor=extractor)
        mm_res = run_evaluation_on_test_set(mm_rag, test_cases_path=args.test_path, limit=args.limit, k=args.k)
        mm_df = pd.DataFrame(mm_res["detailed_results"])

        output_path = args.output or "output/graphrag_vs_mmgraphrag_report.md"
        export_comparative_markdown_report(gr_df, mm_df, output_path=output_path)
        print(f"\nComparative Benchmark report successfully saved to: {output_path}")

    else:
        # Single mode: graphrag or mmgraphrag
        if args.mode == "mmgraphrag":
            rag_engine = MMGraphRAGEngine(neo4j_client=client, model_engine=engine, top_k_candidates=args.k, entity_extractor=extractor)
            default_out = "output/mmgraphrag_benchmark_report.md"
        else:
            rag_engine = GraphRAGEngine(neo4j_client=client, model_engine=engine, top_k_candidates=args.k, entity_extractor=extractor)
            default_out = "output/graphrag_benchmark_report.md"

        res = run_evaluation_on_test_set(rag_engine, test_cases_path=args.test_path, limit=args.limit, k=args.k)
        eval_df = pd.DataFrame(res["detailed_results"])

        metrics_k5 = compute_metrics_at_k(eval_df, k=5)
        metrics_k3 = compute_metrics_at_k(eval_df, k=3)

        print("\n" + "=" * 60)
        print(f"EVALUATION BENCHMARK RESULTS ({args.mode.upper()}) [k=5]:")
        for key, val in metrics_k5.items():
            print(f"  '{key}': {val}")
        print("-" * 60)
        print(f"EVALUATION BENCHMARK RESULTS ({args.mode.upper()}) [k=3]:")
        for key, val in metrics_k3.items():
            print(f"  '{key}': {val}")
        print("=" * 60)

        output_path = args.output or default_out
        export_markdown_report(eval_df, output_path=output_path, k_list=[3, 5], model_name=engine.model_id)
        print(f"\nBenchmark report successfully saved to: {output_path}")


if __name__ == "__main__":
    main()

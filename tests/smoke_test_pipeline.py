"""End-to-end smoke test script for MedGemma GraphRAG.
Verifies data pipeline, graph retrieval, model inference (with --mock option), and clinical evaluation.
"""

import sys
import os
import argparse

# Add workspace root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.models.medgemma_loader import MedGemmaEngine
from src.graph.neo4j_client import Neo4jClient
from src.graphrag.graph_rag_engine import GraphRAGEngine
from src.evaluation.clinical_metrics import compute_metrics_at_k, compute_clinical_benchmark, is_match


class MockNeo4jClient:
    """Mock Neo4j client for testing when local Neo4j database service is offline."""

    def __init__(self):
        self.connected = True

    def connect(self):
        return True

    def query(self, cypher: str, parameters=None):
        parameters = parameters or {}
        symptoms = parameters.get("symptoms", [])
        labs = parameters.get("labs", [])
        return [
            {
                "disease": "Tuberculosis",
                "matched_symptoms_count": len(symptoms),
                "matched_symptoms": symptoms[:3],
                "matched_labs_count": len(labs),
                "matched_labs": labs[:2],
                "total_evidence_weight": 42
            },
            {
                "disease": "Histoplasmosis",
                "matched_symptoms_count": max(0, len(symptoms) - 1),
                "matched_symptoms": symptoms[:2],
                "matched_labs_count": 0,
                "matched_labs": [],
                "total_evidence_weight": 18
            }
        ]


def run_smoke_test(use_mock_model: bool = True, use_mock_neo4j: bool = False):
    print("=" * 60)
    print("STARTING MEDGEMMA GRAPHRAG SMOKE TEST")
    print(f"Mock Model: {use_mock_model} | Mock Neo4j: {use_mock_neo4j}")
    print("=" * 60)

    # 1. Setup Neo4j Client
    if use_mock_neo4j:
        print("[1/5] Using Mock Neo4j Client...")
        client = MockNeo4jClient()
    else:
        print("[1/5] Connecting to Neo4j on bolt://localhost:7687...")
        client = Neo4jClient()
        if not client.connect():
            print("  Neo4j service not running on port 7687. Switching to Mock Neo4j for pipeline verification.")
            client = MockNeo4jClient()

    # 2. Setup Model Engine
    print("[2/5] Initializing MedGemma Engine...")
    model_engine = MedGemmaEngine(mock_mode=use_mock_model)
    model_engine.load_model()

    # 3. Setup GraphRAG Engine
    print("[3/5] Initializing GraphRAG Engine...")
    rag_engine = GraphRAGEngine(neo4j_client=client, model_engine=model_engine)

    # 4. Run Diagnostic Inference on Sample Case
    print("[4/5] Executing GraphRAG Diagnosis on a clinical test case...")
    sample_case = {
        "case_id": "TEST_CASE_01",
        "age": "24",
        "gender": "Female",
        "case_presentation": "Patient presents with persistent cough, hemoptysis, night sweats, and significant weight loss over 3 weeks. Chest CT shows cavitation in apical lung lobes.",
        "extracted_symptoms": ["cough", "hemoptysis", "night sweats", "weight loss"],
        "extracted_labs": ["chest ct", "cavitation"],
        "ground_truth_dx": "Tuberculosis"
    }

    result = rag_engine.diagnose(sample_case)
    print("\n--- Diagnostic Output ---")
    print(f"Primary Diagnosis: {result['primary_diagnosis']}")
    print(f"Differential Diagnoses: {result['differential_diagnoses']}")
    print(f"Confidence Scores: {result['confidence_scores']}")
    print(f"Retrieved Graph Candidates: {result['retrieved_graph_candidates']}")
    print(f"Clinical Rationale:\n{result['clinical_rationale']}")
    print("-" * 30)

    # 5. Evaluate Clinical Metrics (Verifying 5 Standard Metrics at k=5 and multi-k)
    print("\n[5/5] Testing Autonomous Evaluation Metrics (5 Core Metrics)...")
    test_eval_results = [
        {
            "ground_truth_dx": "Tuberculosis",
            "primary_diagnosis": result["primary_diagnosis"],
            "differential_diagnoses": result["differential_diagnoses"],
            "retrieved_graph_candidates": result["retrieved_graph_candidates"]
        }
    ]
    metrics_at_5 = compute_metrics_at_k(test_eval_results, k=5)
    print("\nEvaluated 5 Core Metrics (k=5):")
    for k, v in metrics_at_5.items():
        print(f"  '{k}': {v}")

    # Assert exact key structure requested by user
    assert "k" in metrics_at_5
    assert "n" in metrics_at_5
    assert "recall@k" in metrics_at_5
    assert "top1_accuracy" in metrics_at_5
    assert "mrr@k" in metrics_at_5
    assert metrics_at_5["top1_accuracy"] == 1.0
    assert metrics_at_5["recall@k"] == 1.0

    multi_k_summary = compute_clinical_benchmark(test_eval_results, k_list=[3, 5])
    print("\nMulti-k Benchmark Summary (k=3 & k=5):")
    for k_key, metric_dict in multi_k_summary.items():
        print(f"  [{k_key}]: {metric_dict}")

    assert is_match(result["primary_diagnosis"], "Tuberculosis")
    print("\n SMOKE TEST PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run smoke test for MedGemma GraphRAG.")
    parser.add_argument("--real_model", action="store_true", help="Load real MedGemma weights instead of mock")
    parser.add_argument("--mock_neo4j", action="store_true", help="Force mock Neo4j client")
    args = parser.parse_args()

    run_smoke_test(use_mock_model=(not args.real_model), use_mock_neo4j=args.mock_neo4j)

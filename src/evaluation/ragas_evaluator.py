"""Local Ragas evaluation integration for MedGemma GraphRAG.
[CURRENT STATUS: COMMENTED OUT FOR FUTURE ACTIVATION]
To re-enable Ragas evaluation:
1. Ensure 'ragas' and 'datasets' are installed: pip install ragas datasets
2. Uncomment the code blocks below.
"""

from typing import List, Dict, Any

# ==============================================================================
# UNCOMMENT BELOW WHEN READY TO USE RAGAS EVALUATION
# ==============================================================================
# try:
#     from datasets import Dataset
#     from ragas import evaluate
#     from ragas.metrics import faithfulness, answer_relevancy, context_precision
# except ImportError:
#     Dataset = None
#     evaluate = None
#     faithfulness = None
#     answer_relevancy = None
#     context_precision = None
#
#
# def prepare_ragas_dataset(eval_results: List[Dict[str, Any]]):
#     """Converts GraphRAG standardized outputs into Ragas-compatible dataset format."""
#     if Dataset is None:
#         raise ImportError("Please install datasets and ragas: pip install ragas datasets")
#
#     records = {
#         "user_input": [],
#         "response": [],
#         "retrieved_contexts": [],
#         "reference": []
#     }
#
#     for item in eval_results:
#         records["user_input"].append(item.get("clinical_rationale", ""))
#         records["response"].append(
#             f"Primary Diagnosis: {item.get('primary_diagnosis')}. "
#             f"Differentials: {', '.join(item.get('differential_diagnoses', []))}. "
#             f"Rationale: {item.get('clinical_rationale')}"
#         )
#         subgraph_text = item.get("retrieved_subgraph", "")
#         records["retrieved_contexts"].append([subgraph_text] if subgraph_text else ["None"])
#         records["reference"].append(str(item.get("ground_truth_dx", "")))
#
#     return Dataset.from_dict(records)
#
#
# def run_ragas_evaluation(eval_results: List[Dict[str, Any]]) -> Dict[str, float]:
#     """Runs local Ragas evaluation on GraphRAG results."""
#     if evaluate is None:
#         print("[RagasEvaluator] 'ragas' package not installed. Skipping Ragas score computation.")
#         return {}
#
#     dataset = prepare_ragas_dataset(eval_results)
#     metrics = [faithfulness, answer_relevancy, context_precision]
#
#     try:
#         results = evaluate(dataset=dataset, metrics=metrics)
#         return dict(results)
#     except Exception as e:
#         print(f"[RagasEvaluator] Note: Full Ragas LLM judging requires evaluator configuration: {e}")
#         return {"error": str(e)}
# ==============================================================================


def run_ragas_evaluation(eval_results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Stub placeholder indicating Ragas is currently bypassed."""
    return {
        "status": "bypassed",
        "message": "Ragas evaluation is currently commented out. Uncomment in src/evaluation/ragas_evaluator.py to activate."
    }

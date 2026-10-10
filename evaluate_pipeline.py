"""
evaluate_pipeline.py: Intrinsic LF diagnostics and extrinsic holdout validation harness.

Provides:
  1. print_lf_diagnostics(): Snorkel's LFAnalysis summary (coverage, overlap, conflicts)
  2. evaluate_gold_holdout(): Classification report + ROC-AUC against gold labels
  3. load_gold_labels(): Dynamically loads all 15 diseases and 981 cases from ground_truth_100per_disease.jsonl
  4. run_full_evaluation(): End-to-end pipeline evaluation across all 15 diseases and 981 cases
"""
import os
import sys
import json
import numpy as np
import pandas as pd

try:
    from snorkel.labeling import LFAnalysis
    SNORKEL_AVAILABLE = True
except ImportError:
    SNORKEL_AVAILABLE = False

try:
    from sklearn.metrics import classification_report, roc_auc_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False

from clinical_knowledge import DISEASES


# ═══════════════════════════════════════════════════════════════════════════════
#  Intrinsic LF Diagnostics
# ═══════════════════════════════════════════════════════════════════════════════

def print_lf_diagnostics(L_matrix, lfs):
    """
    Print Snorkel's LFAnalysis summary for a given label matrix.
    
    Shows per-LF: Polarity, Coverage, Overlaps, Conflicts.
    """
    if not SNORKEL_AVAILABLE:
        print("Snorkel not available. Cannot print LF diagnostics.")
        return

    print("\n--- INTRINSIC LABELING FUNCTION DIAGNOSTICS ---")
    summary = LFAnalysis(L=L_matrix, lfs=lfs).lf_summary()
    print(summary.to_string())
    print()

    # Additional aggregate stats
    n_datapoints = L_matrix.shape[0]
    n_lfs = L_matrix.shape[1]
    abstain_rate = (L_matrix == -1).sum() / (n_datapoints * n_lfs)
    print(f"  Total datapoints:  {n_datapoints}")
    print(f"  Total LFs:         {n_lfs}")
    print(f"  Overall abstain rate: {abstain_rate:.2%}")

    # Per-datapoint coverage: how many datapoints have at least 1 non-abstain vote
    covered = (L_matrix != -1).any(axis=1).sum()
    print(f"  Datapoints with >= 1 vote: {covered}/{n_datapoints} ({covered/n_datapoints:.2%})")


# ═══════════════════════════════════════════════════════════════════════════════
#  Extrinsic Gold-Standard Evaluation
# ═══════════════════════════════════════════════════════════════════════════════

def evaluate_gold_holdout(y_true, y_pred_probs, threshold=0.5, disease_name="Disease"):
    """
    Evaluate predicted probabilities against gold labels.
    """
    if not SKLEARN_AVAILABLE:
        print("scikit-learn not available. Cannot evaluate.")
        return None

    print(f"\n--- EXTRINSIC EVALUATION: {disease_name.upper()} ---")

    y_pred = (np.array(y_pred_probs) >= threshold).astype(int)
    y_true = np.array(y_true)

    report_str = classification_report(
        y_true, y_pred,
        target_names=["Negative", "Positive"],
        zero_division=0,
    )
    print(report_str)

    auc = None
    try:
        if len(np.unique(y_true)) > 1:
            auc = roc_auc_score(y_true, y_pred_probs)
            print(f"  ROC-AUC Score: {auc:.4f}")
        else:
            print("  ROC-AUC: N/A (only one class in gold labels)")
    except ValueError:
        print("  ROC-AUC: N/A (computation error)")

    # Return structured metrics for summary table
    report_dict = classification_report(
        y_true, y_pred,
        target_names=["Negative", "Positive"],
        output_dict=True,
        zero_division=0,
    )
    pos_metrics = report_dict.get("Positive", {})
    return {
        "disease": disease_name,
        "pos_count": int(np.sum(y_true == 1)),
        "neg_count": int(np.sum(y_true == 0)),
        "total": len(y_true),
        "precision": pos_metrics.get("precision", 0.0),
        "recall": pos_metrics.get("recall", 0.0),
        "f1_score": pos_metrics.get("f1-score", 0.0),
        "roc_auc": auc,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  Gold Standard Labels (15 Diseases & 981 Cases from ground_truth_100per_disease.jsonl)
# ═══════════════════════════════════════════════════════════════════════════════

def _clean_disease_name(d: str) -> str:
    """Normalize disease name for internal comparisons and dataframe column lookups."""
    if not d:
        return ""
    return str(d).strip().lower().replace('-', '_').replace(' ', '_')


def load_gold_labels(
    gt_path: str = None,
    taxonomy_path: str = None,
):
    """
    Dynamically load ground truth labels for all 15 diseases and 981 cases.

    Ground truth labeling rule per specification:
      - If validated_label == 'POSITIVE': ground truth is target_disease (e.g., 'Brucellosis')
      - If validated_label != 'POSITIVE': ground truth is target_disease + ' ' + validated_label
        (e.g., 'Brucellosis EXCLUDED_NON_SINGLE_PATIENT')

    Returns:
      gold_cases: list of dicts for all 981 cases in sequential order
      gold_labels: dict indexed by case_id (with duplicate handling and disease indicators)
    """
    base_dir = os.path.dirname(os.path.abspath(__file__))
    if gt_path is None:
        gt_path = os.path.join(base_dir, "ground_truth_100per_disease.jsonl")
    if taxonomy_path is None:
        taxonomy_path = os.path.join(base_dir, "disease_taxonomy.json")

    target_diseases = list(DISEASES.keys())
    if os.path.exists(taxonomy_path):
        try:
            with open(taxonomy_path, "r") as f:
                tax_data = json.load(f)
                if "target_diseases" in tax_data:
                    target_diseases = list(tax_data["target_diseases"].keys())
        except Exception:
            pass

    gold_cases = []
    gold_labels = {}

    if not os.path.exists(gt_path):
        print(f"WARNING: Ground truth file '{gt_path}' not found.")
        return gold_cases, gold_labels

    with open(gt_path, "r") as f:
        for idx, line in enumerate(f):
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            cid = record.get("case_id")
            target_d = record.get("target_disease", "")

            # Extract validated_label from top-level, _provenance, or step12_dataset_label
            v_label = (
                record.get("validated_label")
                or (record.get("_provenance") or {}).get("validated_label")
                or record.get("step12_dataset_label")
                or "UNKNOWN"
            )

            # Ground truth label assignment per prompt specifications
            if v_label == "POSITIVE":
                gt_label = target_d
            else:
                gt_label = f"{target_d} {v_label}"

            pair_id = record.get("pair_id", f"{cid}::{target_d}")

            # Binary indicator map for all 15 diseases (used in holdout validation)
            # Only 1 if target_disease matches disease d AND validated_label == 'POSITIVE'
            disease_binary = {}
            for d in target_diseases:
                col = _clean_disease_name(d)
                is_pos = 1 if (_clean_disease_name(d) == _clean_disease_name(target_d) and v_label == "POSITIVE") else 0
                disease_binary[col] = is_pos

            case_item = {
                "index": idx,
                "case_id": cid,
                "pair_id": pair_id,
                "target_disease": target_d,
                "validated_label": v_label,
                "ground_truth_label": gt_label,
                "binary_labels": disease_binary,
            }
            gold_cases.append(case_item)

            if cid not in gold_labels:
                gold_labels[cid] = {
                    "case_id": cid,
                    "target_disease": target_d,
                    "validated_label": v_label,
                    "ground_truth_label": gt_label,
                    "pair_id": pair_id,
                    **disease_binary,
                }
            else:
                # Merge binary labels for multi-candidate / coinfection cases
                for col, val in disease_binary.items():
                    if val == 1:
                        gold_labels[cid][col] = 1

    return gold_cases, gold_labels


# Initialize global gold standards for all 15 diseases and 981 cases
GOLD_CASES, GOLD_LABELS = load_gold_labels()


# ═══════════════════════════════════════════════════════════════════════════════
#  Full Pipeline Evaluation Harness
# ═══════════════════════════════════════════════════════════════════════════════

def run_full_evaluation(
    df_patients: pd.DataFrame,
    threshold: float = 0.6,
    gt_path: str = None,
    output_file: str = "evaluation_results.json",
    csv_file: str = "evaluation_case_summary.csv",
):
    """
    Run full evaluation against gold standard labels across all 15 diseases and 981 cases.
    """
    if not SKLEARN_AVAILABLE:
        print("scikit-learn not available. Install it for evaluation.")
        return

    # Load custom gold dataset if specified, otherwise use preloaded global data
    if gt_path is not None:
        gold_cases, gold_labels = load_gold_labels(gt_path=gt_path)
    else:
        gold_cases, gold_labels = GOLD_CASES, GOLD_LABELS

    if not gold_cases:
        print("  No gold cases available for evaluation. Skipping evaluation.")
        return

    eval_diseases = list(DISEASES.keys())

    print("\n" + "=" * 90)
    print("  GOLD-STANDARD HOLDOUT EVALUATION (15 DISEASES, 981 CASES)")
    print("=" * 90)

    # Align cases between df_patients and gold_cases
    aligned_cases = []
    is_aligned_by_index = (
        len(df_patients) == len(gold_cases)
        and all(df_patients.iloc[i]["case_id"] == gold_cases[i]["case_id"] for i in range(len(df_patients)))
    )

    if is_aligned_by_index:
        for i in range(len(df_patients)):
            aligned_cases.append((df_patients.iloc[i], gold_cases[i]))
    else:
        # Fallback to case_id lookup for subsets or unordered dataframes
        for _, row in df_patients.iterrows():
            cid = row["case_id"]
            if cid in gold_labels:
                aligned_cases.append((row, gold_labels[cid]))

    if not aligned_cases:
        print("  No gold labels matched any case IDs. Skipping evaluation.")
        return

    print(f"\n  Evaluating {len(aligned_cases)} cases with gold labels.\n")

    # 1. Build per-disease gold and prediction arrays
    gold_arrays = {d: [] for d in eval_diseases}
    pred_arrays = {d: [] for d in eval_diseases}

    for row, case_gold in aligned_cases:
        for d in eval_diseases:
            col_name = _clean_disease_name(d)
            if "binary_labels" in case_gold:
                is_pos = case_gold["binary_labels"].get(col_name, 0)
            else:
                is_pos = case_gold.get(col_name, 0)
            gold_arrays[d].append(is_pos)
            pred_arrays[d].append(float(row.get(f"p_{col_name}", 0.0)))

    # 2. Extrinsic Evaluation: Per-disease classification reports and ROC-AUC
    disease_metrics = []
    for d in eval_diseases:
        metrics = evaluate_gold_holdout(
            gold_arrays[d],
            pred_arrays[d],
            threshold=threshold,
            disease_name=d.upper(),
        )
        if metrics:
            disease_metrics.append(metrics)

    # 3. 15-Disease Aggregate Benchmark Summary Table
    print("\n" + "=" * 90)
    print(f"  15-DISEASE EXTRINSIC PERFORMANCE BENCHMARK (THRESHOLD = {threshold:.2f})")
    print("=" * 90)
    print(f"  {'Disease':<20} {'Pos / Total':<14} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'ROC-AUC':<10}")
    print(f"  {'-'*20} {'-'*14} {'-'*12} {'-'*12} {'-'*12} {'-'*10}")

    auc_values = []
    for m in disease_metrics:
        auc_str = f"{m['roc_auc']:.4f}" if m['roc_auc'] is not None else "N/A"
        if m['roc_auc'] is not None:
            auc_values.append(m['roc_auc'])
        pos_ratio = f"{m['pos_count']}/{m['total']}"
        print(f"  {m['disease']:<20} {pos_ratio:<14} {m['precision']:<12.4f} {m['recall']:<12.4f} {m['f1_score']:<12.4f} {auc_str:<10}")

    avg_prec = np.mean([m['precision'] for m in disease_metrics]) if disease_metrics else 0.0
    avg_rec = np.mean([m['recall'] for m in disease_metrics]) if disease_metrics else 0.0
    avg_f1 = np.mean([m['f1_score'] for m in disease_metrics]) if disease_metrics else 0.0
    avg_auc = np.mean(auc_values) if auc_values else 0.0
    print(f"  {'-'*20} {'-'*14} {'-'*12} {'-'*12} {'-'*12} {'-'*10}")
    print(f"  {'Macro Average':<20} {'-':<14} {avg_prec:<12.4f} {avg_rec:<12.4f} {avg_f1:<12.4f} {avg_auc:<10.4f}")

    # 4. Case-Level Prediction Summary Table (Most Likely Disease)
    print("\n" + "-" * 105)
    print("  CASE-LEVEL PREDICTION SUMMARY (MOST LIKELY DISEASE - 981 CASES)")
    print("-" * 105)
    print(f"  {'#':<5} {'Case ID':<18} {'Gold Label':<42} {'Predicted Disease':<32} {'Match?'}")
    print(f"  {'-'*5} {'-'*18} {'-'*42} {'-'*32} {'-'*6}")

    correct = 0
    total = 0
    pos_correct = 0
    pos_total = 0
    non_pos_rejected = 0
    non_pos_total = 0
    csv_rows = []

    for idx, (row, case_gold) in enumerate(aligned_cases):
        cid = row["case_id"]
        gold_str = case_gold["ground_truth_label"]
        v_label = case_gold.get("validated_label", "")

        # Predicted disease: prefer explicit predicted_disease from report/model
        pred_disease = row.get("predicted_disease")
        if not pred_disease or pred_disease == "UNKNOWN (Insufficient Evidence)":
            probs = {}
            for d in eval_diseases:
                col = _clean_disease_name(d)
                if f"p_{col}" in row:
                    probs[d] = float(row[f"p_{col}"])
            if probs:
                best_d, max_p = max(probs.items(), key=lambda item: item[1])
                pred_str = best_d if max_p > 0.50 else "UNKNOWN (Insufficient Evidence)"
            else:
                pred_str = "UNKNOWN (Insufficient Evidence)"
        else:
            pred_str = str(pred_disease)

        # Match calculation:
        # If validated_label == 'POSITIVE': gold is target_disease. Matches iff pred_str == target_disease.
        # If validated_label != 'POSITIVE': gold is target_disease + ' ' + validated_label.
        # If the pipeline labels this case as target_disease, it is marked incorrect (✗) since not positive.
        match = (_clean_disease_name(pred_str) == _clean_disease_name(gold_str))

        if match:
            correct += 1
        total += 1

        if v_label == "POSITIVE":
            pos_total += 1
            if match:
                pos_correct += 1
        else:
            non_pos_total += 1
            if pred_str in ["none", "UNKNOWN", "UNKNOWN (Insufficient Evidence)"]:
                non_pos_rejected += 1

        symbol = "✓" if match else "✗"
        print(f"  {idx+1:<5} {cid:<18} {gold_str:<42} {pred_str:<32} {symbol}")

        case_entry = {
            "index": idx + 1,
            "case_id": cid,
            "pair_id": case_gold.get("pair_id", f"{cid}::{case_gold.get('target_disease', '')}"),
            "target_disease": case_gold.get("target_disease", ""),
            "validated_label": v_label,
            "ground_truth_label": gold_str,
            "predicted_disease": pred_str,
            "match": match,
        }
        csv_rows.append(case_entry)

    print("\n" + "=" * 105)
    print("  FINAL EVALUATION SUMMARY")
    print("=" * 105)
    print(f"  Overall Exact Match Accuracy: {correct}/{total} ({correct/total:.1%})")
    print("\n  Breakdown by Ground Truth Status:")
    if pos_total > 0:
        print(f"    • Confirmed Positive Cases ({pos_total} total):")
        print(f"        Correctly diagnosed:      {pos_correct}/{pos_total} ({pos_correct/pos_total:.1%})")
        print(f"        Misdiagnosed / Missed:    {pos_total - pos_correct}/{pos_total} ({(pos_total - pos_correct)/pos_total:.1%})")
    if non_pos_total > 0:
        print(f"    • Non-Positive / Excluded Cases ({non_pos_total} total):")
        print(f"        Correctly rejected (Unknown / Abstain): {non_pos_rejected}/{non_pos_total} ({non_pos_rejected/non_pos_total:.1%})")
        print(f"        Incorrectly given positive diagnosis:   {non_pos_total - non_pos_rejected}/{non_pos_total} ({(non_pos_total - non_pos_rejected)/non_pos_total:.1%})")
    print("=" * 105)

    # 5. Compile and Save Evaluation Results
    results_payload = {
        "metadata": {
            "total_cases": total,
            "num_diseases": len(eval_diseases),
            "threshold": threshold,
        },
        "overall_summary": {
            "total_cases": total,
            "exact_match_correct": correct,
            "overall_accuracy": round(correct / total, 4) if total > 0 else 0.0,
            "confirmed_positive_cases": {
                "total": pos_total,
                "correctly_diagnosed": pos_correct,
                "accuracy": round(pos_correct / pos_total, 4) if pos_total > 0 else 0.0,
                "missed_or_misdiagnosed": pos_total - pos_correct,
            },
            "non_positive_cases": {
                "total": non_pos_total,
                "correctly_rejected_unknown": non_pos_rejected,
                "rejection_rate": round(non_pos_rejected / non_pos_total, 4) if non_pos_total > 0 else 0.0,
                "incorrectly_given_positive": non_pos_total - non_pos_rejected,
            },
            "macro_averages": {
                "precision": round(float(avg_prec), 4),
                "recall": round(float(avg_rec), 4),
                "f1_score": round(float(avg_f1), 4),
                "roc_auc": round(float(avg_auc), 4),
            },
        },
        "disease_benchmarks": disease_metrics,
        "case_evaluations": csv_rows,
    }

    # Save to JSON
    if output_file:
        with open(output_file, "w") as f:
            json.dump(results_payload, f, indent=2)
        print(f"\nSaved structured evaluation results to {output_file}")

    # Save to CSV
    if csv_file:
        df_csv = pd.DataFrame(csv_rows)
        df_csv.to_csv(csv_file, index=False)
        print(f"Saved case-level evaluation summary to {csv_file}")

    return results_payload


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    report_file = "final_diagnosis_report.json"
    if not os.path.exists(report_file):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        report_file = os.path.join(base_dir, "final_diagnosis_report.json")

    try:
        with open(report_file, "r") as f:
            report = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: '{report_file}' not found. Run stage2_diagnosis.py first.")
        sys.exit(1)

    rows = []
    for entry in report:
        row = {
            "case_id": entry["case_id"],
            "predicted_disease": entry.get("predicted_disease"),
            "valid_symptoms": entry.get("evidence_used", []),
        }
        for d, vals in entry.get("diagnoses", {}).items():
            row[f"p_{d}"] = vals["probability"]
            row[f"{d}_label"] = vals["label"]
        rows.append(row)

    df_patients = pd.DataFrame(rows)
    run_full_evaluation(
        df_patients,
        threshold=0.6,
        output_file="evaluation_results.json",
        csv_file="evaluation_case_summary.csv",
    )

    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)

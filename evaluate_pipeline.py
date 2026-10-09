"""
evaluate_pipeline.py: Intrinsic LF diagnostics and extrinsic holdout validation harness.

Provides:
  1. print_lf_diagnostics(): Snorkel's LFAnalysis summary (coverage, overlap, conflicts)
  2. evaluate_gold_holdout(): Classification report + ROC-AUC against gold labels
  3. run_full_evaluation(): End-to-end pipeline evaluation with built-in gold labels
"""
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
    
    Args:
        y_true: Array of binary gold labels (0 or 1)
        y_pred_probs: Array of predicted positive-class probabilities
        threshold: Decision threshold for converting probabilities to labels
        disease_name: Name of the disease for display
    """
    if not SKLEARN_AVAILABLE:
        print("scikit-learn not available. Cannot evaluate.")
        return

    print(f"\n--- EXTRINSIC EVALUATION: {disease_name.upper()} ---")

    y_pred = (np.array(y_pred_probs) >= threshold).astype(int)
    y_true = np.array(y_true)

    print(classification_report(
        y_true, y_pred,
        target_names=["Negative", "Positive"],
        zero_division=0,
    ))

    try:
        if len(np.unique(y_true)) > 1:
            auc = roc_auc_score(y_true, y_pred_probs)
            print(f"  ROC-AUC Score: {auc:.4f}")
        else:
            print("  ROC-AUC: N/A (only one class in gold labels)")
    except ValueError:
        print("  ROC-AUC: N/A (computation error)")


# ═══════════════════════════════════════════════════════════════════════════════
#  Gold Standard Labels (from case report titles/PMC sources)
# ═══════════════════════════════════════════════════════════════════════════════

# Hand-annotated ground truth for the 10 cases in extracted_cases_top3_new.jsonl
# Derived from the PMC paper titles and case diagnoses
GOLD_LABELS = {
    # COVID-19 cases
    "PMC10007705_01": {"covid19": 1, "tuberculosis": 0, "dengue": 0},  # COVID-19 myositis (background case)
    "PMC10007705_02": {"covid19": 1, "tuberculosis": 0, "dengue": 0},  # COVID-19 myositis (patient)
    "PMC10010120_01": {"covid19": 1, "tuberculosis": 0, "dengue": 0},  # COVID-19 dermatitis herpetiformis
    # Tuberculosis cases
    "PMC10041991_01": {"covid19": 0, "tuberculosis": 1, "dengue": 0},  # TB meningitis (pre-XDR)
    "PMC10043165_01": {"covid19": 0, "tuberculosis": 1, "dengue": 0},  # Muscular tuberculosis case 1
    "PMC10043165_02": {"covid19": 0, "tuberculosis": 1, "dengue": 0},  # Muscular tuberculosis case 2
    # Dengue cases
    "PMC10010886_01": {"covid19": 0, "tuberculosis": 0, "dengue": 1},  # Dengue acute pancreatitis
    "PMC10062082_01": {"covid19": 0, "tuberculosis": 0, "dengue": 1},  # Dengue retinopathy
    "PMC10402786_01": {"covid19": 0, "tuberculosis": 0, "dengue": 1},  # Dengue myocarditis
}


def run_full_evaluation(df_patients: pd.DataFrame):
    """
    Run full evaluation against gold standard labels.
    
    Args:
        df_patients: DataFrame with columns case_id, p_covid19, p_tuberculosis, p_dengue
    """
    if not SKLEARN_AVAILABLE:
        print("scikit-learn not available. Install it for evaluation.")
        return

    print("\n" + "=" * 70)
    print("  GOLD-STANDARD HOLDOUT EVALUATION")
    print("=" * 70)

    # Build aligned arrays
    case_ids = df_patients["case_id"].tolist()
    gold_covid, gold_tb, gold_dengue = [], [], []
    pred_covid, pred_tb, pred_dengue = [], [], []

    for _, row in df_patients.iterrows():
        cid = row["case_id"]
        if cid in GOLD_LABELS:
            gold = GOLD_LABELS[cid]
            gold_covid.append(gold["covid19"])
            gold_tb.append(gold["tuberculosis"])
            gold_dengue.append(gold["dengue"])
            pred_covid.append(row["p_covid19"])
            pred_tb.append(row["p_tuberculosis"])
            pred_dengue.append(row["p_dengue"])

    if not gold_covid:
        print("  No gold labels matched any case IDs. Skipping evaluation.")
        return

    print(f"\n  Evaluating {len(gold_covid)} cases with gold labels.\n")

    evaluate_gold_holdout(gold_covid, pred_covid, threshold=0.6, disease_name="COVID-19")
    evaluate_gold_holdout(gold_tb, pred_tb, threshold=0.6, disease_name="Tuberculosis")
    evaluate_gold_holdout(gold_dengue, pred_dengue, threshold=0.6, disease_name="Dengue")

    # Summary confusion table
    print("\n" + "-" * 70)
    print("  CASE-LEVEL PREDICTION SUMMARY (MOST LIKELY DISEASE)")
    print("-" * 70)
    print(f"  {'Case ID':<22} {'Gold':<20} {'Predicted':<30} {'Match?'}")
    print(f"  {'-'*22} {'-'*20} {'-'*30} {'-'*6}")

    correct = 0
    total = 0

    for _, row in df_patients.iterrows():
        cid = row["case_id"]
        if cid not in GOLD_LABELS:
            continue

        gold = GOLD_LABELS[cid]

        # Gold disease(s)
        gold_diseases = [d for d, v in gold.items() if v == 1]
        gold_str = ", ".join(gold_diseases) if gold_diseases else "none"

        # Predicted disease: select the single most likely disease (argmax)
        probs = {
            "covid19": float(row["p_covid19"]),
            "tuberculosis": float(row["p_tuberculosis"]),
            "dengue": float(row["p_dengue"]),
        }
        top_disease, max_prob = max(probs.items(), key=lambda item: item[1])
        
        # Only predict if probability strictly exceeds the neutral prior (0.50)
        pred_str = top_disease if max_prob > 0.50 else "none"

        match = pred_str in gold_diseases
        if match:
            correct += 1
        total += 1

        symbol = "✓" if match else "✗"
        print(f"  {cid:<22} {gold_str:<20} {pred_str:<30} {symbol}")

    print(f"\n  Overall Accuracy: {correct}/{total} ({correct/total:.1%})")


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Load the final diagnosis report and reconstruct the DataFrame
    try:
        with open("final_diagnosis_report.json", "r") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("ERROR: final_diagnosis_report.json not found. Run stage2_diagnosis.py first.")
        exit(1)

    rows = []
    for entry in report:
        rows.append({
            "case_id": entry["case_id"],
            "predicted_disease": entry.get("predicted_disease"),
            "p_covid19": entry["diagnoses"]["covid19"]["probability"],
            "p_tuberculosis": entry["diagnoses"]["tuberculosis"]["probability"],
            "p_dengue": entry["diagnoses"]["dengue"]["probability"],
            "valid_symptoms": entry.get("evidence_used", []),
        })

    df_patients = pd.DataFrame(rows)
    run_full_evaluation(df_patients)

    import os, sys
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


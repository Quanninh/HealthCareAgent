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
# For brevity, these are hardcoded for 3 diseases. Add more for 15 diseases if needed.
GOLD_LABELS = {
    # COVID-19 cases
    "PMC10007705_01": {"covid-19": 1, "tuberculosis": 0, "dengue": 0},  # COVID-19 myositis (background case)
    "PMC10007705_02": {"covid-19": 1, "tuberculosis": 0, "dengue": 0},  # COVID-19 myositis (patient)
    "PMC10010120_01": {"covid-19": 1, "tuberculosis": 0, "dengue": 0},  # COVID-19 dermatitis herpetiformis
    # Tuberculosis cases
    "PMC10041991_01": {"covid-19": 0, "tuberculosis": 1, "dengue": 0},  # TB meningitis (pre-XDR)
    "PMC10043165_01": {"covid-19": 0, "tuberculosis": 1, "dengue": 0},  # Muscular tuberculosis case 1
    "PMC10043165_02": {"covid-19": 0, "tuberculosis": 1, "dengue": 0},  # Muscular tuberculosis case 2
    # Dengue cases
    "PMC10010886_01": {"covid-19": 0, "tuberculosis": 0, "dengue": 1},  # Dengue acute pancreatitis
    "PMC10062082_01": {"covid-19": 0, "tuberculosis": 0, "dengue": 1},  # Dengue retinopathy
    "PMC10402786_01": {"covid-19": 0, "tuberculosis": 0, "dengue": 1},  # Dengue myocarditis
}


def run_full_evaluation(df_patients: pd.DataFrame):
    """
    Run full evaluation against gold standard labels.
    """
    if not SKLEARN_AVAILABLE:
        print("scikit-learn not available. Install it for evaluation.")
        return

    print("\n" + "=" * 70)
    print("  GOLD-STANDARD HOLDOUT EVALUATION")
    print("=" * 70)

    # Build aligned arrays for diseases present in GOLD_LABELS
    case_ids = df_patients["case_id"].tolist()
    
    # We only care about diseases that actually appear in GOLD_LABELS inner dicts
    eval_diseases = set()
    for gl in GOLD_LABELS.values():
        eval_diseases.update(gl.keys())
        
    gold_arrays = {d: [] for d in eval_diseases}
    pred_arrays = {d: [] for d in eval_diseases}

    for _, row in df_patients.iterrows():
        cid = row["case_id"]
        if cid in GOLD_LABELS:
            gold = GOLD_LABELS[cid]
            for d in eval_diseases:
                gold_arrays[d].append(gold.get(d, 0))
                # match column name
                col_name = d.lower().replace('-', '_').replace(' ', '_')
                pred_arrays[d].append(row.get(f"p_{col_name}", 0.0))

    if not any(gold_arrays.values()):
        print("  No gold labels matched any case IDs. Skipping evaluation.")
        return

    print(f"\n  Evaluating {len(next(iter(gold_arrays.values())))} cases with gold labels.\n")

    for d in eval_diseases:
        evaluate_gold_holdout(gold_arrays[d], pred_arrays[d], threshold=0.6, disease_name=d.upper())

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
        probs = {}
        for d in DISEASES.keys():
            col = d.lower().replace('-', '_').replace(' ', '_')
            if f"p_{col}" in row:
                probs[d.lower()] = float(row[f"p_{col}"])
            
        if probs:
            top_disease, max_prob = max(probs.items(), key=lambda item: item[1])
            pred_str = top_disease if max_prob > 0.50 else "none"
        else:
            pred_str = "none"

        match = pred_str in [g.lower() for g in gold_diseases]
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
    run_full_evaluation(df_patients)

    import os, sys
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)

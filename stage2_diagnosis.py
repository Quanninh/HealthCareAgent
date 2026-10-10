"""
stage2_diagnosis.py: Multi-label disease prediction using independent binary Snorkel models.

Key Architecture Changes from the old pipeline:
  1. MULTI-LABEL: 15 independent binary classifiers (one for each disease)
     instead of 1 multi-class softmax that forces artificial competition.
  2. MULTI-LF SUITES: Each disease has 3 LFs (Hallmark, Lab, Exclusion) dynamically generated.
  3. CORRECT CARDINALITY: cardinality=2 per binary model.

Supports comorbidities: a patient can be diagnosed with multiple diseases
if the evidence supports it.
"""
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import json
import pandas as pd
import numpy as np

try:
    from snorkel.labeling import labeling_function, PandasLFApplier
    from snorkel.labeling.model import LabelModel, MajorityLabelVoter
    SNORKEL_AVAILABLE = True
except ImportError as e:
    SNORKEL_AVAILABLE = False
    print(f"WARNING: Snorkel failed to import: {e}")

from schemas import BinaryDiseaseLabel
from clinical_knowledge import DISEASE_HALLMARKS, DISEASE_LAB_TESTS, DISEASE_EXCLUSIONS, DISEASES, SHARED_SYSTEMIC_SYMPTOMS


# ═══════════════════════════════════════════════════════════════════════════════
#  Helper: Symptom Matching
# ═══════════════════════════════════════════════════════════════════════════════

def _symptom_match(symptoms: list, targets: list) -> bool:
    """Check if any symptom string contains any target keyword."""
    if not targets:
        return False
    for symptom in symptoms:
        s_lower = symptom.lower()
        for target in targets:
            if target in s_lower:
                return True
    return False

def _count_matches(symptoms: list, targets: list) -> int:
    """Count how many distinct targets are matched."""
    count = 0
    if not targets:
        return 0
    for target in targets:
        if any(target in s.lower() for s in symptoms):
            count += 1
    return count

# ═══════════════════════════════════════════════════════════════════════════════
#  Dynamic Labeling Functions Factory
# ═══════════════════════════════════════════════════════════════════════════════

def make_lfs_for_disease(disease_name: str):
    """Dynamically generate labeling functions for a given disease."""
    hallmarks = DISEASE_HALLMARKS.get(disease_name, [])
    lab_tests = DISEASE_LAB_TESTS.get(disease_name, [])
    exclusions = DISEASE_EXCLUSIONS.get(disease_name, [])
    
    sanitized_name = disease_name.lower().replace('-', '_').replace(' ', '_')

    # Note: Default arguments used in the lambda/functions below are necessary to capture
    # the variables in the closure instead of late-binding them in a loop.
    
    @labeling_function(name=f"lf_{sanitized_name}_hallmarks")
    def lf_hallmarks(x, hm=hallmarks):
        if _symptom_match(x.valid_symptoms, hm):
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    @labeling_function(name=f"lf_{sanitized_name}_lab_confirmation")
    def lf_lab(x, lt=lab_tests):
        if _symptom_match(x.valid_symptoms, lt):
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    @labeling_function(name=f"lf_{sanitized_name}_constellation")
    def lf_constellation(x, hm=hallmarks, sys_sym=SHARED_SYSTEMIC_SYMPTOMS):
        has_systemic = _symptom_match(x.valid_symptoms, sys_sym)
        has_specific = _symptom_match(x.valid_symptoms, hm)
        # If the patient has a general systemic symptom AND a disease-specific hallmark
        if has_systemic and has_specific:
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    @labeling_function(name=f"lf_{sanitized_name}_negative_test")
    def lf_neg(x, ex=exclusions):
        if _symptom_match(x.valid_symptoms, ex):
            return BinaryDiseaseLabel.NEGATIVE
        return BinaryDiseaseLabel.ABSTAIN

    return [lf_hallmarks, lf_lab, lf_constellation, lf_neg]


DISEASE_LFS = {disease: make_lfs_for_disease(disease) for disease in DISEASES.keys()}


# ═══════════════════════════════════════════════════════════════════════════════
#  Model Training & Prediction
# ═══════════════════════════════════════════════════════════════════════════════

def build_disease_model(df_patients: pd.DataFrame, lfs: list, disease_name: str) -> tuple:
    """
    Train an independent binary Snorkel LabelModel for a single disease.
    
    Returns (probabilities_array, L_matrix) where probabilities are P(POSITIVE).
    Falls back to MajorityLabelVoter if LabelModel fails to converge.
    """
    applier = PandasLFApplier(lfs=lfs)
    L_train = applier.apply(df=df_patients)

    # Check if we have any non-abstain votes
    non_abstain = (L_train != -1).sum()
    if non_abstain == 0:
        print(f"  [{disease_name}] WARNING: All LFs abstained. Returning 0.0 for all cases.")
        return np.zeros(len(df_patients)), L_train

    try:
        model = LabelModel(cardinality=2, verbose=False)
        model.fit(L_train=L_train, n_epochs=500, seed=42)
        probs = model.predict_proba(L_train)
        print(f"  [{disease_name}] LabelModel trained successfully.")
    except Exception as e:
        print(f"  [{disease_name}] LabelModel failed ({e}), falling back to MajorityLabelVoter.")
        voter = MajorityLabelVoter(cardinality=2)
        probs = voter.predict_proba(L_train)

    return probs[:, 1], L_train  # Return P(POSITIVE)


def _classify_label(prob: float, pos_threshold: float = 0.60, neg_threshold: float = 0.40) -> str:
    """Convert probability to a human-readable label."""
    if prob >= pos_threshold:
        return "POSITIVE"
    elif prob <= neg_threshold:
        return "NEGATIVE"
    else:
        return "UNCERTAIN"


def run_stage2_multilabel_diagnosis(
    raw_data: list,
    accepted_entities: list,
    pos_threshold: float = 0.60,
    neg_threshold: float = 0.40,
) -> pd.DataFrame:
    if not SNORKEL_AVAILABLE:
        print("Snorkel not available. Cannot run Stage 2.")
        return pd.DataFrame(), {}

    # 1. Group VALID entities by case_id
    valid_by_case = {}
    for r in accepted_entities:
        cid = r["case_id"]
        if cid not in valid_by_case:
            valid_by_case[cid] = []
        if float(r["probability"]) >= 0.85:
            # Add both the MedCAT standard_name AND the raw LLM text
            if r.get("standard_name"):
                valid_by_case[cid].append(r["standard_name"].lower())
            valid_by_case[cid].append(r["entity"].lower())

    # 2. Build patient-level DataFrame
    patient_cases = []
    for case in raw_data:
        cid = case["case_id"]
        patient_cases.append({
            "case_id": cid,
            "valid_symptoms": valid_by_case.get(cid, []),
        })
    df_patients = pd.DataFrame(patient_cases)

    print(f"\n{'='*60}")
    print(f"  STAGE 2: MULTI-LABEL DISEASE PREDICTION")
    print(f"  Patients: {len(df_patients)} | Threshold: POSITIVE >= {pos_threshold}, NEGATIVE <= {neg_threshold}")
    print(f"{'='*60}\n")

    # 3. Train independent binary models
    L_matrices = {}
    disease_probs = {}
    
    for disease_name, lfs in DISEASE_LFS.items():
        print(f"Training {disease_name} binary classifier...")
        probs, L_matrix = build_disease_model(df_patients, lfs, disease_name)
        disease_probs[disease_name] = probs
        L_matrices[disease_name] = L_matrix
        
        # Save to dataframe
        col_name = disease_name.lower().replace('-', '_').replace(' ', '_')
        df_patients[f"p_{col_name}"] = probs
        df_patients[f"{col_name}_label"] = df_patients[f"p_{col_name}"].apply(
            lambda p: _classify_label(p, pos_threshold, neg_threshold)
        )

    # 5. Determine the single most likely disease (highest probability above baseline 0.5)
    def _get_top_disease(row):
        probs = {}
        for d in DISEASES.keys():
            col = d.lower().replace('-', '_').replace(' ', '_')
            probs[d] = row[f"p_{col}"]
            
        best_disease, max_p = max(probs.items(), key=lambda item: item[1])
        if max_p > 0.50:
            return best_disease
        return "UNKNOWN (Insufficient Evidence)"

    df_patients["predicted_disease"] = df_patients.apply(_get_top_disease, axis=1)

    return df_patients, L_matrices


# ═══════════════════════════════════════════════════════════════════════════════
#  Output Formatting & Saving
# ═══════════════════════════════════════════════════════════════════════════════

def save_diagnosis_outputs(
    df_patients: pd.DataFrame,
    report_file: str = "final_diagnosis_report.json",
    csv_file: str = "final_labels.csv",
):
    """Save the multi-label diagnosis results in JSON and CSV formats."""
    
    # JSON report
    results = []
    for _, row in df_patients.iterrows():
        diagnoses = {}
        for disease_name in DISEASES.keys():
            col = disease_name.lower().replace('-', '_').replace(' ', '_')
            diagnoses[col] = {
                "probability": round(float(row[f"p_{col}"]), 4),
                "label": row[f"{col}_label"],
            }
            
        results.append({
            "case_id": row["case_id"],
            "predicted_disease": row["predicted_disease"],
            "diagnoses": diagnoses,
            "evidence_used": row["valid_symptoms"],
        })

    with open(report_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\nSaved diagnosis report to {report_file}")

    # CSV labels
    cols = ["case_id", "predicted_disease"]
    for disease_name in DISEASES.keys():
        col = disease_name.lower().replace('-', '_').replace(' ', '_')
        cols.append(f"p_{col}")
        cols.append(f"{col}_label")
        
    csv_df = df_patients[cols].copy()
    csv_df.to_csv(csv_file, index=False)
    print(f"Saved tabular labels to {csv_file}")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 1. Load raw data
    input_file = "extracted_cases_100per_disease.jsonl"
    print(f"Loading raw patient case data from {input_file}...")
    with open(input_file, "r") as f:
        raw_data = [json.loads(line) for line in f if line.strip()]

    # 2. Load accepted entities
    print("Loading AUTO-ACCEPTED entities...")
    with open("accepted_entities.json", "r") as f:
        accepted_entities = json.load(f)

    # 3. Load human-reviewed entities (if any)
    expert_approved = []
    try:
        with open("human_review_queue.json", "r") as f:
            review_queue = json.load(f)
        for entity in review_queue:
            if entity.get("expert_decision") == "APPROVED":
                entity["probability"] = "1.00"
                expert_approved.append(entity)
        print(f"  -> Found {len(expert_approved)} entities manually APPROVED by expert.")
    except FileNotFoundError:
        print("  -> No human review queue found. Proceeding with auto-accepted only.")

    final_accepted = accepted_entities + expert_approved
    print(f"\nTotal Confirmed Entities for Stage 2: {len(final_accepted)}")

    # 4. Run multi-label diagnosis
    df_patients, L_matrices = run_stage2_multilabel_diagnosis(raw_data, final_accepted)

    if not df_patients.empty:
        # 5. Print results
        print(f"\n{'='*70}")
        print(f"  MULTI-LABEL DIAGNOSIS RESULTS")
        print(f"{'='*70}")
        for _, row in df_patients.iterrows():
            print(f"\n  [{row['case_id']}] -> Most Likely: {row['predicted_disease'].upper()}")
            for disease_name in list(DISEASES.keys())[:3]: # print top 3 to keep it brief
                col = disease_name.lower().replace('-', '_').replace(' ', '_')
                print(f"    {disease_name}:      P={row[f'p_{col}']:.4f}  -> {row[f'{col}_label']}")
            print("    ...")

        # 6. Save outputs
        results = save_diagnosis_outputs(df_patients)

        # 7. Run LF diagnostics
        from evaluate_pipeline import print_lf_diagnostics
        print("\n" + "=" * 60)
        print("  STAGE 2 LABELING FUNCTION DIAGNOSTICS")
        print("=" * 60)
        for disease_name, lfs in DISEASE_LFS.items():
            print(f"\n--- {disease_name} LFs ---")
            print_lf_diagnostics(L_matrices[disease_name], lfs)

    # Cleanly exit to prevent hanging on background threads
    import sys
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)

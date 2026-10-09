"""
stage2_diagnosis.py: Multi-label disease prediction using independent binary Snorkel models.

Key Architecture Changes from the old pipeline:
  1. MULTI-LABEL: 3 independent binary classifiers (has_covid, has_tb, has_dengue)
     instead of 1 multi-class softmax that forces artificial competition.
  2. MULTI-LF SUITES: Each disease has 3+ LFs (Hallmark, Constellation, Exclusion)
     instead of the old 1-LF-per-disease which made the covariance matrix unidentifiable.
  3. CORRECT CARDINALITY: cardinality=2 per binary model, not cardinality=6.
  4. DECOUPLED SYMPTOMS: Shared systemic symptoms (fever, myalgia) are only used
     in constellation LFs that require co-occurrence with disease-specific signs.

Supports comorbidities: a patient can be diagnosed with BOTH COVID-19 and Dengue
if the evidence supports it (e.g., co-infection).
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
from clinical_knowledge import (
    COVID19_HALLMARKS, TUBERCULOSIS_HALLMARKS, DENGUE_HALLMARKS,
    COVID19_EXCLUSIONS, TB_EXCLUSIONS, DENGUE_EXCLUSIONS,
    SHARED_SYSTEMIC_SYMPTOMS,
)


# ═══════════════════════════════════════════════════════════════════════════════
#  Helper: Symptom Matching
# ═══════════════════════════════════════════════════════════════════════════════

def _symptom_match(symptoms: list, targets: list) -> bool:
    """Check if any symptom string contains any target keyword."""
    for symptom in symptoms:
        s_lower = symptom.lower()
        for target in targets:
            if target in s_lower:
                return True
    return False


def _count_matches(symptoms: list, targets: list) -> int:
    """Count how many distinct targets are matched."""
    count = 0
    for target in targets:
        if any(target in s.lower() for s in symptoms):
            count += 1
    return count


# ═══════════════════════════════════════════════════════════════════════════════
#  COVID-19 Binary Labeling Functions
# ═══════════════════════════════════════════════════════════════════════════════

@labeling_function()
def lf_covid_hallmarks(x):
    """
    Hallmark LF: Vote POSITIVE if any COVID-19-specific pathognomonic sign
    is present (anosmia, ground-glass opacities, positive PCR, etc.).
    """
    if _symptom_match(x.valid_symptoms, COVID19_HALLMARKS):
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_covid_respiratory_syndrome(x):
    """
    Constellation LF: Fever + dyspnea/shortness of breath together
    suggest COVID-19 respiratory presentation.
    """
    has_fever = _symptom_match(x.valid_symptoms, ["fever", "febrile"])
    has_dyspnea = _symptom_match(x.valid_symptoms, ["dyspnea", "shortness of breath"])
    if has_fever and has_dyspnea:
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_covid_lab_confirmation(x):
    """
    Lab LF: Explicit mention of positive SARS-CoV-2 lab test or COVID-19 diagnosis.
    """
    lab_terms = [
        "positive rrt-pcr", "positive sars-cov-2", "covid-19 swab",
        "which was positive", "sars-cov-2 infection", "anti-sars-cov-2",
    ]
    if _symptom_match(x.valid_symptoms, lab_terms):
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_covid_negative_test(x):
    """
    Exclusion LF: If a negative COVID test is recorded, vote NEGATIVE.
    """
    if _symptom_match(x.valid_symptoms, COVID19_EXCLUSIONS):
        return BinaryDiseaseLabel.NEGATIVE
    return BinaryDiseaseLabel.ABSTAIN


# ═══════════════════════════════════════════════════════════════════════════════
#  TUBERCULOSIS Binary Labeling Functions
# ═══════════════════════════════════════════════════════════════════════════════

@labeling_function()
def lf_tb_hallmarks(x):
    """
    Hallmark LF: Vote POSITIVE if any TB-specific pathognomonic sign is present
    (hemoptysis, cavitary lesion, caseating granuloma, GeneXpert+, etc.).
    """
    if _symptom_match(x.valid_symptoms, TUBERCULOSIS_HALLMARKS):
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_tb_chronic_wasting(x):
    """
    Constellation LF: Chronic presentation of fever + (night sweats OR
    weight loss OR chronic cough) suggests TB.
    """
    has_fever = _symptom_match(x.valid_symptoms, ["fever", "febrile"])
    has_wasting = _symptom_match(x.valid_symptoms, [
        "sweats", "night sweats", "weight loss", "cough",
    ])
    if has_fever and has_wasting:
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_tb_meningitis(x):
    """
    Constellation LF: Meningeal signs (neck stiffness, meningeal enhancement)
    + elevated CSF protein + low CSF glucose = tuberculous meningitis pattern.
    """
    has_meningeal = _symptom_match(x.valid_symptoms, [
        "neck stiffness", "meningeal", "kernig",
    ])
    has_csf = _symptom_match(x.valid_symptoms, [
        "elevated protein", "low glucose", "csf",
    ])
    if has_meningeal and has_csf:
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_tb_negative_stain(x):
    """
    Exclusion LF: Negative acid-fast bacilli stain or negative TB PCR.
    Note: Alone this is insufficient to rule out TB (sensitivity ~50%),
    but it provides a weak negative signal.
    """
    if _symptom_match(x.valid_symptoms, TB_EXCLUSIONS):
        return BinaryDiseaseLabel.NEGATIVE
    return BinaryDiseaseLabel.ABSTAIN


# ═══════════════════════════════════════════════════════════════════════════════
#  DENGUE Binary Labeling Functions
# ═══════════════════════════════════════════════════════════════════════════════

@labeling_function()
def lf_dengue_hallmarks(x):
    """
    Hallmark LF: Vote POSITIVE if any Dengue-specific sign is present
    (retro-orbital pain, thrombocytopenia, NS1+, petechiae, etc.).
    """
    if _symptom_match(x.valid_symptoms, DENGUE_HALLMARKS):
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_dengue_fever_ache_triad(x):
    """
    Constellation LF: Classic dengue triad — fever + (myalgia OR headache
    OR retro-orbital pain) + (rash OR petechiae).
    """
    has_fever = _symptom_match(x.valid_symptoms, ["fever", "febrile"])
    has_pain = _symptom_match(x.valid_symptoms, [
        "myalgia", "headache", "retro-orbital", "body aches", "muscle aches",
    ])
    has_rash = _symptom_match(x.valid_symptoms, ["rash", "petechiae"])
    if has_fever and has_pain and has_rash:
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_dengue_serology(x):
    """
    Lab LF: Positive dengue serology (NS1, IgM ELISA, RT-PCR).
    """
    lab_terms = [
        "ns1 antigen", "elisa igm", "dengue test", "dengue virus",
        "immunoglobulin m enzyme-linked immunosorbent assay",
    ]
    if _symptom_match(x.valid_symptoms, lab_terms):
        return BinaryDiseaseLabel.POSITIVE
    return BinaryDiseaseLabel.ABSTAIN


@labeling_function()
def lf_dengue_exclusion(x):
    """
    Exclusion LF: Normal platelet count or negative dengue serology.
    """
    if _symptom_match(x.valid_symptoms, DENGUE_EXCLUSIONS):
        return BinaryDiseaseLabel.NEGATIVE
    return BinaryDiseaseLabel.ABSTAIN


# ═══════════════════════════════════════════════════════════════════════════════
#  Model Training & Prediction
# ═══════════════════════════════════════════════════════════════════════════════

COVID_LFS = [lf_covid_hallmarks, lf_covid_respiratory_syndrome, lf_covid_lab_confirmation, lf_covid_negative_test]
TB_LFS = [lf_tb_hallmarks, lf_tb_chronic_wasting, lf_tb_meningitis, lf_tb_negative_stain]
DENGUE_LFS = [lf_dengue_hallmarks, lf_dengue_fever_ache_triad, lf_dengue_serology, lf_dengue_exclusion]


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
    """
    Stage 2: Multi-label disease prediction.
    
    Builds 3 independent binary Snorkel models (one per disease) and produces
    calibrated probability scores. Supports comorbidities.
    
    Args:
        raw_data: Original case documents (list of dicts)
        accepted_entities: Verified entities from Stage 1
        pos_threshold: Probability above which a disease is labeled POSITIVE
        neg_threshold: Probability below which a disease is labeled NEGATIVE
    
    Returns:
        DataFrame with case_id, probabilities, labels, and evidence
    """
    if not SNORKEL_AVAILABLE:
        print("Snorkel not available. Cannot run Stage 2.")
        return pd.DataFrame()

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
    print("Training COVID-19 binary classifier...")
    covid_probs, L_covid = build_disease_model(df_patients, COVID_LFS, "COVID-19")

    print("Training Tuberculosis binary classifier...")
    tb_probs, L_tb = build_disease_model(df_patients, TB_LFS, "Tuberculosis")

    print("Training Dengue binary classifier...")
    dengue_probs, L_dengue = build_disease_model(df_patients, DENGUE_LFS, "Dengue")

    # 4. Assemble results
    df_patients["p_covid19"] = covid_probs
    df_patients["p_tuberculosis"] = tb_probs
    df_patients["p_dengue"] = dengue_probs

    df_patients["covid19_label"] = df_patients["p_covid19"].apply(
        lambda p: _classify_label(p, pos_threshold, neg_threshold)
    )
    df_patients["tuberculosis_label"] = df_patients["p_tuberculosis"].apply(
        lambda p: _classify_label(p, pos_threshold, neg_threshold)
    )
    df_patients["dengue_label"] = df_patients["p_dengue"].apply(
        lambda p: _classify_label(p, pos_threshold, neg_threshold)
    )

    # 5. Determine the single most likely disease (highest probability above baseline 0.5)
    def _get_top_disease(row):
        probs = {
            "covid19": row["p_covid19"],
            "tuberculosis": row["p_tuberculosis"],
            "dengue": row["p_dengue"],
        }
        best_disease, max_p = max(probs.items(), key=lambda item: item[1])
        if max_p > 0.50:
            return best_disease
        return "UNKNOWN (Insufficient Evidence)"

    df_patients["predicted_disease"] = df_patients.apply(_get_top_disease, axis=1)

    return df_patients, {"covid": L_covid, "tb": L_tb, "dengue": L_dengue}


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
        results.append({
            "case_id": row["case_id"],
            "predicted_disease": row["predicted_disease"],
            "diagnoses": {
                "covid19": {
                    "probability": round(float(row["p_covid19"]), 4),
                    "label": row["covid19_label"],
                },
                "tuberculosis": {
                    "probability": round(float(row["p_tuberculosis"]), 4),
                    "label": row["tuberculosis_label"],
                },
                "dengue": {
                    "probability": round(float(row["p_dengue"]), 4),
                    "label": row["dengue_label"],
                },
            },
            "evidence_used": row["valid_symptoms"],
        })

    with open(report_file, "w") as f:
        json.dump(results, f, indent=4)
    print(f"\nSaved diagnosis report to {report_file}")

    # CSV labels - include predicted_disease right after case_id
    csv_df = df_patients[[
        "case_id", "predicted_disease",
        "p_covid19", "p_tuberculosis", "p_dengue",
        "covid19_label", "tuberculosis_label", "dengue_label"
    ]].copy()
    csv_df.to_csv(csv_file, index=False)
    print(f"Saved tabular labels to {csv_file}")

    return results


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 1. Load raw data
    input_file = "extracted_cases_top3_new.jsonl"
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

    # 5. Print results
    print(f"\n{'='*70}")
    print(f"  MULTI-LABEL DIAGNOSIS RESULTS")
    print(f"{'='*70}")
    for _, row in df_patients.iterrows():
        print(f"\n  [{row['case_id']}] -> Most Likely: {row['predicted_disease'].upper()}")
        print(f"    COVID-19:      P={row['p_covid19']:.4f}  -> {row['covid19_label']}")
        print(f"    Tuberculosis:  P={row['p_tuberculosis']:.4f}  -> {row['tuberculosis_label']}")
        print(f"    Dengue:        P={row['p_dengue']:.4f}  -> {row['dengue_label']}")

    # 6. Save outputs
    results = save_diagnosis_outputs(df_patients)

    # 7. Run LF diagnostics
    from evaluate_pipeline import print_lf_diagnostics
    print("\n" + "=" * 60)
    print("  STAGE 2 LABELING FUNCTION DIAGNOSTICS")
    print("=" * 60)
    print("\n--- COVID-19 LFs ---")
    print_lf_diagnostics(L_matrices["covid"], COVID_LFS)
    print("\n--- Tuberculosis LFs ---")
    print_lf_diagnostics(L_matrices["tb"], TB_LFS)
    print("\n--- Dengue LFs ---")
    print_lf_diagnostics(L_matrices["dengue"], DENGUE_LFS)

    # Cleanly exit to prevent hanging on background threads
    import sys
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)


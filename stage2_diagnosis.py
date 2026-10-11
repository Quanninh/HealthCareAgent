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
os.environ['PYTHONWARNINGS'] = 'ignore:resource_tracker:UserWarning'

# Compatibility patch for macOS Python 3.10 multiprocessing resource_tracker false-positive warning
try:
    import multiprocessing.resource_tracker
    _orig_register = multiprocessing.resource_tracker.register
    def _safe_register(name, rtype):
        if rtype == "semaphore":
            return
        return _orig_register(name, rtype)
    multiprocessing.resource_tracker.register = _safe_register
except Exception:
    pass

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
    # Dummy fallbacks to prevent NameError when defining the functions
    def labeling_function(name=None):
        def decorator(f):
            return f
        return decorator
    PandasLFApplier = None
    LabelModel = None
    MajorityLabelVoter = None

from schemas import BinaryDiseaseLabel
from clinical_knowledge import (
    DISEASE_HALLMARKS,
    DISEASE_LAB_TESTS,
    DISEASE_HALLMARK_CUIS,
    DISEASE_LAB_CUIS,
    DISEASES,
    SHARED_SYSTEMIC_SYMPTOMS,
    GENERIC_AND_SPURIOUS_CUI_BLACKLIST,
    DISEASE_E1_LABS,
    DISEASE_E2_SEROLOGY,
    DISEASE_E3_EPIDEMIOLOGY,
    DISEASE_EXCLUSIONS_LAB,
    DISEASE_HOMONYMS,
    COHORT_AND_AGGREGATE_PATTERNS,
    SINGLE_PATIENT_ANCHOR_PATTERNS,
    NON_HUMAN_PATTERNS,
    DISEASE_ORGANISMS,
    is_valid_relational_affirmation,
)
import re

# Precompile global regex patterns for high-throughput LF evaluation
COMPILED_COHORT_PATTERNS = [re.compile(p, re.IGNORECASE) for p in COHORT_AND_AGGREGATE_PATTERNS]
COMPILED_NON_HUMAN_PATTERNS = [re.compile(p, re.IGNORECASE) for p in NON_HUMAN_PATTERNS]
COMPILED_SINGLE_PATIENT_ANCHOR = re.compile(SINGLE_PATIENT_ANCHOR_PATTERNS[0], re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════════════════
#  Helpers: Text & Symptom Matching
# ═══════════════════════════════════════════════════════════════════════════════

def _symptom_match(symptoms: list, targets: list) -> bool:
    """Check if any symptom string contains any target keyword."""
    if not targets or not symptoms:
        return False
    for symptom in symptoms:
        s_lower = str(symptom).lower()
        for target in targets:
            if target in s_lower:
                return True
    return False

def _text_contains(text: str, targets: list) -> bool:
    """Check if narrative case text contains any target phrase."""
    if not text or not targets:
        return False
    t_lower = str(text).lower()
    for target in targets:
        if target in t_lower:
            return True
    return False

def _regex_matches(text: str, compiled_patterns: list) -> bool:
    """Check if text matches any compiled regex pattern."""
    if not text or not compiled_patterns:
        return False
    for p in compiled_patterns:
        if p.search(text):
            return True
    return False

def is_disease_explicitly_negated(text: str, disease_name: str) -> bool:
    """Check if narrative text explicitly contradicts/rules out this specific disease."""
    if not text:
        return False
    t_lower = text.lower()
    orgs = DISEASE_ORGANISMS.get(disease_name, [disease_name.lower()])
    for org in orgs:
        patterns = [
            rf"\b(negative|nonreactive|non-reactive|sterile)\s+(for|in)\s+[^.\n]{{0,15}}\b{org}\b",
            rf"\b(no evidence of|no growth of|tested negative for|discarded|ruled out)\s+[^.\n]{{0,15}}\b{org}\b",
            rf"\b{org}\b\s+(was|were|tested|proved)\s+(negative|ruled out|discarded|excluded|nonreactive)\b",
            rf"\b{org}\s+(negative|nonreactive|non-reactive)\b",
            rf"\bdid not belong to the {org}\b",
        ]
        for p in patterns:
            if re.search(p, t_lower):
                return True
    return False

def _count_matches(symptoms: list, targets: list) -> int:
    """Count how many distinct targets are matched."""
    count = 0
    if not targets:
        return 0
    for target in targets:
        if any(target in str(s).lower() for s in symptoms):
            count += 1
    return count


# ═══════════════════════════════════════════════════════════════════════════════
#  Dynamic Multi-Tiered Labeling Functions Factory (8 LFs per Disease)
# ═══════════════════════════════════════════════════════════════════════════════

def make_lfs_for_disease(disease_name: str):
    """
    Dynamically generate 8 multi-tiered labeling functions per disease:
      Tier 1 (E1): Gold standard confirmatory labs (votes +1)
      Tier 2 (E2): High-titer serology & pathognomonic hallmarks (votes +1)
      Tier 3A (E3): Pathognomonic hallmarks / signs (votes +1)
      Tier 3B (E3): Clinical constellation (hallmark + systemic syndrome) (votes +1)
      Tier 3C (E3): Epidemiological exposure, vectors, & animal reservoirs (votes +1)
      Tier 4A: Explicit negative lab exclusion / ruled out (votes 0)
      Tier 4B: Lexical homonyms & vaccine/discourse exclusion (votes 0)
      Tier 4C: Document scope / cohort / animal exclusion (votes 0)
    """
    hallmarks = DISEASE_HALLMARKS.get(disease_name, [])
    lab_tests = DISEASE_LAB_TESTS.get(disease_name, [])
    hallmark_cuis = DISEASE_HALLMARK_CUIS.get(disease_name, set())
    lab_cuis = DISEASE_LAB_CUIS.get(disease_name, set())
    e1_labs = DISEASE_E1_LABS.get(disease_name, [])
    e2_serology = DISEASE_E2_SEROLOGY.get(disease_name, [])
    e3_epidemiology = DISEASE_E3_EPIDEMIOLOGY.get(disease_name, [])
    exclusions_lab = DISEASE_EXCLUSIONS_LAB.get(disease_name, [])
    homonyms = DISEASE_HOMONYMS.get(disease_name, [])
    
    sanitized_name = disease_name.lower().replace('-', '_').replace(' ', '_')

    # 1. Tier 1 (E1): Confirmatory Molecular / Culture Labs
    @labeling_function(name=f"lf_{sanitized_name}_e1_confirmatory_lab")
    def lf_e1_lab(x, d_name=disease_name, e1=e1_labs, lt_cuis=lab_cuis):
        patient_cuis = getattr(x, "affirmed_cuis", set())
        if patient_cuis & lt_cuis:
            return BinaryDiseaseLabel.POSITIVE
        valid_syms = getattr(x, "valid_symptoms", [])
        if _symptom_match(valid_syms, e1):
            return BinaryDiseaseLabel.POSITIVE
        case_text = getattr(x, "case_presentation", "")
        if _text_contains(case_text, e1):
            return BinaryDiseaseLabel.POSITIVE
        title_text = getattr(x, "title", "")
        combined = f"{title_text} {case_text}"
        if is_valid_relational_affirmation(combined, d_name):
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 2. Tier 2 (E2): Strong Serology / High Titer
    @labeling_function(name=f"lf_{sanitized_name}_e2_strong_serology")
    def lf_e2_serology(x, e2=e2_serology):
        valid_syms = getattr(x, "valid_symptoms", [])
        if _symptom_match(valid_syms, e2):
            return BinaryDiseaseLabel.POSITIVE
        case_text = getattr(x, "case_presentation", "")
        if _text_contains(case_text, e2):
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 3. Tier 3A (E3): Hallmark Signs
    @labeling_function(name=f"lf_{sanitized_name}_e3_hallmarks")
    def lf_e3_hallmarks(x, hm=hallmarks, hm_cuis=hallmark_cuis):
        patient_cuis = getattr(x, "affirmed_cuis", set())
        if patient_cuis & hm_cuis:
            return BinaryDiseaseLabel.POSITIVE
        valid_syms = getattr(x, "valid_symptoms", [])
        if _symptom_match(valid_syms, hm):
            return BinaryDiseaseLabel.POSITIVE
        case_text = getattr(x, "case_presentation", "")
        if _text_contains(case_text, hm):
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 4. Tier 3B (E3): Clinical Constellation (Hallmark + Systemic Syndrome)
    @labeling_function(name=f"lf_{sanitized_name}_e3_constellation")
    def lf_e3_constellation(x, hm=hallmarks, hm_cuis=hallmark_cuis, sys_sym=SHARED_SYSTEMIC_SYMPTOMS):
        valid_syms = getattr(x, "valid_symptoms", [])
        case_text = getattr(x, "case_presentation", "")
        patient_cuis = getattr(x, "affirmed_cuis", set())
        has_systemic = _symptom_match(valid_syms, sys_sym) or _text_contains(case_text, sys_sym)
        has_specific = bool(patient_cuis & hm_cuis) or _symptom_match(valid_syms, hm) or _text_contains(case_text, hm)
        if has_systemic and has_specific:
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 5. Tier 3C (E3): Epidemiological Exposure & Vector Context
    @labeling_function(name=f"lf_{sanitized_name}_e3_epidemiology_exposure")
    def lf_e3_exposure(x, epi=e3_epidemiology, hm=hallmarks, hm_cuis=hallmark_cuis):
        if not epi:
            return BinaryDiseaseLabel.ABSTAIN
        valid_syms = getattr(x, "valid_symptoms", [])
        case_text = getattr(x, "case_presentation", "")
        patient_cuis = getattr(x, "affirmed_cuis", set())
        has_exposure = _text_contains(case_text, epi) or _symptom_match(valid_syms, epi)
        has_disease_context = (
            bool(patient_cuis & hm_cuis)
            or _symptom_match(valid_syms, hm)
            or _text_contains(case_text, hm)
        )
        if has_exposure and has_disease_context:
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 6. Tier 4A: Negative Laboratory Test Exclusion / Ruled Out (Votes 0)
    @labeling_function(name=f"lf_{sanitized_name}_negative_lab_exclusion")
    def lf_neg_lab(x, d_name=disease_name, exc=exclusions_lab):
        case_text = getattr(x, "case_presentation", "")
        valid_syms = getattr(x, "valid_symptoms", [])
        if _text_contains(case_text, exc) or _symptom_match(valid_syms, exc):
            return BinaryDiseaseLabel.NEGATIVE
        d_clean = d_name.lower().replace('_', ' ').replace('-', ' ')
        generic_neg = [
            f"negative for {d_clean}",
            f"ruled out {d_clean}",
            f"{d_clean} was ruled out",
            f"{d_clean} ruled out",
            f"tested negative for {d_clean}",
            f"no evidence of {d_clean}",
        ]
        if _text_contains(case_text, generic_neg):
            return BinaryDiseaseLabel.NEGATIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 7. Tier 4B: Lexical Homonym & Discourse / Vaccine Exclusion (Votes 0)
    @labeling_function(name=f"lf_{sanitized_name}_homonym_and_discourse_exclusion")
    def lf_homonym(x, d_name=disease_name, hom=homonyms, e1=e1_labs, lt_cuis=lab_cuis):
        if not hom:
            return BinaryDiseaseLabel.ABSTAIN
        case_text = getattr(x, "case_presentation", "")
        title_text = getattr(x, "title", "")
        combined = f"{title_text} {case_text}"
        if _text_contains(combined, hom):
            patient_cuis = getattr(x, "affirmed_cuis", set())
            valid_syms = getattr(x, "valid_symptoms", [])
            has_confirmed = (
                bool(patient_cuis & lt_cuis)
                or _symptom_match(valid_syms, e1)
                or _text_contains(case_text, e1)
            )
            if not has_confirmed:
                return BinaryDiseaseLabel.NEGATIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 8. Tier 4C: Document Scope / Cohort / Non-Human Exclusion (Votes 0)
    @labeling_function(name=f"lf_{sanitized_name}_scope_cohort_exclusion")
    def lf_scope_cohort(x, cohort_patterns=COMPILED_COHORT_PATTERNS, animal_patterns=COMPILED_NON_HUMAN_PATTERNS, anchor_pattern=COMPILED_SINGLE_PATIENT_ANCHOR):
        case_text = getattr(x, "case_presentation", "")
        title_text = getattr(x, "title", "")
        combined = f"{title_text} {case_text}"
        is_single = bool(anchor_pattern.search(case_text[:300]))
        if (not is_single and _regex_matches(combined, cohort_patterns)) or _regex_matches(combined, animal_patterns):
            return BinaryDiseaseLabel.NEGATIVE
        return BinaryDiseaseLabel.ABSTAIN


    return [
        lf_e1_lab,
        lf_e2_serology,
        lf_e3_hallmarks,
        lf_e3_constellation,
        lf_e3_exposure,
        lf_neg_lab,
        lf_homonym,
        lf_scope_cohort,
    ]


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

    # 1. Group VALID affirmed entities by case_id into CUIs and symptom tokens
    valid_by_case = {}
    cuis_by_case = {}
    for r in accepted_entities:
        cid = r["case_id"]
        if cid not in valid_by_case:
            valid_by_case[cid] = []
            cuis_by_case[cid] = set()
            
        # Ensure entity is affirmed (negated entities kept out)
        if r.get("assertion") == "negated":
            continue

        if float(r.get("probability", 1.0)) >= 0.85:
            cui = r.get("cui")
            if cui and cui not in GENERIC_AND_SPURIOUS_CUI_BLACKLIST:
                cuis_by_case[cid].add(cui)
            if r.get("standard_name"):
                valid_by_case[cid].append(r["standard_name"].lower())
            if r.get("entity"):
                valid_by_case[cid].append(r["entity"].lower())

    # 2. Build patient-level DataFrame with full-text fallback
    patient_cases = []
    for case in raw_data:
        cid = case["case_id"]
        patient_cases.append({
            "case_id": cid,
            "affirmed_cuis": cuis_by_case.get(cid, set()),
            "valid_symptoms": valid_by_case.get(cid, []),
            "case_presentation": str(case.get("case_presentation") or "").lower(),
            "title": str(case.get("title") or "").lower(),
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

    # 5. Determine the single most likely disease (satisfying Step 11 VPD Gate)
    def _get_top_disease(row):
        case_text = str(row.get("case_presentation") or "")
        title_text = str(row.get("title") or "")
        combined = f"{title_text} {case_text}"

        # Global Document Scope Gate (Protocol Steps 1 & 2): Cohorts, case series, non-human
        is_single = bool(COMPILED_SINGLE_PATIENT_ANCHOR.search(case_text[:300]))
        is_cohort = (not is_single) and _regex_matches(combined, COMPILED_COHORT_PATTERNS)
        is_animal = _regex_matches(combined, COMPILED_NON_HUMAN_PATTERNS)
        if is_cohort or is_animal:
            return "UNKNOWN (Insufficient Evidence)"

        # Sort candidate diseases by predicted probability descending
        candidates = []
        for d in DISEASES.keys():
            col = d.lower().replace('-', '_').replace(' ', '_')
            p = float(row[f"p_{col}"])
            candidates.append((d, p))
        candidates.sort(key=lambda item: item[1], reverse=True)

        for best_disease, max_p in candidates:
            # Baseline probability threshold (must exceed pos_threshold or 0.50)
            if max_p < 0.50:
                break

            e1_labs = DISEASE_E1_LABS.get(best_disease, [])
            e2_sero = DISEASE_E2_SEROLOGY.get(best_disease, [])
            hm_cuis = DISEASE_HALLMARK_CUIS.get(best_disease, set())
            lt_cuis = DISEASE_LAB_CUIS.get(best_disease, set())
            exc_labs = DISEASE_EXCLUSIONS_LAB.get(best_disease, [])
            homonyms = DISEASE_HOMONYMS.get(best_disease, [])

            patient_cuis = row.get("affirmed_cuis", set())
            valid_syms = row.get("valid_symptoms", [])

            # Confirmatory E1 evidence check
            has_e1 = (
                bool(patient_cuis & lt_cuis)
                or _symptom_match(valid_syms, e1_labs)
                or _text_contains(case_text, e1_labs)
                or is_valid_relational_affirmation(combined, best_disease)
            )

            # Check direct generic disease negation (explicit clinical exclusion)
            has_neg_lab = _text_contains(case_text, exc_labs) or _symptom_match(valid_syms, exc_labs)
            d_clean = best_disease.lower().replace('_', ' ').replace('-', ' ')
            generic_neg = [
                f"negative for {d_clean}",
                f"ruled out {d_clean}",
                f"{d_clean} was ruled out",
                f"{d_clean} ruled out",
                f"tested negative for {d_clean}",
                f"no evidence of {d_clean}",
            ]
            if _text_contains(case_text, generic_neg):
                continue

            # Check analyte-specific negation or negative lab (overridden if E1 confirmatory lab present)
            neg_flag = has_neg_lab or is_disease_explicitly_negated(combined, best_disease)
            if neg_flag and not has_e1:
                continue

            # Check for homonym trap on candidate disease
            if homonyms and _text_contains(combined, homonyms):
                if not has_e1:
                    continue

            # Protocol Step 11 VPD Gate: E1 or E2 evidence (or verified hallmark CUI or relational affirmation) required
            has_e1_or_e2 = (
                bool(patient_cuis & (hm_cuis | lt_cuis))
                or _symptom_match(valid_syms, e1_labs)
                or _symptom_match(valid_syms, e2_sero)
                or _text_contains(case_text, e1_labs)
                or _text_contains(case_text, e2_sero)
                or is_valid_relational_affirmation(combined, best_disease)
            )

            # Disease mention context (must mention the disease or its specific hallmarks)
            disease_mentioned = d_clean in combined or any(k in combined for k in DISEASE_HALLMARKS.get(best_disease, []))

            if has_e1_or_e2 and disease_mentioned:
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

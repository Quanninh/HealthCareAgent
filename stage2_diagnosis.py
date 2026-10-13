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
    parse_brucellosis_titer,
    parse_leptospirosis_titer,
    parse_leishmaniasis_titer,
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

# for the embedding sentences
def _select_representative_terms(terms: list, max_count: int = 12) -> list:
    """
    Selects up to max_count distinct, non-redundant diagnostic evidence phrases
    to keep reference embedding prompts within sentence transformer token limits.
    """
    selected = []
    for t in terms:
        t_clean = str(t).strip()
        if not t_clean:
            continue
        # Avoid exact or near-identical substring duplicates
        if any(t_clean == s or (len(t_clean) > 8 and t_clean in s) for s in selected):
            continue
        selected.append(t_clean)
        if len(selected) >= max_count:
            break
    if len(selected) < max_count:
        for t in terms:
            t_clean = str(t).strip()
            if t_clean and t_clean not in selected:
                selected.append(t_clean)
                if len(selected) >= max_count:
                    break
    return selected

# for the embedding sentences
def extract_salient_clinical_snippet(
    text: str,
    title: str,
    disease_terms: list,
    evidence_terms: list,
    target_len: int = 600,
) -> str:
    """
    Extracts a high-information focal window (~target_len chars) from clinical presentation text:
      1. Diagnostic Anchor (Tier 1): Search for explicit disease mentions. If found,
         extract a window centered around the match (± target_len // 2 chars).
      2. Confirmatory Evidence Anchor (Tier 2): Search for E1/E2 lab/serology terms. If found,
         extract window starting shortly before the match [-60, +target_len - 60].
      3. Terminal Course Fallback (Tier 3): If neither is found, fall back to the tail
         (last target_len chars), where final diagnosis/discharge summary usually resides.
    Snaps window boundaries to whitespace to avoid severing words, and prepends the case title.
    """
    if not text:
        return title.strip() if title else ""

    text_clean = text.strip()
    t_len = len(text_clean)

    if t_len <= target_len:
        snippet = text_clean
    else:
        t_lower = text_clean.lower()
        match_start = -1
        match_tier = 0
        matched_term = ""

        # Tier 1: Explicit disease mentions (prefer latest occurrence)
        for term in disease_terms:
            if not term:
                continue
            pos = t_lower.rfind(term)
            if pos != -1 and pos > match_start:
                match_start = pos
                match_tier = 1
                matched_term = term

        # Tier 2: E1 / E2 confirmatory evidence (if no Tier 1 match)
        if match_tier == 0:
            for term in evidence_terms:
                if not term:
                    continue
                pos = t_lower.rfind(term)
                if pos != -1 and pos > match_start:
                    match_start = pos
                    match_tier = 2
                    matched_term = term

        if match_tier == 1:
            # Center around the disease match (± target_len // 2)
            half = target_len // 2
            mid = match_start + len(matched_term) // 2
            raw_start = max(0, mid - half)
            raw_end = min(t_len, raw_start + target_len)
            if raw_end == t_len:
                raw_start = max(0, t_len - target_len)

            start = raw_start
            if start > 0:
                space_idx = text_clean.find(" ", start)
                if space_idx != -1 and space_idx - start <= 30 and space_idx < match_start:
                    start = space_idx + 1

            end = raw_end
            if end < t_len:
                space_idx = text_clean.rfind(" ", start, end)
                if space_idx != -1 and end - space_idx <= 30 and space_idx > match_start:
                    end = space_idx

            snippet = text_clean[start:end].strip()

        elif match_tier == 2:
            # Lead slightly before the evidence match [-60, +target_len - 60]
            raw_start = max(0, match_start - 60)
            raw_end = min(t_len, raw_start + target_len)
            if raw_end == t_len:
                raw_start = max(0, t_len - target_len)

            start = raw_start
            if start > 0:
                space_idx = text_clean.find(" ", start)
                if space_idx != -1 and space_idx - start <= 30 and space_idx <= match_start:
                    start = space_idx + 1

            end = raw_end
            if end < t_len:
                space_idx = text_clean.rfind(" ", start, end)
                if space_idx != -1 and end - space_idx <= 30 and space_idx > match_start:
                    end = space_idx

            snippet = text_clean[start:end].strip()

        else:
            # Tier 3: Tail fallback (last target_len chars)
            raw_start = max(0, t_len - target_len)
            start = raw_start
            if start > 0:
                space_idx = text_clean.find(" ", start)
                if space_idx != -1 and space_idx - start <= 30:
                    start = space_idx + 1
            snippet = text_clean[start:].strip()

    title_str = title.strip() if title else ""
    if title_str:
        clean_title = title_str.rstrip(".!?;:")
        return f"{clean_title}. {snippet}".strip()
    return snippet


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
        if d_name == "Brucellosis" and parse_brucellosis_titer(case_text):
            return BinaryDiseaseLabel.POSITIVE
        if d_name == "Leptospirosis" and parse_leptospirosis_titer(case_text, 400):
            return BinaryDiseaseLabel.POSITIVE
        if d_name == "Leishmaniasis" and parse_leishmaniasis_titer(case_text, 800):
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 2. Tier 2 (E2): Strong Serology / High Titer
    @labeling_function(name=f"lf_{sanitized_name}_e2_strong_serology")
    def lf_e2_serology(x, d_name=disease_name, e2=e2_serology):
        valid_syms = getattr(x, "valid_symptoms", [])
        if _symptom_match(valid_syms, e2):
            return BinaryDiseaseLabel.POSITIVE
        case_text = getattr(x, "case_presentation", "")
        if _text_contains(case_text, e2):
            return BinaryDiseaseLabel.POSITIVE
        if d_name == "Leptospirosis" and parse_leptospirosis_titer(case_text, 100):
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

    # 6. Dense Semantic Similarity LF (Phase 4)
    @labeling_function(name=f"lf_{sanitized_name}_dense_semantic_similarity")
    def lf_dense_sim(x, col=sanitized_name, threshold=0.70):
        sim = getattr(x, f"sim_{col}", 0.0)
        if sim >= threshold:
            return BinaryDiseaseLabel.POSITIVE
        return BinaryDiseaseLabel.ABSTAIN

    # 7. Tier 4A: Negative Laboratory Test Exclusion / Ruled Out (Votes 0)
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

    # 8. Tier 4B: Lexical Homonym & Discourse / Vaccine Exclusion (Votes 0)
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

    # 9. Tier 4C: Document Scope / Cohort / Non-Human Exclusion (Votes 0)
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
        lf_dense_sim,
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

    # Also ingest raw clinical entities from extracted_cases_100per_disease.jsonl (Phase 1)
    for case in raw_data:
        cid = case["case_id"]
        if cid not in valid_by_case:
            valid_by_case[cid] = []
            cuis_by_case[cid] = set()
        for ent in case.get("clinical_entities", []):
            if ent.get("assertion") != "negated" and ent.get("experiencer") != "family":
                span = ent.get("text_span")
                if span:
                    valid_by_case[cid].append(span.lower())

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

    # Phase 4: Precompute Dense Semantic Similarity
    try:
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity
        print("Pre-encoding cases with all-MiniLM-L6-v2 for dense semantic similarity...")
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
        
        disease_keys = list(DISEASES.keys())
        
        # Build search vocabularies for strategic extraction
        disease_search_terms = []
        for d in disease_keys:
            d_clean = d.lower().replace('_', ' ').replace('-', ' ')
            disease_search_terms.append(d_clean)
            if d.lower() != d_clean:
                disease_search_terms.append(d.lower())
        disease_search_terms = sorted(list(dict.fromkeys(disease_search_terms)), key=len, reverse=True)

        evidence_search_terms = []
        for d in disease_keys:
            for t in DISEASE_E1_LABS.get(d, []):
                if t:
                    evidence_search_terms.append(str(t).lower().strip())
            for t in DISEASE_E2_SEROLOGY.get(d, []):
                if t:
                    evidence_search_terms.append(str(t).lower().strip())
        evidence_search_terms = sorted(list(dict.fromkeys(evidence_search_terms)), key=len, reverse=True)

        # Build disease criteria reference embeddings with representative terms (safe under 256 tokens)
        crit_texts = []
        for d in disease_keys:
            d_clean = d.replace('_', ' ').replace('-', ' ')
            e1_selected = _select_representative_terms(DISEASE_E1_LABS.get(d, []), max_count=10)
            e2_selected = _select_representative_terms(DISEASE_E2_SEROLOGY.get(d, []), max_count=10)
            e1_terms = ", ".join(e1_selected)
            e2_terms = ", ".join(e2_selected)
            crit_texts.append(f"Confirmed clinical case and diagnosis of {d_clean}. Confirmatory tests: {e1_terms}. Clinical evidence: {e2_terms}.")
        crit_embs = embedder.encode(crit_texts, show_progress_bar=False)
        
        # Strategic salient extraction for patient presentations (Tier 1 disease -> Tier 2 evidence -> Tier 3 tail)
        patient_texts = [
            extract_salient_clinical_snippet(
                text=r["case_presentation"],
                title=r["title"],
                disease_terms=disease_search_terms,
                evidence_terms=evidence_search_terms,
                target_len=600,
            )
            for r in patient_cases
        ]
        patient_embs = embedder.encode(patient_texts, batch_size=64, show_progress_bar=False)
        sim_matrix = cosine_similarity(patient_embs, crit_embs)
        for idx, d in enumerate(disease_keys):
            col_name = d.lower().replace('-', '_').replace(' ', '_')
            df_patients[f"sim_{col_name}"] = sim_matrix[:, idx]
        print("Dense semantic similarities precomputed successfully.")
    except Exception as e:
        print(f"Dense semantic similarity failed ({e}). Defaulting sim columns to 0.0.")
        for d in DISEASES.keys():
            col_name = d.lower().replace('-', '_').replace(' ', '_')
            df_patients[f"sim_{col_name}"] = 0.0

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
        case_text = str(row.get("case_presentation") or "").lower()
        title_text = str(row.get("title") or "").lower()
        combined = f"{title_text} {case_text}"

        # Global Document Scope Gate (Protocol Steps 1 & 2): Cohorts, case series, non-human
        is_single = bool(COMPILED_SINGLE_PATIENT_ANCHOR.search(case_text[:300]))
        is_cohort = (not is_single) and _regex_matches(combined, COMPILED_COHORT_PATTERNS)
        is_animal = (not is_single) and _regex_matches(combined, COMPILED_NON_HUMAN_PATTERNS)
        if is_cohort or is_animal:
            return "UNKNOWN (Insufficient Evidence)"

        # Rank candidate diseases by Clinical Evidence Hierarchy + Model Probability
        candidate_scores = []
        for d in DISEASES.keys():
            col = d.lower().replace('-', '_').replace(' ', '_')
            p = float(row[f"p_{col}"])
            if p < 0.50:
                continue

            e1_labs = DISEASE_E1_LABS.get(d, [])
            e2_sero = DISEASE_E2_SEROLOGY.get(d, [])
            hm_cuis = DISEASE_HALLMARK_CUIS.get(d, set())
            lt_cuis = DISEASE_LAB_CUIS.get(d, set())
            exc_labs = DISEASE_EXCLUSIONS_LAB.get(d, [])
            homonyms = DISEASE_HOMONYMS.get(d, [])

            patient_cuis = row.get("affirmed_cuis", set())
            valid_syms = row.get("valid_symptoms", [])

            d_clean = d.lower().replace('_', ' ').replace('-', ' ')
            orgs = DISEASE_ORGANISMS.get(d, [d_clean])

            # Check title congruence and position
            title_pos = -1
            in_title = False
            for org in [d_clean] + orgs:
                pos = title_text.find(org)
                if pos != -1:
                    in_title = True
                    if title_pos == -1 or pos < title_pos:
                        title_pos = pos

            # Confirmatory E1 evidence check
            has_titer_e1 = False
            if d == "Brucellosis" and parse_brucellosis_titer(case_text):
                has_titer_e1 = True
            elif d == "Leptospirosis" and parse_leptospirosis_titer(case_text, 400):
                has_titer_e1 = True
            elif d == "Leishmaniasis" and parse_leishmaniasis_titer(case_text, 800):
                has_titer_e1 = True

            has_e1 = (
                bool(patient_cuis & lt_cuis)
                or _symptom_match(valid_syms, e1_labs)
                or _text_contains(case_text, e1_labs)
                or is_valid_relational_affirmation(combined, d)
                or has_titer_e1
            )

            # Check direct generic disease negation (only reject if no confirmatory E1)
            generic_neg = [
                f"negative for {d_clean}",
                f"ruled out {d_clean}",
                f"{d_clean} was ruled out",
                f"{d_clean} ruled out",
                f"tested negative for {d_clean}",
                f"no evidence of {d_clean}",
            ]
            has_generic_neg = _text_contains(case_text, generic_neg)
            if has_generic_neg and not has_e1:
                continue

            # Check negative lab
            has_neg_lab = _text_contains(case_text, exc_labs) or _symptom_match(valid_syms, exc_labs)
            neg_flag = has_neg_lab or is_disease_explicitly_negated(combined, d)
            if neg_flag and not has_e1:
                continue

            # Check homonyms
            if homonyms and _text_contains(combined, homonyms):
                if not has_e1:
                    continue

            # Check E2 evidence
            has_titer_e2 = False
            if d == "Leptospirosis" and parse_leptospirosis_titer(case_text, 100):
                has_titer_e2 = True

            has_e2 = (
                bool(patient_cuis & (hm_cuis | lt_cuis))
                or _symptom_match(valid_syms, e2_sero)
                or _text_contains(case_text, e2_sero)
                or has_titer_e2
            )

            hm = DISEASE_HALLMARKS.get(d, [])
            has_hm = _text_contains(case_text, hm) or _symptom_match(valid_syms, hm)
            has_constellation = in_title and (has_hm or (p >= 0.60))

            # Protocol Step 11 VPD Gate: MUST have E1, E2, or Hallmark Constellation evidence!
            if not (has_e1 or has_e2 or has_constellation):
                continue

            # Disease mention context in text
            disease_mentioned = in_title or (d_clean in combined) or any(k in combined for k in hm)
            if not disease_mentioned:
                continue

            # Composite clinical evidence score:
            # E1 confirmatory lab: 100 points
            # Title congruence: 50 points
            # Earlier title appearance bonus: up to 15 points
            # E2 strong evidence: 25 points
            # Hallmark Constellation: 10 points
            # Model probability: p * 10 points
            title_order_bonus = (15 - min(15, title_pos / 5)) if (in_title and title_pos >= 0) else 0
            score = (
                (100 if has_e1 else 0)
                + (50 if in_title else 0)
                + title_order_bonus
                + (25 if has_e2 else 0)
                + (10 if has_constellation else 0)
                + (p * 10)
            )
            candidate_scores.append((d, score, p))

        if not candidate_scores:
            return "UNKNOWN (Insufficient Evidence)"

        # Sort by clinical composite score descending, then by probability
        candidate_scores.sort(key=lambda item: (item[1], item[2]), reverse=True)
        return candidate_scores[0][0]

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

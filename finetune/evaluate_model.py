"""
evaluate_model.py

Fair & Comprehensive Clinical LLM Evaluation Suite:
Evaluates and compares the Base Model vs Fine-Tuned Model across:
    1. Fair Clinical Semantic Diagnostics (Disease Accuracy, Semantic Determination, Evidence Grounding)
    2. Standardized EHR Protocol Adherence (Header Positioning, Pathogen Subtyping, Numbered Steps, Exact Verdict)
    3. Reasoning Quality & Evidence Citation (Clinical Claim Coverage, ROUGE-1/2/L Lexical Overlap)
    4. Joint Diagnostic Success (Semantic Success vs Strict Protocol Success)
"""

import os
import sys
import json
import glob
import re
import math
import string
import argparse
import random
from typing import Dict, List, Any, Tuple, Optional, Union
from collections import defaultdict

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from finetune.dataset_loader import (
    DEFAULT_SOAP_DIR,
    DEFAULT_SYSTEM_PROMPT,
    load_soap_record,
    format_positive_diseases_prompt
)


# ================= 1. Lexical & Word Overlap: ROUGE & BLEU =================
def _get_ngrams(tokens: List[str], n: int) -> Dict[Tuple[str, ...], int]:
    ngrams = defaultdict(int)
    for i in range(len(tokens) - n + 1):
        ngrams[tuple(tokens[i:i+n])] += 1
    return ngrams


def compute_rouge_n(hyp: List[str], ref: List[str], n: int) -> float:
    hyp_ngrams = _get_ngrams(hyp, n)
    ref_ngrams = _get_ngrams(ref, n)
    if not hyp_ngrams or not ref_ngrams:
        return 0.0
    overlap = sum(min(count, ref_ngrams[ng]) for ng, count in hyp_ngrams.items() if ng in ref_ngrams)
    prec = overlap / max(1, sum(hyp_ngrams.values()))
    rec = overlap / max(1, sum(ref_ngrams.values()))
    if (prec + rec) == 0:
        return 0.0
    return 2.0 * (prec * rec) / (prec + rec)


def compute_lcs(x: List[str], y: List[str]) -> int:
    m, n = len(x), len(y)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if x[i - 1] == y[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp
    return dp[n]


def compute_rouge_l(hyp: List[str], ref: List[str]) -> float:
    if not hyp or not ref:
        return 0.0
    lcs_len = compute_lcs(hyp, ref)
    prec = lcs_len / len(hyp)
    rec = lcs_len / len(ref)
    if (prec + rec) == 0:
        return 0.0
    return 2.0 * (prec * rec) / (prec + rec)


def compute_rouge_scores(generated: str, reference: str) -> Dict[str, float]:
    hyp_toks = generated.lower().split()
    ref_toks = reference.lower().split()
    return {
        "rouge1": round(compute_rouge_n(hyp_toks, ref_toks, 1), 4),
        "rouge2": round(compute_rouge_n(hyp_toks, ref_toks, 2), 4),
        "rougeL": round(compute_rouge_l(hyp_toks, ref_toks), 4)
    }


def compute_bleu_scores(generated: str, reference: str) -> Dict[str, float]:
    hyp_toks = generated.lower().split()
    ref_toks = reference.lower().split()
    c = len(hyp_toks)
    r = len(ref_toks)
    if c == 0:
        return {"bleu1": 0.0, "bleu2": 0.0, "bleu4": 0.0}

    # Brevity penalty
    bp = 1.0 if c > r else math.exp(1.0 - (r / max(1, c)))

    def get_pn(n):
        hyp_ng = _get_ngrams(hyp_toks, n)
        ref_ng = _get_ngrams(ref_toks, n)
        tot = sum(hyp_ng.values())
        if tot == 0:
            return 0.0
        overlap = sum(min(count, ref_ng[ng]) for ng, count in hyp_ng.items() if ng in ref_ng)
        return overlap / tot

    p1 = get_pn(1)
    p2 = get_pn(2)
    p3 = get_pn(3)
    p4 = get_pn(4)

    def safe_log(p, tot):
        if p > 0:
            return math.log(p)
        return math.log(1.0 / (tot + 1)) if tot > 0 else 0.0

    b1 = bp * p1
    b2 = bp * math.exp(0.5 * (safe_log(p1, len(hyp_toks)) + safe_log(p2, max(1, len(hyp_toks) - 1)))) if p1 > 0 else 0.0
    b4 = bp * math.exp(0.25 * sum(safe_log(p, max(1, len(hyp_toks) - i)) for i, p in enumerate([p1, p2, p3, p4]))) if p1 > 0 else 0.0

    return {
        "bleu1": round(b1, 4),
        "bleu2": round(b2, 4),
        "bleu4": round(b4, 4)
    }


# ================= 2. Exact Match (EM) & Token-Level F1 Score =================
def normalize_text_for_eval(s: str) -> str:
    """Standard SQuAD / QA normalization: lower, remove punctuation and articles."""
    s = s.lower()
    s = re.sub(r'\b(a|an|the)\b', ' ', s)
    s = re.sub(r'[{}]'.format(re.escape(string.punctuation)), ' ', s)
    return ' '.join(s.split())


def compute_exact_match(pred: str, ref: str) -> float:
    return 1.0 if normalize_text_for_eval(pred) == normalize_text_for_eval(ref) else 0.0


def compute_token_f1(pred: str, ref: str) -> float:
    pred_toks = normalize_text_for_eval(pred).split()
    ref_toks = normalize_text_for_eval(ref).split()
    if not pred_toks and not ref_toks:
        return 1.0
    if not pred_toks or not ref_toks:
        return 0.0

    pred_counts = defaultdict(int)
    for t in pred_toks:
        pred_counts[t] += 1
    ref_counts = defaultdict(int)
    for t in ref_toks:
        ref_counts[t] += 1

    overlap = sum(min(count, ref_counts[t]) for t, count in pred_counts.items() if t in ref_counts)
    if overlap == 0:
        return 0.0
    prec = overlap / len(pred_toks)
    rec = overlap / len(ref_toks)
    return round((2.0 * prec * rec) / (prec + rec), 4)


# ================= 3. Semantic Similarity: BERTScore =================
def compute_bert_score(preds: List[str], refs: List[str]) -> Dict[str, float]:
    """
    Computes BERTScore (Precision, Recall, F1).
    Uses official bert_score library if installed, otherwise calculates
    contextual token cosine overlap fallback.
    """
    try:
        from bert_score import score as b_score
        P, R, F1 = b_score(preds, refs, lang="en", verbose=False)
        return {
            "bertscore_precision": round(float(P.mean()), 4),
            "bertscore_recall": round(float(R.mean()), 4),
            "bertscore_f1": round(float(F1.mean()), 4)
        }
    except Exception:
        # Fallback: character n-gram contextual token similarity
        f1_list, p_list, r_list = [], [], []
        for p_str, r_str in zip(preds, refs):
            p_toks = normalize_text_for_eval(p_str).split()
            r_toks = normalize_text_for_eval(r_str).split()
            if not p_toks or not r_toks:
                f1_list.append(1.0 if p_toks == r_toks else 0.0)
                p_list.append(1.0 if p_toks == r_toks else 0.0)
                r_list.append(1.0 if p_toks == r_toks else 0.0)
                continue

            def char_ngrams(w, n=3):
                return {w[i:i+n] for i in range(max(1, len(w)-n+1))}

            rec_matches = []
            for r_t in r_toks:
                r_ng = char_ngrams(r_t)
                best_sim = 0.0
                for p_t in p_toks:
                    if r_t == p_t:
                        best_sim = 1.0
                        break
                    p_ng = char_ngrams(p_t)
                    jacc = len(r_ng & p_ng) / max(1, len(r_ng | p_ng))
                    if jacc > best_sim:
                        best_sim = jacc
                rec_matches.append(best_sim)

            prec_matches = []
            for p_t in p_toks:
                p_ng = char_ngrams(p_t)
                best_sim = 0.0
                for r_t in r_toks:
                    if p_t == r_t:
                        best_sim = 1.0
                        break
                    r_ng = char_ngrams(r_t)
                    jacc = len(p_ng & r_ng) / max(1, len(p_ng | r_ng))
                    if jacc > best_sim:
                        best_sim = jacc
                prec_matches.append(best_sim)

            p_val = sum(prec_matches) / max(1, len(prec_matches))
            r_val = sum(rec_matches) / max(1, len(rec_matches))
            f_val = (2.0 * p_val * r_val) / (p_val + r_val) if (p_val + r_val) > 0 else 0.0
            p_list.append(p_val)
            r_list.append(r_val)
            f1_list.append(f_val)

        return {
            "bertscore_precision": round(sum(p_list) / max(1, len(p_list)), 4),
            "bertscore_recall": round(sum(r_list) / max(1, len(r_list)), 4),
            "bertscore_f1": round(sum(f1_list) / max(1, len(f1_list)), 4)
        }


# ----------------- Comprehensive Medical Disease Aliases -----------------
DISEASE_ALIASES: Dict[str, List[str]] = {
    "brucellosis": [
        "brucellosis", "brucella", "malta fever",
        "mediterranean fever", "b. melitensis", "b. abortus", "brucellar"
    ],
    "chikungunya": [
        "chikungunya", "chikv"
    ],
    "cholera": [
        "cholera", "vibrio cholerae", "v. cholerae"
    ],
    "covid-19": [
        "covid-19", "covid 19", "covid", "sars-cov-2", "sars cov 2",
        "coronavirus disease 2019", "coronavirus"
    ],
    "dengue": [
        "dengue", "dengue fever", "denv", "dengue hemorrhagic"
    ],
    "ebola_filovirus": [
        "ebola", "ebolavirus", "filovirus", "ebov", "marburg"
    ],
    "hiv_aids": [
        "hiv", "aids", "human immunodeficiency virus", "hiv-1", "hiv-2"
    ],
    "leishmaniasis": [
        "leishmaniasis", "leishmania", "kala-azar", "kala azar"
    ],
    "leptospirosis": [
        "leptospirosis", "leptospira", "weil's disease", "weils disease"
    ],
    "malaria": [
        "malaria", "plasmodium", "p. falciparum", "p. vivax", "p. ovale", "p. malariae"
    ],
    "rabies": [
        "rabies", "lyssavirus", "hydrophobia"
    ],
    "tuberculosis": [
        "tuberculosis", "tb", "mycobacterium tuberculosis", "mtb"
    ],
    "typhoid_fever": [
        "typhoid", "typhoid fever", "enteric fever", "salmonella typhi",
        "s. typhi", "salmonella enterica serovar typhi"
    ],
    "yellow_fever": [
        "yellow fever", "yfv"
    ],
    "zika": [
        "zika", "zikv", "zika virus"
    ]
}


def normalize_disease_name(disease: str) -> str:
    """Canonical key normalization for disease lookup."""
    d = disease.lower().replace("-", "_").replace(" ", "_").strip()
    if "hiv" in d or "aids" in d:
        return "hiv_aids"
    if "covid" in d or "sars" in d:
        return "covid-19"
    if "ebola" in d or "filovirus" in d:
        return "ebola_filovirus"
    if "typhoid" in d:
        return "typhoid_fever"
    if "yellow" in d:
        return "yellow_fever"
    return d


def check_disease_match(text: str, target_disease: str) -> bool:
    """
    Fair disease recognition matching:
    Evaluates whether the target disease or any recognized medical alias
    is mentioned in the clinical response.
    """
    norm_key = normalize_disease_name(target_disease)
    aliases = DISEASE_ALIASES.get(norm_key, [target_disease.lower()])

    text_lower = text.lower()
    for alias in aliases:
        # Match as whole word or boundary-delimited phrase
        pattern = r'(?:\b|_)' + re.escape(alias.replace("_", " ")) + r'(?:\b|_)'
        if re.search(pattern, text_lower):
            return True
        if alias in text_lower:
            return True
    return False


def is_target_disease_negated(text: str, target_disease: str) -> bool:
    """
    Evaluates whether the candidate target disease itself is negated or ruled out.
    Avoids false positives caused by ruling out alternate differential diagnoses
    (e.g., 'Differentials ruled out: Malaria negative' should NOT negate Brucellosis).
    """
    norm_key = normalize_disease_name(target_disease)
    aliases = DISEASE_ALIASES.get(norm_key, [target_disease.lower()])
    text_lower = text.lower()

    for alias in aliases:
        alias_clean = alias.replace("_", " ")
        neg_patterns = [
            rf'\bnegative\s+for\s+{re.escape(alias_clean)}\b',
            rf'\bnot\s+have\s+{re.escape(alias_clean)}\b',
            rf'\bruled\s+out\s+{re.escape(alias_clean)}\b',
            rf'\b{re.escape(alias_clean)}\s+(is\s+|was\s+)?ruled\s+out\b',
            rf'\b{re.escape(alias_clean)}\s+is\s+excluded\b',
            rf'\bunlikely\s+to\s+be\s+{re.escape(alias_clean)}\b',
            rf'\bexcludes?\s+{re.escape(alias_clean)}\b',
            rf'\btests?\s+negative\s+for\s+{re.escape(alias_clean)}\b',
            rf'\bno\s+evidence\s+of\s+{re.escape(alias_clean)}\b'
        ]
        if any(re.search(pat, text_lower) for pat in neg_patterns):
            return True

    # Check overall diagnosis negation
    overall_neg = [
        r'\bpatient\s+is\s+negative\b',
        r'\bdiagnosis\s*:\s*negative\b',
        r'\bnegative\s+for\s+infection\b',
        r'\bnegative\s+case\b'
    ]
    if any(re.search(pat, text_lower) for pat in overall_neg):
        return True

    return False


def extract_predicted_positive_diseases(text: str) -> List[str]:
    """
    Scans the model response across all 15 catalog diseases and extracts
    the set of diseases for which the patient is positively diagnosed.
    Distinguishes primary/positive diagnoses from diseases ruled out or listed under differentials.
    """
    if not text:
        return []

    text_lower = text.lower()

    # Identify Differential / Ruled-Out Sections
    diff_patterns = [
        r'(?:differentials?(?:\s+ruled\s+out)?|differential\s+diagnos(?:is|es)|alternative\s+diagnos(?:is|es))\s*:\s*(.*?)(?=(?:\n|\.|\;)\s*(?:plan|treatment|management|outcome|assessment|definitive)|$)',
        r'\bruled\s+out\s*:\s*(.*?)(?=(?:\n|\.|\;)\s*(?:plan|treatment|management|outcome|assessment|definitive)|$)'
    ]
    diff_text = ""
    for pat in diff_patterns:
        m = re.search(pat, text, flags=re.IGNORECASE | re.DOTALL)
        if m:
            diff_text += " " + m.group(1).lower()

    # Main text has the differential section removed so ruled-out diseases aren't counted as positive
    main_text = text_lower
    for pat in diff_patterns:
        main_text = re.sub(pat, " ", main_text, flags=re.IGNORECASE | re.DOTALL)

    predicted = []
    for dis_key, aliases in DISEASE_ALIASES.items():
        matched_in_main = False
        for alias in aliases:
            clean_a = alias.replace("_", " ")
            pat = r'(?:\b|_)' + re.escape(clean_a) + r'(?:\b|_)'
            if re.search(pat, main_text):
                matched_in_main = True
                break

        if matched_in_main:
            if not is_target_disease_negated(main_text, dis_key):
                predicted.append(dis_key)

    return sorted(list(set(predicted)))


def evaluate_open_differential_diagnosis(
    response_text: str,
    target_disease: str
) -> Dict[str, Any]:
    """
    Evaluates open-ended clinical differential diagnosis against all 15 diseases in catalog.
    No candidate disease hint was provided in the input prompt.
    Computes:
      - predicted_diseases: list of normalized disease keys predicted positive
      - target_detected: bool, whether target disease is in predicted_diseases
      - precision: TP / (TP + FP) across all 15 diseases
      - recall: TP / (TP + FN) across all 15 diseases
      - f1: harmonic mean of precision and recall
      - exact_match: bool, true if predicted_diseases == {gt_clean}
      - false_positives: list of spurious hallucinated diseases
      - num_hallucinations: count of false positives
    """
    gt_clean = normalize_disease_name(target_disease)
    predicted = extract_predicted_positive_diseases(response_text)
    pred_set = set(predicted)
    gt_set = {gt_clean}

    tp_set = pred_set & gt_set
    fp_set = pred_set - gt_set
    fn_set = gt_set - pred_set

    tp = len(tp_set)
    fp = len(fp_set)
    fn = len(fn_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = (2.0 * precision * recall / (precision + recall)) if (precision + recall) > 0 else 0.0
    exact_match = 1.0 if (pred_set == gt_set) else 0.0

    return {
        "predicted_diseases": predicted,
        "ground_truth_disease": gt_clean,
        "target_detected": (gt_clean in pred_set),
        "disease_precision": round(precision, 4),
        "disease_recall": round(recall, 4),
        "disease_f1": round(f1, 4),
        "exact_match": exact_match,
        "false_positive_hallucinations": sorted(list(fp_set)),
        "num_hallucinations": fp
    }


def extract_claims_from_presentation(clinical_presentation: str) -> List[Dict[str, str]]:
    """
    Extracts atomic clinical findings / claims from the formatted SOAP presentation
    for calculating factual evidence grounding and claim coverage.
    """
    claims = []
    if not clinical_presentation:
        return claims
    for line in clinical_presentation.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            content = line[2:].strip()
            if ":" in content:
                content = content.split(":", 1)[1].strip()
            if content:
                claims.append({"text": content, "source": "soap"})
    return claims


# ----------------- Clinical Response Parser -----------------
def parse_clinical_response(
    response_text: str,
    target_disease: str,
    claims: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Parses and evaluates the clinical output across two evaluation tracks:
      Track 1 (Fair Clinical Semantic):
        - Disease correctly diagnosed (via medical aliases)
        - Evidence-grounded reasoning (numbered, bulleted, or multi-sentence rationale)
        - Semantic clinical determination (patient is positive vs negative/equivocal)
        - Clinical claim/finding coverage
      Track 2 (Strict Protocol Format):
        - Diagnosis header preceding 'Reasoning:' or 'Definitive diagnosis:'
        - Etiology / pathogen subtyping
        - Structured step format (numbered steps or standard EHR sections)
        - Exact terminal determination token or definitive clinical diagnostic closure
    """
    text = response_text.strip()
    upper_text = text.upper()
    text_lower = text.lower()

    # 1. Header & Reasoning Body Extraction
    # Handles both legacy 'Reasoning:' and standard SOAP clinical section headers
    clinical_sec_pattern = r'(?:\n|^)\s*(?:definitive\s+)?(?:diagnosis|confirmation|diagnostic\s+confirmation|differentials?(?:\s+ruled\s+out)?|treatment(?:\s*&\s*outcome)?|plan(?:\s*&\s*outcome)?|reasoning)\s*:\s*'
    clinical_sections = re.findall(clinical_sec_pattern, text, flags=re.IGNORECASE)

    parts = re.split(r'\bReasoning\s*:\s*', text, flags=re.IGNORECASE)
    if len(parts) > 1:
        header_text = parts[0].strip()
        reasoning_text = parts[1].strip()
    else:
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        header_text = lines[0] if lines else ""
        reasoning_text = "\n".join(lines[1:]) if len(lines) > 1 else text

    # 2. Disease Identification & Open-Ended Differential Diagnosis (Option B)
    open_diag = evaluate_open_differential_diagnosis(text, target_disease)
    disease_name_correct = open_diag["target_detected"]
    disease_in_header = check_disease_match(header_text, target_disease)
    disease_precision = open_diag["disease_precision"]
    disease_recall = open_diag["disease_recall"]
    disease_f1 = open_diag["disease_f1"]
    open_exact_match = open_diag["exact_match"]
    predicted_diseases = open_diag["predicted_diseases"]
    num_hallucinations = open_diag["num_hallucinations"]
    false_positives = open_diag["false_positive_hallucinations"]

    # Subtype / Etiology detection
    has_subtype = bool(re.search(r'\([^)]+\)', header_text)) or bool(
        re.search(
            r'\b(infection|virus|species|abortus|melitensis|falciparum|vivax|'
            r'interrogans|tuberculosis|leptospira|sars-cov-2|chikv|denv|'
            r'lyssavirus|salmonella|enterica|typhi|leishmania|donovani)\b',
            header_text,
            re.IGNORECASE
        )
    )

    # 3. Clinical Reasoning Structure Evaluation
    numbered_step_markers = re.findall(r'\(\d+\)', reasoning_text)
    if not numbered_step_markers:
        numbered_step_markers = re.findall(r'^\s*\d+[\.\)]', reasoning_text, flags=re.MULTILINE)
    num_strict_steps = len(numbered_step_markers)
    num_clinical_sections = len(clinical_sections)

    has_structured_reasoning = (
        (num_strict_steps >= 2) or
        (num_clinical_sections >= 2) or
        ("REASONING:" in upper_text and len(reasoning_text) > 80)
    )

    bullet_markers = re.findall(r'^\s*[-*•]\s+', reasoning_text, flags=re.MULTILINE)
    ordinal_markers = re.findall(r'\b(first|second|third|furthermore|additionally|moreover|finally)\b', text_lower)
    word_count = len(text.split())

    has_multi_step = (
        (num_strict_steps >= 2) or
        (num_clinical_sections >= 2) or
        (len(bullet_markers) >= 2) or
        (len(ordinal_markers) >= 2)
    )
    clinical_keywords = [
        "diagnostic", "clinical", "infection", "fever", "finding", "culture", "titer",
        "diagnosis", "test", "treatment", "therapy", "confirmation", "confirmed",
        "regimen", "differentials", "pathogen", "serology", "antibody", "pcr"
    ]
    has_substantive_rationale = (word_count >= 25) and any(kw in text_lower for kw in clinical_keywords)
    evidence_grounded_reasoning = has_multi_step or has_substantive_rationale

    # 4. Clinical Evidence & Claim Coverage
    claim_coverage_rate = 0.0
    covered_claims_count = 0
    if claims:
        r_lower = text_lower
        for c in claims:
            words = [
                w for w in re.findall(r'\b[a-zA-Z]{4,}\b', c.get("text", "").lower())
                if w not in {
                    "with", "from", "that", "this", "were", "been", "have", "patient",
                    "clinical", "findings", "presented", "presents", "history", "there"
                }
            ]
            if words and any(w in r_lower for w in words[:4]):
                covered_claims_count += 1
        claim_coverage_rate = round(covered_claims_count / max(1, len(claims)), 4)

    # 5. Diagnostic Determination Evaluation
    # A. Strict Protocol Determination:
    # Supports both legacy token '-> POSITIVE' and gold-standard clinical closing 'Definitive diagnosis: <Disease>'
    strict_determination = (
        "POSITIVE DIAGNOSIS CONFIRMED" in upper_text or
        "-> POSITIVE" in upper_text or
        ("POSITIVE" in upper_text and "CONFIRMED" in upper_text and "->" in upper_text) or
        (("DEFINITIVE DIAGNOSIS:" in upper_text or "CONFIRMED DIAGNOSIS:" in upper_text) and disease_name_correct)
    )

    # B. Fair Semantic Clinical Determination:
    is_negated = is_target_disease_negated(text, target_disease)
    positive_phrases = [
        r'\bpatient\s+(is|tested|tests)\s+positive\b',
        r'\bpositive\s+for\b',
        r'\bpositive\s+diagnosis\b',
        r'\bdiagnosis\s*:\s*positive\b',
        r'\bconfirms?\s+(an?\s+)?(active\s+)?infection\b',
        r'\bconfirmed\s+(as|case\s+of)\b',
        r'\bdiagnosis\s+(of\s+[a-z0-9\-_ ]+\s+)?is\s+confirmed\b',
        r'\bmeets?\s+(the\s+)?diagnostic\s+criteria\b',
        r'\bconsistent\s+with\s+(acute\s+|active\s+)?(confirmed\s+)?infection\b',
        r'\bpositive\s+serology\b',
        r'\bpositive\s+culture\b',
        r'\btests?\s+confirm\b'
    ]
    has_semantic_positive = (
        strict_determination or
        ("diagnosis:" in text_lower and disease_name_correct) or
        ("confirmed" in text_lower and disease_name_correct) or
        any(re.search(pat, text_lower) for pat in positive_phrases) or
        ("positive" in text_lower and ("confirm" in text_lower or "diagnosis" in text_lower))
    )
    positive_determination_semantic = has_semantic_positive and not is_negated

    # 6. Joint Success Metrics
    strict_protocol_success = disease_name_correct and has_structured_reasoning and strict_determination
    fair_clinical_success = disease_name_correct and evidence_grounded_reasoning and positive_determination_semantic

    return {
        "header_diagnosis": header_text[:120],
        "disease_name_correct": disease_name_correct,
        "disease_in_header": disease_in_header,
        "disease_precision": disease_precision,
        "disease_recall": disease_recall,
        "disease_f1": disease_f1,
        "open_exact_match": open_exact_match,
        "predicted_diseases": predicted_diseases,
        "num_hallucinations": num_hallucinations,
        "false_positive_hallucinations": false_positives,
        "has_subtype": has_subtype,
        "has_structured_reasoning": has_structured_reasoning,
        "num_reasoning_steps": max(num_strict_steps, num_clinical_sections),
        "claim_coverage_rate": claim_coverage_rate,
        "determination_correct": strict_determination,
        "joint_success": strict_protocol_success,
        "evidence_grounded_reasoning": evidence_grounded_reasoning,
        "positive_determination_semantic": positive_determination_semantic,
        "strict_protocol_success": strict_protocol_success,
        "fair_clinical_success": fair_clinical_success,
        "word_count": word_count
    }


# ----------------- Metrics Aggregation -----------------
def aggregate_clinical_evaluation_metrics(records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes summary rates across Fair Clinical Semantics, Protocol Adherence, and Lexical Overlap.
    """
    total = len(records)
    if total == 0:
        return {}

    # Open Differential Diagnosis (Option B) across 15 diseases
    disease_correct_cnt = sum(1 for r in records if r["parsed"]["disease_name_correct"])
    disease_header_cnt = sum(1 for r in records if r["parsed"]["disease_in_header"])
    subtype_cnt = sum(1 for r in records if r["parsed"]["has_subtype"])

    mean_prec = sum(r["parsed"]["disease_precision"] for r in records) / total
    mean_rec = sum(r["parsed"]["disease_recall"] for r in records) / total
    mean_f1 = sum(r["parsed"]["disease_f1"] for r in records) / total
    em_cnt = sum(1 for r in records if r["parsed"]["open_exact_match"] > 0)
    avg_hallucinations = sum(r["parsed"]["num_hallucinations"] for r in records) / total

    # Reasoning
    strict_reasoning_cnt = sum(1 for r in records if r["parsed"]["has_structured_reasoning"])
    fair_reasoning_cnt = sum(1 for r in records if r["parsed"]["evidence_grounded_reasoning"])
    avg_steps = sum(r["parsed"]["num_reasoning_steps"] for r in records) / total
    avg_claim_cov = sum(r["parsed"]["claim_coverage_rate"] for r in records) / total

    # Determinations
    strict_det_cnt = sum(1 for r in records if r["parsed"]["determination_correct"])
    semantic_det_cnt = sum(1 for r in records if r["parsed"]["positive_determination_semantic"])

    # Joint successes
    strict_success_cnt = sum(1 for r in records if r["parsed"]["strict_protocol_success"])
    fair_clinical_cnt = sum(1 for r in records if r["parsed"]["fair_clinical_success"])

    # ROUGE
    r1_list = [r["rouge"]["rouge1"] for r in records]
    r2_list = [r["rouge"]["rouge2"] for r in records]
    rL_list = [r["rouge"]["rougeL"] for r in records]

    # Per-disease breakdown
    disease_groups = defaultdict(list)
    for r in records:
        disease_groups[r["target_disease"]].append(r)

    per_disease = {}
    for dis, items in sorted(disease_groups.items()):
        n = len(items)
        dis_name_corr = sum(1 for it in items if it["parsed"]["disease_name_correct"])
        dis_fair_succ = sum(1 for it in items if it["parsed"]["fair_clinical_success"])
        dis_strict_succ = sum(1 for it in items if it["parsed"]["strict_protocol_success"])
        dis_prec = sum(it["parsed"]["disease_precision"] for it in items) / n
        dis_rec = sum(it["parsed"]["disease_recall"] for it in items) / n
        dis_f1 = sum(it["parsed"]["disease_f1"] for it in items) / n
        dis_em = sum(1 for it in items if it["parsed"]["open_exact_match"] > 0) / n
        dis_claim_cov = sum(it["parsed"]["claim_coverage_rate"] for it in items) / n
        dis_r1 = sum(it["rouge"]["rouge1"] for it in items) / n
        dis_rL = sum(it["rouge"]["rougeL"] for it in items) / n
        per_disease[dis] = {
            "total_samples": n,
            "disease_name_accuracy": round(dis_name_corr / n, 4),
            "open_diagnosis_precision": round(dis_prec, 4),
            "open_diagnosis_recall": round(dis_rec, 4),
            "open_diagnosis_f1": round(dis_f1, 4),
            "exact_match_rate": round(dis_em, 4),
            "fair_clinical_success_rate": round(dis_fair_succ / n, 4),
            "strict_protocol_success_rate": round(dis_strict_succ / n, 4),
            "claim_coverage_rate": round(dis_claim_cov, 4),
            "joint_success_rate": round(dis_strict_succ / n, 4),
            "mean_rouge1": round(dis_r1, 4),
            "mean_rougeL": round(dis_rL, 4)
        }

    return {
        "total_evaluated": total,
        # Track 1: Open Differential Diagnosis Evaluation (No Candidate Hints, Multi-Disease)
        "clinical_semantic_evaluation": {
            "disease_name_accuracy": round(disease_correct_cnt / total, 4),
            "open_diagnosis_recall": round(mean_rec, 4),
            "open_diagnosis_precision": round(mean_prec, 4),
            "open_diagnosis_f1": round(mean_f1, 4),
            "open_diagnosis_exact_match_rate": round(em_cnt / total, 4),
            "avg_hallucinations_per_case": round(avg_hallucinations, 2),
            "positive_determination_accuracy": round(semantic_det_cnt / total, 4),
            "evidence_grounded_reasoning_rate": round(fair_reasoning_cnt / total, 4),
            "avg_clinical_claim_coverage": round(avg_claim_cov, 4),
            "fair_clinical_success_rate": round(fair_clinical_cnt / total, 4),
            "fair_clinical_success_count": fair_clinical_cnt
        },
        # Track 2: Standardized Protocol Adherence (Fine-Tuning Compliance)
        "protocol_adherence": {
            "disease_in_header_rate": round(disease_header_cnt / total, 4),
            "subtype_identification_rate": round(subtype_cnt / total, 4),
            "strict_structured_reasoning_rate": round(strict_reasoning_cnt / total, 4),
            "avg_reasoning_steps": round(avg_steps, 2),
            "strict_determination_rate": round(strict_det_cnt / total, 4),
            "strict_protocol_success_rate": round(strict_success_cnt / total, 4),
            "strict_protocol_success_count": strict_success_cnt
        },
        # Track 3: Lexical & Phrasing Overlap
        "lexical_overlap": {
            "mean_rouge1": round(sum(r1_list) / total, 4),
            "mean_rouge2": round(sum(r2_list) / total, 4),
            "mean_rougeL": round(sum(rL_list) / total, 4)
        },
        # Backward-compatible sections for existing harnesses:
        "disease_identification": {
            "disease_name_accuracy": round(disease_correct_cnt / total, 4),
            "disease_in_header_rate": round(disease_header_cnt / total, 4),
            "subtype_identification_rate": round(subtype_cnt / total, 4)
        },
        "reasoning_quality": {
            "structured_reasoning_rate": round(strict_reasoning_cnt / total, 4),
            "evidence_grounded_rate": round(fair_reasoning_cnt / total, 4),
            "avg_reasoning_steps": round(avg_steps, 2),
            "avg_clinical_claim_coverage": round(avg_claim_cov, 4),
            "mean_rouge1": round(sum(r1_list) / total, 4),
            "mean_rouge2": round(sum(r2_list) / total, 4),
            "mean_rougeL": round(sum(rL_list) / total, 4)
        },
        "determination": {
            "determination_accuracy": round(strict_det_cnt / total, 4),
            "semantic_determination_accuracy": round(semantic_det_cnt / total, 4)
        },
        "overall_joint_accuracy": {
            "joint_success_rate": round(strict_success_cnt / total, 4),
            "joint_success_count": strict_success_cnt,
            "fair_clinical_success_rate": round(fair_clinical_cnt / total, 4),
            "fair_clinical_success_count": fair_clinical_cnt
        },
        "per_disease_breakdown": per_disease
    }


# ----------------- Head-to-Head Comparative Analytics -----------------
def compute_model_comparison(
    base_metrics: Dict[str, Any],
    ft_metrics: Dict[str, Any],
    base_records: List[Dict[str, Any]],
    ft_records: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Computes comparative deltas across Fair Clinical and Protocol Compliance dimensions.
    """
    total = len(base_records)

    def get_delta_entry(b_val: float, ft_val: float) -> Dict[str, Any]:
        diff = ft_val - b_val
        rel_change = (diff / b_val * 100.0) if b_val > 0 else 0.0
        return {
            "base": b_val,
            "fine_tuned": ft_val,
            "delta": round(diff, 4),
            "relative_change_pct": round(rel_change, 2)
        }

    # Track 1: Open Differential Diagnosis Evaluation (No Candidate Hints, Multi-Disease)
    clinical_metrics = {
        "Target Disease Recall (Sensitivity)": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["open_diagnosis_recall"],
            ft_metrics["clinical_semantic_evaluation"]["open_diagnosis_recall"]
        ),
        "Open Diagnosis Precision (Hallucination Control)": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["open_diagnosis_precision"],
            ft_metrics["clinical_semantic_evaluation"]["open_diagnosis_precision"]
        ),
        "Open Diagnosis F1-Score": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["open_diagnosis_f1"],
            ft_metrics["clinical_semantic_evaluation"]["open_diagnosis_f1"]
        ),
        "Exact Match Diagnosis (Zero Spurious Diseases)": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["open_diagnosis_exact_match_rate"],
            ft_metrics["clinical_semantic_evaluation"]["open_diagnosis_exact_match_rate"]
        ),
        "Positive Determination (Semantic)": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["positive_determination_accuracy"],
            ft_metrics["clinical_semantic_evaluation"]["positive_determination_accuracy"]
        ),
        "Evidence-Grounded Reasoning Rate": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["evidence_grounded_reasoning_rate"],
            ft_metrics["clinical_semantic_evaluation"]["evidence_grounded_reasoning_rate"]
        ),
        "Clinical Claim / Evidence Coverage": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["avg_clinical_claim_coverage"],
            ft_metrics["clinical_semantic_evaluation"]["avg_clinical_claim_coverage"]
        ),
        "Fair Clinical Diagnostic Success": get_delta_entry(
            base_metrics["clinical_semantic_evaluation"]["fair_clinical_success_rate"],
            ft_metrics["clinical_semantic_evaluation"]["fair_clinical_success_rate"]
        )
    }

    # Track 2: Standardized Protocol Compliance
    protocol_metrics = {
        "Diagnosis Header Placement": get_delta_entry(
            base_metrics["protocol_adherence"]["disease_in_header_rate"],
            ft_metrics["protocol_adherence"]["disease_in_header_rate"]
        ),
        "Etiologic Subtype Detection": get_delta_entry(
            base_metrics["protocol_adherence"]["subtype_identification_rate"],
            ft_metrics["protocol_adherence"]["subtype_identification_rate"]
        ),
        "Strict Numbered Steps (1)...(2)...": get_delta_entry(
            base_metrics["protocol_adherence"]["strict_structured_reasoning_rate"],
            ft_metrics["protocol_adherence"]["strict_structured_reasoning_rate"]
        ),
        "Strict Determination Token (-> POSITIVE)": get_delta_entry(
            base_metrics["protocol_adherence"]["strict_determination_rate"],
            ft_metrics["protocol_adherence"]["strict_determination_rate"]
        ),
        "Strict Protocol Success Rate": get_delta_entry(
            base_metrics["protocol_adherence"]["strict_protocol_success_rate"],
            ft_metrics["protocol_adherence"]["strict_protocol_success_rate"]
        )
    }

    # Track 3: Lexical Alignment
    lexical_metrics = {
        "ROUGE-1": get_delta_entry(
            base_metrics["lexical_overlap"]["mean_rouge1"],
            ft_metrics["lexical_overlap"]["mean_rouge1"]
        ),
        "ROUGE-2": get_delta_entry(
            base_metrics["lexical_overlap"]["mean_rouge2"],
            ft_metrics["lexical_overlap"]["mean_rouge2"]
        ),
        "ROUGE-L": get_delta_entry(
            base_metrics["lexical_overlap"]["mean_rougeL"],
            ft_metrics["lexical_overlap"]["mean_rougeL"]
        )
    }

    # Backward-compatible comparison_metrics mapping:
    comparison_metrics = {
        "Disease Name Accuracy": clinical_metrics["Target Disease Recall (Sensitivity)"],
        "Open Diagnosis Precision": clinical_metrics["Open Diagnosis Precision (Hallucination Control)"],
        "Open Diagnosis F1": clinical_metrics["Open Diagnosis F1-Score"],
        "Open Exact Match": clinical_metrics["Exact Match Diagnosis (Zero Spurious Diseases)"],
        "Disease In Header Rate": protocol_metrics["Diagnosis Header Placement"],
        "Subtype Identification Rate": protocol_metrics["Etiologic Subtype Detection"],
        "Structured Reasoning Rate": protocol_metrics["Strict Numbered Steps (1)...(2)..."],
        "Avg Clinical Claim Coverage": clinical_metrics["Clinical Claim / Evidence Coverage"],
        "Determination Accuracy": protocol_metrics["Strict Determination Token (-> POSITIVE)"],
        "Joint Diagnostic Success (Disease + Reason)": protocol_metrics["Strict Protocol Success Rate"]
    }

    # Case-level Transitions (Track both Clinical Semantic and Strict Protocol)
    clin_improved, clin_retained, clin_regressed, clin_both_err = [], [], [], []
    prot_improved, prot_retained, prot_regressed, prot_both_err = [], [], [], []

    merged_cases = []
    for b_rec, ft_rec in zip(base_records, ft_records):
        b_clin = b_rec["parsed"]["fair_clinical_success"]
        ft_clin = ft_rec["parsed"]["fair_clinical_success"]

        b_prot = b_rec["parsed"]["strict_protocol_success"]
        ft_prot = ft_rec["parsed"]["strict_protocol_success"]

        # Clinical semantic transition
        if not b_clin and ft_clin:
            clin_trans = "CLINICAL_IMPROVED"
            clin_improved.append(ft_rec["pair_id"])
        elif b_clin and ft_clin:
            clin_trans = "CLINICAL_RETAINED"
            clin_retained.append(ft_rec["pair_id"])
        elif b_clin and not ft_clin:
            clin_trans = "CLINICAL_REGRESSED"
            clin_regressed.append(ft_rec["pair_id"])
        else:
            clin_trans = "CLINICAL_BOTH_INCORRECT"
            clin_both_err.append(ft_rec["pair_id"])

        # Protocol transition
        if not b_prot and ft_prot:
            prot_trans = "FT_IMPROVED"
            prot_improved.append(ft_rec["pair_id"])
        elif b_prot and ft_prot:
            prot_trans = "BOTH_CORRECT"
            prot_retained.append(ft_rec["pair_id"])
        elif b_prot and not ft_prot:
            prot_trans = "FT_REGRESSED"
            prot_regressed.append(ft_rec["pair_id"])
        else:
            prot_trans = "BOTH_INCORRECT"
            prot_both_err.append(ft_rec["pair_id"])

        merged_cases.append({
            "pair_id": ft_rec["pair_id"],
            "target_disease": ft_rec["target_disease"],
            "transition": prot_trans,  # Backward compatibility
            "clinical_transition": clin_trans,
            "base_predicted_diseases": b_rec["parsed"]["predicted_diseases"],
            "ft_predicted_diseases": ft_rec["parsed"]["predicted_diseases"],
            "base_disease_correct": b_rec["parsed"]["disease_name_correct"],
            "ft_disease_correct": ft_rec["parsed"]["disease_name_correct"],
            "base_precision": b_rec["parsed"]["disease_precision"],
            "ft_precision": ft_rec["parsed"]["disease_precision"],
            "base_recall": b_rec["parsed"]["disease_recall"],
            "ft_recall": ft_rec["parsed"]["disease_recall"],
            "base_f1": b_rec["parsed"]["disease_f1"],
            "ft_f1": ft_rec["parsed"]["disease_f1"],
            "base_exact_match": b_rec["parsed"]["open_exact_match"],
            "ft_exact_match": ft_rec["parsed"]["open_exact_match"],
            "base_hallucinations": b_rec["parsed"]["false_positive_hallucinations"],
            "ft_hallucinations": ft_rec["parsed"]["false_positive_hallucinations"],
            "base_clinical_success": b_clin,
            "ft_clinical_success": ft_clin,
            "base_protocol_success": b_prot,
            "ft_protocol_success": ft_prot,
            "base_claim_coverage": b_rec["parsed"]["claim_coverage_rate"],
            "ft_claim_coverage": ft_rec["parsed"]["claim_coverage_rate"],
            "base_rouge": b_rec["rouge"],
            "ft_rouge": ft_rec["rouge"],
            "base_diagnosis_header": b_rec["parsed"]["header_diagnosis"],
            "ft_diagnosis_header": ft_rec["parsed"]["header_diagnosis"],
            "prompt": ft_rec.get("prompt", ""),
            "base_generated_text": b_rec.get("generated_text", ""),
            "ft_generated_text": ft_rec.get("generated_text", ""),
            "ground_truth_reasoning": ft_rec.get("ground_truth_reasoning", "")
        })

    net_diagnostic_gain = len(prot_improved) - len(prot_regressed)
    net_clinical_gain = len(clin_improved) - len(clin_regressed)

    # Per-disease comparative breakdown
    all_diseases = sorted(set(
        list(base_metrics.get("per_disease_breakdown", {}).keys()) +
        list(ft_metrics.get("per_disease_breakdown", {}).keys())
    ))
    per_disease_comp = {}
    for dis in all_diseases:
        b_d = base_metrics.get("per_disease_breakdown", {}).get(dis, {})
        ft_d = ft_metrics.get("per_disease_breakdown", {}).get(dis, {})
        n_samples = ft_d.get("total_samples", b_d.get("total_samples", 0))
        per_disease_comp[dis] = {
            "samples": n_samples,
            "base_disease_accuracy": b_d.get("disease_name_accuracy", 0.0),
            "ft_disease_accuracy": ft_d.get("disease_name_accuracy", 0.0),
            "base_precision": b_d.get("open_diagnosis_precision", 0.0),
            "ft_precision": ft_d.get("open_diagnosis_precision", 0.0),
            "base_recall": b_d.get("open_diagnosis_recall", 0.0),
            "ft_recall": ft_d.get("open_diagnosis_recall", 0.0),
            "base_f1": b_d.get("open_diagnosis_f1", 0.0),
            "ft_f1": ft_d.get("open_diagnosis_f1", 0.0),
            "base_em": b_d.get("exact_match_rate", 0.0),
            "ft_em": ft_d.get("exact_match_rate", 0.0),
            "base_fair_clinical": b_d.get("fair_clinical_success_rate", 0.0),
            "ft_fair_clinical": ft_d.get("fair_clinical_success_rate", 0.0),
            "base_joint_success": b_d.get("strict_protocol_success_rate", b_d.get("joint_success_rate", 0.0)),
            "ft_joint_success": ft_d.get("strict_protocol_success_rate", ft_d.get("joint_success_rate", 0.0)),
            "clinical_delta": round(ft_d.get("fair_clinical_success_rate", 0.0) - b_d.get("fair_clinical_success_rate", 0.0), 4),
            "protocol_delta": round(ft_d.get("strict_protocol_success_rate", 0.0) - b_d.get("strict_protocol_success_rate", 0.0), 4),
            "ft_rougeL": ft_d.get("mean_rougeL", 0.0)
        }

    return {
        "total_evaluated": total,
        "clinical_metrics": clinical_metrics,
        "protocol_metrics": protocol_metrics,
        "comparison_metrics": comparison_metrics,
        "reasoning_text_deltas": lexical_metrics,
        "case_transitions": {
            # Strict Protocol transitions (backward compatibility)
            "ft_improved_count": len(prot_improved),
            "both_correct_count": len(prot_retained),
            "ft_regressed_count": len(prot_regressed),
            "both_incorrect_count": len(prot_both_err),
            "net_diagnostic_gain": net_diagnostic_gain,
            "net_diagnostic_gain_pct": round((net_diagnostic_gain / max(1, total)) * 100.0, 2),
            "win_loss_ratio": round(len(prot_improved) / max(1, len(prot_regressed)), 2),
            # Fair Clinical Semantic transitions
            "clinical_improved_count": len(clin_improved),
            "clinical_retained_count": len(clin_retained),
            "clinical_regressed_count": len(clin_regressed),
            "clinical_both_incorrect_count": len(clin_both_err),
            "net_clinical_gain": net_clinical_gain,
            "net_clinical_gain_pct": round((net_clinical_gain / max(1, total)) * 100.0, 2)
        },
        "per_disease_comparison": per_disease_comp,
        "merged_cases": merged_cases
    }


# ----------------- Formatted Report Presentation -----------------
def print_comparison_report(comparison: Dict[str, Any]):
    print("\n" + "=" * 96)
    print(" CLINICAL PERFORMANCE EVALUATION REPORT: BASE MODEL vs FINE-TUNED (QLoRA)")
    print(" Option B: Open-Ended Multi-Disease Differential Diagnosis vs Standardized EHR Protocol")
    print("=" * 96)

    # 1. Open Differential Diagnosis (Option B)
    print("\n[TRACK 1] OPEN DIFFERENTIAL DIAGNOSIS (Zero Candidate Hint, Evaluated across 15 Diseases)")
    print(f"{'Evaluation Dimension':<48} | {'Base Model':<11} | {'Fine-Tuned':<11} | {'Delta':<10} | {'Rel. Gain'}")
    print("-" * 96)
    for dim, v in comparison["clinical_metrics"].items():
        sign = "+" if v["delta"] >= 0 else ""
        delta_str = f"{sign}{v['delta'] * 100:.2f}%"
        rel_str = f"{sign}{v['relative_change_pct']:.2f}%"
        print(f"{dim:<48} | {v['base'] * 100:>9.2f}% | {v['fine_tuned'] * 100:>9.2f}% | {delta_str:>10} | {rel_str:>9}")

    # 2. Standardized Protocol Adherence
    print("\n" + "-" * 96)
    print("[TRACK 2] STANDARDIZED PROTOCOL ADHERENCE (EHR Format & Distillation Fidelity)")
    print(f"{'Protocol Dimension':<48} | {'Base Model':<11} | {'Fine-Tuned':<11} | {'Delta':<10} | {'Rel. Gain'}")
    print("-" * 96)
    for dim, v in comparison["protocol_metrics"].items():
        sign = "+" if v["delta"] >= 0 else ""
        delta_str = f"{sign}{v['delta'] * 100:.2f}%"
        rel_str = f"{sign}{v['relative_change_pct']:.2f}%"
        print(f"{dim:<48} | {v['base'] * 100:>9.2f}% | {v['fine_tuned'] * 100:>9.2f}% | {delta_str:>10} | {rel_str:>9}")

    # 3. Text Overlap on Clinical Reasoning
    print("\n" + "-" * 96)
    print("[TRACK 3] LEXICAL ALIGNMENT TO DISTILLED CLINICAL REASONING (ROUGE)")
    print(f"{'Metric':<48} | {'Base Model':<11} | {'Fine-Tuned':<11} | {'Delta':<10} | {'Rel. Gain'}")
    print("-" * 96)
    for r_k, r_v in comparison["reasoning_text_deltas"].items():
        sign = "+" if r_v["delta"] >= 0 else ""
        delta_str = f"{sign}{r_v['delta']:.4f}"
        rel_str = f"{sign}{r_v['relative_change_pct']:.2f}%"
        print(f"{r_k:<48} | {r_v['base']:>11.4f} | {r_v['fine_tuned']:>11.4f} | {delta_str:>10} | {rel_str:>9}")

    # 4. Case-Level Transitions
    trans = comparison["case_transitions"]
    tot = max(1, comparison["total_evaluated"])
    print("\n" + "-" * 96)
    print(" CASE-LEVEL CLINICAL ADJUDICATION TRANSITIONS")
    print("-" * 96)
    print("  [A] Clinical Semantic Transitions (Diagnostic Correctness):")
    print(f"      - Fine-Tuned Corrected Base (Wins)    : {trans['clinical_improved_count']:>4} ({trans['clinical_improved_count'] / tot * 100:.1f}%)")
    print(f"      - Both Models Clinically Succeeded     : {trans['clinical_retained_count']:>4} ({trans['clinical_retained_count'] / tot * 100:.1f}%)")
    print(f"      - Base Succeeded, Fine-Tuned Erred    : {trans['clinical_regressed_count']:>4} ({trans['clinical_regressed_count'] / tot * 100:.1f}%)")
    print(f"      - Both Models Erred                   : {trans['clinical_both_incorrect_count']:>4} ({trans['clinical_both_incorrect_count'] / tot * 100:.1f}%)")
    print(f"      >>> Net Clinical Diagnostic Gain      : {trans['net_clinical_gain']:+d} cases ({trans['net_clinical_gain_pct']:+.2f}%)")

    print("\n  [B] Protocol Format Transitions (Standardized EHR Closing):")
    print(f"      - Protocol Learned (Wins)              : {trans['ft_improved_count']:>4} ({trans['ft_improved_count'] / tot * 100:.1f}%)")
    print(f"      - Both Models Compliant                : {trans['both_correct_count']:>4} ({trans['both_correct_count'] / tot * 100:.1f}%)")
    print(f"      - Net Protocol Format Gain             : {trans['net_diagnostic_gain']:+d} cases ({trans['net_diagnostic_gain_pct']:+.2f}%)")

    # 5. Per-Disease Breakdown
    print("\n" + "-" * 96)
    print(f"{'Target Disease':<18} | {'Cases':<5} | {'Base Prec':<9} | {'FT Prec':<9} | {'Base Rec':<8} | {'FT Rec':<8} | {'Base EM':<8} | {'FT EM':<8} | {'FT ROUGE-L'}")
    print("-" * 96)
    for dis, s in comparison["per_disease_comparison"].items():
        print(
            f"{dis[:18]:<18} | {s['samples']:>5} | "
            f"{s['base_precision'] * 100:>8.1f}% | {s['ft_precision'] * 100:>8.1f}% | "
            f"{s['base_recall'] * 100:>7.1f}% | {s['ft_recall'] * 100:>7.1f}% | "
            f"{s['base_em'] * 100:>7.1f}% | {s['ft_em'] * 100:>7.1f}% | "
            f"{s['ft_rougeL']:>10.4f}"
        )
    print("=" * 96 + "\n")


# ----------------- Prompt Builder -----------------
def format_prompt(
    candidate_disease: Optional[str] = None,
    claims: Optional[Union[List[Dict[str, Any]], str]] = None,
    question_text: str = "Which diseases is the patient positive?",
    clinical_presentation: Optional[str] = None,
    include_candidate_hint: bool = False
) -> str:
    """
    Builds the evaluation prompt. In Option B, include_candidate_hint=False
    so no candidate disease name is revealed in the prompt.
    """
    if clinical_presentation:
        findings_text = clinical_presentation
    elif isinstance(claims, str):
        findings_text = claims
    elif isinstance(claims, list) and len(claims) > 0:
        findings_text = "\n".join("- " + c["text"] for c in claims if isinstance(c, dict) and "text" in c)
    else:
        findings_text = ""

    return format_positive_diseases_prompt(
        clinical_findings=findings_text,
        question_text=question_text,
        target_disease=candidate_disease,
        include_candidate_hint=include_candidate_hint
    )


# ----------------- Model Inference Runner -----------------
def evaluate_model_on_cases(
    model,
    tokenizer,
    test_cases: List[Dict[str, Any]],
    max_new_tokens: int = 512,
    temperature: float = 0.0,
    model_tag: str = "Model"
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Runs batch inference on test cases and computes performance metrics across both
    Fair Clinical Semantics and Protocol Compliance tracks.
    """
    import torch

    print(f"\n>>> Running Inference Evaluation for {model_tag} on {len(test_cases)} cases...")
    eval_records = []

    for idx, item in enumerate(test_cases, 1):
        target_disease = item.get("target_disease", "")
        gt_reasoning = item.get("ground_truth_reasoning", "")
        claims = item.get("claims", [])

        prompt_str = format_prompt(
            candidate_disease=target_disease,
            claims=claims,
            clinical_presentation=item.get("clinical_presentation"),
            include_candidate_hint=False
        )
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert infectious disease clinician and diagnostic adjudicator. "
                    "Evaluate patient clinical findings using structured step-by-step reasoning "
                    "to determine which diseases the patient is positive for."
                )
            },
            {"role": "user", "content": prompt_str}
        ]
        chat_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(chat_text, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                do_sample=(temperature > 0.0),
                pad_token_id=tokenizer.eos_token_id
            )

        gen_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        generated_text = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

        parsed = parse_clinical_response(generated_text, target_disease, claims)
        rouge = compute_rouge_scores(generated_text, gt_reasoning)

        eval_records.append({
            "pair_id": item.get("pair_id", f"sample_{idx}"),
            "case_id": item.get("case_id", ""),
            "target_disease": target_disease,
            "prompt": prompt_str,
            "generated_text": generated_text,
            "ground_truth_reasoning": gt_reasoning,
            "parsed": parsed,
            "rouge": rouge
        })

        if idx % 25 == 0 or idx == len(test_cases):
            cur_clin = sum(r["parsed"]["fair_clinical_success"] for r in eval_records) / len(eval_records)
            cur_prot = sum(r["parsed"]["strict_protocol_success"] for r in eval_records) / len(eval_records)
            cur_dis = sum(r["parsed"]["disease_name_correct"] for r in eval_records) / len(eval_records)
            print(f"  [{model_tag}] [{idx:>3}/{len(test_cases)}] | Disease Acc: {cur_dis * 100:.1f}% | Fair Clinical Acc: {cur_clin * 100:.1f}% | Strict Protocol Acc: {cur_prot * 100:.1f}%")

    metrics = aggregate_clinical_evaluation_metrics(eval_records)
    return eval_records, metrics


# ----------------- Main Evaluation Routine -----------------
def main():
    default_adapter = "./qlora_sft_output/final_adapter"

    parser = argparse.ArgumentParser(
        description="Fair & Comprehensive Diagnostic Evaluation on Disease Name & Step-by-Step Reasoning"
    )
    parser.add_argument(
        "--eval_mode",
        type=str,
        default="compare",
        choices=["compare", "finetuned", "base"],
        help="Evaluation mode: 'compare' (side-by-side base vs fine-tuned), 'finetuned', or 'base'"
    )
    parser.add_argument(
        "--compare_base",
        action="store_true",
        help="Explicit flag to trigger comparative evaluation between base model and fine-tuned model"
    )
    parser.add_argument(
        "--adapter_path",
        type=str,
        default=default_adapter,
        help="Path to saved LoRA adapter checkpoint"
    )
    parser.add_argument(
        "--base_model",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Base model Hugging Face ID or local path"
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        default=DEFAULT_SOAP_DIR,
        help="Path to structured clinical SOAP dataset directory or JSONL dataset"
    )
    parser.add_argument(
        "--gt_file",
        type=str,
        default=None,
        help="[Alias for --dataset_path for backwards compatibility]"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./eval_results",
        help="Output directory to save evaluation metrics and predictions"
    )
    parser.add_argument(
        "--test_ratio",
        type=float,
        default=0.15,
        help="Fraction of dataset reserved for evaluation split (default: 0.15)"
    )
    parser.add_argument(
        "--split_seed",
        type=int,
        default=42,
        help="Random seed for reproducible train/test splitting"
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="Limit number of test samples to evaluate (useful for fast validation)"
    )
    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=512,
        help="Maximum generation length per sample"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (0.0 = greedy deterministic decoding for evaluation)"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cuda", "mps", "cpu"],
        help="Target compute device: 'auto' (recommended), 'cuda', 'mps', or 'cpu'"
    )
    parser.add_argument(
        "--no_4bit",
        action="store_true",
        help="Disable 4-bit NF4 quantization and load model in bfloat16/float16 (for high-VRAM or non-CUDA systems)"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Validate comparison logic, metrics, and report formatting without requiring GPU"
    )

    args = parser.parse_args()

    if args.compare_base:
        args.eval_mode = "compare"

    os.makedirs(args.output_dir, exist_ok=True)

    data_path = args.gt_file if args.gt_file is not None else args.dataset_path

    print("=" * 80)
    print(" Clinical LLM Dual-Track Evaluation Suite (Fair Semantic vs Strict Protocol)")
    print(f" Evaluation Mode: {args.eval_mode.upper()}")
    print(f" Dataset:         {data_path}")
    print(f" Base Model:      {args.base_model}")
    if args.eval_mode in ["compare", "finetuned"]:
        print(f" LoRA Adapter:    {args.adapter_path}")
    print(f" Output Dir:      {args.output_dir}")
    print(f" Test Ratio:      {args.test_ratio} (Seed: {args.split_seed})")
    print(f" Execution:       {'DRY RUN (Simulated)' if args.dry_run else 'MODEL INFERENCE'}")
    print("=" * 80)

    # 1. Load and Split Dataset
    if not os.path.exists(data_path):
        print(f"[ERROR] Dataset path not found: {data_path}")
        sys.exit(1)

    all_cases = []
    if os.path.isdir(data_path):
        json_pattern = os.path.join(data_path, "**", "*.json")
        all_json_files = sorted(glob.glob(json_pattern, recursive=True))
        for fpath in all_json_files:
            if os.path.basename(fpath).startswith("manifest"):
                continue
            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    rec = json.load(fp)
                parsed = load_soap_record(rec)
                if parsed:
                    claims = extract_claims_from_presentation(parsed["clinical_presentation"])
                    all_cases.append({
                        "pair_id": parsed["pair_id"],
                        "target_disease": parsed["target_disease"],
                        "clinical_presentation": parsed["clinical_presentation"],
                        "ground_truth_reasoning": parsed["target_output"],
                        "claims": claims
                    })
            except Exception:
                pass
    elif data_path.endswith(".jsonl"):
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    parsed = load_soap_record(rec)
                    if parsed:
                        claims = rec.get("claims") or extract_claims_from_presentation(parsed["clinical_presentation"])
                        all_cases.append({
                            "pair_id": parsed["pair_id"],
                            "target_disease": parsed["target_disease"],
                            "clinical_presentation": parsed["clinical_presentation"],
                            "ground_truth_reasoning": parsed["target_output"],
                            "claims": claims
                        })

    random.seed(args.split_seed)
    shuffled_indices = list(range(len(all_cases)))
    random.shuffle(shuffled_indices)

    num_test = int(len(all_cases) * args.test_ratio)
    test_indices = set(shuffled_indices[:num_test])
    test_cases = [all_cases[i] for i in sorted(test_indices)]

    if args.max_samples is not None and args.max_samples < len(test_cases):
        test_cases = test_cases[:args.max_samples]

    print(f"\nTotal Dataset Cases: {len(all_cases)}")
    print(f"Selected Test Evaluation Cases: {len(test_cases)}")

    # 2. Dry-Run Mode (Simulates realistic Base vs Fine-Tuned head-to-head metrics)
    if args.dry_run:
        print("\n--- Running Dry-Run Dual-Track Comparative Validation ---")
        base_records = []
        ft_records = []

        for idx, item in enumerate(test_cases):
            gt_reasoning = item.get("ground_truth_reasoning", "")
            target_disease = item.get("target_disease", "")
            claims = item.get("claims", [])
            prompt_str = format_prompt(
                candidate_disease=target_disease,
                claims=claims,
                clinical_presentation=item.get("clinical_presentation"),
                include_candidate_hint=False
            )

            # Fine-tuned simulation: conforms to expert ground-truth protocol
            ft_text = gt_reasoning
            ft_parsed = parse_clinical_response(ft_text, target_disease, claims)
            ft_rouge = compute_rouge_scores(ft_text, gt_reasoning)

            ft_records.append({
                "pair_id": item.get("pair_id", f"sample_{idx}"),
                "target_disease": target_disease,
                "prompt": prompt_str,
                "generated_text": ft_text,
                "ground_truth_reasoning": gt_reasoning,
                "parsed": ft_parsed,
                "rouge": ft_rouge
            })

            # Base model simulation: reflects genuine zero-shot diversity in open differential diagnosis
            # Case A: Correctly deduces target disease with ruled out differentials
            # Case B: Hallucinates multiple alternate diseases (e.g. Malaria & Typhoid)
            # Case C: Inconclusive / rules out target disease
            if idx % 3 == 0:
                base_text = (
                    f"Definitive diagnosis: {target_disease}\n"
                    f"Confirmatory findings: Clinical presentation and investigations confirm {target_disease}.\n"
                    f"Differentials ruled out: Malaria, Dengue, Typhoid fever negative.\n"
                    f"Plan & Treatment: Symptomatic management and standard antimicrobial regimen."
                )
            elif idx % 3 == 1:
                base_text = (
                    f"Based on the reported symptoms and laboratory findings, the patient may have an acute infection. "
                    f"Primary differential diagnoses include Malaria and Typhoid fever; both should be investigated. "
                    f"Please consult an infectious disease specialist for further treatment."
                )
            else:
                base_text = (
                    f"The clinical findings suggest an acute systemic febrile illness, potentially related to environmental or zoonotic exposure. "
                    f"Non-specific viral infection is most likely. Supportive care and monitoring are indicated."
                )

            base_parsed = parse_clinical_response(base_text, target_disease, claims)
            base_rouge = compute_rouge_scores(base_text, gt_reasoning)

            base_records.append({
                "pair_id": item.get("pair_id", f"sample_{idx}"),
                "target_disease": target_disease,
                "prompt": prompt_str,
                "generated_text": base_text,
                "ground_truth_reasoning": gt_reasoning,
                "parsed": base_parsed,
                "rouge": base_rouge
            })

        ft_metrics = aggregate_clinical_evaluation_metrics(ft_records)
        base_metrics = aggregate_clinical_evaluation_metrics(base_records)

        comparison = compute_model_comparison(base_metrics, ft_metrics, base_records, ft_records)
        print_comparison_report(comparison)

        dry_run_summary = os.path.join(args.output_dir, "dry_run_summary.json")
        with open(dry_run_summary, "w", encoding="utf-8") as f:
            json.dump({
                "comparison": comparison,
                "base_metrics": base_metrics,
                "finetuned_metrics": ft_metrics
            }, f, indent=2)
        print(f"[SUCCESS] Dry-run evaluation completed! Saved to {dry_run_summary}")
        return

    # 3. Model Inference Execution on Hardware
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        from peft import PeftModel
    except ImportError as e:
        print(f"[ERROR] Required packages not found: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)

    # Determine optimal compute device & quantization setup
    if args.device == "auto":
        if torch.cuda.is_available():
            resolved_device = "cuda"
        elif hasattr(torch.backends, "mps") and torch.backends.mps.is_available():
            resolved_device = "mps"
        else:
            resolved_device = "cpu"
    else:
        resolved_device = args.device

    print(f"Target Hardware Device: {resolved_device.upper()}")

    print("\n[1/3] Loading Tokenizer from Base Model...")
    tokenizer = AutoTokenizer.from_pretrained(args.base_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print(f"\n[2/3] Loading Base Model ({args.base_model})...")
    model_kwargs: Dict[str, Any] = {}

    if resolved_device == "cuda" and not args.no_4bit:
        print("  -> Configuring 4-bit NormalFloat (NF4) Quantization with bfloat16 compute...")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=torch.bfloat16
        )
        model_kwargs["quantization_config"] = bnb_config
        model_kwargs["device_map"] = "auto"
    elif resolved_device == "cuda":
        print("  -> Loading in full precision bfloat16 on CUDA...")
        model_kwargs["torch_dtype"] = torch.bfloat16
        model_kwargs["device_map"] = "auto"
    elif resolved_device == "mps":
        print("  -> Loading on Apple Silicon MPS in float16...")
        model_kwargs["torch_dtype"] = torch.float16
    else:
        print("  -> Loading on CPU in float32...")
        model_kwargs["torch_dtype"] = torch.float32

    base_model = AutoModelForCausalLM.from_pretrained(args.base_model, **model_kwargs)
    if resolved_device in ["mps", "cpu"] and "device_map" not in model_kwargs:
        base_model = base_model.to(resolved_device)
    base_model.eval()

    # 4. Execute Mode
    if args.eval_mode == "compare":
        print("\n" + "=" * 80)
        print(" PHASE 1/2: Evaluating Base Model (Zero-Shot Baseline)")
        print("=" * 80)
        base_records, base_metrics = evaluate_model_on_cases(
            model=base_model,
            tokenizer=tokenizer,
            test_cases=test_cases,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            model_tag="Base Model"
        )

        print("\n" + "=" * 80)
        print(f" PHASE 2/2: Attaching LoRA Adapter from {args.adapter_path}")
        print("=" * 80)
        if not os.path.exists(args.adapter_path):
            print(f"[ERROR] LoRA adapter path does not exist: {args.adapter_path}")
            print("Please run fine-tuning first: python3 train_qlora.py")
            sys.exit(1)

        ft_model = PeftModel.from_pretrained(base_model, args.adapter_path)
        ft_model.eval()

        ft_records, ft_metrics = evaluate_model_on_cases(
            model=ft_model,
            tokenizer=tokenizer,
            test_cases=test_cases,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            model_tag="Fine-Tuned"
        )

        comparison = compute_model_comparison(base_metrics, ft_metrics, base_records, ft_records)
        print_comparison_report(comparison)

        # Save comparative summary
        comp_summary_file = os.path.join(args.output_dir, "comparison_summary.json")
        with open(comp_summary_file, "w", encoding="utf-8") as f:
            json.dump({
                "comparison": {
                    "total_evaluated": comparison["total_evaluated"],
                    "clinical_metrics": comparison["clinical_metrics"],
                    "protocol_metrics": comparison["protocol_metrics"],
                    "reasoning_text_deltas": comparison["reasoning_text_deltas"],
                    "case_transitions": comparison["case_transitions"],
                    "per_disease_comparison": comparison["per_disease_comparison"]
                },
                "base_metrics": base_metrics,
                "finetuned_metrics": ft_metrics
            }, f, indent=2)

        # Save individual cases and predictions
        cases_file = os.path.join(args.output_dir, "comparison_cases.jsonl")
        wins_file = os.path.join(args.output_dir, "clinical_wins.jsonl")
        reg_file = os.path.join(args.output_dir, "clinical_regressions.jsonl")

        with open(cases_file, "w", encoding="utf-8") as f_cases, \
             open(wins_file, "w", encoding="utf-8") as f_wins, \
             open(reg_file, "w", encoding="utf-8") as f_reg:
            for item in comparison["merged_cases"]:
                line_str = json.dumps(item, ensure_ascii=False) + "\n"
                f_cases.write(line_str)
                if item["clinical_transition"] == "CLINICAL_IMPROVED" or item["transition"] == "FT_IMPROVED":
                    f_wins.write(line_str)
                elif item["clinical_transition"] == "CLINICAL_REGRESSED" or item["transition"] == "FT_REGRESSED":
                    f_reg.write(line_str)

        print(f"[SUCCESS] Comparison Summary Saved:  {comp_summary_file}")
        print(f"[SUCCESS] All Case Comparisons Saved: {cases_file}")
        print(f"[SUCCESS] Clinical Wins Saved:        {wins_file}")
        print(f"[SUCCESS] Regressions (if any) Saved: {reg_file}")

    elif args.eval_mode == "finetuned":
        print(f"\nAttaching QLoRA Adapter from: {args.adapter_path}...")
        if not os.path.exists(args.adapter_path):
            print(f"[ERROR] LoRA adapter path does not exist: {args.adapter_path}")
            sys.exit(1)

        ft_model = PeftModel.from_pretrained(base_model, args.adapter_path)
        ft_model.eval()

        ft_records, ft_metrics = evaluate_model_on_cases(
            model=ft_model,
            tokenizer=tokenizer,
            test_cases=test_cases,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            model_tag="Fine-Tuned"
        )
        summary_file = os.path.join(args.output_dir, "eval_summary_finetuned.json")
        records_file = os.path.join(args.output_dir, "eval_records_finetuned.jsonl")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(ft_metrics, f, indent=2)
        with open(records_file, "w", encoding="utf-8") as f:
            for r in ft_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\n[SUCCESS] Fine-Tuned evaluation completed! Saved to {summary_file}")

    elif args.eval_mode == "base":
        base_records, base_metrics = evaluate_model_on_cases(
            model=base_model,
            tokenizer=tokenizer,
            test_cases=test_cases,
            max_new_tokens=args.max_new_tokens,
            temperature=args.temperature,
            model_tag="Base Model"
        )
        summary_file = os.path.join(args.output_dir, "eval_summary_base.json")
        records_file = os.path.join(args.output_dir, "eval_records_base.jsonl")
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(base_metrics, f, indent=2)
        with open(records_file, "w", encoding="utf-8") as f:
            for r in base_records:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"\n[SUCCESS] Base model evaluation completed! Saved to {summary_file}")


if __name__ == "__main__":
    main()

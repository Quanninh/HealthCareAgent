#!/usr/bin/env python3
"""
Script 02 (Proposed Method): Pair-Level High-Recall Clinical Candidate Generator
=================================================================================
Unified production pipeline for MultiCaRe Tropical & Infectious Disease analysis.

Methodological Philosophy:
--------------------------
The fundamental unit of analysis is the PAIR (case_id, target_disease), not the case.
A case may have valid clinical claims for multiple target diseases simultaneously
(multi-positive case unit). Winner-take-all suppression of secondary disease claims
is clinically invalid for this corpus.

This script is the unification of ablation experiments 02b-A and 02b-B:
  - 02b-A contribution: Negation-Safe Detection
      * Proximity negation (disease-level) is KEPT + FLAGGED, not dropped.
      * Abstract-level negation is only a signal, never a gate (A2).
      * Any disease keyword mention in case_text is a Tier 3 candidate (A3);
        Tier 3 is a high-recall MENTION layer, not an evidence filter.
  - 02b-B contribution: Pair-Level Representation
      * Each case expands into N (case, disease) pairs, one per candidate disease.
      * Per-pair BM25 physical boundary gate (drops metadata/abstract-only pairs
        with zero evidence) without cascading to other pairs of the same case.
  - BM25 is true Okapi BM25 with GLOBAL IDF/avgdl computed over all of
    cases.parquet (A1), independent of the candidate filter. It is a
    retrieval/ranking signal only; clinical validity is decided downstream.

Historical baselines (preserved as ablations):
  code/scripts/02b_create_high_recall_candidate_pool.py    [02b-A ablation]
  code/scripts/02b_B_create_candidate_pairs.py             [02b-B ablation]

Outputs:
  - Parquet: data/raw_filtered/tropical_infectious_candidate_pairs.parquet
  - Summary: reports/02_candidate_pairs_summary.json

Usage:
  python scripts/02_create_clinical_candidate_pairs.py [--output PATH] [--summary PATH]
"""

import json
import re
import argparse
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Any, Tuple, Iterable

# ---------------------------------------------------------------------------
# Path configuration (Relative to repository root)
# ---------------------------------------------------------------------------
REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CONFIG_PATH = REPO_ROOT / "config" / "disease_taxonomy.json"
DEFAULT_PARQUET_OUT = (
    REPO_ROOT / "data" / "raw_filtered"
    / "tropical_infectious_candidate_pairs.parquet"
)
DEFAULT_SUMMARY_OUT = (
    REPO_ROOT / "reports" / "02_candidate_pairs_summary.json"
)

# Auto-detect multicare_dataset_repo: inside repo or at parent workspace level
DEFAULT_RAW_DATA_DIR = (
    REPO_ROOT / "multicare_dataset_repo"
    if (REPO_ROOT / "multicare_dataset_repo").exists()
    else REPO_ROOT.parent / "multicare_dataset_repo"
)

# ---------------------------------------------------------------------------
# Helpers: Taxonomy & BM25
# ---------------------------------------------------------------------------

def load_taxonomy(config_path: Path) -> Dict[str, Any]:
    """Load disease taxonomy configuration."""
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_keyword_regex(keywords: List[str]) -> re.Pattern:
    """Build word-boundary regex for a list of disease keywords."""
    escaped = [re.escape(k.lower()) for k in keywords]
    pattern = r"\b(?:" + "|".join(escaped) + r")\b"
    return re.compile(pattern, re.IGNORECASE)


def build_disease_evidence_vocab(target_diseases: Dict[str, Any]) -> Dict[str, List[str]]:
    """
    Build clinical evidence vocabulary per disease from taxonomy,
    grounded in CDC DPDx, CDC NNDSS, and WHO case definitions.
    """
    vocab = {}
    for d_name, d_info in target_diseases.items():
        ev = d_info.get("evidence_terms", {})
        raw_terms = (
            d_info.get("keywords", []) +
            d_info.get("pathogens", []) +
            ev.get("gold_tests", []) +
            ev.get("clinical_signs", []) +
            ev.get("treatment", [])
        )
        terms = {t.strip().lower() for t in raw_terms if t and isinstance(t, str)}
        vocab[d_name] = sorted(terms, key=len, reverse=True)
    return vocab


def build_bm25_idf_table(
    all_evidence_terms: List[str],
    case_texts: Iterable[str],
) -> Tuple[Dict[str, float], int, float]:
    """
    Build GLOBAL corpus-level IDF table for true Okapi BM25.

    Statistics are computed over the entire cases.parquet universe (streamed:
    df and doc length are accumulated, texts are discarded), so IDF is
    independent of any candidate filter and stable across experiments.
    Returns (idf_table, N, avg_doc_len).

    IDF(t) = log((N - df(t) + 0.5) / (df(t) + 0.5) + 1)
    where N = total number of documents and df(t) = number of documents
    containing term t at least once. Formula follows Robertson & Sparck Jones
    with the +1 floor to keep IDF positive for high-frequency terms.

    Args:
        all_evidence_terms: Flat list of all unique evidence terms across all diseases.
        case_texts: Iterable of all case narrative texts in the universe.
    """
    N = 0
    total_len = 0

    df_counts: Dict[str, int] = {}
    # One combined alternation regex per corpus pass (longest terms first) is
    # far faster than one regex per term per document.
    combined = re.compile(
        r"\b(?:" + "|".join(re.escape(t) for t in sorted(all_evidence_terms, key=len, reverse=True)) + r")\b"
    )
    term_set = set(all_evidence_terms)
    for text in case_texts:
        N += 1
        low = text.lower()
        total_len += len(re.findall(r"\b\w+\b", low))
        found = {m.group(0) for m in combined.finditer(low)} & term_set
        for term in found:
            df_counts[term] = df_counts.get(term, 0) + 1

    if N == 0:
        return {}, 0, 445.0

    idf_table: Dict[str, float] = {}
    for term in all_evidence_terms:
        df_t = df_counts.get(term, 0)
        idf_table[term] = round(np.log((N - df_t + 0.5) / (df_t + 0.5) + 1.0), 6)

    return idf_table, N, total_len / N


def compute_bm25_score(
    evidence_terms: List[str],
    doc_text: str,
    idf_table: Dict[str, float],
    avg_doc_len: float = 445.0,
    k1: float = 1.2,
    b: float = 0.75,
) -> Tuple[float, List[str]]:
    """
    True Okapi BM25 score for case_text against disease evidence terms.

    BM25(D, Q) = sum_t [ IDF(t) * TF_norm(t, D) ]
    where TF_norm(t, D) = f(t,D)(k1+1) / (f(t,D) + k1*(1 - b + b*|D|/avgdl))
    and IDF(t) comes from corpus-level precomputation in build_bm25_idf_table().

    Args:
        evidence_terms: Disease-specific evidence vocabulary.
        doc_text: Case narrative to score.
        idf_table: Precomputed IDF weights from build_bm25_idf_table().
        avg_doc_len: Average document length in tokens (corpus-level statistic).
        k1: BM25 TF saturation parameter.
        b: BM25 document length normalization parameter.

    Returns:
        (score, matched_evidence_terms)
    """
    if not doc_text or not evidence_terms:
        return 0.0, []

    doc_lower = doc_text.lower()
    doc_tokens = re.findall(r"\b\w+\b", doc_lower)
    doc_len = len(doc_tokens)
    if doc_len == 0:
        return 0.0, []

    score = 0.0
    matched_terms: List[str] = []

    for term in evidence_terms:
        pat = r"\b" + re.escape(term) + r"\b"
        matches = len(re.findall(pat, doc_lower))
        if matches > 0:
            matched_terms.append(term)
            tf = float(matches)
            tf_norm = (tf * (k1 + 1.0)) / (
                tf + k1 * (1.0 - b + b * (doc_len / avg_doc_len))
            )
            idf = idf_table.get(term, 1.0)  # fallback: IDF=1 for unseen terms
            score += idf * tf_norm

    return round(score, 4), matched_terms


# ---------------------------------------------------------------------------
# Helpers: Document type classification
# ---------------------------------------------------------------------------

SINGLE_PATIENT_PATTERNS = [
    (re.compile(r"\ba\s+\d+[-\s]year[-\s]old\s+(male|female|man|woman|boy|girl|patient|infant|neonate|child)", re.IGNORECASE), "age_gender_presentation"),
    (re.compile(r"\bthe patient\s+(presented|was admitted|underwent|complained|reported|was diagnosed|was seen)", re.IGNORECASE), "patient_presentation"),
    (re.compile(r"\b(he|she)\s+(presented|was admitted|had|reported|denied|complained|underwent)", re.IGNORECASE), "pronoun_history"),
    (re.compile(r"\bcase\s+presentation\b", re.IGNORECASE), "case_presentation_header"),
    (re.compile(r"\ba\s+(male|female)\s+(infant|neonate|child|patient|newborn)\b", re.IGNORECASE), "demographic_intro"),
]

AGGREGATE_PATTERNS = [
    (re.compile(r"\bmedian age\b", re.IGNORECASE), "median_age"),
    (re.compile(r"\bmean age\b", re.IGNORECASE), "mean_age"),
    (re.compile(r"\b\d+(\.\d+)?%\s+of\s+(the\s+)?(patients|cases|individuals|subjects)\b", re.IGNORECASE), "percentage_cohort"),
    (re.compile(r"\b\(\s*n\s*=\s*\d+\s*\)", re.IGNORECASE), "sample_size_parenthesis"),
    (re.compile(r"\bn\s*=\s*\d+\b", re.IGNORECASE), "sample_size_n"),
    (re.compile(r"\bIQR\b"), "iqr_metric"),
    (re.compile(r"\binterquartile range\b", re.IGNORECASE), "iqr_full"),
    (re.compile(r"\bstandard deviation\b", re.IGNORECASE), "sd_metric"),
    (re.compile(r"\bcase series\b", re.IGNORECASE), "case_series_phrase"),
    (re.compile(r"\bcohort\b", re.IGNORECASE), "cohort_phrase"),
    (re.compile(r"\b(a total of|among the)\s+\d+\s+(patients|cases)\b", re.IGNORECASE), "cohort_count"),
]


def classify_document_type(case_text: str) -> Tuple[str, List[str]]:
    """Classify clinical narrative unit of analysis."""
    if not case_text:
        return "uncertain", []

    single_hits = [name for pat, name in SINGLE_PATIENT_PATTERNS if pat.search(case_text)]
    agg_hits = [name for pat, name in AGGREGATE_PATTERNS if pat.search(case_text)]
    signals = [f"single:{s}" for s in single_hits] + [f"agg:{a}" for a in agg_hits]

    if len(agg_hits) >= 2 and len(single_hits) == 0:
        return "aggregate_cohort", signals
    elif len(single_hits) >= 1 and len(agg_hits) == 0:
        return "single_patient", signals
    elif len(single_hits) >= 1 and len(agg_hits) >= 1:
        if len(agg_hits) >= 3 and len(single_hits) <= 1:
            return "aggregate_cohort", signals
        return "mixed_or_case_series", signals
    return "uncertain", signals


# ---------------------------------------------------------------------------
# Tier ordering (lower = higher retrieval confidence)
# ---------------------------------------------------------------------------

TIER_ORDER = {
    "tier1_confirmed": 1,
    "tier2_confirmed": 2,
    "tier3_case_text": 3,
    "tier1_metadata_text_present": 4,
    "tier2_abstract_text_present": 5,
    "tier1_metadata_text_negated": 6,
    "tier2_abstract_text_negated": 7,
    "tier1_metadata_only": 8,
    "tier2_abstract_only": 9,
}


# ---------------------------------------------------------------------------
# Core pipeline functions
# ---------------------------------------------------------------------------

def build_article_tier_matches(
    df_meta_raw: pd.DataFrame,
    abst_dict: Dict[str, str],
    disease_regexes: Dict[str, re.Pattern],
    disease_mesh: Dict[str, set],
    neg_re: re.Pattern,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Pass 1: Article-level signal evaluation (Tier 1: metadata, Tier 2: abstract).
    Returns (article_meta_map, art_tier_matches).
    """
    article_meta_map: Dict[str, Any] = {}
    art_tier_matches: Dict[str, Any] = {}
    tier1_arts: set = set()
    tier2_arts: set = set()

    for row in df_meta_raw.itertuples(index=False):
        art_id = row.article_id
        m_dict = row.article_metadata if isinstance(row.article_metadata, dict) else {}

        title = str(m_dict.get("title", ""))
        raw_kws = m_dict.get("keywords", [])
        kw_str = " ; ".join([str(k) for k in raw_kws]) if isinstance(raw_kws, (list, np.ndarray)) else str(raw_kws or "")

        raw_mesh = m_dict.get("mesh_terms", [])
        mesh_bases: set = set()
        if isinstance(raw_mesh, (list, np.ndarray)):
            mesh_bases = set(str(m).split("/")[0].strip().lower() for m in raw_mesh)
        elif isinstance(raw_mesh, str):
            mesh_bases = set(str(x).split("/")[0].strip().lower() for x in raw_mesh.split(";"))

        abstract = abst_dict.get(art_id, "")

        article_meta_map[art_id] = {
            "title": title,
            "keywords": raw_kws if isinstance(raw_kws, (list, np.ndarray)) else ([] if not raw_kws else [raw_kws]),
            "mesh_terms": raw_mesh if isinstance(raw_mesh, (list, np.ndarray)) else [],
            "major_mesh_terms": m_dict.get("major_mesh_terms", []),
            "doi": m_dict.get("doi", ""),
            "year": m_dict.get("year", ""),
            "journal": m_dict.get("journal", ""),
            "abstract": abstract,
        }

        dis_hits: Dict[str, Any] = {}
        for d_name, regex in disease_regexes.items():
            mesh_hit = bool(disease_mesh[d_name] & mesh_bases)
            kw_hit = bool(regex.search(kw_str)) if kw_str else False
            title_hit = bool(regex.search(title)) if title else False

            signals = []
            if mesh_hit:
                signals.append("mesh")
            if kw_hit:
                signals.append("keywords")
            if title_hit:
                signals.append("title")

            if signals:
                dis_hits[d_name] = ("tier1_metadata", signals)
                tier1_arts.add(art_id)
            elif abstract and regex.search(abstract):
                # A2: Abstract negation is NOT a gate here.
                # Any abstract disease mention creates a Tier 2 candidate.
                # Negation becomes a signal at case-level (evaluate_case_candidates),
                # not a suppression at article level.
                dis_hits[d_name] = ("tier2_abstract", ["abstract"])
                tier2_arts.add(art_id)

        if dis_hits:
            art_tier_matches[art_id] = dis_hits

    print(f"  - Tier 1 articles matched: {len(tier1_arts):,}")
    print(f"  - Tier 2 additional articles: {len(tier2_arts - tier1_arts):,}")
    print(f"  - Total Tier 1 + Tier 2 articles: {len(art_tier_matches):,}")
    return article_meta_map, art_tier_matches


def evaluate_case_candidates(
    case_text: str,
    art_matches: Dict[str, Any],
    disease_regexes: Dict[str, re.Pattern],
    disease_conf_regexes: Dict[str, re.Pattern],
    disease_neg_regexes: Dict[str, re.Pattern],
    disease_evidence_vocab: Dict[str, List[str]],
    idf_table: Dict[str, float],
    avg_doc_len: float,
    broad_conf_re: re.Pattern,
) -> List[Dict[str, Any]]:
    """
    Evaluate all candidate diseases for a single case narrative.

    02b-A Negation-Safe logic:
      - Proximity negation: KEEP + flag (has_negation_mention = True)
      - Broad document negation gate: REMOVED
      - Per-pair BM25 gate: applied downstream in apply_per_pair_bm25_gate()

    Returns list of candidate dicts sorted by (tier_rank ASC, evidence_score DESC).
    """
    case_has_conf = bool(broad_conf_re.search(case_text))
    matched_dict: Dict[str, Tuple[str, List[str]]] = {}

    # Phase 1: Cross-validate article-level disease signals against case narrative
    for d_name, (art_tier, art_signals) in art_matches.items():
        has_dis_neg = bool(disease_neg_regexes[d_name].search(case_text))
        text_hit = bool(disease_regexes[d_name].search(case_text))
        conf_hit = bool(disease_conf_regexes[d_name].search(case_text)) if case_has_conf else False

        signals = list(art_signals)
        if has_dis_neg:
            signals.append("proximity_neg_present")

        if conf_hit:
            tier = art_tier.replace("metadata", "confirmed").replace("abstract", "confirmed")
            signals.append("case_text_confirmed")
            matched_dict[d_name] = (tier, signals)
        elif text_hit:
            if has_dis_neg:
                signals.append("case_text_negated")
                matched_dict[d_name] = (art_tier + "_text_negated", signals)
            else:
                signals.append("case_text_present")
                matched_dict[d_name] = (art_tier + "_text_present", signals)
        else:
            signals.append("narrative_unmentioned")
            matched_dict[d_name] = (art_tier + "_only", signals)

    # Phase 2: Tier 3 — any disease mention in case narrative not captured by article metadata.
    # A3: High-recall candidate generator: any disease keyword mention is sufficient.
    # Confirmation phrases are treated as a stronger sub-signal, not a prerequisite.
    # Clinical Claim Agent is responsible for downstream specificity (FP handling).
    for d_name, d_regex in disease_regexes.items():
        if d_name not in matched_dict and d_regex.search(case_text):
            has_dis_neg = bool(disease_neg_regexes[d_name].search(case_text))
            conf_hit = bool(disease_conf_regexes[d_name].search(case_text)) if case_has_conf else False
            signals = ["case_text_mentioned"]
            if conf_hit:
                signals.append("case_text_confirmed")
            if has_dis_neg:
                signals.append("proximity_neg_present")
            matched_dict[d_name] = ("tier3_case_text", signals)

    if not matched_dict:
        return []

    candidates = []
    for d, (tier, sigs) in matched_dict.items():
        score, m_terms = compute_bm25_score(disease_evidence_vocab.get(d, []), case_text, idf_table, avg_doc_len=avg_doc_len)
        candidates.append({
            "disease": d,
            "tier": tier,
            "tier_rank": TIER_ORDER.get(tier, 99),
            "evidence_score": score,
            "matched_evidence_terms": m_terms,
            "signals": sigs,
            "has_negation": ("proximity_neg_present" in sigs or "case_text_negated" in sigs),
        })

    candidates.sort(key=lambda x: (x["tier_rank"], -x["evidence_score"]))
    return candidates


def apply_per_pair_bm25_gate(
    candidates: List[Dict[str, Any]]
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    02b-B Per-Pair BM25 Physical Boundary Gate.

    Drops a (case, disease) pair if and only if:
      - disease is only present in article metadata/abstract (not case narrative), AND
      - BM25 clinical evidence score in case_text is 0.

    Dropping one pair does NOT cascade to other pairs for the same case.
    Returns (valid_candidates, dropped_candidates).
    """
    valid = []
    dropped = []
    for cand in candidates:
        noise = cand["tier"] in ("tier1_metadata_only", "tier2_abstract_only") and cand["evidence_score"] == 0.0
        (dropped if noise else valid).append(cand)
    return valid, dropped


def load_image_map(cap_path: Path) -> Dict[str, List[Dict[str, Any]]]:
    """Load diagnostic image annotations keyed by patient_id."""
    case_images_map: Dict[str, List[Dict[str, Any]]] = {}
    if not cap_path.exists():
        print("  Warning: captions_and_labels.csv not found; proceeding without image attachments.")
        return case_images_map

    df_caps = pd.read_csv(cap_path, low_memory=False)
    diagnostic_types = {"radiology", "pathology", "medical_photograph"}
    df_caps_diag = df_caps[df_caps["image_type"].isin(diagnostic_types)].copy()
    print(f"  Found {len(df_caps_diag):,} diagnostic images in MultiCaRe.")

    for row in df_caps_diag.itertuples(index=False):
        pid = row.patient_id
        if pid not in case_images_map:
            case_images_map[pid] = []
        case_images_map[pid].append({
            "file_id": row.file_id,
            "file": row.file,
            "image_type": row.image_type,
            "image_subtype": row.image_subtype if pd.notna(row.image_subtype) else "",
            "caption": str(row.caption).strip() if pd.notna(row.caption) else "",
            "license": row.license if pd.notna(row.license) else "",
        })
    return case_images_map


def attach_images(case_id: str, image_map: Dict[str, List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Return image metadata block for a given case_id."""
    imgs = image_map.get(case_id, [])
    return {
        "has_images": bool(imgs),
        "image_count": len(imgs),
        "image_files": [x["file"] for x in imgs],
        "image_types": list({x["image_type"] for x in imgs if x["image_type"]}),
        "image_captions": [x["caption"] for x in imgs if x["caption"]],
        "image_metadata": imgs,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Script 02 (Proposed Method): Pair-Level High-Recall Clinical Candidate Generator. "
            "Unified pipeline replacing the two-step 02b-A -> 02b-B sequence."
        )
    )
    parser.add_argument(
        "--config", type=str, default=str(DEFAULT_CONFIG_PATH),
        help=f"Disease taxonomy configuration JSON path (default: {DEFAULT_CONFIG_PATH})",
    )
    parser.add_argument(
        "--raw-data-dir", type=str, default=str(DEFAULT_RAW_DATA_DIR),
        help=f"Path to multicare_dataset_repo directory (default: {DEFAULT_RAW_DATA_DIR})",
    )
    parser.add_argument(
        "--output", type=str, default=str(DEFAULT_PARQUET_OUT),
        help=f"Output parquet path (default: {DEFAULT_PARQUET_OUT})",
    )
    parser.add_argument(
        "--summary", type=str, default=str(DEFAULT_SUMMARY_OUT),
        help=f"Output summary JSON path (default: {DEFAULT_SUMMARY_OUT})",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Compute and print stats without writing any output files.",
    )
    return parser.parse_args()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    args = parse_args()
    config_path = Path(args.config)
    raw_data_dir = Path(args.raw_data_dir)
    output_parquet = Path(args.output)
    summary_path = Path(args.summary)

    print("=" * 80)
    print("SCRIPT 02 (PROPOSED METHOD): PAIR-LEVEL HIGH-RECALL CANDIDATE GENERATOR")
    print("=" * 80)
    print(f"Taxonomy Config:  {config_path}")
    print(f"Raw Data Dir:     {raw_data_dir}")
    print(f"Output Parquet:   {output_parquet}")
    print(f"Summary Report:   {summary_path}")
    if args.dry_run:
        print("** DRY RUN -- no files will be written **")
    print("=" * 80)

    # ------------------------------------------------------------------
    # Step 0: Load taxonomy and compile patterns
    # ------------------------------------------------------------------
    taxonomy = load_taxonomy(config_path)
    target_diseases = taxonomy["target_diseases"]
    print(f"\nLoaded {len(target_diseases)} target disease definitions.")

    neg_re = re.compile(
        r"(?:negative for|ruled out|no evidence of|non-reactive|was excluded|tested negative)",
        re.IGNORECASE,
    )
    broad_conf_re = re.compile(
        r"(?:confirmed|diagnosed with|positive for|cultures grew|biopsy revealed)",
        re.IGNORECASE,
    )

    disease_regexes: Dict[str, re.Pattern] = {}
    disease_mesh: Dict[str, set] = {}
    disease_conf_regexes: Dict[str, re.Pattern] = {}
    disease_neg_regexes: Dict[str, re.Pattern] = {}

    for d_name, d_info in target_diseases.items():
        all_terms = d_info["keywords"] + d_info.get("pathogens", []) + [d_name.lower()]
        disease_regexes[d_name] = build_keyword_regex(all_terms)
        disease_mesh[d_name] = {m.lower() for m in d_info["mesh_terms"]}

        dis_pat = r"\b(?:" + "|".join(re.escape(k.lower()) for k in all_terms) + r")\b"
        disease_conf_regexes[d_name] = re.compile(
            r"(?:confirmed|diagnosed with|positive for|cultures grew|biopsy revealed)"
            r"(?:\s+\w+){0,3}\s+" + dis_pat,
            re.IGNORECASE,
        )
        disease_neg_regexes[d_name] = re.compile(
            r"(?:negative for|ruled out|no evidence of|non-reactive|was excluded|tested negative)"
            r"(?:\s+\w+){0,3}\s+" + dis_pat,
            re.IGNORECASE,
        )

    disease_evidence_vocab = build_disease_evidence_vocab(target_diseases)

    # ------------------------------------------------------------------
    # Step 1: Article-level signals (Tier 1 metadata + Tier 2 abstract)
    # ------------------------------------------------------------------
    meta_path = raw_data_dir / "metadata.parquet"
    abst_path = raw_data_dir / "abstracts.parquet"

    print(f"\n[1/5] Loading metadata from {meta_path}...")
    df_meta_raw = pd.read_parquet(meta_path)

    print(f"[1/5] Loading abstracts from {abst_path}...")
    df_abst = pd.read_parquet(abst_path)
    abst_dict = dict(zip(df_abst["article_id"], df_abst["abstract"].fillna("")))

    print("Evaluating Tier 1 (Metadata) & Tier 2 (Abstract) article-level signals...")
    article_meta_map, art_tier_matches = build_article_tier_matches(
        df_meta_raw, abst_dict, disease_regexes, disease_mesh, neg_re
    )

    # ------------------------------------------------------------------
    # Step 2: Build GLOBAL IDF table (true Okapi BM25) over ALL cases in
    # cases.parquet, streamed. Independent of the candidate filter.
    # ------------------------------------------------------------------
    print("\n[2/5] Building global BM25 IDF table over entire cases.parquet...")
    cases_path = raw_data_dir / "cases.parquet"

    def _iter_all_case_texts():
        for row in pd.read_parquet(cases_path).itertuples(index=False):
            for case in row.cases:
                ct = case.get("case_text", "")
                if ct:
                    yield ct

    all_evidence_terms_flat = sorted({
        term
        for terms in disease_evidence_vocab.values()
        for term in terms
    })
    idf_table, n_docs, avg_doc_len_corpus = build_bm25_idf_table(
        all_evidence_terms_flat, _iter_all_case_texts()
    )
    print(f"  - Global corpus size:         {n_docs:,} texts")
    print(f"  - Average document length:    {avg_doc_len_corpus:.1f} tokens")
    print(f"  - IDF table entries:          {len(idf_table):,} unique terms")

    # ------------------------------------------------------------------
    # Step 3: Case-level scan + pair construction (single pass, no intermediate parquet)
    # ------------------------------------------------------------------
    print(f"\n[3/5] Constructing candidate pairs from {cases_path}...")
    df_cases_raw = pd.read_parquet(cases_path)

    cap_path = raw_data_dir / "captions_and_labels.csv"
    image_map = load_image_map(cap_path)


    pair_records: List[Dict[str, Any]] = []
    stats = {
        "total_cases_scanned": 0,
        "cases_with_candidates": 0,
        "raw_candidate_signals": 0,
        "pairs_dropped_noise": 0,
        "pairs_retained": 0,
    }

    for row in df_cases_raw.itertuples(index=False):
        art_id = row.article_id
        meta_info = article_meta_map.get(art_id, {
            "title": "", "keywords": [], "mesh_terms": [], "major_mesh_terms": [],
            "doi": "", "year": "", "journal": "", "abstract": "",
        })
        art_matches = art_tier_matches.get(art_id, {})

        for case in row.cases:
            case_id = case.get("case_id")
            case_text = case.get("case_text", "")
            stats["total_cases_scanned"] += 1

            candidates = evaluate_case_candidates(
                case_text=case_text,
                art_matches=art_matches,
                disease_regexes=disease_regexes,
                disease_conf_regexes=disease_conf_regexes,
                disease_neg_regexes=disease_neg_regexes,
                disease_evidence_vocab=disease_evidence_vocab,
                idf_table=idf_table,
                avg_doc_len=avg_doc_len_corpus,
                broad_conf_re=broad_conf_re,
            )
            if not candidates:
                continue

            stats["raw_candidate_signals"] += len(candidates)
            valid_cands, dropped_cands = apply_per_pair_bm25_gate(candidates)
            stats["pairs_dropped_noise"] += len(dropped_cands)

            if not valid_cands:
                continue

            stats["cases_with_candidates"] += 1
            stats["pairs_retained"] += len(valid_cands)

            doc_type, doc_signals = classify_document_type(case_text)
            img_block = attach_images(case_id, image_map)
            valid_disease_names = [c["disease"] for c in valid_cands]

            for cand in valid_cands:
                d_name = cand["disease"]
                co_occurring = [d for d in valid_disease_names if d != d_name]

                pair_records.append({
                    # Primary composite identifier
                    "pair_id":                 f"{case_id}::{d_name}",
                    "case_id":                 case_id,
                    "target_disease":          d_name,
                    # Retrieval signals for this specific (case, disease) pair
                    "confidence_tier":         cand["tier"],
                    "tier_rank":               int(cand["tier_rank"]),
                    "evidence_score":          float(cand["evidence_score"]),
                    "matched_evidence_terms":  list(cand["matched_evidence_terms"]),
                    "match_signals":           list(cand["signals"]),
                    "has_negation_mention":    bool(cand["has_negation"]),
                    # Multi-disease context
                    "case_candidate_count":    len(valid_cands),
                    "co_occurring_candidates": co_occurring,
                    # Clinical narrative and article metadata
                    "article_id":              art_id,
                    "title":                   meta_info["title"],
                    "abstract":                meta_info["abstract"],
                    "case_text":               case_text,
                    "age":                     case.get("age"),
                    "gender":                  case.get("gender"),
                    "year":                    meta_info["year"],
                    "journal":                 meta_info["journal"],
                    "doi":                     meta_info["doi"],
                    "keywords":                meta_info["keywords"],
                    "mesh_terms":              meta_info["mesh_terms"],
                    "major_mesh_terms":        meta_info["major_mesh_terms"],
                    "document_type":           doc_type,
                    "document_type_signals":   doc_signals,
                    # Multimodal attachments
                    **img_block,
                })

    # ------------------------------------------------------------------
    # Step 3: Build DataFrame and validate
    # ------------------------------------------------------------------
    df_pairs = pd.DataFrame(pair_records)
    total_pairs = len(df_pairs)
    n_unique_pair_ids = df_pairs["pair_id"].nunique()
    assert n_unique_pair_ids == total_pairs, (
        f"Duplicate pair_ids found: {total_pairs} records but {n_unique_pair_ids} unique pair_ids."
    )

    unique_cases = df_pairs["case_id"].nunique()
    unique_articles = df_pairs["article_id"].nunique()

    # ------------------------------------------------------------------
    # Step 4: Print summary statistics
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("CANDIDATE PAIR GENERATION SUMMARY")
    print("=" * 60)
    print(f"  Total cases scanned:           {stats['total_cases_scanned']:>8,}")
    print(f"  Cases with >=1 valid pair:     {stats['cases_with_candidates']:>8,}")
    print(f"  Raw candidate signals:         {stats['raw_candidate_signals']:>8,}")
    print(f"  Dropped noise pairs (BM25=0): {stats['pairs_dropped_noise']:>8,}")
    print(f"  Retained candidate pairs:      {stats['pairs_retained']:>8,}")
    print(f"  Unique case units:             {unique_cases:>8,}")
    print(f"  Unique articles:               {unique_articles:>8,}")
    print()

    degree_dist = df_pairs.groupby("case_id")["target_disease"].count().value_counts().sort_index()
    multi_cand_cases = int(degree_dist[degree_dist.index > 1].sum())
    single_cand_cases = int(degree_dist.get(1, 0))

    print("  Candidate pairs per case unit:")
    for n_cands, n_cases in degree_dist.items():
        label = "  [multi-candidate]" if n_cands > 1 else ""
        print(f"    - {n_cands} disease(s): {n_cases:,} cases{label}")
    print(f"  Multi-candidate case units: {multi_cand_cases:,} ({multi_cand_cases / unique_cases * 100:.1f}%)")
    print()

    print("  Pairs by confidence tier:")
    for tier, count in df_pairs["confidence_tier"].value_counts().items():
        print(f"    - {tier:<35}: {count:>5,} ({count / total_pairs * 100:.1f}%)")
    print()

    neg_count = int(df_pairs["has_negation_mention"].sum())
    print(f"  Pairs with negation flag:      {neg_count:>8,} ({neg_count / total_pairs * 100:.1f}%)")
    print()

    pair_counts = df_pairs["target_disease"].value_counts()
    print("  Per-disease pair counts:")
    for d, c in pair_counts.items():
        mc = df_pairs[(df_pairs["target_disease"] == d) & (df_pairs["case_candidate_count"] > 1)].shape[0]
        print(f"    - {d:<20}: {c:>5,} total  ({mc:>4,} in multi-candidate cases)")
    print("=" * 60)

    # ------------------------------------------------------------------
    # Step 5: Save outputs
    # ------------------------------------------------------------------
    if not args.dry_run:
        output_parquet.parent.mkdir(parents=True, exist_ok=True)
        summary_path.parent.mkdir(parents=True, exist_ok=True)

        print(f"\n[5/5] Writing pair parquet to {output_parquet}...")
        df_pairs.to_parquet(output_parquet, index=False)
        print(f"  Saved {total_pairs:,} pairs to {output_parquet}")

        summary_data = {
            "pipeline": "Script 02 (Proposed Method): Pair-Level High-Recall Candidate Generator",
            "ablation_components": [
                "02b-A: Negation-Safe Detection (proximity negation kept, abstract negation signal-only; A2)",
                "02b-B: Per-Pair BM25 Physical Boundary Gate (pair-level, not case-level)",
                "A1: True Okapi BM25 with global IDF over all cases.parquet",
                "A3: Tier 3 = any disease keyword mention in case_text (high-recall mention layer)",
            ],
            "output_parquet": (
                str(output_parquet.relative_to(REPO_ROOT))
                if output_parquet.is_relative_to(REPO_ROOT) else str(output_parquet)
            ),
            "total_cases_scanned": stats["total_cases_scanned"],
            "cases_with_candidates": stats["cases_with_candidates"],
            "raw_candidate_signals": stats["raw_candidate_signals"],
            "pairs_dropped_noise": stats["pairs_dropped_noise"],
            "pairs_retained": stats["pairs_retained"],
            "unique_case_units": int(unique_cases),
            "unique_articles": int(unique_articles),
            "single_candidate_cases": single_cand_cases,
            "multi_candidate_cases": multi_cand_cases,
            "multi_candidate_rate_pct": round(multi_cand_cases / unique_cases * 100, 2),
            "confidence_tier_counts": {
                k: int(v) for k, v in df_pairs["confidence_tier"].value_counts().items()
            },
            "has_negation_mention_counts": {
                "true": neg_count,
                "false": total_pairs - neg_count,
            },
            "document_type_counts": {
                k: int(v) for k, v in df_pairs["document_type"].value_counts().items()
            },
            "disease_pair_counts": {
                k: int(v) for k, v in pair_counts.items()
            },
            "evidence_score_stats": {
                "mean": float(df_pairs["evidence_score"].mean()),
                "median": float(df_pairs["evidence_score"].median()),
                "min": float(df_pairs["evidence_score"].min()),
                "max": float(df_pairs["evidence_score"].max()),
            },
            "degree_distribution": {int(k): int(v) for k, v in degree_dist.items()},
        }

        with open(summary_path, "w", encoding="utf-8") as f_sum:
            json.dump(summary_data, f_sum, indent=2, ensure_ascii=False)
        print(f"  Saved summary to {summary_path}")

    else:
        print("\n[DRY RUN] Stats printed above. No files written.")

    print("\n" + "=" * 80)
    print("COMPLETED: Pair-Level High-Recall Candidate Generator")
    print("=" * 80)


if __name__ == "__main__":
    main()

"""
Dataset Filtering Module for MultiCaRe.
Filters articles and clinical cases for 15 specific tropical and infectious diseases
using high-performance Parquet filtering and optional multiversity package integration.
"""

import json
import logging
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import numpy as np
import pandas as pd

from config import (
    ABSTRACTS_PARQUET,
    CASES_PARQUET,
    COMPILED_DISEASE_REGEX,
    DATA_DIR,
    METADATA_PARQUET,
    OUTPUT_DIR,
    TARGET_DISEASE_PATTERNS,
)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def extract_metadata_searchable_text(meta_dict: Any) -> str:
    """Combines title, keywords, and mesh terms from the article_metadata dict."""
    if not isinstance(meta_dict, dict):
        return ""
    title = str(meta_dict.get("title", "") or "")
    kw = meta_dict.get("keywords", [])
    kw_str = " ".join(kw) if isinstance(kw, (list, np.ndarray)) else str(kw or "")
    mesh = meta_dict.get("mesh_terms", [])
    mesh_str = " ".join(mesh) if isinstance(mesh, (list, np.ndarray)) else str(mesh or "")
    return f"{title} {kw_str} {mesh_str}".strip()


def unpack_cases_parquet(cases_path: Path, filter_article_ids: Optional[Set[str]] = None) -> pd.DataFrame:
    """
    Unpacks cases.parquet where the 'cases' column contains an array of case dicts:
    [{'case_id': ..., 'case_text': ..., 'age': ..., 'gender': ...}, ...]
    """
    logger.info("Reading cases from %s...", cases_path)
    raw_cases_df = pd.read_parquet(cases_path)

    if filter_article_ids is not None:
        raw_cases_df = raw_cases_df[raw_cases_df["article_id"].isin(filter_article_ids)]

    unpacked_records = []
    for _, row in raw_cases_df.iterrows():
        aid = str(row["article_id"]).strip()
        case_items = row.get("cases", [])
        if isinstance(case_items, (list, np.ndarray)):
            for c in case_items:
                if isinstance(c, dict):
                    unpacked_records.append(
                        {
                            "article_id": aid,
                            "case_id": str(c.get("case_id", "")).strip(),
                            "case_text": c.get("case_text", ""),
                            "age": c.get("age"),
                            "gender": c.get("gender"),
                        }
                    )
        elif isinstance(case_items, dict):
            unpacked_records.append(
                {
                    "article_id": aid,
                    "case_id": str(case_items.get("case_id", "")).strip(),
                    "case_text": case_items.get("case_text", ""),
                    "age": case_items.get("age"),
                    "gender": case_items.get("gender"),
                }
            )

    unpacked_df = pd.DataFrame(unpacked_records)
    logger.info("Unpacked %d cases across %d articles.", len(unpacked_df), len(raw_cases_df))
    return unpacked_df


def filter_multicare_parquet(
    metadata_path: Path = METADATA_PARQUET,
    abstracts_path: Path = ABSTRACTS_PARQUET,
    cases_path: Path = CASES_PARQUET,
) -> Tuple[pd.DataFrame, Dict[str, Set[str]], Dict[str, Set[str]]]:
    """
    Direct high-speed Parquet filtering across metadata and abstracts.
    
    Searches:
      - metadata.parquet: 'article_metadata' -> title, keywords, mesh_terms
      - abstracts.parquet: 'abstract'
      
    Returns:
      - filtered_cases_df: DataFrame of cases with metadata attached.
      - disease_to_articles: Dict mapping disease name -> set of article_ids.
      - disease_to_cases: Dict mapping disease name -> set of case_ids.
    """
    logger.info("Loading metadata from %s...", metadata_path)
    metadata_df = pd.read_parquet(metadata_path)

    logger.info("Loading abstracts from %s...", abstracts_path)
    abstracts_df = pd.read_parquet(abstracts_path)

    # Extract combined searchable text for each article
    logger.info("Extracting searchable text from metadata and abstracts...")
    metadata_search_texts = metadata_df["article_metadata"].apply(extract_metadata_searchable_text)
    metadata_text_series = pd.Series(metadata_search_texts.values, index=metadata_df["article_id"])

    abstract_text_series = abstracts_df.set_index("article_id")["abstract"].fillna("").astype(str)

    # Track article matches per disease
    disease_to_articles: Dict[str, Set[str]] = {d: set() for d in TARGET_DISEASE_PATTERNS}

    logger.info("Scanning metadata and abstracts for 15 target diseases...")
    for disease_name, compiled_regex in COMPILED_DISEASE_REGEX.items():
        # Match in metadata
        meta_mask = metadata_text_series.str.contains(compiled_regex)
        meta_matched_arts = set(metadata_text_series[meta_mask].index)

        # Match in abstracts
        abs_mask = abstract_text_series.str.contains(compiled_regex)
        abs_matched_arts = set(abstract_text_series[abs_mask].index)

        combined_arts = meta_matched_arts | abs_matched_arts
        disease_to_articles[disease_name] = combined_arts
        logger.info(
            "  -> %-20s: %5d articles (meta: %4d, abstract: %4d)",
            disease_name,
            len(combined_arts),
            len(meta_matched_arts),
            len(abs_matched_arts),
        )

    all_matched_article_ids: Set[str] = set()
    for art_set in disease_to_articles.values():
        all_matched_article_ids.update(art_set)

    logger.info("Total unique articles matched across all 15 diseases: %d", len(all_matched_article_ids))

    # Unpack cases for matching articles
    filtered_cases_df = unpack_cases_parquet(cases_path, filter_article_ids=all_matched_article_ids)

    # Extract metadata attributes to attach to cases
    meta_info_by_article = {}
    for _, row in metadata_df[metadata_df["article_id"].isin(all_matched_article_ids)].iterrows():
        aid = str(row["article_id"]).strip()
        m = row.get("article_metadata", {})
        if isinstance(m, dict):
            meta_info_by_article[aid] = {
                "title": m.get("title", ""),
                "journal": m.get("journal", ""),
                "year": m.get("year", ""),
                "doi": m.get("doi", ""),
                "authors": list(m.get("authors", [])) if isinstance(m.get("authors"), (list, np.ndarray)) else [],
            }

    # Map diseases and metadata to each case
    article_to_diseases: Dict[str, List[str]] = {}
    for d_name, art_set in disease_to_articles.items():
        for art_id in art_set:
            article_to_diseases.setdefault(art_id, []).append(d_name)

    filtered_cases_df["matched_diseases"] = filtered_cases_df["article_id"].map(
        lambda aid: article_to_diseases.get(aid, [])
    )
    filtered_cases_df["title"] = filtered_cases_df["article_id"].map(
        lambda aid: meta_info_by_article.get(aid, {}).get("title", "")
    )
    filtered_cases_df["journal"] = filtered_cases_df["article_id"].map(
        lambda aid: meta_info_by_article.get(aid, {}).get("journal", "")
    )
    filtered_cases_df["year"] = filtered_cases_df["article_id"].map(
        lambda aid: meta_info_by_article.get(aid, {}).get("year", "")
    )
    filtered_cases_df["doi"] = filtered_cases_df["article_id"].map(
        lambda aid: meta_info_by_article.get(aid, {}).get("doi", "")
    )

    # Map disease -> cases
    disease_to_cases: Dict[str, Set[str]] = {d: set() for d in TARGET_DISEASE_PATTERNS}
    for _, row in filtered_cases_df.iterrows():
        cid = str(row["case_id"]).strip()
        for d in row["matched_diseases"]:
            disease_to_cases[d].add(cid)

    return filtered_cases_df, disease_to_articles, disease_to_cases


def run_filter_pipeline(
    use_multiversity: bool = True,
    save_summary: bool = True,
) -> Tuple[pd.DataFrame, Dict[str, Set[str]]]:
    """
    Executes the MultiCaRe filtering pipeline and outputs summary statistics.
    """
    logger.info("=== Starting MultiCaRe 15-Disease Filtering Pipeline ===")

    filtered_cases_df, disease_to_articles, disease_to_cases = filter_multicare_parquet()

    # Summary statistics
    summary_data = {
        "total_matched_articles": len({art for arts in disease_to_articles.values() for art in arts}),
        "total_matched_cases": len(filtered_cases_df),
        "disease_breakdown": {
            d: {
                "article_count": len(disease_to_articles.get(d, set())),
                "case_count": len(disease_to_cases.get(d, set())),
            }
            for d in TARGET_DISEASE_PATTERNS
        },
    }

    print("\n" + "=" * 60)
    print(" 🏥 MULTICARE 15-DISEASE SUBSET FILTERING SUMMARY")
    print("=" * 60)
    print(f"Total Unique Articles Matched: {summary_data['total_matched_articles']}")
    print(f"Total Patient Cases:          {summary_data['total_matched_cases']}")
    print("-" * 60)
    print(f"{'Target Disease':<25} | {'Articles':<10} | {'Cases':<10}")
    print("-" * 60)
    for d, stats in summary_data["disease_breakdown"].items():
        print(f"{d:<25} | {stats['article_count']:<10} | {stats['case_count']:<10}")
    print("=" * 60 + "\n")

    if save_summary:
        summary_file = OUTPUT_DIR / "matched_cases_summary.json"
        with open(summary_file, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "summary": summary_data,
                    "matched_case_ids": filtered_cases_df["case_id"].tolist(),
                    "matched_article_ids": list({art for arts in disease_to_articles.values() for art in arts}),
                },
                f,
                indent=2,
            )
        logger.info("Saved filtering summary to %s", summary_file)

    return filtered_cases_df, disease_to_articles


if __name__ == "__main__":
    run_filter_pipeline(use_multiversity=False, save_summary=True)

"""
Content List Payload Construction Module for RAG-Anything.
Converts filtered MultiCaRe clinical cases and images into RAG-Anything-compliant
content_list structures ready for direct insertion via rag.insert_content_list().
"""

import argparse
import json
import logging
import os
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import pandas as pd

from config import (
    CAPTIONS_CSV,
    IMAGES_BASE_DIR,
    OUTPUT_DIR,
    PAYLOADS_DIR,
)
from filter_dataset import run_filter_pipeline

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def format_clinical_narrative(case_row: pd.Series, mask_diagnosis: bool = False) -> str:
    """
    Constructs a clean clinical text block containing the case title and presentation narrative.
    Omits bibliographic citations, internal IDs, and raw indication tags to eliminate
    LightRAG knowledge graph pollution, while full provenance is kept in payloads_manifest.json.
    """
    parts = []

    title = str(case_row.get("title", "")).strip()
    if title and title != "nan":
        if mask_diagnosis:
            matched_diseases = case_row.get("matched_diseases", [])
            for disease in matched_diseases:
                pattern = re.compile(re.escape(str(disease)), re.IGNORECASE)
                title = pattern.sub("[DISEASE]", title)
        parts.append(f"Case Title: {title}")
        parts.append("")

    parts.append("Clinical Presentation:")
    raw_text = str(case_row.get("case_text", "")).strip()
    parts.append(raw_text)

    return "\n".join(parts)


def format_taxonomy_footnote(img_row: pd.Series) -> str:
    """
    Extracts taxonomy and classification attributes into a clean, informative footnote string.
    Supports both MultiCaRe v2 and v3 taxonomy column names.
    """
    footnote_parts = []
    taxonomy_fields = [
        ("Type", ["image_type"]),
        ("Subtype", ["image_subtype"]),
        ("Region", ["radiology_region"]),
        ("Region Granular", ["radiology_region_granular"]),
        ("View", ["radiology_view"]),
        ("Labels", ["ml_labels_for_supervised_classification", "supervised_multilabel_classification"]),
    ]

    for label, col_candidates in taxonomy_fields:
        for col in col_candidates:
            if col in img_row and pd.notna(img_row[col]):
                val = str(img_row[col]).strip()
                if val and val != "nan":
                    footnote_parts.append(f"{label}: {val}")
                    break

    if footnote_parts:
        return "Taxonomy: " + " | ".join(footnote_parts)
    return "Medical Case Figure"


def build_content_lists_for_rag(
    filtered_cases_df: pd.DataFrame,
    captions_csv_path: Path = CAPTIONS_CSV,
    images_base_dir: Path = IMAGES_BASE_DIR,
    output_payloads_dir: Path = PAYLOADS_DIR,
    max_cases: Optional[int] = None,
    mask_diagnosis: bool = False,
) -> Tuple[Dict[str, List[Dict[str, Any]]], Dict[str, Any]]:
    """
    Builds RAG-Anything-compliant content_list payloads for each patient case.
    
    Validates:
      1. Case narrative is non-empty.
      2. Image files exist on disk before including them in the content_list.
      3. Payload schema matches RAG-Anything specifications.
      
    Returns:
      - payloads: Dict mapping case_id -> content_list
      - stats: Dictionary of generation statistics
    """
    logger.info("Loading captions and labels from %s...", captions_csv_path)
    captions_df = pd.read_csv(captions_csv_path, low_memory=False)

    # Convert patient_id to string and index
    captions_df["patient_id"] = captions_df["patient_id"].astype(str).str.strip()
    logger.info("Indexing captions by patient_id...")
    captions_by_case = captions_df.groupby("patient_id")

    payloads: Dict[str, List[Dict[str, Any]]] = {}
    total_images_processed = 0
    verified_images_count = 0
    missing_images_count = 0
    cases_with_images_count = 0

    cases_to_process = (
        filtered_cases_df.head(max_cases) if max_cases else filtered_cases_df
    )
    logger.info("Processing %d patient cases...", len(cases_to_process))

    manifest_entries = []

    for idx, (_, case_row) in enumerate(cases_to_process.iterrows()):
        case_id = str(case_row["case_id"]).strip()
        article_id = str(case_row["article_id"]).strip()
        case_text = str(case_row.get("case_text", "")).strip()

        content_list: List[Dict[str, Any]] = []

        # 1. Text Component
        if case_text and case_text != "nan":
            formatted_text = format_clinical_narrative(case_row, mask_diagnosis=mask_diagnosis)
            content_list.append(
                {
                    "type": "text",
                    "text": formatted_text,
                    "page_idx": 0,
                }
            )

        # 2. Image Components
        case_images = []
        if case_id in captions_by_case.groups:
            img_rows = captions_by_case.get_group(case_id)
            for _, img_row in img_rows.iterrows():
                total_images_processed += 1
                file_name = str(img_row["file"]).strip()
                if not file_name or file_name == "nan":
                    continue

                # MultiCaRe directory partition: e.g., PMC1/PMC10/PMC10000323_...
                sub_path = f"{file_name[:4]}/{file_name[:5]}/{file_name}"
                abs_img_path = str((images_base_dir / sub_path).resolve())

                # Disk existence validation
                if not os.path.isfile(abs_img_path):
                    missing_images_count += 1
                    logger.debug("Image missing on disk: %s", abs_img_path)
                    continue

                verified_images_count += 1

                # Extract and format caption
                raw_caption = str(img_row.get("caption", "")).strip()
                caption_str = (
                    raw_caption
                    if raw_caption and raw_caption != "nan"
                    else "Medical case illustration."
                )

                # Extract and format footnote
                footnote_str = format_taxonomy_footnote(img_row)

                img_item = {
                    "type": "image",
                    "img_path": abs_img_path,
                    "image_caption": [caption_str],
                    "image_footnote": [footnote_str],
                    "page_idx": 0,
                }
                content_list.append(img_item)
                case_images.append(abs_img_path)

        if content_list:
            payloads[case_id] = content_list
            if case_images:
                cases_with_images_count += 1

            # Save individual payload to disk for persistence and inspection
            payload_path = output_payloads_dir / f"{case_id}.json"
            with open(payload_path, "w", encoding="utf-8") as f:
                json.dump(content_list, f, indent=2)

            manifest_entries.append(
                {
                    "case_id": case_id,
                    "article_id": article_id,
                    "title": str(case_row.get("title", "")).strip() if pd.notna(case_row.get("title")) and str(case_row.get("title")) != "nan" else "",
                    "journal": str(case_row.get("journal", "")).strip() if pd.notna(case_row.get("journal")) and str(case_row.get("journal")) != "nan" else "",
                    "year": str(case_row.get("year", "")).strip() if pd.notna(case_row.get("year")) and str(case_row.get("year")) != "nan" else "",
                    "doi": str(case_row.get("doi", "")).strip() if pd.notna(case_row.get("doi")) and str(case_row.get("doi")) != "nan" else "",
                    "patient_demographics": {
                        "age": float(case_row["age"]) if pd.notna(case_row.get("age")) and str(case_row.get("age")) != "nan" else None,
                        "gender": str(case_row.get("gender", "")).strip() if pd.notna(case_row.get("gender")) and str(case_row.get("gender")) != "nan" else None,
                    },
                    "matched_diseases": case_row.get("matched_diseases", []),
                    "payload_file": str(payload_path),
                    "file_path_reference": f"{case_id}.json",
                    "total_items": len(content_list),
                    "text_items": 1 if case_text else 0,
                    "image_items": len(case_images),
                }
            )

        if (idx + 1) % 500 == 0:
            logger.info("  Processed %d / %d cases...", idx + 1, len(cases_to_process))

    stats = {
        "total_cases_processed": len(cases_to_process),
        "total_payloads_generated": len(payloads),
        "cases_with_images": cases_with_images_count,
        "cases_text_only": len(payloads) - cases_with_images_count,
        "total_images_referenced": total_images_processed,
        "verified_images_on_disk": verified_images_count,
        "missing_images_on_disk": missing_images_count,
    }

    # Save manifest
    manifest_file = OUTPUT_DIR / "payloads_manifest.json"
    with open(manifest_file, "w", encoding="utf-8") as f:
        json.dump({"statistics": stats, "manifest": manifest_entries}, f, indent=2)

    logger.info("Saved payloads manifest to %s", manifest_file)
    logger.info("Payloads construction finished! Total: %d payloads ready.", len(payloads))

    print("\n" + "=" * 60)
    print(" 📦 CONTENT LIST PAYLOAD CONSTRUCTION SUMMARY")
    print("=" * 60)
    print(f"Total Cases Processed:          {stats['total_cases_processed']}")
    print(f"Total Ready Payloads:           {stats['total_payloads_generated']}")
    print(f"Cases with Verified Images:     {stats['cases_with_images']}")
    print(f"Cases (Text-only):              {stats['cases_text_only']}")
    print(f"Total Verified Images on Disk:  {stats['verified_images_on_disk']}")
    print(f"Missing Images Skipped:         {stats['missing_images_on_disk']}")
    print(f"Output Directory:               {output_payloads_dir}")
    print("=" * 60 + "\n")

    return payloads, stats


def main():
    parser = argparse.ArgumentParser(description="Build RAG-Anything content list payloads from filtered MultiCaRe cases.")
    parser.add_argument(
        "--max-cases",
        type=int,
        default=None,
        help="Maximum number of cases to process (useful for testing).",
    )
    parser.add_argument(
        "--mask-diagnosis",
        action="store_true",
        help="Mask target disease mentions in case titles to avoid label leakage in diagnostic evaluation benchmarks.",
    )
    args = parser.parse_args()

    logger.info("Running filtering first to get matched cases...")
    filtered_cases_df, _ = run_filter_pipeline(use_multiversity=False, save_summary=True)
    build_content_lists_for_rag(
        filtered_cases_df,
        max_cases=args.max_cases,
        mask_diagnosis=args.mask_diagnosis,
    )


if __name__ == "__main__":
    main()

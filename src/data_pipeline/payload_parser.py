"""Payload parser and dataset curation for MedGemma GraphRAG.
Extracts clinical cases from raw payloads.zip, normalizes entities, and generates 80/20 train/test splits.
"""

import os
import re
import json
import random
import zipfile
import argparse
from typing import Dict, List, Any, Optional

# Curated Medical Lexicon for entity anchoring in Tropical and Infectious Diseases
COMMON_SYMPTOMS = [
    "fever", "cough", "dyspnea", "shortness of breath", "chest pain", "hemoptysis",
    "fatigue", "malaise", "weight loss", "night sweats", "chills", "headache",
    "rash", "erythema", "maculopapular lesion", "nodule", "papule", "ulcer",
    "purpura", "pruritus", "itching", "hypopigmented patch", "skin lesion",
    "abdominal pain", "diarrhea", "vomiting", "nausea", "hepatomegaly",
    "splenomegaly", "hepatosplenomegaly", "lymphadenopathy", "jaundice", "ascites",
    "myalgia", "arthralgia", "joint pain", "stiffness", "muscle weakness",
    "edema", "chilblains", "petechiae", "hematuria", "seizure", "confusion"
]

COMMON_LABS = [
    "pcr", "rt-pcr", "chest x-ray", "chest ct", "computed tomography",
    "ground-glass opacity", "consolidation", "cavitation", "infiltrate",
    "biopsy", "histopathology", "acid-fast bacilli", "afb smear", "gram stain",
    "blood culture", "sputum culture", "serology", "elisa", "antibody titer",
    "leukopenia", "leukocytosis", "thrombocytopenia", "elevated crp", "high esr",
    "anemia", "microscopy", "stool exam", "blood smear", "tuberculin skin test"
]


def extract_clinical_entities(text: str, lexicon: List[str]) -> List[str]:
    """Finds matching clinical entities from text using normalized boundary matching."""
    text_lower = text.lower()
    matched = []
    for term in lexicon:
        # Match as full word or phrase
        pattern = r"\b" + re.escape(term) + r"\b"
        if re.search(pattern, text_lower):
            matched.append(term)
    return matched


def parse_raw_text(raw_text: str) -> Optional[Dict[str, Any]]:
    """Parses a raw case narrative string into structured clinical fields."""
    cid_match = re.search(r"Case ID:\s*([^|\n]+)", raw_text)
    age_match = re.search(r"Age:\s*([^|\n]+)", raw_text)
    gender_match = re.search(r"Gender:\s*([^|\n]+)", raw_text)
    dx_match = re.search(r"Target Disease Indications:\s*([^\n]+)", raw_text)
    title_match = re.search(r"Title:\s*([^\n]+)", raw_text)
    source_match = re.search(r"Source:\s*([^\n]+)", raw_text)
    pres_match = re.search(r"Case Presentation:\s*(.*)", raw_text, re.DOTALL)

    case_id = cid_match.group(1).strip() if cid_match else "UNKNOWN_ID"
    age = age_match.group(1).strip() if age_match else "Unknown"
    gender = gender_match.group(1).strip() if gender_match else "Unknown"
    target_disease = dx_match.group(1).strip() if dx_match else "Unknown"
    title = title_match.group(1).strip() if title_match else ""
    source = source_match.group(1).strip() if source_match else ""
    presentation = pres_match.group(1).strip() if pres_match else raw_text.strip()

    if target_disease == "Unknown" or not presentation:
        return None

    # Entity normalization / extraction
    symptoms = extract_clinical_entities(presentation, COMMON_SYMPTOMS)
    labs = extract_clinical_entities(presentation, COMMON_LABS)

    return {
        "case_id": case_id,
        "title": title,
        "source": source,
        "age": age,
        "gender": gender,
        "target_disease": target_disease,
        "case_presentation": presentation,
        "extracted_symptoms": symptoms,
        "extracted_labs": labs
    }


def process_zip_payloads(
    zip_path: str,
    train_output_path: str,
    test_output_path: str,
    train_ratio: float = 0.8,
    limit: Optional[int] = None,
    seed: int = 42
) -> Dict[str, int]:
    """Reads zip archive, extracts valid cases, and creates 80/20 train/test JSONL files."""
    if not os.path.exists(zip_path):
        raise FileNotFoundError(f"Payload archive not found at: {zip_path}")

    cases = []
    print(f"Reading payloads from: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as z:
        valid_names = [
            n for n in z.namelist()
            if n.endswith(".json") and not n.startswith("__MACOSX")
        ]
        if limit:
            valid_names = valid_names[:limit]

        print(f"Parsing {len(valid_names)} case files...")
        for name in valid_names:
            try:
                raw_json = json.loads(z.read(name).decode("utf-8"))
                text_content = raw_json[0].get("text", "")
                parsed = parse_raw_text(text_content)
                if parsed:
                    # Extract associated diagnostic images
                    images = []
                    for item in raw_json[1:]:
                        if item.get("type") == "image":
                            full_path = item.get("img_path", "")
                            pmc_match = re.search(r"(PMC\d+[/\\].*)", full_path)
                            rel_path = pmc_match.group(1).replace("\\", "/") if pmc_match else full_path
                            images.append({
                                "img_path": rel_path,
                                "caption": item.get("image_caption", []),
                                "footnote": item.get("image_footnote", []),
                                "page_idx": item.get("page_idx", 0)
                            })
                    parsed["images"] = images
                    cases.append(parsed)
            except Exception as e:
                continue

    print(f"Successfully extracted {len(cases)} valid clinical cases.")

    # Shuffle and split
    random.seed(seed)
    random.shuffle(cases)

    split_idx = int(len(cases) * train_ratio)
    train_cases = cases[:split_idx]
    test_cases = cases[split_idx:]

    os.makedirs(os.path.dirname(train_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(test_output_path), exist_ok=True)

    # Save train cases (Knowledge Graph ingestion)
    with open(train_output_path, "w", encoding="utf-8") as f:
        for case in train_cases:
            f.write(json.dumps(case) + "\n")

    # Save test cases (Evaluation with withheld diagnosis)
    with open(test_output_path, "w", encoding="utf-8") as f:
        for case in test_cases:
            eval_record = {
                "case_id": case["case_id"],
                "age": case["age"],
                "gender": case["gender"],
                "case_presentation": case["case_presentation"],
                "extracted_symptoms": case["extracted_symptoms"],
                "extracted_labs": case["extracted_labs"],
                "images": case.get("images", []),
                "ground_truth_dx": case["target_disease"]  # Withheld from prompt, kept for scoring
            }
            f.write(json.dumps(eval_record) + "\n")

    print(f"Wrote {len(train_cases)} train cases to: {train_output_path}")
    print(f"Wrote {len(test_cases)} test cases to: {test_output_path}")

    return {
        "total_cases": len(cases),
        "train_count": len(train_cases),
        "test_count": len(test_cases)
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse clinical case payloads for GraphRAG.")
    parser.add_argument("--zip_path", type=str, default="payload_for_ref/payloads.zip")
    parser.add_argument("--train_out", type=str, default="data/train_cases.jsonl")
    parser.add_argument("--test_out", type=str, default="data/test_cases.jsonl")
    parser.add_argument("--limit", type=int, default=None, help="Limit number of cases (e.g. 500 for testing)")
    args = parser.parse_args()

    process_zip_payloads(
        zip_path=args.zip_path,
        train_output_path=args.train_out,
        test_output_path=args.test_out,
        limit=args.limit
    )

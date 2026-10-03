"""Image2Graph module for clinical diagnostic imaging.
Transforms medical images and clinical visual findings into structured scene graphs.
"""

import os
import re
import zipfile
from typing import List, Dict, Any, Optional

# Clinical Visual Entity Lexicon for Tropical/Infectious Pathology & Radiology
COMMON_VISUAL_ENTITIES = [
    # Radiological Findings
    "cavitary lesion", "cavitation", "ground glass opacity", "consolidation",
    "infiltrate", "ring enhancing lesion", "perilesional edema", "mass effect",
    "cystic mass", "calcification", "pleural effusion", "miliary nodule",
    "apical infiltrate", "bronchiectasis", "lymphadenopathy", "hepatosplenomegaly",
    # Pathological & Microscopic Findings
    "granuloma", "caseous necrosis", "acid fast bacilli", "lateral spine egg",
    "schistosoma egg", "trophozoite", "pseudocyst", "scolex", "hyphae",
    "yeast cell", "amastigote", "macrophage", "epithelioid cell", "giant cell",
    "eosinophil", "ulceration", "mucosal erythema", "polyp", "purpura"
]


class Image2GraphExtractor:
    """Extracts visual entities, anatomical context, and scene graph relations from diagnostic images."""

    def __init__(self, multicare_dir: str = "multicare"):
        self.multicare_dir = multicare_dir

    def extract_from_image_record(self, img_record: Dict[str, Any]) -> Dict[str, Any]:
        """Extracts structured scene graph from image metadata (captions & taxonomy footnotes)."""
        captions = img_record.get("caption", [])
        caption_text = " ".join(captions) if isinstance(captions, list) else str(captions)
        footnotes = img_record.get("footnote", [])
        footnote_text = " ".join(footnotes) if isinstance(footnotes, list) else str(footnotes)

        full_text = f"{caption_text} {footnote_text}".lower()

        # 1. Extract Visual Entities
        detected_entities = []
        for term in COMMON_VISUAL_ENTITIES:
            pattern = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern, full_text):
                detected_entities.append(term)

        # 2. Extract Modality & Anatomical Region from Taxonomy Footnote
        modality_match = re.search(r"Type:\s*([^\s|]+)", footnote_text)
        subtype_match = re.search(r"Subtype:\s*([^\s|]+)", footnote_text)
        region_match = re.search(r"Region:\s*([^\s|]+)", footnote_text)

        modality = modality_match.group(1) if modality_match else "radiology/pathology"
        subtype = subtype_match.group(1) if subtype_match else "unspecified"
        region = region_match.group(1) if region_match else "general"

        # 3. Construct Scene Graph Relations between visual entities and anatomical region
        relations = []
        for ent in detected_entities:
            relations.append({
                "source": ent,
                "target": region if region != "general" else modality,
                "relation": "OBSERVED_IN_REGION",
                "weight": 1.0
            })

        return {
            "img_path": img_record.get("img_path", ""),
            "modality": modality,
            "subtype": subtype,
            "region": region,
            "caption": caption_text,
            "visual_entities": detected_entities,
            "visual_relations": relations
        }

    def load_raw_image_bytes(self, rel_path: str) -> Optional[bytes]:
        """Loads raw image bytes directly from multicare/PMC*.zip without extracting to disk."""
        if not rel_path:
            return None

        # Determine target zip (e.g. PMC5/PMC51/... -> multicare/PMC5.zip)
        match = re.match(r"(PMC\d+)[/\\]", rel_path)
        if not match:
            return None

        zip_name = f"{match.group(1)}.zip"
        zip_file_path = os.path.join(self.multicare_dir, zip_name)
        if not os.path.exists(zip_file_path):
            return None

        norm_rel_path = rel_path.replace("\\", "/")
        try:
            with zipfile.ZipFile(zip_file_path, "r") as z:
                if norm_rel_path in z.namelist():
                    return z.read(norm_rel_path)
        except Exception:
            return None
        return None

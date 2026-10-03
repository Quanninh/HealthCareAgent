"""Verification and smoke test suite for MMGraphRAG and SpecLink.
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.mmgraphrag.image2graph import Image2GraphExtractor
from src.mmgraphrag.speclink import SpecLinkAligner
from src.mmgraphrag.mm_graph_rag_engine import MMGraphRAGEngine
from src.models.medgemma_loader import MedGemmaEngine


class MockNeo4jClient:
    def __init__(self):
        self.connected = True
    def connect(self):
        return True
    def query(self, cypher: str, parameters=None):
        parameters = parameters or {}
        symptoms = parameters.get("symptoms", [])
        visuals = parameters.get("visual_entities", [])
        return [
            {
                "disease": "Tuberculosis",
                "matched_symptoms_count": len(symptoms),
                "matched_symptoms": symptoms[:2],
                "matched_labs_count": 1,
                "matched_labs": ["chest ct"],
                "matched_visual_count": len(visuals),
                "matched_visual_entities": visuals[:2],
                "visual_modalities": ["radiology"],
                "total_evidence_weight": 55
            }
        ]


def test_mmgraphrag_pipeline():
    print("=" * 60)
    print("TESTING MMGRAPHRAG & SPECLINK COMPONENTS")
    print("=" * 60)

    # 1. Test Image2Graph
    print("[1/4] Testing Image2Graph scene graph extraction...")
    i2g = Image2GraphExtractor()
    sample_img = {
        "img_path": "PMC4/PMC41/PMC4192926_SNI-5-143-g001_a_1_2.webp",
        "caption": ["Noncontrast head CT shows a cavitary lesion with perilesional edema."],
        "footnote": ["Taxonomy: Type: radiology | Subtype: ct | Region: head"]
    }
    sg = i2g.extract_from_image_record(sample_img)
    print("  Detected Visual Entities:", sg["visual_entities"])
    print("  Modality & Region:", sg["modality"], "|", sg["region"])
    assert "cavitary lesion" in sg["visual_entities"]
    assert "perilesional edema" in sg["visual_entities"]

    # 2. Test SpecLink Spectral Clustering CMEL
    print("\n[2/4] Testing SpecLink spectral clustering & alignment...")
    speclink = SpecLinkAligner()
    text_entities = ["cough", "cavitary lesion", "fever", "weight loss", "hemoptysis"]
    alignment = speclink.align_visual_entity("cavitary lesion", text_entities)
    print(f"  SpecLink Alignment Result: {alignment}")
    assert alignment is not None
    assert alignment[0] == "cavitary lesion"
    assert alignment[1] >= 0.55

    # 3. Test MMGraphRAGEngine
    print("\n[3/4] Testing MMGraphRAGEngine inference (Mock Mode)...")
    mock_client = MockNeo4jClient()
    mock_engine = MedGemmaEngine(mock_mode=True)
    mock_engine.load_model()

    mm_rag = MMGraphRAGEngine(neo4j_client=mock_client, model_engine=mock_engine)

    sample_case = {
        "case_id": "PMC4192926_01",
        "age": "71.0",
        "gender": "Male",
        "case_presentation": "Patient presented with 1-day history of headache, nausea, and vomiting. Head CT demonstrated a cystic mass with perilesional edema.",
        "extracted_symptoms": ["headache", "nausea", "vomiting"],
        "extracted_labs": ["chest ct"],
        "images": [sample_img],
        "ground_truth_dx": "Tuberculosis"
    }

    result = mm_rag.diagnose(sample_case)
    print("\n  Diagnosis Result:")
    print("    Primary:", result["primary_diagnosis"])
    print("    Differentials:", result["differential_diagnoses"])
    print("    Extracted Visual Entities:", result["extracted_visual_entities"])
    print("    Retrieved Subgraph:\n" + result["retrieved_subgraph"])

    assert result["primary_diagnosis"] == "Tuberculosis"
    assert "cavitary lesion" in result["extracted_visual_entities"]

    print("\n[4/4] ALL MMGRAPHRAG TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)


if __name__ == "__main__":
    test_mmgraphrag_pipeline()

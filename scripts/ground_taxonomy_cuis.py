"""
scripts/ground_taxonomy_cuis.py: Pre-ground all 15 diseases in disease_taxonomy.json
to canonical UMLS Concept Unique Identifiers (CUIs) using MedCAT.
"""
import os
import sys
import json
import logging

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stage1_verification import load_medcat_model

logging.getLogger('medcat').setLevel(logging.ERROR)

def ground_taxonomy_to_cuis(
    taxonomy_file: str = "disease_taxonomy.json",
    output_file: str = "disease_cui_taxonomy.json"
):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.isabs(taxonomy_file):
        taxonomy_file = os.path.join(base_dir, taxonomy_file)
    if not os.path.isabs(output_file):
        output_file = os.path.join(base_dir, output_file)

    print("Loading MedCAT model...")
    cat = load_medcat_model()
    if cat is None:
        raise RuntimeError("MedCAT model could not be loaded. Check MEDCAT_MODEL_PATH in .env")

    with open(taxonomy_file, "r") as f:
        taxonomy = json.load(f)

    target_diseases = taxonomy.get("target_diseases", {})
    cui_taxonomy = {}

    print(f"\nGrounding {len(target_diseases)} target diseases into UMLS CUIs...")

    for disease_name, data in target_diseases.items():
        print(f"  • Grounding {disease_name}...", flush=True)
        evidence = data.get("evidence_terms", {})
        
        hallmark_terms = (
            data.get("keywords", [])
            + data.get("mesh_terms", [])
            + evidence.get("clinical_signs", [])
        )
        lab_terms = evidence.get("gold_tests", [])

        def extract_cuis(term_list):
            cuis = {}
            for term in term_list:
                try:
                    res = cat.get_entities(term)
                    entities = res.get("entities", {})
                    for _, ent in entities.items():
                        cui = ent.get("cui")
                        pretty_name = ent.get("pretty_name")
                        if cui:
                            cuis[cui] = pretty_name
                except Exception as e:
                    print(f"    Warning: Error extracting CUI for term '{term}': {e}", flush=True)
            return cuis

        hallmark_cuis = extract_cuis(hallmark_terms)
        lab_cuis = extract_cuis(lab_terms)

        print(f"    -> Found {len(hallmark_cuis)} hallmark CUIs, {len(lab_cuis)} lab CUIs.", flush=True)

        cui_taxonomy[disease_name] = {
            "hallmark_cuis": hallmark_cuis,      # Dict of CUI -> Pretty Name
            "lab_cuis": lab_cuis,                # Dict of CUI -> Pretty Name
            "raw_keywords": [t.lower() for t in hallmark_terms],
            "raw_labs": [t.lower() for t in lab_terms],
        }

    with open(output_file, "w") as f:
        json.dump(cui_taxonomy, f, indent=2)

    print(f"\n[DONE] Successfully saved CUI taxonomy to {output_file}")


if __name__ == "__main__":
    ground_taxonomy_to_cuis()


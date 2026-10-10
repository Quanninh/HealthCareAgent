"""
clinical_knowledge.py: Granular medical profiles separating hallmark pathognomonic
signs from non-specific systemic symptoms.

Dynamically loaded from disease_taxonomy.json for 15 diseases.
"""

import json
import os

_taxonomy_path = os.path.join(os.path.dirname(__file__), "disease_taxonomy.json")
with open(_taxonomy_path, "r") as f:
    taxonomy = json.load(f)

DISEASES = taxonomy["target_diseases"]

DISEASE_HALLMARKS = {}
DISEASE_LAB_TESTS = {}
DISEASE_EXCLUSIONS = {}

for disease, data in DISEASES.items():
    hallmarks = []
    hallmarks.extend([k.lower() for k in data.get("keywords", [])])
    hallmarks.extend([m.lower() for m in data.get("mesh_terms", [])])
    
    evidence = data.get("evidence_terms", {})
    clinical_signs = [s.lower() for s in evidence.get("clinical_signs", [])]
    gold_tests = [t.lower() for t in evidence.get("gold_tests", [])]
    
    hallmarks.extend(clinical_signs)
    
    DISEASE_HALLMARKS[disease] = list(set(hallmarks))
    DISEASE_LAB_TESTS[disease] = list(set(gold_tests))
    
    # Generic exclusion by negating the gold tests
    DISEASE_EXCLUSIONS[disease] = [f"negative {t}" for t in gold_tests] + [f"no {s}" for s in clinical_signs]

SHARED_SYSTEMIC_SYMPTOMS = [
    "fever", "high-grade fever", "febrile", "chills", "fatigue",
    "headache", "headaches", "myalgia", "muscle aches", "weakness",
    "nausea", "vomiting", "diarrhea",
]

# For backwards compatibility with other scripts if needed, though we'll update them to use the dicts
COVID19_HALLMARKS = DISEASE_HALLMARKS.get("COVID-19", [])
COVID19_EXCLUSIONS = DISEASE_EXCLUSIONS.get("COVID-19", [])
TUBERCULOSIS_HALLMARKS = DISEASE_HALLMARKS.get("Tuberculosis", [])
TB_EXCLUSIONS = DISEASE_EXCLUSIONS.get("Tuberculosis", [])
DENGUE_HALLMARKS = DISEASE_HALLMARKS.get("Dengue", [])
DENGUE_EXCLUSIONS = DISEASE_EXCLUSIONS.get("Dengue", [])

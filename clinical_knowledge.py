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

_cui_taxonomy_path = os.path.join(os.path.dirname(__file__), "disease_cui_taxonomy.json")
DISEASE_CUI_TAXONOMY = {}
if os.path.exists(_cui_taxonomy_path):
    with open(_cui_taxonomy_path, "r") as f:
        DISEASE_CUI_TAXONOMY = json.load(f)

GENERIC_AND_SPURIOUS_CUI_BLACKLIST = {
    # Broad Systemic Symptoms (Non-disease-specific, shared constitutional signs)
    "C0015967",  # Pyrexial (Fever)
    "C0018681",  # Headache
    "C0015672",  # Fatigue
    "C0026848",  # Muscle weakness
    "C0026827",  # Myalgia
    "C0015230",  # Eruption Of Skin (Generic rash)
    "C0443253",  # Maculo Papular (Generic rash)
    "C0022346",  # Jaundiced
    "C0011991",  # Observation Of Diarrhoea
    "C0027497",  # Nausea
    "C0042963",  # Vomiting
    "C0018926",  # Vomiting Of Blood (Hematemesis)
    "C0038984",  # Portion Of Sweat (Sweating)
    "C0424790",  # Rigor Temperature Associated Observation (Chills/Rigors)
    "C0013404",  # Sob Shortness Of Breath (Dyspnea)
    "C0028961",  # Decreased Urine Volume (Oliguria)
    "C0038002",  # Enlargement Of Spleen (Splenomegaly)
    "C0019209",  # Hepatomegaly
    "C0019214",  # Hepatosplenomegaly
    "C0038999",  # Observation Of Swelling (Generic edema)
    "C0013604",  # Interstitial Oedema
    "C0085631",  # Agitated Behaviour (Delirium/Agitation)
    "C0026766",  # Mods Multiple Organ Dysfunction Syndrome
    "C4552597",  # Acute Kidney Injury Ctcae
    "C0035078",  # Renal Insufficiency Syndrome
    "C0005779",  # Blood Coagulation Disorder
    "C0392386",  # Platelet Count Below Reference Range (Thrombocytopenia)
    "C0428977",  # Decreased Heart Rate (Bradycardia)
    "C0238883",  # Calf Tenderness
    # Spurious NLP / MedCAT Lexical Mappings
    "C5203119",  # Intensity And Distress 5 (from "severe")
    "C4085211",  # Pain Distress Question (from "epigastric pain")
    "C0221198",  # Visible Lesion (from "cavitary lesion")
    "C3540682",  # Losing Weight Question (from "weight loss")
    "C0311392",  # Physical Findings (from "faget sign")
    "C0549099",  # Perforation Observation (from "perforation")
    "C0332448",  # Infiltration Into Tissue (from "bilateral infiltrates")
    "C0240526",  # On Omni Nocte (from "night sweats")
    "C0205390",  # Phases (from "toxic phase")
    "C0439541",  # Black Coloring (from "black vomitus")
    "C0205145",  # Sites (from "bite site")
    "C0600688",  # Effects Toxics
    "C0240321",  # Mediterranean (from "mediterranean fever")
    "C0014533",  # Epididymal Structures
    "C0020885",  # Small Intestine Ileum
    "C0004388",  # Autonomic Nervous System Structure
    "C0005658",  # Bite Injury (Generic animal bite)
    "C0277937",  # Turgor Skin
    "C0037361",  # Sensory Perception Of Smell
    "C1705493",  # West Direction (from "western blot")
    "C1708715",  # Loading Technique (from "viral load")
    "C0010453",  # Anthropological Culture (from "culture")
    "C1947931",  # Direct Qualifier (from "direct")
    "C1123023",  # Integumental System (from "skin biopsy")
    "C0016318",  # Fluorescent Identification Of Anti Nuclear Antibody
    "C0003241",  # Little Not Otherwise Specified Antibody
    "C5139976",  # Capture (from "antigen capture")
    "C0204727",  # Isolation Precautions (from "virus isolation")
    "C3665438",  # Juxtapapillary Focal Retinitis And Retinochoroiditis
    "C0370199",  # Aspirate Substance
    "C1304890",  # Enteric
    # Generic Inpatient Procedural & Lab Tests
    "C0200949",  # Blood Culture Procedure
    "C1254426",  # Bone Marrow Culture
    "C0430414",  # Microbial Stool Culture
    "C0036745",  # Study Of Serum (Generic serology)
    "C0444186",  # Smear Tests
    "C0086143",  # Diagnostic Test Procedure
    "C0010454",  # Culture Mediums
    "C0729856",  # Antigen Testing
    "C0183753",  # Swab Speciman
    "C0368675",  # Antibodies Antigens
    "C1167909",  # Lymphocytes T Cells
    "C0037296",  # Special Dermatological Testing
    "C1553151",  # Darkfield Microscopy
    "C1551404",  # Serum Neutralization
    "C0857285",  # Human Bone Marrow Aspirate
    "C0037993",  # Reticuloendothelial System Spleen
}

DISEASE_HALLMARK_CUIS = {
    d: {c for c in data.get("hallmark_cuis", {}).keys() if c not in GENERIC_AND_SPURIOUS_CUI_BLACKLIST}
    for d, data in DISEASE_CUI_TAXONOMY.items()
}
DISEASE_LAB_CUIS = {
    d: {c for c in data.get("lab_cuis", {}).keys() if c not in GENERIC_AND_SPURIOUS_CUI_BLACKLIST}
    for d, data in DISEASE_CUI_TAXONOMY.items()
}

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

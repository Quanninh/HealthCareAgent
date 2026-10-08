"""
clinical_knowledge.py: Granular medical profiles separating hallmark pathognomonic
signs from non-specific systemic symptoms.

Design Rationale:
- Pathognomonic / High-Specificity markers carry high diagnostic weight and are
  used in standalone hallmark LFs.
- Shared systemic symptoms (fever, myalgia, etc.) are only meaningful in
  constellation / co-occurrence LFs to avoid false attribution.
- Negative exclusion triggers allow LFs to vote NEGATIVE when definitive
  rule-out evidence is present.
"""

# ═══════════════════════════════════════════════════════════════════════
#  COVID-19
# ═══════════════════════════════════════════════════════════════════════

COVID19_HALLMARKS = [
    "anosmia", "loss of smell", "ageusia", "loss of taste",
    "ground-glass opacities", "ground-glass appearance", "ground glass opacification",
    "bilateral infiltrates",
    "positive sars-cov-2", "positive rrt-pcr", "rrt-pcr", "anti-sars-cov-2",
    "sars-cov-2 infection", "covid-19", "coronavirus",
    "covid-19 swab", "which was positive",
]

COVID19_EXCLUSIONS = [
    "negative sars-cov-2", "negative rrt-pcr", "covid-19 swab negative",
]

# ═══════════════════════════════════════════════════════════════════════
#  TUBERCULOSIS
# ═══════════════════════════════════════════════════════════════════════

TUBERCULOSIS_HALLMARKS = [
    "hemoptysis", "cavitary lesion", "cavitary lesions",
    "caseating granuloma", "caseous necrosis", "caseating necrosis",
    "epithelioid granulomas", "epithelioid granuloma",
    "nodular epithelioid granulomas",
    "genexpert mtb/rif", "genexpert", "mtb/rif",
    "mycobacterium tuberculosis", "mycobacterium",
    "tuberculous meningitis", "tuberculosis", "tb", "mt",
    "ghon focus", "miliary pattern",
    "granulomatous inflammation",
    "pcr for tb was positive", "pcr for the mycobacterium tuberculosis",
    "positive in frozen sections",
    "non-necrotizing epithelioid granulomas compatible with tb",
    "antituberculosis",
]

TB_EXCLUSIONS = [
    "acid-fast bacilli stain was negative", "pcr for tb was negative",
    "tuberculin skin test negative",
]

# ═══════════════════════════════════════════════════════════════════════
#  DENGUE FEVER
# ═══════════════════════════════════════════════════════════════════════

DENGUE_HALLMARKS = [
    "retro-orbital pain", "retro-orbital",
    "thrombocytopenia", "platelet count decreased", "platelet count",
    "positive ns1 antigen", "ns1 antigen test", "ns1 antigen",
    "dengue virus", "dengue", "dengue fever", "df",
    "elisa igm", "dengue test",
    "petechiae",
    "dengue retinopathy", "dengue myocarditis",
    "immunoglobulin m enzyme-linked immunosorbent assay serology for the dengue virus",
]

DENGUE_EXCLUSIONS = [
    "normal platelet count", "dengue serology negative",
]

# ═══════════════════════════════════════════════════════════════════════
#  SHARED SYSTEMIC (Non-Specific) — Only for constellation LFs
# ═══════════════════════════════════════════════════════════════════════

SHARED_SYSTEMIC_SYMPTOMS = [
    "fever", "high-grade fever", "febrile", "chills", "fatigue",
    "headache", "headaches", "myalgia", "muscle aches", "weakness",
    "nausea", "vomiting", "diarrhea",
]

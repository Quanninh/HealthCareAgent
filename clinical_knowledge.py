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

# ═══════════════════════════════════════════════════════════════════════════════
#  MULTI-TIERED CLINICAL EVIDENCE TAXONOMY (Synthesized from 16 Skill Files)
# ═══════════════════════════════════════════════════════════════════════════════

# Tier 1 (E1): Disease-defining confirmatory molecular, culture, and microscopic tests
DISEASE_E1_LABS = {
    "Dengue": [
        "ns1", "ns1 antigen", "dengue pcr", "dengue rt-pcr", "denv pcr", "denv rna",
        "dengue virus rna", "ns1 positive", "dengue ns1",
    ],
    "Malaria": [
        "thick smear", "thin smear", "blood smear positive", "plasmodium falciparum",
        "plasmodium vivax", "plasmodium malariae", "plasmodium ovale", "plasmodium knowlesi",
        "malaria rdt", "rapid diagnostic test for malaria", "parasitemia", "giemsa stain",
        "malaria pcr", "plasmodium pcr", "blood film showed plasmodium",
    ],
    "Ebola_Filovirus": [
        "ebola rt-pcr", "ebola pcr", "ebolavirus pcr", "antigen capture elisa",
        "virus isolation", "zaire ebolavirus", "sudan ebolavirus", "marburg pcr",
        "filovirus pcr", "ebola virus rna",
    ],
    "Tuberculosis": [
        "genexpert", "gene xpert", "xpert mtb", "xpert mtb/rif", "mtb/rif",
        "mycobacterial culture", "lowenstein-jensen", "mgit", "mycobacterium tuberculosis",
        "m. tuberculosis", "mtb pcr", "truenat mtb", "culture confirmed tuberculosis",
    ],
    "COVID-19": [
        "sars-cov-2 pcr", "sars-cov-2 rt-pcr", "covid-19 pcr", "covid-19 rt-pcr",
        "sars-cov-2 naat", "covid naat", "nasopharyngeal swab pcr", "covid-19 naat",
        "reverse transcription-polymerase chain reaction for sars-cov-2", "sars-cov-2 rna",
    ],
    "HIV_AIDS": [
        "western blot", "hiv-1 rna", "hiv viral load", "hiv naat", "hiv pcr",
        "differentiation immunoassay", "geenius", "4th generation", "fourth generation",
        "antigen/antibody combo", "hiv-1/2 differentiation", "detectable hiv rna",
    ],
    "Chikungunya": [
        "chikungunya rt-pcr", "chikungunya pcr", "chkv pcr", "chkv rt-pcr",
        "chikungunya virus isolation", "chkv rna",
    ],
    "Zika": [
        "zika rt-pcr", "zika pcr", "zikv pcr", "zikv rt-pcr", "zika naat", "trioplex",
        "zika virus rna", "zikv rna",
    ],
    "Brucellosis": [
        "brucella culture", "blood culture positive for brucella",
        "bone marrow culture positive for brucella", "brucella pcr",
        "brucella melitensis", "brucella abortus", "brucella suis",
        "isolation of brucella", "blood culture yielded brucella",
    ],
    "Leishmaniasis": [
        "amastigotes", "leishman-donovan bodies", "ld bodies", "leishmania pcr",
        "bone marrow aspirate showing amastigotes", "splenic aspirate",
        "skin biopsy showing amastigotes", "giemsa-stained smear showed amastigotes",
    ],
    "Typhoid_Fever": [
        "blood culture positive for salmonella typhi", "salmonella typhi culture",
        "salmonella paratyphi culture", "bone marrow culture positive for salmonella",
        "s. typhi culture", "salmonella enterica serovar typhi", "salmonella typhi isolated",
    ],
    "Cholera": [
        "vibrio cholerae culture", "tcbs agar", "vibrio cholerae", "cholera pcr",
        "v. cholerae", "seroagglutination o1", "seroagglutination o139",
        "stool culture positive for vibrio", "isolation of vibrio cholerae",
    ],
    "Rabies": [
        "fluorescent antibody", "rabies fat", "nuchal skin biopsy",
        "saliva rt-pcr for rabies", "rabies virus pcr", "rabies neutralizing antibody in csf",
        "direct fluorescent antibody test", "ante-mortem rabies pcr",
    ],
    "Leptospirosis": [
        "leptospira pcr", "leptospira dna", "microscopic agglutination test",
        "mat titer", "mat confirmation", "leptospira isolation",
    ],
    "Yellow_Fever": [
        "yellow fever rt-pcr", "yellow fever pcr", "yfv pcr", "yfv rt-pcr",
        "yellow fever rna", "prnt for yellow fever", "plaque reduction neutralization test for yellow fever",
    ],
}

# Tier 2 (E2): Strong Evidence / Serology & High Titer / Pathognomonic Hallmarks
DISEASE_E2_SEROLOGY = {
    "Dengue": [
        "dengue igm", "mac-elisa", "igm elisa", "paired sera seroconversion",
        "dengue serology positive", "positive dengue igm",
    ],
    "Malaria": [
        "trophozoites", "schizonts", "ring forms", "gametocytes", "blackwater fever",
        "cerebral malaria", "plasmodium", "falciparum", "vivax",
    ],
    "Ebola_Filovirus": [
        "igm elisa", "ebola igm", "filovirus antigen", "antigen detection",
    ],
    "Tuberculosis": [
        "caseating granuloma", "caseating granulomas", "langhans giant cells",
        "cavitary lesion", "apical cavity", "miliary tb", "acid-fast bacilli",
        "afb smear", "ziehl-neelsen",
    ],
    "COVID-19": [
        "rapid antigen test", "rapid antigen positive", "covid antigen",
        "sars-cov-2 antigen", "nucleocapsid antigen", "rat positive",
    ],
    "HIV_AIDS": [
        "cd4 count", "cd4+", "cd4 < 200", "cd4 percentage", "pneumocystis jirovecii",
        "kaposi sarcoma", "cryptococcal meningitis", "opportunistic infection",
        "wasting syndrome", "oral candidiasis in hiv",
    ],
    "Chikungunya": [
        "chikungunya igm", "chkv igm", "chikungunya serology", "positive chkv igm",
    ],
    "Zika": [
        "zika igm", "zikv igm", "zika serology", "congenital zika syndrome",
        "microcephaly", "positive zikv igm",
    ],
    "Brucellosis": [
        "standard tube agglutination", "wright test", "rose bengal", "brucellacapt",
        "2-mercaptoethanol", "brucella agglutination", "brucella serology",
        "sta titer", "wright agglutination",
    ],
    "Leishmaniasis": [
        "rk39", "rk-39", "direct agglutination test", "dat titer",
        "visceral leishmaniasis serology", "kala-azar", "positive rk39",
    ],
    "Typhoid_Fever": [
        "s. typhi pcr", "salmonella pcr", "rose spots", "relative bradycardia",
    ],
    "Cholera": [
        "cholera rdt", "crystal vc", "rice-water stool", "rice-water diarrhea",
        "rice water stool", "profuse watery diarrhea",
    ],
    "Rabies": [
        "hydrophobia", "aerophobia", "negri bodies", "progressive encephalomyelitis",
    ],
    "Leptospirosis": [
        "leptospira igm", "leptospirosis serology", "mat titer >= 1:100",
        "weil's disease", "conjunctival suffusion", "positive leptospira igm",
    ],
    "Yellow_Fever": [
        "yellow fever igm", "yfv igm", "faget sign", "black vomitus",
    ],
}

# Tier 3A (E3): Epidemiological Exposures, Vectors, Food/Water & Animal Reservoirs
DISEASE_E3_EPIDEMIOLOGY = {
    "Dengue": [
        "aedes", "mosquito bite", "mosquito bites", "endemic area", "tropical travel",
        "caribbean", "latin america", "southeast asia",
    ],
    "Malaria": [
        "anopheles", "mosquito bite", "mosquito bites", "endemic area",
        "travel to africa", "sub-saharan", "no malaria prophylaxis", "chemoprophylaxis",
    ],
    "Ebola_Filovirus": [
        "bushmeat", "fruit bats", "contact with ebola", "outbreak area",
        "democratic republic of congo", "drc", "uganda", "west africa outbreak",
        "burial ceremony", "ebola treatment unit",
    ],
    "Tuberculosis": [
        "household contact with tb", "contact with active tb", "prison",
        "homeless shelter", "endemic country", "tb contact investigation",
    ],
    "COVID-19": [
        "exposure to covid", "household contact with covid", "covid cluster",
        "covid-19 contact",
    ],
    "HIV_AIDS": [
        "unprotected sexual", "intravenous drug", "iv drug use", "needle stick",
        "blood transfusion", "sex worker", "multiple sexual partners",
    ],
    "Chikungunya": [
        "aedes", "mosquito bite", "mosquito bites", "travel to endemic",
    ],
    "Zika": [
        "aedes", "mosquito bite", "mosquito bites", "sexual transmission",
        "travel to endemic", "brazil", "latin america travel",
    ],
    "Brucellosis": [
        "unpasteurized milk", "raw milk", "unpasteurized cheese", "raw cheese",
        "unpasteurized dairy", "livestock", "sheep", "goats", "cattle",
        "veterinarian", "slaughterhouse", "stockbreeders", "stockbreeder", "farm animals",
    ],
    "Leishmaniasis": [
        "sandfly", "sand fly", "sandflies", "phlebotomus", "lutzomyia",
        "mediterranean travel", "endemic area", "middle east travel",
    ],
    "Typhoid_Fever": [
        "street food", "contaminated food", "contaminated water",
        "travel to south asia", "india", "pakistan", "bangladesh", "endemic travel",
    ],
    "Cholera": [
        "contaminated water", "raw seafood", "shellfish", "cholera outbreak",
        "refugee camp", "poor sanitation", "flooding and drinking water",
    ],
    "Rabies": [
        "dog bite", "bat bite", "bitten by a dog", "bitten by a bat",
        "stray dog", "animal bite", "animal scratch", "raccoon", "skunk",
        "fox", "monkey bite",
    ],
    "Leptospirosis": [
        "floodwater", "flooding", "flood", "sewer", "sewage", "rat urine",
        "rodents", "freshwater swimming", "rafting", "paddy field", "farming",
        "occupational exposure to water",
    ],
    "Yellow_Fever": [
        "haemagogus", "aedes", "jungle exposure", "travel to south america",
        "amazon", "travel to west africa", "endemic zone",
    ],
}

# Tier 4A: Explicit Negative Test Results Ruling Out the Target Disease
DISEASE_EXCLUSIONS_LAB = {
    "Dengue": [
        "dengue negative", "dengue pcr negative", "ns1 negative", "dengue igm negative",
        "negative for dengue", "ruled out dengue", "dengue was ruled out",
    ],
    "Malaria": [
        "smear negative for parasites", "no parasites seen", "malaria negative",
        "negative for malaria", "no plasmodium", "blood smear was negative",
        "rdt was negative for malaria", "ruled out malaria", "thick and thin smear were negative",
    ],
    "Ebola_Filovirus": [
        "ebola negative", "ebola pcr negative", "negative for ebola", "ruled out ebola",
    ],
    "Tuberculosis": [
        "afb negative", "genexpert negative", "mtb pcr negative",
        "culture negative for m. tuberculosis", "negative for tb", "ruled out tuberculosis",
        "tuberculosis was ruled out",
    ],
    "COVID-19": [
        "covid negative", "covid-19 negative", "sars-cov-2 negative",
        "pcr negative for sars-cov-2", "negative for covid-19", "rapid antigen negative",
        "tested negative for covid",
    ],
    "HIV_AIDS": [
        "hiv negative", "nonreactive hiv", "non-reactive hiv", "hiv test was negative",
        "negative for hiv", "both hiv tests negative", "western blot negative",
        "elisa for hiv was negative", "hiv non-reactive",
    ],
    "Chikungunya": [
        "chikungunya negative", "chikungunya pcr negative", "chkv negative",
        "negative for chikungunya", "ruled out chikungunya",
    ],
    "Zika": [
        "zika negative", "zika pcr negative", "negative for zika", "ruled out zika",
    ],
    "Brucellosis": [
        "brucella negative", "wright test negative", "rose bengal negative",
        "serology negative for brucella", "negative for brucellosis", "ruled out brucellosis",
    ],
    "Leishmaniasis": [
        "leishmania negative", "rk39 negative", "smear negative for leishmania",
        "negative for leishmaniasis", "ruled out leishmaniasis",
    ],
    "Typhoid_Fever": [
        "widal negative", "blood culture negative for salmonella",
        "negative for typhoid", "ruled out typhoid",
    ],
    "Cholera": [
        "culture negative for vibrio", "negative for cholera", "ruled out cholera",
        "stool culture negative for vibrio",
    ],
    "Rabies": [
        "negative for rabies", "ruled out rabies",
    ],
    "Leptospirosis": [
        "mat negative", "leptospira negative", "negative for leptospirosis",
        "ruled out leptospirosis",
    ],
    "Yellow_Fever": [
        "yellow fever negative", "yellow fever pcr negative", "negative for yellow fever",
        "ruled out yellow fever",
    ],
}

# Tier 4B: Spurious Homonyms & Discourse Mention Contexts (Filter out / Vote 0)
DISEASE_HOMONYMS = {
    "HIV_AIDS": [
        "walking aid", "walking aids", "mobility aid", "mobility aids",
        "hearing aid", "hearing aids", "visual aid", "visual aids",
        "first aid", "band aid", "teaching aid",
    ],
    "Malaria": [
        "patent foramen ovale", "foramen ovale", "pfo closure", "pfo", "fossa ovalis",
    ],
    "Ebola_Filovirus": [
        "external ventricular drain", "evd drain", "evd catheter",
        "evd placement", "evd insertion",
    ],
    "COVID-19": [
        "covid-19 vaccine", "covid-19 vaccination", "covid vaccine", "covid vaccination",
        "received bnt162b2", "mrna-1273", "covishield", "sinovac",
        "pfizer-biontech vaccine", "astrazeneca vaccine", "moderna vaccine",
        "post-vaccination", "after vaccination", "received covid-19 vaccine",
    ],
    "Yellow_Fever": [
        "yellow fever vaccine", "yellow fever vaccination", "17d vaccine",
        "17d vaccination", "stamaril", "received yellow fever vaccine",
    ],
    "Tuberculosis": [
        "bcg vaccine", "bcg vaccination", "family history of tb",
        "father had tb", "mother had tb",
    ],
    "Rabies": [
        "rabies vaccine", "rabies vaccination", "pre-exposure prophylaxis",
    ],
}

# Document Scope Filters: Aggregate Cohorts, Population Studies, and Reviews (Must be excluded)
COHORT_AND_AGGREGATE_PATTERNS = [
    r"\ba total of \d+ (cases|patients)\b",
    r"\bcohort of \d+\b",
    r"\bsystematic (scoping )?review\b",
    r"\bmeta-analysis\b",
    r"\bretrospective study on about \d+\b",
    r"\bmedian age was \d+ years\b",
    r"\bwe analyzed \d+ cases\b",
    r"\btables? \d+[-–\d]* presents? descriptive\b",
]

# Single Patient Anchor Indicators (Demonstrates single human patient CCU)
SINGLE_PATIENT_ANCHOR_PATTERNS = [
    r"\b(a \d+[\s-]year[\s-]old|a \d+[\s-]month[\s-]old|the patient (is|was) a|a female patient|a male patient|presented with|was admitted (to|with))\b",
]

# Non-Human / Veterinary Document Patterns (Must be excluded)
NON_HUMAN_PATTERNS = [
    r"\bcanine\b",
    r"\bbovine\b",
    r"\bfeline\b",
    r"\bmurine model\b",
    r"\bmice were inoculated\b",
    r"\bcows were\b",
    r"\bdogs were\b",
    r"\brabbits were\b",
    r"\brats were infected\b",
]

# Pathogen / Organism keywords for Relational Evidence Grounding
DISEASE_ORGANISMS = {
    "Dengue": ["dengue", "denv"],
    "Malaria": ["malaria", "plasmodium", "falciparum", "vivax", "ovale", "malariae", "knowlesi"],
    "Ebola_Filovirus": ["ebola", "marburg", "filovirus"],
    "Tuberculosis": ["tuberculosis", "mycobacterium", "m. tuberculosis", "mtb", "acid-fast", "afb"],
    "COVID-19": ["sars-cov-2", "covid-19", "coronavirus disease 2019", "covid19"],
    "HIV_AIDS": ["hiv", "human immunodeficiency virus", "aids"],
    "Chikungunya": ["chikungunya", "chkv"],
    "Zika": ["zika", "zikv"],
    "Brucellosis": ["brucella", "brucellosis"],
    "Leishmaniasis": ["leishmania", "amastigote", "kala-azar"],
    "Typhoid_Fever": ["salmonella typhi", "s. typhi", "salmonella paratyphi", "typhoid fever"],
    "Cholera": ["cholera", "vibrio cholerae"],
    "Rabies": ["rabies", "lyssavirus"],
    "Leptospirosis": ["leptospir", "weil disease", "leptospirosis"],
    "Yellow_Fever": ["yellow fever", "yfv"],
}

LAB_CONFIRMATORY_ROOTS = [
    "pcr", "rt-pcr", "naat", "culture", "isolate", "isolation", "smear",
    "film", "antigen", "ns1", "genexpert", "xpert", "elisa", "mat", "agglutination",
    "serology", "serological", "seropositive", "igm", "titer", "titre", "biopsy",
    "amastigote", "western blot", "viral load", "rdt", "diagnosed with",
    "confirmed"
]

SENTENCE_NEGATIONS = [
    "negative", "not detected", "no growth", "non-reactive", "nonreactive",
    "undetectable", "ruled out", "no evidence", "unremarkable", "failed to detect",
    "absence of", "normal"
]

SENTENCE_PAST_OR_FAMILY = [
    "history of", "in childhood", "years ago", "months ago", "past medical history",
    "mother", "father", "parent", "partner", "wife", "husband", "brother", "sister",
    "differential diagnosis", "suspected but excluded"
]

import re

def is_valid_relational_affirmation(text: str, disease_name: str) -> bool:
    """
    Check if a sentence in narrative text affirms the target disease organism with
    confirmatory lab/diagnostic roots without sentence-level negation, remote past history,
    or family-member context.
    """
    if not text:
        return False
    orgs = DISEASE_ORGANISMS.get(disease_name, [])
    if not orgs:
        return False
    t_lower = text.lower()
    for sent in re.split(r"[.\n;]", t_lower):
        sent = sent.strip()
        if not sent:
            continue
        if any(org in sent for org in orgs) and any(lab in sent for lab in LAB_CONFIRMATORY_ROOTS):
            if any(neg in sent for neg in SENTENCE_NEGATIONS):
                continue
            if any(pf in sent for pf in SENTENCE_PAST_OR_FAMILY):
                continue
            return True
    return False



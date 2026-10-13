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
#  MULTI-TIERED CLINICAL EVIDENCE TAXONOMY (Synthesized from 16 Skill Files & Trove)
# ═══════════════════════════════════════════════════════════════════════════════

# Tier 1 (E1): Disease-defining confirmatory molecular, culture, and microscopic tests
DISEASE_E1_LABS = {
    "Dengue": [
        "ns1", "ns1 antigen", "dengue pcr", "dengue rt-pcr", "denv pcr", "denv rna",
        "dengue virus rna", "ns1 positive", "dengue ns1", "positive ns1", "ns1 reactive",
        "dengue rna detected", "dengue virus isolated", "denv-1 pcr", "denv-2 pcr", "denv-3 pcr", "denv-4 pcr",
    ],
    "Malaria": [
        "thick smear", "thin smear", "blood smear positive", "plasmodium falciparum",
        "plasmodium vivax", "plasmodium malariae", "plasmodium ovale", "plasmodium knowlesi",
        "malaria rdt", "rapid diagnostic test for malaria", "giemsa stain showed plasmodium",
        "malaria pcr", "plasmodium pcr", "blood film showed plasmodium", "blood smear showed ring",
        "trophozoites of plasmodium", "schizonts of plasmodium", "gametocytes of plasmodium",
        "malaria parasitemia", "plasmodium parasitemia", "blood film positive for malaria",
        "thick and thin films", "parasites per microliter of plasmodium",
    ],
    "Ebola_Filovirus": [
        "ebola rt-pcr", "ebola pcr", "ebolavirus pcr", "antigen capture elisa",
        "virus isolation", "zaire ebolavirus", "sudan ebolavirus", "marburg pcr",
        "filovirus pcr", "ebola virus rna", "ebola viral rna", "filovirus rna",
        "bundibugyo ebolavirus", "orthoebolavirus pcr",
    ],
    "Tuberculosis": [
        "genexpert", "gene xpert", "xpert mtb", "xpert mtb/rif", "mtb/rif", "xpert ultra",
        "mycobacterial culture", "lowenstein-jensen", "mgit", "mycobacterium tuberculosis",
        "m. tuberculosis", "mtb pcr", "truenat mtb", "culture confirmed tuberculosis",
        "m. tuberculosis complex", "mtb complex", "dna of mycobacterium tuberculosis",
        "line probe assay for mtb", "culture positive for m. tuberculosis",
    ],
    "COVID-19": [
        "sars-cov-2 pcr", "sars-cov-2 rt-pcr", "covid-19 pcr", "covid-19 rt-pcr",
        "sars-cov-2 naat", "covid naat", "nasopharyngeal swab pcr", "covid-19 naat",
        "reverse transcription-polymerase chain reaction for sars-cov-2", "sars-cov-2 rna",
        "sars-cov-2 viral rna", "detected sars-cov-2", "positive for sars-cov-2",
        "rt-pcr for sars-cov-2", "rt-pcr for covid-19", "positive covid-19 pcr",
    ],
    "HIV_AIDS": [
        "western blot", "hiv-1 rna", "hiv viral load", "hiv naat", "hiv pcr",
        "differentiation immunoassay", "geenius", "4th generation", "fourth generation",
        "antigen/antibody combo", "hiv-1/2 differentiation", "detectable hiv rna",
        "hiv-1/2 antibody differentiation", "multispot hiv-1/hiv-2", "hiv-1 proviral dna",
        "hiv rna quantitative", "detectable hiv-1 viral load",
    ],
    "Chikungunya": [
        "chikungunya rt-pcr", "chikungunya pcr", "chkv pcr", "chkv rt-pcr",
        "chikungunya virus isolation", "chkv rna", "chikungunya virus rna",
        "chikv pcr", "chikv rt-pcr", "chikv rna", "chikungunya naat",
    ],
    "Zika": [
        "zika rt-pcr", "zika pcr", "zikv pcr", "zikv rt-pcr", "zika naat", "trioplex",
        "zika virus rna", "zikv rna", "zika viral rna", "trioplex real-time rt-pcr",
        "zika virus in amniotic fluid", "congenital zika confirmed",
    ],
    "Brucellosis": [
        "brucella culture", "blood culture positive for brucella",
        "bone marrow culture positive for brucella", "brucella pcr",
        "brucella melitensis", "brucella abortus", "brucella suis", "brucella canis",
        "b. melitensis", "b. abortus", "b. suis",
        "isolation of brucella", "blood culture yielded brucella",
        "brucella dna", "identified as brucella", "yielded b. melitensis",
        "melitensis was isolated", "abortus was isolated",
    ],
    "Leishmaniasis": [
        "amastigotes", "amastigote", "leishman-donovan bodies", "ld bodies", "leishmania pcr",
        "bone marrow aspirate showing amastigotes", "splenic aspirate", "leishmania dna",
        "skin biopsy showing amastigotes", "giemsa-stained smear showed amastigotes",
        "visualization of amastigotes", "presence of amastigotes", "leishman-donovan body",
        "leishmania infantum", "leishmania donovani", "leishmania major", "leishmania tropica",
        "leishmania braziliensis", "leishmania per ml", "leishmania culture", "nnn medium",
        "katex", "leishmania amastigotes", "bone marrow trephine showing amastigotes",
    ],
    "Typhoid_Fever": [
        "blood culture positive for salmonella typhi", "salmonella typhi culture",
        "salmonella paratyphi culture", "bone marrow culture positive for salmonella",
        "s. typhi culture", "salmonella enterica serovar typhi", "salmonella typhi isolated",
        "s. paratyphi culture", "isolated salmonella typhi", "salmonella typhi was isolated",
        "s. typhi was isolated", "blood culture yielded salmonella typhi", "s. typhi pcr",
        "salmonella typhi pcr", "salmonella paratyphi a", "salmonella paratyphi b",
    ],
    "Cholera": [
        "vibrio cholerae culture", "tcbs agar", "vibrio cholerae", "cholera pcr",
        "v. cholerae", "seroagglutination o1", "seroagglutination o139",
        "stool culture positive for vibrio", "isolation of vibrio cholerae",
        "vibrio cholerae o1", "vibrio cholerae o139", "cholera toxin pcr",
        "stool culture yielded vibrio", "v. cholerae isolated",
    ],
    "Rabies": [
        "fluorescent antibody", "rabies fat", "nuchal skin biopsy",
        "saliva rt-pcr for rabies", "rabies virus pcr", "rabies neutralizing antibody in csf",
        "direct fluorescent antibody test", "ante-mortem rabies pcr", "negri bodies",
        "rabies dfat", "rabies viral rna in saliva", "rabies viral antigen",
    ],
    "Leptospirosis": [
        "leptospira pcr", "leptospira dna", "microscopic agglutination test",
        "mat titer", "mat confirmation", "leptospira isolation", "leptospira interrogans",
        "mat titer >= 1:400", "mat of 1:400", "mat result was positive at 1:400",
        "mat titer of 1:800", "mat titer of 1:1600", "mat was positive at 1:400",
        "leptospira culture", "leptospiral dna",
    ],
    "Yellow_Fever": [
        "yellow fever rt-pcr", "yellow fever pcr", "yfv pcr", "yfv rt-pcr",
        "yellow fever rna", "prnt for yellow fever", "plaque reduction neutralization test for yellow fever",
        "yfv rna", "yellow fever viral rna", "yellow fever virus isolation",
    ],
}

# Tier 2 (E2): Strong Evidence / Serology & High Titer / Pathognomonic Hallmarks
DISEASE_E2_SEROLOGY = {
    "Dengue": [
        "dengue igm", "mac-elisa", "igm elisa", "paired sera seroconversion",
        "dengue serology positive", "positive dengue igm", "dengue igm reactive",
        "anti-dengue igm", "dengue duo",
    ],
    "Malaria": [
        "trophozoites", "schizonts", "ring forms", "gametocytes", "blackwater fever",
        "cerebral malaria", "plasmodium", "falciparum", "vivax", "ovale", "malariae",
        "falciparum malaria", "vivax malaria", "plasmodium ring",
    ],
    "Ebola_Filovirus": [
        "igm elisa", "ebola igm", "filovirus antigen", "antigen detection",
        "convalescent antibody", "filovirus antibody",
    ],
    "Tuberculosis": [
        "caseating granuloma", "caseating granulomas", "langhans giant cells",
        "cavitary lesion", "apical cavity", "miliary tb", "acid-fast bacilli",
        "afb smear", "ziehl-neelsen", "miliary mottling", "pott disease", "pott's disease",
        "caseous necrosis", "tuberculous granuloma",
    ],
    "COVID-19": [
        "rapid antigen test", "rapid antigen positive", "covid antigen",
        "sars-cov-2 antigen", "nucleocapsid antigen", "rat positive",
        "positive rapid antigen", "lateral flow positive",
    ],
    "HIV_AIDS": [
        "pneumocystis jirovecii", "kaposi sarcoma", "kaposi's sarcoma",
        "cryptococcal meningitis", "opportunistic infection",
        "wasting syndrome", "oral candidiasis in hiv", "cd4 count < 200 in hiv",
        "hiv-1 reactive", "reactive 4th generation", "reactive fourth generation",
        "hiv positive antibody",
    ],
    "Chikungunya": [
        "chikungunya igm", "chkv igm", "chikungunya serology", "positive chkv igm",
        "chikv igm", "anti-chikungunya igm", "severe polyarthralgia", "bilateral joint swelling",
        "tenosynovitis in chikungunya",
    ],
    "Zika": [
        "zika igm", "zikv igm", "zika serology", "congenital zika syndrome",
        "microcephaly", "positive zikv igm", "anti-zika igm", "fetal microcephaly",
        "congenital zika", "intracranial calcifications with microcephaly",
    ],
    "Brucellosis": [
        "standard tube agglutination", "wright test", "rose bengal", "brucellacapt",
        "2-mercaptoethanol", "brucella agglutination", "brucella serology",
        "sta titer", "wright agglutination", "tube agglutination test", "sat titer",
        "coombs test for brucella", "positive rose bengal",
    ],
    "Leishmaniasis": [
        "rk39", "rk-39", "direct agglutination test", "dat titer",
        "visceral leishmaniasis serology", "kala-azar", "positive rk39",
        "rk39 dipstick", "rk39 rapid test", "anti-leishmania antibodies",
    ],
    "Typhoid_Fever": [
        "s. typhi pcr", "salmonella pcr", "rose spots", "relative bradycardia",
        "faget sign", "faget's sign", "step-ladder fever", "stepladder fever",
        "widal test positive", "widal o titer",
    ],
    "Cholera": [
        "cholera rdt", "crystal vc", "rice-water stool", "rice-water diarrhea",
        "rice water stool", "profuse watery diarrhea", "cholera rapid test",
        "rice water diarrhea",
    ],
    "Rabies": [
        "hydrophobia", "aerophobia", "negri bodies", "progressive encephalomyelitis",
        "hypersalivation and agitation", "autonomic instability with hydrophobia",
    ],
    "Leptospirosis": [
        "leptospira igm", "leptospirosis serology", "mat titer >= 1:100",
        "weil's disease", "weil disease", "conjunctival suffusion", "positive leptospira igm",
        "anti-leptospira igm", "mat titer of 1:100", "mat titer of 1:200",
    ],
    "Yellow_Fever": [
        "yellow fever igm", "yfv igm", "faget sign", "black vomitus",
        "vomito negro", "yellow fever serology", "anti-yfv igm",
    ],
}

# Tier 3A (E3): Epidemiological Exposures, Vectors, Food/Water & Animal Reservoirs
DISEASE_E3_EPIDEMIOLOGY = {
    "Dengue": [
        "aedes", "mosquito bite", "mosquito bites", "endemic area", "tropical travel",
        "caribbean", "latin america", "southeast asia", "aedes aegypti",
    ],
    "Malaria": [
        "anopheles", "mosquito bite", "mosquito bites", "endemic area",
        "travel to africa", "sub-saharan", "no malaria prophylaxis", "chemoprophylaxis",
        "anopheles mosquito",
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
        "aedes", "mosquito bite", "mosquito bites", "travel to endemic", "aedes albopictus",
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
        "mediterranean travel", "endemic area", "middle east travel", "sandfly bite",
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
        "negative for dengue", "ruled out dengue", "dengue was ruled out", "tested negative for dengue",
    ],
    "Malaria": [
        "smear negative for parasites", "no parasites seen", "malaria negative",
        "negative for malaria", "no plasmodium", "blood smear was negative",
        "rdt was negative for malaria", "ruled out malaria", "thick and thin smear were negative",
        "no malaria parasites", "tested negative for malaria",
    ],
    "Ebola_Filovirus": [
        "ebola negative", "ebola pcr negative", "negative for ebola", "ruled out ebola",
        "tested negative for ebola", "ebola was ruled out",
    ],
    "Tuberculosis": [
        "afb negative", "genexpert negative", "mtb pcr negative",
        "culture negative for m. tuberculosis", "negative for tb", "ruled out tuberculosis",
        "tuberculosis was ruled out", "tested negative for tb",
    ],
    "COVID-19": [
        "covid negative", "covid-19 negative", "sars-cov-2 negative",
        "pcr negative for sars-cov-2", "negative for covid-19", "rapid antigen negative",
        "tested negative for covid", "negative sars-cov-2", "sars-cov-2 was not detected",
        "tested negative for sars-cov-2",
    ],
    "HIV_AIDS": [
        "hiv negative", "nonreactive hiv", "non-reactive hiv", "hiv test was negative",
        "negative for hiv", "both hiv tests negative", "western blot negative",
        "elisa for hiv was negative", "hiv non-reactive", "undetectable hiv viral load",
        "tested negative for hiv",
    ],
    "Chikungunya": [
        "chikungunya negative", "chikungunya pcr negative", "chkv negative",
        "negative for chikungunya", "ruled out chikungunya", "tested negative for chikungunya",
    ],
    "Zika": [
        "zika negative", "zika pcr negative", "negative for zika", "ruled out zika",
        "tested negative for zika",
    ],
    "Brucellosis": [
        "brucella negative", "wright test negative", "rose bengal negative",
        "serology negative for brucella", "negative for brucellosis", "ruled out brucellosis",
        "tested negative for brucellosis",
    ],
    "Leishmaniasis": [
        "leishmania negative", "rk39 negative", "smear negative for leishmania",
        "negative for leishmaniasis", "ruled out leishmaniasis", "tested negative for leishmaniasis",
    ],
    "Typhoid_Fever": [
        "widal negative", "blood culture negative for salmonella",
        "negative for typhoid", "ruled out typhoid", "tested negative for typhoid",
    ],
    "Cholera": [
        "culture negative for vibrio", "negative for cholera", "ruled out cholera",
        "stool culture negative for vibrio", "tested negative for cholera",
    ],
    "Rabies": [
        "negative for rabies", "ruled out rabies", "tested negative for rabies",
    ],
    "Leptospirosis": [
        "mat negative", "leptospira negative", "negative for leptospirosis",
        "ruled out leptospirosis", "tested negative for leptospirosis",
    ],
    "Yellow_Fever": [
        "yellow fever negative", "yellow fever pcr negative", "negative for yellow fever",
        "ruled out yellow fever", "tested negative for yellow fever",
    ],
}

# Tier 4B: Spurious Homonyms & Discourse Mention Contexts (Filter out / Vote 0)
DISEASE_HOMONYMS = {
    "HIV_AIDS": [
        "walking aid", "walking aids", "mobility aid", "mobility aids",
        "hearing aid", "hearing aids", "visual aid", "visual aids",
        "first aid", "band aid", "teaching aid", "mother was hiv-positive",
        "maternal hiv", "partner had hiv",
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
        "during the covid-19 pandemic", "in the covid-19 era", "amidst the covid-19 pandemic",
        "during the pandemic", "covid-19 precautions", "ppe precautions",
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

# ─────────────────────────────────────────────────────────────────────────────
# Concluding Diagnostic Frames & Alternative Disease Indicators
# ─────────────────────────────────────────────────────────────────────────────
# Explicit diagnostic confirmation phrasing typically found in title or concluding narrative
CONCLUDING_DIAGNOSIS_PATTERNS = [
    r"\b(final|definitive|confirmed|discharge|primary|histological|pathological)\s+diagnosis\s+(?:was|is|of)\s+([a-zA-Z\s\-]{3,45})",
    r"\bwas\s+(?:finally\s+)?diagnosed\s+with\s+([a-zA-Z\s\-]{3,45})",
    r"\bdiagnosis\s+of\s+([a-zA-Z\s\-]{3,45})\s+was\s+(?:confirmed|established|made)\b",
    r"\b(?:biopsy|histopathology|surgical pathology|pathology)\s+(?:revealed|confirmed|showed)\s+([a-zA-Z\s\-]{3,45})",
    r"\bconsistent\s+with\s+(?:a\s+diagnosis\s+of\s+)?([a-zA-Z\s\-]{3,45})",
    r"\bstarted\s+on\s+[^.\n]{0,30}\s+(?:for|to treat)\s+([a-zA-Z\s\-]{3,45})",
]
# Explicit non-target disease entities frequently encountered in rule-out case series
COMMON_NON_TARGET_DISEASE_TERMS = [
    "familial mediterranean fever", "fmf",
    "adenocarcinoma", "carcinoma", "lymphoma", "leukemia", "sarcoma", "melanoma",
    "systemic lupus erythematosus", "lupus", "sle",
    "felty syndrome", "rheumatoid arthritis", "juvenile idiopathic arthritis",
    "acinetobacter", "pseudomonas", "klebsiella", "leptotrichia", "enterococcus",
    "kawasaki disease", "still's disease", "adult-onset still",
    "sarcoidosis", "syphilis", "treponema pallidum", "endocarditis",
    "pheochromocytoma", "iga vasculitis", "henoch-schonlein", "vasculitis",
    "hidradenitis suppurativa", "hereditary angioedema", "c1-inh",
    "chagas", "trypanosoma", "cruzi",
    "west nile", "west nile virus", "wnv",
    "cryptococcal", "cryptococcus", "cryptococcosis",
    "leprosy", "mycobacterium leprae", "hansen's disease",
    "cystic fibrosis",
    "lupus nephritis",
    "monkeypox", "mpox",
    "lassa fever",
    "powassan",
    "ramsay hunt", "herpes zoster",
    "cryptosporidium", "cryptosporidiosis",
    "patent foramen ovale", "foramen ovale", "atrial septal defect",
    "vitt", "vaccine-induced immune thrombotic thrombocytopenia",
    "coronary artery atresia",
    "compartment syndrome",
    "necrotizing soft tissue infection", "necrotizing fasciitis",
    "post dengue mania",
    "amebic liver abscess", "entamoeba histolytica",
    "mycobacterium mucogenicum", "non-tuberculous mycobacteria", "ntm",
]
# Generic complications of infectious diseases that must NEVER be flagged as "alternative diseases"
GENERIC_COMPLICATION_BLACKLIST = {
    "ards", "acute respiratory distress syndrome",
    "septic shock", "sepsis", "severe sepsis",
    "multi-organ failure", "multiorgan failure", "multiple organ dysfunction",
    "acute kidney injury", "aki", "renal failure",
    "hepatic failure", "acute liver failure",
    "cardiac arrest", "heart failure", "cardiogenic shock",
    "respiratory failure", "hypoxemic respiratory failure",
    "disseminated intravascular coagulation", "dic",
    "thrombocytopenia", "severe thrombocytopenia",
    "secondary bacterial pneumonia", "bacterial superinfection",
    "encephalopathy", "coagulopathy",
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
    r"\bwhole-of-society response\b",
    r"\bpopulation-level response\b",
    r"\brefugee population spread across\b",
]

# Single Patient Anchor Indicators (Demonstrates single human patient CCU)
SINGLE_PATIENT_ANCHOR_PATTERNS = [
    r"\b(a \d+[\s-]year[\s-]old|a \d+[\s-]month[\s-]old|the patient (is|was) a|a female patient|a male patient|presented with|was admitted (to|with)|born to a|neonate born)\b",
]

# Non-Human / Veterinary Document Patterns (Must be excluded)
NON_HUMAN_PATTERNS = [
    # Veterinary context & institutions
    r"\bveterinary\s+(clinic|hospital|faculty|school|medicine|college|center|service)\b",
    r"\bclinical nutrition service at the ontario veterinary college\b",
    r"\bin companion animals\b",
    r"\banimal cases?\b",
    
    # Explicit single-animal subjects in title or presentation
    r"\b(domestic short-?hair(ed)?|domestic cat|castrated male cat|neutered (male|female) cat)\b",
    r"\b(female|male)\s+(cat|dog|feline|canine)\b",
    r"\b(in|of)\s+a\s+(cat|dog|feline|canine|alpaca|cria|tiger|ferret)\b",
    r"\b(a|the)\s+\d+[\s-](year|month|day|week)[\s-]old[^\.\n]{0,40}\b(cat|dog|feline|canine|alpaca|cria|kitten|puppy|panda|tiger|bulldog|pomeranian|hound)\b",
    
    # Specific animal species/breeds when subjects
    r"\b(alpaca|cria|red panda|american bulldog|pomeranian)\b",
    r"\bcanine\s+(patient|case|leishmaniosis|distemper|parvovirus)\b",
    r"\bfeline\s+(patient|case|leishmaniosis|infectious peritonitis)\b",
    r"\bmeningoencephalomyelitis of unknown origin in cats\b",
    
    # Laboratory animal models
    r"\bmurine model\b",
    r"\bmice were inoculated\b",
    r"\brabbits were\b",
    r"\brats were infected\b",
    r"\bcows were\b",
]

# Pathogen / Organism keywords for Relational Evidence Grounding
DISEASE_ORGANISMS = {
    "Dengue": ["dengue", "denv", "denv-1", "denv-2", "denv-3", "denv-4"],
    "Malaria": ["malaria", "plasmodium", "falciparum", "vivax", "plasmodium ovale", "p. ovale", "malariae", "knowlesi"],
    "Ebola_Filovirus": ["ebola", "marburg", "filovirus", "ebolavirus", "zaire", "sudan ebolavirus"],
    "Tuberculosis": ["tuberculosis", "mycobacterium", "m. tuberculosis", "mtb", "mtbc", "acid-fast", "afb", "tb", "tuberculous", "tubercular"],
    "COVID-19": ["sars-cov-2", "covid-19", "coronavirus disease 2019", "covid19", "2019-ncov", "omicron", "covid"],
    "HIV_AIDS": ["hiv", "human immunodeficiency virus", "aids", "hiv-1", "hiv-2", "antiretroviral", "haart"],
    "Chikungunya": ["chikungunya", "chkv", "chikv", "chicungunha"],
    "Zika": ["zika", "zikv"],
    "Brucellosis": ["brucella", "brucellosis", "melitensis", "abortus", "suis", "canis"],
    "Leishmaniasis": ["leishmania", "amastigote", "amastigotes", "ld body", "ld bodies", "kala-azar", "infantum", "donovani", "tropica", "braziliensis"],
    "Typhoid_Fever": ["salmonella typhi", "s. typhi", "salmonella paratyphi", "s. paratyphi", "typhoid fever", "enteric fever", "typhoid"],
    "Cholera": ["cholera", "vibrio cholerae", "v. cholerae", "vibrio cholera"],
    "Rabies": ["rabies", "lyssavirus", "negri bodies"],
    "Leptospirosis": ["leptospir", "weil disease", "leptospirosis", "leptospira interrogans"],
    "Yellow_Fever": ["yellow fever", "yfv"],
}

LAB_CONFIRMATORY_ROOTS = [
    "pcr", "rt-pcr", "naat", "culture", "isolate", "isolation", "smear",
    "film", "antigen", "ns1", "genexpert", "xpert", "elisa", "mat", "agglutination",
    "serology", "serological", "seropositive", "igm", "titer", "titre", "biopsy",
    "amastigote", "western blot", "viral load", "rdt", "diagnosed with",
    "confirmed", "identified as", "detected", "yielded", "flagged positive", "grew"
]

import re

# Strict negation regex with word boundaries to avoid matching "abnormal" as "normal"
COMPILED_NEGATIONS = re.compile(
    r"\b(negative|not detected|no growth|non-reactive|nonreactive|undetectable|ruled out|no evidence|unremarkable|unrevealing|failed to detect|absence of|sterile|did not show|misinterpretation|misinterpreted|misidentification|misidentified)\b|(?<!ab)\bnormal\b",
    re.IGNORECASE
)

COMPILED_PAST_OR_FAMILY = re.compile(
    r"\b(in childhood|years ago|months ago|past medical history|mother|father|parent|partner|wife|husband|brother|sister|differential diagnosis|suspected but excluded)\b",
    re.IGNORECASE
)

SPECIMEN_WORDS = [
    "blood", "serum", "sera", "plasma", "bone marrow", "csf", "cerebrospinal",
    "nasopharyngeal", "respiratory", "sputum", "stool", "feces", "urine",
    "saliva", "skin", "nuchal", "biopsy", "aspirate", "swab", "tissue",
    "specimen", "sample", "bottle", "bottles", "film", "smear", "trephine",
    "bal", "bronchoalveolar", "swabs"
]

AFFIRMATORY_ACTION_WORDS = [
    "positive", "isolated", "isolation", "isolate", "cultured", "culture",
    "detected", "detection", "yielded", "flagged positive", "grew", "growth",
    "demonstrated", "confirmed", "visualized", "visualization", "revealed",
    "identified", "reactive", "amplified", "found"
]


# ═══════════════════════════════════════════════════════════════════════════════
#  Dynamic Mathematical Titer Parsers (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════════

def parse_brucellosis_titer(text: str) -> bool:
    """
    Dynamic mathematical titer parser for Brucellosis.
    Standard Tube Agglutination (STA), Wright agglutination, SAT, or Coombs titer >= 1:160
    is diagnostic in clinically compatible illness. Catches 1:160, 1:320, 1:400, 1:640, 1:800, 1:1280, etc.
    """
    if not text:
        return False
    t_lower = text.lower()
    for m in re.finditer(r"1\s*[:/]\s*(\d+)", t_lower):
        try:
            denom = int(m.group(1))
        except ValueError:
            continue
        start = max(0, m.start() - 60)
        end = min(len(t_lower), m.end() + 60)
        window = t_lower[start:end]
        if any(w in window for w in ["sta", "sat", "wright", "agglutin", "brucell", "coombs", "tube"]):
            if denom >= 160:
                return True
    return False


def parse_leptospirosis_titer(text: str, min_denom: int = 100) -> bool:
    """
    Dynamic mathematical titer parser for Leptospirosis.
    Microscopic Agglutination Test (MAT) titer >= 1:400 (confirmatory E1) or >= 1:100 (E2).
    """
    if not text:
        return False
    t_lower = text.lower()
    for m in re.finditer(r"1\s*[:/]\s*(\d+)", t_lower):
        try:
            denom = int(m.group(1))
        except ValueError:
            continue
        start = max(0, m.start() - 60)
        end = min(len(t_lower), m.end() + 60)
        window = t_lower[start:end]
        if any(w in window for w in ["mat", "microscopic agglutin", "leptospir"]):
            if denom >= min_denom:
                return True
    return False


def parse_leishmaniasis_titer(text: str, min_denom: int = 800) -> bool:
    """
    Dynamic mathematical titer parser for Leishmaniasis.
    Direct Agglutination Test (DAT) titer >= 1:800 (confirmatory/strong serology).
    """
    if not text:
        return False
    t_lower = text.lower()
    for m in re.finditer(r"1\s*[:/]\s*(\d+)", t_lower):
        try:
            denom = int(m.group(1))
        except ValueError:
            continue
        start = max(0, m.start() - 60)
        end = min(len(t_lower), m.end() + 60)
        window = t_lower[start:end]
        if any(w in window for w in ["dat", "direct agglutin", "leishmani"]):
            if denom >= min_denom:
                return True
    return False


# ═══════════════════════════════════════════════════════════════════════════════
#  Directional Predicate Frames & Relational Affirmation (Phase 2)
# ═══════════════════════════════════════════════════════════════════════════════

def is_valid_relational_affirmation(text: str, disease_name: str) -> bool:
    """
    Directional Predicate Frame matching:
    Validates Clause = [Specimen] -> (<= 15 tokens) -> [Affirmatory Action] -> (<= 10 tokens) -> [Pathogen]
    or reverse permutations, terminating at conjunctions, and strictly verifying absence of negation.
    Also incorporates dynamic mathematical titer parsers.
    """
    if not text:
        return False

    # Check disease-specific confirmatory mathematical titers (E1)
    if disease_name == "Leptospirosis" and parse_leptospirosis_titer(text, min_denom=400):
        return True
    if disease_name == "Leishmaniasis" and parse_leishmaniasis_titer(text, min_denom=800):
        return True

    orgs = DISEASE_ORGANISMS.get(disease_name, [])
    if not orgs:
        return False

    homonyms = DISEASE_HOMONYMS.get(disease_name, [])
    t_lower = text.lower()

    # Split into clauses by sentence endings and conjunctions
    clauses = re.split(r"[.\n;]|,\s*(?:but|however|although|whereas|while|despite)\s+", t_lower)
    for clause in clauses:
        clause = clause.strip()
        if not clause:
            continue

        # Skip clauses matching known disease homonyms (e.g., rabies vaccine, foramen ovale)
        if any(h in clause for h in homonyms):
            continue

        # Check if clause contains target pathogen
        matched_orgs = [org for org in orgs if re.search(rf"\b{re.escape(org)}\b", clause)]
        if not matched_orgs:
            continue

        # Check for confirmatory lab roots or affirmatory actions
        has_lab = any(lab in clause for lab in LAB_CONFIRMATORY_ROOTS)
        has_action = any(act in clause for act in AFFIRMATORY_ACTION_WORDS)
        if not (has_lab or has_action):
            continue

        # Check if clause contains specimen context
        has_specimen = any(spec in clause for spec in SPECIMEN_WORDS)

        # Check negation: word boundary regex ensures 'abnormal' is not treated as 'normal'
        if COMPILED_NEGATIONS.search(clause):
            continue

        # Check remote past or family member context
        if COMPILED_PAST_OR_FAMILY.search(clause):
            continue

        # Predicate frame satisfied
        if has_specimen or has_action:
            return True

    return False




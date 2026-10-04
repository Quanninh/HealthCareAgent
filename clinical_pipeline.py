import json
import pandas as pd
import numpy as np

# Note: To run the Snorkel portion, you will need to install snorkel:
# pip install snorkel pandas numpy

try:
    from snorkel.labeling import labeling_function, PandasLFApplier
    from snorkel.labeling.model import LabelModel
except ImportError:
    print("Please install snorkel: pip install snorkel")

# ==========================================
# STEP 3: Ontology Grounding (Mock SapBERT)
# ==========================================
# In a production environment, this would call a local MedCAT instance
# or a HuggingFace SapBERT model to return real UMLS CUIs.
# For this script, we use a mock dictionary to demonstrate the transformation.

MOCK_ONTOLOGY_DB = {
    "fatigue": {"cui": "C0015672", "standard_name": "Fatigue"},
    "loss of appetite": {"cui": "C0232462", "standard_name": "Decreased appetite"},
    "fever": {"cui": "C0015967", "standard_name": "Fever"},
    "covid-19": {"cui": "C5203670", "standard_name": "COVID-19"},
    "ground-glass opacities": {"cui": "C2073530", "standard_name": "Ground glass opacity"},
    "chilblains-like lesions": {"cui": "C0008182", "standard_name": "Chilblains"}
}

def step3_ontology_grounding(clinical_entities):
    """
    Takes the raw entities from Step 2 and maps them to standard IDs.
    """
    grounded_entities = []
    for entity in clinical_entities:
        text = entity.get("text_span", "").lower()
        
        # Try to find a match in our "Database"
        match = None
        for key, value in MOCK_ONTOLOGY_DB.items():
            if key in text:
                match = value
                break
        
        # Append the grounding data
        if match:
            entity["ontology_mapping"] = {
                "umls_cui": match["cui"],
                "standard_name": match["standard_name"],
                "status": "Mapped"
            }
        else:
            entity["ontology_mapping"] = {
                "umls_cui": None,
                "standard_name": None,
                "status": "Unmapped"
            }
        grounded_entities.append(entity)
        
    return grounded_entities


# ==========================================
# STEP 4: Snorkel Weak Supervision
# ==========================================
# Task: Predict if the document confirms an active COVID-19 diagnosis.

ABSTAIN = -1
NEGATIVE = 0
POSITIVE = 1

# Labeling Function 1 (The LLM / Step 3 Vote)
@labeling_function()
def lf_llm_affirmed_covid(x):
    # Check if our LLM extracted COVID-19 and affirmed it
    for entity in x.clinical_entities:
        mapping = entity.get("ontology_mapping", {})
        if mapping.get("umls_cui") == "C5203670": # COVID-19 CUI
            if entity.get("assertion") == "affirmed":
                return POSITIVE
            elif entity.get("assertion") == "negated":
                return NEGATIVE
    return ABSTAIN

# Labeling Function 2 (Legacy Regex / Heuristic)
@labeling_function()
def lf_pcr_negative(x):
    text = str(x.case_presentation).lower()
    if "rt-pcr was negative" in text or "pcr negative" in text:
        return NEGATIVE
    return ABSTAIN

# Labeling Function 3 (Clinical Symptom Heuristic)
@labeling_function()
def lf_ground_glass_opacities(x):
    # Ground glass opacities are highly indicative of COVID pneumonia
    for entity in x.clinical_entities:
        mapping = entity.get("ontology_mapping", {})
        if mapping.get("umls_cui") == "C2073530" and entity.get("assertion") == "affirmed":
            return POSITIVE
    return ABSTAIN

def step4_apply_snorkel(df):
    """
    Applies the labeling functions and trains the Snorkel LabelModel
    to calculate a final probability score.
    """
    lfs = [lf_llm_affirmed_covid, lf_pcr_negative, lf_ground_glass_opacities]
    applier = PandasLFApplier(lfs=lfs)
    
    # 1. Get the vote matrix from our rules
    print("Applying Labeling Functions...")
    L_train = applier.apply(df=df)
    
    # 2. Train the Snorkel LabelModel to resolve conflicts
    # (It learns which rules are most accurate automatically)
    print("Training Snorkel LabelModel...")
    label_model = LabelModel(cardinality=2, verbose=False)
    label_model.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=123)
    
    # 3. Predict the final probability (0.0 to 1.0)
    # Get the probability of the POSITIVE class (index 1)
    probs = label_model.predict_proba(L_train)
    df['covid_probability'] = probs[:, 1] 
    
    return df


# ==========================================
# STEP 5: Active Learning Thresholds
# ==========================================
def step5_route_records(df, threshold=0.85):
    """
    Routes records based on the Snorkel probability.
    > Threshold = Auto Accept
    < Threshold = Human Review (SME Dashboard)
    """
    auto_accepted = []
    human_review_queue = []
    
    for index, row in df.iterrows():
        prob = row['covid_probability']
        
        record = {
            "case_id": row['case_id'],
            "probability": f"{prob:.2f}",
            "gold_disease": row['gold_disease']
        }
        
        # Route based on confidence
        if prob >= threshold or prob <= (1 - threshold): 
            # High confidence positive OR high confidence negative
            record['status'] = "AUTO_ACCEPTED"
            auto_accepted.append(record)
        else:
            # Low confidence (conflicting signals) -> Route to Human
            record['status'] = "REQUIRES_HUMAN_REVIEW"
            human_review_queue.append(record)
            
    return auto_accepted, human_review_queue


# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    file_path = "labeled_cases_top5.jsonl"
    
    print(f"Loading data from {file_path}...\n")
    data = []
    with open(file_path, 'r') as f:
        for line in f:
            data.append(json.loads(line))
            
    # Run Step 3
    print("--- RUNNING STEP 3: ONTOLOGY GROUNDING ---")
    for record in data:
        record['clinical_entities'] = step3_ontology_grounding(record['clinical_entities'])
    print(f"Grounded entities for {len(data)} records.\n")
    
    # Convert to DataFrame for Snorkel
    df = pd.DataFrame(data)
    
    # Run Step 4
    print("--- RUNNING STEP 4: SNORKEL WEAK SUPERVISION ---")
    if 'LabelModel' in globals():
        df = step4_apply_snorkel(df)
        print("\nCalculated Probabilities:")
        for idx, row in df.iterrows():
            print(f"[{row['case_id']}] COVID-19 Probability: {row['covid_probability']:.2f}")
    else:
        print("Snorkel not installed. Skipping Step 4.\n")
        
    # Run Step 5
    if 'covid_probability' in df.columns:
        print("\n--- RUNNING STEP 5: ROUTING (Threshold = 0.85) ---")
        accepted, review = step5_route_records(df, threshold=0.85)
        
        print(f"\nAUTO-ACCEPTED ({len(accepted)} records):")
        for r in accepted: print(f"  -> {r['case_id']} (Prob: {r['probability']})")
            
        print(f"\nHUMAN REVIEW QUEUE ({len(review)} records):")
        for r in review: print(f"  -> {r['case_id']} (Prob: {r['probability']}) - CONFLICTING SIGNALS!")

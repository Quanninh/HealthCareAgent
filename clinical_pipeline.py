import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import re
import json
import pandas as pd
import numpy as np
from medcat.cat import CAT

try:
    from snorkel.labeling import labeling_function, PandasLFApplier
    from snorkel.labeling.model import LabelModel, MajorityLabelVoter
except ImportError as e:
    print(f"\n WARNING: Snorkel failed to import. The exact error is:\n{e}\n")

"""Step 3"""

print("Loading MedCAT UMLS Model (This may take a minute...)")
cat = CAT.load_model_pack("MedCAT/umls_self_train_model_pt2ch_3760d588371755d0.zip") 
def step3_ontology_grounding(clinical_entities):
    grounded_entities = []
    
    for entity in clinical_entities:
        # Safely handle None values from JSON
        text_span = entity.get("text_span") or ""
        text_span = text_span.lower()
        
        # Use the full sentence for context, fallback to text_span if missing or None
        context = entity.get("sentence_context")
        if not context:
            context = text_span
            
        # Pass the ENTIRE sentence to MedCAT. 
        # This gives MedCAT the surrounding words it needs to correctly disambiguate!
        medcat_results = cat.get_entities(str(context))
        
        best_match = None
        if medcat_results and len(medcat_results['entities']) > 0:
            # MedCAT found concepts in the sentence. We need to find the one that matches our specific text_span.
            for ent_id, ent_data in medcat_results['entities'].items():
                medcat_word = ent_data['source_value'].lower()
                # If MedCAT's found word overlaps with our LLM's text span, we found our target!
                if medcat_word in text_span or text_span in medcat_word:
                    best_match = ent_data
                    break
            
            if best_match:
                entity["ontology_mapping"] = {
                    "umls_cui": best_match['cui'],
                    "standard_name": best_match['pretty_name'],
                    "status": "Mapped"
                }
            else:
                entity["ontology_mapping"] = {
                    "umls_cui": None,
                    "standard_name": None,
                    "status": "Unmapped"
                }
        else:
            entity["ontology_mapping"] = {
                "umls_cui": None,
                "standard_name": None,
                "status": "Unmapped"
            }
        grounded_entities.append(entity)
        
    return grounded_entities


"""Step 4"""

ABSTAIN = -1
INVALID = 0  # Not an active problem for the patient (e.g. negated, historical, family member)
VALID = 1    # Confirmed active problem for the patient

@labeling_function()
def lf_regex_negation(x):
    """
    The True LF 1 (Heuristic): Independent Regex Negation Check.
    If the LLM accidentally marks something as 'affirmed', but the raw text
    clearly says 'rules out', this independent juror will catch it and vote INVALID.
    """
    text_span = str(x.text_span).lower()
    raw_text = str(x.case_presentation).lower()
    
    # Check for common negation phrases allowing for up to 3 intermediate words
    escaped_span = re.escape(text_span)
    negation_pattern = re.compile(rf"(rules out|denies|no evidence of)(?:\s+\w+){{0,3}}\s+{escaped_span}")
    
    if negation_pattern.search(raw_text):
        return INVALID
        
    return ABSTAIN

@labeling_function()
def lf_llm_assertion(x):
    if x.assertion == "affirmed": return VALID
    if x.assertion == "negated": return INVALID
    return ABSTAIN

@labeling_function()
def lf_experiencer_filter(x):
    if x.experiencer in ["family_member", "other"]:
        return INVALID
    return ABSTAIN

@labeling_function()
def lf_temporality_filter(x):
    if x.temporality == "historical":
        return INVALID
    return ABSTAIN

@labeling_function()
def lf_medcat_validation(x):
    """
    Independent Juror 1: If MedCAT failed to find a dictionary ID for this term,
    it is likely an LLM hallucination or a non-clinical word. Vote INVALID.
    """
    mapping = x.ontology_mapping if pd.notnull(x.ontology_mapping) else {}
    if mapping.get('status') == 'Unmapped' or mapping.get('umls_cui') is None:
        return INVALID
    return VALID

@labeling_function()
def lf_raw_text_check(x):
    """
    Independent Juror 2: Does the exact text span exist in the raw doctor's note?
    If not, the LLM hallucinated the entity entirely. Vote INVALID.
    """
    text_span = str(x.text_span).lower()
    raw_text = str(x.case_presentation).lower()
    
    if text_span not in raw_text:
        return INVALID
    return VALID


def step4_apply_snorkel(df_entities):
    """
    Applies the labeling functions to the flattened entity dataframe.
    """
    lfs = [
        lf_regex_negation,
        lf_llm_assertion, 
        lf_experiencer_filter, 
        lf_temporality_filter, 
        lf_medcat_validation,
        lf_raw_text_check
    ]
    applier = PandasLFApplier(lfs=lfs)
    
    print("Applying Labeling Functions to all entities...")
    L_train = applier.apply(df=df_entities)
    
    print("Computing probabilities with Majority Vote (LabelModel shrinks scores on small datasets)...")
    label_model = MajorityLabelVoter(cardinality=2)
    
    probs = label_model.predict_proba(L_train)

    df_entities['valid_probability'] = probs[:, 1] 
    
    return df_entities


# ==========================================
# STEP 5: Active Learning Thresholds
# ==========================================
def step5_route_entities(df_entities, threshold=0.85):
    auto_accepted = []
    human_review = []
    
    for index, row in df_entities.iterrows():
        prob = row['valid_probability']
        ontology = row.get('ontology_mapping', {})
        
        record = {
            "case_id": row['case_id'],
            "entity": row['text_span'],
            "cui": ontology.get('umls_cui'),
            "standard_name": ontology.get('standard_name'),
            "probability": f"{prob:.2f}",
            "assertion": row['assertion'],
            "experiencer": row['experiencer']
        }
        
        if prob >= threshold: 
            auto_accepted.append(record)
        else:
            human_review.append(record)
            
    return auto_accepted, human_review


# ==========================================
# STEP 6 (STAGE 2): DISEASE PREDICTION
# ==========================================
# 1. Define the Stage 2 Label Space
ABSTAIN = -1
COVID19 = 0
TUBERCULOSIS = 1
DENGUE = 2

# Map indices to names for output
DISEASE_MAP = {COVID19: "covid19", TUBERCULOSIS: "tuberculosis", 
               DENGUE: "dengue"}

COVID19_SIGNS = ["covid", "sars-cov-2", "coronavirus", "ground-glass", "anosmia", "ageusia", "loss of taste", "loss of smell"]
TUBERCULOSIS_SIGNS = ["tuberculosis", "tb", "mycobacterium", "hemoptysis", "night sweats", "cavitary lesion", "granuloma", "caseous"]
DENGUE_SIGNS = ["dengue", "tourniquet test", "ns1 antigen", "retro-orbital pain", "breakbone fever", "dengue hemorrhagic fever", "petechiae", "thrombocytopenia"]

# Automatically run MedCAT on our lists to generate their UMLS standard names!
def standardize_signs(signs):
    mapped_signs = set(signs) # Keep original words as a fallback
    for sign in signs:
        res = cat.get_entities(sign)
        if res and res['entities']:
            for ent in res['entities'].values():
                mapped_signs.add(ent['pretty_name'].lower())
    return list(mapped_signs)

COVID19_SIGNS = standardize_signs(COVID19_SIGNS)
TUBERCULOSIS_SIGNS = standardize_signs(TUBERCULOSIS_SIGNS)
DENGUE_SIGNS = standardize_signs(DENGUE_SIGNS)

# ECHINOCOCCOSIS_SIGNS = ["hydatid cyst", "cyst", "abdominal mass", "liver cyst"]
# CRYPTOCOCCOSIS_SIGNS = ["headache", "neck stiffness", "meningitis", "confusion"]

# 3. The Stage 2 Labeling Functions
@labeling_function()
def lf_diagnose_covid(x):
    if any(sign in x.valid_symptoms for sign in COVID19_SIGNS):
        return COVID19
    return ABSTAIN

@labeling_function()
def lf_diagnose_tb(x):
    if any(sign in x.valid_symptoms for sign in TUBERCULOSIS_SIGNS):
        return TUBERCULOSIS
    return ABSTAIN

# @labeling_function()
# def lf_diagnose_chikungunya(x):
#     if any(sign in x.valid_symptoms for sign in CHIKUNGUNYA_SIGNS):
#         return CHIKUNGUNYA
#     return ABSTAIN

@labeling_function()
def lf_diagnose_dengue(x):
    if any(sign in x.valid_symptoms for sign in DENGUE_SIGNS):
        return DENGUE
    return ABSTAIN

# @labeling_function()
# def lf_diagnose_echinococcosis(x):
#     if any(sign in x.valid_symptoms for sign in ECHINOCOCCOSIS_SIGNS):
#         return ECHINOCOCCOSIS
#     return ABSTAIN

# @labeling_function()
# def lf_diagnose_crypto(x):
#     if any(sign in x.valid_symptoms for sign in CRYPTOCOCCOSIS_SIGNS):
#         return CRYPTOCOCCOSIS
#     return ABSTAIN

def step6_stage2_disease_prediction(raw_data, accepted_entities):
    """
    Stage 2: Uses a second Snorkel model to predict the disease 
    based purely on the validated symptoms from Stage 1.
    """
    # 1. Group VALID entities by case using UMLS standard_name when available!
    valid_by_case = {}
    for r in accepted_entities:
        cid = r['case_id']
        if cid not in valid_by_case:
            valid_by_case[cid] = []
        if float(r['probability']) >= 0.85:
            # Safely add BOTH the MedCAT standard_name AND the raw LLM text
            # This ensures your LF lists can match against either the official term or the raw slang!
            if r.get('standard_name'):
                valid_by_case[cid].append(r['standard_name'].lower())
            valid_by_case[cid].append(r['entity'].lower())
            
    # 2. Build the Document-Level DataFrame (No gold_disease here!)
    patient_cases = []
    for case in raw_data:
        cid = case['case_id']
        patient_cases.append({
            "case_id": cid,
            "valid_symptoms": valid_by_case.get(cid, [])
        })
        
    df_patients = pd.DataFrame(patient_cases)
    
    # 3. Apply Stage 2 LFs
    lfs_stage_2 = [
        lf_diagnose_covid, 
        lf_diagnose_tb, 
        lf_diagnose_dengue
    ]
    applier = PandasLFApplier(lfs=lfs_stage_2)
    
    L_train_stage2 = applier.apply(df=df_patients)
    
    # Cardinality = 3 for our 3 diseases
    disease_model = LabelModel(cardinality=3, verbose=False)
    disease_model.fit(L_train=L_train_stage2, n_epochs=500, seed=123)
    
    # 4. Predict probabilities (Pick the highest score!)
    probs = disease_model.predict_proba(L_train_stage2)
    predicted_indices = np.argmax(probs, axis=1)
    
    # 5. Format results
    results = []
    for i, row in df_patients.iterrows():
        best_index = predicted_indices[i]
        winning_score = probs[i][best_index]
        
        # If the model abstained entirely (score is evenly split, i.e., ~0.33 for 3 classes)
        if winning_score <= 0.34:
            predicted_disease = "UNKNOWN (Insufficient Evidence)"
        else:
            predicted_disease = DISEASE_MAP.get(best_index, "Unknown")
            
        results.append({
            "case_id": row['case_id'],
            "predicted_disease": predicted_disease,
            "confidence": f"{winning_score:.2f}",
            "evidence_used": row['valid_symptoms']
        })
        
    return results

# ==========================================
# MAIN EXECUTION
# ==========================================
file_path = "extracted_cases_top3.jsonl"

print("Loading case documents...\n")
raw_data = []
with open(file_path, 'r') as f:
    for line in f:
        raw_data.append(json.loads(line))
        
print("--- RUNNING STEP 3: ONTOLOGY GROUNDING ---")
for record in raw_data:
    record['clinical_entities'] = step3_ontology_grounding(record['clinical_entities'])

# Flatten the data for Snorkel
flattened_entities = []
for record in raw_data:
    for ent in record['clinical_entities']:
        ent['case_id'] = record['case_id']
        # NEW: Attach the raw text to the entity so Snorkel can cross-check it!
        ent['case_presentation'] = record.get('case_presentation', '')
        flattened_entities.append(ent)
        
df_entities = pd.DataFrame(flattened_entities)
print(f"Flattened data into {len(df_entities)} individual clinical entities.\n")

print("--- RUNNING STEP 4: SNORKEL WEAK SUPERVISION ---")
if 'LabelModel' in globals():
    df_entities = step4_apply_snorkel(df_entities)
    
    print("\n--- RUNNING STEP 5: ENTITY ROUTING (Threshold = 0.85) ---")
    accepted, review = step5_route_entities(df_entities, threshold=0.85)
    
    # --- NEW: Asynchronous Human Review Export ---
    
    # 1. Save the AUTO-ACCEPTED entities
    accepted_filename = "accepted_entities.json"
    with open(accepted_filename, "w") as f:
        json.dump(accepted, f, indent=4)
    print(f"Saved {len(accepted)} AUTO-ACCEPTED entities to {accepted_filename}.")
    
    # 2. Add 'PENDING' flag and save the HUMAN REVIEW queue
    review_filename = "human_review_queue.json"
    for r in review:
        r['expert_decision'] = "PENDING"
        
    with open(review_filename, "w") as f:
        json.dump(review, f, indent=4)
    print(f"Saved {len(review)} entities to {review_filename} for expert review.")
    print("Please review the JSON file, change 'PENDING' to 'APPROVED', and then run stage2_prediction.py!")
    print("\n===========================================\n")

else:
    print("Snorkel not installed. Skipping Step 4.\n")

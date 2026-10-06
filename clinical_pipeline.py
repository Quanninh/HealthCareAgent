import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

import json
import pandas as pd
import numpy as np
from medcat.cat import CAT
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

try:
    from snorkel.labeling import labeling_function, PandasLFApplier
    from snorkel.labeling.model import LabelModel
except ImportError as e:
    print(f"\n WARNING: Snorkel failed to import. The exact error is:\n{e}\n")

"""Step 3"""

print("Loading MedCAT UMLS Model (This may take a minute...)")
cat = CAT.load_model_pack("MedCAT/umls_self_train_model_pt2ch_3760d588371755d0.zip") 
def step3_ontology_grounding(clinical_entities):
    grounded_entities = []
    
    for entity in clinical_entities:
        text = entity.get("text_span", "")
        
        # Pass the extracted string to MedCAT
        medcat_results = cat.get_entities(text)
        
        if medcat_results and len(medcat_results['entities']) > 0:
            # Grab the best match
            best_match = list(medcat_results['entities'].values())[0]
            
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
    
    # Check for common negation phrases right next to the disease name
    if f"rules out {text_span}" in raw_text or f"denies {text_span}" in raw_text or f"no evidence of {text_span}" in raw_text:
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
    return ABSTAIN

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
    return ABSTAIN


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
    
    print("Training Snorkel LabelModel...")
    label_model = LabelModel(cardinality=2, verbose=False)
    label_model.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=123)
    
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
        record = {
            "case_id": row['case_id'],
            "entity": row['text_span'],
            "cui": row.get('ontology_mapping', {}).get('umls_cui'),
            "probability": f"{prob:.2f}",
            "assertion": row['assertion'],
            "experiencer": row['experiencer']
        }
        
        if prob >= threshold or prob <= (1 - threshold): 
            auto_accepted.append(record)
        else:
            human_review.append(record)
            
    return auto_accepted, human_review


# ==========================================
# STEP 6: Document-Level Diagnosis Verification
# ==========================================
def step6_verify_gold_disease(raw_data, accepted_entities):
    """
    Evaluates the 'gold_disease' based purely on the mathematically validated entities.
    """
    # Initialize the client ONCE outside the loop to make it run faster
    load_dotenv()
    HF_TOKEN = os.getenv("HF_TOKEN")
    client = InferenceClient(model="meta-llama/Meta-Llama-3-8B-Instruct", token=HF_TOKEN)
    # 1. Group validated entities by case (only keeping the VALID ones)
    valid_by_case = {}
    for r in accepted_entities:
        cid = r['case_id']
        if cid not in valid_by_case:
            valid_by_case[cid] = []
        
        # Only keep it if it was classified as VALID (> 0.85)
        if float(r['probability']) >= 0.85:
            valid_by_case[cid].append(r['entity'].lower())
        
    results = []
    
    # 2. Evaluate each case
    for case in raw_data:
        cid = case['case_id']
        gold = str(case.get('gold_disease', 'Unknown')).lower()
        valid_symptoms = valid_by_case.get(cid, [])
        
        # Method 1 Check (Direct Mention)
        evidence = [symp for symp in valid_symptoms if gold in symp or symp in gold]
        
        if len(evidence) > 0:
            status = "VERIFIED (Direct diagnostic mention found and validated)"
        else:
            # Method 2 Check (Qwen LLM Evaluation)
            prompt = (f"You are a medical AI. The patient was diagnosed with {gold}. "
                      f"Their mathematically validated clinical symptoms are: {valid_symptoms}. "
                      f"Based purely on medical knowledge, do these symptoms clinically support "
                      f"the diagnosis of {gold}? Answer with only the word YES or NO.")
            try:
                # Send the prompt to Qwen
                response = client.chat_completion(
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=10
                )
                
                answer = response.choices[0].message.content.strip().upper()
                
                if "YES" in answer:
                    status = f"VERIFIED (Qwen LLM successfully matched symptoms to {gold})"
                else:
                    status = f"UNVERIFIED (Qwen LLM determined symptoms do not match {gold})"
                    
            except Exception as e:
                status = f"API Error: {e}"
        
        # FIXED: Pulled this back so it runs regardless of which method was used!
        results.append({"case_id": cid, "gold_disease": gold, "status": status, "evidence": evidence, "valid_findings": valid_symptoms})
            
    return results
# ==========================================
# MAIN EXECUTION
# ==========================================
if __name__ == "__main__":
    file_path = "labeled_cases_top5.jsonl"
    
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
        print(accepted)
        
        print(f"\n AUTO-ACCEPTED ENTITIES ({len(accepted)}):")
        for r in accepted[:10]: 
            status = "VALID" if float(r['probability']) >= 0.85 else "INVALID/IGNORED"
            print(f"  -> [{r['case_id']}] '{r['entity']}' | Decision: {status} (Prob: {r['probability']})")
        if len(accepted) > 10: print("  -> ...and more")
            
        print(f"\n HUMAN REVIEW QUEUE ({len(review)}):")
        for r in review: 
            print(f"  -> [{r['case_id']}] '{r['entity']}' | CONFLICTING SIGNALS (Prob: {r['probability']})")
            print(f"       Details: assertion={r['assertion']}, experiencer={r['experiencer']}")

        print("\n===========================================")
        print("--- RUNNING STEP 6: GOLD DISEASE VERIFICATION ---")
        verification_results = step6_verify_gold_disease(raw_data, accepted)
        for res in verification_results:
            print(f"\n  [{res['case_id']}] Gold Label: {res['gold_disease']}")
            print(f"  Status: {res['status']}")
            print(f"  Supporting Evidence Found: {res['evidence']}")
            
        # --- NEW: Store Step 6 results to a file ---
        output_filename = "final_verification_results.json"
        with open(output_filename, "w") as out_f:
            json.dump(verification_results, out_f, indent=4)
        
        print(f"\n SUCCESS: Verification results saved to {output_filename}")
        print("===========================================\n")

    else:
        print("Snorkel not installed. Skipping Step 4.\n")

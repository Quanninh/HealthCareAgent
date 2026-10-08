import os
import json
import pandas as pd

# Import the Stage 2 logic from the primary pipeline file
from clinical_pipeline import step6_stage2_disease_prediction

print("\n--- STAGE 2: DISEASE PREDICTION (WITH HUMAN REVIEW) ---")

# 1. Load the original raw documents to reconstruct the cases
print("Loading raw patient case data...")
try:
    with open("extracted_cases_top3.jsonl", "r") as f:
        raw_data = [json.loads(line) for line in f]
except FileNotFoundError:
    print("ERROR: extracted_cases_top3.jsonl not found.")

# 2. Load the entities that Snorkel auto-accepted
print("Loading AUTO-ACCEPTED entities...")
try:
    with open("accepted_entities.json", "r") as f:
        accepted_entities = json.load(f)
except FileNotFoundError:
    print("ERROR: accepted_entities.json not found. Did you run clinical_pipeline.py first?")
    
    
# 3. Load the Human Review Queue and filter for expert approvals
print("Loading HUMAN REVIEW queue and checking for expert approvals...")
expert_approved = []
try:
    with open("human_review_queue.json", "r") as f:
        review_queue = json.load(f)
        
    for entity in review_queue:
        if entity.get("expert_decision") == "APPROVED":
            # Artificially set the probability to 1.00 so Stage 2 accepts it
            entity["probability"] = "1.00"
            expert_approved.append(entity)
            
    print(f"  -> Found {len(expert_approved)} entities manually APPROVED by an expert.")
except FileNotFoundError:
    print("  -> No human_review_queue.json found. Proceeding without expert overrides.")
    
# 4. Merge the two lists
final_accepted_list = accepted_entities + expert_approved
print(f"\nTotal Confirmed Entities passed to Stage 2: {len(final_accepted_list)}")

if len(final_accepted_list) == 0:
    print("WARNING: No valid entities found! Predictions will likely all be UNKNOWN.")

# 5. Run the Stage 2 Multiclass Snorkel Model!
print("\nRunning Stage 2 Disease Prediction...")
prediction_results = step6_stage2_disease_prediction(raw_data, final_accepted_list)

for res in prediction_results:
    print(f"\n  [{res['case_id']}] Predicted: {res['predicted_disease']} (Confidence: {res['confidence']})")
    print(f"  Evidence Used: {res['evidence_used']}")
    
# 6. Save final output
output_filename = "stage2_predictions.json"
with open(output_filename, "w") as out_f:
    json.dump(prediction_results, out_f, indent=4)
    
csv_filename = "final_labels.csv"
df_csv = pd.DataFrame(prediction_results)[['case_id', 'predicted_disease']]
df_csv.to_csv(csv_filename, index=False)

print(f"\nSUCCESS: Stage 2 predictions saved to {output_filename} and {csv_filename}")
print("===========================================\n")

"""
stage1_verification.py: MedCAT UMLS Grounding and Snorkel Entity Fact-Checking.

Stage 1 Pipeline:
  1. Load raw extracted cases from JSONL
  2. Ground each entity against UMLS via MedCAT
  3. Flatten entities into a DataFrame
  4. Apply 6 independent juror Labeling Functions via Snorkel
  5. Route entities: auto-accept (p >= threshold) or human review queue

Key Fix: Uses cardinality=2 (binary: INVALID/VALID) instead of the old
cardinality=6 which diluted probability mass across phantom classes.
"""
import os
import sys
import warnings
import logging
from typing import Optional

# Suppress OpenMP duplicate errors, tokenizer deadlocks, and legacy conversion blocks
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
os.environ['TOKENIZERS_PARALLELISM'] = 'false'

# Suppress noisy spaCy compatibility warnings and MedCAT unpickling logs
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', message='.*spaCy.*')
logging.getLogger('medcat').setLevel(logging.ERROR)

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

# Keep legacy conversion enabled even if overridden by external environment
os.environ['MEDCAT_AVOID_LECACY_CONVERSION'] = 'False'

import re
import json
import pandas as pd
import numpy as np

# Compatibility patch for legacy MedCAT v1 model unpickling
try:
    import medcat.config
    if not hasattr(medcat.config, '_DefPartial'):
        class _DefPartial:
            pass
        medcat.config._DefPartial = _DefPartial
    if not hasattr(medcat.config, 'weighted_average'):
        def weighted_average(*args, **kwargs):
            return 0.0
        medcat.config.weighted_average = weighted_average
except Exception:
    pass

try:
    from medcat.cat import CAT
    MEDCAT_AVAILABLE = True
except ImportError:
    MEDCAT_AVAILABLE = False
    print("WARNING: MedCAT not available. Ontology grounding will be skipped.")

try:
    from snorkel.labeling import labeling_function, PandasLFApplier
    from snorkel.labeling.model import LabelModel, MajorityLabelVoter
    SNORKEL_AVAILABLE = True
except ImportError as e:
    SNORKEL_AVAILABLE = False
    print(f"WARNING: Snorkel failed to import: {e}")

from schemas import EntityValidity


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 3: Ontology Grounding via MedCAT
# ═══════════════════════════════════════════════════════════════════════════════

def load_medcat_model(model_path: Optional[str] = None):
    """
    Load the MedCAT UMLS model pack directly from disk.
    Reads from model_path argument if provided, otherwise falls back to MEDCAT_MODEL_PATH from .env.
    """
    if not MEDCAT_AVAILABLE:
        return None
    
    if model_path is None:
        model_path = os.getenv("MEDCAT_MODEL_PATH")

    if not model_path:
        print("WARNING: MEDCAT_MODEL_PATH not configured in .env. Ontology grounding will be skipped.")
        return None

    if not os.path.exists(model_path):
        print(f"WARNING: MedCAT model path not found: {model_path}")
        return None

    print(f"Loading MedCAT UMLS Model from: {model_path}...")
    return CAT.load_model_pack(model_path)


def step3_ontology_grounding(clinical_entities: list, cat) -> list:
    """
    Ground each clinical entity against UMLS using MedCAT.
    Uses the full sentence_context for disambiguation.
    """
    grounded_entities = []

    for entity in clinical_entities:
        text_span = (entity.get("text_span") or "").lower()
        context = entity.get("sentence_context") or text_span

        if cat is not None:
            medcat_results = cat.get_entities(str(context))
            best_match = None

            if medcat_results and len(medcat_results['entities']) > 0:
                for ent_id, ent_data in medcat_results['entities'].items():
                    medcat_word = ent_data['source_value'].lower()
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
            # MedCAT not available — mark as unmapped
            entity["ontology_mapping"] = {
                "umls_cui": None,
                "standard_name": None,
                "status": "Unmapped"
            }

        grounded_entities.append(entity)

    return grounded_entities


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 4: Snorkel Labeling Functions (6 Independent Jurors)
# ═══════════════════════════════════════════════════════════════════════════════

@labeling_function()
def lf_regex_negation(x):
    """
    Juror 1 (Heuristic): Independent regex negation check.
    If the raw text clearly negates the entity, vote INVALID even if
    the LLM assertion says 'affirmed'.
    """
    text_span = str(x.text_span).lower()
    raw_text = str(x.case_presentation).lower()

    escaped_span = re.escape(text_span)
    negation_pattern = re.compile(
        rf"(rules out|denies|no evidence of|not observed|were not observed|no symptoms of|did not complain of)"
        rf"(?:\s+\w+){{0,5}}\s+{escaped_span}"
    )
    if negation_pattern.search(raw_text):
        return EntityValidity.INVALID
    return EntityValidity.ABSTAIN


@labeling_function()
def lf_llm_assertion(x):
    """
    Juror 2 (LLM-derived): Trust the assertion field from the extraction LLM.
    """
    if x.assertion == "affirmed":
        return EntityValidity.VALID
    if x.assertion == "negated":
        return EntityValidity.INVALID
    return EntityValidity.ABSTAIN


@labeling_function()
def lf_experiencer_filter(x):
    """
    Juror 3: If the entity belongs to a family member or other non-patient,
    it is not an active problem for THIS patient.
    """
    if x.experiencer in ["family_member", "other"]:
        return EntityValidity.INVALID
    return EntityValidity.ABSTAIN


@labeling_function()
def lf_temporality_filter(x):
    """
    Juror 4: Historical findings are not current active problems.
    """
    if x.temporality == "historical":
        return EntityValidity.INVALID
    return EntityValidity.ABSTAIN


@labeling_function()
def lf_medcat_validation(x):
    """
    Juror 5 (Ontology): If MedCAT failed to map the entity to UMLS,
    it is likely a hallucination or non-clinical term.
    
    FIX: Returns ABSTAIN (not VALID) on successful mapping to avoid
    biasing the vote count — ontology presence alone is not clinical validity.
    """
    mapping = x.ontology_mapping if isinstance(x.ontology_mapping, dict) else {}
    if mapping.get("status") == "Unmapped" or mapping.get("umls_cui") is None:
        return EntityValidity.INVALID
    return EntityValidity.ABSTAIN


@labeling_function()
def lf_raw_text_check(x):
    """
    Juror 6 (Grounding): Does the text span actually exist in the raw text?
    If not, the LLM hallucinated the entity entirely.
    
    FIX: Returns ABSTAIN (not VALID) when found, to avoid inflating agreement.
    """
    text_span = str(x.text_span).lower()
    raw_text = str(x.case_presentation).lower()
    if text_span not in raw_text:
        return EntityValidity.INVALID
    return EntityValidity.ABSTAIN


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 4: Apply Snorkel Pipeline
# ═══════════════════════════════════════════════════════════════════════════════

STAGE1_LFS = [
    lf_regex_negation,
    lf_llm_assertion,
    lf_experiencer_filter,
    lf_temporality_filter,
    lf_medcat_validation,
    lf_raw_text_check,
]


def step4_apply_snorkel(df_entities: pd.DataFrame):
    """
    Apply all Stage 1 labeling functions and compute validity probabilities.
    
    Uses MajorityLabelVoter with cardinality=2 (binary: INVALID/VALID).
    Returns the annotated DataFrame, label matrix, and LF list.
    """
    applier = PandasLFApplier(lfs=STAGE1_LFS)
    print("Applying Labeling Functions to all entities...")
    L_matrix = applier.apply(df=df_entities)

    print("Computing probabilities with MajorityLabelVoter (cardinality=2)...")
    voter = MajorityLabelVoter(cardinality=2)
    probs = voter.predict_proba(L_matrix)

    # Column 1 = P(VALID)
    df_entities["valid_probability"] = probs[:, 1]

    return df_entities, L_matrix


# ═══════════════════════════════════════════════════════════════════════════════
#  STEP 5: Active Learning Threshold Routing
# ═══════════════════════════════════════════════════════════════════════════════

def step5_route_entities(df_entities: pd.DataFrame, threshold: float = 0.85):
    """
    Route entities into auto-accepted (high confidence) and human review queues.
    """
    auto_accepted = []
    human_review = []

    for _, row in df_entities.iterrows():
        prob = row["valid_probability"]
        ontology = row.get("ontology_mapping", {})
        if not isinstance(ontology, dict):
            ontology = {}

        record = {
            "case_id": row["case_id"],
            "entity": row["text_span"],
            "cui": ontology.get("umls_cui"),
            "standard_name": ontology.get("standard_name"),
            "probability": f"{prob:.2f}",
            "assertion": row["assertion"],
            "experiencer": row["experiencer"],
        }

        if prob >= threshold:
            auto_accepted.append(record)
        else:
            record["expert_decision"] = "PENDING"
            human_review.append(record)

    return auto_accepted, human_review


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN: Full Stage 1 Pipeline
# ═══════════════════════════════════════════════════════════════════════════════

def run_stage1_pipeline(
    input_file: str = "extracted_cases_100per_disease.jsonl",
    threshold: float = 0.85,
    accepted_output: str = "accepted_entities.json",
    review_output: str = "human_review_queue.json",
    model_path: Optional[str] = None,
):
    """
    End-to-end Stage 1 execution:
      1. Load cases
      2. Ground via MedCAT
      3. Flatten + apply Snorkel LFs
      4. Route and save outputs
    
    Returns: raw_data, accepted, review, L_matrix
    """
    # 1. Load case documents
    print(f"\nLoading case documents from {input_file}...")
    raw_data = []
    with open(input_file, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                raw_data.append(json.loads(line))
    print(f"Loaded {len(raw_data)} cases.\n")

    # 2. MedCAT grounding
    cat = load_medcat_model(model_path=model_path)
    print("--- RUNNING STEP 3: ONTOLOGY GROUNDING ---")
    for record in raw_data:
        record["clinical_entities"] = step3_ontology_grounding(
            record["clinical_entities"], cat
        )

    # 3. Flatten entities into DataFrame
    flattened_entities = []
    for record in raw_data:
        for ent in record["clinical_entities"]:
            ent["case_id"] = record["case_id"]
            ent["case_presentation"] = record.get("case_presentation", "")
            flattened_entities.append(ent)

    df_entities = pd.DataFrame(flattened_entities)
    print(f"Flattened data into {len(df_entities)} individual clinical entities.\n")

    # 4. Apply Snorkel Stage 1
    if not SNORKEL_AVAILABLE:
        print("Snorkel not available. Skipping entity verification.")
        return raw_data, [], [], None

    print("--- RUNNING STEP 4: SNORKEL WEAK SUPERVISION ---")
    df_entities, L_matrix = step4_apply_snorkel(df_entities)

    # 5. Route entities
    print("\n--- RUNNING STEP 5: ENTITY ROUTING (Threshold = {:.2f}) ---".format(threshold))
    accepted, review = step5_route_entities(df_entities, threshold=threshold)

    # 6. Save outputs
    with open(accepted_output, "w") as f:
        json.dump(accepted, f, indent=4)
    print(f"Saved {len(accepted)} AUTO-ACCEPTED entities to {accepted_output}.")

    with open(review_output, "w") as f:
        json.dump(review, f, indent=4)
    print(f"Saved {len(review)} entities to {review_output} for expert review.")

    return raw_data, accepted, review, L_matrix


# ═══════════════════════════════════════════════════════════════════════════════
#  CLI Entry Point
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    raw_data, accepted, review, L_matrix = run_stage1_pipeline()

    if L_matrix is not None:
        # Print quick LF diagnostics
        from evaluate_pipeline import print_lf_diagnostics
        print_lf_diagnostics(L_matrix, STAGE1_LFS)

    print("\n" + "=" * 60)
    print("Stage 1 Complete.")
    print(f"  Auto-accepted: {len(accepted)}")
    print(f"  Human review:  {len(review)}")
    print("=" * 60)

    # Flush all output buffers and immediately exit to prevent hanging on background OpenMP/spaCy worker threads
    sys.stdout.flush()
    sys.stderr.flush()
    os._exit(0)

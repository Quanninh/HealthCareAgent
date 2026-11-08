"""
dataset_loader.py

Dataset loader for Clinical LLM Supervised Fine-Tuning (SFT) using QLoRA.
Loads exclusively from the clinical SOAP-structured dataset in:
    sandbox_soap/workspace/core_positive_1500

Option B: Open-Ended Differential Diagnosis
The prompt presents the un-leaked clinical presentation (Subjective and Objective)
WITHOUT providing a candidate target disease hint. The model must perform true differential
diagnosis from clinical findings alone to answer:
    "Which diseases is the patient positive?"

Target Output (Completion):
The output represents the clinical Assessment & Plan:
- Definitive Diagnosis & Pathogen Subtyping
- Confirmatory Microbiological / Diagnostic Evidence
- Differential Diagnoses Ruled Out
- Management Plan & Clinical Outcome
"""

import os
import glob
import json
from typing import Optional, List, Dict, Any

try:
    from datasets import Dataset
except ImportError:
    class Dataset(list):
        @classmethod
        def from_list(cls, data_list):
            return cls(data_list)

        def map(self, function, batched=False, **kwargs):
            if not batched:
                return Dataset([function(item) for item in self])
            else:
                batch = {}
                keys = self[0].keys() if len(self) > 0 else []
                for k in keys:
                    batch[k] = [item[k] for item in self]
                mapped_batch = function(batch)
                res = []
                num_items = len(self)
                for i in range(num_items):
                    item = {k: mapped_batch[k][i] for k in mapped_batch}
                    res.append(item)
                return Dataset(res)


DEFAULT_SOAP_DIR = "sandbox_soap/workspace/core_positive_1500"
DEFAULT_SYSTEM_PROMPT = (
    "You are an expert infectious disease clinician and diagnostic adjudicator. "
    "Evaluate the patient's structured clinical presentation (Subjective and Objective findings) "
    "using rigorous step-by-step reasoning to determine which diseases the patient is positive for, "
    "state the definitive diagnosis, cite confirmatory evidence, rule out differential diagnoses, "
    "and formulate the management plan."
)


def format_soap_presentation(soap_note: Dict[str, Any]) -> str:
    """
    Formats the Subjective (S) and Objective (O) clinical sections into a
    standardized, un-leaked LOINC/EHR presentation text.

    Excludes absent/null fields to keep the presentation natural and concise.
    """
    if not isinstance(soap_note, dict):
        return ""

    subj = soap_note.get("subjective", {}) or {}
    obj = soap_note.get("objective", {}) or {}

    sections = []

    # Subjective section
    subj_lines = []
    if subj.get("chief_complaint"):
        subj_lines.append(f"- Chief Complaint: {str(subj['chief_complaint']).strip()}")
    if subj.get("history_of_present_illness"):
        subj_lines.append(f"- History of Present Illness: {str(subj['history_of_present_illness']).strip()}")
    if subj.get("past_medical_history"):
        subj_lines.append(f"- Past Medical History & Exposures: {str(subj['past_medical_history']).strip()}")
    if subj.get("review_of_systems"):
        subj_lines.append(f"- Review of Systems: {str(subj['review_of_systems']).strip()}")

    if subj_lines:
        sections.append("[SUBJECTIVE]\n" + "\n".join(subj_lines))

    # Objective section
    obj_lines = []
    if obj.get("physical_examination"):
        obj_lines.append(f"- Physical Examination: {str(obj['physical_examination']).strip()}")
    if obj.get("routine_investigations"):
        obj_lines.append(f"- Routine Investigations: {str(obj['routine_investigations']).strip()}")
    if obj.get("advanced_workup"):
        obj_lines.append(f"- Advanced Workup: {str(obj['advanced_workup']).strip()}")

    if obj_lines:
        sections.append("[OBJECTIVE]\n" + "\n".join(obj_lines))

    return "\n\n".join(sections)


def format_positive_diseases_prompt(
    clinical_findings: str,
    question_text: str = "Which diseases is the patient positive?",
    target_disease: Optional[str] = None,
    include_candidate_hint: bool = False
) -> str:
    """
    Constructs the open-ended clinical diagnosis prompt (Option B).
    Presents the un-leaked SOAP clinical findings WITHOUT revealing the candidate disease,
    requiring the model to perform true differential diagnosis.
    """
    hint_line = f"Candidate Target Disease: {target_disease}\n\n" if (include_candidate_hint and target_disease) else ""
    return (
        f"Instruction: Based on the clinical presentation below, answer the question: {question_text}\n"
        f"Provide the definitive diagnosis, confirmatory findings, differential diagnoses ruled out, and management plan.\n\n"
        f"{hint_line}"
        f"Clinical Presentation (SOAP):\n{clinical_findings}\n\n"
        f"Question: {question_text}"
    )


def extract_claims_from_presentation(clinical_presentation: str) -> List[Dict[str, str]]:
    """
    Extracts atomic clinical findings / claims from the formatted SOAP presentation
    for calculating factual evidence grounding and claim coverage.
    """
    claims = []
    if not clinical_presentation:
        return claims
    for line in clinical_presentation.split("\n"):
        line = line.strip()
        if line.startswith("- "):
            content = line[2:].strip()
            if ":" in content:
                content = content.split(":", 1)[1].strip()
            if content:
                claims.append({"text": content, "source": "soap"})
    return claims


def load_soap_record(record: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Parses a single clinical case record from the sandbox_soap dataset.
    Requires 'soap_note' with valid Subjective/Objective presentation
    and 'assessment_and_plan.assessment_and_confirmation'.

    Returns None if unpopulated or missing required clinical sections.
    """
    soap = record.get("soap_note")
    if not isinstance(soap, dict):
        return None

    ap = soap.get("assessment_and_plan", {}).get("assessment_and_confirmation")
    if ap is None or not str(ap).strip():
        # Unpopulated template
        return None

    clinical_presentation = format_soap_presentation(soap)
    if not clinical_presentation.strip():
        # No subjective or objective data
        return None

    target_disease = record.get("target_disease", "Infectious Disease")
    pair_id = record.get("pair_id", record.get("case_id", ""))
    target_output = str(ap).strip()

    return {
        "pair_id": pair_id,
        "case_id": record.get("case_id", ""),
        "target_disease": target_disease,
        "clinical_presentation": clinical_presentation,
        "target_output": target_output,
        "raw_case_text": record.get("raw_case_text", ""),
        "soap_note": soap,
        "claims": extract_claims_from_presentation(clinical_presentation)
    }


def load_dataset_from_path(
    data_path: str = DEFAULT_SOAP_DIR,
    format_type: str = "chatml",
    system_prompt: Optional[str] = None,
    question_text: str = "Which diseases is the patient positive?",
    include_candidate_hint: bool = False,
    max_samples: Optional[int] = None
) -> Dataset:
    """
    Loads clinical SOAP cases exclusively from the sandbox_soap workspace.
    Constructs open-ended prompts (without candidate disease hints by default).

    Args:
        data_path: Path to dataset directory or JSON file.
        format_type: 'chatml' for conversational models or 'alpaca' for instruction models.
        system_prompt: Custom system prompt (defaults to DEFAULT_SYSTEM_PROMPT).
        question_text: The evaluation question to answer.
        include_candidate_hint: Whether to include the candidate disease hint in prompt (default False for Option B).
        max_samples: Optional limit on number of samples.

    Returns:
        Hugging Face Dataset.
    """
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Dataset path not found at: {data_path}")

    if system_prompt is None:
        system_prompt = DEFAULT_SYSTEM_PROMPT

    raw_records: List[Dict[str, Any]] = []

    if os.path.isdir(data_path):
        json_pattern = os.path.join(data_path, "**", "*.json")
        all_json_files = sorted(glob.glob(json_pattern, recursive=True))
        case_files = [f for f in all_json_files if not os.path.basename(f).startswith("manifest")]

        for fpath in case_files:
            try:
                with open(fpath, "r", encoding="utf-8") as fp:
                    raw_records.append(json.load(fp))
            except Exception as e:
                print(f"[WARNING] Skipping unparseable file {fpath}: {e}")

    elif data_path.endswith(".json"):
        with open(data_path, "r", encoding="utf-8") as f:
            raw_records.append(json.load(f))
    elif data_path.endswith(".jsonl"):
        with open(data_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    try:
                        raw_records.append(json.loads(line))
                    except Exception:
                        pass
    else:
        raise ValueError(f"Unsupported data source type for path: {data_path}")

    samples: List[Dict[str, Any]] = []
    skipped_unpopulated = 0

    for rec in raw_records:
        parsed = load_soap_record(rec)
        if parsed is None:
            skipped_unpopulated += 1
            continue

        target_disease = parsed["target_disease"]
        user_prompt = format_positive_diseases_prompt(
            clinical_findings=parsed["clinical_presentation"],
            question_text=question_text,
            target_disease=target_disease,
            include_candidate_hint=include_candidate_hint
        )
        target_output = parsed["target_output"]

        if format_type == "chatml":
            samples.append({
                "pair_id": parsed["pair_id"],
                "case_id": parsed["case_id"],
                "target_disease": target_disease,
                "dataset_label": "POSITIVE",
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                    {"role": "assistant", "content": target_output}
                ]
            })
        elif format_type == "alpaca":
            hint_str = f"Candidate Target Disease: {target_disease}\n\n" if include_candidate_hint else ""
            samples.append({
                "pair_id": parsed["pair_id"],
                "case_id": parsed["case_id"],
                "target_disease": target_disease,
                "dataset_label": "POSITIVE",
                "instruction": f"Answer the question: {question_text} Based on the clinical presentation, identify which disease(s) the patient is positive for.",
                "input": f"{hint_str}Clinical Presentation (SOAP):\n{parsed['clinical_presentation']}",
                "output": target_output
            })
        else:
            raise ValueError(f"Unknown format_type: {format_type}. Must be 'chatml' or 'alpaca'.")

        if max_samples is not None and len(samples) >= max_samples:
            break

    print(
        f"Successfully loaded {len(samples)} clinical SOAP cases from '{data_path}' "
        f"in '{format_type}' format (Open-ended Option B, Skipped {skipped_unpopulated} unpopulated templates)."
    )
    return Dataset.from_list(samples)


# Aliases
load_clinical_soap_dataset = load_dataset_from_path
load_gt_reasoning_dataset = load_dataset_from_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test SOAP dataset loader")
    parser.add_argument("--data_path", default=DEFAULT_SOAP_DIR, help="Path to sandbox_soap directory")
    parser.add_argument("--format", default="chatml", choices=["chatml", "alpaca"])
    parser.add_argument("--limit", type=int, default=2)
    args = parser.parse_args()

    ds = load_clinical_soap_dataset(data_path=args.data_path, format_type=args.format, max_samples=args.limit)
    print(f"\nLoaded {len(ds)} samples.")
    print("\n" + "=" * 60)
    print("SAMPLE 1 PREVIEW (OPTION B: ZERO CANDIDATE HINTS)")
    print("=" * 60)
    if args.format == "chatml":
        for m in ds[0]["messages"]:
            print(f"[{m['role'].upper()}]:\n{m['content']}\n")
    else:
        print(f"Instruction:\n{ds[0]['instruction']}\n\nInput:\n{ds[0]['input']}\n\nOutput:\n{ds[0]['output']}")

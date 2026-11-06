"""
dataset_loader.py

Dataset loader for Clinical LLM Supervised Fine-Tuning (SFT) using QLoRA.
Loads the offline-distilled clinical reasoning dataset (ground_truth_reasoning_all.jsonl),
preparing samples in ChatML and Alpaca formats, specifically instructing the model
to answer: "Which diseases is the patient positive?"
"""

import os
import glob
import json
from typing import Optional, List, Dict, Any, Tuple

try:
    from datasets import Dataset
except ImportError:
    # Graceful fallback when HuggingFace datasets is not yet installed
    class Dataset(list):
        @classmethod
        def from_list(cls, data_list):
            inst = cls(data_list)
            return inst

        def map(self, function, batched=False, **kwargs):
            if not batched:
                return Dataset([function(item) for item in self])
            else:
                # Simple batched approximation
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


def format_positive_diseases_prompt(
    target_disease: str,
    bullet_findings: str,
    question_text: str = "Which diseases is the patient positive?"
) -> str:
    """
    Constructs the prompt instructing the model to answer which diseases the patient is positive for,
    evaluating candidate target disease using step-by-step reasoning.
    """
    return (
        f"Instruction: Based on the clinical findings below, answer the question: {question_text}\n"
        f"State the diagnosis, provide your step-by-step clinical reasoning, and give your final diagnostic determination.\n\n"
        f"Candidate Target Disease: {target_disease}\n\n"
        f"Clinical Findings:\n{bullet_findings}\n\n"
        f"Question: {question_text}"
    )


def load_gt_reasoning_dataset(
    gt_file: str = "gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl",
    format_type: str = "chatml",
    system_prompt: Optional[str] = None,
    question_text: str = "Which diseases is the patient positive?",
    max_samples: Optional[int] = None
) -> Dataset:
    """
    Directly loads ground_truth_reasoning_all.jsonl (5,308 cases: POSITIVE & OUT_OF_SCOPE)
    without requiring external payload zips or raw narrative files.

    The prompt is constructed from `target_disease` and atomic `claims`,
    framed around the user question: "Which diseases is the patient positive?",
    and the completion is `ground_truth_reasoning`.

    Args:
        gt_file: Path to ground_truth_reasoning_all.jsonl.
        format_type: 'chatml' for conversational models or 'alpaca' for instruction models.
        system_prompt: Optional custom system prompt.
        question_text: The evaluation question to answer (default: 'Which diseases is the patient positive?').
        max_samples: Optional limit on the number of samples to load (useful for testing).

    Returns:
        Hugging Face Dataset.
    """
    if not os.path.exists(gt_file):
        raise FileNotFoundError(f"Dataset file not found at: {gt_file}")

    if system_prompt is None:
        system_prompt = (
            "You are an expert infectious disease clinician and diagnostic adjudicator. "
            "Evaluate patient clinical findings using structured step-by-step reasoning "
            "to determine which diseases the patient is positive for."
        )

    samples: List[Dict[str, Any]] = []

    with open(gt_file, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            rec = json.loads(line)
            claims = rec.get("claims", [])
            if not claims:
                continue

            target_disease = rec.get("target_disease", "Infectious Disease")
            bullet_findings = "\n".join("- " + c["text"] for c in claims)

            user_prompt = format_positive_diseases_prompt(
                target_disease=target_disease,
                bullet_findings=bullet_findings,
                question_text=question_text
            )
            target_output = rec.get("ground_truth_reasoning", "").strip()

            if format_type == "chatml":
                samples.append({
                    "pair_id": rec.get("pair_id", ""),
                    "target_disease": target_disease,
                    "dataset_label": rec.get("dataset_label", ""),
                    "messages": [
                        {
                            "role": "system",
                            "content": system_prompt
                        },
                        {"role": "user", "content": user_prompt},
                        {"role": "assistant", "content": target_output}
                    ]
                })
            elif format_type == "alpaca":
                samples.append({
                    "pair_id": rec.get("pair_id", ""),
                    "target_disease": target_disease,
                    "dataset_label": rec.get("dataset_label", ""),
                    "instruction": f"Answer the question: {question_text} Evaluate the clinical findings for {target_disease}.",
                    "input": f"Candidate Target Disease: {target_disease}\n\nClinical Findings:\n{bullet_findings}",
                    "output": target_output
                })
            else:
                raise ValueError(f"Unknown format_type: {format_type}. Must be 'chatml' or 'alpaca'.")

            if max_samples is not None and len(samples) >= max_samples:
                break

    print(f"Successfully loaded {len(samples)} records from {gt_file} in '{format_type}' format.")
    return Dataset.from_list(samples)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test dataset loader")
    parser.add_argument("--gt_file", default="gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl")
    parser.add_argument("--format", default="chatml", choices=["chatml", "alpaca"])
    parser.add_argument("--limit", type=int, default=3)
    args = parser.parse_args()

    ds = load_gt_reasoning_dataset(gt_file=args.gt_file, format_type=args.format, max_samples=args.limit)
    print(f"\nLoaded {len(ds)} samples.")
    print("\n--- SAMPLE 1 ---")
    if args.format == "chatml":
        for m in ds[0]["messages"]:
            print(f"[{m['role'].upper()}]:\n{m['content']}\n")
    else:
        print(f"Instruction: {ds[0]['instruction']}\nInput: {ds[0]['input']}\nOutput: {ds[0]['output']}")

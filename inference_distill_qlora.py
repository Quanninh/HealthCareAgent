"""
inference_distill_qlora.py

Inference script for the fine-tuned Clinical LLM (Student Base + QLoRA Adapter).
Evaluates patient cases with the distilled reasoning of the 70B Teacher model
specifically answering: "Which diseases is the patient positive?"
"""

import os
import sys
import json
import argparse

from dataset_loader import format_positive_diseases_prompt

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import PeftModel
    HF_PACKAGES_AVAILABLE = True
except ImportError as e:
    HF_PACKAGES_AVAILABLE = False
    _IMPORT_ERROR_MSG = str(e)


def build_chat_prompt(tokenizer, candidate_disease: str, findings: str, question_text: str = "Which diseases is the patient positive?") -> str:
    """
    Builds the model prompt formatted according to the model's native chat template.
    """
    user_prompt = format_positive_diseases_prompt(
        target_disease=candidate_disease,
        bullet_findings=findings,
        question_text=question_text
    )

    messages = [
        {
            "role": "system",
            "content": (
                "You are an expert infectious disease clinician and diagnostic adjudicator. "
                "Evaluate patient clinical findings using structured step-by-step reasoning "
                "to determine which diseases the patient is positive for."
            )
        },
        {"role": "user", "content": user_prompt}
    ]

    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def run_inference(
    model,
    tokenizer,
    candidate_disease: str,
    findings: str,
    question_text: str = "Which diseases is the patient positive?",
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    top_p: float = 0.9
) -> str:
    """
    Runs generation for a clinical case presentation.
    """
    prompt_text = build_chat_prompt(tokenizer, candidate_disease, findings, question_text)
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=(temperature > 0.0),
            pad_token_id=tokenizer.eos_token_id
        )

    # Slice out prompt tokens to isolate generated response
    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    return response


def main():
    parser = argparse.ArgumentParser(
        description="Inference evaluation for Distilled QLoRA Clinical Model"
    )
    parser.add_argument(
        "--adapter_path",
        type=str,
        default="./qlora_distilled_output/final_adapter",
        help="Path to the saved LoRA adapter directory"
    )
    parser.add_argument(
        "--base_model",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Base student model Hugging Face ID or local path"
    )
    parser.add_argument(
        "--question_text",
        type=str,
        default="Which diseases is the patient positive?",
        help="Question to ask the model"
    )
    parser.add_argument(
        "--disease",
        type=str,
        default="Brucellosis",
        help="Candidate target disease to evaluate"
    )
    parser.add_argument(
        "--findings",
        type=str,
        default=None,
        help="Bullet list or description of clinical findings"
    )
    parser.add_argument(
        "--sample_index",
        type=int,
        default=None,
        help="Load a specific case from ground_truth_reasoning_all.jsonl"
    )
    parser.add_argument(
        "--gt_file",
        type=str,
        default="gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl",
        help="Path to ground truth dataset"
    )
    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=512,
        help="Maximum generation length"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Sampling temperature (lower = more deterministic reasoning)"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Print the formatted prompt and findings without loading the model"
    )

    args = parser.parse_args()

    # Resolve clinical case findings
    candidate_disease = args.disease
    findings = args.findings
    expected_gt = None

    if args.sample_index is not None and os.path.exists(args.gt_file):
        print(f"Loading sample #{args.sample_index} from {args.gt_file}...")
        with open(args.gt_file, "r", encoding="utf-8") as f:
            for idx, line in enumerate(f):
                if idx == args.sample_index:
                    rec = json.loads(line)
                    candidate_disease = rec.get("target_disease", candidate_disease)
                    claims = rec.get("claims", [])
                    findings = "\n".join("- " + c["text"] for c in claims)
                    expected_gt = rec.get("ground_truth_reasoning", "")
                    break

    if findings is None:
        # Default representative clinical test case
        candidate_disease = "Brucellosis"
        findings = (
            "- Neurological presentation with headache and fever is accompanied by identification "
            "of Brucella abortus in cerebrospinal fluid via metagenomic next-generation sequencing (mNGS).\n"
            "- Systemic brucellosis is serologically confirmed by a positive serum Rose Bengal plate "
            "agglutination test and a positive standard tube agglutination test (SAT) meeting the diagnostic threshold (>= 1:160)."
        )

    if args.dry_run:
        prompt_text = format_positive_diseases_prompt(
            target_disease=candidate_disease,
            bullet_findings=findings,
            question_text=args.question_text
        )
        print("=" * 70)
        print(" INFERENCE DRY-RUN PROMPT PREVIEW")
        print("=" * 70)
        print(f"Candidate Disease: {candidate_disease}")
        print(f"Question:          {args.question_text}\n")
        print(f"--- Formatted Prompt ---\n{prompt_text}")
        if expected_gt:
            print(f"\n--- Ground Truth Reasoning ---\n{expected_gt}")
        print("\n[SUCCESS] Inference prompt validated.")
        return

    if not HF_PACKAGES_AVAILABLE:
        print(f"[ERROR] Required packages not found: {_IMPORT_ERROR_MSG}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)

    print("=" * 70)
    print(" Clinical Model Inference: Question & Reasoning Evaluation")
    print(f" Target Question: {args.question_text}")
    print(f" Candidate Disease: {candidate_disease}")
    print(f" Adapter Path: {args.adapter_path}")
    print("=" * 70)

    print("\n[1/3] Loading Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.adapter_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    print("\n[2/3] Loading Base Model in 4-bit NF4...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    base_model = AutoModelForCausalLM.from_pretrained(
        args.base_model,
        quantization_config=bnb_config,
        device_map="auto"
    )

    print("\n[3/3] Attaching Distilled LoRA Adapter...")
    model = PeftModel.from_pretrained(base_model, args.adapter_path)
    model.eval()

    print("\nEvaluating Patient Case Presentation...")
    print(f"\n[CLINICAL FINDINGS]:\n{findings}")

    result = run_inference(
        model=model,
        tokenizer=tokenizer,
        candidate_disease=candidate_disease,
        findings=findings,
        question_text=args.question_text,
        max_new_tokens=args.max_new_tokens,
        temperature=args.temperature
    )

    print("\n" + "=" * 70)
    print(" MODEL RESPONSE (Step-by-Step Reasoning & Determination):")
    print("=" * 70)
    print(result)

    if expected_gt:
        print("\n" + "=" * 70)
        print(" GROUND TRUTH ADJUDICATION REFERENCE:")
        print("=" * 70)
        print(expected_gt)


if __name__ == "__main__":
    main()

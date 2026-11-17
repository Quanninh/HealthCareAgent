"""
inference_qlora.py

Inference script for the fine-tuned Clinical LLM (Base Model + QLoRA Adapter).
Evaluates patient cases with the structured SOAP clinical presentation,
specifically answering: "Which diseases is the patient positive?"
"""

import os
import sys
import json
import glob
import argparse
from typing import Optional, Dict, Any

# Ensure repository root is on sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from finetune.dataset_loader import (
    format_positive_diseases_prompt,
    format_soap_presentation,
    load_soap_record,
    DEFAULT_SOAP_DIR,
    DEFAULT_SYSTEM_PROMPT
)

try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
    from peft import PeftModel
    HF_PACKAGES_AVAILABLE = True
except ImportError as e:
    HF_PACKAGES_AVAILABLE = False
    _IMPORT_ERROR_MSG = str(e)


def build_chat_prompt(
    tokenizer,
    findings: str,
    candidate_disease: Optional[str] = None,
    question_text: str = "Which diseases is the patient positive?",
    system_prompt: str = DEFAULT_SYSTEM_PROMPT,
    include_candidate_hint: bool = False
) -> str:
    """
    Builds the model prompt formatted according to the model's native chat template.
    In Option B (Open Differential Diagnosis), include_candidate_hint=False so no candidate disease
    is revealed in the input prompt.
    """
    user_prompt = format_positive_diseases_prompt(
        clinical_findings=findings,
        question_text=question_text,
        target_disease=candidate_disease,
        include_candidate_hint=include_candidate_hint
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ]

    return tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)


def run_inference(
    model,
    tokenizer,
    findings: str,
    candidate_disease: Optional[str] = None,
    question_text: str = "Which diseases is the patient positive?",
    max_new_tokens: int = 512,
    temperature: float = 0.2,
    top_p: float = 0.9,
    include_candidate_hint: bool = False
) -> str:
    """
    Runs generation for a clinical case presentation.
    """
    prompt_text = build_chat_prompt(
        tokenizer=tokenizer,
        findings=findings,
        candidate_disease=candidate_disease,
        question_text=question_text,
        include_candidate_hint=include_candidate_hint
    )
    inputs = tokenizer(prompt_text, return_tensors="pt").to(model.device)

    if hasattr(model, "config"):
        model.config.use_cache = True
    if hasattr(model, "generation_config") and model.generation_config is not None:
        model.generation_config.max_length = None

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=(temperature > 0.0),
            pad_token_id=tokenizer.eos_token_id,
            use_cache=True
        )

    # Slice out prompt tokens to isolate generated response
    generated_tokens = outputs[0][inputs["input_ids"].shape[1]:]
    response = tokenizer.decode(generated_tokens, skip_special_tokens=True).strip()
    return response


def main():
    default_adapter = (
        "./qlora_sft_output/final_adapter"
        if os.path.exists("./qlora_sft_output/final_adapter")
        else (
            "./qlora_distilled_output/final_adapter"
            if os.path.exists("./qlora_distilled_output/final_adapter")
            else "./qlora_sft_output/final_adapter"
        )
    )

    parser = argparse.ArgumentParser(
        description="Inference evaluation for QLoRA Supervised Fine-Tuned Clinical Model"
    )
    parser.add_argument(
        "--adapter_path",
        type=str,
        default=default_adapter,
        help="Path to the saved LoRA adapter directory"
    )
    parser.add_argument(
        "--base_model",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Base model Hugging Face ID or local path"
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
        help="Custom clinical presentation (SOAP format or findings description)"
    )
    parser.add_argument(
        "--case_file",
        type=str,
        default=None,
        help="Path to a single JSON case file (e.g. sandbox_soap/workspace/core_positive_1500/Brucellosis/PMC10164848_01__Brucellosis.json)"
    )
    parser.add_argument(
        "--sample_index",
        type=int,
        default=None,
        help="Load sample by index from dataset"
    )
    parser.add_argument(
        "--dataset_path",
        type=str,
        default=DEFAULT_SOAP_DIR,
        help="Path to SOAP workspace directory or JSONL dataset"
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

    candidate_disease = args.disease
    findings = args.findings
    expected_gt = None

    # Load from specific case file if provided
    if args.case_file and os.path.exists(args.case_file):
        print(f"Loading clinical case from: {args.case_file}")
        with open(args.case_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        parsed = load_soap_record(data)
        if parsed:
            candidate_disease = parsed["target_disease"]
            findings = parsed["clinical_presentation"]
            expected_gt = parsed["target_output"]

    # Load from sample index in dataset
    elif args.sample_index is not None and os.path.exists(args.dataset_path):
        if os.path.isdir(args.dataset_path):
            case_files = sorted(glob.glob(os.path.join(args.dataset_path, "**", "*.json"), recursive=True))
            case_files = [f for f in case_files if not os.path.basename(f).startswith("manifest")]
            if args.sample_index < len(case_files):
                target_f = case_files[args.sample_index]
                print(f"Loading sample #{args.sample_index} from: {target_f}")
                with open(target_f, "r", encoding="utf-8") as f:
                    data = json.load(f)
                parsed = load_soap_record(data)
                if parsed:
                    candidate_disease = parsed["target_disease"]
                    findings = parsed["clinical_presentation"]
                    expected_gt = parsed["target_output"]
        elif args.dataset_path.endswith(".jsonl"):
            with open(args.dataset_path, "r", encoding="utf-8") as f:
                for idx, line in enumerate(f):
                    if idx == args.sample_index:
                        rec = json.loads(line)
                        parsed = load_soap_record(rec)
                        if parsed:
                            candidate_disease = parsed["target_disease"]
                            findings = parsed["clinical_presentation"]
                            expected_gt = parsed["target_output"]
                        break

    # Default representative clinical test case if none provided
    if findings is None:
        candidate_disease = "Brucellosis"
        findings = (
            "[SUBJECTIVE]\n"
            "- Chief Complaint: A 42-year-old male farmer presenting with 3-week undulant fever and joint pain.\n"
            "- History of Present Illness: Patient developed evening fevers, profuse night sweats, and severe bilateral hip and knee arthralgias.\n"
            "- Past Medical History & Exposures: Consumed unpasteurized goat milk and assisted in livestock calving one month prior.\n"
            "- Review of Systems: Anorexia, 4 kg weight loss, backache.\n\n"
            "[OBJECTIVE]\n"
            "- Physical Examination: Temperature 38.8 C, pulse 94 bpm, BP 120/75 mmHg. Palpable splenomegaly; tenderness over lumbar spine.\n"
            "- Routine Investigations: WBC 4.2 x 10^9/L, Hemoglobin 10.4 g/dL, Platelets 135 x 10^9/L, ESR 48 mm/h, CRP 62 mg/L. AST 78 U/L, ALT 85 U/L."
        )

    if args.dry_run:
        prompt_text = format_positive_diseases_prompt(
            clinical_findings=findings,
            question_text=args.question_text,
            target_disease=candidate_disease,
            include_candidate_hint=False
        )
        print("=" * 70)
        print(" INFERENCE DRY-RUN PROMPT PREVIEW (OPTION B: ZERO CANDIDATE HINT)")
        print("=" * 70)
        print(f"Ground Truth Label: {candidate_disease}")
        print(f"Question:           {args.question_text}\n")
        print(f"--- Formatted Input Prompt to Model ---\n{prompt_text}")
        if expected_gt:
            print(f"\n--- Ground Truth Assessment & Plan ---\n{expected_gt}")
        print("\n[SUCCESS] Inference prompt validated without candidate hint.")
        return

    if not HF_PACKAGES_AVAILABLE:
        print(f"[ERROR] Required packages not found: {_IMPORT_ERROR_MSG}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)

    print("=" * 70)
    print(" Clinical Model Inference: Question & Reasoning Evaluation")
    print(f" Target Question:  {args.question_text}")
    print(f" Candidate Disease:{candidate_disease}")
    print(f" Adapter Path:     {args.adapter_path}")
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

    print("\n[3/3] Attaching QLoRA Adapter...")
    model = PeftModel.from_pretrained(base_model, args.adapter_path)
    model.eval()

    print("\nEvaluating Patient Case Presentation...")
    print(f"\n[CLINICAL PRESENTATION]:\n{findings}")

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
    print(" MODEL RESPONSE (Assessment & Plan):")
    print("=" * 70)
    print(result)

    if expected_gt:
        print("\n" + "=" * 70)
        print(" GROUND TRUTH ASSESSMENT REFERENCE:")
        print("=" * 70)
        print(expected_gt)


if __name__ == "__main__":
    main()

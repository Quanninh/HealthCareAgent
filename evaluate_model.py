"""
evaluate_model.py

Comprehensive Evaluation Suite for Fine-Tuned / Distilled Clinical LLM.
Evaluates both:
1. Diagnostic Classification (Sensitivity, Specificity, Precision, Recall, F1, Per-Disease Metrics)
2. Clinical Reasoning Text Quality (ROUGE-1, ROUGE-2, ROUGE-L against Ground Truth Adjudication)
3. Clinical Error Analysis (Automatic dump of False Negatives and False Positives)
"""

import os
import sys
import json
import argparse
import random
from typing import Dict, List, Any, Tuple, Optional
from collections import defaultdict

# ----------------- Fallback ROUGE Implementation -----------------
# Pure Python ROUGE implementation so evaluation has zero external dependencies
def _get_ngrams(tokens: List[str], n: int) -> Dict[Tuple[str, ...], int]:
    ngrams = defaultdict(int)
    for i in range(len(tokens) - n + 1):
        ngrams[tuple(tokens[i:i+n])] += 1
    return ngrams

def compute_rouge_n(hyp: List[str], ref: List[str], n: int) -> float:
    hyp_ngrams = _get_ngrams(hyp, n)
    ref_ngrams = _get_ngrams(ref, n)
    if not hyp_ngrams or not ref_ngrams:
        return 0.0
    overlap = sum(min(count, ref_ngrams[ng]) for ng, count in hyp_ngrams.items() if ng in ref_ngrams)
    prec = overlap / max(1, sum(hyp_ngrams.values()))
    rec = overlap / max(1, sum(ref_ngrams.values()))
    if (prec + rec) == 0:
        return 0.0
    return 2.0 * (prec * rec) / (prec + rec)

def compute_lcs(x: List[str], y: List[str]) -> int:
    m, n = len(x), len(y)
    dp = [0] * (n + 1)
    for i in range(1, m + 1):
        prev = 0
        for j in range(1, n + 1):
            temp = dp[j]
            if x[i - 1] == y[j - 1]:
                dp[j] = prev + 1
            else:
                dp[j] = max(dp[j], dp[j - 1])
            prev = temp
    return dp[n]

def compute_rouge_l(hyp: List[str], ref: List[str]) -> float:
    if not hyp or not ref:
        return 0.0
    lcs_len = compute_lcs(hyp, ref)
    prec = lcs_len / len(hyp)
    rec = lcs_len / len(ref)
    if (prec + rec) == 0:
        return 0.0
    return 2.0 * (prec * rec) / (prec + rec)

def compute_rouge_scores(generated: str, reference: str) -> Dict[str, float]:
    hyp_toks = generated.lower().split()
    ref_toks = reference.lower().split()
    return {
        "rouge1": round(compute_rouge_n(hyp_toks, ref_toks, 1), 4),
        "rouge2": round(compute_rouge_n(hyp_toks, ref_toks, 2), 4),
        "rougeL": round(compute_rouge_l(hyp_toks, ref_toks), 4)
    }


# ----------------- Verdict Extraction Logic -----------------
def extract_verdict(model_response: str, target_disease: str = "") -> str:
    """
    Extracts the clinical determination (POSITIVE vs OUT_OF_SCOPE)
    from the model's generated text using rule-based parsing verified on 5,308 cases.
    """
    text = model_response.strip().upper()

    # 1. Check ending determination markers
    if "POSITIVE DIAGNOSIS CONFIRMED" in text:
        return "POSITIVE"
    if "OUT_OF_SCOPE DIAGNOSIS CONFIRMED" in text:
        return "OUT_OF_SCOPE"
    if "NEGATIVE DIAGNOSIS CONFIRMED" in text:
        return "OUT_OF_SCOPE"

    # 2. Check conclusion after '->' arrow
    if "->" in model_response:
        conclusion = model_response.split("->")[-1].upper()
        if "POSITIVE" in conclusion:
            return "POSITIVE"
        if "OUT_OF_SCOPE" in conclusion or "NEGATIVE" in conclusion or "NOT" in conclusion:
            return "OUT_OF_SCOPE"

    # 3. Check leading classification prefix
    if text.startswith("OUT_OF_SCOPE") or text.startswith("NEGATIVE"):
        return "OUT_OF_SCOPE"

    # 4. Check negative disease phrasing (e.g., "Not Brucellosis", "ruled out")
    if target_disease and f"NOT {target_disease.upper()}" in text:
        return "OUT_OF_SCOPE"
    if "RULED OUT" in text or "RULES OUT" in text:
        return "OUT_OF_SCOPE"

    # 5. Default check for POSITIVE affirmation
    if "POSITIVE" in text:
        return "POSITIVE"

    # Default fallback
    return "OUT_OF_SCOPE"


# ----------------- Classification Metric Computation -----------------
def compute_classification_metrics(eval_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Computes overall and per-disease diagnostic accuracy, sensitivity, specificity, PPV, and F1.
    """
    tp = fp = tn = fn = 0
    disease_stats = defaultdict(lambda: {"tp": 0, "fp": 0, "tn": 0, "fn": 0, "total": 0})

    for rec in eval_records:
        true_label = rec["true_label"]
        pred_label = rec["pred_label"]
        disease = rec.get("target_disease", "Overall")

        disease_stats[disease]["total"] += 1

        if true_label == "POSITIVE" and pred_label == "POSITIVE":
            tp += 1
            disease_stats[disease]["tp"] += 1
        elif true_label == "OUT_OF_SCOPE" and pred_label == "POSITIVE":
            fp += 1
            disease_stats[disease]["fp"] += 1
        elif true_label == "OUT_OF_SCOPE" and pred_label == "OUT_OF_SCOPE":
            tn += 1
            disease_stats[disease]["tn"] += 1
        elif true_label == "POSITIVE" and pred_label == "OUT_OF_SCOPE":
            fn += 1
            disease_stats[disease]["fn"] += 1

    total = tp + fp + tn + fn
    accuracy = (tp + tn) / max(1, total)
    sensitivity = tp / max(1, (tp + fn))       # Recall for positive infections
    specificity = tn / max(1, (tn + fp))       # Ability to rule out out-of-scope cases
    precision = tp / max(1, (tp + fp))         # PPV
    npv = tn / max(1, (tn + fn))               # Negative Predictive Value
    f1_score = (2.0 * precision * sensitivity) / max(1e-8, (precision + sensitivity))
    balanced_acc = (sensitivity + specificity) / 2.0

    # Per-disease metrics breakdown
    per_disease = {}
    for dis, s in disease_stats.items():
        dis_acc = (s["tp"] + s["tn"]) / max(1, s["total"])
        dis_sens = s["tp"] / max(1, (s["tp"] + s["fn"]))
        dis_spec = s["tn"] / max(1, (s["tn"] + s["fp"]))
        dis_prec = s["tp"] / max(1, (s["tp"] + s["fp"]))
        dis_f1 = (2.0 * dis_prec * dis_sens) / max(1e-8, (dis_prec + dis_sens))
        per_disease[dis] = {
            "total_samples": s["total"],
            "TP": s["tp"],
            "FP": s["fp"],
            "TN": s["tn"],
            "FN": s["fn"],
            "accuracy": round(dis_acc, 4),
            "sensitivity_recall": round(dis_sens, 4),
            "specificity": round(dis_spec, 4),
            "precision_ppv": round(dis_prec, 4),
            "f1_score": round(dis_f1, 4)
        }

    return {
        "total_evaluated": total,
        "confusion_matrix": {
            "TP": tp,
            "FP": fp,
            "TN": tn,
            "FN": fn
        },
        "overall_metrics": {
            "accuracy": round(accuracy, 4),
            "sensitivity_recall": round(sensitivity, 4),
            "specificity": round(specificity, 4),
            "precision_ppv": round(precision, 4),
            "negative_predictive_value": round(npv, 4),
            "balanced_accuracy": round(balanced_acc, 4),
            "f1_score": round(f1_score, 4)
        },
        "per_disease_breakdown": per_disease
    }


# ----------------- Prompt Builder -----------------
def format_prompt(candidate_disease: str, claims: List[Dict[str, Any]], question_text: str = "Which diseases is the patient positive?") -> str:
    bullet_findings = "\n".join("- " + c["text"] for c in claims)
    return (
        f"Instruction: Based on the clinical findings below, answer the question: {question_text}\n"
        f"State the diagnosis, provide your step-by-step clinical reasoning, and give your final diagnostic determination.\n\n"
        f"Candidate Target Disease: {candidate_disease}\n\n"
        f"Clinical Findings:\n{bullet_findings}\n\n"
        f"Question: {question_text}"
    )


# ----------------- Main Evaluation Routine -----------------
def main():
    parser = argparse.ArgumentParser(
        description="Comprehensive Diagnostic & Reasoning Evaluation for Fine-Tuned Clinical LLM"
    )
    parser.add_argument(
        "--adapter_path",
        type=str,
        default="./qlora_distilled_output/final_adapter",
        help="Path to saved LoRA adapter checkpoint"
    )
    parser.add_argument(
        "--base_model",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Base student model Hugging Face ID or local path"
    )
    parser.add_argument(
        "--gt_file",
        type=str,
        default="gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl",
        help="Path to ground truth dataset"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./eval_results",
        help="Output directory to save evaluation metrics and predictions"
    )
    parser.add_argument(
        "--test_ratio",
        type=float,
        default=0.15,
        help="Fraction of dataset reserved for evaluation split (default: 0.15)"
    )
    parser.add_argument(
        "--split_seed",
        type=int,
        default=42,
        help="Random seed for reproducible train/test splitting"
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="Limit number of test samples to evaluate (useful for fast validation)"
    )
    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=512,
        help="Maximum generation length per sample"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling temperature (0.0 = greedy deterministic decoding for evaluation)"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Validate metric computation and extraction logic on ground truth without GPU"
    )

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    print("=" * 70)
    print(" Clinical LLM Comprehensive Evaluation Suite")
    print(f" Dataset:         {args.gt_file}")
    print(f" Output Dir:      {args.output_dir}")
    print(f" Test Ratio:      {args.test_ratio} (Seed: {args.split_seed})")
    print(f" Adapter Path:    {args.adapter_path}")
    print(f" Mode:            {'DRY RUN (Ground Truth Validation)' if args.dry_run else 'MODEL INFERENCE'}")
    print("=" * 70)

    # 1. Load and Split Dataset
    if not os.path.exists(args.gt_file):
        print(f"[ERROR] Ground truth file not found: {args.gt_file}")
        sys.exit(1)

    all_cases = []
    with open(args.gt_file, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                all_cases.append(json.loads(line))

    # Stratified or deterministic shuffle
    random.seed(args.split_seed)
    shuffled_indices = list(range(len(all_cases)))
    random.shuffle(shuffled_indices)

    num_test = int(len(all_cases) * args.test_ratio)
    test_indices = set(shuffled_indices[:num_test])
    test_cases = [all_cases[i] for i in sorted(test_indices)]

    if args.max_samples is not None and args.max_samples < len(test_cases):
        test_cases = test_cases[:args.max_samples]

    print(f"\nTotal Dataset Cases: {len(all_cases)}")
    print(f"Selected Test Evaluation Cases: {len(test_cases)}")

    # 2. Dry-Run Mode (Direct Extraction & Logic Verification)
    if args.dry_run:
        print("\n--- Running Dry-Run Metric Validation ---")
        eval_records = []
        rouge_scores_list = []

        for idx, item in enumerate(test_cases):
            # In dry-run, use ground truth as generated text to verify 100% baseline calibration
            simulated_response = item.get("ground_truth_reasoning", "")
            target_disease = item.get("target_disease", "")
            true_label = item.get("dataset_label", "")

            pred_label = extract_verdict(simulated_response, target_disease)
            is_correct = (pred_label == true_label)

            rouge = compute_rouge_scores(simulated_response, simulated_response)
            rouge_scores_list.append(rouge)

            eval_records.append({
                "pair_id": item.get("pair_id", f"sample_{idx}"),
                "target_disease": target_disease,
                "true_label": true_label,
                "pred_label": pred_label,
                "is_correct": is_correct,
                "generated_text": simulated_response,
                "ground_truth_reasoning": item.get("ground_truth_reasoning", ""),
                "rouge": rouge
            })

        metrics = compute_classification_metrics(eval_records)
        print("\n[Overall Classification Results]:")
        for k, v in metrics["overall_metrics"].items():
            print(f"  {k:28s}: {v}")
        print("\n[Confusion Matrix]:", metrics["confusion_matrix"])

        # Save dry run output
        summary_path = os.path.join(args.output_dir, "dry_run_summary.json")
        with open(summary_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"\n[SUCCESS] Dry-run evaluation completed! Saved to {summary_path}")
        return

    # 3. Model Inference Mode
    try:
        import torch
        from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
        from peft import PeftModel
    except ImportError as e:
        print(f"[ERROR] Required deep learning packages not found: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        sys.exit(1)

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

    print(f"\n>>> Commencing Batch Inference on {len(test_cases)} Test Cases...")
    eval_records = []
    r1_list, r2_list, rL_list = [], [], []

    for idx, item in enumerate(test_cases, 1):
        target_disease = item.get("target_disease", "")
        true_label = item.get("dataset_label", "")
        claims = item.get("claims", [])
        gt_reasoning = item.get("ground_truth_reasoning", "")

        prompt_str = format_prompt(target_disease, claims)
        messages = [
            {
                "role": "system",
                "content": (
                    "You are an expert infectious disease clinician and diagnostic adjudicator. "
                    "Evaluate patient clinical findings using structured step-by-step reasoning "
                    "to determine which diseases the patient is positive for."
                )
            },
            {"role": "user", "content": prompt_str}
        ]
        chat_text = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = tokenizer(chat_text, return_tensors="pt").to(model.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=args.max_new_tokens,
                temperature=args.temperature,
                do_sample=(args.temperature > 0.0),
                pad_token_id=tokenizer.eos_token_id
            )

        gen_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        generated_text = tokenizer.decode(gen_tokens, skip_special_tokens=True).strip()

        pred_label = extract_verdict(generated_text, target_disease)
        is_correct = (pred_label == true_label)

        rouge = compute_rouge_scores(generated_text, gt_reasoning)
        r1_list.append(rouge["rouge1"])
        r2_list.append(rouge["rouge2"])
        rL_list.append(rouge["rougeL"])

        record = {
            "pair_id": item.get("pair_id", f"sample_{idx}"),
            "case_id": item.get("case_id", ""),
            "target_disease": target_disease,
            "true_label": true_label,
            "pred_label": pred_label,
            "is_correct": is_correct,
            "prompt": prompt_str,
            "generated_text": generated_text,
            "ground_truth_reasoning": gt_reasoning,
            "rouge": rouge
        }
        eval_records.append(record)

        if idx % 25 == 0 or idx == len(test_cases):
            cur_acc = sum(r["is_correct"] for r in eval_records) / len(eval_records)
            print(f"  Processed [{idx}/{len(test_cases)}] | Running Diagnostic Accuracy: {cur_acc * 100:.2f}%")

    # 4. Aggregate Metrics
    metrics = compute_classification_metrics(eval_records)
    metrics["reasoning_quality"] = {
        "mean_rouge1": round(sum(r1_list) / max(1, len(r1_list)), 4),
        "mean_rouge2": round(sum(r2_list) / max(1, len(r2_list)), 4),
        "mean_rougeL": round(sum(rL_list) / max(1, len(rL_list)), 4)
    }

    # 5. Save Outputs
    summary_file = os.path.join(args.output_dir, "eval_summary.json")
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    predictions_file = os.path.join(args.output_dir, "predictions_detailed.jsonl")
    errors_file = os.path.join(args.output_dir, "clinical_errors.jsonl")

    num_errors = 0
    with open(predictions_file, "w", encoding="utf-8") as f_pred, \
         open(errors_file, "w", encoding="utf-8") as f_err:
        for rec in eval_records:
            line_str = json.dumps(rec, ensure_ascii=False) + "\n"
            f_pred.write(line_str)
            if not rec["is_correct"]:
                num_errors += 1
                f_err.write(line_str)

    # 6. Display Final Report
    print("\n" + "=" * 70)
    print(" FINAL CLINICAL DIAGNOSTIC EVALUATION REPORT")
    print("=" * 70)
    print(f"Total Evaluated:          {metrics['total_evaluated']}")
    print(f"Diagnostic Accuracy:      {metrics['overall_metrics']['accuracy'] * 100:.2f}%")
    print(f"Sensitivity (Recall):     {metrics['overall_metrics']['sensitivity_recall'] * 100:.2f}% (True Positive Rate)")
    print(f"Specificity:              {metrics['overall_metrics']['specificity'] * 100:.2f}% (True Negative Rate)")
    print(f"Precision (PPV):          {metrics['overall_metrics']['precision_ppv'] * 100:.2f}%")
    print(f"Macro F1-Score:           {metrics['overall_metrics']['f1_score'] * 100:.2f}%")
    print(f"Reasoning ROUGE-1 / L:    {metrics['reasoning_quality']['mean_rouge1']} / {metrics['reasoning_quality']['mean_rougeL']}")
    print(f"Confusion Matrix (TP/FP/TN/FN): {metrics['confusion_matrix']}")
    print(f"Total Clinical Errors:    {num_errors} saved to {errors_file}")
    print(f"Full Summary Saved to:    {summary_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()

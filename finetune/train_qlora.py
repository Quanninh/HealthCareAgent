"""
train_qlora.py

Supervised Fine-Tuning (SFT) using QLoRA for Clinical Diagnostic LLMs.

Context:
Offline distillation was already performed to generate high-capacity clinical reasoning
in the gold-standard dataset (ground_truth_reasoning_all.jsonl).
This script performs parameter-efficient Supervised Fine-Tuning (QLoRA) on the base model
(e.g., Meta-Llama-3-8B-Instruct) directly on this offline-distilled dataset without requiring
an online teacher model during training.

Task Instruction:
Instructs the model to evaluate patient clinical findings and answer:
    "Which diseases is the patient positive?"
"""

import os
import sys
import argparse
from typing import Optional

from finetune.dataset_loader import load_gt_reasoning_dataset, format_positive_diseases_prompt

# Hugging Face and PyTorch imports with friendly fallbacks
try:
    import torch
    from datasets import Dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainingArguments
    )
    from peft import (
        prepare_model_for_kbit_training,
        LoraConfig,
        get_peft_model,
        PeftModel
    )
    from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
    HF_PACKAGES_AVAILABLE = True
except ImportError as e:
    HF_PACKAGES_AVAILABLE = False
    _IMPORT_ERROR_MSG = str(e)
    class SFTTrainer:
        pass
    class TrainingArguments:
        pass


# ================= Command-Line Argument Parser =================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Supervised Fine-Tuning (SFT) using QLoRA on Offline-Distilled Clinical Reasoning"
    )

    # Model & Tokenizer settings
    parser.add_argument(
        "--model_name_or_path",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Hugging Face ID or local path for the target base model (e.g. Meta-Llama-3-8B-Instruct)"
    )
    # Alias for backwards compatibility
    parser.add_argument(
        "--student_model",
        type=str,
        default=None,
        help="[Deprecated alias for --model_name_or_path]"
    )

    # Dataset & Instruction settings
    parser.add_argument(
        "--gt_file",
        type=str,
        default="gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl",
        help="Path to offline-distilled ground truth reasoning dataset JSONL"
    )
    parser.add_argument(
        "--format_type",
        type=str,
        default="chatml",
        choices=["chatml", "alpaca"],
        help="Dataset format: chatml (conversational) or alpaca (instruction-input-output)"
    )
    parser.add_argument(
        "--question_text",
        type=str,
        default="Which diseases is the patient positive?",
        help="Evaluation question to instruct the model to answer"
    )
    parser.add_argument(
        "--max_samples",
        type=int,
        default=None,
        help="Limit number of training samples (useful for quick validation/debugging)"
    )

    # Training & Optimization Hyperparameters
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./qlora_sft_output",
        help="Directory to save checkpoints and final adapter"
    )
    parser.add_argument(
        "--max_seq_length",
        type=int,
        default=2048,
        help="Maximum token sequence length"
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=1,
        help="Per-device train batch size"
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=16,
        help="Number of update steps to accumulate before performing a backward/update pass"
    )
    parser.add_argument(
        "--learning_rate",
        type=float,
        default=2e-4,
        help="Learning rate for LoRA parameters"
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=3,
        help="Number of training epochs"
    )
    parser.add_argument(
        "--warmup_ratio",
        type=float,
        default=0.03,
        help="Ratio of total training steps used for linear warmup"
    )
    parser.add_argument(
        "--lr_scheduler_type",
        type=str,
        default="cosine",
        help="Learning rate scheduler type (e.g. cosine, linear, constant)"
    )

    # QLoRA (LoRA) Hyperparameters
    parser.add_argument(
        "--lora_r",
        type=int,
        default=16,
        help="LoRA rank dimension"
    )
    parser.add_argument(
        "--lora_alpha",
        type=int,
        default=32,
        help="LoRA scaling factor alpha"
    )
    parser.add_argument(
        "--lora_dropout",
        type=float,
        default=0.05,
        help="LoRA dropout rate"
    )
    parser.add_argument(
        "--target_modules",
        nargs="+",
        default=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        help="Names of module linear layers to apply LoRA to"
    )
    parser.add_argument(
        "--response_template",
        type=str,
        default="<|start_header_id|>assistant<|end_header_id|>\n\n",
        help="Token delimiter prefixing assistant response for completion-only loss masking"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Validate dataset formatting and tokenization without downloading/running large models"
    )

    # Deprecated online distillation parameters accepted for backwards compatibility
    parser.add_argument(
        "--teacher_model",
        type=str,
        default=None,
        help="[Deprecated: Online distillation removed; offline-distilled reasoning used directly]"
    )
    parser.add_argument(
        "--no_teacher",
        action="store_true",
        help="[Deprecated: Online distillation removed; SFT QLoRA runs by default]"
    )
    parser.add_argument(
        "--alpha",
        type=float,
        default=None,
        help="[Deprecated: Online distillation loss weight removed]"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=None,
        help="[Deprecated: Online distillation temperature removed]"
    )

    return parser.parse_args()


# ================= Main Training Routine =================
def main():
    args = parse_arguments()

    # Resolve model name
    model_name = args.student_model if args.student_model is not None else args.model_name_or_path

    # Notify if legacy online distillation arguments were passed
    if args.teacher_model or args.alpha is not None or args.temperature is not None:
        print("\n[NOTE] Online distillation arguments (--teacher_model, --alpha, --temperature) are deprecated.")
        print("       Reason: The dataset already contains offline-distilled clinical reasoning.")
        print("       Running pure Supervised Fine-Tuning (SFT) with QLoRA.\n")

    print("=" * 75)
    print(" Clinical LLM Supervised Fine-Tuning (SFT) via QLoRA")
    print(f" Target Question:  '{args.question_text}'")
    print(f" Dataset Path:     {args.gt_file}")
    print(f" Format Type:      {args.format_type}")
    print(f" Base Model:       {model_name}")
    print(f" Output Directory: {args.output_dir}")
    print(f" LoRA Config:      r={args.lora_r}, alpha={args.lora_alpha}, dropout={args.lora_dropout}")
    print(f" Training Config:  epochs={args.epochs}, lr={args.learning_rate}, batch_size={args.batch_size}, grad_accum={args.gradient_accumulation_steps}")
    print("=" * 75)

    # 1. Load Dataset
    print("\n[1/4] Loading offline-distilled clinical reasoning dataset...")
    raw_dataset = load_gt_reasoning_dataset(
        gt_file=args.gt_file,
        format_type=args.format_type,
        question_text=args.question_text,
        max_samples=args.max_samples
    )

    # Dry-run validation check (can run even without GPU/torch dependencies)
    if args.dry_run:
        print("\n--- Dry Run Validation ---")
        print(f"Successfully loaded {len(raw_dataset)} sample record(s).")
        sample = raw_dataset[0]
        if args.format_type == "chatml":
            print(f"\n[System Prompt]:\n{sample['messages'][0]['content']}")
            print(f"\n[User Prompt (with Target Question)]:\n{sample['messages'][1]['content']}")
            print(f"\n[Target Output (Offline-Distilled Reasoning)]:\n{sample['messages'][2]['content']}")
        else:
            print(f"\n[Instruction]:\n{sample['instruction']}")
            print(f"\n[Input]:\n{sample['input']}")
            print(f"\n[Output (Offline-Distilled Reasoning)]:\n{sample['output']}")
        print("\n[SUCCESS] Dataset formatting and prompt question validated. Exiting dry run.")
        return

    if not HF_PACKAGES_AVAILABLE:
        print(f"\n[ERROR] Required packages not found: {_IMPORT_ERROR_MSG}")
        print("Please install required dependencies via:")
        print("    pip install -r requirements.txt")
        sys.exit(1)

    # 2. Setup Tokenizer & Tokenize Dataset
    print(f"\n[2/4] Initializing Tokenizer from {model_name}...")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    print("Formatting text sequences...")
    if args.format_type == "chatml":
        formatted_dataset = raw_dataset.map(lambda batch: {
            "text": [
                tokenizer.apply_chat_template(m, tokenize=False)
                for m in batch["messages"]
            ]
        }, batched=True)
    else:
        prompt_tmpl = "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:\n{output}"
        formatted_dataset = raw_dataset.map(lambda item: {
            "text": prompt_tmpl.format(
                instruction=item["instruction"],
                input=item["input"],
                output=item["output"]
            )
        })

    # Mask prompt tokens so Cross-Entropy loss is calculated strictly on the assistant completion
    collator = DataCollatorForCompletionOnlyLM(
        response_template=args.response_template,
        tokenizer=tokenizer
    )

    # 3. Load Model in 4-bit NF4
    print(f"\n[3/4] Loading Base Model ({model_name}) in 4-bit NormalFloat (NF4)...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    model = prepare_model_for_kbit_training(model)

    print("Configuring LoRA Adapter...")
    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=args.target_modules,
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM"
    )

    # 4. TRL SFTTrainer & Training Loop
    print("\n[4/4] Configuring TRL SFTTrainer...")
    is_cuda = torch.cuda.is_available()
    use_bf16 = is_cuda and torch.cuda.is_bf16_supported()

    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        warmup_ratio=args.warmup_ratio,
        lr_scheduler_type=args.lr_scheduler_type,
        optim="paged_adamw_8bit",
        bf16=use_bf16,
        fp16=(not use_bf16 and is_cuda),
        logging_steps=10,
        save_strategy="epoch",
        save_total_limit=2,
        evaluation_strategy="no",
        report_to="none"
    )

    trainer = SFTTrainer(
        model=model,
        train_dataset=formatted_dataset,
        dataset_text_field="text",
        max_seq_length=args.max_seq_length,
        peft_config=peft_config,
        data_collator=collator,
        tokenizer=tokenizer,
        args=training_args
    )

    print("Trainable Parameters:")
    trainer.model.print_trainable_parameters()

    print("\n>>> Commencing Supervised Fine-Tuning (QLoRA) Training Loop...")
    trainer.train()

    # Save final LoRA adapter weights and tokenizer
    final_adapter_dir = os.path.join(args.output_dir, "final_adapter")
    print(f"\nTraining complete! Saving final LoRA adapter to: {final_adapter_dir}")
    trainer.model.save_pretrained(final_adapter_dir)
    tokenizer.save_pretrained(final_adapter_dir)
    print(f"Adapter successfully saved to: {final_adapter_dir}")


if __name__ == "__main__":
    main()

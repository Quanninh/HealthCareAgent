"""
train_distill_qlora.py

Unified Clinical LLM Fine-Tuning Pipeline:
Online Knowledge Distillation (Teacher: e.g., Llama-3-70B in 8-bit)
+ QLoRA (Student: e.g., Llama-3-8B in 4-bit NF4)

Task Instruction:
Evaluates patient clinical findings and answers: "Which diseases is the patient positive?"
"""

import os
import sys
import argparse

from dataset_loader import load_gt_reasoning_dataset, format_positive_diseases_prompt

# Try importing PyTorch and Hugging Face libraries; provide friendly message if not installed
try:
    import torch
    import torch.nn as nn
    import torch.nn.functional as F
    from datasets import Dataset
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        Trainer,
        TrainingArguments
    )
    from peft import (
        prepare_model_for_kbit_training,
        LoraConfig,
        get_peft_model,
        PeftModel
    )
    from trl import DataCollatorForCompletionOnlyLM
    HF_PACKAGES_AVAILABLE = True
except ImportError as e:
    HF_PACKAGES_AVAILABLE = False
    _IMPORT_ERROR_MSG = str(e)
    # Define minimal placeholder class so script structure parses
    class Trainer:
        pass


# ================= Custom Distillation Trainer =================
class QLoRADistillationTrainer(Trainer):
    """
    Custom Trainer that combines Hard Cross-Entropy Loss with Soft KL Divergence
    Loss from a frozen Teacher model.
    """
    def __init__(
        self,
        model=None,
        teacher_model=None,
        alpha: float = 0.5,
        temperature: float = 2.0,
        distill_on_completion_only: bool = True,
        *args,
        **kwargs
    ):
        super().__init__(model=model, *args, **kwargs)
        self.teacher_model = teacher_model.eval() if teacher_model is not None else None
        self.alpha = alpha
        self.temperature = temperature
        self.distill_on_completion_only = distill_on_completion_only
        self.kl_loss_fn = nn.KLDivLoss(reduction="batchmean")

    def compute_loss(self, model, inputs, return_outputs=False):
        # A. Student forward pass (computes logits and standard CE loss on labels)
        student_outputs = model(**inputs)
        student_logits = student_outputs.logits
        loss_ce = student_outputs.loss

        # If student-only mode or teacher not loaded, return hard loss directly
        if self.teacher_model is None or self.alpha >= 1.0:
            return (loss_ce, student_outputs) if return_outputs else loss_ce

        # B. Teacher forward pass (strictly frozen, no gradient graph)
        with torch.no_grad():
            teacher_outputs = self.teacher_model(
                input_ids=inputs["input_ids"],
                attention_mask=inputs.get("attention_mask")
            )
            teacher_logits = teacher_outputs.logits

        # Ensure vocabulary dimensions match
        if student_logits.size(-1) != teacher_logits.size(-1):
            min_vocab = min(student_logits.size(-1), teacher_logits.size(-1))
            student_logits = student_logits[..., :min_vocab]
            teacher_logits = teacher_logits[..., :min_vocab]

        # C. Target Token Masking for Distillation
        # Mask out prompt tokens so distillation concentrates strictly on response generation
        labels = inputs.get("labels")
        if self.distill_on_completion_only and labels is not None:
            # Causal shift: logits at index t predict token at index t+1
            shift_student_logits = student_logits[..., :-1, :].contiguous()
            shift_teacher_logits = teacher_logits[..., :-1, :].contiguous()
            shift_labels = labels[..., 1:].contiguous()

            mask = (shift_labels != -100)
            if mask.sum() > 0:
                s_logits_active = shift_student_logits[mask]
                t_logits_active = shift_teacher_logits[mask]
            else:
                s_logits_active = shift_student_logits.view(-1, shift_student_logits.size(-1))
                t_logits_active = shift_teacher_logits.view(-1, shift_teacher_logits.size(-1))
        else:
            attention_mask = inputs.get("attention_mask")
            if attention_mask is not None:
                mask = (attention_mask == 1)
                s_logits_active = student_logits[mask]
                t_logits_active = teacher_logits[mask]
            else:
                s_logits_active = student_logits.view(-1, student_logits.size(-1))
                t_logits_active = teacher_logits.view(-1, teacher_logits.size(-1))

        # Ensure teacher logits match student device (crucial for multi-GPU setups)
        t_logits_active = t_logits_active.to(s_logits_active.device)

        # D. Soft Distillation Loss (KL Divergence scaled by T^2)
        student_soft = F.log_softmax(s_logits_active / self.temperature, dim=-1)
        teacher_soft = F.softmax(t_logits_active / self.temperature, dim=-1)
        loss_kd = self.kl_loss_fn(student_soft, teacher_soft) * (self.temperature ** 2)

        # E. Total Multi-Task Distillation Objective
        total_loss = (self.alpha * loss_ce) + ((1.0 - self.alpha) * loss_kd)

        return (total_loss, student_outputs) if return_outputs else total_loss


# ================= Command-Line Argument Parser =================
def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Unified Clinical LLM Knowledge Distillation & QLoRA Fine-Tuning"
    )

    # Model & Tokenizer settings
    parser.add_argument(
        "--teacher_model",
        type=str,
        default="meta-llama/Meta-Llama-3-70B-Instruct",
        help="Hugging Face ID or local path for high-capacity Teacher model"
    )
    parser.add_argument(
        "--student_model",
        type=str,
        default="meta-llama/Meta-Llama-3-8B-Instruct",
        help="Hugging Face ID or local path for deployable Student model"
    )
    parser.add_argument(
        "--no_teacher",
        action="store_true",
        help="Disable teacher distillation; run Student-only QLoRA fine-tuning"
    )

    # Dataset & Instruction settings
    parser.add_argument(
        "--gt_file",
        type=str,
        default="gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl",
        help="Path to ground truth reasoning dataset JSONL"
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
        help="Limit number of training samples (useful for quick validation)"
    )

    # Distillation Hyperparameters
    parser.add_argument(
        "--alpha",
        type=float,
        default=0.5,
        help="Weight balancing Cross-Entropy loss (alpha) and Distillation loss (1 - alpha)"
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=2.0,
        help="Temperature T for probability distribution softening"
    )

    # QLoRA & Training Hyperparameters
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./qlora_distilled_output",
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
        help="Gradient accumulation steps"
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
        "--response_template",
        type=str,
        default="<|start_header_id|>assistant<|end_header_id|>\n\n",
        help="Token delimiter prefixing assistant response for loss masking"
    )
    parser.add_argument(
        "--dry_run",
        action="store_true",
        help="Validate dataset formatting and tokenization without downloading/running large models"
    )

    return parser.parse_args()


# ================= Main Training Routine =================
def main():
    args = parse_arguments()

    print("=" * 70)
    print(" Clinical LLM Knowledge Distillation & QLoRA Fine-Tuning")
    print(f" Question Target: '{args.question_text}'")
    print(f" Format Type:     {args.format_type}")
    print(f" Dataset Path:    {args.gt_file}")
    print(f" Student Model:   {args.student_model}")
    print(f" Teacher Model:   {'Disabled' if args.no_teacher else args.teacher_model}")
    print(f" Loss Weights:    alpha={args.alpha} (CE), 1-alpha={1.0 - args.alpha} (KD), T={args.temperature}")
    print("=" * 70)

    # 1. Load Dataset
    print("\n[1/5] Loading ground truth clinical reasoning dataset...")
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
            print(f"\n[Target Output (Adjudication Reasoning)]:\n{sample['messages'][2]['content']}")
        else:
            print(f"\n[Instruction]:\n{sample['instruction']}")
            print(f"\n[Input]:\n{sample['input']}")
            print(f"\n[Output]:\n{sample['output']}")
        print("\n[SUCCESS] Dataset formatting and prompt question validated. Exiting dry run.")
        return

    if not HF_PACKAGES_AVAILABLE:
        print(f"\n[ERROR] Required packages not found: {_IMPORT_ERROR_MSG}")
        print("Please install required dependencies via:")
        print("    pip install -r requirements.txt")
        sys.exit(1)

    # 2. Setup Tokenizer
    print("\n[2/5] Initializing Tokenizer...")
    tokenizer = AutoTokenizer.from_pretrained(args.student_model)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Tokenize dataset based on format
    print("Applying text formatting...")
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

    # Tokenize into input_ids and attention_mask required by transformers.Trainer
    print("Tokenizing sequence into input_ids and attention_mask...")
    def tokenize_fn(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            max_length=args.max_seq_length,
            padding=False
        )

    tokenized_dataset = formatted_dataset.map(
        tokenize_fn,
        batched=True,
        remove_columns=formatted_dataset.column_names
    )

    # Prompt Loss Masking Collator (calculates loss strictly on the assistant response)
    collator = DataCollatorForCompletionOnlyLM(
        response_template=args.response_template,
        tokenizer=tokenizer
    )

    # 3. Load Teacher Model (if enabled)
    teacher_model = None
    if not args.no_teacher and args.alpha < 1.0:
        print(f"\n[3/5] Loading Teacher Model ({args.teacher_model}) in 8-bit...")
        teacher_model = AutoModelForCausalLM.from_pretrained(
            args.teacher_model,
            load_in_8bit=True,
            device_map="auto"
        )
        for param in teacher_model.parameters():
            param.requires_grad = False
        print("Teacher model loaded and frozen successfully.")
    else:
        print("\n[3/5] Teacher distillation disabled. Running in student-only QLoRA mode.")

    # 4. Load Student Model in 4-bit NF4 with LoRA
    print(f"\n[4/5] Loading Student Model ({args.student_model}) in 4-bit NF4...")
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_use_double_quant=True,
        bnb_4bit_compute_dtype=torch.bfloat16
    )
    student_model = AutoModelForCausalLM.from_pretrained(
        args.student_model,
        quantization_config=bnb_config,
        device_map="auto"
    )
    student_model = prepare_model_for_kbit_training(student_model)

    peft_config = LoraConfig(
        r=args.lora_r,
        lora_alpha=args.lora_alpha,
        target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
        lora_dropout=args.lora_dropout,
        bias="none",
        task_type="CAUSAL_LM"
    )
    student_model = get_peft_model(student_model, peft_config)
    print("LoRA Adapter Attached. Trainable Parameters:")
    student_model.print_trainable_parameters()

    # 5. Initialize Trainer & Train
    print("\n[5/5] Configuring Distillation Trainer & Training Arguments...")
    training_args = TrainingArguments(
        output_dir=args.output_dir,
        per_device_train_batch_size=args.batch_size,
        gradient_accumulation_steps=args.gradient_accumulation_steps,
        learning_rate=args.learning_rate,
        num_train_epochs=args.epochs,
        optim="paged_adamw_8bit",
        bf16=True,
        logging_steps=10,
        save_strategy="epoch",
        evaluation_strategy="no",
        report_to="none"
    )

    trainer = QLoRADistillationTrainer(
        model=student_model,
        teacher_model=teacher_model,
        alpha=args.alpha,
        temperature=args.temperature,
        train_dataset=tokenized_dataset,
        data_collator=collator,
        args=training_args
    )

    print("\n>>> Commencing Distillation + QLoRA Training Loop...")
    trainer.train()

    # Save final LoRA adapter weights and tokenizer
    final_adapter_dir = os.path.join(args.output_dir, "final_adapter")
    print(f"\nTraining complete! Saving final LoRA adapter to: {final_adapter_dir}")
    trainer.model.save_pretrained(final_adapter_dir)
    tokenizer.save_pretrained(final_adapter_dir)
    print(f"Adapter successfully saved to: {final_adapter_dir}")


if __name__ == "__main__":
    main()

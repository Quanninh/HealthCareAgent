# Step-by-Step Running Commands Guide

This operational manual documents the exact step-by-step commands to set up the environment, validate datasets, run **Supervised Fine-Tuning (SFT) using QLoRA** on the offline-distilled reasoning dataset, monitor progress, and perform clinical evaluation answering:
> **"Which diseases is the patient positive?"**

---

## Quick Reference Table of Commands

| Step | Action | Command |
| :--- | :--- | :--- |
| **1** | Environment Setup | `python3 -m venv venv && source venv/bin/activate` |
| **2** | Install Dependencies | `pip install -r requirements.txt` |
| **3** | Hugging Face Auth | `huggingface-cli login` |
| **4** | Pre-Flight Validation | `python3 test_qlora_pipeline.py` |
| **5** | Dataset Format Check | `python3 train_qlora.py --dry_run --max_samples 1` |
| **6A** | **Full SFT QLoRA Training** | `python3 train_qlora.py --epochs 3 --output_dir ./qlora_sft_output` |
| **6B** | **Fast Smoke Test (10 cases)** | `python3 train_qlora.py --max_samples 10 --epochs 1 --output_dir ./qlora_smoke_test` |
| **7** | Inference on Dataset Case | `python3 inference_qlora.py --sample_index 30` |
| **8** | Custom Clinical Evaluation | `python3 inference_qlora.py --disease "COVID-19" --findings "..."` |
| **9** | **Base vs Fine-Tuned Comparison** | `python3 evaluate_model.py --eval_mode compare` |

---

## Phase 1: Environment Setup & Prerequisites

### 1.1 Hardware Sizing Recommendations
* **Supervised Fine-Tuning using QLoRA (Base 8B in 4-bit NF4 + LoRA Adapters):**
  * Memory footprint: **~8–12 GB VRAM**.
  * Fits comfortably on standard GPUs: RTX 3080/3090/4080/4090, T4, A10G, V100, A5000, A100.
  * No 70B online teacher needed in memory, because **offline distillation was already pre-computed** in `ground_truth_reasoning_all.jsonl`.

### 1.2 Virtual Environment Creation & Installation
```bash
# 1. Create a dedicated Python virtual environment
python3 -m venv venv

# 2. Activate virtual environment
source venv/bin/activate

# 3. Upgrade pip and wheel
pip install --upgrade pip setuptools wheel

# 4. Install all required dependencies
pip install -r requirements.txt
```

### 1.3 Hugging Face Authentication (For Llama-3 Models)
Meta-Llama-3 models (`Meta-Llama-3-8B-Instruct`) are gated models. Accept Meta's license agreement on Hugging Face and log in via the CLI:
```bash
huggingface-cli login
```
*(Paste your User Access Token when prompted)*

---

## Phase 2: Pre-Flight Pipeline & Dataset Validation

Always run dry-run validation before committing GPU compute hours.

### 2.1 Run Unit Tests
Verifies dataset loading logic, Alpaca/ChatML formatting, deterministic verdict extraction, and completion loss masking math:
```bash
python3 test_qlora_pipeline.py
```
*Expected Output:* `Ran 5 tests in ... OK`

### 2.2 Dry-Run Dataset & Prompt Inspection (ChatML Format)
Inspects how clinical claims are formatted with the target question without downloading models:
```bash
python3 train_qlora.py --dry_run --max_samples 1
```

### 2.3 Dry-Run Dataset Inspection (Alpaca Format)
```bash
python3 train_qlora.py --dry_run --max_samples 1 --format_type alpaca
```

### 2.4 Verify Inference Prompt Construction
Inspects how an unseen clinical case is presented to the model:
```bash
python3 inference_qlora.py --dry_run --sample_index 30
```

---

## Phase 3: Training Execution Commands

### Scenario A: Full Supervised Fine-Tuning (QLoRA)
Trains the base model on all 5,308 offline-distilled clinical reasoning records:

```bash
python3 train_qlora.py \
    --model_name_or_path meta-llama/Meta-Llama-3-8B-Instruct \
    --gt_file gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl \
    --format_type chatml \
    --question_text "Which diseases is the patient positive?" \
    --max_seq_length 2048 \
    --batch_size 1 \
    --gradient_accumulation_steps 16 \
    --learning_rate 2e-4 \
    --epochs 3 \
    --lora_r 16 \
    --lora_alpha 32 \
    --lora_dropout 0.05 \
    --output_dir ./qlora_sft_output
```

---

### Scenario B: Fast Debugging / Smoke Run (10 Samples)
Before launching a multi-hour run, verify that the training loop, completion loss masking, backward pass, and adapter saving execute end-to-end:

```bash
python3 train_qlora.py \
    --max_samples 10 \
    --epochs 1 \
    --output_dir ./qlora_smoke_test
```

---

### Scenario C: Background Execution via `tmux` or `nohup`
For long-running training jobs on remote compute instances:

#### Using `tmux`:
```bash
# 1. Start a new session
tmux new -s train_sft

# 2. Activate environment and run command
source venv/bin/activate
python3 train_qlora.py --epochs 3 --output_dir ./qlora_sft_output

# 3. Detach from session: Press Ctrl+B, then D
# 4. Re-attach to session later:
tmux attach -t train_sft
```

#### Using `nohup`:
```bash
nohup python3 train_qlora.py \
    --epochs 3 \
    --output_dir ./qlora_sft_output \
    > training.log 2>&1 &

# Monitor live training logs
tail -f training.log
```

---

## Phase 4: Post-Training Inference & Evaluation

Once training finishes, the final LoRA adapter is saved at `./qlora_sft_output/final_adapter`.

### 4.1 Evaluate Cases from the Dataset

#### Test a Confirmed Positive Case (Sample #30: Brucellosis):
```bash
python3 inference_qlora.py \
    --adapter_path ./qlora_sft_output/final_adapter \
    --sample_index 30
```

#### Test an Out-of-Scope / Negative Case (Sample #0: Brucellosis Ruled Out):
```bash
python3 inference_qlora.py \
    --adapter_path ./qlora_sft_output/final_adapter \
    --sample_index 0
```

---

### 4.2 Evaluate Custom Unseen Patient Findings

Provide clinical claims directly from the command line:

```bash
python3 inference_qlora.py \
    --adapter_path ./qlora_sft_output/final_adapter \
    --disease "COVID-19" \
    --findings "- 45-year-old patient presented with acute onset fever, dyspnea, and bilateral lung infiltrates on CT.\n- Real-time RT-PCR nasopharyngeal swab tested positive for SARS-CoV-2 RNA." \
    --temperature 0.1
```

```bash
python3 inference_qlora.py \
    --adapter_path ./qlora_sft_output/final_adapter \
    --disease "Tuberculosis" \
    --findings "- Chronic productive cough for 4 weeks accompanied by night sweats and weight loss.\n- Sputum smear microscopy identified acid-fast bacilli (AFB 3+), and GeneXpert MTB/RIF detected Mycobacterium tuberculosis without rifampicin resistance." \
    --temperature 0.1
```

---

### 4.3 Head-to-Head Evaluation: Base Model vs Fine-Tuned Model (Disease Name + Reason)
Runs comparative evaluation on the held-out test split, evaluating the complete fine-tuning objective (**Disease Name & Subtype Identification + Step-by-Step Reasoning**):
* **Disease Identification**: Disease name accuracy, header positioning, and etiologic subtype/pathogen detection rate.
* **Clinical Reasoning Quality**: Structured reasoning rate (`Reasoning: (1)...`), average reasoning steps, clinical claim coverage, and ROUGE-1/2/L text overlap.
* **Joint Diagnostic Success**: Full success rate where model correctly names the disease, provides structured rationale, and confirms diagnosis.
* **Case-Level Adjudication Transitions**: Wins (`FT_IMPROVED`), Retained (`BOTH_CORRECT`), and Net Gain.
* Exports `comparison_summary.json`, `comparison_cases.jsonl`, and `clinical_wins.jsonl`.

```bash
# 1. Full comparative evaluation on held-out test cases
python3 evaluate_model.py \
    --eval_mode compare \
    --base_model meta-llama/Meta-Llama-3-8B-Instruct \
    --adapter_path ./qlora_sft_output/final_adapter \
    --test_ratio 0.15 \
    --output_dir ./eval_results

# 2. Fast comparative dry-run (validates comparative tables and metrics without GPU)
python3 evaluate_model.py --dry_run --max_samples 10

# 3. Fine-Tuned model only (standalone)
python3 evaluate_model.py --eval_mode finetuned --adapter_path ./qlora_sft_output/final_adapter

# 4. Base model only (standalone zero-shot baseline)
python3 evaluate_model.py --eval_mode base --base_model meta-llama/Meta-Llama-3-8B-Instruct
```

---

## Phase 5: Hyperparameter Tuning Reference

| Flag | Default | Description | Guidance |
| :--- | :--- | :--- | :--- |
| `--batch_size` | `1` | Per-device training batch size | Keep at 1 or 2 to stay within GPU VRAM limits. |
| `--gradient_accumulation_steps` | `16` | Steps before gradient update | Effective batch size = `batch_size * gradient_accumulation_steps` (e.g. 16). |
| `--learning_rate` | `2e-4` | LoRA AdamW learning rate | Recommended range for QLoRA SFT: `1e-4` to `3e-4`. |
| `--lora_r` | `16` | LoRA rank dimension | Higher rank (`32` or `64`) provides greater representational capacity for complex reasoning. |
| `--lora_alpha` | `32` | LoRA scaling factor | Typically set to $2 \times r$. |
| `--lora_dropout` | `0.05` | LoRA dropout rate | Prevents overfitting on reasoning patterns. |
| `--max_seq_length` | `2048` | Maximum token sequence length | Accommodates long multi-bullet clinical findings + step-by-step diagnostic reasoning. |
| `--warmup_ratio` | `0.03` | Linear warmup ratio | Smoothly ramps learning rate during initial training steps. |
| `--lr_scheduler_type` | `cosine` | Learning rate schedule | Cosine schedule provides gradual decay toward end of training. |

---

## Phase 6: Troubleshooting & Common Pitfalls

1. **CUDA Out of Memory (OOM):**
   * Keep `--batch_size 1` and compensate with `--gradient_accumulation_steps 16` or `32`.
   * Ensure 4-bit NF4 quantization is enabled (default in `train_qlora.py`).
2. **Gated Model Access / 403 Forbidden:**
   * Accept the license terms at [meta-llama/Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct).
   * Run `huggingface-cli login` and paste your User Access Token.
3. **`bitsandbytes` CUDA Architecture Warning:**
   * Ensure `pip install -U bitsandbytes>=0.43.0` is installed with a CUDA-compatible PyTorch build.

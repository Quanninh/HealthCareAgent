# Step-by-Step Running Commands Guide

This operational manual documents the exact step-by-step commands to set up the environment, validate datasets, run Knowledge Distillation + QLoRA training, monitor progress, and perform clinical inference evaluation answering:
> **"Which diseases is the patient positive?"**

---

## Quick Reference Table of Commands

| Step | Action | Command |
| :--- | :--- | :--- |
| **1** | Environment Setup | `python3 -m venv venv && source venv/bin/activate` |
| **2** | Install Dependencies | `pip install -r requirements.txt` |
| **3** | Hugging Face Auth | `huggingface-cli login` |
| **4** | Pre-Flight Validation | `python3 test_distill_pipeline.py` |
| **5** | Dataset Format Check | `python3 train_distill_qlora.py --dry_run --max_samples 1` |
| **6A** | **Full 70B Distillation** | `python3 train_distill_qlora.py --alpha 0.5 --epochs 3` |
| **6B** | **Single-GPU QLoRA** | `python3 train_distill_qlora.py --no_teacher --epochs 3` |
| **7** | Inference on Dataset Case | `python3 inference_distill_qlora.py --sample_index 30` |
| **8** | Custom Clinical Evaluation | `python3 inference_distill_qlora.py --disease "COVID-19" --findings "..."` |

---

## Phase 1: Environment Setup & Prerequisites

### 1.1 Hardware Sizing Recommendations
* **Full Online Distillation (Teacher 70B in 8-bit + Student 8B in 4-bit):**
  * Requires **~78–82 GB VRAM**.
  * Recommended: 1× A100 (80GB), 1× H100 (80GB), or 2× A100 (40GB/80GB) / 4× RTX 3090/4090 (24GB).
* **Student-Only QLoRA (`--no_teacher` mode):**
  * Requires **~8–12 GB VRAM**.
  * Supported on: RTX 3080/3090/4080/4090, T4, A10G, V100, A5000.

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
Meta-Llama-3 models (`Meta-Llama-3-70B-Instruct` and `Meta-Llama-3-8B-Instruct`) are gated models. You must accept Meta's license agreement on Hugging Face and log in via the CLI:
```bash
huggingface-cli login
```
*(Paste your User Access Token when prompted)*

---

## Phase 2: Pre-Flight Pipeline & Dataset Validation

Always run dry-run validation before committing GPU compute hours.

### 2.1 Run Unit Tests
Verifies dataset loading logic, Alpaca/ChatML formatting, and mathematical loss computation ($T^2 \cdot \text{KL}$ dual loss):
```bash
python3 test_distill_pipeline.py
```
*Expected Output:* `Ran 4 tests in ... OK`

### 2.2 Dry-Run Dataset & Prompt Inspection (ChatML Format)
Inspects how clinical claims are formatted with the target question without downloading models:
```bash
python3 train_distill_qlora.py --dry_run --max_samples 1
```

### 2.3 Dry-Run Dataset Inspection (Alpaca Format)
```bash
python3 train_distill_qlora.py --dry_run --max_samples 1 --format_type alpaca
```

### 2.4 Verify Inference Prompt Construction
Inspects how an unseen clinical case is presented to the model:
```bash
python3 inference_distill_qlora.py --dry_run --sample_index 30
```

---

## Phase 3: Training Execution Commands

### Scenario A: Full Knowledge Distillation (Teacher 70B in 8-bit + Student 8B in 4-bit)
*Ideal for multi-GPU nodes or 80GB GPUs (A100/H100).*

```bash
python3 train_distill_qlora.py \
    --teacher_model meta-llama/Meta-Llama-3-70B-Instruct \
    --student_model meta-llama/Meta-Llama-3-8B-Instruct \
    --gt_file gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl \
    --format_type chatml \
    --question_text "Which diseases is the patient positive?" \
    --alpha 0.5 \
    --temperature 2.0 \
    --max_seq_length 2048 \
    --batch_size 1 \
    --gradient_accumulation_steps 16 \
    --learning_rate 2e-4 \
    --epochs 3 \
    --lora_r 16 \
    --lora_alpha 32 \
    --lora_dropout 0.05 \
    --output_dir ./qlora_distilled_output
```

---

### Scenario B: Student-Only QLoRA Training (Single Consumer GPU / Lower VRAM)
*Ideal for machines with 16GB–24GB VRAM (RTX 3090, 4090, A10, Colab Pro).*
By passing `--no_teacher`, the script bypasses loading the 70B model and optimizes the 8B student with completion-loss masking.

```bash
python3 train_distill_qlora.py \
    --no_teacher \
    --student_model meta-llama/Meta-Llama-3-8B-Instruct \
    --gt_file gt_reasoning/output_gt_reasoning/ground_truth_reasoning_all.jsonl \
    --format_type chatml \
    --question_text "Which diseases is the patient positive?" \
    --batch_size 1 \
    --gradient_accumulation_steps 16 \
    --learning_rate 2e-4 \
    --epochs 3 \
    --output_dir ./qlora_distilled_output
```

---

### Scenario C: Fast Debugging / Smoke Run (10 Samples)
Before launching a multi-hour run, verify that the training loop, backward pass, and adapter saving execute end-to-end on 10 samples:

```bash
python3 train_distill_qlora.py \
    --no_teacher \
    --max_samples 10 \
    --epochs 1 \
    --output_dir ./qlora_smoke_test
```

---

### Scenario D: Background Execution via `nohup` or `tmux`
For long-running training jobs on remote servers:

#### Using `tmux`:
```bash
# 1. Start a new session
tmux new -s train_distill

# 2. Activate environment and run command
source venv/bin/activate
python3 train_distill_qlora.py --alpha 0.5 --output_dir ./qlora_distilled_output

# 3. Detach from session: Press Ctrl+B, then D
# 4. Re-attach to session later:
tmux attach -t train_distill
```

#### Using `nohup`:
```bash
nohup python3 train_distill_qlora.py \
    --alpha 0.5 \
    --output_dir ./qlora_distilled_output \
    > training.log 2>&1 &

# Monitor live training logs
tail -f training.log
```

---

## Phase 4: Post-Training Inference & Evaluation

Once training finishes, the final LoRA adapter is saved at `./qlora_distilled_output/final_adapter`.

### 4.1 Evaluate Known Cases from the Dataset

#### Test a Confirmed Positive Case (Sample #30: Brucellosis):
```bash
python3 inference_distill_qlora.py \
    --adapter_path ./qlora_distilled_output/final_adapter \
    --sample_index 30
```

#### Test an Out-of-Scope / Negative Case (Sample #0: Brucellosis Ruled Out):
```bash
python3 inference_distill_qlora.py \
    --adapter_path ./qlora_distilled_output/final_adapter \
    --sample_index 0
```

---

### 4.2 Evaluate Custom Unseen Patient Findings

Provide clinical claims directly from the command line:

```bash
python3 inference_distill_qlora.py \
    --adapter_path ./qlora_distilled_output/final_adapter \
    --disease "COVID-19" \
    --findings "- 45-year-old patient presented with acute onset fever, dyspnea, and bilateral lung infiltrates on CT.\n- Real-time RT-PCR nasopharyngeal swab tested positive for SARS-CoV-2 RNA." \
    --temperature 0.1
```

```bash
python3 inference_distill_qlora.py \
    --adapter_path ./qlora_distilled_output/final_adapter \
    --disease "Tuberculosis" \
    --findings "- Chronic productive cough for 4 weeks accompanied by night sweats and weight loss.\n- Sputum smear microscopy identified acid-fast bacilli (AFB 3+), and GeneXpert MTB/RIF detected Mycobacterium tuberculosis without rifampicin resistance." \
    --temperature 0.1
```

---

## Phase 5: Hyperparameter Tuning Reference

| Flag | Default | Description | Guidance |
| :--- | :--- | :--- | :--- |
| `--alpha` | `0.5` | Weight for Cross-Entropy vs Distillation | `0.5` is balanced. Higher (`0.7`) emphasizes exact text match; lower (`0.3`) emphasizes teacher probability distribution. |
| `--temperature` | `2.0` | Softmax temperature ($T$) | Values between `2.0` and `4.0` soften probabilities to expose secondary candidate rankings. |
| `--gradient_accumulation_steps` | `16` | Steps before gradient update | With `batch_size=1`, effective batch size is `16`. Increase to `32` if training stability is needed. |
| `--learning_rate` | `2e-4` | LoRA AdamW learning rate | Recommended range: `1e-4` to `3e-4`. |
| `--lora_r` | `16` | LoRA rank | `16` or `32` provides sufficient expressive capacity for multi-step clinical reasoning. |
| `--lora_alpha` | `32` | LoRA scaling factor | Typically set to $2 \times r$. |
| `--max_seq_length` | `2048` | Maximum token sequence length | Covers long multi-bullet clinical claims + detailed reasoning traces. |

---

## Phase 6: Troubleshooting & Common Pitfalls

1. **CUDA Out of Memory (OOM) during Distillation:**
   * Set `--batch_size 1` and increase `--gradient_accumulation_steps 32`.
   * If on a 24GB or 40GB GPU, run in `--no_teacher` mode (Student 4-bit QLoRA uses only ~9GB VRAM).
2. **Gated Repo / Hugging Face 403 Forbidden:**
   * Make sure you accepted the terms at [meta-llama/Meta-Llama-3-8B-Instruct](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct).
   * Run `huggingface-cli login` and paste your access token.
3. **`bitsandbytes` CUDA Architecture Warning:**
   * Ensure `pip install -U bitsandbytes>=0.43.0` is installed with a CUDA-compatible PyTorch build.

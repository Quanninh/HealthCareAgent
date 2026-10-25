# QLoRA Input Format & Implementation Guide

This guide documents the data structure, input format, and a concise QLoRA implementation tailored to the clinical claim adjudication dataset in `workspace/labeled_pool`.

---

## 1. Dataset Structure & Pairing

The dataset pairs clinical narratives with gold-standard clinical adjudications using `pair_id` (e.g., `PMC10196249_01::COVID-19`):

* **Input Features** (`workspace/labeled_pool/input/input_<disease>.jsonl`):
  * `pair_id`, `target_disease`, `case_text`, `title`, `abstract`, `age`, `gender`.
* **Target Annotations** (`workspace/labeled_pool/output/output_<disease>.jsonl`):
  * `pair_id`, `step12_dataset_label` (`POSITIVE`, `NEGATIVE`, `EXCLUDED_NON_TARGET_CASE`), `rationale`, `confidence`, `step9_key_evidence`.

---

## 2. Input Formats & Their Python Definitions

In your preprocessing pipeline, every case from your dataset produces two foundational variables:
* **`user_prompt`**: String combining patient demographics (`target_disease`, `age`, `gender`, `title`) and the raw `case_text`.
* **`target_output`**: String containing the ground-truth adjudication JSON (`decision`, `confidence`, `rationale`, `key_evidence`).

Below is how `user_prompt`, `target_output`, and `samples` define the two format types:

---

### Format Type 1: ChatML / Multi-Turn Conversational Format (Recommended for Chat Models)
Best suited for chat-instruct models (e.g., Llama-3-Instruct, MedGemma) using native chat templates.

#### 1. Python Code Definition:
```python
# In your pipeline loop:
samples.append({
    "messages": [
        {
            "role": "system",
            "content": "You are a clinical expert. Adjudicate whether the case report contains a confirmed clinical claim for the target disease. Output valid JSON."
        },
        {
            "role": "user",
            "content": user_prompt       # <-- Connects patient context + raw case_text
        },
        {
            "role": "assistant",
            "content": target_output     # <-- Connects ground-truth adjudication JSON
        }
    ]
})
```

#### 2. Resulting JSON Record:
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a clinical expert. Adjudicate whether the case report contains a confirmed clinical claim for the target disease. Output valid JSON."
    },
    {
      "role": "user",
      "content": "Target Disease: COVID-19\nPatient Demographics: Age 0.0, Gender Male\n\nCase Report:\nA 27-day-old boy presented with fever... RNA test for SARS-CoV-2 from a throat swab was positive.\n\nTask: Adjudicate the case and output decision, rationale, and key evidence as JSON."
    },
    {
      "role": "assistant",
      "content": "{\n  \"decision\": \"POSITIVE\",\n  \"confidence\": \"HIGH\",\n  \"rationale\": \"Patient diagnosed with active COVID-19 confirmed by positive SARS-CoV-2 RT-PCR.\",\n  \"key_evidence\": [\n    {\n      \"source_quote\": \"RNA test for SARS-CoV-2 from a throat swab was positive.\",\n      \"test_name\": \"SARS-CoV-2 RT-PCR / NAAT\",\n      \"result\": \"POSITIVE\"\n    }\n  ]\n}"
    }
  ]
}
```

#### 3. How Tokenized in QLoRA:
```python
# Applies model-specific tokens (e.g. <|start_header_id|>user<|end_header_id|>)
formatted_text = tokenizer.apply_chat_template(item["messages"], tokenize=False)
```

---

### Format Type 2: Alpaca / Instruction-Input-Output Format (Standard 3-Field Format)
Best suited for base models or custom prompt templates, cleanly isolating the instructions from the case text.

#### 1. Python Code Definition:
```python
# In your pipeline loop:
instruction_text = (
    f"Adjudicate whether the clinical case report contains a confirmed clinical claim "
    f"for {in_rec.get('target_disease')}. Output decision, rationale, and key evidence as JSON."
)

samples.append({
    "instruction": instruction_text,     # <-- Connects task instruction rule
    "input": user_prompt,               # <-- Connects patient context + raw case_text
    "output": target_output             # <-- Connects ground-truth adjudication JSON
})
```

#### 2. Resulting JSON Record:
```json
{
  "instruction": "Adjudicate whether the clinical case report contains a confirmed clinical claim for COVID-19. Output decision, rationale, and key evidence as JSON.",
  "input": "Target Disease: COVID-19\nPatient Demographics: Age 0.0, Gender Male\n\nCase Report:\nA 27-day-old boy presented with fever... RNA test for SARS-CoV-2 from a throat swab was positive.",
  "output": "{\n  \"decision\": \"POSITIVE\",\n  \"confidence\": \"HIGH\",\n  \"rationale\": \"Patient diagnosed with active COVID-19 confirmed by positive SARS-CoV-2 RT-PCR.\",\n  \"key_evidence\": [\n    {\n      \"source_quote\": \"RNA test for SARS-CoV-2 from a throat swab was positive.\",\n      \"test_name\": \"SARS-CoV-2 RT-PCR / NAAT\",\n      \"result\": \"POSITIVE\"\n    }\n  ]\n}"
}
```

#### 3. How Tokenized in QLoRA:
```python
prompt_template = "### Instruction:\n{instruction}\n\n### Input:\n{input}\n\n### Response:\n{output}"
formatted_text = prompt_template.format(**item)
```

---

### 2.3 Tensor Representation (Common to Both Formats)
Regardless of the text format chosen above, during training the formatted text is converted into PyTorch tensors:
* **`input_ids`**: `[batch_size, seq_len]` (Tokens representing System/Instruction + Input + Output).
* **`attention_mask`**: `[batch_size, seq_len]` (`1` for active tokens, `0` for padding).
* **`labels`**: `[batch_size, seq_len]` (Prompt tokens up to the response header are masked with **`-100`**; loss is computed **strictly on the output/assistant tokens**).

---

## 3. Connecting Pipeline Variables to the Two Format Types

Inside your data loading script, you extract and build two core strings for each paired case:
* **`user_prompt`**: Combines patient metadata and the raw `case_text`.
* **`target_output`**: The ground-truth adjudication JSON string (`decision`, `rationale`, `key_evidence`).

Here is how `user_prompt` and `target_output` map directly into `samples` for each format:

### Mapping Table

| Code Variable | Format 1 (ChatML) | Format 2 (Alpaca) |
| :--- | :--- | :--- |
| **Task / System prompt** | `{"role": "system", "content": ...}` | `"instruction": ...` |
| **`user_prompt` (Case narrative + info)** | `{"role": "user", "content": user_prompt}` | `"input": user_prompt` |
| **`target_output` (Adjudication JSON)** | `{"role": "assistant", "content": target_output}` | `"output": target_output` |
| **How Tokenized in QLoRA** | `tokenizer.apply_chat_template(messages)` | `f"### Instruction:\n{inst}\n\n### Input:\n{inp}\n\n### Response:\n{out}"` |

---

### Implementation in Python (Supporting Both Formats)

```python
import json, glob, os
from datasets import Dataset

def load_paired_dataset(input_dir, output_dir, format_type="chatml") -> Dataset:
    """
    Loads and pairs records from input/ and output/ by pair_id.
    format_type: "chatml" (Format 1) or "alpaca" (Format 2)
    """
    inputs = {}
    for f in glob.glob(os.path.join(input_dir, "input_*.jsonl")):
        with open(f, "r", encoding="utf-8") as r:
            for line in r:
                if line.strip():
                    item = json.loads(line)
                    inputs[item["pair_id"]] = item

    samples = []
    for f in glob.glob(os.path.join(output_dir, "output_*.jsonl")):
        with open(f, "r", encoding="utf-8") as r:
            for line in r:
                if not line.strip():
                    continue
                out_rec = json.loads(line)
                in_rec = inputs.get(out_rec.get("pair_id"))
                if not in_rec or not in_rec.get("case_text"):
                    continue

                # 1. The input prompt (metadata + raw case text)
                user_prompt = (
                    f"Target Disease: {in_rec.get('target_disease')}\n"
                    f"Patient Demographics: Age {in_rec.get('age', 'N/A')}, Gender {in_rec.get('gender', 'N/A')}\n\n"
                    f"Case Report:\n{in_rec['case_text'].strip()}\n\n"
                    f"Task: Adjudicate the case and output decision, rationale, and key evidence as JSON."
                )

                # 2. The expected completion (decision + rationale + evidence)
                target_output = json.dumps({
                    "decision": out_rec.get("step12_dataset_label"),
                    "confidence": out_rec.get("confidence"),
                    "rationale": out_rec.get("rationale"),
                    "key_evidence": out_rec.get("step9_key_evidence", {}).get("evidence_items", [])
                }, ensure_ascii=False, indent=2)

                # 3. Append to samples based on format_type
                if format_type == "chatml":
                    # Format 1: ChatML
                    samples.append({
                        "messages": [
                            {"role": "system", "content": "You are a clinical expert adjudicator. Output valid JSON."},
                            {"role": "user", "content": user_prompt},
                            {"role": "assistant", "content": target_output}
                        ]
                    })
                elif format_type == "alpaca":
                    # Format 2: Alpaca
                    instruction_text = (
                        f"Adjudicate whether the clinical case report contains a confirmed clinical claim "
                        f"for {in_rec.get('target_disease')}. Output decision, rationale, and key evidence as JSON."
                    )
                    samples.append({
                        "instruction": instruction_text,
                        "input": user_prompt,
                        "output": target_output
                    })

    return Dataset.from_list(samples)
```

---

## 4. Short QLoRA Implementation

```python
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, TrainingArguments
from peft import prepare_model_for_kbit_training, LoraConfig, get_peft_model
from trl import SFTTrainer, DataCollatorForCompletionOnlyLM

MODEL_ID = "meta-llama/Meta-Llama-3-8B-Instruct"  # or "google/medgemma-7b"

# 1. 4-bit Quantization Config (NF4 + Double Quant)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

# 2. Tokenizer & Base Model
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    quantization_config=bnb_config,
    device_map="auto"
)
model = prepare_model_for_kbit_training(model)

# 3. LoRA Configuration
peft_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

# 4. Load & Format Dataset
dataset = load_paired_dataset("sandbox/workspace/labeled_pool/input", "sandbox/workspace/labeled_pool/output")
dataset = dataset.map(lambda batch: {
    "text": [tokenizer.apply_chat_template(msgs, tokenize=False) for msgs in batch["messages"]]
}, batched=True)

# 5. Mask prompt tokens so loss is computed only on the target response
response_template = "<|start_header_id|>assistant<|end_header_id|>\n\n"
collator = DataCollatorForCompletionOnlyLM(response_template=response_template, tokenizer=tokenizer)

# 6. Training Arguments & SFTTrainer
training_args = TrainingArguments(
    output_dir="./qlora_adjudicator",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=8,
    learning_rate=2e-4,
    num_train_epochs=3,
    optim="paged_adamw_8bit",
    bf16=True,
    logging_steps=10,
    report_to="none"
)

trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    peft_config=peft_config,
    dataset_text_field="text",
    max_seq_length=2048,
    data_collator=collator,
    args=training_args
)

trainer.train()
trainer.model.save_pretrained("./qlora_adjudicator/final_adapter")
```

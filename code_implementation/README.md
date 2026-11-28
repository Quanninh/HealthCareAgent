# Clinical Diagnostic Case Extraction & Reasoning Stitching Pipeline

This directory (`code_implementation`) contains the two-stage pipeline for transforming raw published clinical case reports into structured teaching cases (`run_extraction.py`) and stitching their bulleted diagnostic reasoning points into cohesive, present-tense diagnostic reasoning narratives (`run_stitch.py`).

Built exclusively with Python's standard library (`urllib.request`, `json`, `re`, `pathlib`)—**no third-party `pip` packages are required**.

---

## 1. Directory Structure

```text
code_implementation/
├── config.py                        # Central configuration, prompt templates, and tunables
├── api_helpers.py                   # Stateless HTTP client for OpenAI-compatible, Anthropic, and Ollama APIs
├── run_extraction.py                # Stage 1: Extract <case_prompt>, <diagnostic_reasoning>, <final_diagnosis>
├── run_stitch.py                    # Stage 2: Stitch reasoning bullets into <stitched_reasoning> via local Ollama
├── scripts/
│   ├── __init__.py
│   └── fix_extracted_cases.py       # XML tag normalizer, disease synonym mapper, and Rule 7 validator
├── submit/
│   ├── build_soap_inputs.py         # Builds model_inputs_soap_21.jsonl from raw soap/ case JSONs
│   ├── build_soap_inputs_final.py   # Builds model_inputs_soap_21_final.jsonl with clinical_label & 12step diagnosis
│   ├── export_oss_extracted_cases.py# Joins out_oss_Khoa29/*.md with inputs into oss_extracted_cases.jsonl
│   └── export_openrouter_jsonl.py   # Legacy markdown-to-JSONL converter
├── out_oss_Khoa29/                  # Stage 1 extracted markdown outputs (<case_id>.md) + manifest.jsonl (currently contains DUMMY data)
└── out_oss_Khoa29_stitch/           # Stage 2 stitched reasoning outputs (<case_id>.md) + manifest.jsonl
```

---

## 2. Cost & Execution Overview (What Costs Money vs. What Is Free/Offline)

| Script / Command | Network / Provider | Costs Money? | Requirements |
|---|---|---|---|
| `python3 run_extraction.py` *(Live)* | Cloud LLM API (OpenAI, OpenRouter, DeepSeek, Groq, etc.) | **YES (Consumes API Credits)** | Requires a valid `API_KEY` and internet connection (unless pointed to a local endpoint). |
| `python3 run_extraction.py --dry-run` | None (Offline simulation) | **NO ($0 / 0 credits)** | Simulates extraction and checks input parsing without sending requests. |
| `python3 run_stitch.py` *(Live)* | Local Ollama (`http://localhost:11434/api/chat`) | **NO ($0 / 100% Offline)** | Requires Ollama running locally with `llama3.1:latest` pulled. |
| `python3 run_stitch.py --dry-run` | None (Offline simulation) | **NO ($0 / 0 credits)** | Simulates stitching prompt construction offline. |
| `python3 scripts/fix_extracted_cases.py` | None (Local regex repair & validation) | **NO ($0 / 0 credits)** | Offline validation and formatting cleanup of `.md` files. |

---

## 3. Stage 1: Case Extraction (`run_extraction.py`)

### What It Does
Reads raw clinical case reports from `model_inputs_soap_21.jsonl` (each containing `sample_id` and `raw_case_text`) and sends a stateless request (`1 API call = 1 case`) to an LLM using `EXTRACTION_PROMPT` in `config.py`.

Each response is automatically cleaned and validated by `scripts/fix_extracted_cases.py` to ensure it contains:
1. `<case_analysis>...</case_analysis>`: Target diagnosis scope check (21 selected diseases vs. `OUT_OF_SCOPE`), breakpoint planning, and key analytic distinctions.
2. `<case_prompt>...</case_prompt>`: The unspoiled clinical presentation stopping strictly before the diagnosis is revealed.
3. `<diagnostic_reasoning>...</diagnostic_reasoning>`: Numbered reasoning points, each formatted as `Summary | "Direct quote from article"`.
4. `<final_diagnosis>...</final_diagnosis>`: Canonical disease name from the 21 selected diseases (e.g., `aspergillosis`) or `[Exact disease name] -> OUT_OF_SCOPE`.

Valid outputs are saved to `out_oss_Khoa29/<case_id>.md`.

> **⚠️ Dummy Data Notice:** The `out_oss_Khoa29/` folder in this repository currently contains **dummy placeholder data** (`DUMMY_CASE_01__Aspergillosis.md`, `DUMMY_CASE_02__COVID-19.md`, and `manifest.jsonl`) for schema/pipeline demonstration only, not the real 2,949 clinical case outputs. To populate `out_oss_Khoa29/` with real outputs, clear the dummy files and run `run_extraction.py` as shown below.

### ⚠️ Where It Takes Money to Run
- **Live runs of `run_extraction.py` against cloud providers (OpenAI, OpenRouter, DeepSeek, Anthropic, Together, Groq) consume paid API tokens/credits** for every case processed (~1,500–3,500 tokens per case).
- **Built-in Cost Guardrails**:
  1. **Interactive Confirmation**: By default (`CONFIRM_FIRST = True`), `run_extraction.py` displays the target endpoint, model, and number of pending cases and pauses for you to press `[ENTER]` before sending the first live request.
  2. **Dry-Run Mode (`--dry-run`)**: Runs the entire loop offline at zero cost so you can verify case counts and prompt lengths first.
  3. **Limit Flag (`--limit N`)**: Lets you test on a single case (`--limit 1`) before committing to a full batch.
  4. **Non-Retry on Auth/Client Errors**: HTTP `400`, `401`, and `403` errors abort immediately without wasting retries.

### How to Run `run_extraction.py`

```bash
# 1. Export your API credentials
export API_KEY="sk-your-api-key"
export API_BASE="https://openrouter.ai/api/v1"   # or https://api.openai.com/v1
export MODEL="openai/gpt-oss-120b"               # or gpt-4o, deepseek-chat, etc.

# 2. Test with a $0 dry run first
python3 run_extraction.py --dry-run --limit 5

# 3. Test 1 live case to verify credentials and output quality
python3 run_extraction.py --limit 1 --input ../model_inputs_soap_21.jsonl

# 4. Run the full extraction pipeline
python3 run_extraction.py --input ../model_inputs_soap_21.jsonl
```

### Exporting Extracted Cases to JSONL
Once `out_oss_Khoa29/` is populated, you can join the extracted `.md` files with `model_inputs_soap_21_final.jsonl` into `oss_extracted_cases.jsonl`:

```bash
python3 submit/export_oss_extracted_cases.py \
    --inputs ../model_inputs_soap_21_final.jsonl \
    --md-dir out_oss_Khoa29 \
    --output ../oss_extracted_cases.jsonl
```

---

## 4. Stage 2: Diagnostic Reasoning Stitching (`run_stitch.py`)

### What It Does
Reads `case_prompt`, `diagnostic_reasoning` (`reasoning_points`), and `final_diagnosis` from either `oss_extracted_cases.jsonl` or directly from the `out_oss_Khoa29/` folder. It sends each case to a local Ollama model to stitch the numbered reasoning points and verbatim quotes into a single continuous, present-tense, third-person diagnostic narrative wrapped in `<stitched_reasoning>...</stitched_reasoning>`.

Valid stitched narratives are saved to `out_oss_Khoa29_stitch/<case_id>.md`.

### 🖥️ Ollama Setup & Required Model
`run_stitch.py` runs **100% locally and offline for free** via Ollama:
1. **Install & Start Ollama**: Ensure the Ollama app or daemon (`ollama serve`) is running locally on port `11434`.
2. **Pull the Model in Ollama**: By default, `config.py` is configured to use `llama3.1:latest` (Llama 3.1 8B Instruct). Verify it is available in your local Ollama registry:
   ```bash
   # Check installed Ollama models
   ollama list

   # If llama3.1:latest is not listed, pull it once while online:
   ollama pull llama3.1:latest
   ```
   *(If you use a different model tag in Ollama, pass `--model <tag>` or set `export STITCH_MODEL="<tag>"`.)*
3. **Why It Uses Native `/api/chat` with `num_ctx=4096` and `temperature=0.2`**:
   - **No Silent Truncation**: Ollama's default context window is `2048` tokens, and Ollama's `/v1/chat/completions` endpoint can ignore `options.num_ctx`. `run_stitch.py` targets Ollama's native `http://localhost:11434/api/chat` endpoint with `"options": {"num_ctx": 4096, "num_predict": 2048}`, ensuring even the longest case (~3,350 combined input + output tokens) is never truncated.
   - **Grounded Temperature (`0.2`)**: A low temperature prevents the 8B model from inventing outside clinical reasoning while giving it enough flexibility to weave verbatim quotes into smooth present-tense prose.

### How to Run `run_stitch.py`

```bash
# 1. Dry run (offline, 0 requests) to verify input loading
python3 run_stitch.py --dry-run --limit 5 --input out_oss_Khoa29

# 2. Run a single specific case (e.g., the longest case)
python3 run_stitch.py --case-id PMC5437444_01__Histoplasmosis --input out_oss_Khoa29 --no-confirm

# 3. Run all 2,949 cases reading from the out_oss_Khoa29 folder
#    (Use 'caffeinate -i' on macOS so your computer doesn't sleep mid-run)
caffeinate -i python3 run_stitch.py --input out_oss_Khoa29 --no-confirm

# Or run reading from oss_extracted_cases.jsonl in the parent directory:
caffeinate -i python3 run_stitch.py --input ../oss_extracted_cases.jsonl --no-confirm
```

---

## 5. What Happens If You Stop Execution? (Crash Recovery & Resumption)

Both `run_extraction.py` and `run_stitch.py` are designed to be **interrupt-safe and idempotent**:

1. **Stopping Anytime (`Ctrl+C`, Sleep, Power Loss, or Network Drop)**:
   - Each case is processed as an independent, stateless request (`1 request = 1 case`).
   - Immediately after each case finishes and validates, the script writes `<case_id>.md` to disk and flushes a line to `manifest.jsonl` (`out_oss_Khoa29/manifest.jsonl` or `out_oss_Khoa29_stitch/manifest.jsonl`).
   - If you press `Ctrl+C`, the script catches `KeyboardInterrupt`, prints `[ABORTED] Process interrupted by user. Manifest saved up to last case.`, and exits cleanly without corrupting any files.

2. **Resuming Execution**:
   - Simply **re-run the exact same command**.
   - On startup, the script reads `manifest.jsonl` and checks the output directory:
     - Any case marked `"status": "done"` in `manifest.jsonl` is immediately skipped (`[SKIP] <case_id> (already marked done)`).
     - Any case whose `<case_id>.md` file already exists on disk is also skipped and never overwritten (`[SKIP] <case_id> (file exists)`).
   - Only cases that were not yet processed—or cases that previously had `"status": "failed"`—will be sent to the model.

3. **Inspecting Failures**:
   - If a model reply fails XML validation (e.g., missing closing tag), the raw unparsed response is saved as `<case_id>.raw.txt` in the output directory, and the error reason is recorded in `manifest.jsonl` with `"status": "failed"`.
   - Because `<case_id>.md` is not written for failed cases, re-running the script will automatically retry those failed cases.

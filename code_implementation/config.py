"""Configuration and tunables for the Clinical Diagnostic Case Extraction Pipeline."""

from pathlib import Path
import os
import re

# ==========================================
# PATHS
# ==========================================
BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / os.environ.get("INPUT_FILE", "model_inputs_soap_21.jsonl")
OUTPUT_DIR = BASE_DIR / os.environ.get("OUTPUT_DIR", "out_oss_Khoa29")
MANIFEST_FILE = OUTPUT_DIR / "manifest.jsonl"
REASONING_LOG_DIR = BASE_DIR / os.environ.get("REASONING_LOG_DIR", "logs_internal_reasoning")

# ==========================================
# LLM API CONFIGURATION
# ==========================================
# API key resolved from environment variables
API_KEY = (os.environ.get("API_KEY") or os.environ.get("OPENAI_API_KEY") or "").strip()

# Base URL for API calls (OpenAI-compatible)
API_BASE = (os.environ.get("API_BASE") or os.environ.get("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")

# Target Model identifier (e.g. "gpt-4o", "llama-3.3-70b", "claude-3-5-sonnet")
API_MODEL = (os.environ.get("MODEL") or os.environ.get("OPENAI_MODEL") or "gpt-4o").strip()

# Request temperature (None uses provider default)
TEMPERATURE = None

# Max retries on transient errors (HTTP 429, 5xx, timeouts)
MAX_RETRIES = int(os.environ.get("MAX_RETRIES", "3"))

# Exponential backoff base factor (seconds)
RETRY_BACKOFF_SEC = float(os.environ.get("RETRY_BACKOFF_SEC", "2.0"))

# ==========================================
# SAFETY & PACING TUNABLES
# ==========================================
# If True, simulate actions without sending API requests.
DRY_RUN = False

# If True, pause and wait for the user to confirm before sending the first live request.
CONFIRM_FIRST = True

# Pacing delay range between API requests (in seconds) to avoid rate limit spikes.
MIN_DELAY_SEC = 3.0
MAX_DELAY_SEC = 8.0

# Timeout waiting for LLM API response (in seconds).
TIMEOUT_SEC = 120.0

# ==========================================
# SELECTED DISEASES LIST
# ==========================================
SELECTED_DISEASES = [
    "aspergillosis",
    "brucellosis",
    "cholera",
    "covid_19",
    "cryptococcosis",
    "cytomegalovirus",
    "dengue",
    "ebola_filovirus",
    "echinococcosis",
    "histoplasmosis",
    "hiv_aids",
    "leishmaniasis",
    "leprosy",
    "malaria",
    "neurocysticercosis",
    "nocardiosis",
    "pneumocystis",
    "rabies",
    "syphilis",
    "tuberculosis",
    "yellow_fever",
]

# ==========================================
# VALIDATION TAGS
# ==========================================
REQUIRED_XML_TAGS = [
    "<case_prompt>",
    "</case_prompt>",
    "<diagnostic_reasoning>",
    "</diagnostic_reasoning>",
    "<final_diagnosis>",
    "</final_diagnosis>",
]

# ==========================================
# EXTRACTION PROMPT TEMPLATE
# ==========================================
EXTRACTION_PROMPT = """You are an expert clinician-educator.
Your job is to transform a published case report into a teaching diagnostic case that medical students can work through step-by-step.
In terms of style, think of NEJM's Clinicopathologic Conferences ("Case Records of the Mass General Hospital") as a template.

RULES (Read Carefully—No Exceptions)

1. Source Fidelity - Extract facts *only* from the supplied case report.
- Do NOT invent, embellish, or "smooth out" missing data.
- Paraphrase narrative prose into concise bullets where helpful, but never add new facts.

2. Structure the Output in Four Visible XML Blocks
   <case_analysis> -> <case_prompt> -> <diagnostic_reasoning> -> <final_diagnosis>
   IMPORTANT: Even after completing your internal chain-of-thought reasoning, you MUST explicitly output all four XML tags in your final response.

3. Use the XML Tags Exactly as Shown
- <case_analysis>...</case_analysis> - your visible analytic notes and breakpoint planning (not shown to students).
- <case_prompt>...</case_prompt> - the clinical presentation (symptoms, vitals, exam, labs/imaging) given *before* the target diagnosis is revealed.
- <diagnostic_reasoning>...</diagnostic_reasoning> - numbered bullet reasons, each built as a full sentence followed by a direct quote.
- <final_diagnosis>...</final_diagnosis> - must strictly follow the classification rules in Rule 7.

4. What Goes Inside <case_analysis>
   1. Target Diagnosis Identification: Check if the patient has any disease from the 21 SELECTED diseases list (Rule 7).
      - If YES, and the paper has sufficient clinical/lab details to deduce that SELECTED disease, make that SELECTED disease (plus any simultaneous SELECTED co-infections) the primary target diagnosis.
      - If the SELECTED disease is only mentioned as already-diagnosed past medical history without a diagnostic workup, OR if the patient has NO diseases from the 21 SELECTED list, the target diagnosis is the paper's main OUT_OF_SCOPE diagnosis.
   2. Ideal Breakpoint: Choose the exact cutoff point in the case presentation so that the reader has enough symptoms, exam findings, and initial labs/imaging to deduce the Target Diagnosis, with ZERO spoilers (never state the Target Diagnosis inside <case_prompt>).
   3. Author's Analytic Distinctions: How did the authors support the Target Diagnosis and rule out competing differentials?

5. What Goes Inside <case_prompt>
- Present *only* the facts known *before* the Target Diagnosis was confirmed: chief complaint, HPI, vitals, physical exam, and initial lab/imaging investigations up to your chosen breakpoint.
- Do not include references to Figure 1, Table 1, etc. directly. Summarize any imaging findings from what is given in the text.
- Present the case in the chronological order presented in the case report.
- CRITICAL: Omit any wording, serology result, or clinical statement that directly names or gives away the <final_diagnosis>.
- Present this as closely as possible to the style in which the case report is written.

6. What Goes Inside <diagnostic_reasoning>
- Numbered list (1, 2, 3, ...).
- Include every alternative diagnosis mentioned in the article, along with reasons why it was considered and excluded, plus the key clinical/lab reasoning that led to the <final_diagnosis>.
- Each entry: *concise summary of reason* | "direct quote from article".
- You can use ellipses (...) to shorten the quote if there are irrelevant details.
- Quotes must justify why one possibility rose or fell in likelihood.

7. What Goes Inside <final_diagnosis>
   You must classify the target diagnosis being solved by <case_prompt> using the following 21 SELECTED diseases list:
   [aspergillosis, brucellosis, cholera, covid_19, cryptococcosis, cytomegalovirus, dengue, ebola_filovirus, echinococcosis, histoplasmosis, hiv_aids, leishmaniasis, leprosy, malaria, neurocysticercosis, nocardiosis, pneumocystis, rabies, syphilis, tuberculosis, yellow_fever]

   Follow these strict rules to format the output:
- Rule 7.1: If the diagnosis being solved is ONLY from the SELECTED diseases list, output the exact name(s) from the list (e.g., brucellosis).
- Rule 7.2: If the patient has BOTH a SELECTED disease and an OUT_OF_SCOPE disease (and your <case_prompt> breakpoint is set before the SELECTED disease is revealed so it can be diagnosed), output ONLY the SELECTED disease(s). Do not mention the OUT_OF_SCOPE disease here.
- Rule 7.3: If the patient has ONLY OUT_OF_SCOPE diseases (or if a SELECTED disease was already given away in the past medical history and cannot be cut out), format the active mystery diagnosis exactly as: [Exact disease name(s)] -> OUT_OF_SCOPE (e.g., ANCA-associated vasculitis -> OUT_OF_SCOPE).
- Rule 7.4: No adjectives, punctuation, or explanatory text outside of the allowed formats.
- Rule 7.5: If a disease on the list appears in the text under a synonym (e.g., SARS-CoV-2 for covid_19, PJP/PCP for pneumocystis, Hansen's disease for leprosy, visceral leishmaniasis for leishmaniasis), output the exact name from the list (e.g., covid_19, pneumocystis, leprosy, leishmaniasis).

OUTPUT TEMPLATE (copy exactly)

<case_analysis>
1. [Target Diagnosis & Scope Check (21 SELECTED vs OUT_OF_SCOPE)]
2. [Best breakpoint of case report, what to include and what to exclude so <final_diagnosis> is not spoiled]
3. [Key analytic distinctions between competing diagnoses (taken from case report)]
</case_analysis>

<case_prompt>
[Your case presentation text, faithful to the report and stopping strictly at the breakpoint]
</case_prompt>

<diagnostic_reasoning>
1. Summarized reasoning | "Direct quote from article..."
2. Summarized reasoning | "Direct quote from article..."
</diagnostic_reasoning>

<final_diagnosis>
[Follow Rule 7 exactly here. E.g., "brucellosis" OR "ANCA-associated vasculitis -> OUT_OF_SCOPE"]
</final_diagnosis>"""


def format_payload(raw_case_text: str) -> str:
    """Format the clinical case report as the user prompt message."""
    clean_text = raw_case_text.strip()
    return f"<case_report>\n{clean_text}\n</case_report>"


# ==========================================
# STITCHING PIPELINE CONFIGURATION
# ==========================================
STITCH_INPUT_JSONL = BASE_DIR / os.environ.get("STITCH_INPUT_JSONL", "oss_extracted_cases.jsonl")
STITCH_INPUT_DIR = BASE_DIR / os.environ.get("STITCH_INPUT_DIR", "out_oss_Khoa29")
STITCH_OUTPUT_DIR = BASE_DIR / os.environ.get("STITCH_OUTPUT_DIR", "out_oss_Khoa29_stitch")
STITCH_MANIFEST_FILE = STITCH_OUTPUT_DIR / "manifest.jsonl"
STITCH_API_BASE = (os.environ.get("STITCH_API_BASE") or os.environ.get("OLLAMA_API_BASE") or "http://localhost:11434/api/chat").rstrip("/")
STITCH_MODEL = (os.environ.get("STITCH_MODEL") or "llama3.1:latest").strip()

# Low temperature (0.2) prevents hallucinating new reasoning while allowing smooth narrative transitions
STITCH_TEMPERATURE = float(os.environ.get("STITCH_TEMPERATURE", "0.2"))

# Context window and generation cap:
# Ollama's default num_ctx is 2048 tokens, which silently truncates ~23% of cases (max case is ~3,350 in+out tokens).
# Setting num_ctx=4096 and max_tokens=2048 via native /api/chat options guarantees 0% truncation across all 2,949 cases.
STITCH_NUM_CTX = int(os.environ.get("STITCH_NUM_CTX", "4096"))
STITCH_MAX_TOKENS = int(os.environ.get("STITCH_MAX_TOKENS", "2048"))
STITCH_TIMEOUT_SEC = float(os.environ.get("STITCH_TIMEOUT_SEC", "600.0"))

STITCH_REQUIRED_XML_TAGS = [
    "<stitched_reasoning>",
    "</stitched_reasoning>",
]

STITCH_PROMPT_TEMPLATE = """Your job is to convert a list of diagnostic reasoning points into a cohesive diagnostic reasoning narrative.

INPUTS
* CASE_PROMPT:
{case_prompt}

* REASONING_POINTS (in the order they were generated):
{reasoning_points}

* FINAL_DIAGNOSIS:
{final_diagnosis}

TASK
Write a single, cohesive reasoning trace by stitching together all the REASONING_POINTS.
The REASONING_POINTS are given as an enumerated list, where each point is a brief summary of a particular reasoning point, followed by a quote from the full case report that supports the reasoning point.
This should be written from the perspective of a reasoning trace that an LLM chatbot would write in response to a case presentation.
Do not use the past-tense nature of REASONING_POINTS, instead make them present-tense and third-person as you are considering each potential diagnosis.

OUTPUT
Only use the reasoning from the REASONING_POINTS to come up with the final diagnosis.
Use ALL of the REASONING_POINTS in producing the reasoning trace.
Do not include your own reasoning over the case, only use the reasoning points provided.
Try to incorporate as much of the quotes as possible into the reasoning trace, using word-for-word copies when possible (don't actually put quotation marks in the reasoning trace).
You may rephrase the reasoning points, but only for style and tone, not for substance.
No headings, no bullets, no numbered lists - just a continuous explanatory narrative.

Place this between the tags <stitched_reasoning> and </stitched_reasoning>"""


def format_stitch_prompt(case_prompt: str, reasoning_points: str, final_diagnosis: str) -> str:
    """Format the stitching prompt with the extracted case components."""
    return STITCH_PROMPT_TEMPLATE.format(
        case_prompt=case_prompt.strip(),
        reasoning_points=reasoning_points.strip(),
        final_diagnosis=final_diagnosis.strip(),
    )


def sanitize_case_id(sample_id: str) -> str:
    """Convert sample_id (e.g. 'PMC8639279_01::Brucellosis') into a safe filename stem."""
    # Replace ::, /, \, and whitespace with double underscores or underscores
    clean = re.sub(r"::", "__", sample_id)
    clean = re.sub(r'[\\/*?:"<>| \t\n\r]+', "_", clean)
    return clean.strip("._")


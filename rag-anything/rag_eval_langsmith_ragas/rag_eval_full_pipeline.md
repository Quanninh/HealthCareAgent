# Antigravity Task Prompt: End-to-End RAG Evaluation Pipeline

**Role & Goal:**
You are an expert Machine Learning Engineer. I need you to build a robust evaluation pipeline for a Medical RAG system. You will write a script that samples 10 clinical cases, uploads them to LangSmith, and runs a complete Ragas evaluation covering both Retrieval and Generation. The generator is a local Ollama model, and the judge is Google Gemini.

Please generate the complete, runnable Python script based on the exact specifications below.

### 1. Data Processing & Sampling
- Import the test dataset from `@evaluate_retrieval.py` (e.g., `test_df`, `held_out_cases`, or the equivalent DataFrame).
- Set a random seed and extract exactly 10 cases.
- Format the input query dynamically: `"Here is the clinical case description: {text}. What is the most possible disease that this patient may have?"`
- Map the target output to the ground-truth disease name (e.g., `"Tinea Corporis"`).

### 2. LangSmith Integration
- Initialize the `langsmith.Client`.
- Programmatically create a new dataset named `"Diagnostic RAG Eval - 10 Cases"`.
- Upload the 10 sampled cases to this LangSmith dataset (storing `question` in inputs and `ground_truth` in outputs).
- Ensure tracing is enabled via standard LangSmith environment variables (`LANGCHAIN_TRACING_V2`, `LANGCHAIN_API_KEY`).

### 3. Model & Prompt Configuration
- **Generator (Ollama):** Initialize `ChatOllama(model="qwen2.5:7b")` from LangChain.
  - **System Prompt:** `"You are an expert diagnostic AI. Based on the provided clinical context, output exactly ONE disease name. Do not include any explanations, greetings, or punctuation beyond the disease name."`
- **Judge LLM (Gemini):** Initialize `ChatGoogleGenerativeAI(model="gemini-1.5-pro")`. Expose `GOOGLE_API_KEY` or `GEMINI_API_KEY` cleanly via `os.environ` or `.env` loads.
- **Judge Embeddings (Gemini):** Initialize `GoogleGenerativeAIEmbeddings(model="models/embedding-001")`.

### 4. Ragas Wrappers (Ragas >= 0.2 Standard)
Ragas now requires explicit wrapping of LangChain models. You must wrap the Gemini models before passing them to the metrics:
```python
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

judge_llm = LangchainLLMWrapper(ChatGoogleGenerativeAI(model="gemini-1.5-pro"))
judge_embeddings = LangchainEmbeddingsWrapper(GoogleGenerativeAIEmbeddings(model="models/embedding-001"))

Evaluation Pillars (Generation + Retrieval)
Initialize and configure the 4 core Ragas metrics to evaluate both system halves:

Faithfulness (Generation Groundedness): Ensures the generated disease is explicitly supported by the retrieved context.

Answer Relevancy (Generation Relevance): Ensures the AI actually answered the diagnostic question.

Context Precision (Retrieval Relevance): Ensures the most relevant clinical text chunks were ranked at the top.

Context Recall (Retrieval Comprehensiveness): Ensures all necessary facts to diagnose the disease were successfully retrieved.

Note: Assign the wrapped judge_llm and judge_embeddings to these metrics.

6. Execution Loop Structure
Design the evaluation workflow to execute as follows:

Fetch the 10 examples from the LangSmith dataset.

For each example, execute the RAG retrieval step to fetch contexts.

Pass the contexts and the question to the Ollama generator to get the answer.

Format the results into a Ragas SingleTurnSample or HuggingFace Dataset format containing: question, answer, contexts, and ground_truth.

Run the Ragas evaluate() function on the dataset.

Push the metric scores back to LangSmith (using langsmith.evaluate with custom evaluators, or logging the Ragas output directly to the LangSmith trace).

Make the code modular, fully typed, and production-ready. Ensure placeholders for API keys are clearly marked. Do not omit necessary imports.

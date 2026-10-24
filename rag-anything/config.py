"""
Configuration module for MultiCaRe to RAG-Anything Ingestion Pipeline.
Defines dataset paths, 15 target tropical and infectious diseases with regex patterns,
and local AI model connection configurations.
"""

import os
import re
from pathlib import Path

# ==============================================================================
# 1. Directory and File Paths
# ==============================================================================
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "medical_datasets" / "whole_multicare_dataset"
IMAGES_BASE_DIR = DATA_DIR

OUTPUT_DIR = BASE_DIR / "output"
PAYLOADS_DIR = OUTPUT_DIR / "payloads"

# Ensure output directories exist
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
PAYLOADS_DIR.mkdir(parents=True, exist_ok=True)

METADATA_PARQUET = DATA_DIR / "metadata.parquet"
ABSTRACTS_PARQUET = DATA_DIR / "abstracts.parquet"
CASES_PARQUET = DATA_DIR / "cases.parquet"
CAPTIONS_CSV = DATA_DIR / "captions_and_labels.csv"
DATA_DICTIONARY_CSV = DATA_DIR / "data_dictionary.csv"

# ==============================================================================
# 2. Targeted Diseases & Comprehensive Synonym Regex Patterns
# ==============================================================================
# 15 specific tropical and infectious diseases with clinical synonyms,
# pathogen names, and spelling variations (British/American).
TARGET_DISEASE_PATTERNS = {
    "Tuberculosis": r"\b(tuberculosis|mycobacterium\s+tuberculosis|tuberculous|tb|miliary\s+tb|pulmonary\s+tb)\b",
    "Melioidosis": r"\b(melioidosis|burkholderia\s+pseudomallei|whitmore'?s\s+disease)\b",
    "Amoebiasis": r"\b(amoebiasis|amebiasis|entamoeba\s+histolytica|amebic\s+dysentery|amoebic\s+liver\s+abscess|amoebic|amebic)\b",
    "Neurocysticercosis": r"\b(neurocysticercosis|cysticercosis|taenia\s+solium|pork\s+tapeworm)\b",
    "Echinococcosis": r"\b(echinococcosis|echinococcus|hydatid\s+disease|hydatid\s+cyst|alveolar\s+echinococcosis)\b",
    "Schistosomiasis": r"\b(schistosomiasis|schistosoma|bilharzia|bilharziasis|snail\s+fever)\b",
    "Leprosy": r"\b(leprosy|mycobacterium\s+leprae|hansen'?s\s+disease|hansens\s+disease|lepromatous)\b",
    "Leishmaniasis": r"\b(leishmaniasis|leishmania|kala-?azar|black\s+fever|cutaneous\s+leishmaniasis|visceral\s+leishmaniasis)\b",
    "Cryptococcosis": r"\b(cryptococcosis|cryptococcus|cryptococcal|cryptococcus\s+neoformans)\b",
    "Histoplasmosis": r"\b(histoplasmosis|histoplasma|histoplasma\s+capsulatum|darling'?s\s+disease)\b",
    "Paragonimiasis": r"\b(paragonimiasis|paragonimus|lung\s+fluke|paragonimus\s+westermani)\b",
    "Lymphatic Filariasis": r"\b(lymphatic\s+filariasis|filariasis|elephantiasis|wuchereria\s+bancrofti|brugia\s+malayi|microfilaria)\b",
    "Malaria": r"\b(malaria|plasmodium\s+falciparum|plasmodium\s+vivax|plasmodium\s+ovale|plasmodium\s+malariae|plasmodium)\b",
    "Covid19": r"\b(covid-?19|sars-cov-2|coronavirus\s+disease\s+2019|novel\s+coronavirus)\b",
    "Dengue": r"\b(dengue|dengue\s+fever|severe\s+dengue|dengue\s+shock\s+syndrome|dengue\s+hemorrhagic\s+fever|dengue\s+haemorrhagic\s+fever)\b",
}

# Compile unified regex pattern for high-performance vectorized matching
COMPILED_DISEASE_REGEX = {
    name: re.compile(pattern, re.IGNORECASE)
    for name, pattern in TARGET_DISEASE_PATTERNS.items()
}

COMBINED_REGEX_PATTERN = "|".join(
    f"(?P<{re.sub(r'[^a-zA-Z0-9]', '_', name)}>{pattern})"
    for name, pattern in TARGET_DISEASE_PATTERNS.items()
)
COMPILED_COMBINED_REGEX = re.compile(COMBINED_REGEX_PATTERN, re.IGNORECASE)

# ==============================================================================
# 3. Local Free AI Model Configurations (Zero Cloud Cost)
# ==============================================================================
# Local OpenAI-compatible server endpoint (e.g., Ollama or llama-server)
LOCAL_LLM_BASE_URL = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:11434/v1")
LOCAL_LLM_API_KEY = os.getenv("LOCAL_LLM_API_KEY", "ollama")

# User's model: medgemma-1.5-4b-it-GGUF: hf.co/unsloth/medgemma-1.5-4b-it-GGUF:UD-Q4_K_XL on my machine
DEFAULT_LLM_MODEL = os.getenv("DEFAULT_LLM_MODEL", "qwen2.5:7b")

# Recommended local free vision model (Ollama or vLLM)
DEFAULT_VISION_MODEL = os.getenv("DEFAULT_VISION_MODEL", "qwen2.5vl:7b")

# Recommended local free embeddings (HuggingFace sentence-transformers or Ollama)
DEFAULT_EMBEDDING_MODEL = os.getenv("DEFAULT_EMBEDDING_MODEL", "bge-m3:latest")
DEFAULT_EMBEDDING_DIM = int(os.getenv("DEFAULT_EMBEDDING_DIM", "1024"))

# RAG-Anything Storage Directory
RAG_STORAGE_DIR = BASE_DIR / "rag_storage"


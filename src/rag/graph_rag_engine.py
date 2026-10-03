"""Independent, modular GraphRAG engine for Clinical Diagnosis using MedGemma.
"""
import sys
import os
import re
import json
from typing import Dict, Any, Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from configs.prompts import CLINICAL_SYSTEM_PROMPT, GRAPH_RAG_DIAGNOSIS_PROMPT
from src.graph.neo4j_client import Neo4jClient
from src.rag.graph_retriever import GraphRetriever
from src.models.medgemma_loader import MedGemmaEngine


class GraphRAGEngine:
    """End-to-end GraphRAG pipeline for clinical differential diagnosis."""

    def __init__(
        self,
        neo4j_client: Neo4jClient,
        model_engine: MedGemmaEngine,
        top_k_candidates: int = 5
    ):
        self.client = neo4j_client
        self.model_engine = model_engine
        self.retriever = GraphRetriever(neo4j_client=self.client)
        self.top_k_candidates = top_k_candidates

    def _parse_model_output(self, raw_output: str) -> Dict[str, Any]:
        """Extracts JSON object from model's generation with fallback cleaning."""
        # Try finding markdown code block
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw_output, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            # Fallback: look for outermost curly braces
            match_brace = re.search(r"(\{.*\})", raw_output, re.DOTALL)
            json_str = match_brace.group(1) if match_brace else raw_output

        try:
            return json.loads(json_str)
        except Exception:
            return {
                "primary_diagnosis": "Unspecified",
                "differential_diagnoses": [],
                "confidence_scores": [],
                "clinical_rationale": raw_output
            }

    def diagnose(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """Executes full GraphRAG pipeline for a given patient case:

        1. Retrieves knowledge graph evidence.
        2. Constructs grounded clinical prompt.
        3. Executes MedGemma inference.
        4. Returns standardized diagnosis output dictionary.
        """
        case_id = case.get("case_id", "UNKNOWN")
        age = case.get("age", "Unknown")
        gender = case.get("gender", "Unknown")
        narrative = case.get("case_presentation", "")
        symptoms = case.get("extracted_symptoms", [])
        labs = case.get("extracted_labs", [])

        # 1. Retrieve Knowledge Graph Subgraph
        linearized_evidence, raw_graph_records = self.retriever.retrieve_subgraph(
            symptoms=symptoms,
            labs=labs,
            top_k=self.top_k_candidates
        )
        retrieved_disease_candidates = [r["disease"] for r in raw_graph_records]

        # 2. Formulate Prompt
        prompt = GRAPH_RAG_DIAGNOSIS_PROMPT.format(
            age=age,
            gender=gender,
            case_presentation=narrative,
            graph_evidence=linearized_evidence
        )

        # 3. Model Generation
        raw_generation = self.model_engine.generate(
            prompt=prompt,
            system_prompt=CLINICAL_SYSTEM_PROMPT
        )

        # 4. Parse Structured Diagnostic Output
        parsed_diagnosis = self._parse_model_output(raw_generation)

        # Standardized output interface for benchmarking
        return {
            "case_id": case_id,
            "primary_diagnosis": parsed_diagnosis.get("primary_diagnosis", "Unknown"),
            "differential_diagnoses": parsed_diagnosis.get("differential_diagnoses", []),
            "confidence_scores": parsed_diagnosis.get("confidence_scores", []),
            "clinical_rationale": parsed_diagnosis.get("clinical_rationale", ""),
            "retrieved_subgraph": linearized_evidence,
            "retrieved_graph_candidates": retrieved_disease_candidates,
            "raw_generation": raw_generation
        }

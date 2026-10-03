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
from src.graphrag.graph_retriever import GraphRetriever
from src.models.medgemma_loader import MedGemmaEngine


class GraphRAGEngine:
    """End-to-end GraphRAG pipeline for clinical differential diagnosis."""

    def __init__(
        self,
        neo4j_client: Neo4jClient,
        model_engine: Any,
        top_k_candidates: int = 5,
        entity_extractor: Optional[Any] = None
    ):
        self.client = neo4j_client
        self.model_engine = model_engine
        self.retriever = GraphRetriever(neo4j_client=self.client)
        self.top_k_candidates = top_k_candidates
        self.entity_extractor = entity_extractor

    def _parse_model_output(self, raw_output: str) -> Dict[str, Any]:
        """Extracts JSON object from model's generation with resilient multi-tier fallback."""
        clean_text = raw_output.strip()
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", clean_text, re.DOTALL)
        if match:
            json_str = match.group(1)
        else:
            match_brace = re.search(r"(\{.*\})", clean_text, re.DOTALL)
            json_str = match_brace.group(1) if match_brace else clean_text

        try:
            return json.loads(json_str)
        except Exception:
            pass

        # Resilient Tier 2: Regex extraction to salvage truncated or broken JSON
        primary_dx = "Unspecified"
        differentials = []
        confidence_scores = []
        rationale = clean_text

        m_prim = re.search(r'"primary_diagnosis":\s*"([^"]+)"', clean_text)
        if m_prim:
            primary_dx = m_prim.group(1).strip()

        m_diff = re.search(r'"differential_diagnoses":\s*\[(.*?)\]', clean_text, re.DOTALL)
        if m_diff:
            items = re.findall(r'"([^"]+)"', m_diff.group(1))
            differentials = [it.strip() for it in items if it.strip()]

        m_conf = re.search(r'"confidence_scores":\s*\[(.*?)\]', clean_text, re.DOTALL)
        if m_conf:
            scores = re.findall(r'([0-9]*\.?[0-9]+)', m_conf.group(1))
            confidence_scores = [float(s) for s in scores if s]

        m_rat = re.search(r'"clinical_rationale":\s*"([^"]*)', clean_text)
        if m_rat:
            rationale = m_rat.group(1).strip()

        return {
            "primary_diagnosis": primary_dx,
            "differential_diagnoses": differentials,
            "confidence_scores": confidence_scores,
            "clinical_rationale": rationale
        }

    def diagnose(self, case: Dict[str, Any]) -> Dict[str, Any]:
        """Executes full GraphRAG pipeline for a given patient case:

        1. Extracts entities via LLM if available, or uses pre-extracted fields.
        2. Retrieves knowledge graph evidence.
        3. Constructs grounded clinical prompt.
        4. Executes model inference.
        5. Returns standardized diagnosis output dictionary.
        """
        case_id = case.get("case_id", "UNKNOWN")
        age = case.get("age", "Unknown")
        gender = case.get("gender", "Unknown")
        narrative = case.get("case_presentation", "")
        symptoms = case.get("extracted_symptoms", [])
        labs = case.get("extracted_labs", [])

        # Role A: Semantic extraction via LLM if enabled and available
        if self.entity_extractor is not None and hasattr(self.entity_extractor, "extract_entities"):
            extracted = self.entity_extractor.extract_entities(case_presentation=narrative)
            if extracted.get("symptoms"):
                symptoms = extracted["symptoms"]
            if extracted.get("labs"):
                labs = extracted["labs"]

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

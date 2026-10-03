"""MMGraphRAG Engine for Multimodal Clinical Diagnosis using MedGemma and Neo4j.
"""

import sys
import os
import re
import json
from typing import Dict, Any, Optional

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from configs.prompts import CLINICAL_SYSTEM_PROMPT
from src.graph.neo4j_client import Neo4jClient
from src.models.medgemma_loader import MedGemmaEngine
from src.mmgraphrag.image2graph import Image2GraphExtractor
from src.mmgraphrag.mm_graph_retriever import MMGraphRetriever

MM_GRAPH_RAG_DIAGNOSIS_PROMPT = """You are evaluating a patient case using a unified Multimodal Knowledge Graph.
Review the patient clinical narrative, diagnostic imaging findings, and the retrieved cross-modal knowledge graph evidence below.

=== PATIENT CLINICAL PRESENTATION ===
Age: {age}
Gender: {gender}
Clinical Narrative:
{case_presentation}

=== DIAGNOSTIC IMAGING & VISUAL FINDINGS ===
{visual_findings_summary}

=== RETRIEVED MULTIMODAL KNOWLEDGE GRAPH EVIDENCE ===
{graph_evidence}

=== INSTRUCTIONS ===
Synthesize the clinical presentation, visual radiology/pathology findings, and knowledge graph evidence:
1. Identify the primary diagnosis.
2. Provide a ranked list of differential diagnoses (up to 3-5 candidates).
3. Assign a confidence score (0.0 to 1.0) for each differential diagnosis candidate.
4. Explain your clinical diagnostic rationale concisely (2-3 sentences max), highlighting how the patient's symptoms AND visual imaging findings align with the multimodal knowledge graph evidence.

Respond strictly in valid JSON format matching the following schema:
```json
{{
  "primary_diagnosis": "<Exact disease name>",
  "differential_diagnoses": [
    "<Candidate 1>",
    "<Candidate 2>",
    "<Candidate 3>"
  ],
  "confidence_scores": [
    0.85,
    0.10,
    0.05
  ],
  "clinical_rationale": "<Concise 2-3 sentence diagnostic reasoning grounded in presentation, visual pathology/radiology, and graph evidence>"
}}
```
"""


class MMGraphRAGEngine:
    """End-to-end Multimodal GraphRAG pipeline for clinical differential diagnosis."""

    def __init__(
        self,
        neo4j_client: Neo4jClient,
        model_engine: Any,
        top_k_candidates: int = 5,
        entity_extractor: Optional[Any] = None
    ):
        self.client = neo4j_client
        self.model_engine = model_engine
        self.retriever = MMGraphRetriever(neo4j_client=self.client)
        self.i2g = Image2GraphExtractor()
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
        """Executes full MMGraphRAG pipeline for a multimodal patient case."""
        case_id = case.get("case_id", "UNKNOWN")
        age = case.get("age", "Unknown")
        gender = case.get("gender", "Unknown")
        narrative = case.get("case_presentation", "")
        symptoms = case.get("extracted_symptoms", [])
        labs = case.get("extracted_labs", [])
        images = case.get("images", [])

        # Role A: Semantic extraction via LLM if available
        if self.entity_extractor is not None and hasattr(self.entity_extractor, "extract_entities"):
            extracted = self.entity_extractor.extract_entities(case_presentation=narrative)
            if extracted.get("symptoms"):
                symptoms = extracted["symptoms"]
            if extracted.get("labs"):
                labs = extracted["labs"]

        # 1. Process diagnostic images with Image2Graph
        extracted_visual_entities = []
        visual_summaries = []
        for idx, img in enumerate(images, start=1):
            sg = self.i2g.extract_from_image_record(img)
            extracted_visual_entities.extend(sg["visual_entities"])
            caption = sg["caption"][:150]
            visual_summaries.append(f"Image {idx} ({sg['modality']}, {sg['region']}): {caption}")

        extracted_visual_entities = list(set(extracted_visual_entities))
        visual_findings_text = "\n".join(visual_summaries) if visual_summaries else "No diagnostic images available for this case."

        # 2. Retrieve Multimodal Subgraph from Neo4j
        linearized_evidence, raw_graph_records = self.retriever.retrieve_multimodal_subgraph(
            symptoms=symptoms,
            labs=labs,
            visual_entities=extracted_visual_entities,
            top_k=self.top_k_candidates
        )
        retrieved_disease_candidates = [r["disease"] for r in raw_graph_records]

        # 3. Formulate Multimodal Clinical Prompt
        prompt = MM_GRAPH_RAG_DIAGNOSIS_PROMPT.format(
            age=age,
            gender=gender,
            case_presentation=narrative,
            visual_findings_summary=visual_findings_text,
            graph_evidence=linearized_evidence
        )

        # 4. MedGemma Generation
        raw_generation = self.model_engine.generate(
            prompt=prompt,
            system_prompt=CLINICAL_SYSTEM_PROMPT
        )

        # 5. Parse Output
        parsed_diagnosis = self._parse_model_output(raw_generation)

        return {
            "case_id": case_id,
            "primary_diagnosis": parsed_diagnosis.get("primary_diagnosis", "Unknown"),
            "differential_diagnoses": parsed_diagnosis.get("differential_diagnoses", []),
            "confidence_scores": parsed_diagnosis.get("confidence_scores", []),
            "clinical_rationale": parsed_diagnosis.get("clinical_rationale", ""),
            "retrieved_subgraph": linearized_evidence,
            "retrieved_graph_candidates": retrieved_disease_candidates,
            "extracted_visual_entities": extracted_visual_entities,
            "raw_generation": raw_generation
        }

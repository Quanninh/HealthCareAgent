"""Multimodal Graph Retriever for querying unified cross-modal subgraphs in Neo4j.
"""

from typing import List, Dict, Any, Tuple
from src.graph.neo4j_client import Neo4jClient


class MMGraphRetriever:
    """Retrieves and ranks multimodal subgraphs (text entities + visual entities + image nodes)."""

    def __init__(self, neo4j_client: Neo4jClient):
        self.client = neo4j_client

    def retrieve_multimodal_subgraph(
        self,
        symptoms: List[str],
        labs: List[str],
        visual_entities: List[str],
        top_k: int = 5
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Queries Neo4j across both textual and visual modalities, returning linearized evidence."""
        if not symptoms and not labs and not visual_entities:
            return "No matching clinical or visual entities detected to query multimodal knowledge graph.", []

        cypher = """
        MATCH (d:Disease)
        OPTIONAL MATCH (d)-[r1:PRESENTS_WITH]->(s:Symptom)
        WHERE s.name IN $symptoms
        OPTIONAL MATCH (d)-[r2:CONFIRMED_BY]->(l:LabFinding)
        WHERE l.name IN $labs
        OPTIONAL MATCH (d)-[r3:EVIDENCED_BY]->(v:VisualEntity)
        WHERE v.name IN $visual_entities
        OPTIONAL MATCH (img:ImageNode)-[:OBSERVES]->(v)
        WITH d,
             count(DISTINCT s) AS matched_symptoms_count,
             collect(DISTINCT s.name) AS matched_symptoms,
             count(DISTINCT l) AS matched_labs_count,
             collect(DISTINCT l.name) AS matched_labs,
             count(DISTINCT v) AS matched_visual_count,
             collect(DISTINCT v.name) AS matched_visual_entities,
             collect(DISTINCT img.modality) AS visual_modalities,
             coalesce(sum(coalesce(r1.frequency, 0)), 0) +
             coalesce(sum(coalesce(r2.frequency, 0)), 0) +
             coalesce(sum(coalesce(r3.frequency, 0)) * 2, 0) AS total_evidence_weight
        WHERE matched_symptoms_count > 0 OR matched_labs_count > 0 OR matched_visual_count > 0
        RETURN
          d.name AS disease,
          matched_symptoms_count,
          matched_symptoms,
          matched_labs_count,
          matched_labs,
          matched_visual_count,
          matched_visual_entities,
          visual_modalities,
          total_evidence_weight
        ORDER BY (matched_visual_count * 2 + matched_symptoms_count) DESC, total_evidence_weight DESC
        LIMIT $top_k
        """

        try:
            records = self.client.query(cypher, {
                "symptoms": symptoms,
                "labs": labs,
                "visual_entities": visual_entities,
                "top_k": top_k
            })
        except Exception as e:
            print(f"[MMGraphRetriever] Query error: {e}")
            return f"Multimodal knowledge graph query failed: {e}", []

        if not records:
            return "No matching diseases found in multimodal graph for these symptoms/labs/images.", []

        # Linearize into clear cross-modal clinical evidence table
        lines = [
            "| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Visual Pathology/Radiology Findings | Modalities | Evidence Weight |",
            "|---|---|---|---|---|---|"
        ]
        for rec in records:
            s_str = ", ".join(rec["matched_symptoms"]) if rec["matched_symptoms"] else "None"
            l_str = ", ".join(rec["matched_labs"]) if rec["matched_labs"] else "None"
            v_str = ", ".join(rec["matched_visual_entities"]) if rec["matched_visual_entities"] else "None"
            m_str = ", ".join(rec["visual_modalities"]) if rec["visual_modalities"] else "text"
            lines.append(f"| **{rec['disease']}** | {s_str} | {l_str} | {v_str} | {m_str} | {rec['total_evidence_weight']} |")

        linearized_text = "\n".join(lines)
        return linearized_text, records

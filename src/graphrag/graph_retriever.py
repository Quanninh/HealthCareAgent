"""Graph retriever for querying clinical subgraphs and linearizing evidence.
"""

from typing import List, Dict, Any, Tuple
from src.graph.neo4j_client import Neo4jClient


class GraphRetriever:
    """Retrieves and ranks subgraphs from Neo4j based on clinical entities."""

    def __init__(self, neo4j_client: Neo4jClient):
        self.client = neo4j_client

    def retrieve_subgraph(
        self,
        symptoms: List[str],
        labs: List[str],
        top_k: int = 5
    ) -> Tuple[str, List[Dict[str, Any]]]:
        """Queries Neo4j for diseases linked to the given symptoms and labs,

        returns linearized markdown evidence and raw structured records.
        """
        if not symptoms and not labs:
            return "No matching clinical entities detected to query knowledge graph.", []

        cypher = """
        MATCH (d:Disease)
        OPTIONAL MATCH (d)-[r1:PRESENTS_WITH]->(s:Symptom)
        WHERE s.name IN $symptoms
        OPTIONAL MATCH (d)-[r2:CONFIRMED_BY]->(l:LabFinding)
        WHERE l.name IN $labs
        WITH d,
             count(DISTINCT s) AS matched_symptoms_count,
             collect(DISTINCT s.name) AS matched_symptoms,
             count(DISTINCT l) AS matched_labs_count,
             collect(DISTINCT l.name) AS matched_labs,
             coalesce(sum(coalesce(r1.frequency, 0)), 0) + coalesce(sum(coalesce(r2.frequency, 0)), 0) AS total_evidence_weight
        WHERE matched_symptoms_count > 0 OR matched_labs_count > 0
        RETURN
          d.name AS disease,
          matched_symptoms_count,
          matched_symptoms,
          matched_labs_count,
          matched_labs,
          total_evidence_weight
        ORDER BY matched_symptoms_count DESC, total_evidence_weight DESC
        LIMIT $top_k
        """

        try:
            records = self.client.query(cypher, {
                "symptoms": symptoms,
                "labs": labs,
                "top_k": top_k
            })
        except Exception as e:
            print(f"[GraphRetriever] Query error: {e}")
            return f"Knowledge graph query failed: {e}", []

        if not records:
            return "No matching diseases found in knowledge graph for these symptoms/labs.", []

        # Linearize into clear clinical evidence text
        lines = ["| Candidate Disease | Matched Symptoms | Key Confirmatory Labs | Evidence Weight |"]
        lines.append("|---|---|---|---|")
        for rec in records:
            s_str = ", ".join(rec["matched_symptoms"]) if rec["matched_symptoms"] else "None"
            l_str = ", ".join(rec["matched_labs"]) if rec["matched_labs"] else "None"
            lines.append(f"| **{rec['disease']}** | {s_str} | {l_str} | {rec['total_evidence_weight']} |")

        linearized_text = "\n".join(lines)
        return linearized_text, records

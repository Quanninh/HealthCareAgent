"""Builds the Multimodal Knowledge Graph (MMKG) in Neo4j from the training split.
Integrates Text2Graph, Image2Graph, and SpecLink Cross-Modal Entity Linking.
"""

import sys
import os
import json
import argparse
from typing import List, Dict, Any

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.graph.neo4j_client import Neo4jClient
from src.graph.schema import SCHEMA_CONSTRAINTS, SCHEMA_INDEXES
from src.mmgraphrag.image2graph import Image2GraphExtractor
from src.mmgraphrag.speclink import SpecLinkAligner


MM_SCHEMA_CONSTRAINTS = SCHEMA_CONSTRAINTS + [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (v:VisualEntity) REQUIRE v.name IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (i:ImageNode) REQUIRE i.path IS UNIQUE;"
]

MM_SCHEMA_INDEXES = SCHEMA_INDEXES + [
    "CREATE INDEX IF NOT EXISTS FOR (v:VisualEntity) ON (v.name);",
    "CREATE INDEX IF NOT EXISTS FOR (i:ImageNode) ON (i.path);"
]


def ingest_batch_multimodal_cases(
    client: Neo4jClient,
    batch: List[Dict[str, Any]],
    i2g: Image2GraphExtractor,
    speclink: SpecLinkAligner
):
    """Batched ingestion of multimodal clinical cases, visual scene graphs, and cross-modal links."""
    # 1. Base Text KG Ingestion
    text_cypher = """
    UNWIND $batch AS case
    MERGE (d:Disease {name: case.target_disease})

    MERGE (c:CaseReport {case_id: case.case_id})
    SET c.age = case.age,
        c.gender = case.gender,
        c.title = case.title

    MERGE (d)-[:DOCUMENTED_IN]->(c)

    FOREACH (symptom_name IN case.extracted_symptoms |
        MERGE (s:Symptom {name: symptom_name})
        MERGE (d)-[r:PRESENTS_WITH]->(s)
        ON CREATE SET r.frequency = 1
        ON MATCH SET r.frequency = r.frequency + 1
    )

    FOREACH (lab_name IN case.extracted_labs |
        MERGE (l:LabFinding {name: lab_name})
        MERGE (d)-[r:CONFIRMED_BY]->(l)
        ON CREATE SET r.frequency = 1
        ON MATCH SET r.frequency = r.frequency + 1
    )
    """
    client.execute_write(text_cypher, {"batch": batch})

    # 2. Multimodal Image & Cross-Modal Links Ingestion
    img_records = []
    aligned_links = []

    for case in batch:
        case_id = case["case_id"]
        disease_name = case["target_disease"]
        text_entities = case.get("extracted_symptoms", []) + case.get("extracted_labs", [])

        for img in case.get("images", []):
            scene_graph = i2g.extract_from_image_record(img)
            img_path = scene_graph["img_path"]
            if not img_path:
                continue

            img_records.append({
                "case_id": case_id,
                "disease": disease_name,
                "path": img_path,
                "caption": scene_graph["caption"][:300],
                "modality": scene_graph["modality"],
                "region": scene_graph["region"],
                "visual_entities": scene_graph["visual_entities"]
            })

            # Run SpecLink alignment between visual entities and case text entities
            for vent in scene_graph["visual_entities"]:
                alignment = speclink.align_visual_entity(vent, text_entities)
                if alignment:
                    matched_text_ent, conf = alignment
                    aligned_links.append({
                        "visual_entity": vent,
                        "text_entity": matched_text_ent,
                        "confidence": conf
                    })

    if img_records:
        image_cypher = """
        UNWIND $img_records AS rec
        MATCH (c:CaseReport {case_id: rec.case_id})
        MATCH (d:Disease {name: rec.disease})

        MERGE (img:ImageNode {path: rec.path})
        SET img.caption = rec.caption,
            img.modality = rec.modality,
            img.region = rec.region

        MERGE (c)-[:CONTAINS_IMAGE]->(img)

        FOREACH (vent_name IN rec.visual_entities |
            MERGE (v:VisualEntity {name: vent_name})
            SET v.modality = 'visual'
            MERGE (img)-[:OBSERVES]->(v)
            MERGE (d)-[r:EVIDENCED_BY]->(v)
            ON CREATE SET r.frequency = 1
            ON MATCH SET r.frequency = r.frequency + 1
        )
        """
        client.execute_write(image_cypher, {"img_records": img_records})

    if aligned_links:
        align_cypher = """
        UNWIND $aligned_links AS link
        MATCH (v:VisualEntity {name: link.visual_entity})
        MATCH (target) WHERE (target:Symptom OR target:LabFinding) AND target.name = link.text_entity
        MERGE (v)-[r:ALIGNED_WITH]->(target)
        SET r.confidence = link.confidence,
            r.method = 'speclink'
        """
        client.execute_write(align_cypher, {"aligned_links": aligned_links})


def build_multimodal_knowledge_graph(
    train_path: str = "data/train_cases.jsonl",
    neo4j_uri: str = "bolt://localhost:7687",
    neo4j_user: str = "neo4j",
    neo4j_password: str = "password",
    batch_size: int = 100,
    clear_existing: bool = False
):
    """Constructs the unified Multimodal Knowledge Graph in Neo4j."""
    client = Neo4jClient(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    print(f"Connecting to Neo4j at {neo4j_uri}...")
    if not client.connect():
        raise ConnectionError(f"Could not connect to Neo4j at {neo4j_uri}.")

    if clear_existing:
        print("Clearing existing database prior to MMKG build...")
        client.execute_write("MATCH (n) DETACH DELETE n;")

    print("Applying multimodal constraints and indexes...")
    client.apply_schema(MM_SCHEMA_CONSTRAINTS, MM_SCHEMA_INDEXES)

    i2g = Image2GraphExtractor()
    speclink = SpecLinkAligner()

    print(f"Loading multimodal training cases from {train_path}...")
    batch = []
    total_ingested = 0

    with open(train_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            batch.append(record)
            if len(batch) >= batch_size:
                ingest_batch_multimodal_cases(client, batch, i2g, speclink)
                total_ingested += len(batch)
                print(f"  Ingested {total_ingested} multimodal cases...")
                batch = []

        if batch:
            ingest_batch_multimodal_cases(client, batch, i2g, speclink)
            total_ingested += len(batch)

    stats = client.query("""
        RETURN
          COUNT { MATCH (:Disease) } AS diseases,
          COUNT { MATCH (:Symptom) } AS symptoms,
          COUNT { MATCH (:LabFinding) } AS labs,
          COUNT { MATCH (:VisualEntity) } AS visual_entities,
          COUNT { MATCH (:ImageNode) } AS image_nodes,
          COUNT { MATCH ()-[:EVIDENCED_BY]->() } AS visual_evidence_rels,
          COUNT { MATCH ()-[:ALIGNED_WITH]->() } AS speclink_crossmodal_rels
    """)

    print(f"Successfully constructed Multimodal Knowledge Graph (MMKG)!")
    print(f"MMKG Statistics: {stats[0] if stats else 'N/A'}")
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Multimodal Knowledge Graph (MMKG) in Neo4j.")
    parser.add_argument("--train_path", type=str, default="data/train_cases.jsonl")
    parser.add_argument("--uri", type=str, default="bolt://localhost:7687")
    parser.add_argument("--user", type=str, default="neo4j")
    parser.add_argument("--password", type=str, default="password")
    parser.add_argument("--batch_size", type=int, default=100)
    parser.add_argument("--clear", action="store_true")
    args = parser.parse_args()

    build_multimodal_knowledge_graph(
        train_path=args.train_path,
        neo4j_uri=args.uri,
        neo4j_user=args.user,
        neo4j_password=args.password,
        batch_size=args.batch_size,
        clear_existing=args.clear
    )

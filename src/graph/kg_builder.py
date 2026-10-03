"""Ingests clinical cases into Neo4j to construct the Medical Knowledge Graph.
"""
import sys
import os
import json
import argparse
from typing import List, Dict, Any

# Ensure project root is in sys.path when running script directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.graph.neo4j_client import Neo4jClient
from src.graph.schema import SCHEMA_CONSTRAINTS, SCHEMA_INDEXES


def ingest_batch_cases(client: Neo4jClient, batch: List[Dict[str, Any]]):
    """Batched Cypher ingestion of clinical cases into Neo4j."""
    cypher = """
    UNWIND $batch AS case
    MERGE (d:Disease {name: case.target_disease})

    MERGE (c:CaseReport {case_id: case.case_id})
    SET c.age = case.age,
        c.gender = case.gender,
        c.title = case.title

    MERGE (d)-[:DOCUMENTED_IN]->(c)

    // Ingest Symptoms & update frequency weights
    FOREACH (symptom_name IN case.extracted_symptoms |
        MERGE (s:Symptom {name: symptom_name})
        MERGE (d)-[r:PRESENTS_WITH]->(s)
        ON CREATE SET r.frequency = 1
        ON MATCH SET r.frequency = r.frequency + 1
    )

    // Ingest Lab Findings & update frequency weights
    FOREACH (lab_name IN case.extracted_labs |
        MERGE (l:LabFinding {name: lab_name})
        MERGE (d)-[r:CONFIRMED_BY]->(l)
        ON CREATE SET r.frequency = 1
        ON MATCH SET r.frequency = r.frequency + 1
    )
    """
    client.execute_write(cypher, {"batch": batch})


def build_knowledge_graph(
    train_path: str = "data/train_cases.jsonl",
    neo4j_uri: str = "bolt://localhost:7687",
    neo4j_user: str = "neo4j",
    neo4j_password: str = "password",
    batch_size: int = 100,
    clear_existing: bool = False
):
    """Main builder function to initialize Neo4j schema and ingest training set."""
    client = Neo4jClient(uri=neo4j_uri, user=neo4j_user, password=neo4j_password)
    print(f"Connecting to Neo4j at {neo4j_uri}...")
    if not client.connect():
        raise ConnectionError(f"Could not connect to Neo4j at {neo4j_uri}. Make sure Neo4j is running.")

    if clear_existing:
        print("Clearing existing database nodes and relations...")
        client.execute_write("MATCH (n) DETACH DELETE n;")

    print("Applying schema constraints and indexes...")
    client.apply_schema(SCHEMA_CONSTRAINTS, SCHEMA_INDEXES)

    print(f"Loading training cases from {train_path}...")
    batch = []
    total_ingested = 0

    with open(train_path, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            record = json.loads(line)
            batch.append(record)
            if len(batch) >= batch_size:
                ingest_batch_cases(client, batch)
                total_ingested += len(batch)
                print(f"  Ingested {total_ingested} cases...")
                batch = []

        if batch:
            ingest_batch_cases(client, batch)
            total_ingested += len(batch)

    # Summary query
    stats = client.query("""
        RETURN
          COUNT { MATCH (:Disease) } AS diseases,
          COUNT { MATCH (:Symptom) } AS symptoms,
          COUNT { MATCH (:LabFinding) } AS labs,
          COUNT { MATCH ()-[:PRESENTS_WITH]->() } AS presents_rels,
          COUNT { MATCH ()-[:CONFIRMED_BY]->() } AS confirmed_rels
    """)

    print(f"Successfully constructed Medical Knowledge Graph!")
    print(f"Graph Statistics: {stats[0] if stats else 'N/A'}")
    client.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build Neo4j Medical Knowledge Graph from training split.")
    parser.add_argument("--train_path", type=str, default="data/train_cases.jsonl")
    parser.add_argument("--uri", type=str, default="bolt://localhost:7687")
    parser.add_argument("--user", type=str, default="neo4j")
    parser.add_argument("--password", type=str, default="password")
    parser.add_argument("--batch_size", type=int, default=100)
    parser.add_argument("--clear", action="store_true", help="Clear existing database prior to ingestion")
    args = parser.parse_args()

    build_knowledge_graph(
        train_path=args.train_path,
        neo4j_uri=args.uri,
        neo4j_user=args.user,
        neo4j_password=args.password,
        batch_size=args.batch_size,
        clear_existing=args.clear
    )

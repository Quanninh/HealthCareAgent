"""Neo4j schema definitions, constraints, and indexes for Clinical Knowledge Graph.
"""

from typing import List

# Cypher constraints for unique entities
SCHEMA_CONSTRAINTS: List[str] = [
    "CREATE CONSTRAINT IF NOT EXISTS FOR (d:Disease) REQUIRE d.name IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (s:Symptom) REQUIRE s.name IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (l:LabFinding) REQUIRE l.name IS UNIQUE;",
    "CREATE CONSTRAINT IF NOT EXISTS FOR (c:CaseReport) REQUIRE c.case_id IS UNIQUE;"
]

# Cypher indexes for fast lookup during retrieval
SCHEMA_INDEXES: List[str] = [
    "CREATE INDEX IF NOT EXISTS FOR (d:Disease) ON (d.name);",
    "CREATE INDEX IF NOT EXISTS FOR (s:Symptom) ON (s.name);",
    "CREATE INDEX IF NOT EXISTS FOR (l:LabFinding) ON (l.name);"
]

# Node labels and relationships
LABEL_DISEASE = "Disease"
LABEL_SYMPTOM = "Symptom"
LABEL_LAB_FINDING = "LabFinding"
LABEL_CASE_REPORT = "CaseReport"

REL_PRESENTS_WITH = "PRESENTS_WITH"
REL_CONFIRMED_BY = "CONFIRMED_BY"
REL_DOCUMENTED_IN = "DOCUMENTED_IN"
REL_DIFFERENTIAL_TO = "DIFFERENTIAL_TO"

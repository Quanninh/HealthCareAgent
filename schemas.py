"""
schemas.py: Formal label space definitions and typed data models.

Defines the label enumerations used by both Stage 1 (Entity Verification) and
Stage 2 (Disease Diagnosis), plus the Pydantic data models for structured I/O.
"""
from enum import IntEnum
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


# ─── Stage 1 Label Space ───────────────────────────────────────────────
class EntityValidity(IntEnum):
    """Binary label for clinical-entity fact-checking."""
    ABSTAIN  = -1
    INVALID  =  0   # Negated, hallucinated, historical, or non-patient entity
    VALID    =  1   # Confirmed active clinical problem for the patient


# ─── Stage 2 Label Space ───────────────────────────────────────────────
class BinaryDiseaseLabel(IntEnum):
    """Independent binary label for each disease classifier."""
    ABSTAIN  = -1
    NEGATIVE =  0
    POSITIVE =  1


# ─── Pydantic Data Models ──────────────────────────────────────────────
class ClinicalEntity(BaseModel):
    """Represents a single extracted clinical entity from a case report."""
    entity_id: str
    text_span: str
    category: str
    modality: Optional[str] = None
    anatomical_site: Optional[str] = None
    assertion: str           # "affirmed", "negated", "suspected"
    temporality: str         # "current", "historical"
    experiencer: str         # "patient", "family_member", "other"
    sentence_context: str
    ontology_mapping: Optional[Dict[str, Any]] = None
    valid_probability: Optional[float] = None


class DiagnosisResult(BaseModel):
    """Multi-label diagnosis output for a single patient case."""
    case_id: str
    p_covid19: float = Field(ge=0.0, le=1.0)
    p_tuberculosis: float = Field(ge=0.0, le=1.0)
    p_dengue: float = Field(ge=0.0, le=1.0)
    covid19_label: str = ""     # POSITIVE / NEGATIVE / UNCERTAIN
    tuberculosis_label: str = ""
    dengue_label: str = ""
    evidence_used: List[str] = Field(default_factory=list)

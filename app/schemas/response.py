from pydantic import BaseModel
from typing import List

class ConceptOverlap(BaseModel):
    concept: str
    status: str  # "Found" | "Missing"
    confidence: float

class SimilarityResponse(BaseModel):
    similarity_score: float
    analysis_status: str
    key_concept_overlap: List[ConceptOverlap]

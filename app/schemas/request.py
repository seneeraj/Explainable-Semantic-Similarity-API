from pydantic import BaseModel, Field

class SimilarityRequest(BaseModel):
    source_document: str = Field(
        ..., description="Reference document (truth)"
    )
    candidate_document: str = Field(
        ..., description="Document under evaluation"
    )
    language: str = Field(
        default="en", description="ISO 639-1 language code"
    )

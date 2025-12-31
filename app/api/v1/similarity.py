from fastapi import APIRouter

from app.schemas.request import SimilarityRequest
from app.schemas.response import SimilarityResponse
from app.core.config import MAX_DOC_CHARS
from app.core.errors import InputTooLargeError

from app.core.chunking import chunk_document
from app.core.similarity import compute_global_similarity
from app.core.concepts import extract_key_concepts
from app.core.concept_matching import match_concepts_to_candidate


router = APIRouter()


@router.post(
    "/compare",
    response_model=SimilarityResponse,
    summary="Compare two documents for semantic similarity and concept overlap"
)
def compare_documents(payload: SimilarityRequest):

    # 1️⃣ Input size validation
    if len(payload.source_document) > MAX_DOC_CHARS:
        raise InputTooLargeError("Source document exceeds size limit")

    if len(payload.candidate_document) > MAX_DOC_CHARS:
        raise InputTooLargeError("Candidate document exceeds size limit")

    # 2️⃣ Chunk documents
    source_chunks = chunk_document(payload.source_document)
    candidate_chunks = chunk_document(payload.candidate_document)

    # 3️⃣ Stage-1: Global semantic similarity
    similarity_score = compute_global_similarity(
        source_chunks,
        candidate_chunks
    )

    # 4️⃣ Stage-2a: Extract key concepts from SOURCE
    key_concepts = extract_key_concepts(payload.source_document)

    # 5️⃣ Stage-2b: Match concepts against CANDIDATE
    concept_analysis = match_concepts_to_candidate(
        key_concepts,
        candidate_chunks
    )

    # 6️⃣ Final response
    return SimilarityResponse(
        similarity_score=round(similarity_score, 3),
        analysis_status="Success",
        key_concept_overlap=concept_analysis
    )

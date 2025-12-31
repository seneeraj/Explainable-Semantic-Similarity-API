"""
Phase-7 Evaluation Harness
Evaluates similarity score and concept explainability
"""

from app.core.chunking import chunk_document
from app.core.similarity import compute_global_similarity
from app.core.concepts import extract_key_concepts
from app.core.concept_matching import match_concepts_to_candidate


def evaluate_pair(source_text: str, candidate_text: str):
    """
    Runs full pipeline on one document pair
    """

    # Chunk documents
    source_chunks = chunk_document(source_text)
    candidate_chunks = chunk_document(candidate_text)

    # Stage-1 similarity
    similarity = compute_global_similarity(
        source_chunks,
        candidate_chunks
    )

    # Stage-2 explainability
    concepts = extract_key_concepts(source_text)
    concept_results = match_concepts_to_candidate(
        concepts,
        candidate_chunks
    )

    return {
        "similarity_score": round(similarity, 3),
        "concept_analysis": concept_results
    }


if __name__ == "__main__":
    # Simple sanity test
    source = "Ethical sourcing and supplier audits ensure sustainability."
    candidate = "Supplier audits help companies meet sustainability goals."

    result = evaluate_pair(source, candidate)

    print("Similarity Score:", result["similarity_score"])
    print("Concept Analysis:")
    for c in result["concept_analysis"]:
        print(c)

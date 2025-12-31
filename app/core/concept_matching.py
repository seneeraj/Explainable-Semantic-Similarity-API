from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict

# Load model ONCE (important for performance & consistency)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    """
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def normalize_concept(text: str) -> str:
    """
    Normalize concept phrasing to improve embedding alignment.
    Deterministic and explainable (Path-A compliant).
    """
    text = text.lower().strip()

    for suffix in [
        "policies",
        "policy",
        "procedures",
        "processes",
        "framework",
        "frameworks",
        "strategies",
        "strategy",
        "practices",
        "standards",
        "programs"
    ]:
        if text.endswith(" " + suffix):
            text = text[: -len(suffix) - 1]

    return text


def match_concepts_to_candidate(
    concepts: List[str],
    candidate_chunks: List[str],
    threshold: float = 0.62
) -> List[Dict]:
    """
    Match each source concept against candidate document chunks.

    Uses conservative, concept-aware thresholding
    with normalization to improve Recall and
    Missing Detection Accuracy.
    """

    if not concepts or not candidate_chunks:
        return []

    # --- Normalize concepts (CRITICAL for recall) ---
    normalized_concepts = [normalize_concept(c) for c in concepts]

    # --- Embed once ---
    concept_embeddings = _model.encode(normalized_concepts, convert_to_numpy=True)
    chunk_embeddings = _model.encode(candidate_chunks, convert_to_numpy=True)

    results: List[Dict] = []

    for idx, concept in enumerate(concepts):
        scores = [
            cosine_similarity(concept_embeddings[idx], chunk_emb)
            for chunk_emb in chunk_embeddings
        ]

        max_score = max(scores)

        # --- Adaptive thresholding (precision control) ---
        adjusted_threshold = threshold

        if len(concept.split()) >= 3:
            adjusted_threshold += 0.03

        if max_score >= adjusted_threshold:
            status = "Found"
        else:
            status = "Missing"

        results.append({
            "concept": concept,
            "status": status,
            "confidence": round(max_score, 3)
        })

    return results

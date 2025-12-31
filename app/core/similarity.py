from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List

# Load model ONCE (important for performance)
_model = SentenceTransformer("all-MiniLM-L6-v2")


def cosine_similarity_matrix(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Compute cosine similarity matrix between two embedding sets.
    """
    a_norm = a / np.linalg.norm(a, axis=1, keepdims=True)
    b_norm = b / np.linalg.norm(b, axis=1, keepdims=True)
    return np.dot(a_norm, b_norm.T)


def compute_global_similarity(
    source_chunks: List[str],
    candidate_chunks: List[str],
    top_n: int = 5
) -> float:
    """
    Compute global semantic similarity score between two documents.
    """

    if not source_chunks or not candidate_chunks:
        return 0.0

    # Embed chunks
    src_embeddings = _model.encode(source_chunks, convert_to_numpy=True)
    cand_embeddings = _model.encode(candidate_chunks, convert_to_numpy=True)

    # Similarity matrix
    sim_matrix = cosine_similarity_matrix(src_embeddings, cand_embeddings)

    # Take top-N similarities per source chunk
    top_similarities = np.sort(sim_matrix, axis=1)[:, -top_n:]

    # Aggregate
    return float(np.mean(top_similarities))

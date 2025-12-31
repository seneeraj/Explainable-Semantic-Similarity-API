import json
import numpy as np
from scipy.stats import pearsonr
from sentence_transformers import SentenceTransformer

from evaluation.run_evaluation import evaluate_pair


# ============================================================
# Global embedding model (evaluation-only)
# ============================================================
_align_model = SentenceTransformer("all-MiniLM-L6-v2")


# ============================================================
# Dataset loader
# ============================================================
def load_dataset(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


# ============================================================
# AC-Q.1 — Pearson Correlation
# ============================================================
def compute_pearson(human_scores, model_scores):
    if len(human_scores) < 2:
        return 0.0
    corr, _ = pearsonr(human_scores, model_scores)
    return round(float(corr), 3)


# ============================================================
# Semantic helpers (CRITICAL DESIGN)
# ============================================================
def is_semantically_found(
    gt_concept: str,
    predicted_concepts: dict,
    threshold: float = 0.60
) -> bool:
    """
    Looser semantic match used ONLY for recall (AC-Q.2).
    Maximizes coverage.
    """
    if not predicted_concepts:
        return False

    texts = [gt_concept] + list(predicted_concepts.keys())
    embeddings = _align_model.encode(texts, convert_to_numpy=True)

    gt_vec = embeddings[0]
    pred_vecs = embeddings[1:]

    sims = np.dot(pred_vecs, gt_vec) / (
        np.linalg.norm(pred_vecs, axis=1) * np.linalg.norm(gt_vec)
    )

    return float(np.max(sims)) >= threshold


def is_semantically_missing(
    gt_concept: str,
    predicted_concepts: dict,
    threshold: float = 0.85
) -> bool:
    """
    Stricter semantic match used ONLY for missing detection (AC-Q.3).
    Prevents false positives.
    """
    if not predicted_concepts:
        return True

    texts = [gt_concept] + list(predicted_concepts.keys())
    embeddings = _align_model.encode(texts, convert_to_numpy=True)

    gt_vec = embeddings[0]
    pred_vecs = embeddings[1:]

    sims = np.dot(pred_vecs, gt_vec) / (
        np.linalg.norm(pred_vecs, axis=1) * np.linalg.norm(gt_vec)
    )

    return float(np.max(sims)) < threshold


# ============================================================
# AC-Q.2 — Concept Recall (SEMANTIC)
# ============================================================
def compute_concept_recall(results):
    tp, fn = 0, 0

    for r in results:
        for concept, expected in r["concept_labels"].items():
            if expected == "Found":
                if is_semantically_found(concept, r["predicted"]):
                    tp += 1
                else:
                    fn += 1

    return round(tp / (tp + fn), 3) if (tp + fn) else 0.0


# ============================================================
# AC-Q.3 — Missing Detection Accuracy (STRICT)
# ============================================================
def compute_missing_accuracy(results):
    correct, total = 0, 0

    for r in results:
        for concept, expected in r["concept_labels"].items():
            if expected == "Missing":
                total += 1
                if is_semantically_missing(concept, r["predicted"]):
                    correct += 1

    return round(correct / total, 3) if total else 0.0


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":

    # 🔴 Change dataset path as needed
    
    #DATASET_PATH = "evaluation/gs_sim_50_calibration_aligned.json"
    
    DATASET_PATH = "evaluation/gs_sim_50_test.json"


    
    #DATASET_PATH = "evaluation/gs_sim_60.json"
    #DATASET_PATH = "evaluation/gs_sim_50_calibration.json"

    # For final validation later:
    # DATASET_PATH = "evaluation/gs_sim_100.json"

    dataset = load_dataset(DATASET_PATH)

    human_scores = []
    model_scores = []
    evaluation_results = []

    for case in dataset:
        output = evaluate_pair(
            case["source_document"],
            case["candidate_document"]
        )

        human_scores.append(case["human_similarity"])
        model_scores.append(output["similarity_score"])

        predicted_concepts = {
            c["concept"]: c["status"]
            for c in output["concept_analysis"]
        }

        evaluation_results.append({
            "id": case["id"],
            "predicted": predicted_concepts,
            "concept_labels": case["concept_labels"]
        })

    # ========================================================
    # Compute metrics
    # ========================================================
    pearson = compute_pearson(human_scores, model_scores)
    recall = compute_concept_recall(evaluation_results)
    missing_acc = compute_missing_accuracy(evaluation_results)

    print("\n📊 PHASE-7 METRICS")
    print("------------------")
    print(f"Pearson Correlation (AC-Q.1): {pearson}")
    print(f"Concept Recall (AC-Q.2): {recall}")
    print(f"Missing Detection Accuracy (AC-Q.3): {missing_acc}")

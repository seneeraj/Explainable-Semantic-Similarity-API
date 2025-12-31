# Explainable Semantic Similarity API

An explainable, production-grade semantic similarity engine for
comparing long documents with concept-level interpretability.

This system computes:
- A global semantic similarity score
- An explainable breakdown of key concepts
- Found / Missing classification with confidence scores

The API is designed to be:
- Deterministic
- Auditable
- Scalable
- Docker-first and reproducible

---

## ⚠️ Usage Notice

This repository is shared strictly for academic evaluation and
technical review purposes.

Copying, redistribution, modification, or reuse of this code for
any commercial or non-evaluative purpose is **not permitted**
without prior written consent from the author.

---

## 📐 High-Level Architecture
Client
|
| POST /api/v1/similarity/compare
v
FastAPI Application
|
+-- Input Validation
+-- Document Chunking Engine
+-- Global Similarity Computation (Sentence-BERT)
+-- Explainable Concept Extraction
+-- Concept-to-Document Matching
|
v
JSON Response (Score + Explainability)


---

## 🚀 Run the API Using Docker (Recommended)

### Prerequisites
- Docker installed and running
- No Python setup required

---

### Step 1: Build the Docker Image

```bash
docker build -t explainable-semantic-similarity-api .

Step 2: Run the Container

docker run -p 8000:8000 explainable-semantic-similarity-api

Step 3: Open Swagger UI

Open the following URL in your browser:

http://localhost:8000/docs

You will see the interactive Swagger interface.

API ENDPOINT

POST /api/v1/similarity/compare
Request Body Example

{
  "source_document": "The company has implemented supplier diversification strategies to improve supply chain resilience.",
  "candidate_document": "The organization expanded its vendor base to reduce dependency on individual suppliers.",
  "language": "en"
}

Response Example:
{
  "similarity_score": 0.82,
  "analysis_status": "Success",
  "key_concept_overlap": [
    {
      "concept": "supplier diversification",
      "status": "Found",
      "confidence": 0.78
    },
    {
      "concept": "supply chain resilience",
      "status": "Found",
      "confidence": 0.74
    }
  ]
}


Optional: Evaluation Scripts

The evaluation/ directory contains:

Golden standard datasets (GS-Sim)

Metric computation scripts

Pearson correlation and recall evaluation

These are not required to run the API but are included for
validation and research completeness.

🧠 Design Philosophy

No LLM prompt-based reasoning

No hallucination-prone explanations

Concept-level explainability over token-level opacity

Threshold-based, auditable decisions

This makes the system suitable for compliance, governance,
and enterprise-grade semantic comparison use cases.

explainable-semantic-similarity-api/
├── app/
├── evaluation/
├── Dockerfile
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore

Author

Neeraj Bhatia
(Provided for academic evaluation and review)
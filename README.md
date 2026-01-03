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

## Running Evaluation Metrics

Metrics must be run inside the Docker container.

```bash
docker run -it explainable-semantic-similarity-api /bin/bash
python -m evaluation.compute_metrics


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


📌 Use Cases & Acceptance Criteria Alignment

This section demonstrates how the system’s Acceptance Criteria (AC) are not abstract checks, but directly support real-world, production-grade use cases.
Each acceptance criterion is intentionally designed to enable explainability, auditability, and reliability across different domains.

1. Compliance & Policy Verification

Scenario
Compare a regulatory policy, standard, or guideline (source document) with an internal company policy or SOP (candidate document) to identify missing compliance requirements.

Supported Acceptance Criteria

Acceptance Criterion	Justification
AC-F.1 – API returns valid JSON	Compliance platforms require structured, machine-readable outputs
AC-F.2 – Supports long documents	Policies and regulations are often very large
AC-F.3 – Global similarity score	Provides a high-level compliance coverage indicator
AC-F.4 – Concept-level Found/Missing	Auditors must see exactly which requirements are missing
AC-Q.2 – Concept Recall ≥ 80%	Missing compliance requirements must be minimized
AC-Q.3 – Missing Detection Accuracy ≥ 90%	False negatives are unacceptable in compliance workflows
AC-NFR.1 – Deterministic results	Audits require repeatable and defensible outputs

2. Legal Contract Gap Analysis (Pre-Screening)

Scenario
Compare a standard contract template with a vendor-submitted contract to identify missing or weakly covered clauses before legal review.

Supported Acceptance Criteria

Acceptance Criterion	Justification
AC-F.1 – API-based interface	Legal tech platforms integrate via APIs
AC-F.4 – Concept-level analysis	Lawyers need explicit clause gaps, not black-box scores
AC-Q.3 – Missing Detection Accuracy	Missing clauses pose legal and financial risk
AC-NFR.2 – No hallucinated explanations	Conservative behavior is mandatory in legal contexts
AC-NFR.4 – Explainability	Legal decisions must be reviewable and auditable

Note: The system does not claim legal correctness; it provides semantic coverage evidence to support human decision-making.


3. RFP / Proposal Matching (Procurement)

Scenario
Compare an RFP or tender document with vendor proposals to assess requirement coverage and identify missing responses.

Supported Acceptance Criteria

Acceptance Criterion	Justification
AC-F.3 – Global similarity score	Enables rapid proposal shortlisting
AC-F.4 – Concept overlap report	Identifies unmet RFP requirements
AC-Q.1 – Pearson Correlation ≥ 0.85	Ensures similarity scores align with human judgment
AC-NFR.3 – Scalability	Procurement teams evaluate many proposals
AC-NFR.5 – CPU-based inference	Enables large-scale evaluation without GPUs

4. Academic & Educational Content Coverage

Scenario
Evaluate whether a student report, thesis, or assignment covers required syllabus topics or learning objectives.

Supported Acceptance Criteria

Acceptance Criterion	Justification
AC-F.2 – Long document support	Academic documents are often lengthy
AC-F.4 – Concept extraction & matching	Enables topic-level coverage analysis
AC-Q.2 – Concept Recall ≥ 80%	Required topics should not be missed
AC-NFR.1 – Deterministic behavior	Ensures consistent and fair evaluation

5. Software Requirements ↔ Documentation Verification

Scenario
Compare software requirements or specifications with design or implementation documentation to detect missing requirements.

Supported Acceptance Criteria

Acceptance Criterion	Justification
AC-F.3 – Global similarity score	High-level alignment check
AC-F.4 – Concept-level matching	Identifies dropped or unaddressed requirements
AC-Q.2 – Concept Recall	Prevents silent requirement omissions
AC-NFR.4 – Explainability	Required for engineering and audit reviews

6. LLM Guardrail / Validation Layer

Scenario
Validate documents generated by large language models (LLMs) against a reference document to detect missing concepts.

Supported Acceptance Criteria

Acceptance Criterion	Justification
AC-F.1 – REST API design	Easy integration into AI pipelines
AC-F.4 – Explicit gap reporting	LLMs require concrete, structured feedback
AC-NFR.2 – Conservative behavior	Prevents hallucinated validation
AC-NFR.1 – Reproducibility	Same input always produces the same validation result

Summary: 

Each acceptance criterion defined for this project directly supports at least one real-world deployment scenario.
This ensures the system is not only technically correct, but also practically useful, explainable, and defensible in enterprise, academic, and regulatory environments.


Author
Neeraj Bhatia
(Provided for academic evaluation and review)


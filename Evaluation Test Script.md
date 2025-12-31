**"Evaluation Test Script”**.

-------------------------------

# Test Script – Explainable Semantic Similarity API

This test script verifies **functional correctness**, **explainability**, and **model quality** using Docker and Swagger UI.

-----------------------------

## 🔹 Prerequisites (Tester's System)

Before starting, the tester must have:

1. **Docker Desktop installed and running**

   * Windows / macOS / Linux supported
   
2. **Internet connection** (for first Docker build only)

3. **No Python installation required** (Docker encapsulates everything)

---------------------------------

## 🔹 Test Activity 1 — API Startup & Swagger Verification

**(Validates AC-F.1: API returns JSON for valid inputs)**

### Step 1.1 — Clone Repository

```bash
git clone https://github.com/<username>/Explainable-Semantic-Similarity-API.git
cd Explainable-Semantic-Similarity-API
```

**Instructor verifies**

* Repository contains:

  * `app/`
  * `Dockerfile`
  * `requirements.txt`
  * `README.md`

-------------------

### Step 1.2 — Build Docker Image

```bash
docker build -t explainable-semantic-similarity-api .
```

(First build may take several minutes)

**Instructor verifies**

* Build completes without error
* spaCy model downloads successfully
* No missing dependency errors

-------------------

### Step 1.3 — Run Docker Container

```bash
docker run -p 8000:8000 explainable-semantic-similarity-api
```

Expected console output:

```
Uvicorn running on http://0.0.0.0:8000
```

------------------------

### Step 1.4 — Open Swagger UI

Open browser and visit:

```
http://localhost:8000/docs
```

**Instructor verifies**

* Swagger UI loads
* Endpoint visible:

  ```
  POST /api/v1/similarity/compare
  ```

✔️ **AC-F.1 satisfied**

---

## 🔹 Test Activity 2 — Functional + Explainability Test

**(Validates AC-F.1 + AC-Q.3)**

### Step 2.1 — Execute API Test via Swagger

Click **Try it out** and paste the following JSON:

```json
{
  "source_document": "The company has implemented supplier diversification strategies to reduce dependency on single vendors and improve supply chain resilience.",
  "candidate_document": "To strengthen supply chain stability, the organization has expanded its vendor base and reduced reliance on individual suppliers.",
  "language": "en"
}
```

Click **Execute**.

-----------------------

### Step 2.2 — Verify Response Structure

Expected response format:

```json
{
  "similarity_score": 0.7 – 0.9,
  "analysis_status": "Success",
  "key_concept_overlap": [
    {
      "concept": "supplier diversification",
      "status": "Found",
      "confidence": 0.7+
    }
  ]
}
```

**Instructor verifies**

* Response is valid JSON
* `analysis_status = "Success"`
* `similarity_score` is numeric (0–1)
* Concept list shows **Found / Missing**
* Confidence values are provided

✔️ **Explainability confirmed (AC-Q.3)**

-------------------------

## 🔹 Test Activity 3 — Negative / Contrast Test

**(Validates model discrimination & missing concept detection)**

### Step 3.1 — Submit Unrelated Documents

```json
{
  "source_document": "The study explores marine biodiversity and coral reef conservation methods.",
  "candidate_document": "The report focuses on financial risk modeling and investment portfolio optimization.",
  "language": "en"
}
```

----------------------------

### Step 3.2 — Verify Output

Expected:

```json
{
  "similarity_score": < 0.2,
  "analysis_status": "Success",
  "key_concept_overlap": [
    {
      "concept": "marine biodiversity",
      "status": "Missing",
      "confidence": low
    }
  ]
}
```

**Tester verifies**

* Low similarity score
* Concepts correctly marked **Missing**
* No false positives

✔️ **Missing Detection Accuracy validated (AC-Q.3)**

-------------------------

## 🔹 (Optional) Test Activity 4 — Model Quality Metrics

**(Validates AC-Q.1 & AC-Q.2)**

> This step is optional if instructor wants to verify quantitative metrics.

### Step 4.1 — Run Metrics Script

```bash
docker exec -it <container_id> python -m evaluation.compute_metrics
```

Expected output:

```
Pearson Correlation (AC-Q.1): ≥ 0.85
Concept Recall (AC-Q.2): ≥ 0.80
Missing Detection Accuracy (AC-Q.3): ≥ 0.90
```

✔️ **Model quality acceptance confirmed**

---

## Final Tester Verification Checklist

| Criteria                           | Verified  |
| ---------------------------------- | --------  |
| API runs via Docker                | ✅        |
| Swagger UI accessible              | ✅        |
| Valid JSON response                | ✅        |
| Explainable concept output         | ✅        |
| Low similarity for unrelated texts | ✅        |
| Metrics meet thresholds            | ✅        |

---

## 🏁 Final Outcome

**All mandatory launch acceptance criteria are satisfied.**
The system is:

* Reproducible
* Explainable
* Docker-portable
* Instructor-verifiable

-------------------------------------**** END of the Test Script----------------------***


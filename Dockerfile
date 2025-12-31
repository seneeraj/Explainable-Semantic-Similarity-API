# =====================================
# Explainable Semantic Similarity API
# Dockerfile (Submission Safe)
# =====================================

# ---- Base Image ----
FROM python:3.10-slim

# ---- Environment Safety ----
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ---- Working Directory ----
WORKDIR /app

# ---- System Dependencies ----
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ---- Copy Dependency File ----
COPY requirements.txt .

# ---- Install Python Dependencies ----
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ---- Download spaCy Model ----
RUN python -m spacy download en_core_web_sm

# ---- Copy Application Code ----
COPY app ./app
COPY evaluation ./evaluation

# ---- Expose API Port ----
EXPOSE 8000

# ---- Run API ----
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

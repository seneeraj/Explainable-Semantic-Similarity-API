from fastapi import FastAPI
from app.api.v1.similarity import router as similarity_router

app = FastAPI(
    title="Explainable Semantic Similarity API",
    version="1.0.0"
)

app.include_router(
    similarity_router,
    prefix="/api/v1/similarity",
    tags=["Semantic Similarity"]
)

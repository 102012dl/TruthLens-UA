"""TruthLens UA — FastAPI Production Backend"""
from typing import Optional, List
import time
import logging

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict, Field

from src.ml.analyzer import analyze_text, get_analyzer

logger = logging.getLogger(__name__)

app = FastAPI(
    title="TruthLens UA API",
    description="AI-powered Ukrainian Fake News & ІПСО Detector",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=5,
        max_length=10000,
        description="Text to analyze (UA or EN)",
    )
    source: Optional[str] = Field(
        None,
        description="Source URL or Telegram channel",
    )
    language: Optional[str] = Field(
        "auto",
        description="ua|en|auto",
    )


class AnalyzeResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    label: str
    fake_score: float
    credibility: int
    confidence: float
    sentiment: str
    verdict: str
    ipso_techniques: List[str]
    manipulation_flags: List[str]
    model_used: str
    deepfake_risk: str
    processing_time_ms: float


@app.get("/")
async def root() -> dict:
    """Root: посилання на документацію та ендпоінти."""
    return {
        "service": "TruthLens UA API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
        "analyze": "POST /api/analyze",
    }


@app.get("/health")
async def health() -> dict:
    analyzer = get_analyzer()
    return {
        "status": "ok",
        "model_loaded": analyzer.model_loaded,
        "model_path": getattr(analyzer, "_model_path", None) or "rule-based-fallback",
        "version": "2.0.0",
    }


@app.post("/api/analyze", response_model=AnalyzeResponse)
async def analyze(req: AnalyzeRequest) -> AnalyzeResponse:
    start = time.time()
    try:
        result = analyze_text(req.text)
        return AnalyzeResponse(
            **result,
            processing_time_ms=round((time.time() - start) * 1000, 1),
        )
    except Exception as exc:  # noqa: BLE001
        logger.error("Analyze error: %s", exc)
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/api/models")
async def models() -> dict:
    return {
        "current": "LinearSVC+ISOT+UA-ІПСО",
        "f1": 0.9947,
        "accuracy": 0.9942,
        "dataset": "ISOT 39,103 articles",
        "features": "TF-IDF 50k ngram(1,2)",
        "mlflow_run": "06ea1987abfd43bb81f11c283f7586c8",
    }


@app.get("/api/stats")
async def stats() -> dict:
    return {
        "total_analyzed": 26,
        "real": 18,
        "fake": 3,
        "suspicious": 5,
        "accuracy_rate": "69.2% verified",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )


from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="TruthLens V5 MVP")

class Analyze(BaseModel):
    text: str

@app.post("/api/analyze")
def analyze(req: Analyze):
    exclam = req.text.count("!!!") * 0.15
    upper_words = sum(1 for w in req.text.split() if w.isupper()) * 0.05
    fake_score = min(1.0, exclam + upper_words + 0.4)
    verdict = "FAKE" if fake_score > 0.7 else "SUSPICIOUS" if fake_score > 0.4 else "REAL"
    return {
        "verdict": verdict,
        "confidence": round(fake_score, 2),
        "text": (req.text[:50] + "...") if len(req.text) > 50 else req.text
    }

@app.get("/")
def root():
    return {"TruthLens": "V5 Ready! 🚀"}

@app.get("/health")
def health():
    return {"status": "ok"}

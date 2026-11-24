import time
from fastapi import APIRouter
from backend.app.services.ai.gemini_provider import GeminiProvider

router = APIRouter(tags=["Health & Status"])

@router.get("/health")
def health_status():
    gemini = GeminiProvider()
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "gemini_live_connected": gemini.is_available(),
        "mode": "Live Gemini AI + Campus Knowledge Base" if gemini.is_available() else "Local Grounded Campus Knowledge Base (Fallback Ready)"
    }

@router.get("/health/ai")
def ai_status():
    gemini = GeminiProvider()
    return {
        "provider": "google-gemini-2.5-flash",
        "status": "available" if gemini.is_available() else "fallback_active",
        "fallback_engine": "deterministic_sqlite_rag"
    }

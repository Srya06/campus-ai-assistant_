import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.app.core.config import settings
from backend.app.db.seed import init_db
from backend.app.api.v1.auth import router as auth_router
from backend.app.api.v1.chat import router as chat_router
from backend.app.api.v1.timetable import router as timetable_router
from backend.app.api.v1.courses import router as courses_router
from backend.app.api.v1.exams import router as exams_router
from backend.app.api.v1.faqs import router as faqs_router
from backend.app.api.v1.documents import router as documents_router
from backend.app.api.v1.notes import router as notes_router
from backend.app.api.v1.admin import router as admin_router
from backend.app.api.v1.health import router as health_router

from backend.campus_knowledge import CAMPUS_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("campus_ai")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database schema & seed data are initialized
    if os.getenv("TESTING") != "1":
        logger.info("Initializing Campus AI Assistant application...")
        try:
            init_db()
        except Exception as e:
            logger.error(f"Error during database startup initialization: {e}")
    yield
    logger.info("Campus AI Assistant shutting down...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Student-Centric Conversational Academic Navigator & Advisory System.",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API v1 Routers
api_v1_prefix = settings.API_V1_STR
app.include_router(health_router, prefix=api_v1_prefix)
app.include_router(auth_router, prefix=api_v1_prefix)
app.include_router(chat_router, prefix=api_v1_prefix)
app.include_router(timetable_router, prefix=api_v1_prefix)
app.include_router(courses_router, prefix=api_v1_prefix)
app.include_router(exams_router, prefix=api_v1_prefix)
app.include_router(faqs_router, prefix=api_v1_prefix)
app.include_router(documents_router, prefix=api_v1_prefix)
app.include_router(notes_router, prefix=api_v1_prefix)
app.include_router(admin_router, prefix=api_v1_prefix)

# Root-level backward-compatible aliases
app.include_router(health_router)
app.include_router(chat_router)
app.include_router(documents_router)

from backend.app.schemas.common import DocumentRequest, DocumentResponse
from backend.app.api.v1.documents import generate_academic_document
from backend.app.db.session import get_db
from fastapi import Depends
from sqlalchemy.orm import Session

@app.post("/generate", response_model=DocumentResponse, tags=["Document Drafter Legacy Alias"])
def generate_legacy(payload: DocumentRequest, db: Session = Depends(get_db)):
    return generate_academic_document(payload=payload, db=db)

@app.get("/api/campus-data", tags=["Campus Data"])
async def get_campus_data():
    """Returns verified campus structured dataset."""
    return CAMPUS_DATA

@app.get("/api/overview", tags=["Root"])
@app.get("/api-info", tags=["Root"])
async def root_overview():
    return {
        "title": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "online",
        "api_v1_documentation": "/docs",
        "endpoints": {
            "chat": f"{api_v1_prefix}/chat",
            "timetable": f"{api_v1_prefix}/timetable",
            "courses": f"{api_v1_prefix}/courses",
            "exams": f"{api_v1_prefix}/exams",
            "faqs": f"{api_v1_prefix}/faqs",
            "documents": f"{api_v1_prefix}/documents/generate",
            "auth": f"{api_v1_prefix}/auth/login"
        }
    }

# Mount static frontend assets so http://localhost:8000 serves the full web app
from pathlib import Path
from fastapi.staticfiles import StaticFiles

frontend_dir = Path(__file__).resolve().parent.parent / "frontend"
if frontend_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_dir), html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.models.entities import GeneratedDocument
from backend.app.schemas.common import DocumentRequest, DocumentResponse
from backend.app.services.ai.gemini_provider import GeminiProvider
from backend.app.services.ai.fallback_engine import FallbackEngine

router = APIRouter(prefix="/documents", tags=["Academic Document Drafter"])

@router.post("/generate", response_model=DocumentResponse)
def generate_academic_document(payload: DocumentRequest, db: Session = Depends(get_db)):
    """
    Drafts formal Leave Letters, Permissions, and Faculty Emails.
    Guarantees bracketed placeholders so personal identity is never forged.
    """
    gemini = GeminiProvider()
    output_text = None
    source = "gemini_live"

    if gemini.is_available():
        output_text = gemini.generate_document(
            doc_type=payload.type,
            context=payload.message,
            tone=payload.tone,
            length=payload.length
        )

    if not output_text:
        output_text = FallbackEngine.generate_document_template(
            doc_type=payload.type,
            context=payload.message,
            tone=payload.tone
        )
        source = "deterministic_template"

    # Persist document record
    try:
        doc = GeneratedDocument(
            document_type=payload.type,
            situation_context=payload.message,
            tone=payload.tone,
            content=output_text
        )
        db.add(doc)
        db.commit()
    except Exception:
        db.rollback()

    return DocumentResponse(
        output=output_text,
        type=payload.type,
        status="success",
        source=source
    )

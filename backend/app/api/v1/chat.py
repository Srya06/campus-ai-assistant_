from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.entities import Conversation, ConversationMessage
from backend.app.schemas.common import ChatRequest, ChatResponse, Citation
from backend.app.services.rag.rag_service import RAGService
from backend.app.services.ai.gemini_provider import GeminiProvider
from backend.app.services.ai.fallback_engine import FallbackEngine

router = APIRouter(prefix="/chat", tags=["Conversational AI"])

@router.post("", response_model=ChatResponse)
def handle_chat_message(payload: ChatRequest, db: Session = Depends(get_db)):
    """
    Main conversational endpoint:
    1. Loads grounded institutional context.
    2. Attempts live Gemini 2.5 Flash query.
    3. Seamlessly falls back to local deterministic knowledge if Gemini key is missing or offline.
    4. Persists conversation.
    """
    user_query = payload.message.strip()
    history_dicts = [{"role": m.role, "content": m.content} for m in payload.history]
    
    # 1. Retrieve RAG grounded context & potential citations
    system_instruction, rag_citations = RAGService.get_grounded_system_prompt(db, user_query)

    # 2. Try Gemini Provider
    gemini = GeminiProvider()
    response_text = None
    source = "gemini_live"
    is_fallback = False

    if gemini.is_available():
        response_text = gemini.generate_chat_response(
            prompt=user_query,
            system_instruction=system_instruction,
            history=history_dicts
        )

    # 3. Fallback if Gemini unavailable or failed
    if not response_text:
        fallback_text, fallback_citations = FallbackEngine.answer_query(db, user_query)
        response_text = fallback_text + "\n\n> *ℹ️ Note: Grounded response retrieved directly from the Verified Campus Knowledge Base.*"
        source = "offline_knowledge_base"
        is_fallback = True
        rag_citations = fallback_citations or rag_citations

    # 4. Persist conversation
    try:
        conv_id = payload.conversation_id
        if not conv_id:
            conv = Conversation(title=user_query[:50])
            db.add(conv)
            db.flush()
            conv_id = conv.id
        
        db.add(ConversationMessage(
            conversation_id=conv_id,
            role="user",
            content=user_query
        ))
        db.add(ConversationMessage(
            conversation_id=conv_id,
            role="model",
            content=response_text
        ))
        db.commit()
    except Exception:
        db.rollback()

    return ChatResponse(
        response=response_text,
        source=source,
        citations=rag_citations,
        is_fallback=is_fallback,
        conversation_id=conv_id
    )

@router.get("/conversations")
def list_conversations(db: Session = Depends(get_db)):
    convs = db.query(Conversation).order_by(Conversation.created_at.desc()).limit(20).all()
    return [{"id": c.id, "title": c.title, "created_at": c.created_at} for c in convs]

@router.get("/conversations/{conversation_id}")
def get_conversation_history(conversation_id: str, db: Session = Depends(get_db)):
    conv = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    messages = [
        {"role": m.role, "content": m.content, "created_at": m.created_at}
        for m in conv.messages
    ]
    return {"id": conv.id, "title": conv.title, "messages": messages}

import pytest
from backend.app.db.session import SessionLocal
from backend.app.api.v1.chat import handle_chat_message
from backend.app.schemas.common import ChatRequest

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_chat_fallback_when_gemini_unavailable(db_session):
    """Validates that chat returns grounded answers with fallback engine when Gemini is offline."""
    req = ChatRequest(
        message="What are the prerequisites for Machine Learning?",
        history=[]
    )
    res = handle_chat_message(payload=req, db=db_session)
    assert res.response is not None
    assert any(term in res.response for term in ["CS601", "Machine Learning", "MA301", "CS401"])
    assert len(res.citations) > 0
    assert res.is_fallback is True

def test_chat_timetable_query(db_session):
    req = ChatRequest(
        message="Show me CSE timetable for Monday",
        history=[]
    )
    res = handle_chat_message(payload=req, db=db_session)
    assert "Monday" in res.response
    assert any(slot in res.response for slot in ["09:00", "CS401", "Algorithms", "Operating Systems"])

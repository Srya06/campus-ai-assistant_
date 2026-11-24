import pytest
from backend.app.db.session import SessionLocal
from backend.app.api.v1.health import health_status, ai_status
from backend.app.api.v1.timetable import get_timetable
from backend.app.api.v1.courses import list_courses, get_prerequisites_graph
from backend.app.api.v1.exams import list_exam_notices
from backend.app.api.v1.faqs import list_faqs
from backend.app.api.v1.documents import generate_academic_document
from backend.app.schemas.common import DocumentRequest

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_health_endpoints():
    res = health_status()
    assert res["status"] == "healthy"
    assert "timestamp" in res

    ai_res = ai_status()
    assert ai_res["provider"] == "google-gemini-2.5-flash"
    assert "status" in ai_res

def test_timetable_filtering(db_session):
    # Test CSE Monday
    res = get_timetable(department="CSE", semester="Sem 4", day="Monday", db=db_session)
    assert res.department == "CSE"
    assert res.semester == "Sem 4"
    assert "Monday" in res.schedule
    assert len(res.schedule["Monday"]) > 0
    slot = res.schedule["Monday"][0]
    assert slot.faculty != ""
    assert slot.room != ""

    # Test ECE Tuesday (verified fix for Screenshot 1)
    ece_res = get_timetable(department="ECE", semester="Sem 4", day="Tuesday", db=db_session)
    assert ece_res.department == "ECE"
    assert "Tuesday" in ece_res.schedule
    assert len(ece_res.schedule["Tuesday"]) > 0
    ece_slot = ece_res.schedule["Tuesday"][0]
    assert ece_slot.code.startswith("EC")

def test_course_search(db_session):
    courses = list_courses(query="Algorithms", db=db_session)
    assert len(courses) > 0
    codes = [c.code for c in courses]
    assert "CS401" in codes or "CS201" in codes

def test_course_prerequisites_graph(db_session):
    graph = get_prerequisites_graph(course_id="CS601", db=db_session)
    assert graph.target_course.code == "CS601"
    prereq_codes = [p.code for p in graph.upstream_prerequisites]
    assert "CS401" in prereq_codes or "MA301" in prereq_codes

    # Test CS101 (verified fix for Screenshot 2)
    cs101_graph = get_prerequisites_graph(course_id="CS101", db=db_session)
    assert cs101_graph.target_course.code == "CS101"
    assert cs101_graph.course_code == "CS101"
    assert len(cs101_graph.upstream_prerequisites) == 0  # Entry course has no upstream prereqs

def test_exam_notices(db_session):
    notices = list_exam_notices(db=db_session)
    assert len(notices) >= 2
    assert any(n.notice_code == "EXAM-2026-01" for n in notices)

def test_administrative_faqs(db_session):
    faqs = list_faqs(search="scholarship", db=db_session)
    assert len(faqs) > 0
    assert any("scholarship" in f.question.lower() for f in faqs)

def test_document_generation(db_session):
    req = DocumentRequest(
        type="Leave Letter",
        message="Medical leave for viral fever for 2 days",
        tone="Formal",
        length="Medium"
    )
    res = generate_academic_document(payload=req, db=db_session)
    assert res.status == "success"
    assert "[Your Name]" in res.output
    assert "[Your Roll Number]" in res.output

import pytest
from fastapi import HTTPException
from backend.app.db.session import SessionLocal
from backend.app.models.entities import Course, CourseNote, Department
from backend.app.api.v1.auth import login
from backend.app.api.v1.admin import verify_admin, create_course, create_course_note
from backend.app.api.v1.notes import list_course_notes, get_note_by_id, download_note_pdf
from backend.app.schemas.common import LoginRequest

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_notes_listing_and_filtering(db_session):
    """Verify students can list and filter course study materials."""
    all_notes = list_course_notes(db=db_session)
    assert len(all_notes) >= 4

    # Filter by CS401
    cs401_notes = list_course_notes(course_code="CS401", db=db_session)
    assert len(cs401_notes) >= 2
    for n in cs401_notes:
        assert "CS401" in n.course_code

    # Search by keyword "Dynamic Programming"
    dp_notes = list_course_notes(search="Dynamic Programming", db=db_session)
    assert len(dp_notes) >= 1
    assert any("Dynamic Programming" in n.title for n in dp_notes)

def test_notes_pdf_download_and_counter(db_session):
    """Verify PDF streaming and download count incrementation."""
    first_note = db_session.query(CourseNote).first()
    assert first_note is not None
    initial_downloads = first_note.download_count or 0

    # Trigger PDF download endpoint
    response = download_note_pdf(note_id=first_note.id, db=db_session)
    assert response.status_code == 200
    assert response.media_type == "application/pdf"
    assert response.body.startswith(b"%PDF")

    # Verify download count incremented
    db_session.refresh(first_note)
    assert first_note.download_count == initial_downloads + 1

def test_admin_publish_course_and_notes(db_session):
    """Verify administrator can add courses and publish official notes."""
    # 1. Login as admin
    login_res = login(payload=LoginRequest(username="admin", password="admin123"), db=db_session)
    admin_payload = verify_admin(authorization=f"Bearer {login_res.access_token}")

    # 2. Add course
    course_res = create_course(
        data={
            "code": "CS750",
            "title": "Distributed Cloud Infrastructure",
            "credits": 4,
            "semester_number": 7,
            "description": "Raft, Paxos, Kubernetes, Distributed Storage."
        },
        db=db_session,
        admin_user=admin_payload
    )
    assert course_res["status"] == "success"
    assert course_res["code"] == "CS750"

    # 3. Add course note for newly created course
    note_res = create_course_note(
        data={
            "course_code": "CS750",
            "unit_number": 1,
            "unit_title": "Consensus & Fault Tolerance",
            "title": "Raft and Paxos Consensus Protocols",
            "topic_description": "Leader election, log replication, safety invariants.",
            "content_markdown": "# Unit 1: Distributed Consensus\n\n## 1. Raft Protocol\nRaft decomposes consensus into:\n- Leader election\n- Log replication\n- Safety invariants.",
            "faculty_author": "Dr. Sharma"
        },
        db=db_session,
        admin_user=admin_payload
    )
    assert note_res["status"] == "success"
    assert note_res["course_code"] == "CS750"

    # 4. Verify note is downloadable
    pdf_res = download_note_pdf(note_id=note_res["note_id"], db=db_session)
    assert pdf_res.body.startswith(b"%PDF")
    assert len(pdf_res.body) > 1000

def test_unauthorized_user_cannot_publish_note(db_session):
    """Students or unauthenticated callers must be rejected with 401 or 403."""
    # Without token
    with pytest.raises(HTTPException) as exc_info:
        verify_admin(authorization=None)
    assert exc_info.value.status_code == 401

    # Student token
    student_login = login(payload=LoginRequest(username="student", password="student123"), db=db_session)
    with pytest.raises(HTTPException) as exc_info:
        verify_admin(authorization=f"Bearer {student_login.access_token}")
    assert exc_info.value.status_code == 403

import pytest
from fastapi import HTTPException
from backend.app.db.session import SessionLocal
from backend.app.api.v1.auth import login
from backend.app.api.v1.admin import verify_admin, create_course
from backend.app.schemas.common import LoginRequest

@pytest.fixture
def db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_admin_route_without_token():
    """Unauthenticated request without bearer token must raise 401."""
    with pytest.raises(HTTPException) as exc_info:
        verify_admin(authorization=None)
    assert exc_info.value.status_code == 401

def test_admin_route_with_invalid_token():
    with pytest.raises(HTTPException) as exc_info:
        verify_admin(authorization="Bearer invalid_garbage_token")
    assert exc_info.value.status_code == 403

def test_admin_login_and_access(db_session):
    # 1. Login with admin credentials
    login_req = LoginRequest(username="admin", password="admin123")
    token_res = login(payload=login_req, db=db_session)
    assert token_res.access_token is not None
    assert token_res.role == "admin"

    # 2. Verify token
    admin_payload = verify_admin(authorization=f"Bearer {token_res.access_token}")
    assert admin_payload["role"] == "admin"

    # 3. Create course through admin handler
    course_data = {
        "department_id": "test-dept-id",
        "code": "CS888",
        "title": "Quantum Computing & Quantum Algorithms",
        "credits": 4,
        "semester_number": 8,
        "description": "Foundations of quantum information theory."
    }
    result = create_course(data=course_data, db=db_session, admin_user=admin_payload)
    assert result["status"] == "success"
    assert result["code"] == "CS888"

def test_student_and_admin_registration(db_session):
    from backend.app.api.v1.auth import register
    from backend.app.schemas.common import RegisterRequest
    import uuid

    uid = str(uuid.uuid4())[:6]
    # 1. Register student
    student_req = RegisterRequest(
        username=f"student_{uid}",
        email=f"student_{uid}@campus.edu",
        password="securepass123",
        full_name="Priya Patel",
        role="student",
        department="CSE (AI)",
        semester="Sem 5"
    )
    student_res = register(payload=student_req, db=db_session)
    assert student_res.access_token is not None
    assert student_res.role == "student"
    assert student_res.full_name == "Priya Patel"
    assert student_res.department == "CSE (AI)"

    # 2. Login newly registered student
    login_req = LoginRequest(username=f"student_{uid}", password="securepass123")
    login_res = login(payload=login_req, db=db_session)
    assert login_res.full_name == "Priya Patel"
    assert login_res.role == "student"

    # 3. Duplicate username rejection
    with pytest.raises(HTTPException) as exc_info:
        register(payload=student_req, db=db_session)
    assert exc_info.value.status_code == 400

    # 4. Admin minimal registration (only email and password)
    admin_uid = str(uuid.uuid4())[:6]
    admin_req = RegisterRequest(
        email=f"admin_{admin_uid}@campus.edu",
        password="adminpassword123",
        role="admin"
    )
    admin_res = register(payload=admin_req, db=db_session)
    assert admin_res.role == "admin"
    assert admin_res.email == f"admin_{admin_uid}@campus.edu"

    # 5. Student profile update (CGPA, resume, skills)
    from backend.app.api.v1.auth import update_student_profile
    from backend.app.schemas.common import StudentProfileUpdateRequest

    update_payload = StudentProfileUpdateRequest(
        full_name="Priya Patel Updated",
        roll_number="22AI999",
        cgpa="9.2",
        resume_url="https://campus.edu/resumes/priya_resume.pdf",
        skills="Python, PyTorch, LangChain, React",
        phone="+91 99999 88888"
    )
    updated_profile = update_student_profile(
        payload=update_payload,
        user_id=student_res.user_id,
        db=db_session
    )
    assert updated_profile.full_name == "Priya Patel Updated"
    assert updated_profile.roll_number == "22AI999"
    assert updated_profile.cgpa == "9.2"
    assert updated_profile.resume_url == "https://campus.edu/resumes/priya_resume.pdf"
    assert "PyTorch" in updated_profile.skills

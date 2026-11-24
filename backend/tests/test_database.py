import pytest
from backend.app.db.session import SessionLocal
from backend.app.models.entities import Course, TimetableEntry, ExamNotice, AdministrativeFAQ, User

def test_database_counts():
    db = SessionLocal()
    try:
        assert db.query(Course).count() >= 10, "Should have seeded courses"
        assert db.query(TimetableEntry).count() >= 15, "Should have seeded timetable slots"
        assert db.query(ExamNotice).count() >= 2, "Should have seeded exam notices"
        assert db.query(AdministrativeFAQ).count() >= 5, "Should have seeded administrative FAQs"
        assert db.query(User).count() >= 2, "Should have seeded admin and student users"
    finally:
        db.close()

def test_course_prerequisite_structure():
    db = SessionLocal()
    try:
        ml = db.query(Course).filter(Course.code == "CS601").first()
        assert ml is not None
        assert "CS401" in ml.prerequisites_text
        assert "MA301" in ml.prerequisites_text
    finally:
        db.close()

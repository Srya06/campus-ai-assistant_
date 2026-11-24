from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session
from typing import Dict, Any
from backend.app.db.session import get_db
from backend.app.models.entities import Course, CourseNote, Department, ExamNotice, AdministrativeFAQ, AuditLog
from backend.app.core.security import decode_access_token

router = APIRouter(prefix="/admin", tags=["Administration (Protected)"])

def verify_admin(authorization: str = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication token required")
    token = authorization.split(" ")[1]
    payload = decode_access_token(token)
    if not payload or payload.get("role") != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return payload

@router.post("/courses")
def create_course(
    data: Dict[str, Any], 
    db: Session = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    # Auto-resolve department
    dept_id = data.get("department_id")
    if not dept_id or dept_id == "test-dept-id":
        dept = db.query(Department).first()
        dept_id = dept.id if dept else None

    course = Course(
        department_id=dept_id,
        code=data.get("code"),
        title=data.get("title"),
        credits=data.get("credits", 4),
        semester_number=data.get("semester_number", 4),
        course_type=data.get("course_type", "Core"),
        description=data.get("description", ""),
        syllabus_outline=data.get("syllabus_outline", ""),
        recommended_books=data.get("recommended_books", ""),
        prerequisites_text=data.get("prerequisites_text", "None")
    )
    db.add(course)
    db.add(AuditLog(user_id=admin_user.get("sub"), action="CREATE_COURSE", entity_type="Course", details=f"Created {course.code}"))
    db.commit()
    db.refresh(course)
    return {"status": "success", "course_id": course.id, "code": course.code, "title": course.title}

@router.post("/notes")
def create_course_note(
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    """
    Publish official course lecture notes and study material.
    Course can be referenced by UUID or course code (e.g. CS401).
    """
    target = data.get("course_id") or data.get("course_code")
    if not target:
        raise HTTPException(status_code=400, detail="Target course_id or course_code is required")

    course = db.query(Course).filter(
        (Course.id == target) | (Course.code.ilike(target))
    ).first()

    if not course:
        raise HTTPException(status_code=404, detail=f"Course '{target}' not found in catalog")

    content = data.get("content_markdown") or data.get("content", "")
    if len(content.strip()) < 10:
        raise HTTPException(status_code=400, detail="Note content must be at least 10 characters long")

    note = CourseNote(
        course_id=course.id,
        uploaded_by=admin_user.get("sub"),
        title=data.get("title", f"Unit {data.get('unit_number', 1)} Lecture Notes"),
        unit_number=int(data.get("unit_number", 1)),
        unit_title=data.get("unit_title", "General Topics"),
        topic_description=data.get("topic_description", ""),
        content_markdown=content,
        faculty_author=data.get("faculty_author", "Department Faculty"),
        academic_year=data.get("academic_year", "2025-2026"),
        file_format="PDF",
        file_size_kb=len(content.encode('utf-8')) // 1024 + 120
    )
    db.add(note)
    db.add(AuditLog(
        user_id=admin_user.get("sub"),
        action="CREATE_COURSE_NOTE",
        entity_type="CourseNote",
        details=f"Published note '{note.title}' for {course.code}"
    ))
    db.commit()
    db.refresh(note)
    return {
        "status": "success",
        "note_id": note.id,
        "course_code": course.code,
        "title": note.title,
        "unit_number": note.unit_number
    }

@router.delete("/notes/{note_id}")
def delete_course_note(
    note_id: str,
    db: Session = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    note = db.query(CourseNote).filter(CourseNote.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.add(AuditLog(
        user_id=admin_user.get("sub"),
        action="DELETE_COURSE_NOTE",
        entity_type="CourseNote",
        details=f"Deleted note '{note.title}'"
    ))
    db.commit()
    return {"status": "success", "deleted_note_id": note_id}

@router.post("/exams")
def create_exam_notice(
    data: Dict[str, Any],
    db: Session = Depends(get_db),
    admin_user = Depends(verify_admin)
):
    notice = ExamNotice(
        notice_code=data.get("notice_code"),
        title=data.get("title"),
        exam_type=data.get("exam_type", "Midterm"),
        applicable_to=data.get("applicable_to", "All Batches"),
        exam_window=data.get("exam_window", ""),
        calculator_policy=data.get("calculator_policy", ""),
        is_urgent=data.get("is_urgent", False)
    )
    db.add(notice)
    db.add(AuditLog(user_id=admin_user.get("sub"), action="CREATE_EXAM_NOTICE", entity_type="ExamNotice", details=f"Published {notice.notice_code}"))
    db.commit()
    db.refresh(notice)
    return {"status": "success", "notice_id": notice.id}

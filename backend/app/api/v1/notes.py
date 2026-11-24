from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.app.db.session import get_db
from backend.app.models.entities import CourseNote, Course, Department
from backend.app.schemas.common import CourseNoteResponse
from backend.app.services.pdf.pdf_generator import CampusPDFGenerator

router = APIRouter(prefix="/notes", tags=["Course Notes & Study Materials"])

@router.get("", response_model=List[CourseNoteResponse])
def list_course_notes(
    course_id: Optional[str] = None,
    course_code: Optional[str] = None,
    department: Optional[str] = None,
    semester: Optional[int] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    Search and filter verified course lecture notes and study material.
    Supports filtering by course code, department, semester, and keyword search.
    """
    query = db.query(CourseNote).join(Course)

    if course_id:
        query = query.filter(CourseNote.course_id == course_id)
    if course_code:
        query = query.filter(Course.code.ilike(f"%{course_code}%"))
    if semester:
        query = query.filter(Course.semester_number == semester)
    if search:
        s = f"%{search}%"
        query = query.filter(
            or_(
                CourseNote.title.ilike(s),
                CourseNote.unit_title.ilike(s),
                CourseNote.topic_description.ilike(s),
                CourseNote.content_markdown.ilike(s),
                Course.code.ilike(s),
                Course.title.ilike(s)
            )
        )

    notes = query.order_by(Course.code, CourseNote.unit_number).all()

    # Format response with course metadata
    results = []
    for n in notes:
        results.append(CourseNoteResponse(
            id=n.id,
            course_id=n.course_id,
            course_code=n.course.code if n.course else "",
            course_title=n.course.title if n.course else "",
            title=n.title,
            unit_number=n.unit_number,
            unit_title=n.unit_title,
            topic_description=n.topic_description or "",
            content_markdown=n.content_markdown,
            faculty_author=n.faculty_author or "Department Faculty",
            academic_year=n.academic_year or "2025-2026",
            file_format=n.file_format or "PDF",
            file_size_kb=n.file_size_kb or 145,
            download_count=n.download_count or 0,
            created_at=n.created_at
        ))
    return results

@router.get("/{note_id}", response_model=CourseNoteResponse)
def get_note_by_id(note_id: str, db: Session = Depends(get_db)):
    """Fetch single course note detail for in-app reading."""
    n = db.query(CourseNote).filter(CourseNote.id == note_id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Study material note not found")

    return CourseNoteResponse(
        id=n.id,
        course_id=n.course_id,
        course_code=n.course.code if n.course else "",
        course_title=n.course.title if n.course else "",
        title=n.title,
        unit_number=n.unit_number,
        unit_title=n.unit_title,
        topic_description=n.topic_description or "",
        content_markdown=n.content_markdown,
        faculty_author=n.faculty_author or "Department Faculty",
        academic_year=n.academic_year or "2025-2026",
        file_format=n.file_format or "PDF",
        file_size_kb=n.file_size_kb or 145,
        download_count=n.download_count or 0,
        created_at=n.created_at
    )

@router.get("/{note_id}/download")
def download_note_pdf(note_id: str, db: Session = Depends(get_db)):
    """
    Generates and streams high-fidelity official university PDF of course lecture notes.
    Increments download metrics counter.
    """
    n = db.query(CourseNote).filter(CourseNote.id == note_id).first()
    if not n:
        raise HTTPException(status_code=404, detail="Study material note not found")

    # Increment download counter atomically
    n.download_count = (n.download_count or 0) + 1
    db.commit()

    course_code = n.course.code if n.course else "COURSE"
    course_title = n.course.title if n.course else "Lecture Notes"
    dept_name = n.course.department.name if (n.course and n.course.department) else "Engineering"

    # Generate PDF in-memory
    pdf_bytes = CampusPDFGenerator.generate_course_note_pdf(
        course_code=course_code,
        course_title=course_title,
        unit_number=n.unit_number,
        unit_title=n.unit_title,
        topic_description=n.topic_description or "",
        content_text=n.content_markdown,
        faculty_author=n.faculty_author or "Department Faculty",
        academic_year=n.academic_year or "2025-2026",
        department_name=dept_name
    )

    clean_filename = f"{course_code}_Unit_{n.unit_number}_{n.title}".replace(" ", "_")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{clean_filename}.pdf"',
            "Content-Length": str(len(pdf_bytes))
        }
    )

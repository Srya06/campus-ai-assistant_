from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.db.session import get_db
from backend.app.models.entities import Course, CoursePrerequisite
from backend.app.schemas.common import CourseResponse, CoursePrerequisiteGraph, PrerequisiteNode

router = APIRouter(prefix="/courses", tags=["Courses & Prerequisites"])

@router.get("", response_model=List[CourseResponse])
def list_courses(
    query: Optional[str] = Query(None, description="Search term for code or title"),
    semester: Optional[int] = Query(None, description="Filter by semester number"),
    db: Session = Depends(get_db)
):
    q = db.query(Course)
    if semester is not None and isinstance(semester, int):
        q = q.filter(Course.semester_number == semester)
    courses = q.all()

    if query and isinstance(query, str):
        query_str = query.lower()
        courses = [
            c for c in courses 
            if query_str in c.code.lower() or query_str in c.title.lower() or query_str in (c.description or "").lower()
        ]

    return courses

@router.get("/{course_id}/prerequisites", response_model=CoursePrerequisiteGraph)
def get_prerequisites_graph(course_id: str, db: Session = Depends(get_db)):
    course = db.query(Course).filter((Course.id == course_id) | (Course.code == course_id)).first()
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # Upstream prerequisites (courses this course requires)
    upstream_links = db.query(CoursePrerequisite).filter(CoursePrerequisite.course_id == course.id).all()
    upstream_nodes = []
    strict_nodes = []
    for link in upstream_links:
        prereq = db.query(Course).filter(Course.id == link.prerequisite_course_id).first()
        if prereq:
            node = PrerequisiteNode(
                code=prereq.code,
                title=prereq.title,
                is_strict=link.is_strict,
                credits=prereq.credits,
                semester_number=prereq.semester_number
            )
            upstream_nodes.append(node)
            if link.is_strict:
                strict_nodes.append(node)

    # Downstream courses (courses that require this course)
    downstream_links = db.query(CoursePrerequisite).filter(CoursePrerequisite.prerequisite_course_id == course.id).all()
    downstream_nodes = []
    for link in downstream_links:
        dependent = db.query(Course).filter(Course.id == link.course_id).first()
        if dependent:
            downstream_nodes.append(PrerequisiteNode(
                code=dependent.code,
                title=dependent.title,
                is_strict=link.is_strict,
                credits=dependent.credits,
                semester_number=dependent.semester_number
            ))

    return CoursePrerequisiteGraph(
        target_course=course,
        course_code=course.code,
        course_title=course.title,
        strict_prerequisites=strict_nodes,
        co_requisites=[],
        upstream_prerequisites=upstream_nodes,
        downstream_dependent_courses=downstream_nodes
    )

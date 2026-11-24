from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional, Dict, List
from backend.app.db.session import get_db
from backend.app.models.entities import TimetableEntry, Department, Course
from backend.app.schemas.common import TimetableResponse, TimetableSlot

router = APIRouter(prefix="/timetable", tags=["Timetables"])

@router.get("", response_model=TimetableResponse)
def get_timetable(
    department: str = Query("CSE", description="Department code, e.g. CSE, ECE"),
    semester: str = Query("Sem 4", description="Semester label, e.g. Sem 4, Sem 6"),
    day: Optional[str] = Query(None, description="Optional filter by day, e.g. Monday"),
    day_of_week: Optional[str] = Query(None, description="Alternative parameter for day filter"),
    db: Session = Depends(get_db)
):
    dept_query = (department or "CSE").strip()
    sem_query = (semester or "Sem 4").strip()
    target_day = day or day_of_week

    query = (
        db.query(TimetableEntry)
        .join(Department, TimetableEntry.department_id == Department.id)
        .join(Course, TimetableEntry.course_id == Course.id)
        .filter(
            (Department.code.ilike(f"%{dept_query}%")) |
            (Department.name.ilike(f"%{dept_query}%"))
        )
    )
    
    if "4" in sem_query:
        query = query.filter((TimetableEntry.semester_label == "Sem 4") | (TimetableEntry.semester_label.ilike("%4%")))
    elif "6" in sem_query:
        query = query.filter((TimetableEntry.semester_label == "Sem 6") | (TimetableEntry.semester_label.ilike("%6%")))
    else:
        query = query.filter(TimetableEntry.semester_label == sem_query)

    if target_day and target_day.upper() != "ALL":
        # Extract clean day name, e.g. "Tuesday (Today)" -> "Tuesday"
        clean_day = target_day.split()[0].capitalize()
        query = query.filter(TimetableEntry.day_of_week.ilike(f"%{clean_day}%"))

    entries = query.all()
    
    schedule: Dict[str, List[TimetableSlot]] = {}
    for e in entries:
        day_key = e.day_of_week
        if day_key not in schedule:
            schedule[day_key] = []

        times = (e.time_slot or "").split("-")
        s_time = times[0].strip() if len(times) > 0 else "09:00 AM"
        e_time = times[1].strip() if len(times) > 1 else "10:00 AM"
        c_title = e.course.title if e.course else "Class Lecture"
        c_code = e.course.code if e.course else "CS"
        
        schedule[day_key].append(TimetableSlot(
            time=e.time_slot,
            subject=c_title,
            code=c_code,
            faculty=e.faculty_name,
            room=e.room_number,
            is_lab=e.is_lab,
            start_time=s_time,
            end_time=e_time,
            course_title=c_title,
            course_code=c_code,
            room_number=e.room_number,
            faculty_name=e.faculty_name,
            course_type="Laboratory" if e.is_lab else "Lecture"
        ))

    return TimetableResponse(
        department=dept_query,
        semester=sem_query,
        schedule=schedule
    )

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.app.db.session import get_db
from backend.app.models.entities import ExamNotice
from backend.app.schemas.common import ExamNoticeResponse

router = APIRouter(prefix="/exams", tags=["Examinations"])

@router.get("", response_model=List[ExamNoticeResponse])
def list_exam_notices(db: Session = Depends(get_db)):
    notices = db.query(ExamNotice).order_by(ExamNotice.is_urgent.desc()).all()
    return notices

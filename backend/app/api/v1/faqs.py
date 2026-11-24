from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from backend.app.db.session import get_db
from backend.app.models.entities import AdministrativeFAQ
from backend.app.schemas.common import AdministrativeFAQResponse

router = APIRouter(prefix="/faqs", tags=["Administrative FAQs"])

@router.get("", response_model=List[AdministrativeFAQResponse])
def list_faqs(
    category: Optional[str] = Query(None, description="Category filter"),
    search: Optional[str] = Query(None, description="Search term"),
    db: Session = Depends(get_db)
):
    q = db.query(AdministrativeFAQ)
    if category and isinstance(category, str) and category != "All":
        q = q.filter(AdministrativeFAQ.category == category)
    faqs = q.all()

    if search and isinstance(search, str):
        s = search.lower()
        faqs = [
            f for f in faqs 
            if s in f.question.lower() or s in f.answer.lower() or s in f.category.lower()
        ]

    return faqs

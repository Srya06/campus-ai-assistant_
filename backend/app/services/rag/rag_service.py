import logging
import json
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    Course, TimetableEntry, ExamNotice, AdministrativeFAQ, Institution
)
from backend.app.schemas.common import Citation

logger = logging.getLogger("rag_service")

class RAGService:
    @staticmethod
    def get_grounded_system_prompt(db: Session, user_query: str) -> Tuple[str, List[Citation]]:
        """
        Retrieves relevant database records and packages them into a strict,
        grounded system instruction preventing hallucination.
        """
        inst = db.query(Institution).first()
        inst_name = inst.name if inst else "Apex Institute of Technology & Engineering"
        
        # Query database for knowledge context
        courses = db.query(Course).all()
        course_data = [
            {
                "code": c.code,
                "title": c.title,
                "credits": c.credits,
                "semester": c.semester_number,
                "prerequisites": c.prerequisites_text,
                "description": c.description,
                "books": c.recommended_books
            }
            for c in courses
        ]

        tt_entries = db.query(TimetableEntry).join(Course).all()
        timetable_data = [
            {
                "day": e.day_of_week,
                "time": e.time_slot,
                "course": e.course.title if e.course else "",
                "code": e.course.code if e.course else "",
                "faculty": e.faculty_name,
                "room": e.room_number,
                "is_lab": e.is_lab
            }
            for e in tt_entries
        ]

        exams = db.query(ExamNotice).all()
        exam_data = [
            {
                "notice_code": ex.notice_code,
                "title": ex.title,
                "applicable_to": ex.applicable_to,
                "window": ex.exam_window,
                "deadline": ex.deadline,
                "calculator_policy": ex.calculator_policy,
                "hall_ticket": ex.hall_ticket_guidelines
            }
            for ex in exams
        ]

        faqs = db.query(AdministrativeFAQ).all()
        faq_data = [
            {
                "category": f.category,
                "question": f.question,
                "answer": f.answer,
                "location": f.office_location,
                "contact": f.contact_email
            }
            for f in faqs
        ]

        citations: List[Citation] = []
        q_lower = user_query.lower()
        
        # Collect relevant citations based on query
        for c in courses:
            if c.code.lower() in q_lower or any(term in c.title.lower() for term in q_lower.split() if len(term) > 3):
                citations.append(Citation(type="course", title=f"{c.code}: {c.title}", reference_id=c.code))
        
        for ex in exams:
            if any(term in ex.title.lower() for term in q_lower.split() if len(term) > 3) or "exam" in q_lower:
                citations.append(Citation(type="exam", title=ex.title, reference_id=ex.notice_code))
                break

        if not citations and any(w in q_lower for w in ["timetable", "schedule", "class"]):
            citations.append(Citation(type="timetable", title="Official Academic Timetable"))

        knowledge_payload = {
            "institution": inst_name,
            "courses": course_data,
            "timetables": timetable_data,
            "examination_notices": exam_data,
            "administrative_faqs": faq_data
        }

        system_instruction = f"""You are the official Campus AI Assistant for {inst_name}.
You are a student-centric conversational academic navigator and advisor.

GROUND TRUTH INSTITUTIONAL KNOWLEDGE BASE:
```json
{json.dumps(knowledge_payload, indent=2)}
```

STRICT OPERATING INSTRUCTIONS:
1. Always ground your responses in the verified knowledge base provided above.
2. If a student asks for information not present in the institutional knowledge base, state clearly and transparently: "I cannot verify that information in the current official campus records. Please consult the respective department office."
3. NEVER fabricate dates, room numbers, or exam regulations.
4. When answering timetable inquiries, format the output clearly in a Markdown table.
5. When answering prerequisite inquiries, clearly state the required prior courses and why they are necessary.
6. When drafting emails or letters, include professional placeholders such as [Your Name], [Roll Number], and [Department].
7. Keep responses concise, supportive, and formatted with clean Markdown bolding, tables, and bullet points.
"""
        return system_instruction, citations

import logging
import datetime
from typing import Dict, Any, List, Tuple
from sqlalchemy.orm import Session
from backend.app.models.entities import (
    Course, TimetableEntry, ExamNotice, AdministrativeFAQ
)
from backend.app.schemas.common import Citation

logger = logging.getLogger("fallback_engine")

class FallbackEngine:
    """
    Deterministic Knowledge Retrieval Engine.
    Executes when the Gemini API key is unconfigured, rate-limited, or offline.
    Directly queries the normalized database and formats rich academic responses.
    """

    @staticmethod
    def answer_query(db: Session, query: str) -> Tuple[str, List[Citation]]:
        q = query.lower()
        citations: List[Citation] = []

        # 1. Timetable Queries
        if any(w in q for w in ["timetable", "schedule", "class", "lecture", "timing", "slot", "lab", "monday", "tuesday", "wednesday", "thursday", "friday", "today", "tomorrow"]):
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            matched_day = next((d for d in days if d.lower() in q), None)
            
            # Filter entries
            query_filter = db.query(TimetableEntry).join(Course)
            if matched_day:
                query_filter = query_filter.filter(TimetableEntry.day_of_week == matched_day)
            
            entries = query_filter.limit(15).all()
            if entries:
                citations.append(Citation(type="timetable", title="Academic Timetable Schedule"))
                res = f"### 📅 Academic Timetable Schedule ({matched_day or 'Weekly Overview'})\n\n"
                res += "| Day | Time | Subject | Faculty | Venue |\n|---|---|---|---|---|\n"
                for e in entries:
                    subject = e.course.title if e.course else "Lecture"
                    res += f"| {e.day_of_week} | `{e.time_slot}` | **{subject}** ({e.course.code}) | {e.faculty_name} | `{e.room_number}` |\n"
                return res, citations

        # 2. Course & Prerequisite Queries
        if any(w in q for w in ["prereq", "prerequisite", "course", "credit", "syllabus", "book", "algorithm", "os", "operating", "machine learning", "compiler", "network", "database"]):
            courses = db.query(Course).all()
            matched_courses = []
            for c in courses:
                if c.code.lower() in q or any(term in c.title.lower() for term in q.split() if len(term) > 3):
                    matched_courses.append(c)
            
            if not matched_courses:
                matched_courses = courses[:3]

            res = "### 📚 Course Curriculum & Prerequisites\n\n"
            for c in matched_courses:
                citations.append(Citation(type="course", title=f"{c.code}: {c.title}", reference_id=c.code))
                res += f"#### **{c.code}: {c.title}** ({c.credits} Credits - Sem {c.semester_number})\n"
                res += f"- **Prerequisites Required**: `{c.prerequisites_text or 'None (Open Entry)'}`\n"
                res += f"- **Description**: {c.description}\n"
                if c.recommended_books:
                    res += f"- **Recommended Books**: {c.recommended_books}\n"
                res += "\n"
            return res, citations

        # 3. Examination Queries
        if any(w in q for w in ["exam", "midterm", "final", "test", "hall ticket", "calculator", "malpractice", "backlog", "date sheet"]):
            exams = db.query(ExamNotice).all()
            res = "### 📢 Examination Notices & Regulations\n\n"
            for ex in exams:
                citations.append(Citation(type="exam", title=ex.title, reference_id=ex.notice_code))
                res += f"#### 📝 **{ex.title}**\n"
                if ex.exam_window:
                    res += f"- **Exam Window**: {ex.exam_window}\n"
                if ex.deadline:
                    res += f"- **Deadline**: {ex.deadline}\n"
                if ex.calculator_policy:
                    res += f"- **Calculator Policy**: {ex.calculator_policy}\n"
                if ex.hall_ticket_guidelines:
                    res += f"- **Hall Ticket Guidelines**: {ex.hall_ticket_guidelines}\n"
                res += "\n"
            return res, citations

        # 4. Administrative Queries (fees, scholarships, library, hostel, bonafide)
        faqs = db.query(AdministrativeFAQ).all()
        matched_faqs = []
        for f in faqs:
            if (f.category.lower() in q) or any(term in f.question.lower() or term in f.answer.lower() for term in q.split() if len(term) > 3):
                matched_faqs.append(f)

        if not matched_faqs and any(w in q for w in ["fee", "scholarship", "library", "hostel", "bonafide", "attendance", "ragging"]):
            matched_faqs = faqs[:2]

        if matched_faqs:
            res = "### 🏢 Administrative & Student Services Information\n\n"
            for f in matched_faqs:
                citations.append(Citation(type="faq", title=f.category, reference_id=f.id))
                res += f"#### 📌 **{f.category}: {f.question}**\n"
                res += f"{f.answer}\n\n"
                if f.office_location:
                    res += f"📍 **Location / Office**: `{f.office_location}`\n"
                if f.contact_email:
                    res += f"✉️ **Contact**: {f.contact_email} | {f.contact_phone}\n\n"
            return res, citations

        # Fallback helpful navigation guide
        res = (
            "### 🎓 Campus AI Assistant (Verified Campus Knowledge Base)\n\n"
            "I could not locate an exact match for that inquiry in the current institutional records. Here is what I can help you with:\n\n"
            "- 📅 **Academic Timetables**: Ask *'Show me CSE 4th semester timetable'* or *'When is Algorithms Lab?'*\n"
            "- 📚 **Course Prerequisites**: Ask *'What are the prerequisites for Machine Learning (CS601)?'*\n"
            "- 📢 **Examination Notices**: Ask *'What are the calculator rules for Mid-Sem exams?'*\n"
            "- 🏢 **Administrative Services**: Ask *'How do I apply for a scholarship or bonafide certificate?'*\n"
            "- ✍️ **Formal Document Drafting**: Use the **Academic Letter Drafter** tab to generate official leave applications."
        )
        return res, citations

    @staticmethod
    def generate_document_template(doc_type: str, context: str, tone: str) -> str:
        date_str = datetime.date.today().strftime("%B %d, %Y")

        if "leave" in doc_type.lower():
            return f"""Date: {date_str}

To,
The Head of the Department,
Department of Computer Science & Engineering,
Apex Institute of Technology & Engineering.

Subject: Application for Leave of Absence - Reg.

Respected Sir/Madam,

I am writing to formally request a leave of absence from classes regarding the following circumstance:
"{context}"

I assure you that I will coordinate with my professors and peers to complete any missed assignments, laboratory sessions, and coursework promptly upon my return.

I kindly request you to grant me leave for the specified duration and regularize my attendance.

Thanking you.

Yours sincerely,
[Your Name]
Roll No: [Your Roll Number]
Semester & Section: [e.g. 4th Sem, CSE-A]
Contact No: [Your Phone Number]"""

        elif "permission" in doc_type.lower():
            return f"""Date: {date_str}

To,
The Dean of Academic Affairs / Faculty Advisor,
Apex Institute of Technology & Engineering.

Subject: Request for Official Permission / On-Duty Attendance - Reg.

Respected Sir/Madam,

I am writing to formally seek your kind permission regarding:
"{context}"

I understand institutional regulations and assure you that this engagement will not compromise my academic performance and regular coursework requirements.

I respectfully request your approval and authorization for on-duty (OD) attendance.

Thank you for your consideration.

Yours respectfully,
[Your Name]
Roll No: [Your Roll Number]
Department: [Your Department]"""

        elif "email" in doc_type.lower():
            return f"""Subject: Academic Query Regarding Coursework - [Your Name] (Roll: [Your Roll No])

Respected Professor / Sir / Madam,

I hope this email finds you well.

I am reaching out regarding the following academic matter:
{context}

Could you please provide your guidance or advise on the appropriate steps forward? If a brief meeting or discussion is required, I am available at your convenience during your office hours.

Thank you very much for your time and assistance.

Sincerely,
[Your Name]
Roll Number: [Your Roll Number]
Department of Computer Science & Engineering
Apex Institute of Technology & Engineering"""

        else:
            return f"""Date: {date_str}

To Whom It May Concern,
Apex Institute of Technology & Engineering.

Subject: Official Request Regarding {doc_type}

Respected Authority,

This formal communication is submitted regarding the following matter:
{context}

Please process this request in accordance with institutional guidelines.

Yours faithfully,
[Your Name]
Roll No: [Your Roll Number]
Department: [Your Department]"""

from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

# Auth Schemas
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    username: str
    role: str
    full_name: Optional[str] = ""
    email: Optional[str] = ""
    roll_number: Optional[str] = ""
    department: Optional[str] = "CSE (AI)"
    semester: Optional[str] = "Sem 5"
    cgpa: Optional[str] = "8.0"
    resume_url: Optional[str] = ""
    skills: Optional[str] = ""
    phone: Optional[str] = ""

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: Optional[str] = None
    email: str
    password: str
    full_name: Optional[str] = ""
    role: str = "student" # 'student' or 'admin'
    roll_number: Optional[str] = ""
    department: Optional[str] = "Computer Science & Engineering (AI)"
    semester: Optional[str] = "Sem 5 (CSE - AI)"
    cgpa: Optional[str] = "8.0"
    resume_url: Optional[str] = ""
    skills: Optional[str] = ""
    phone: Optional[str] = ""

class StudentProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    roll_number: Optional[str] = None
    department: Optional[str] = None
    semester: Optional[str] = None
    cgpa: Optional[str] = None
    resume_url: Optional[str] = None
    skills: Optional[str] = None
    phone: Optional[str] = None

class UserResponse(BaseSchema):
    id: str
    username: str
    email: str
    full_name: Optional[str] = None
    role: str
    roll_number: Optional[str] = ""
    department: Optional[str] = "CSE (AI)"
    semester: Optional[str] = "Sem 5"
    cgpa: Optional[str] = "8.0"
    resume_url: Optional[str] = ""
    skills: Optional[str] = ""
    phone: Optional[str] = ""

# Chat Schemas
class MessageHistoryItem(BaseModel):
    role: str = Field(..., description="'user' or 'model'")
    content: str

class Citation(BaseModel):
    type: str # 'course', 'timetable', 'exam', 'faq'
    title: str
    reference_id: Optional[str] = None
    source: str = "Apex Institute Verified Campus DB"

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    history: Optional[List[MessageHistoryItem]] = Field(default=[])
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    source: str # 'gemini_live' or 'offline_knowledge_base'
    citations: List[Citation] = Field(default=[])
    is_fallback: bool = False
    conversation_id: Optional[str] = None

# Timetable Schemas
class TimetableSlot(BaseModel):
    time: str
    subject: str
    code: str
    faculty: str
    room: str
    is_lab: bool = False
    start_time: Optional[str] = ""
    end_time: Optional[str] = ""
    course_title: Optional[str] = ""
    course_code: Optional[str] = ""
    room_number: Optional[str] = ""
    faculty_name: Optional[str] = ""
    course_type: Optional[str] = "Lecture"

class TimetableResponse(BaseModel):
    department: str
    semester: str
    schedule: Dict[str, List[TimetableSlot]]

# Course Schemas
class CourseResponse(BaseSchema):
    id: str
    code: str
    title: str
    credits: int
    semester_number: int
    course_type: str
    description: Optional[str] = None
    recommended_books: Optional[str] = None
    prerequisites_text: Optional[str] = "None"
    corequisites_text: Optional[str] = "None"

class PrerequisiteNode(BaseModel):
    code: str
    title: str
    is_strict: bool = True
    credits: Optional[int] = 4
    semester_number: Optional[int] = 1

class CoursePrerequisiteGraph(BaseModel):
    target_course: CourseResponse
    course_code: Optional[str] = ""
    course_title: Optional[str] = ""
    strict_prerequisites: List[PrerequisiteNode] = []
    co_requisites: List[PrerequisiteNode] = []
    upstream_prerequisites: List[PrerequisiteNode] = []
    downstream_dependent_courses: List[PrerequisiteNode] = []

# Exam Schemas
class ExamNoticeResponse(BaseSchema):
    id: str
    notice_code: str
    title: str
    date_issued: Optional[str] = ""
    exam_type: str
    applicable_to: str
    exam_window: Optional[str] = ""
    deadline: Optional[str] = ""
    calculator_policy: Optional[str] = ""
    hall_ticket_guidelines: Optional[str] = ""
    malpractice_rules: Optional[str] = ""
    is_urgent: bool = False

# FAQ Schemas
class AdministrativeFAQResponse(BaseSchema):
    id: str
    category: str
    question: str
    answer: str
    office_location: Optional[str] = ""
    contact_email: Optional[str] = ""
    contact_phone: Optional[str] = ""

# Document Drafter Schemas
class DocumentRequest(BaseModel):
    type: str = Field(..., description="Document type: Leave Letter, Permission Letter, etc.")
    message: str = Field(..., min_length=5, max_length=1500)
    tone: str = Field(default="Professional")
    length: str = Field(default="Medium")

class DocumentResponse(BaseModel):
    output: str
    type: str
    status: str = "success"
    source: str # 'gemini_live' or 'deterministic_template'

# Course Note & Study Material Schemas
class CourseNoteCreateRequest(BaseModel):
    course_id: str = Field(..., description="Target Course UUID or Course Code (e.g. CS401)")
    title: str = Field(..., min_length=3, max_length=200)
    unit_number: int = Field(default=1, ge=1, le=10)
    unit_title: str = Field(..., min_length=2, max_length=200)
    topic_description: Optional[str] = ""
    content_markdown: str = Field(..., min_length=10)
    faculty_author: Optional[str] = "Department Faculty"
    academic_year: Optional[str] = "2025-2026"

class CourseNoteResponse(BaseSchema):
    id: str
    course_id: str
    course_code: Optional[str] = ""
    course_title: Optional[str] = ""
    title: str
    unit_number: int
    unit_title: str
    topic_description: Optional[str] = ""
    content_markdown: str
    faculty_author: str
    academic_year: str
    file_format: str = "PDF"
    file_size_kb: int = 145
    download_count: int = 0
    created_at: Optional[datetime] = None

class CourseCreateRequest(BaseModel):
    code: str = Field(..., min_length=2, max_length=20)
    title: str = Field(..., min_length=3, max_length=200)
    department_code: Optional[str] = "CSE"
    credits: int = Field(default=4, ge=1, le=10)
    semester_number: int = Field(default=4, ge=1, le=8)
    course_type: Optional[str] = "Core"
    description: Optional[str] = ""
    syllabus_outline: Optional[str] = ""
    recommended_books: Optional[str] = ""
    prerequisites_text: Optional[str] = "None"

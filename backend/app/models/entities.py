import uuid
import datetime
from sqlalchemy import (
    Column, String, Integer, Boolean, Text, DateTime, ForeignKey, Table
)
from sqlalchemy.orm import relationship
from backend.app.db.session import Base

def generate_uuid() -> str:
    return str(uuid.uuid4())

class Institution(Base):
    __tablename__ = "institutions"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False)
    academic_year = Column(String(50), default="2025-2026")
    current_semester = Column(String(50), default="Spring Semester")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    departments = relationship("Department", back_populates="institution", cascade="all, delete-orphan")

class Department(Base):
    __tablename__ = "departments"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=False)
    name = Column(String(150), nullable=False)
    code = Column(String(20), nullable=False)

    institution = relationship("Institution", back_populates="departments")
    courses = relationship("Course", back_populates="department")
    faculty = relationship("Faculty", back_populates="department")
    timetable_entries = relationship("TimetableEntry", back_populates="department")

class AcademicYear(Base):
    __tablename__ = "academic_years"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=False)
    year_label = Column(String(50), nullable=False)
    is_current = Column(Boolean, default=True)

class Semester(Base):
    __tablename__ = "semesters"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    number = Column(Integer, nullable=False) # 1 to 8
    term = Column(String(20), default="Spring")
    is_active = Column(Boolean, default=True)

class Course(Base):
    __tablename__ = "courses"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    code = Column(String(20), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    credits = Column(Integer, default=4)
    semester_number = Column(Integer, index=True, nullable=False)
    course_type = Column(String(50), default="Core")
    description = Column(Text, default="")
    syllabus_outline = Column(Text, default="")
    recommended_books = Column(Text, default="")
    prerequisites_text = Column(String(255), default="None")
    corequisites_text = Column(String(255), default="None")
    is_sample = Column(Boolean, default=True)

    department = relationship("Department", back_populates="courses")
    timetable_entries = relationship("TimetableEntry", back_populates="course")
    notes = relationship("CourseNote", back_populates="course", cascade="all, delete-orphan")

class CourseNote(Base):
    __tablename__ = "course_notes"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True)
    uploaded_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(200), nullable=False, index=True)
    unit_number = Column(Integer, default=1)
    unit_title = Column(String(200), default="Module 1")
    topic_description = Column(Text, default="")
    content_markdown = Column(Text, nullable=False)
    faculty_author = Column(String(150), default="Department Faculty")
    academic_year = Column(String(50), default="2025-2026")
    file_format = Column(String(20), default="PDF")
    file_size_kb = Column(Integer, default=145)
    download_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    course = relationship("Course", back_populates="notes")
    uploader = relationship("User")

class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    prerequisite_course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    is_strict = Column(Boolean, default=True)

class CourseCoRequisite(Base):
    __tablename__ = "course_co_requisites"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    co_requisite_course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)

class Faculty(Base):
    __tablename__ = "faculty"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    department_id = Column(String(36), ForeignKey("departments.id"))
    name = Column(String(150), nullable=False)
    designation = Column(String(100), default="Assistant Professor")
    email = Column(String(150), default="")
    cabin_location = Column(String(100), default="")

    department = relationship("Department", back_populates="faculty")

class Classroom(Base):
    __tablename__ = "classrooms"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    institution_id = Column(String(36), ForeignKey("institutions.id"), nullable=True)
    room_number = Column(String(50), nullable=False)
    building = Column(String(100), default="Main Academic Block")
    capacity = Column(Integer, default=60)
    is_lab = Column(Boolean, default=False)

class TimetableEntry(Base):
    __tablename__ = "timetable_entries"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    department_id = Column(String(36), ForeignKey("departments.id"), nullable=False)
    semester_label = Column(String(20), nullable=False) # e.g. "Sem 4"
    course_id = Column(String(36), ForeignKey("courses.id"), nullable=False)
    faculty_name = Column(String(150), default="")
    room_number = Column(String(50), default="")
    section = Column(String(10), default="A")
    day_of_week = Column(String(20), index=True, nullable=False) # Monday-Friday
    time_slot = Column(String(50), nullable=False) # e.g. "09:00 - 10:00 AM"
    is_lab = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=True)

    department = relationship("Department", back_populates="timetable_entries")
    course = relationship("Course", back_populates="timetable_entries")

class ExamNotice(Base):
    __tablename__ = "exam_notices"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    notice_code = Column(String(50), unique=True, nullable=False)
    title = Column(String(250), nullable=False)
    date_issued = Column(String(50), default="")
    exam_type = Column(String(50), default="Midterm")
    applicable_to = Column(String(100), default="All Batches")
    exam_window = Column(String(100), default="")
    deadline = Column(String(100), default="")
    calculator_policy = Column(Text, default="")
    hall_ticket_guidelines = Column(Text, default="")
    malpractice_rules = Column(Text, default="")
    schedule_payload = Column(Text, default="[]") # JSON string of highlights
    guidelines_payload = Column(Text, default="[]") # JSON string of rules
    is_urgent = Column(Boolean, default=False)
    is_sample = Column(Boolean, default=True)

class AdministrativeFAQ(Base):
    __tablename__ = "administrative_faqs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    category = Column(String(100), index=True, nullable=False)
    question = Column(String(300), nullable=False)
    answer = Column(Text, nullable=False)
    office_location = Column(String(150), default="")
    contact_email = Column(String(150), default="")
    contact_phone = Column(String(50), default="")
    last_verified_at = Column(DateTime, default=datetime.datetime.utcnow)
    is_sample = Column(Boolean, default=True)

class CampusContact(Base):
    __tablename__ = "campus_contacts"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    department_or_office = Column(String(150), nullable=False)
    incharge_name = Column(String(150), default="")
    phone = Column(String(50), default="")
    email = Column(String(150), default="")
    office_room = Column(String(100), default="")

class KnowledgeDocument(Base):
    __tablename__ = "knowledge_documents"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), nullable=False)
    category = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(200), default="Academic Inquiry")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    messages = relationship("ConversationMessage", back_populates="conversation", cascade="all, delete-orphan")

class ConversationMessage(Base):
    __tablename__ = "conversation_messages"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    conversation_id = Column(String(36), ForeignKey("conversations.id"), nullable=False)
    role = Column(String(20), nullable=False) # 'user' or 'model'
    content = Column(Text, nullable=False)
    source_metadata = Column(Text, default="{}") # JSON citations
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    conversation = relationship("Conversation", back_populates="messages")

class GeneratedDocument(Base):
    __tablename__ = "generated_documents"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    document_type = Column(String(100), nullable=False)
    situation_context = Column(Text, nullable=False)
    tone = Column(String(50), default="Professional")
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Role(Base):
    __tablename__ = "roles"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(50), unique=True, nullable=False) # 'student', 'faculty', 'admin'
    description = Column(String(200), default="")

class User(Base):
    __tablename__ = "users"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(150), default="")
    roll_number = Column(String(50), default="")
    department = Column(String(100), default="CSE (AI)")
    semester = Column(String(50), default="Sem 5 (CSE - AI)")
    cgpa = Column(String(20), default="8.0")
    resume_url = Column(String(500), default="")
    skills = Column(Text, default="")
    phone = Column(String(50), default="")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    role = relationship("Role")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=generate_uuid)
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    action = Column(String(100), nullable=False)
    entity_type = Column(String(50))
    entity_id = Column(String(36))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    details = Column(Text, default="")

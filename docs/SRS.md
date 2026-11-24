# Software Requirements Specification (SRS)
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Standard**: IEEE 830-1998 Compatible
- **Version**: 1.0.0
- **Status**: Released

---

## 1. Introduction

### 1.1 Purpose
This document specifies the software requirements for the **Campus AI Assistant**, covering frontend, backend, database, AI retrieval, fallback handling, and administrative operations.

### 1.2 Scope
The system encompasses:
- Conversational chat interface with RAG grounding.
- Interactive timetable navigation.
- Course catalog with prerequisite graph generation.
- Examination notice board and circular management.
- Administrative FAQ and service directory.
- Formal academic correspondence drafting.
- Administrative data management portal with RBAC.

### 1.3 Definitions and Abbreviations
- **RAG**: Retrieval-Augmented Generation.
- **RBAC**: Role-Based Access Control.
- **LLM**: Large Language Model (Google Gemini 2.5 Flash).
- **JWT**: JSON Web Token.
- **UUID**: Universally Unique Identifier.
- **OD**: On-Duty official attendance leave.

---

## 2. Overall Description

### 2.1 System Architecture Overview
The system operates as a client-server architecture:
1. **Frontend**: Single Page Application built with React, TypeScript, Tailwind CSS, Lucide icons, and TanStack Query.
2. **Backend**: Asynchronous REST API built with FastAPI, Pydantic v2, and SQLAlchemy 2.0.
3. **Database**: Relational storage (PostgreSQL / SQLite fallback) supporting structured relational records and full-text search.
4. **AI Engine**: Google Gemini 2.5 Flash via `google-genai` SDK with deterministic rule-based local fallback.

### 2.2 User Classes and Roles
- **Student (`role: student`)**: Read access to timetables, courses, exams, FAQs; write access to own chat conversations and document generation.
- **Faculty (`role: faculty`)**: Same as Student plus access to department syllabus advisories and student leave verification.
- **Administrator (`role: admin`)**: Full CRUD access over institutional data (courses, timetables, exams, FAQs, campus contacts).

---

## 3. Specific Functional Requirements

### 3.1 Conversational AI Assistant
- **FR-001**: The system shall process natural language student queries and classify intent into Timetable, Course, Exam, Administrative, or Document drafting.
- **FR-002**: The system shall retrieve relevant campus knowledge chunks from the database before generating an answer.
- **FR-003**: The system shall inject verified knowledge into the system prompt of Google Gemini 2.5 Flash.
- **FR-004**: The system shall include source document citations in every grounded answer.
- **FR-005**: The system shall display a distinct UI badge distinguishing live AI output from deterministic local fallback data.
- **FR-006**: The system shall maintain multi-turn conversational context up to the previous 10 message exchanges per session.
- **FR-007**: When requested campus information does not exist in the database, the system shall return an explicit non-hallucinating statement explaining that the record cannot be verified.
- **FR-008**: The system shall provide quick prompt suggestion chips to initiate common queries in 1 click.

### 3.2 Timetable Navigator
- **FR-009**: The system shall support filtering of timetable entries by Department, Semester, Section, Academic Year, and Day.
- **FR-010**: The timetable shall present course code, subject title, faculty name, room/lab allocation, and start/end time.
- **FR-011**: The system shall distinguish theory lectures from practical lab sessions and recess intervals.
- **FR-012**: The system shall provide both an interactive grid view and a mobile list view.

### 3.3 Course Catalog & Prerequisite Graph
- **FR-013**: The system shall maintain course records including code, title, credits, department, semester, syllabus outline, and textbooks.
- **FR-014**: The system shall maintain strict prerequisite and co-requisite relationships.
- **FR-015**: The system shall render a visual prerequisite dependency tree for any selected course.
- **FR-016**: The system shall validate and reject circular prerequisite relationships upon course creation or update.

### 3.4 Examination Hub
- **FR-017**: The system shall display active examination notices categorized into Midterm, End-Semester, Practical, and Backlog.
- **FR-018**: Each exam notice shall record publication date, target semesters, exam window dates, reporting instructions, calculator policy, and malpractice regulations.
- **FR-019**: The system shall indicate urgent notices (e.g. registration deadlines within 7 days).

### 3.5 Administrative Helpdesk
- **FR-020**: The system shall maintain categorized FAQs for Fees, Scholarships, Library, Hostel, Attendance, and Grievances.
- **FR-021**: Each FAQ shall include question, answer, department/office contact, and last-verified date.
- **FR-022**: The system shall support full-text keyword search across all FAQ questions and answers.

### 3.6 Academic Document Drafter
- **FR-023**: The system shall draft formal Leave Letters, Permission Letters, Faculty Emails, and Bonafide Requests.
- **FR-024**: The system shall allow parameterization of tone (Formal, Professional, Polite) and length (Short, Medium, Detailed).
- **FR-025**: The system shall provide quick situation presets (Medical Leave, Hackathon OD, Loan Bonafide).
- **FR-026**: The generated documents shall use editable bracketed placeholders (e.g. `[Student Name]`, `[Roll Number]`) and strictly never forge identity details.
- **FR-027**: The system shall provide 1-click clipboard copy and `.txt` file download.

### 3.7 Administration & Management
- **FR-028**: The system shall provide protected CRUD REST endpoints under `/api/v1/admin/*`.
- **FR-029**: Administrative routes shall require valid JWT authentication with `role: admin`.
- **FR-030**: All administrative modifications shall be logged to an `audit_logs` table recording user ID, action, entity type, and timestamp.

---

## 4. Non-Functional Requirements

### 4.1 Performance (NFR-001 – NFR-004)
- **NFR-001**: REST API endpoints for structured data (timetables, courses, FAQs) shall respond within 150 ms under normal load.
- **NFR-002**: Local knowledge base retrieval and fallback answers shall respond within 300 ms.
- **NFR-003**: Database queries shall utilize indexes on foreign keys, course codes, and department/semester composite filters.
- **NFR-004**: The system shall maintain database connection pooling with a pool size of at least 10 connections.

### 4.2 Reliability & Fault Tolerance (NFR-005 – NFR-008)
- **NFR-005**: If the Gemini API call times out (> 10s) or fails with HTTP 4xx/5xx, the system shall seamlessly fall back to local grounded retrieval.
- **NFR-006**: The system shall operate stably without an active internet connection when using local database data.
- **NFR-007**: The system shall not crash or restart due to invalid user inputs or malformed JSON payloads.
- **NFR-008**: Database migrations shall be managed via Alembic with reversible upgrade and downgrade paths.

### 4.3 Security & Privacy (NFR-009 – NFR-013)
- **NFR-009**: User passwords shall be hashed using `bcrypt` with a minimum cost factor of 12.
- **NFR-010**: All authentication tokens shall be signed JWTs with expiration timestamps.
- **NFR-011**: Frontend inputs and markdown rendering shall sanitize HTML to prevent Cross-Site Scripting (XSS).
- **NFR-012**: Database queries shall use parameterized SQLAlchemy ORM statements to prevent SQL Injection.
- **NFR-013**: Secrets (API keys, JWT secret keys, DB passwords) shall be read exclusively from environment variables.

---

## 5. Acceptance Criteria & Verification

| Requirement ID | Verification Method | Pass Criteria |
|---|---|---|
| **FR-001 – FR-008** | Automated API test & UI check | Chat answers accurately cite knowledge chunks; fallback executes on invalid key. |
| **FR-009 – FR-012** | UI interactive test | Filter by CSE Sem 4 displays all 5 days with correct rooms and faculty. |
| **FR-013 – FR-016** | Unit test & UI tree | CS601 shows MA301 and CS401 as prerequisites; cycle detection blocks circular links. |
| **FR-017 – FR-019** | API endpoint test | `/api/v1/exams` returns active notices with correct date windows. |
| **FR-023 – FR-027** | Document generator test | Letter generated with placeholders; copy and download actions work. |
| **NFR-005** | Simulated network failure | Disabling network or setting empty API key triggers local fallback with badge. |
| **NFR-009 – NFR-013** | Security test | Admin routes reject unauthenticated requests with HTTP 401/403. |

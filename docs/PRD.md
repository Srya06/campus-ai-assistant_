# Product Requirements Document (PRD)
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Document Version**: 1.0.0
- **Status**: Approved
- **Author**: Campus AI Engineering & Architecture Team
- **Target Audience**: Software Engineers, Product Managers, Institutional Stakeholders, Evaluators

---

## 1. Executive Summary & Problem Statement

### 1.1 Problem Statement
In higher education institutions, academic and administrative information is chronically fragmented across siloed PDF handbooks, physical notice boards, outdated portals, and conflicting email chains. Students face substantial difficulties navigating:
1. Dynamic class schedules, room shifts, and laboratory batch allocations.
2. Complex prerequisite dependency trees during course enrollment.
3. Rapidly changing examination circulars, hall ticket mandates, and calculator policies.
4. Administrative procedures for fee installments, scholarships, library access, and bonafide certificates.
5. Drafting formal, professional academic communications (leave letters, permission letters, formal emails).

### 1.2 Proposed Solution
**Campus AI Assistant** is an intelligent, full-stack conversational academic navigator. It pairs verified institutional data (timetables, course syllabi, exam notices, FAQs) with Google Gemini 2.5 Flash and a deterministic local fallback engine. Students ask natural language questions and receive accurate, grounded, cited answers in seconds.

---

## 2. Product Vision & Core Objectives

### 2.1 Vision
To serve as the unified conversational operating system for campus academics, ensuring no student misses an exam notice, registers for a course without prerequisites, or struggles with bureaucratic paperwork.

### 2.2 Objectives
1. **Accurate Grounded Answers**: Ground all academic answers in verified campus knowledge; never invent or hallucinate dates, rules, or policies.
2. **Multi-Turn Contextual Dialogue**: Maintain conversation memory across follow-up queries.
3. **Structured Navigation Tools**: Provide dedicated interactive views for Timetables, Course Catalogs, Exam Hubs, and Admin FAQs alongside the chat.
4. **Deterministic Resilience**: Guarantee full operational availability even when external AI APIs (Gemini) are unavailable or unconfigured.
5. **Formal Document Drafter**: Generate editable, formal academic letters and emails with placeholder brackets, preventing personal data leaks.
6. **Multi-Department & Institutional Scalability**: Architect normalized relational data models allowing any institution, department, or semester to be onboarded without code rewrites.

---

## 3. Target User Personas

| Persona | Role | Key Pain Points | Core User Journey |
|---|---|---|---|
| **Aarav (Student)** | 4th Sem Computer Science | Struggles to find lab room venues, uncertain about ML course prerequisites for upcoming semester. | Uses AI Chat or Timetable filter to check daily schedule; queries prerequisite tree for CS601; drafts a leave letter. |
| **Prof. Sunita (Faculty / Advisor)** | Department Academic Advisor | Repeatedly answering identical administrative queries regarding attendance criteria and exam rules. | Refers students to Campus AI Assistant; uses administrative portal to verify published timetable. |
| **Dr. R. Verma (Administrator)** | Academic Registrar / HOD | Managing changes in exam dates, backlog notifications, and issuing bonafide certificates. | Updates examination circulars and administrative FAQs via protected CRUD endpoints. |

---

## 4. Functional Scope & Feature Breakdown

### 4.1 Module 1: Conversational AI Assistant
- Natural language query understanding for timetables, exams, courses, and admin queries.
- Grounded RAG pipeline citing verified knowledge records.
- Visible badge indicating verified campus data vs. fallback local lookup.
- Quick suggestion prompt chips (e.g., "Today's Schedule", "ML Prerequisites", "Mid-Sem Rules").
- Markdown rendering supporting tables, bold text, code tags, and blockquotes.
- Copy, clear, and conversation history controls.

### 4.2 Module 2: Interactive Timetable Navigator
- Filterable by Department, Semester, Academic Year, Section, and Day of Week.
- Grid and list view displaying Course Code, Title, Faculty, Venue/Lab, and Time Slot.
- Highlighting for breaks, labs, and elective periods.

### 4.3 Module 3: Course Catalog & Prerequisite Graph
- Searchable directory of courses with credits, department, semester, and syllabus.
- Visual dependency mapper distinguishing strict prerequisites from co-requisites.
- Cycle detection to prevent circular prerequisites.

### 4.4 Module 4: Examination Hub
- Live notices for Midterm and End-Semester schedules.
- Clear highlight of calculator policies, hall ticket requirements, and malpractice warnings.
- Backlog registration deadlines and portal links.

### 4.5 Module 5: Administrative Helpdesk
- Searchable FAQs categorized into Fees, Scholarships, Library, Hostel, and Bonafide Certificates.
- Direct contact extensions, office room numbers, and verified dates.

### 4.6 Module 6: Academic Document Drafter
- Generates formal Leave Applications, On-Duty Permissions, Faculty Emails, and HOD Requests.
- Situation presets (Medical leave, Hackathon duty, Loan bonafide).
- Download as `.txt` and formatted `.pdf`.
- 100% placeholder compliance (never generates fake student roll numbers or forged signatures).

---

## 5. Non-Functional Requirements (NFRs)

- **Grounding & Zero Hallucination**: AI must state inability to verify if data is missing; never fabricate campus information.
- **Latency**: API response under 1.5 seconds for knowledge retrieval; under 2.5 seconds for LLM generation.
- **Availability**: Deterministic fallback engine ensures core timetable, course, exam, and FAQ modules have 99.9% uptime.
- **Security & RBAC**: Role-Based Access Control (Student, Faculty, Administrator) with JWT tokens and bcrypt password hashing.
- **Responsive UI**: Seamless experience on Mobile (375px+), Tablet (768px+), and Desktop (1200px+).

---

## 6. Success Metrics & KPIs
1. **Query Accuracy Rate**: > 98% grounded responses matching institutional ground truth.
2. **Fallback Seamlessness**: 100% successful response rate when Gemini API key is absent.
3. **Drafting Efficiency**: Student time to create formal academic correspondence reduced from 15 minutes to under 30 seconds.

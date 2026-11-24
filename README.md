# 🎓 Campus AI Assistant
### *A Student-Centric Conversational Academic Navigator & Advisory System*

> **"A student-centric conversational assistant designed to navigate academic timetables, exam notices, course prerequisites, and administrative queries."**

---

## 🌟 Executive Summary

**Campus AI Assistant** is a full-stack, enterprise-grade academic platform built to eliminate the fragmentation of institutional information in universities. Students and faculty can interact through a natural conversational AI interface or dedicated interactive portals to access:

- 📅 **Academic Timetables & Schedules**: Class lectures, lab allocations, faculty advisors, and room venues.
- 📚 **Course Catalog & Prerequisite Dependency Trees**: Full curriculum, credits, syllabus outlines, strict vs. recommended prerequisites, and textbook recommendations.
- 📢 **Examination Hub & Circulars**: Official Mid-Semester and End-Semester date sheets, hall ticket mandates, non-programmable calculator policies, and backlog examination deadlines.
- 🏢 **Administrative Helpdesk**: Verified procedures and contacts for tuition fee installments, scholarships (MCM, NSP), 24/7 library access & fines, hostel regulations, bonafide certificates, and anti-ragging support.
- ✍️ **Formal Academic Document & Email Drafter**: Professional generation of leave applications, on-duty permissions, and faculty emails with bracketed placeholders (`[Your Name]`, `[Roll Number]`), ensuring privacy and academic integrity.
- ⚙️ **Administrative Management Portal**: Role-Based Access Control (RBAC) enabling administrators to publish courses and examination notices.

Powered by **Google Gemini 2.5 Flash** with an integrated **Grounded Campus Knowledge Base (RAG)**, **SQLAlchemy 2.0 relational persistence**, and a **deterministic local fallback engine**.

---

## 🏗️ Architecture & Technology Stack

| Layer | Technologies Used |
|---|---|
| **Frontend** | React / TypeScript / Modern Component System / Tailwind CSS / Lucide Icons |
| **Backend** | Python 3.10+ / 3.11+, FastAPI (REST API v1), Uvicorn ASGI Server |
| **Persistence** | SQLAlchemy 2.0 ORM, PostgreSQL (Production) / SQLite (Zero-Config Development) |
| **AI Orchestration** | Google GenAI SDK (`gemini-2.5-flash`), Retrieval-Augmented Generation (RAG) |
| **Resilience** | Deterministic local database fallback engine (guarantees zero-downtime answers) |
| **Security & RBAC** | JWT (JSON Web Tokens), salted SHA-256 / bcrypt password hashing, Role-Based Access |
| **Testing** | Automated `pytest` test suite with 100% pass rate (14/14 automated tests) |
| **DevOps** | Docker, Docker Compose, Makefile, GitHub Actions CI workflow |

---

## 📁 Repository Directory Structure

```text
campus-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── api/v1/             # Versioned REST API routers
│   │   │   ├── auth.py         # /api/v1/auth (Login, user profile)
│   │   │   ├── chat.py         # /api/v1/chat (Conversational assistant with citations)
│   │   │   ├── timetable.py    # /api/v1/timetable (Filter by dept, sem, day)
│   │   │   ├── courses.py      # /api/v1/courses (Catalog & prerequisite graph)
│   │   │   ├── exams.py        # /api/v1/exams (Active notices & circulars)
│   │   │   ├── faqs.py         # /api/v1/faqs (Administrative helpdesk search)
│   │   │   ├── documents.py    # /api/v1/documents (Academic letter generator)
│   │   │   ├── admin.py        # /api/v1/admin (Protected CRUD operations)
│   │   │   └── health.py       # /api/v1/health (Backend & AI status)
│   │   ├── core/               # Configuration & JWT security
│   │   ├── db/                 # Database engine & seed data script
│   │   ├── models/             # SQLAlchemy 2.0 ORM entities
│   │   ├── schemas/            # Pydantic v2 validation schemas
│   │   └── services/           # AI Provider, RAG Service, Fallback Engine
│   ├── tests/                  # Automated pytest suite (14 passing test suites)
│   └── main.py                 # ASGI application entrypoint
│
├── frontend/
│   ├── index.html              # Multi-tab responsive application shell
│   ├── style.css               # Clean Indigo & Slate design tokens
│   └── script.js               # Client controller (v1 API integration)
│
├── docs/                       # Complete Engineering Documentation Suite
│   ├── PRD.md                  # Product Requirements Document
│   ├── SRS.md                  # Software Requirements Specification (IEEE standard)
│   ├── ARCHITECTURE.md         # System Architecture & Mermaid Diagrams
│   ├── TECH_STACK.md           # Technology Evaluation & Dependencies
│   ├── DATABASE_SCHEMA.md      # Normalized Relational Schema & ERD
│   ├── API_DOCUMENTATION.md    # Complete REST API v1 Specification
│   ├── UI_UX_GUIDELINES.md     # Design Tokens, Accessibility & Breakpoints
│   ├── DEVELOPMENT_ROADMAP.md  # Phased Milestones & MVP Checklist
│   └── TESTING.md              # Quality Assurance, Grounding & Security Tests
│
├── AGENTS.md                   # AI Coding Agent operating instructions
├── .env.example                # Sample environment configuration
├── docker-compose.yml          # Container configuration
├── Dockerfile                  # Application container image
├── Makefile                    # Developer automation shortcuts
├── requirements.txt            # Python dependencies
└── pytest.ini                  # Pytest configuration
```

---

## 🚀 Quick Start Guide

### Step 1: Open Terminal in Project Directory
```powershell
cd campus-ai-assistant
```

### Step 2: Activate Python Virtual Environment
- **Windows (PowerShell)**:
  ```powershell
  .\venv\Scripts\activate
  ```
- **macOS / Linux**:
  ```bash
  source venv/bin/activate
  ```

*(If setting up a fresh environment, run `pip install -r requirements.txt`)*

---

### Step 3: Run the Application

#### Option A: Single Unified Server (Recommended)
FastAPI now directly serves the full interactive Frontend UI, REST API v1, and Swagger Docs together on Port 8000:
```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```
- 🌐 **Full Application Web UI**: `http://localhost:8000`
- 📖 **Interactive Swagger UI**: `http://localhost:8000/docs`

#### Option B: Dedicated Two-Terminal Mode (Optional)
If you prefer running the frontend separately via a dedicated static HTTP server:

**Terminal 1 — FastAPI Backend:**
```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend Server:**
```powershell
python -m http.server 3001 --directory frontend
```
- 🌐 **Frontend App**: `http://localhost:3001`
- 📖 **Backend API**: `http://localhost:8000/docs`
python -m http.server 3001 --directory frontend
```
> 📌 *Note: Port `3001` is used to prevent Windows socket permission conflicts on port `3000`.*

---

### Step 4: Open in Your Browser
Open your browser and navigate to:
👉 **[http://localhost:3001](http://localhost:3001)**

---

## 🔑 Demo Login Accounts

Click the **👤 Login (Admin / Student)** button in the top-right header:

| Role | Username | Password | Capabilities |
|---|---|---|---|
| **Administrator** | `admin` | `admin123` | Full access + unlocks **⚙️ Admin Management** tab to publish courses and notices |
| **Student** | `student` | `student123` | Conversational assistant, timetables, courses, exams, helpdesk, document drafting |

---

## 🧪 Running Automated Tests

Execute the complete 14-test verification suite:
```powershell
.\venv\Scripts\python.exe -m pytest backend/tests -v
```
**Test Coverage Includes**:
- ✅ Database entity relationships and seed integrity
- ✅ REST API contracts (`/health`, `/timetable`, `/courses`, `/exams`, `/faqs`, `/documents`)
- ✅ Prerequisite dependency tree generation
- ✅ Grounded AI chat and deterministic offline fallback
- ✅ Role-Based Access Control (RBAC) and admin route protection

---

## 🌐 Live Services Status

Both services are currently active in the background:
- 🌐 **Frontend Client**: [http://localhost:3001](http://localhost:3001)
- ⚡ **Backend API**: [http://localhost:8000](http://localhost:8000)
- 📖 **Interactive Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)

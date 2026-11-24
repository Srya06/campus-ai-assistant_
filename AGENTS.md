# AGENTS.md — AI Coding Agent Guidelines & Operating Instructions
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

> **Mandatory reading for all automated AI coding agents, subagents, and human contributors working in this repository.**

---

## 1. Project Overview & Architecture Summary
**Campus AI Assistant** is a full-stack academic assistant providing conversational and structured navigation over:
- 📅 **Academic Timetables** (classrooms, labs, faculty, timings)
- 📚 **Course Catalog & Prerequisites** (credit structures, strict prereqs, syllabus)
- 📢 **Exam Notices & Circulars** (date sheets, calculator regulations, malpractice rules)
- 🏢 **Administrative Helpdesk** (fees, scholarships, library, hostel, bonafide)
- ✍️ **Formal Academic Document Drafter** (leave letters, permissions, emails)

### Architecture
- **Backend**: FastAPI (Python 3.10+ / 3.11+) with SQLAlchemy 2.0 ORM, Alembic migrations, dual database support (PostgreSQL + SQLite fallback), and abstract AI service.
- **Frontend**: Responsive Single-Page Application (React / TypeScript / Tailwind CSS) with tabbed navigation, markdown rendering, and real-time status pills.
- **AI Engine**: Google Gemini 2.5 Flash via `google-genai` SDK + Grounded RAG knowledge base + Deterministic local fallback.

---

## 2. Strict Ground Rules for Agents

1. **Inspect Before Changing**: You MUST inspect existing working code before modifying or adding files. Never overwrite working functionality blindly.
2. **Preserve Working Functionality**: Any modification must preserve backward compatibility with existing working endpoints and UI views.
3. **Never Fabricate Test Results**: You MUST actually execute automated tests (`pytest`) using available command tools and report real stdout/stderr output. Never fabricate or imagine passing test outputs.
4. **Never Hardcode Secrets**: API keys, database credentials, and JWT signing keys must be loaded exclusively from environment variables or `.env`.
5. **No Hallucination in Campus Data**: Never make the AI assistant invent fake exam dates, room numbers, or fee policies. When data is absent, the system must clearly state that the record could not be verified.
6. **Update Documentation**: Whenever you change API contracts, database models, or environment variables, you MUST update the corresponding markdown file in `docs/` in the same turn.

---

## 3. Directory Structure

```text
campus-ai-assistant/
├── backend/
│   ├── app/
│   │   ├── api/v1/         # Versioned REST routers
│   │   ├── core/           # Config, security, JWT
│   │   ├── db/             # SQLAlchemy session, base, seeders
│   │   ├── models/         # SQLAlchemy 2.0 ORM models
│   │   ├── schemas/        # Pydantic v2 schemas
│   │   └── services/       # AI provider, RAG, fallback, doc generator
│   ├── tests/              # Pytest test suite
│   ├── main.py             # ASGI entrypoint
│   └── campus_knowledge.py # Structured verified campus dataset
├── frontend/
│   ├── index.html          # Web application shell
│   ├── style.css           # Modern aesthetic stylesheet
│   └── script.js           # Client application logic
├── docs/                   # Full documentation suite (PRD, SRS, Architecture, etc.)
├── .env.example            # Sample configuration
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Container image build definition
└── README.md               # User onboarding guide
```

---

## 4. Setup, Run & Test Commands

### 4.1 Backend Setup
```powershell
# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4.2 Run Backend
```powershell
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

### 4.3 Run Frontend
```powershell
python -m http.server 3001 --directory frontend
```
*(Note: Use port `3001` on Windows to avoid OS Hyper-V reserved port exclusions on `3000`).*

### 4.4 Run Tests
```powershell
pytest backend/tests -v
```

---

## 5. Coding & API Conventions

- **Python**: Follow PEP 8 and use type hints on all function parameters and return types.
- **Pydantic**: Use Pydantic v2 conventions (`model_config = ConfigDict(...)`, avoid deprecated v1 syntax).
- **FastAPI**: Routers must declare explicit response models and status codes.
- **REST Endpoints**: Prefix all versioned routes with `/api/v1/`.
- **Database**: Use SQLAlchemy 2.0 style queries (`select(...)`, session context managers).
- **Error Handling**: Raise `HTTPException` with informative `detail` strings; never return raw traceback strings to end users.
- **Document Generation**: Always output bracketed placeholders like `[Your Name]` and `[Roll Number]` so student identity is never forged.

---

## 6. Definition of Done (DoD)

A task or PR is complete only when:
1. Code follows architectural boundaries and naming conventions.
2. All database migrations apply cleanly.
3. Both backend and frontend run with zero console errors.
4. All unit and integration tests pass with evidence.
5. All relevant documentation in `docs/` is updated.

# Development Roadmap & Release Milestones
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Version**: 1.0.0
- **Status**: Active Execution

---

## 1. Phased Development Lifecycle

### Phase 0: Requirements, Domain Modeling & Specifications (Completed)
- Define PRD, IEEE SRS, System Architecture, and Database Schema.
- Finalize ground truth dataset for initial institution (Apex Institute of Technology & Engineering).
- Define non-hallucination policies and deterministic fallback requirements.

### Phase 1: Foundation & Modular Backend Architecture (Active)
- Set up FastAPI app structure with clean architecture (`app/core`, `app/db`, `app/models`, `app/services`, `app/api`).
- Implement SQLAlchemy 2.0 relational models with dual engine (PostgreSQL + SQLite).
- Write database seeders for multi-department timetables, course catalog, exams, and FAQs.
- Implement JWT authentication and RBAC middlewares.

### Phase 2: AI Orchestration, Grounded RAG & Fallback Engine (Active)
- Abstract AI provider interface (`BaseAIProvider`).
- Implement `GeminiProvider` using Google GenAI SDK with `gemini-2.5-flash`.
- Implement `FallbackEngine` for verified local keyword/semantic retrieval.
- Build citation generator linking answers to primary database records.
- Implement academic document drafter with bracketed placeholder guarantees.

### Phase 3: Frontend Presentation & Accessible UI (Active)
- Create multi-tab responsive interface: AI Chat, Timetable, Course Explorer, Exam Hub, Admin Helpdesk, and Letter Drafter.
- Integrate TanStack Query for caching and error management.
- Build interactive timetable filter and course prerequisite graph visualizer.
- Implement 1-click prompt chips, clipboard copy, and `.txt`/`.pdf` download actions.

### Phase 4: Automated Verification, QA & Security Testing (Active)
- Write unit tests for database models, prerequisite cycle detection, and seed integrity.
- Write API integration tests for `/api/v1/chat`, `/api/v1/timetable`, `/api/v1/courses`, `/api/v1/generate`.
- Test Gemini timeout and offline fallback behavior.
- Validate RBAC enforcement on administrative routes.

### Phase 5: Containerization & Production Packaging
- Author `Dockerfile` and `docker-compose.yml` with PostgreSQL and persistent volume storage.
- Author `Makefile` for automated setup, test, and run workflows.
- Author comprehensive `README.md` and `AGENTS.md`.

---

## 2. MVP Release Checklist

- [x] Grounded dataset covering 2+ departments (CSE, ECE) and semesters (Sem 4, Sem 6).
- [x] Multi-turn conversational chat with conversation history and suggested chips.
- [x] Interactive timetable navigator with day/dept/semester filters.
- [x] Course catalog with credits, syllabus, and prerequisite dependency graph.
- [x] Examination circulars with date sheets, calculator policies, and malpractice rules.
- [x] Administrative helpdesk directory with direct extensions and office hours.
- [x] Document drafter with situation presets and placeholder guarantees.
- [x] Deterministic local fallback when Gemini API key is absent.
- [x] Backend test suite with 100% pass rate.
- [x] Complete documentation suite (`PRD`, `SRS`, `ARCHITECTURE`, `TECH_STACK`, `DATABASE_SCHEMA`, `API_DOCUMENTATION`, `UI_UX_GUIDELINES`, `TESTING`, `AGENTS.md`).

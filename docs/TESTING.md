# Comprehensive Testing Strategy & Verification Guide
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Version**: 1.0.0
- **Frameworks**: pytest, httpx, Vitest, Playwright

---

## 1. Testing Objectives & Scope

The testing strategy validates that:
1. **Academic Grounding**: The AI assistant never fabricates dates, policies, or course details; answers must be traceable to database records.
2. **Resilience & Fallback**: The application functions without errors when the Gemini API key is absent, expired, or rate-limited.
3. **Database Integrity**: Relational foreign keys, prerequisite cycles, and unique constraints are enforced.
4. **Security & RBAC**: Unauthorized users cannot access administrative endpoints.
5. **Contract Compliance**: All REST endpoints conform to OpenAPI schemas.

---

## 2. Test Execution Matrix

### 2.1 Unit & Integration Tests (Backend)
Run backend tests using `pytest`:
```powershell
.\venv\Scripts\pytest backend/tests -v
```

### 2.2 Specific Test Cases & Measurable Assertions

#### Test Suite 1: Database & Seed Data Verification (`test_database.py`)
- **TC-DB-01**: Verifies institutions, departments, courses, and timetables load into the session.
- **TC-DB-02**: Verifies prerequisite relationships (e.g. CS601 Machine Learning requires CS401 and MA301).
- **TC-DB-03**: Validates that foreign key constraints prevent orphan timetable entries.

#### Test Suite 2: API Endpoints & Contracts (`test_api.py`)
- **TC-API-01 (`/health`)**: Returns status `healthy` with timestamp.
- **TC-API-02 (`/api/v1/campus-data`)**: Returns structured data for departments, timetables, courses, exams, and FAQs.
- **TC-API-03 (`/api/v1/timetable`)**: Filter by `department=CSE&semester=Sem 4` returns correct slots for Monday–Friday.
- **TC-API-04 (`/api/v1/courses`)**: Search query `machine` returns CS601 course details.
- **TC-API-05 (`/api/v1/exams`)**: Returns examination circulars with `is_urgent` flags.
- **TC-API-06 (`/api/v1/faqs`)**: FAQ search by keyword `scholarship` returns Student Welfare instructions.

#### Test Suite 3: AI Grounding & Deterministic Fallback (`test_ai_fallback.py`)
- **TC-AI-01 (Missing API Key)**: Querying `/api/v1/chat` without a Gemini key returns the verified local knowledge record with badge `offline_knowledge_base`.
- **TC-AI-02 (Hallucination Prevention)**: When asked about a non-existent course (e.g. `Quantum Teleportation 909`), the assistant explicitly states that the record cannot be verified.
- **TC-AI-03 (Citation Traceability)**: Structured answers include course code or notice ID in the citation payload.

#### Test Suite 4: Document Generation & Placeholders (`test_documents.py`)
- **TC-DOC-01**: Leave application generated contains mandatory bracketed placeholders: `[Your Name]`, `[Roll Number]`, `[Department]`.
- **TC-DOC-02**: Does not fabricate fictitious student registration numbers.
- **TC-DOC-03**: Generates valid text content on both Gemini live and local template engines.

#### Test Suite 5: Security & Role-Based Access (`test_security.py`)
- **TC-SEC-01**: Unauthenticated POST request to `/api/v1/admin/courses` returns HTTP 401 Unauthorized.
- **TC-SEC-02**: Student token attempting administrative POST returns HTTP 403 Forbidden.
- **TC-SEC-03**: Valid admin token successfully creates a new resource.

---

## 3. Continuous Integration (CI) Workflow

The automated GitHub Actions workflow (`.github/workflows/ci.yml`) executes on every push and pull request:
1. Installs Python dependencies in clean virtual environment.
2. Runs database migrations and seed verification.
3. Executes `pytest` with coverage report.
4. Lints codebase with `ruff`.
5. Builds frontend production assets.

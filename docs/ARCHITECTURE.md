# System Architecture
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Version**: 1.0.0
- **Architectural Style**: Modular Clean Architecture / Decoupled Client-Server

---

## 1. Architectural Overview & System Context

The **Campus AI Assistant** is engineered around three guiding principles:
1. **Separation of Concerns**: Decoupled presentation, API, application services, domain models, and infrastructure layers.
2. **Deterministic Fallback & High Resilience**: External AI providers are treated as non-blocking augmentations rather than single points of failure.
3. **Institutional Extensibility**: Multi-tenant-ready domain modeling where institutions, departments, semesters, and courses are first-class relational entities.

```mermaid
flowchart TD
    subgraph Users ["Actors & Clients"]
        Student["🎓 Student (Web / Mobile)"]
        Faculty["👩‍🏫 Faculty Advisor"]
        Admin["🏛️ Campus Administrator"]
    end

    subgraph ClientLayer ["Frontend Client (React 19 + TypeScript + Tailwind)"]
        UI_Chat["AI Conversational Chat"]
        UI_TT["Timetable Navigator"]
        UI_Course["Course & Prereq Explorer"]
        UI_Exam["Exam Notices Hub"]
        UI_Admin["Helpdesk & Admin Directory"]
        UI_Drafter["Academic Letter Drafter"]
        UI_Dash["Admin Management Portal"]
    end

    subgraph APILayer ["FastAPI Gateway (v1 REST API)"]
        Router_Auth["/api/v1/auth"]
        Router_Chat["/api/v1/chat"]
        Router_TT["/api/v1/timetable"]
        Router_Course["/api/v1/courses"]
        Router_Exam["/api/v1/exams"]
        Router_FAQ["/api/v1/faqs"]
        Router_Doc["/api/v1/documents"]
        Router_Admin["/api/v1/admin/* (Protected)"]
    end

    subgraph ServiceLayer ["Application & Domain Services"]
        RAG_Service["RAG & Knowledge Retrieval"]
        AI_Orchestrator["AI Provider Abstraction"]
        Fallback_Engine["Deterministic Local Fallback"]
        Doc_Service["Document Template Engine"]
        Auth_Service["JWT & RBAC Security"]
    end

    subgraph ExternalAndData ["Data & External AI"]
        Gemini["🤖 Google Gemini 2.5 Flash API"]
        Database[("🗄️ Relational Database\nPostgreSQL / SQLite")]
    end

    Student --> UI_Chat & UI_TT & UI_Course & UI_Exam & UI_Admin & UI_Drafter
    Faculty --> UI_TT & UI_Course & UI_Exam
    Admin --> UI_Dash

    ClientLayer --> APILayer
    APILayer --> ServiceLayer
    ServiceLayer --> AI_Orchestrator
    AI_Orchestrator -->|Live API Key| Gemini
    AI_Orchestrator -->|Fallback / Offline| Fallback_Engine
    ServiceLayer --> Database
```

---

## 2. Component Architecture & Modular Layout

```mermaid
flowchart LR
    subgraph Presentation ["Presentation Layer"]
        Views["Page Views & Tabs"]
        State["TanStack Query Cache"]
        Components["Accessible Component Library"]
    end

    subgraph CoreBackend ["FastAPI Core"]
        Security["JWT Authentication Middleware"]
        CORS["CORS & Request Limiter"]
        Routers["REST API Routers (/api/v1)"]
    end

    subgraph CoreServices ["Core Services"]
        KnowledgeManager["Knowledge Base Indexer"]
        PrereqValidator["Prerequisite Cycle Detector"]
        PromptBuilder["Grounding Prompt Builder"]
        DocFormatter["Document Generator"]
    end

    subgraph DataAccess ["Repository & Persistence Layer"]
        ORM_Models["SQLAlchemy 2.0 ORM Models"]
        Alembic["Alembic Database Migrations"]
        SeedEngine["Initial Campus Data Seeder"]
    end

    Presentation --> CoreBackend
    CoreBackend --> CoreServices
    CoreServices --> DataAccess
```

---

## 3. AI & Grounded RAG Pipeline

The application strictly enforces that no external AI call can fabricate institutional facts:

```mermaid
sequenceDiagram
    autonumber
    actor Student as Student
    participant FE as React Frontend
    participant API as FastAPI /api/v1/chat
    participant RAG as RAG Service
    participant DB as Knowledge Database
    participant AI as AI Provider (Gemini)
    participant FB as Deterministic Fallback

    Student->>FE: Types query: "Prerequisites for Machine Learning?"
    FE->>API: POST /api/v1/chat {message, history}
    API->>RAG: Classify & Retrieve Knowledge
    RAG->>DB: Query Courses & Prereq Records
    DB-->>RAG: Matched Ground Truth (CS601: MA301, CS401)
    
    alt Gemini Key Valid & Available
        RAG->>AI: Call Gemini 2.5 Flash with Grounded System Prompt
        AI-->>RAG: Grounded Response + Markdown Output
        RAG-->>API: Response + Source Citations + Badge "gemini_live"
    else Gemini Offline / Timeout / Invalid Key
        RAG->>FB: Trigger Deterministic Local Fallback
        FB-->>RAG: Formatted Structured Knowledge + Badge "offline_knowledge_base"
        RAG-->>API: Response + Source Citations + Fallback Notice
    end

    API->>DB: Persist Conversation & Message
    API-->>FE: Return JSON Response with Sources & Badges
    FE-->>Student: Display Message Bubble + Citations
```

---

## 4. Database Relationship Diagram (High-Level)

```mermaid
erDiagram
    INSTITUTION ||--o{ DEPARTMENT : contains
    DEPARTMENT ||--o{ COURSE : offers
    COURSE ||--o{ PREREQUISITE : requires
    COURSE ||--o{ TIMETABLE_ENTRY : scheduled_in
    DEPARTMENT ||--o{ TIMETABLE_ENTRY : belongs_to
    FACULTY ||--o{ TIMETABLE_ENTRY : teaches
    CLASSROOM ||--o{ TIMETABLE_ENTRY : hosts
    EXAM_NOTICE ||--o{ EXAM_SCHEDULE : contains
    ADMIN_FAQ ||--o{ CAMPUS_CONTACT : references
    USER ||--o{ CONVERSATION : initiates
    CONVERSATION ||--o{ MESSAGE : contains
    MESSAGE ||--o{ CITATION : references
```

---

## 5. Architectural Decision Records (ADRs)

### ADR-01: Decoupled AI Provider Abstraction
- **Context**: Relying exclusively on proprietary SDK calls directly in endpoint handlers creates tight coupling and fragility.
- **Decision**: Define an abstract base class `BaseAIProvider` with concrete implementations `GeminiProvider` and `FallbackProvider`.
- **Consequences**: Enables swapping Gemini for OpenAI, Anthropic, or local open-weights models (Ollama/vLLM) by changing one environment variable (`AI_PROVIDER`).

### ADR-02: Deterministic Local Knowledge Fallback
- **Context**: External AI APIs can exhaust quota, time out, or require payment. Institutional data (timetables, course catalog, exam rules) must remain 100% accessible.
- **Decision**: Implement a local keyword/semantic structured matching fallback engine over the database knowledge chunks.
- **Consequences**: Zero downtime for core campus navigation even when API keys are omitted.

### ADR-03: Dual Database Strategy (PostgreSQL + SQLite Fallback)
- **Context**: Production deployments mandate PostgreSQL with connection pooling and potential pgvector embeddings, but local student/evaluator developer environments may lack a running Postgres daemon.
- **Decision**: SQLAlchemy 2.0 configuration detects `DATABASE_URL`. If a PostgreSQL URL is given, it uses PostgreSQL; otherwise, it seamlessly initializes SQLite (`sqlite:///./campus_assistant.db`).
- **Consequences**: Immediate local execution with zero setup, plus enterprise-grade PostgreSQL scalability in Docker.

### ADR-04: Strict Placeholder Mandate for Document Drafter
- **Context**: Generating formal legal and academic documents using generative AI poses risks of fabricating official credentials, registration numbers, or forged signatures.
- **Decision**: The document generator explicitly mandates bracketed placeholders (e.g. `[Student Name]`, `[Roll Number]`, `[Date]`) and strictly instructs LLMs never to fabricate personal identification.
- **Consequences**: High academic integrity, legal compliance, and editable utility.

# Technology Stack Specification
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Version**: 1.0.0
- **Status**: Released

---

## 1. Core Technology Selection Matrix

| Tier | Technology | Selected Version | Primary Purpose | Alternatives Evaluated | Justification |
|---|---|---|---|---|---|
| **Frontend Framework** | React | 19.x | Component-based UI & dynamic rendering | Next.js, Vue 3, Svelte | Maximum ecosystem compatibility with accessible component primitives and fast client-side navigation. |
| **Language (FE)** | TypeScript | 5.x | Strict static typing and type safety | JavaScript (ES2023) | Eliminates runtime type errors across API payload contracts. |
| **Build Tooling** | Vite | 6.x | Fast HMR & optimized production bundling | Webpack, Turbopack | Sub-second cold starts and optimized tree-shaking. |
| **Styling** | Tailwind CSS | 3.4+ | Utility-first styling & design tokens | CSS Modules, Styled Components | Zero runtime CSS overhead and rapid responsive design implementation. |
| **Iconography** | Lucide React | 0.400+ | Lightweight, consistent accessible icons | FontAwesome, Heroicons | Tree-shakeable SVG icons with native accessibility support. |
| **Server State** | TanStack Query | 5.x | Server caching, deduplication, retry logic | Redux Toolkit, SWR | Robust background refetching and seamless loading/error state management. |
| **Backend Framework** | FastAPI | 0.110+ | Asynchronous REST API framework | Django REST, Flask, Express | Native OpenAPI/Swagger generation, Python async support, high throughput. |
| **Language (BE)** | Python | 3.10+ / 3.11+ | Backend application logic & AI orchestration | Node.js, Go | Dominant ecosystem for AI/LLM SDKs and data modeling. |
| **Data Validation** | Pydantic | v2.6+ | Request/response schema validation | Marshmallow, Cerberus | C-accelerated validation via pydantic-core, seamless FastAPI integration. |
| **ORM / Data Access** | SQLAlchemy | 2.0+ | Relational object-relational mapping | Tortoise ORM, Peewee | Industry-standard declarative models with composable typing and migration support. |
| **Database Migrations** | Alembic | 1.13+ | Schema versioning and migration rollbacks | Flyway, Django Migrations | First-class integration with SQLAlchemy declarative metadata. |
| **Primary Database** | PostgreSQL | 15+ / 16+ | ACID relational storage & full-text search | MySQL, MongoDB | Rich JSON support, full-text search capabilities, and optional pgvector embeddings. |
| **Local DB Fallback** | SQLite | 3.x | Zero-config local development storage | In-memory dict | Enables immediate local testing without requiring a PostgreSQL daemon. |
| **AI Provider** | Google Gemini | 2.5 Flash | Conversational reasoning & grounding | OpenAI GPT-4o, Claude 3.5 | Superior latency/cost profile, large context window for campus knowledge. |
| **AI SDK** | google-genai | 1.x | Official Google GenAI Python client | google-generativeai (legacy) | Official modern SDK supporting structured outputs and unified client interface. |
| **Security & Auth** | PyJWT + Passlib | 2.8+ / 1.7+ | Token generation & bcrypt password hashing | OAuth2 proxies | Self-contained, secure stateless authentication and role-based authorization. |

---

## 2. Dependency Breakdown

### 2.1 Backend Dependencies (`requirements.txt`)
- `fastapi`: Modern async web API framework.
- `uvicorn[standard]`: High-performance ASGI web server.
- `pydantic`: Schema declaration and validation.
- `pydantic-settings`: Environment variable management.
- `sqlalchemy>=2.0.0`: Declarative ORM and connection pooling.
- `alembic`: Database migration tool.
- `psycopg[binary]`: PostgreSQL database adapter for Python.
- `python-jose[cryptography]` / `PyJWT`: JSON Web Token authentication.
- `passlib[bcrypt]`: Secure salted password hashing.
- `python-dotenv`: Environment variable loader from `.env`.
- `google-genai`: Google Gemini API client SDK.
- `pytest`: Automated testing framework.
- `httpx`: Async HTTP client for test requests.

### 2.2 Frontend Dependencies (`package.json`)
- `react`, `react-dom`: React 19 UI library.
- `typescript`: Static typing compiler.
- `vite`: Modern frontend development server and bundler.
- `tailwindcss`, `postcss`, `autoprefixer`: Utility styling pipeline.
- `lucide-react`: Icon system.
- `@tanstack/react-query`: Async state synchronization.
- `clsx`, `tailwind-merge`: Conditional class merging utilities.

---

## 3. Environment & Configuration Settings

| Variable Name | Default Value | Description |
|---|---|---|
| `APP_ENV` | `development` | Runtime environment (`development`, `production`, `test`) |
| `DATABASE_URL` | `sqlite:///./campus_assistant.db` | Connection string for PostgreSQL or SQLite |
| `GEMINI_API_KEY` | *(None)* | Google AI Studio API key |
| `GEMINI_MODEL` | `gemini-2.5-flash` | Gemini model tag |
| `SECRET_KEY` | `dev_campus_secret_key_change_in_production` | Secret key for signing JWT tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` | JWT token lifetime (24 hours) |
| `CORS_ORIGINS` | `*` | Allowed CORS origins (comma-separated) |
| `AI_TIMEOUT_SECONDS` | `10` | Timeout before triggering deterministic fallback |
| `AI_MAX_RETRIES` | `2` | Number of retry attempts on transient AI failures |

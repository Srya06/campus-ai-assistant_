# REST API Documentation (v1)
## Campus AI Assistant — Student-Centric Academic Navigator & Advisory System

- **Base URL**: `http://localhost:8000/api/v1`
- **Interactive Documentation**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative Specification**: `http://localhost:8000/redoc` (ReDoc)

---

## 1. Authentication & Security Conventions

Protected endpoints require a Bearer token in the `Authorization` header:
```http
Authorization: Bearer <jwt_access_token>
```
Standard Error Responses:
- `400 Bad Request`: Payload validation failed.
- `401 Unauthorized`: Token missing or expired.
- `403 Forbidden`: User role lacks permission.
- `404 Not Found`: Resource ID does not exist.
- `500 Internal Server Error`: Unhandled server exception.

---

## 2. API Endpoints Catalog

### 2.1 System & Health

#### `GET /health` / `GET /api/v1/health`
Checks backend and database health status.
- **Response `200 OK`**:
  ```json
  {
    "status": "healthy",
    "timestamp": 1795525813.67,
    "database": "connected",
    "gemini_live_connected": true,
    "mode": "Live Gemini AI + Campus Knowledge Base"
  }
  ```

#### `GET /api/v1/health/ai`
Checks whether Gemini API is actively responding.
- **Response `200 OK`**:
  ```json
  {
    "provider": "gemini-2.5-flash",
    "status": "available",
    "fallback_ready": true
  }
  ```

---

### 2.2 Conversational AI Assistant

#### `POST /api/v1/chat`
Submits a student query to the assistant.
- **Request Body**:
  ```json
  {
    "message": "What are the prerequisites for Machine Learning?",
    "history": [
      {"role": "user", "content": "Hi"},
      {"role": "model", "content": "Hello! How can I assist you with your campus queries today?"}
    ],
    "conversation_id": "optional-uuid"
  }
  ```
- **Response `200 OK`**:
  ```json
  {
    "response": "To enroll in Machine Learning (CS601), you must complete: ...",
    "source": "gemini_live",
    "citations": [
      {
        "type": "course",
        "code": "CS601",
        "title": "Machine Learning",
        "verified_date": "2026-03-10"
      }
    ],
    "is_fallback": false,
    "conversation_id": "c7a83d91-..."
  }
  ```

#### `GET /api/v1/conversations`
Retrieves past conversations for the authenticated user.

#### `GET /api/v1/conversations/{conversation_id}`
Retrieves messages for a specific conversation session.

#### `DELETE /api/v1/conversations/{conversation_id}`
Deletes a conversation history session.

---

### 2.3 Timetables

#### `GET /api/v1/timetable`
Fetches structured timetable schedules with optional filters.
- **Query Parameters**:
  - `department` (e.g., `CSE`, `ECE`)
  - `semester` (e.g., `Sem 4`, `Sem 6`)
  - `day` (e.g., `Monday`, `Tuesday`, `All`)
  - `section` (default `A`)
- **Response `200 OK`**:
  ```json
  {
    "department": "CSE",
    "semester": "Sem 4",
    "schedule": {
      "Monday": [
        {
          "time": "09:00 - 10:00 AM",
          "subject": "Design & Analysis of Algorithms",
          "code": "CS401",
          "faculty": "Dr. Sharma",
          "room": "LH-101",
          "is_lab": false
        }
      ]
    }
  }
  ```

---

### 2.4 Courses & Prerequisite Graph

#### `GET /api/v1/courses`
Lists all courses with filtering by department and semester.
- **Query Parameters**: `department`, `semester`, `query`
- **Response `200 OK`**:
  ```json
  [
    {
      "id": "c401-uuid",
      "code": "CS401",
      "title": "Design & Analysis of Algorithms",
      "credits": 4,
      "semester": 4,
      "department": "CSE",
      "prerequisites": ["CS201 (Data Structures)", "MA201 (Discrete Mathematics)"],
      "corequisites": ["CS401P (Algorithms Lab)"],
      "description": "Asymptotic notation, Divide & Conquer, Dynamic Programming..."
    }
  ]
  ```

#### `GET /api/v1/courses/{course_id}/prerequisites`
Returns the complete upstream dependency graph for a course.

---

### 2.5 Course Notes & Study Materials (PDF Engine)

#### `GET /api/v1/notes`
Lists all verified course lecture notes and study modules.
- **Query Parameters**: `course_id`, `course_code`, `semester`, `search`
- **Response `200 OK`**:
  ```json
  [
    {
      "id": "note-uuid",
      "course_code": "CS401",
      "course_title": "Design & Analysis of Algorithms",
      "title": "Dynamic Programming & Greedy Strategies",
      "unit_number": 2,
      "unit_title": "Dynamic Programming Framework",
      "faculty_author": "Dr. Sharma",
      "file_format": "PDF",
      "download_count": 78
    }
  ]
  ```

#### `GET /api/v1/notes/{note_id}`
Returns full study material content and topic outline for in-app reading.

#### `GET /api/v1/notes/{note_id}/download`
Generates and streams an official high-fidelity university PDF with institutional header, syllabus outline, and formatted lecture notes. Automatically increments the download counter.
- **Response Header**: `Content-Type: application/pdf`, `Content-Disposition: attachment; filename="CS401_Unit_2_Dynamic_Programming.pdf"`

---

### 2.6 Examination Notices

#### `GET /api/v1/exams`
Fetches all active exam notices, date sheets, and guidelines.
- **Response `200 OK`**:
  ```json
  [
    {
      "id": "EXAM-2026-01",
      "title": "Mid-Semester Examination Schedule - Even Sem 2026",
      "exam_type": "Mid-Semester",
      "applicable_to": "Sem 4 & Sem 6",
      "exam_window": "April 06, 2026 to April 15, 2026",
      "calculator_policy": "Non-programmable scientific calculators permitted only for Math & Electronics.",
      "is_urgent": true
    }
  ]
  ```

---

### 2.6 Administrative Helpdesk

#### `GET /api/v1/faqs`
Retrieves categorized campus administrative FAQs.
- **Query Parameters**: `category`, `search`

---

### 2.7 Academic Document Generation

#### `POST /api/v1/documents/generate`
Drafts an official academic communication.
- **Request Body**:
  ```json
  {
    "type": "Leave Letter",
    "message": "Viral fever from March 18 to March 20, 2026",
    "tone": "Formal",
    "length": "Medium"
  }
  ```
- **Response `200 OK`**:
  ```json
  {
    "output": "Date: March 18, 2026\n\nTo,\nThe Head of Department...",
    "type": "Leave Letter",
    "status": "success",
    "source": "gemini_live"
  }
  ```

---

### 2.8 Protected Administration Endpoints

- `POST /api/v1/admin/courses`: Create course (requires `role: admin`).
- `PUT /api/v1/admin/courses/{id}`: Update course.
- `DELETE /api/v1/admin/courses/{id}`: Delete course.
- `POST /api/v1/admin/timetable`: Insert/update timetable entries.
- `POST /api/v1/admin/exams`: Publish examination notice.
- `POST /api/v1/admin/faqs`: Add administrative FAQ entry.

---

### 2.9 Authentication & Registration

#### `POST /api/v1/auth/register`
Creates a new Student or Administrator account.
- **Request Body**:
  ```json
  {
    "username": "surya",
    "email": "surya@campus.edu",
    "password": "mypassword123",
    "full_name": "Surya D.",
    "role": "student",
    "department": "CSE (AI)",
    "semester": "Sem 5 (CSE - AI)",
    "cgpa": "8.0"
  }
  ```
- **Response `201 Created`**:
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "token_type": "bearer",
    "user_id": "usr-uuid",
    "username": "surya",
    "role": "student",
    "full_name": "Surya D.",
    "department": "CSE (AI)",
    "semester": "Sem 5 (CSE - AI)",
    "cgpa": "8.0"
  }
  ```

#### `POST /api/v1/auth/login`
Authenticates a user and returns a signed JWT access token.
- **Request Body**:
  ```json
  {
    "username": "surya",
    "password": "mypassword123"
  }
  ```
- **Response `200 OK`**:
  Returns `TokenResponse` with JWT and profile metadata.

#### `GET /api/v1/auth/me`
Retrieves detailed profile information for the authenticated user.

#### `PUT /api/v1/auth/profile`
Updates student profile metrics and credentials.
- **Request Body (`StudentProfileUpdateRequest`)**:
  ```json
  {
    "full_name": "Surya D.",
    "roll_number": "22AI104",
    "cgpa": "8.25",
    "resume_url": "https://campus.edu/resumes/surya.pdf",
    "skills": "Python, Machine Learning, FastAPI, PostgreSQL, React",
    "phone": "+91 98765 43210"
  }
  ```
- **Response `200 OK`**:
  Returns updated `UserResponse`.

---

### 2.10 Course Notes & Materials (PDF Generator)

#### `GET /api/v1/notes`
Lists all published lecture notes and course study materials.
- **Query Parameters**:
  - `course_id` (optional): Filter by course UUID.
  - `course_code` (optional): Filter by course code, e.g. `CS401`.

#### `GET /api/v1/notes/{id}`
Returns details and markdown content for a specific lecture note.

#### `GET /api/v1/notes/{id}/download`
Generates and streams an official university-formatted PDF with institutional header, metadata table, syllabus topic callout box, and clean typography. Automatically increments download count.
- **Response**: `application/pdf` binary stream.

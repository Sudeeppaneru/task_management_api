# Task Management REST API

A robust personal Task Management REST API built with Python, FastAPI, SQLAlchemy 2.x, Pydantic 2.x, and PostgreSQL, following clean layered architecture and strict security principles.

## Features

- **Authentication & Security:** User registration with password hashing (bcrypt), JWT-based bearer token authentication, secure session handling, and ownership enforcement.
- **User Profile:** Retrieve and update authenticated user profile (`/api/v1/users/me`).
- **Task Management:** Create, list (with pagination), retrieve, partially update, and soft-delete tasks. Automatic completion timestamps (`completed_on`) and date validation.
- **Milestone Management:** Nested under tasks (`/api/v1/tasks/{task_id}/milestones`), support CRUD, completion, and soft deletion with parent task ownership verification.
- **Health Check:** Liveness endpoint at `/health`.
- **Database Migrations:** Version-controlled Alembic migrations.
- **Testing:** Comprehensive automated test suite using `pytest` and FastAPI `TestClient`.

---

## Getting Started

### 1. Prerequisites
- Python 3.11+
- PostgreSQL

### 2. Installation
Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Configuration
Copy `.env.example` to `.env` and configure your PostgreSQL database connection string and secret key:
```bash
cp .env.example .env
```

### 4. Database Migrations
Run Alembic database migrations against your database:
```bash
python -m alembic upgrade head
```

### 5. Running the Application
Start the development server using `run.py`:
```bash
python run.py
```
Or via uvicorn directly:
```bash
uvicorn src.main:app --reload
```

Interactive API documentation (Swagger UI) is available at: `http://127.0.0.1:8000/docs`

---

## Running Tests

Run the test suite using pytest:
```bash
python -m pytest
```

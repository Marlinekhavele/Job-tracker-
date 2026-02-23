# 🎯 Job Application Tracker API

A clean FastAPI backend to monitor your job applications tracking status, follow-ups, and progress across every company you apply to.

## Project Structure

```
job_tracker/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   └── main.py
├── tests/
│   ├── unit/
│   └── integration/
├── .env.example
├── .gitignore
├── pyproject.toml
├── pytest.ini
├── README.md
├── requirements.txt
└── job_tracker.egg-info/
```

## Layered Architecture

```
Router → Service → Repository → Database

```

## Setup

```bash
# 1. Create virtualenv
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies |
#uv sync 
pip install -r requirements.txt

# 3. Copy env file
cp .env.example .env

# 4. Run the server
uvicorn app.main:app --reload
```

Open: http://localhost:8000/docs

## Run Tests

```bash
# All tests
pytest

# Verbose
pytest -v

# Unit only
pytest tests/unit/

# Integration only
pytest tests/integration/
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/api/v1/applications/` | Track a new application |
| `GET` | `/api/v1/applications/` | List all (filter by status/company) |
| `GET` | `/api/v1/applications/dashboard` | Stats overview |
| `GET` | `/api/v1/applications/{id}` | Get single application |
| `PATCH` | `/api/v1/applications/{id}` | Update status / notes |
| `DELETE` | `/api/v1/applications/{id}` | Remove application |
| `GET` | `/health` | Health check |

## Application Statuses

`pending` → `applied` → `phone_screen` → `interview` → `technical` → `offer` / `rejected` / `withdrawn`

## Example: Track a New Application

```bash
curl -X POST http://localhost:8000/api/v1/applications/ \
  -H "Content-Type: application/json" \
  -d '{
    "company": "Stripe",
    "role": "Senior Backend Engineer",
    "location": "Berlin, Germany",
    "salary_range": "€90k-€110k",
    "status": "applied",
    "resume_version": "v3",
    "notes": "Applied via LinkedIn. Spoke to recruiter Sarah.",
    "follow_up_date": "2024-07-15T09:00:00"
  }'
```

## Example: Dashboard Stats

```bash
curl http://localhost:8000/api/v1/applications/dashboard
```

```json
{
  "total": 12,
  "by_status": {
    "pending": 2,
    "applied": 5,
    "interview": 3,
    "offer": 1,
    "rejected": 1
  },
  "follow_ups_due": 3,
  "latest_applications": [...]
}
```

## Tech Stack

- **FastAPI** — async web framework
- **SQLAlchemy 2.0** — async ORM
- **Pydantic v2** — data validation
- **SQLite / aiosqlite** — DB 
- **Pytest + pytest-asyncio** — unit & integration tests



# ResumeAgent

ResumeAgent is an AI resume optimization platform with a Next.js frontend, a FastAPI backend, PostgreSQL, and GitHub OAuth-based authentication.

## Layout

- `frontend/` - Next.js 14 App Router UI
- `backend/` - FastAPI REST API, JWT auth, async SQLAlchemy
- `ai/` - resume parsing, skill extraction, and ATS scoring helpers
- `docker-compose.yml` - local development stack

## Setup

1. Copy `.env.example` to `.env` and fill in the OAuth and secret values.
2. Start the stack:

```bash
docker compose up --build
```

3. Open:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Health: `http://localhost:8000/health`

## Backend

The backend uses async SQLAlchemy sessions against PostgreSQL, JWT bearer auth for protected routes, and GitHub OAuth on `/auth/github` and `/auth/github/callback`.

## Local Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

```bash
cd frontend
npm install
npm run dev
```

## Notes

- Resume uploads accept PDF and DOCX files up to 5MB.
- Job uploads accept plain text or PDF files up to 5MB.
- The AI pipeline is stubbed with deterministic mock scoring for now.

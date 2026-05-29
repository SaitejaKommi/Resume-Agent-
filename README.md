<<<<<<< HEAD

=======
# ResumeAgent

ResumeAgent is a monorepo for an AI resume optimization platform with a Next.js 14 frontend, a FastAPI backend, PostgreSQL persistence, and local AI processing helpers.

## Structure

- `frontend/` - Next.js 14 App Router, Tailwind CSS, TypeScript
- `backend/` - FastAPI, SQLAlchemy, PostgreSQL, GitHub OAuth
- `ai/` - standalone AI processing utilities used by backend services
- `docker-compose.yml` - local production-style stack

## Prerequisites

- Docker and Docker Compose
- Python 3.11 if you want to run the backend outside Docker
- Node.js 18+ if you want to run the frontend outside Docker

## Setup

1. Copy `.env.example` to `.env` and fill in the values.
2. Create a GitHub OAuth App with callback URL `http://localhost:8000/auth/github/callback`.
3. Start the stack:

```bash
docker compose up --build
```

4. Open the apps:
- Frontend: `http://localhost:3000`
- Backend: `http://localhost:8000`
- Health check: `http://localhost:8000/health`

## Local Backend Run

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Local Frontend Run

```bash
cd frontend
npm install
npm run dev
```

## Database Tables

- `users` - stores email, GitHub token, and timestamps
- `resumes` - stores raw text and parsed JSON payloads
- `jobs` - stores job descriptions and extracted skills
- `applications` - stores resume/job links and ATS scores

## GitHub OAuth Flow

The backend exposes `/auth/github/login`, which redirects to GitHub. The callback stores the OAuth token in the `users` table and returns the authenticated profile payload.

## Notes

- The AI helpers in `ai/` are deterministic heuristics that can be swapped for an LLM-backed pipeline later.
- `NEXTAUTH_SECRET` is included in the environment contract for future frontend auth/session use.
>>>>>>> db7155f (fix(phase-1-layout): flatten ResumeAgent to repository root)

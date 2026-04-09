# Claude AI Guidance — Expense Tracker

## Project Context
This is a full-stack expense tracking application.
- Backend: Python 3.11 + Flask + SQLAlchemy + SQLite
- Frontend: React 18 + TypeScript + Vite
- AI Feature: Claude API for expense categorization

## Coding Standards

### Python (Backend)
- Use type hints on ALL function signatures
- All endpoints return `{"data": ..., "error": null}` or `{"data": null, "error": "message"}`
- Never return raw exceptions to the client
- Use Pydantic schemas for request validation — raise 422 if invalid
- All DB writes must go through the service layer, never directly from routes
- Log errors with `app.logger.error(...)`, never `print()`
- Every new route MUST have a corresponding test in `tests/`

### React (Frontend)
- Use TypeScript strictly — no `any` types
- API calls live in `src/api/` only — components never call fetch directly
- Use custom hooks for data fetching (e.g. `useExpenses`)
- Handle loading, error, and empty states in every component
- Form inputs must be validated before submission

## AI Usage Rules (Claude API Integration)
- AI categorization is ADVISORY — user can always override
- Never send PII or sensitive data to the AI API
- Wrap all AI calls in try/except — degrade gracefully if AI fails
- AI responses must be validated against the known category enum before use
- Log AI latency and failures for observability

## What AI Should NOT Do
- Do not generate database migration files — write those manually
- Do not skip error handling "for brevity"
- Do not use `SELECT *` in queries
- Do not store secrets in code — use environment variables

## Constraints
- Keep each function under 40 lines
- No circular imports
- All amounts stored as integers (cents) to avoid float precision bugs

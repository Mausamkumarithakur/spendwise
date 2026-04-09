# Spendwise — AI-Powered Expense Tracker

A full-stack expense tracking app with AI-assisted categorization.

![Full Stack](https://img.shields.io/badge/Stack-Full%20Stack-blueviolet)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?logo=python&logoColor=white)
![Flask API](https://img.shields.io/badge/API-Flask-000000?logo=flask&logoColor=white)
![React](https://img.shields.io/badge/UI-React%2018-61DAFB?logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6?logo=typescript&logoColor=white)
![SQLite](https://img.shields.io/badge/DB-SQLite-003B57?logo=sqlite&logoColor=white)
![AI Integration](https://img.shields.io/badge/AI-Claude-6B21A8)
![Status](https://img.shields.io/badge/Project-Production%20Ready-brightgreen)

---

## Quick Start

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env          # add your ANTHROPIC_API_KEY
python app.py                 # runs on http://localhost:5000
```

### Frontend

```bash
cd frontend
npm install
npm run dev                   # runs on http://localhost:5173
```

### Run Tests

```bash
cd backend
pytest tests/ -v
```

---

## Architecture

```
expense-tracker/
├── backend/
│   ├── app.py              # Flask app factory
│   ├── config.py           # All env/config access
│   ├── models.py           # SQLAlchemy models (Expense, Category enum)
│   ├── schemas.py          # Pydantic request validation
│   ├── routes/
│   │   └── expenses.py     # Thin HTTP layer — delegates to services
│   ├── services/
│   │   ├── expense_service.py   # All business logic
│   │   └── ai_service.py        # Claude API integration
│   └── tests/
│       ├── conftest.py     # Fixtures (in-memory DB)
│       └── test_expenses.py     # 16 tests: happy + error paths
├── frontend/
│   └── src/
│       ├── api/            # All fetch calls (never in components)
│       ├── components/     # ExpenseForm, ExpenseList, Dashboard, FilterBar
│       ├── hooks/          # useExpenses — data + mutations
│       ├── types/          # Shared TypeScript types
│       └── App.tsx
└── ai-guidance/
    ├── claude.md           # Coding standards for AI agents
    └── agents.md           # Workflow + constraints for AI code generation
```

---

## Key Technical Decisions

### 1. Amounts stored as integers (cents)
**Problem:** Floating-point arithmetic causes subtle bugs in financial calculations (e.g. `0.1 + 0.2 !== 0.3`).
**Decision:** All amounts are stored as `INTEGER` cents in the DB and converted to display dollars only at the boundary (API response, UI).
**Tradeoff:** Slightly more conversion code; eliminates an entire class of bugs.

### 2. Service layer between routes and DB
**Problem:** Fat route handlers are hard to test and couple HTTP concerns with business logic.
**Decision:** Routes only parse requests and shape responses. All logic (filtering, AI calls, DB writes) lives in `expense_service.py`.
**Benefit:** Tests can call service functions directly without HTTP overhead.

### 3. AI categorization is advisory and non-blocking
**Problem:** If the AI API is slow or unavailable, the whole expense creation fails.
**Decision:** `ai_service.suggest_category()` catches all exceptions and returns `Category.OTHER` on any failure. A timeout of 5 seconds is enforced. The `ai_categorized` flag on the model lets users see which entries were AI-suggested.
**Tradeoff:** AI failures are silent to the user (logged server-side). This is acceptable because the feature is advisory — users can always override the category manually.

### 4. Pydantic for request validation
**Decision:** All incoming request bodies are parsed with Pydantic schemas (`schemas.py`) before reaching the service layer. Invalid data returns HTTP 422 with a clear message — the service layer never sees malformed input.
**Benefit:** The service layer can trust its inputs. Type safety enforced at the boundary.

### 5. Unified API response envelope
All endpoints return `{"data": ..., "error": null}` or `{"data": null, "error": "message"}`. This means the frontend has one consistent way to check for errors, and clients never need to inspect HTTP status codes alone.

### 6. TypeScript strict mode + no `any`
The frontend uses `strict: true` in tsconfig. The API layer (`src/api/`) uses the same TypeScript types as the components, so a backend schema change propagates as a compile error.

### 7. Vite proxy for local dev
Vite proxies `/api/*` to Flask at `localhost:5000`, so the frontend never needs CORS configuration during development, and no hardcoded backend URLs appear in component code.

---

## API Reference

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/expenses/` | List expenses (filterable by `category`, `start_date`, `end_date`) |
| POST | `/api/expenses/` | Create expense (AI categorizes if `category` omitted) |
| GET | `/api/expenses/:id` | Get single expense |
| PATCH | `/api/expenses/:id` | Partial update |
| DELETE | `/api/expenses/:id` | Delete |
| GET | `/api/expenses/summary` | Aggregated totals by category |
| GET | `/api/health` | Health check |

---

## AI Usage

### Where AI is used
Claude Haiku (`claude-haiku-4-5`) categorizes expenses when the user omits a category. It receives only the description and amount — no user identity or PII.

### How AI guidance files constrain generation
`ai-guidance/claude.md` and `agents.md` were used during development to instruct Claude Code on:
- Response envelope shape (all routes must use `_ok`/`_err` helpers)
- Forbidden patterns (`SELECT *`, hardcoded categories, bare `except: pass`)
- AI feature constraints (validate response against enum, default to OTHER, 5s timeout)
- Test requirements (every endpoint needs happy + error path)

All AI-generated code was reviewed for correctness, security, and adherence to these constraints before being committed.

---

## Risks and Weaknesses

| Risk | Mitigation |
|------|-----------|
| SQLite not suitable for production concurrency | Swap `DATABASE_URL` for Postgres — SQLAlchemy abstracts the difference |
| No authentication | All expenses are global; add Flask-JWT or session auth for multi-user |
| AI API cost on every create | Cache common descriptions; add a manual-only mode toggle |
| No pagination | `list_expenses` returns all rows — add `LIMIT`/`OFFSET` for large datasets |
| CORS allows localhost only | Update `origins` in `app.py` for deployed environments |

---

## Extension Approach

**Adding a new field (e.g. `tags`):**
1. Add column to `models.py`
2. Add field to `ExpenseCreate`/`ExpenseUpdate` in `schemas.py`
3. Update `expense_service.py` create/update logic
4. Add to `to_dict()` return
5. Add type to `frontend/src/types/index.ts`
6. Update `ExpenseForm` and `ExpenseList`
No other files need to change — the boundaries contain the blast radius.

**Adding a new AI feature (e.g. duplicate detection):**
Add a new function to `ai_service.py`, call it from `expense_service.py`. The route and frontend are unaffected until you're ready to surface it.

---

## Running in Production

```bash
# Backend
pip install gunicorn
gunicorn "app:create_app()" -w 4 -b 0.0.0.0:5000

# Frontend
npm run build   # outputs to dist/ — serve with nginx or any static host
```

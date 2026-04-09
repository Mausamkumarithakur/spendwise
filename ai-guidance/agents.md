# Agent Instructions — Expense Tracker

## Agent Role
You are a careful backend/fullstack engineer. Your job is to add features
to this expense tracker without breaking existing behavior.

## Before Writing Any Code
1. Read `claude.md` for coding standards
2. Read the relevant service file before modifying it
3. Check existing tests to understand expected behavior

## Workflow
1. Understand the feature request fully before writing code
2. Write the service/model layer first
3. Write the route (thin — delegate to service)
4. Write the test
5. Only then write frontend code

## Response Contracts
Every Flask route must return:
```python
# Success
{"data": <payload>, "error": None}

# Failure  
{"data": None, "error": "<human-readable message>"}, <status_code>
```

## Database Rules
- Never mutate DB objects outside a `db.session` block
- Always call `db.session.commit()` after writes
- Use `db.session.rollback()` in except blocks

## Forbidden Patterns
- `except Exception: pass` — always handle or re-raise
- Hardcoded category strings — use the `Category` enum
- Direct `os.environ[key]` — use `config.py` getters

## Testing Rules
- Every new endpoint needs a happy-path and an error-path test
- Use the test client fixture, never a real DB
- Assert both the status code and the response shape

## AI Categorization Feature
When asked to categorize an expense:
- Send ONLY: description (string), amount (int cents)
- Expect back: one of the Category enum values
- If response is not a valid category, default to "OTHER"
- Timeout after 5 seconds — return "OTHER" on timeout

"""
Expense service — all business logic lives here.
Routes are thin wrappers; this layer owns the rules.
"""
from __future__ import annotations
from datetime import date
from typing import Optional
from flask import current_app
from models import db, Expense, Category
from schemas import ExpenseCreate, ExpenseUpdate
from services.ai_service import suggest_category


def create_expense(payload: ExpenseCreate) -> Expense:
    """
    Create a new expense. If no category is provided, ask AI to suggest one.
    AI failure is non-fatal — defaults to OTHER.
    """
    category = payload.category
    ai_categorized = False

    if category is None:
        suggested = suggest_category(payload.description, payload.amount_cents())
        category = suggested
        ai_categorized = suggested != Category.OTHER

    expense = Expense(
        description=payload.description,
        amount_cents=payload.amount_cents(),
        category=category,
        date=payload.date,
        note=payload.note,
        ai_categorized=ai_categorized,
    )
    db.session.add(expense)
    db.session.commit()
    return expense


def list_expenses(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> list[Expense]:
    """Return expenses with optional filters, newest first."""
    query = db.select(Expense)

    if category:
        query = query.where(Expense.category == category)
    if start_date:
        query = query.where(Expense.date >= start_date)
    if end_date:
        query = query.where(Expense.date <= end_date)

    query = query.order_by(Expense.date.desc(), Expense.id.desc())
    return list(db.session.scalars(query))


def get_expense(expense_id: int) -> Optional[Expense]:
    return db.session.get(Expense, expense_id)


def update_expense(expense: Expense, payload: ExpenseUpdate) -> Expense:
    """Apply partial update — only fields provided in payload are changed."""
    if payload.description is not None:
        expense.description = payload.description
    if payload.amount is not None:
        expense.amount_cents = payload.amount_cents()  # type: ignore[assignment]
    if payload.category is not None:
        expense.category = payload.category
        expense.ai_categorized = False  # manual override
    if payload.date is not None:
        expense.date = payload.date
    if payload.note is not None:
        expense.note = payload.note

    db.session.commit()
    return expense


def delete_expense(expense: Expense) -> None:
    db.session.delete(expense)
    db.session.commit()


def get_summary() -> dict:
    """Aggregate totals per category for the dashboard."""
    expenses = list_expenses()
    totals: dict[str, int] = {cat.value: 0 for cat in Category}
    for exp in expenses:
        totals[exp.category] += exp.amount_cents

    return {
        "by_category": [
            {"category": cat, "total_cents": cents, "total": round(cents / 100, 2)}
            for cat, cents in totals.items()
        ],
        "grand_total_cents": sum(totals.values()),
        "grand_total": round(sum(totals.values()) / 100, 2),
        "count": len(expenses),
    }

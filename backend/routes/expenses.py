"""
Expense routes — thin layer that delegates to service.
Handles HTTP concerns only: parsing, validation, response shaping.
"""
from __future__ import annotations
from datetime import date
from flask import Blueprint, request, current_app
from pydantic import ValidationError
from models import Category
from schemas import ExpenseCreate, ExpenseUpdate
from services import expense_service

bp = Blueprint("expenses", __name__, url_prefix="/api/expenses")


def _ok(data: object) -> tuple:
    return {"data": data, "error": None}, 200


def _err(message: str, status: int) -> tuple:
    return {"data": None, "error": message}, status


@bp.get("/")
def list_expenses():
    category = request.args.get("category")
    start = request.args.get("start_date")
    end = request.args.get("end_date")

    if category and category not in {c.value for c in Category}:
        return _err(f"Invalid category '{category}'", 422)

    try:
        start_date = date.fromisoformat(start) if start else None
        end_date = date.fromisoformat(end) if end else None
    except ValueError:
        return _err("Dates must be in YYYY-MM-DD format", 422)

    expenses = expense_service.list_expenses(category, start_date, end_date)
    return _ok([e.to_dict() for e in expenses])


@bp.post("/")
def create_expense():
    try:
        payload = ExpenseCreate.model_validate(request.get_json(force=True) or {})
    except ValidationError as exc:
        return _err(exc.errors()[0]["msg"], 422)

    expense = expense_service.create_expense(payload)
    return {"data": expense.to_dict(), "error": None}, 201


@bp.get("/<int:expense_id>")
def get_expense(expense_id: int):
    expense = expense_service.get_expense(expense_id)
    if not expense:
        return _err(f"Expense {expense_id} not found", 404)
    return _ok(expense.to_dict())


@bp.patch("/<int:expense_id>")
def update_expense(expense_id: int):
    expense = expense_service.get_expense(expense_id)
    if not expense:
        return _err(f"Expense {expense_id} not found", 404)

    try:
        payload = ExpenseUpdate.model_validate(request.get_json(force=True) or {})
    except ValidationError as exc:
        return _err(exc.errors()[0]["msg"], 422)

    updated = expense_service.update_expense(expense, payload)
    return _ok(updated.to_dict())


@bp.delete("/<int:expense_id>")
def delete_expense(expense_id: int):
    expense = expense_service.get_expense(expense_id)
    if not expense:
        return _err(f"Expense {expense_id} not found", 404)
    expense_service.delete_expense(expense)
    return _ok({"deleted": expense_id})


@bp.get("/summary")
def get_summary():
    return _ok(expense_service.get_summary())

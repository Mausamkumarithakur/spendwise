"""
Tests for expense CRUD endpoints.
Every endpoint has a happy-path and at least one error-path test.
"""
import json
from unittest.mock import patch
from models import Category


def _post(client, payload: dict):
    return client.post(
        "/api/expenses/",
        data=json.dumps(payload),
        content_type="application/json",
    )


def _patch(client, expense_id: int, payload: dict):
    return client.patch(
        f"/api/expenses/{expense_id}",
        data=json.dumps(payload),
        content_type="application/json",
    )


VALID_EXPENSE = {
    "description": "Coffee",
    "amount": 4.50,
    "category": "FOOD",
    "date": "2024-06-01",
}


# ── CREATE ─────────────────────────────────────────────────────────────────────

def test_create_expense_happy_path(client):
    resp = _post(client, VALID_EXPENSE)
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["error"] is None
    assert body["data"]["description"] == "Coffee"
    assert body["data"]["amount_cents"] == 450
    assert body["data"]["category"] == "FOOD"


def test_create_expense_missing_description(client):
    resp = _post(client, {**VALID_EXPENSE, "description": ""})
    assert resp.status_code == 422
    assert resp.get_json()["error"] is not None


def test_create_expense_negative_amount(client):
    resp = _post(client, {**VALID_EXPENSE, "amount": -10})
    assert resp.status_code == 422


def test_create_expense_invalid_category(client):
    resp = _post(client, {**VALID_EXPENSE, "category": "INVALID"})
    assert resp.status_code == 422


def test_create_expense_ai_categorization(client):
    """When no category is provided, AI service is called."""
    with patch("services.ai_service.suggest_category", return_value=Category.TRANSPORT) as mock_ai:
        resp = _post(client, {k: v for k, v in VALID_EXPENSE.items() if k != "category"})
    assert resp.status_code == 201
    body = resp.get_json()
    assert body["data"]["category"] == "TRANSPORT"
    assert body["data"]["ai_categorized"] is True
    mock_ai.assert_called_once()


# ── READ ───────────────────────────────────────────────────────────────────────

def test_list_expenses_empty(client):
    resp = client.get("/api/expenses/")
    assert resp.status_code == 200
    assert resp.get_json()["data"] == []


def test_list_expenses_returns_created(client):
    _post(client, VALID_EXPENSE)
    resp = client.get("/api/expenses/")
    assert len(resp.get_json()["data"]) == 1


def test_list_expenses_filter_by_category(client):
    _post(client, VALID_EXPENSE)  # FOOD
    _post(client, {**VALID_EXPENSE, "category": "TRANSPORT", "description": "Bus"})
    resp = client.get("/api/expenses/?category=FOOD")
    data = resp.get_json()["data"]
    assert len(data) == 1
    assert data[0]["category"] == "FOOD"


def test_list_expenses_invalid_category_filter(client):
    resp = client.get("/api/expenses/?category=GARBAGE")
    assert resp.status_code == 422


def test_get_expense_not_found(client):
    resp = client.get("/api/expenses/9999")
    assert resp.status_code == 404


# ── UPDATE ─────────────────────────────────────────────────────────────────────

def test_update_expense_happy_path(client):
    created = _post(client, VALID_EXPENSE).get_json()["data"]
    resp = _patch(client, created["id"], {"description": "Latte", "amount": 5.0})
    assert resp.status_code == 200
    body = resp.get_json()["data"]
    assert body["description"] == "Latte"
    assert body["amount_cents"] == 500


def test_update_expense_clears_ai_flag_on_category_change(client):
    created = _post(client, {**VALID_EXPENSE, "category": None}).get_json()
    expense_id = created["data"]["id"]
    resp = _patch(client, expense_id, {"category": "HEALTH"})
    assert resp.get_json()["data"]["ai_categorized"] is False


def test_update_nonexistent_expense(client):
    resp = _patch(client, 9999, {"description": "Ghost"})
    assert resp.status_code == 404


# ── DELETE ─────────────────────────────────────────────────────────────────────

def test_delete_expense(client):
    created = _post(client, VALID_EXPENSE).get_json()["data"]
    resp = client.delete(f"/api/expenses/{created['id']}")
    assert resp.status_code == 200
    assert client.get(f"/api/expenses/{created['id']}").status_code == 404


def test_delete_nonexistent_expense(client):
    resp = client.delete("/api/expenses/9999")
    assert resp.status_code == 404


# ── SUMMARY ───────────────────────────────────────────────────────────────────

def test_summary_totals(client):
    _post(client, {**VALID_EXPENSE, "amount": 10.00})
    _post(client, {**VALID_EXPENSE, "amount": 5.00})
    resp = client.get("/api/expenses/summary")
    body = resp.get_json()["data"]
    assert body["grand_total"] == 15.0
    assert body["count"] == 2

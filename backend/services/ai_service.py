"""
AI categorization service — wraps the Anthropic API.
Contract: always returns a valid Category enum value.
Never raises — degrades to OTHER on any failure.
"""
from __future__ import annotations
import anthropic
from flask import current_app
from models import Category

_SYSTEM_PROMPT = """You are an expense categorization assistant.
Given a description and amount, respond with EXACTLY ONE of these category codes:
FOOD, TRANSPORT, HOUSING, HEALTH, ENTERTAINMENT, SHOPPING, UTILITIES, OTHER

Rules:
- Respond with ONLY the category code — no explanation, no punctuation
- If unsure, use OTHER
- Examples: "Uber ride" → TRANSPORT, "Netflix" → ENTERTAINMENT, "Rent" → HOUSING
"""

_VALID_CATEGORIES = {cat.value for cat in Category}


def suggest_category(description: str, amount_cents: int) -> Category:
    """
    Ask Claude to categorize an expense by description and amount.
    Returns Category.OTHER on any failure (timeout, bad response, API error).
    """
    api_key = current_app.config.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        current_app.logger.warning("ANTHROPIC_API_KEY not set — skipping AI categorization")
        return Category.OTHER

    try:
        client = anthropic.Anthropic(api_key=api_key)
        amount_dollars = amount_cents / 100

        message = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=10,
            system=_SYSTEM_PROMPT,
            messages=[
                {
                    "role": "user",
                    "content": f'Description: "{description}" | Amount: ${amount_dollars:.2f}',
                }
            ],
        )
        raw = message.content[0].text.strip().upper()
        if raw in _VALID_CATEGORIES:
            return Category(raw)

        current_app.logger.warning(f"AI returned unknown category '{raw}' — defaulting to OTHER")
        return Category.OTHER

    except anthropic.APITimeoutError:
        current_app.logger.error("AI categorization timed out — defaulting to OTHER")
        return Category.OTHER
    except anthropic.APIError as exc:
        current_app.logger.error(f"AI API error: {exc} — defaulting to OTHER")
        return Category.OTHER
    except Exception as exc:
        current_app.logger.error(f"Unexpected AI error: {exc} — defaulting to OTHER")
        return Category.OTHER

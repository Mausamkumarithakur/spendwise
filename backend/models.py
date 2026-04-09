"""
Database models — single source of truth for schema.
Amounts are stored in CENTS (int) to avoid float precision bugs.
"""
from __future__ import annotations
import enum
from datetime import date as date_type
from typing import Optional
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(str, enum.Enum):
    FOOD = "FOOD"
    TRANSPORT = "TRANSPORT"
    HOUSING = "HOUSING"
    HEALTH = "HEALTH"
    ENTERTAINMENT = "ENTERTAINMENT"
    SHOPPING = "SHOPPING"
    UTILITIES = "UTILITIES"
    OTHER = "OTHER"


class Expense(db.Model):
    __tablename__ = "expenses"

    id: int = db.Column(db.Integer, primary_key=True)
    description: str = db.Column(db.String(255), nullable=False)
    amount_cents: int = db.Column(db.Integer, nullable=False)  # stored in cents
    category: str = db.Column(
        db.Enum(Category), nullable=False, default=Category.OTHER
    )
    date: date_type = db.Column(db.Date, nullable=False)
    note: Optional[str] = db.Column(db.String(500), nullable=True)
    ai_categorized: bool = db.Column(db.Boolean, default=False, nullable=False)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "description": self.description,
            "amount_cents": self.amount_cents,
            "amount": round(self.amount_cents / 100, 2),
            "category": self.category,
            "date": self.date.isoformat(),
            "note": self.note,
            "ai_categorized": self.ai_categorized,
        }

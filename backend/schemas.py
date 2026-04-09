"""
Request/response schemas using Pydantic.
All incoming data is validated here before reaching the service layer.
"""
from __future__ import annotations
from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator
from models import Category


class ExpenseCreate(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount: float = Field(..., gt=0)
    category: Optional[Category] = None
    date: date
    note: Optional[str] = Field(None, max_length=500)

    @field_validator("description")
    @classmethod
    def description_not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Description cannot be blank")
        return v.strip()

    @field_validator("note", mode="before")
    @classmethod
    def note_empty_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

    def amount_cents(self) -> int:
        return round(self.amount * 100)


class ExpenseUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[float] = Field(None, gt=0)
    category: Optional[Category] = None
    date: Optional[date] = None
    note: Optional[str] = Field(None, max_length=500)

    @field_validator("note", mode="before")
    @classmethod
    def note_empty_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

    @field_validator("category", mode="before")
    @classmethod
    def category_empty_to_none(cls, v):
        if v == "" or v is None:
            return None
        return v

    def amount_cents(self) -> Optional[int]:
        if self.amount is None:
            return None
        return round(self.amount * 100)


class AICategorizationRequest(BaseModel):
    description: str = Field(..., min_length=1, max_length=255)
    amount_cents: int = Field(..., gt=0)


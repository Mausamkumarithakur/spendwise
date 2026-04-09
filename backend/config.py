"""
Application configuration — all env access goes through this module.
Components import from here, never from os.environ directly.
"""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-change-in-prod")
    SQLALCHEMY_DATABASE_URI: str = os.environ.get(
        "DATABASE_URL", "sqlite:///expenses.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    ANTHROPIC_API_KEY: str = os.environ.get("ANTHROPIC_API_KEY", "")
    AI_TIMEOUT_SECONDS: int = 5


class TestConfig(Config):
    TESTING: bool = True
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///:memory:"
    ANTHROPIC_API_KEY: str = "test-key"

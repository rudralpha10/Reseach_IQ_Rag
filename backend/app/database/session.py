
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Project root
PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Load .env from project root
load_dotenv(PROJECT_ROOT / ".env")

# SQLite fallback
DEFAULT_DATABASE_PATH = (
    PROJECT_ROOT / "data" / "research_intelligence.db"
)

# Read database URL
DATABASE_URL = os.getenv("DATABASE_URL") or (
    f"sqlite:///{DEFAULT_DATABASE_PATH.as_posix()}"
)


def normalize_database_url(database_url: str) -> str:
    """Configure PostgreSQL to use psycopg 3."""

    if database_url.startswith("postgres://"):
        return database_url.replace(
            "postgres://",
            "postgresql+psycopg://",
            1,
        )

    if database_url.startswith("postgresql://"):
        return database_url.replace(
            "postgresql://",
            "postgresql+psycopg://",
            1,
        )

    return database_url


DATABASE_URL = normalize_database_url(DATABASE_URL)

# Connection settings
if DATABASE_URL.startswith("sqlite"):
    DEFAULT_DATABASE_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )
    connect_args = {"check_same_thread": False}
else:
    connect_args = {}


# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    pool_pre_ping=True,
)

# Create database sessions
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_session():
    return SessionLocal()

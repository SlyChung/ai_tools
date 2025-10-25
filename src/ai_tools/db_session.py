from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Read URL from env (you already have LIBRARY_DATABASE_URL in .env)
DATABASE_URL = os.getenv("LIBRARY_DATABASE_URL")

# Engine = database connection handle
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Session factory
SessionLocal = sessionmaker(
    bind=engine, autoflush=False, autocommit=False, future=True
)

# Dependency-style helper (handy for scripts/CLI)
def get_session():
    """Context-managed session for DB work"""
    with SessionLocal() as session:
        yield session

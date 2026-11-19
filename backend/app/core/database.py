import os
from typing import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.exc import OperationalError
from app.core.config import settings
import logging

logger = logging.getLogger("aethera.database")
logging.basicConfig(level=logging.INFO)

backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sqlite_default_path = os.path.join(backend_dir, "aethera.db").replace("\\", "/")

db_url = settings.DATABASE_URL
# Automatically normalize legacy postgres:// prefixes provided by Railway/Render
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+psycopg2://", 1)
elif db_url.startswith("postgresql://") and not db_url.startswith("postgresql+psycopg2://"):
    db_url = db_url.replace("postgresql://", "postgresql+psycopg2://", 1)

if db_url.startswith("sqlite:///./") or db_url == "sqlite:///aethera.db":
    db_url = f"sqlite:///{sqlite_default_path}"
is_sqlite = db_url.startswith("sqlite")
connect_args = {"check_same_thread": False} if is_sqlite else {}

try:
    engine = create_engine(
        db_url,
        connect_args=connect_args,
        pool_pre_ping=True
    )
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        if not is_sqlite:
            try:
                conn.execute(text("CREATE EXTENSION IF NOT EXISTS pg_trgm;"))
                conn.commit()
            except Exception as trgm_err:
                logger.warning(f"Note: pg_trgm extension creation: {trgm_err}")
    logger.info("Successfully connected to database.")
except OperationalError as e:
    if not is_sqlite:
        logger.warning(f"PostgreSQL connection failed: {e}. Falling back to SQLite for local development ease.")
        db_url = "sqlite:///./aethera.db"
        is_sqlite = True
        connect_args = {"check_same_thread": False}
        engine = create_engine(
            db_url,
            connect_args=connect_args,
            pool_pre_ping=True
        )
    else:
        raise e

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

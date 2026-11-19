import os
from typing import List, Optional
from pydantic import AnyHttpUrl, BeforeValidator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated
from dotenv import load_dotenv

# Resolve absolute paths to backend/.env and root .env
backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
root_dir = os.path.dirname(backend_dir)
env_path = os.path.join(backend_dir, ".env")
root_env_path = os.path.join(root_dir, ".env")

if os.path.exists(env_path):
    load_dotenv(dotenv_path=env_path)
elif os.path.exists(root_env_path):
    load_dotenv(dotenv_path=root_env_path)

def assemble_cors_origins(v: str | List[str]) -> List[str]:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    elif isinstance(v, (list, str)):
        return v
    raise ValueError(v)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    PROJECT_NAME: str = "Aethera AI"
    API_V1_STR: str = "/api/v1"
    
    # Database connection URL
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/aethera"
    
    # Redis cache configurations
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    REDIS_URL: Optional[str] = None
    
    # Active LLM provider ('groq' or 'gemini')
    LLM_PROVIDER: str = "groq"

    # Groq AI configuration
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "openai/gpt-oss-120b"

    # Gemini AI configuration
    GEMINI_API_KEY: Optional[str] = None
    GEMINI_MODEL: str = "gemini-3.8-flash"
    
    # CORS Origins (list of allowed hosts, e.g., http://localhost:3000)
    BACKEND_CORS_ORIGINS: Annotated[
        List[str] | str, BeforeValidator(assemble_cors_origins)
    ] = ["http://localhost:3000", "http://127.0.0.1:3000"]

settings = Settings()

def get_gemini_credentials() -> tuple[Optional[str], str]:
    """
    Dynamically re-reads environment / .env file on demand.
    This ensures that when a user adds or updates their GEMINI_API_KEY in .env,
    the active backend will immediately use the new key without requiring a server restart.
    """
    # Force reload from disk in case .env was modified after server startup
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)
    if os.path.exists(root_env_path):
        load_dotenv(dotenv_path=root_env_path, override=False)

    raw_key = os.environ.get("GEMINI_API_KEY") or settings.GEMINI_API_KEY
    clean_key: Optional[str] = None
    if raw_key:
        cleaned = raw_key.strip("'\" \t\r\n")
        if cleaned and not cleaned.startswith("YOUR_") and cleaned != "None":
            clean_key = cleaned

    raw_model = os.environ.get("GEMINI_MODEL") or settings.GEMINI_MODEL or "gemini-3.8-flash"
    clean_model = raw_model.strip("'\" \t\r\n")
    # Upgrade legacy or deprecated model references (1.x, 2.x, 3.1) to gemini-3.8-flash
    if not clean_model or any(legacy in clean_model for legacy in ["1.5", "2.0", "2.5", "3.1"]):
        clean_model = "gemini-3.8-flash"

    return clean_key, clean_model

def get_groq_credentials() -> tuple[Optional[str], str]:
    """
    Dynamically re-reads environment / .env file on demand for Groq credentials.
    Ensures updates to GROQ_API_KEY in .env take effect immediately without server restart.
    """
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)
    if os.path.exists(root_env_path):
        load_dotenv(dotenv_path=root_env_path, override=False)

    raw_key = os.environ.get("GROQ_API_KEY") or getattr(settings, "GROQ_API_KEY", None)
    clean_key: Optional[str] = None
    if raw_key:
        cleaned = raw_key.strip("'\" \t\r\n")
        if cleaned and not cleaned.startswith("YOUR_") and cleaned != "None":
            clean_key = cleaned

    raw_model = os.environ.get("GROQ_MODEL") or getattr(settings, "GROQ_MODEL", None) or "openai/gpt-oss-120b"
    clean_model = raw_model.strip("'\" \t\r\n")
    if not clean_model or "llama" in clean_model.lower():
        clean_model = "openai/gpt-oss-120b"

    return clean_key, clean_model

def get_active_provider() -> str:
    """
    Returns the active LLM provider ('groq' or 'gemini').
    Defaults to 'groq' if GROQ_API_KEY is present or LLM_PROVIDER is 'groq'.
    """
    if os.path.exists(env_path):
        load_dotenv(dotenv_path=env_path, override=True)
    if os.path.exists(root_env_path):
        load_dotenv(dotenv_path=root_env_path, override=False)

    explicit_provider = os.environ.get("LLM_PROVIDER") or getattr(settings, "LLM_PROVIDER", None)
    if explicit_provider:
        provider = explicit_provider.strip().lower()
        if provider in ["groq", "gemini"]:
            return provider

    # If not explicitly set, auto-detect based on configured keys
    groq_key, _ = get_groq_credentials()
    if groq_key:
        return "groq"
    gemini_key, _ = get_gemini_credentials()
    if gemini_key:
        return "gemini"

    return "groq"

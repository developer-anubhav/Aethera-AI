import logging
from app.ai.base_client import BaseLLMClient
from app.ai.groq_client import GroqClient
from app.ai.gemini_client import GeminiClient
from app.core.config import get_active_provider, get_groq_credentials, get_gemini_credentials

logger = logging.getLogger("aethera.llm_factory")

def get_llm_client() -> BaseLLMClient:
    """
    Unified LLM Client Factory.
    Selects the active client ('groq' or 'gemini') based on LLM_PROVIDER in .env.
    If no provider is explicitly chosen, intelligently prioritizes whichever key is present.
    """
    provider = get_active_provider()

    if provider == "groq":
        return GroqClient()
    elif provider == "gemini":
        return GeminiClient()

    # Intelligent auto-fallback
    groq_key, _ = get_groq_credentials()
    if groq_key:
        return GroqClient()

    gemini_key, _ = get_gemini_credentials()
    if gemini_key:
        return GeminiClient()

    # Default to GroqClient
    return GroqClient()

import asyncio
import logging
from typing import AsyncGenerator, List, Optional

try:
    from google import genai
    from google.genai import types
    from google.genai.errors import APIError
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False
    genai = None
    types = None
    APIError = Exception

from app.core.config import get_gemini_credentials
from app.ai.base_client import BaseLLMClient

logger = logging.getLogger("aethera.gemini")

# Standard modern models supported by Google AI Studio
FALLBACK_MODELS: List[str] = [
    "gemini-3.8-flash",
    "gemini-flash-latest",
    "gemini-4-hydrogen",
    "gemini-3.5-flash-lite"
]

class GeminiClient(BaseLLMClient):
    provider_name: str = "gemini"

    def __init__(self):
        # Dynamically load credentials to immediately reflect any changes in .env
        self.provider_name = "gemini"
        self.api_key, self.model_name = get_gemini_credentials()

        if not HAS_GENAI:
            logger.warning("google-genai package not installed; GeminiClient in fallback mode.")
            self.client_active = False
            self.client = None
            return

        if self.api_key:
            try:
                # Instantiate Google Gen AI Client with standard Google AI Studio configuration
                self.client = genai.Client(api_key=self.api_key)
                self.client_active = True
                logger.info(f"GeminiClient initialized successfully with model '{self.model_name}' (google-genai SDK).")
            except Exception as e:
                logger.error(f"Failed to initialize GenAI Client with provided key: {e}")
                self.client_active = False
                self.client = None
        else:
            logger.warning("GEMINI_API_KEY is not configured or uses a placeholder. Aera is running in Mock-Client mode.")
            self.client_active = False
            self.client = None

    def _get_candidate_models(self) -> List[str]:
        """Return the prioritized list of models to try."""
        # Ensure deprecated models are mapped to gemini-3.8-flash
        preferred = self.model_name
        if any(legacy in preferred for legacy in ["1.5", "2.0", "2.5", "3.1"]):
            preferred = "gemini-3.8-flash"

        candidates = [preferred]
        for m in FALLBACK_MODELS:
            if m not in candidates:
                candidates.append(m)
        return candidates

    def _format_error_message(self, error: Exception) -> str:
        """Format common Gemini API exceptions into clear, actionable messages."""
        err_str = str(error)
        err_lower = err_str.lower()
        if "api_key_invalid" in err_lower or "api key not valid" in err_lower:
            return "Invalid Gemini API Key. Please verify the API key in backend/.env copied from Google AI Studio (https://aistudio.google.com/)."
        if "quota" in err_lower or "resource_exhausted" in err_lower or "429" in err_str:
            return "Gemini API rate limit exceeded. Please wait a moment and try again or check your quota in Google AI Studio."
        if "permission_denied" in err_lower or "403" in err_str:
            return "Gemini API permission denied. Please verify that Generative Language API is enabled for your API key."
        return f"Gemini API request failed: {err_str}"

    async def generate_response(self, prompt: str, system_prompt: str) -> str:
        if not self.client_active or not self.client:
            return self._mock_response(prompt)

        models_to_try = self._get_candidate_models()
        last_exception = None

        for model in models_to_try:
            try:
                response = await self.client.aio.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )
                text = response.text or ""
                if text:
                    return text
            except APIError as e:
                last_exception = e
                # If 404 Not Found (e.g. invalid model name), try the next model
                if getattr(e, "code", None) == 404 or "not found" in str(e).lower():
                    logger.warning(f"Model '{model}' not found in Gemini API. Falling back to alternative model...")
                    continue
                # For auth or permissions, stop and raise immediately
                logger.error(f"Gemini API client error with model '{model}': {e}")
                raise RuntimeError(self._format_error_message(e)) from e
            except Exception as e:
                last_exception = e
                logger.error(f"Gemini API unexpected error with model '{model}': {e}")
                continue

        if last_exception:
            raise RuntimeError(self._format_error_message(last_exception)) from last_exception
        return ""

    async def stream_response(self, prompt: str, system_prompt: str) -> AsyncGenerator[str, None]:
        if not self.client_active or not self.client:
            mock_text = self._mock_response(prompt)
            for chunk in mock_text.split(" "):
                yield chunk + " "
                await asyncio.sleep(0.04)
            return

        models_to_try = self._get_candidate_models()
        streamed_any = False
        last_exception = None

        for model in models_to_try:
            try:
                response = await self.client.aio.models.generate_content_stream(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )
                async for chunk in response:
                    text = chunk.text
                    if text:
                        streamed_any = True
                        yield text
                
                # If generation streamed successfully, we are done
                if streamed_any:
                    return

            except APIError as e:
                last_exception = e
                if not streamed_any and (getattr(e, "code", None) == 404 or "not found" in str(e).lower()):
                    logger.warning(f"Model '{model}' streaming not available. Falling back to alternative model...")
                    continue
                logger.error(f"Gemini API streaming error with model '{model}': {e}")
                raise RuntimeError(self._format_error_message(e)) from e
            except Exception as e:
                last_exception = e
                if not streamed_any:
                    logger.warning(f"Streaming error on model '{model}': {e}. Attempting next model...")
                    continue
                raise RuntimeError(self._format_error_message(e)) from e

        # If streaming didn't produce chunks, attempt a non-streaming fallback
        if not streamed_any:
            logger.info("Streaming yielded no tokens; attempting single generate_response fallback...")
            try:
                full_text = await self.generate_response(prompt, system_prompt)
                if full_text:
                    yield full_text
                    return
            except Exception as fallback_e:
                logger.error(f"Gemini API fallback execution failed: {fallback_e}")
                raise fallback_e

        if last_exception and not streamed_any:
            raise RuntimeError(self._format_error_message(last_exception)) from last_exception

    def _mock_response(self, prompt: str) -> str:
        return (
            "**[Aera System Notice: Gemini API Key Needed]**\n\n"
            "This simulated scientific summary was generated locally because no valid `GEMINI_API_KEY` was detected in `backend/.env`.\n\n"
            "**To enable live Gemini AI responses:**\n"
            "1. Copy your API key from [Google AI Studio](https://aistudio.google.com/).\n"
            "2. Open `backend/.env` and paste it on line 4: `GEMINI_API_KEY=AIzaSy...`\n"
            "3. Save the file and send your question again — Aera will automatically connect and stream live answers!"
        )

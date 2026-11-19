import asyncio
import logging
from typing import AsyncGenerator, List, Optional
from groq import AsyncGroq, APIError, AuthenticationError, RateLimitError

from app.core.config import get_groq_credentials
from app.ai.base_client import BaseLLMClient

logger = logging.getLogger("aethera.groq")

# Modern reliable models active on Groq
GROQ_FALLBACK_MODELS: List[str] = [
    "openai/gpt-oss-120b",
    "qwen/qwen3.8-27b",
    "openai/gpt-oss-20b"
]

class GroqClient(BaseLLMClient):
    provider_name: str = "groq"

    def __init__(self):
        # Dynamically reload credentials to instantly reflect changes in .env
        self.provider_name = "groq"
        self.api_key, self.model_name = get_groq_credentials()

        if self.api_key:
            try:
                self.client = AsyncGroq(api_key=self.api_key)
                self.client_active = True
                logger.info(f"GroqClient initialized successfully with model '{self.model_name}'.")
            except Exception as e:
                logger.error(f"Failed to initialize Groq client: {e}")
                self.client_active = False
                self.client = None
        else:
            logger.warning("GROQ_API_KEY is not configured or uses a placeholder. Running in Mock mode.")
            self.client_active = False
            self.client = None

    def _get_candidate_models(self) -> List[str]:
        candidates = [self.model_name]
        for m in GROQ_FALLBACK_MODELS:
            if m not in candidates:
                candidates.append(m)
        return candidates

    def _format_error_message(self, error: Exception) -> str:
        err_str = str(error)
        err_lower = err_str.lower()
        if isinstance(error, AuthenticationError) or "invalid api key" in err_lower or "401" in err_str:
            return "Invalid Groq API Key. Please verify the key in backend/.env copied from https://console.groq.com/keys."
        if isinstance(error, RateLimitError) or "rate limit" in err_lower or "429" in err_str:
            return "Groq rate limit reached for this model. Falling back or please retry in a moment."
        return f"Groq request failed: {err_str}"

    async def generate_response(self, prompt: str, system_prompt: str) -> str:
        if not self.client_active or not self.client:
            return self._mock_response(prompt)

        models_to_try = self._get_candidate_models()
        last_exception = None

        for model in models_to_try:
            try:
                completion = await self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    stream=False
                )
                if completion.choices and completion.choices[0].message.content:
                    return completion.choices[0].message.content
            except AuthenticationError as auth_err:
                logger.error(f"Groq authentication error: {auth_err}")
                raise RuntimeError(self._format_error_message(auth_err)) from auth_err
            except (RateLimitError, APIError) as api_err:
                last_exception = api_err
                logger.warning(f"Groq model '{model}' encountered issue: {api_err}. Trying fallback...")
                continue
            except Exception as e:
                last_exception = e
                logger.error(f"Unexpected error with Groq model '{model}': {e}")
                continue

        if last_exception:
            raise RuntimeError(self._format_error_message(last_exception)) from last_exception
        return ""

    async def stream_response(self, prompt: str, system_prompt: str) -> AsyncGenerator[str, None]:
        if not self.client_active or not self.client:
            mock_text = self._mock_response(prompt)
            for chunk in mock_text.split(" "):
                yield chunk + " "
                await asyncio.sleep(0.02)
            return

        models_to_try = self._get_candidate_models()
        streamed_any = False
        last_exception = None

        for model in models_to_try:
            try:
                stream = await self.client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.3,
                    stream=True
                )
                async for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        streamed_any = True
                        yield chunk.choices[0].delta.content

                if streamed_any:
                    return

            except AuthenticationError as auth_err:
                logger.error(f"Groq authentication error: {auth_err}")
                raise RuntimeError(self._format_error_message(auth_err)) from auth_err
            except (RateLimitError, APIError) as api_err:
                last_exception = api_err
                if not streamed_any:
                    logger.warning(f"Groq model '{model}' stream failed: {api_err}. Trying alternative model...")
                    continue
                raise RuntimeError(self._format_error_message(api_err)) from api_err
            except Exception as e:
                last_exception = e
                if not streamed_any:
                    logger.warning(f"Groq unexpected stream error on '{model}': {e}. Trying fallback...")
                    continue
                raise RuntimeError(self._format_error_message(e)) from e

        if not streamed_any:
            logger.info("Groq stream yielded no chunks; trying non-streaming fallback...")
            try:
                full_text = await self.generate_response(prompt, system_prompt)
                if full_text:
                    yield full_text
                    return
            except Exception as fallback_err:
                raise fallback_err

        if last_exception and not streamed_any:
            raise RuntimeError(self._format_error_message(last_exception)) from last_exception

    def _mock_response(self, prompt: str) -> str:
        return (
            "**[Aera System Notice: Groq API Key Needed]**\n\n"
            "This simulated scientific response was generated locally because no valid `GROQ_API_KEY` was detected in `backend/.env`.\n\n"
            "**To enable ultra-fast, live Llama 3.3 responses on Groq:**\n"
            "1. Create a free API key at **[console.groq.com/keys](https://console.groq.com/keys)** (instant signup, no credit card needed).\n"
            "2. Open `backend/.env` and paste it into line 8: `GROQ_API_KEY=gsk_...`\n"
            "3. Save the file and send your question again — Aera will stream responses at 500+ tokens/sec!"
        )

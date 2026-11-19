from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseLLMClient(ABC):
    provider_name: str = "base"
    model_name: str = "default"

    @abstractmethod
    async def generate_response(self, prompt: str, system_prompt: str) -> str:
        """
        Generate a complete text response based on a prompt and system prompt.
        """
        pass

    @abstractmethod
    async def stream_response(self, prompt: str, system_prompt: str) -> AsyncGenerator[str, None]:
        """
        Stream back response tokens in real-time.
        """
        pass

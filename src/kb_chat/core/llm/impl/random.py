import asyncio
import random
import string

from kb_chat.core.llm.abc import LLMClient, LLMError
from kb_chat.domain.models import LLMRequest, LLMResponse


class RandomLLMClient(LLMClient):
    def __init__(self, model: str, fail_rate: float = 0.0) -> None:
        self.__model = model
        self.__fail_rate = fail_rate

    async def generate(self, request: LLMRequest) -> LLMResponse:
        await asyncio.sleep(2.0)

        if random.random() < self.__fail_rate:
            raise LLMError("Simulated LLM failure")

        response = self.__generate_random_string()
        return LLMResponse(
            content=response,
            model=request.model,
            prompt_tokens=len(request.prompt.split()) + len(request.system_prompt.split()),
            completion_tokens=len(response),
        )

    @property
    def model(self) -> str:
        return self.__model

    def __generate_random_string(self, length: int = 32) -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=length))

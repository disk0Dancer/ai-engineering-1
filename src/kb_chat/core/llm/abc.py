import abc

from kb_chat.domain.models import LLMRequest, LLMResponse


class LLMError(Exception):
    pass


class LLMClient(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def generate(self, request: LLMRequest) -> LLMResponse:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def model(self) -> str:
        raise NotImplementedError

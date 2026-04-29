import abc

from kb_chat.domain.models import ChatResult


class ChatServiceError(Exception):
    pass


class ChatService(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def chat(
        self,
        question: str,
        topic: str,
        temperature: float | None = None,
    ) -> ChatResult:
        raise NotImplementedError

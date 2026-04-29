import abc
import typing as t

from kb_chat.domain.models import TopicContent


class KnowledgeBaseError(Exception):
    pass


class KnowledgeBase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get_topic_content(self, topic: str) -> TopicContent | None:
        raise NotImplementedError

    @abc.abstractmethod
    async def list_topics(self) -> t.Sequence[str]:
        raise NotImplementedError

    @abc.abstractmethod
    async def update_topic(self, topic: str, content: str) -> TopicContent:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_topic_version(self, topic: str) -> int | None:
        raise NotImplementedError

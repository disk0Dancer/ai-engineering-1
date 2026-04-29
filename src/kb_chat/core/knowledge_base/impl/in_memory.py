import typing as t
from datetime import datetime

from kb_chat.core.knowledge_base.abc import KnowledgeBase
from kb_chat.core.knowledge_base.impl.topics import DEFAULT_TOPICS
from kb_chat.domain.models import TopicContent


class InMemoryKnowledgeBase(KnowledgeBase):
    def __init__(self, initial_topics: t.Mapping[str, TopicContent] | None = None) -> None:
        self.__topics: t.MutableMapping[str, TopicContent] = (
            dict(initial_topics) if initial_topics else dict(DEFAULT_TOPICS)
        )

    async def get_topic_content(self, topic: str) -> TopicContent | None:
        return self.__topics.get(topic)

    async def list_topics(self) -> t.Sequence[str]:
        return list(self.__topics.keys())

    async def update_topic(self, topic: str, content: str) -> TopicContent:
        existing = self.__topics.get(topic)
        new_version = (existing.version + 1) if existing else 1

        self.__topics[topic] = TopicContent(
            topic=topic,
            content=content,
            version=new_version,
            updated_at=datetime.now(),
        )
        return self.__topics[topic]

    async def get_topic_version(self, topic: str) -> int | None:
        topic_content = self.__topics.get(topic)
        return topic_content.version if topic_content else None

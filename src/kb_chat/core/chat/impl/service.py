import logging
import textwrap
import hashlib

from kb_chat.core.chat.abc import ChatService, ChatServiceError
from kb_chat.core.knowledge_base.abc import KnowledgeBase
from kb_chat.core.llm.abc import LLMClient
from kb_chat.domain.models import ChatResult, LLMRequest, TopicContent
from kb_chat.core.cache.abc import CacheStorage

logger = logging.getLogger(__name__)


class KnowledgeBaseChatService(ChatService):
    """
    Chat service that uses knowledge base content to answer questions.
    """

    def __init__(
        self,
        knowledge_base: KnowledgeBase,
        llm_client: LLMClient,
        cache: CacheStorage,
        default_temperature: float = 0.7,
    ) -> None:
        self.__knowledge_base = knowledge_base
        self.__llm_client = llm_client
        self.__default_temperature = default_temperature
        self.__cache = cache

    def _make_cache_key(self, prompt: str, system_prompt: str, model: str) -> str:
        data = f"{prompt}:{system_prompt}:{model}"
        return hashlib.sha256(data.encode()).hexdigest()


    async def chat(
        self,
        question: str,
        topic: str,
        temperature: float | None = None,
    ) -> ChatResult:
        topic_content = await self.__knowledge_base.get_topic_content(topic)
        if topic_content is None:
            raise ChatServiceError(f"Topic '{topic}' not found")

        system_prompt = self.__build_system_prompt(topic_content)
        effective_temperature = temperature if temperature is not None else self.__default_temperature

        key = self._make_cache_key(question,system_prompt,self.__llm_client.model)
        cached = await self.__cache.get(key)
        if cached:
            return ChatResult(
            answer=cached,
            topic=topic,
            model=self.__llm_client.model,
            cached=True,
        )

        request = LLMRequest(
            prompt=question,
            system_prompt=system_prompt,
            model=self.__llm_client.model,
            temperature=effective_temperature,
        )

        response = await self.__llm_client.generate(request)

        await self.__cache.set(key,response.content)
        await self.__cache.map_topic_to_keys(topic, key)

        return ChatResult(
            answer=response.content,
            topic=topic,
            model=response.model,
            cached=False,
        )

    @property
    def llm_client(self) -> LLMClient:
        return self.__llm_client

    @property
    def knowledge_base(self) -> KnowledgeBase:
        return self.__knowledge_base

    def __build_system_prompt(self, topic_content: TopicContent) -> str:
        return textwrap.dedent(f"""\
            You are a helpful assistant for bank employees.
            Answer questions based on the following knowledge base content.
            Be concise and accurate. If you don't know the answer, say so.

            Knowledge Base Content:
            {topic_content.content}

            Always be professional and helpful.""")

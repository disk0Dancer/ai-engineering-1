import pytest

from kb_chat.core.chat.abc import ChatServiceError
from kb_chat.core.chat.impl.service import KnowledgeBaseChatService
from kb_chat.core.knowledge_base.impl.in_memory import InMemoryKnowledgeBase
from kb_chat.core.llm.impl.random import RandomLLMClient
from kb_chat.domain.models import TopicContent


class TestKnowledgeBaseChatService:
    @pytest.fixture
    def knowledge_base(self) -> InMemoryKnowledgeBase:
        topics = {
            "vacation": TopicContent(topic="vacation", content="Employees get 28 days of vacation."),
            "sick_leave": TopicContent(topic="sick_leave", content="First 3 days require self-certification."),
        }
        return InMemoryKnowledgeBase(initial_topics=topics)

    @pytest.fixture
    def llm_client(self) -> RandomLLMClient:
        return RandomLLMClient(model="test-model")

    @pytest.fixture
    def chat_service(
        self,
        knowledge_base: InMemoryKnowledgeBase,
        llm_client: RandomLLMClient,
    ) -> KnowledgeBaseChatService:
        return KnowledgeBaseChatService(
            knowledge_base=knowledge_base,
            llm_client=llm_client,
            default_temperature=0.7,
        )

    @pytest.mark.asyncio
    async def test_chat_success(self, chat_service: KnowledgeBaseChatService) -> None:
        result = await chat_service.chat(
            question="How many vacation days?",
            topic="vacation",
        )

        assert result.topic == "vacation"
        assert len(result.answer) > 0
        assert result.cached is False

    @pytest.mark.asyncio
    async def test_chat_topic_not_found(self, chat_service: KnowledgeBaseChatService) -> None:
        with pytest.raises(ChatServiceError, match="not found"):
            await chat_service.chat(
                question="Question",
                topic="nonexistent",
            )

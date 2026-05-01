import typing as t
from contextlib import asynccontextmanager

import pytest
import redis.asyncio as redis
from httpx import ASGITransport, AsyncClient

from kb_chat import initialize_service
from kb_chat.configuration import Configuration
from kb_chat.core.chat.impl.service import KnowledgeBaseChatService
from kb_chat.core.knowledge_base.impl.in_memory import InMemoryKnowledgeBase
from kb_chat.core.llm.impl.random import RandomLLMClient


@pytest.fixture
def configuration() -> Configuration:
    return Configuration()


@asynccontextmanager
async def setup_app_state(app: t.Any, configuration: Configuration) -> t.AsyncGenerator[None, None]:
    knowledge_base = InMemoryKnowledgeBase()
    llm_client = RandomLLMClient(model=configuration.llm.model)
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    await redis_client.flushdb()
    chat_service = KnowledgeBaseChatService(
        knowledge_base=knowledge_base,
        llm_client=llm_client,
        default_temperature=configuration.llm.temperature,
        redis_client=redis_client,
    )

    app.state.knowledge_base = knowledge_base
    app.state.llm_client = llm_client
    app.state.chat_service = chat_service
    app.state.redis = redis_client

    yield

    await redis_client.aclose()


@pytest.fixture
async def async_client(configuration: Configuration) -> t.AsyncGenerator[AsyncClient, None]:
    app = initialize_service(configuration)

    async with (
        setup_app_state(app, configuration),
        AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
        ) as client,
    ):
        yield client

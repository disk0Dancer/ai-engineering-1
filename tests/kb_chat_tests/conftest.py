import typing as t
from contextlib import asynccontextmanager
import redis.asyncio

import pytest
from httpx import ASGITransport, AsyncClient

from kb_chat import initialize_service
from kb_chat.configuration import Configuration
from kb_chat.core.chat.impl.service import KnowledgeBaseChatService
from kb_chat.core.knowledge_base.impl.in_memory import InMemoryKnowledgeBase
from kb_chat.core.llm.impl.random import RandomLLMClient
from kb_chat.core.cache.impl.redis import RedisCacheStorage

@pytest.fixture
def configuration() -> Configuration:
    return Configuration()


@asynccontextmanager
async def setup_app_state(app: t.Any, configuration: Configuration) -> t.AsyncGenerator[None, None]:
    knowledge_base = InMemoryKnowledgeBase()
    llm_client = RandomLLMClient(model=configuration.llm.model)

    redis_client = redis.asyncio.Redis(host="localhost", port=6379, decode_responses=True)
    cache_storage = RedisCacheStorage(redis_client)

    chat_service = KnowledgeBaseChatService(
        knowledge_base=knowledge_base,
        llm_client=llm_client,
        cache = cache_storage,
        default_temperature=configuration.llm.temperature,
    )

    app.state.knowledge_base = knowledge_base
    app.state.llm_client = llm_client
    app.state.chat_service = chat_service
    app.state.cache = cache_storage 

    yield

@pytest.fixture
async def cache_storage():
    client = redis.asyncio.from_url(host="localhost", port=6379, decode_responses=True)
    storage = RedisCacheStorage(client)
    yield storage
    await client.aclose()

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


@pytest.fixture(autouse=True)
async def clear_redis_cache():
    """Очищать Redis перед каждым тестом."""
    client = redis.asyncio.from_url("redis://localhost", decode_responses=True)
    await client.flushdb()
    await client.aclose()
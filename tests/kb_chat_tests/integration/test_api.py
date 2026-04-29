import dataclasses as dc
import typing as t

import pytest
from httpx import AsyncClient


@dc.dataclass(frozen=True)
class ChatScenario:
    @dc.dataclass(frozen=True)
    class Input:
        question: str
        topic: str
        temperature: float | None = None

    @dc.dataclass(frozen=True)
    class Output:
        status_code: int
        has_answer: bool = True

    input_: Input
    expected_output: Output


@pytest.fixture(
    params=[
        pytest.param(
            ChatScenario(
                input_=ChatScenario.Input(
                    question="How many vacation days do I get?",
                    topic="vacation",
                ),
                expected_output=ChatScenario.Output(
                    status_code=200,
                    has_answer=True,
                ),
            ),
            id="success",
        ),
        pytest.param(
            ChatScenario(
                input_=ChatScenario.Input(
                    question="What is the meaning of life?",
                    topic="philosophy",
                ),
                expected_output=ChatScenario.Output(
                    status_code=404,
                    has_answer=False,
                ),
            ),
            id="unknown_topic",
        ),
        pytest.param(
            ChatScenario(
                input_=ChatScenario.Input(
                    question="Can I carry over vacation days?",
                    topic="vacation",
                    temperature=0.5,
                ),
                expected_output=ChatScenario.Output(
                    status_code=200,
                    has_answer=True,
                ),
            ),
            id="with_temperature",
        ),
    ]
)
def chat_scenario(request: pytest.FixtureRequest) -> ChatScenario:
    return request.param


class TestTopicsEndpoint:
    @pytest.mark.asyncio
    async def test_list_topics(self, async_client: AsyncClient) -> None:
        response = await async_client.get("/api/v1/topics")

        assert response.status_code == 200
        data = response.json()
        assert "topics" in data
        assert "vacation" in data["topics"]
        assert "sick_leave" in data["topics"]


class TestChatEndpoint:
    @pytest.mark.asyncio
    async def test_chat(self, async_client: AsyncClient, chat_scenario: ChatScenario) -> None:
        request_body: t.MutableMapping[str, t.Any] = {
            "question": chat_scenario.input_.question,
            "topic": chat_scenario.input_.topic,
        }
        if chat_scenario.input_.temperature is not None:
            request_body["temperature"] = chat_scenario.input_.temperature

        response = await async_client.post("/api/v1/chat", json=request_body)

        assert response.status_code == chat_scenario.expected_output.status_code

        if chat_scenario.expected_output.has_answer:
            data = response.json()
            assert "answer" in data
            assert data["topic"] == chat_scenario.input_.topic

    @pytest.mark.asyncio
    async def test_chat_returns_cached_response_for_identical_request(self, async_client: AsyncClient) -> None:
        request_body = {
            "question": "How many vacation days do I get?",
            "topic": "vacation",
        }

        first_response = await async_client.post("/api/v1/chat", json=request_body)
        second_response = await async_client.post("/api/v1/chat", json=request_body)

        assert first_response.status_code == 200
        assert second_response.status_code == 200

        first_data = first_response.json()
        second_data = second_response.json()

        assert first_data["cached"] is False
        assert second_data["cached"] is True
        assert second_data["answer"] == first_data["answer"]

    @pytest.mark.asyncio
    async def test_cache_invalidate_topic_endpoint_exists(self, async_client: AsyncClient) -> None:
        response = await async_client.post("/api/v1/cache/invalidate/vacation")

        assert response.status_code in {200, 204}

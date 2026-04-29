from datetime import datetime

import pydantic
from pydantic import Field


class TopicContent(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    topic: str
    content: str
    version: int = Field(default=1, ge=1)
    updated_at: datetime = Field(default_factory=datetime.now)


class LLMRequest(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    prompt: str
    system_prompt: str
    model: str
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class LLMResponse(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    content: str
    model: str
    prompt_tokens: int = Field(ge=0)
    completion_tokens: int = Field(ge=0)


class ChatResult(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    answer: str
    topic: str
    model: str
    cached: bool = Field(default=False)

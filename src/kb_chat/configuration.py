import pydantic
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class LLMConfig(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    model: str = Field(default="gemma-2b")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)


class CacheConfig(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(extra="forbid")

    ttl_seconds: int = Field(default=300, ge=1)
    redis_url: str = Field(default="redis://localhost:6379")


class Configuration(BaseSettings):
    model_config = SettingsConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
    )

    app_name: str = Field(default="Knowledge Base Chat")
    log_level: str = Field(default="INFO")
    debug: bool = Field(default=False)

    llm: LLMConfig = Field(default_factory=LLMConfig)
    cache: CacheConfig = Field(default_factory=CacheConfig)

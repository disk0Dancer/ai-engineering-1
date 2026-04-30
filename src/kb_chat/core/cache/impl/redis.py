import redis.asyncio as aioredis
from  kb_chat.core.cache.abc import  CacheStorage

class RedisCacheStorage(CacheStorage):
    """Реализация кэша на Redis."""
    
    def __init__(self, redis_client: aioredis.Redis, ttl: int = 300):
        self._redis = redis_client
        self._ttl = ttl
        self._prefix = "llm_cache:"
        self._topic_prefix = "topic_keys:"
    
    async def get(self, key: str) -> str | None:
        return await self._redis.get(f"{self._prefix}{key}")
    
    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        await self._redis.setex(f"{self._prefix}{key}", ttl, value)

    async def map_topic_to_keys(self, topic: str, key: str) -> None:
        await self._redis.sadd(f"topic_keys:{topic}", key)
        
    async def invalidate_topic(self, topic: str) -> None:
        topic_key = f"{self._topic_prefix}{topic}"
        keys = await self._redis.smembers(topic_key)
    
        for key in keys:
            await self._redis.delete(f"{self._prefix}{key}")
        
        await self._redis.delete(topic_key)
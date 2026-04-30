import abc

class CacheStorage(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    async def get(self, key: str) -> str | None: 
        raise NotImplementedError

    
    @abc.abstractmethod
    async def set(self, key: str, value: str, ttl: int = 300) -> None:
        raise NotImplementedError


    @abc.abstractmethod
    async def map_topic_to_keys(self, topic: str, key: str) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def invalidate_topic(self, topic: str) -> None:
        raise NotImplementedError

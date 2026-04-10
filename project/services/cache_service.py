import json
import redis.asyncio as redis
from typing import Any



class CacheService:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    
    async def get(self, key: str) -> Any:
        """
            Fetch a value from cache.
            Returns the deserialized Python object, or None if not found / expired.
        """
        value = await self.redis.get(key)
        if value is None:
            return None
        
        return json.loads(value)
    

    async def set(self, key: str, value: Any, ttl_seconds: int = 300) -> None:
        """
            Store a value in cache with a TTL (time-to-live).
            After ttl_seconds, Redis automatically deletes the key.
            Default 5 minutes — tune per use case:
            - LLM responses: 3600 (1 hour) — expensive to regenerate
            - User profile: 300 (5 min) — changes occasionally  
            - Stock prices: 10 (10 sec) — changes constantly
        """

        await self.redis.setex(
            name=key,
            time=ttl_seconds,
            value=json.dumps(value, default=str)
        )


    async def delete(self, key: str) -> None:
            """Invalidate a cache entry — call this on update/delete operations."""
            await self.redis.delete(key)

    async def delete_pattern(self, pattern: str) -> None:
        """
            Delete all keys matching a pattern.
            Example: delete_pattern("user:*") clears all user cache entries.
            Use carefully — KEYS command scans entire Redis DB.
        """

        keys = await self.redis.keys(pattern)

        if keys:
            await self.redis.delete(*keys)

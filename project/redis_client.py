

import redis.asyncio as redis
from config import get_settings


settings = get_settings()

pool = redis.ConnectionPool.from_url(
        settings.REDIS_URL,
        max_connections=20,
        decode_responses=True
    )


def get_redis() -> redis.Redis:
    """
        Dependency function for FastAPI — exactly like get_db.
        Returns a Redis client using the shared connection pool.
        Unlike DB sessions, Redis clients are stateless so no yield/cleanup needed.
    """
    return redis.Redis(connection_pool=pool)


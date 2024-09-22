from typing import AsyncGenerator

from redis.asyncio import Redis

from config import settings


async def get_redis_instance() -> AsyncGenerator:
    connection = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)
    try:
        yield connection
    finally:
        await connection.close()

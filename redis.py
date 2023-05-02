import aioredis
from aioredis import Redis
from config import REDIS_URL
# async def get_async_redis() -> Redis:
#
#     async with aioredis.Redis.from_url(
#         REDIS_URL, max_connections=10
#     ) as redis:
#         yield redis

redis =  aioredis.Redis.from_url(
        REDIS_URL, max_connections=10
    )
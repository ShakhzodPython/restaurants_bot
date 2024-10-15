import redis.asyncio as aioredis

from config.settings import REDIS_HOST, REDIS_PORT, REDIS_DB


async def get_redis_connection():
    redis_url = f"redis://{REDIS_HOST}:{REDIS_PORT}"
    return await aioredis.from_url(url=redis_url,
                                   encoding="utf-8",
                                   decode_responses=True,
                                   # password=REDIS_PASSWORD,
                                   db=int(REDIS_DB))


async def close_redis_connection():
    redis = None
    if redis:
        redis = await get_redis_connection()
        redis.close()
        await redis.wait_close()

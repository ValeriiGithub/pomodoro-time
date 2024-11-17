import redis


def get_redis_connection() -> redis.Redis:
    return redis.Redis(
        host="localhost",
        port=6379,
        db=0,
    )

# def set_pomodoro_count(key, value):
#     redis_connection = get_redis_connection()
#     # redis_connection.set("pomodoro_count", value, ex=10)
#     redis_connection.set(key, value, ex=5)
#
#
#
# if __name__ == "__main__":
#     for i in range(10):
#         set_pomodoro_count(i, i**2)

# Павук Марсель

# from typing import AsyncGenerator
#
# import redis.asyncio as redis
#
# from settings import (
#     REDIS_HOST,
#     REDIS_PORT,
# )
#
#
# async def get_cache_session() -> AsyncGenerator[redis.Redis, None]:
#     cache_session = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
#     try:
#         yield cache_session
#     finally:
#         await cache_session.aclose()

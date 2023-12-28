import redis


class RedisClient:
    client = None

    @classmethod
    async def get_instance(cls):
        if cls.client is None:
            cls.client = redis.Redis(
                host="localhost", port=6379, db=0, decode_responses=True
            )
        return cls.client


async def get_redis_client():
    return await RedisClient.get_instance()

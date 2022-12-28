import json

import aioredis
import asyncio
from settings import settings


class RedisPool:

    def __init__(self, redis_url):
        self.redis_url = redis_url
        self._pool = None
        self._heartbeat_task = None

    async def set(self, key, value, expire: int = None):
        if type(value) is not str:
            value = json.dumps(value)
        await self._pool.set(key, value, expire=expire)

    async def get(self, key, default=None):
        value = await self._pool.get(key)
        if value is None:
            return default or None
        value = value.decode("utf-8")

        try:
            value = json.loads(value)
        except:
            pass
        return value

    async def connect(self):
        self._pool = await aioredis.create_redis_pool(self.redis_url)
        self._heartbeat_task = asyncio.create_task(self.heartbeat())

    async def disconnect(self):
        self._heartbeat_task.done()
        self._pool.close()
        await self._pool.wait_closed()

    async def heartbeat(self):
        """
        Проверка статуса закрытия каналов pubsub, т.е. грубо говоря сборка мусора :facepalm:

        Раз в минуту
        """
        heartbeat_sleep = 60

        while True:
            try:
                for pubsub_key in await self._pool.pubsub_channels('*'):
                    result = await self._pool.get(pubsub_key)
                    if result is None:
                        await self._pool.unsubscribe(pubsub_key)
                        await self._pool.execute('unsubscribe', pubsub_key)
            except BaseException as e:
                print(e)

            await asyncio.sleep(heartbeat_sleep)


redis = RedisPool(settings.redis_url)

import redis

from config import *


# REDIS_HOST = "192.168.99.254"
# REDIS_PORT = "56379"
# REDIS_PASSWORD = "123456"


class Redis:
    def __init__(self, host: str = REDIS_HOST, port: int = REDIS_PORT, passwd: str = REDIS_PASSWORD):
        try:
            self.redis = redis.Redis(host=host, port=port, decode_responses=True)
            self.redis.auth(passwd)
            self.redis.config_set("requirepass", passwd)
        except Exception as e:
            print("Redis Password Error")
            print(e)
            return

    def set(self, key: str, value: str):
        # self._live_connect()
        self.redis.set(key, value)

    def get(self, key: str):
        # self._live_connect()
        return self.redis.get(key)

    def expire(self, key: str, time: int):
        self.redis.expire(key, time)

    def select(self, dbnum: int):
        for i in range(3):
            try:
                self.redis.select(dbnum)
                break
            except redis.exceptions.AuthenticationError:
                self.live_connect()
                continue



    def del_(self, key):
        if key is not None:
            self.redis.delete(key)

    def sadd(self, key: str, value: str):
        self.redis.sadd(key, value)

    def smembers(self, key: str):
        return self.redis.smembers(key)

    def sismember(self, key: str, value: str):
        return self.redis.sismember(key, value)

    def srem(self, key: str):
        self.redis.srem(key)

    def zadd(self, key: str, value: str, score: int = 1):
        self.redis.zadd(key, {value: score})

    def zrange(self, key: str, min: int = 0, max: int = -1):
        return self.redis.zrange(key, min, max)

    def zcard(self, key):
        self.redis.zcard(key)

    def zrem(self, key: str):
        self.redis.zrem(key)

    def keys(self, k):
        # type is list
        return self.redis.keys(k)

    def close(self):
        return self.close()

    def live_connect(self, host: str = REDIS_HOST, port: int = REDIS_PORT, passwd: str = REDIS_PASSWORD):
        try:
            self.redis = redis.Redis(host=host, port=port, decode_responses=True)
            self.redis.auth(passwd)
            self.redis.config_set("requirepass", passwd)
        except Exception as e:
            print("Redis Password Error")
            print(e)
            return

# def make_token(length=10):
#     string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
#     return ''.join(random.choice(string) for _ in range(length))


# if __name__ == '__main__':
#     REDIS = Redis()
#     REDIS.select(15)
#     # REDIS.set("test", "tese")
#     # REDIS.expire("test", 10)
#     # # REDIS.set("testaa", "tese")
#     # REDIS.del_("testaa")
#     # print(REDIS.keys("*"))
#     # print(REDIS.get("asbdjyh"))
#     import random
#
#     # for i in range(5, 10):
#     #     k = str(i) + (make_token(5))
#     #     print(k)
#     #     REDIS.zadd("myzset", str(k), score=i)
#     print(REDIS.zrange("myzset"))
#     print(REDIS.zrange("myzset", 2, 2))
#     print(type(REDIS.zrange("myzset")))

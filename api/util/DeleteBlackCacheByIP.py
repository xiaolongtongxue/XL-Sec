from dao import REDIS

from config import LUA_BLACK_RULES


def del_cache_by_ip(ip: str):
    redis = REDIS()
    redis.select(LUA_BLACK_RULES)
    redis.del_('auto-ips:banned:' + ip)
    # ifkeys = len(redis.redis.keys("auto-ips:banned:*"))
    # for i in range(ifkeys):

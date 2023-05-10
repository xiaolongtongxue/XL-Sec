from dao import REDIS

import redis

from config import SESSION_DB_NUM, LOGIN_LIMIT, TOKEN_DB_NUM
from util.Get_IP import get_ip_p as get_ip
from util.Get_IP import get_ip as ip
from util.GetSalt import make_token

'''
基于IP设计的自定义session
为了提高设备的可拓展性，并且避免了flask的默认session存在假session的存在
今天之后设计的将由IP加token进行双重校验

后续需补充字段：动荡网络环境下根据请求cookie发来的token进行IP更换（可考虑不添加）
'''


class MyNewSession:
    def __init__(self, redis_=REDIS, db_num: int = SESSION_DB_NUM):
        self.redis = redis_()
        self.redis.select(db_num)

    def set(self, key, value, islogin: bool = False, time: int = None):
        if islogin:
            token_bind(ip_=ip())
        token = get_token(ip_=ip())
        if token is None: return
        if type(value) == bool: value = "1" if value else "0"
        for i in range(5):
            try:
                self.redis = REDIS()
                self.redis.select(SESSION_DB_NUM)
                self.redis.set(key + get_ip() + token, value)
                self.redis.select(SESSION_DB_NUM)
                if time is None:
                    self.redis.expire(key + get_ip() + token, LOGIN_LIMIT)
                else:
                    self.redis.expire(key + get_ip() + token, time)
                break
            except redis.exceptions.AuthenticationError:
                continue

    def get(self, key, t_check: str = None):
        token = get_token(ip_=ip())
        if token is None: return
        if t_check is not None:
            if t_check != token[0:9]:
                token_unbind()
                return None
        for i in range(5):
            try:
                self.redis = REDIS()
                self.redis.live_connect()
                self.redis.select(SESSION_DB_NUM)
                return self.redis.get(key + get_ip() + token)
            except redis.exceptions.AuthenticationError:
                continue

    def del_(self, key, islogout: bool = False):
        token = get_token(ip_=ip())
        if token is None: return
        self.redis.select(SESSION_DB_NUM)
        self.redis.del_(key + get_ip() + token)
        if islogout:
            token_unbind(ip_=ip())

    def live(self, key, time: int = LOGIN_LIMIT):
        token = get_token(ip_=ip())
        if token is None: return
        for i in range(5):
            try:
                self.redis = REDIS()
                self.redis.expire(key + get_ip() + token, time)
                token_live(ip_=ip())
            except redis.exceptions.AuthenticationError:
                continue

    def get_token(self):
        return get_token(ip_=ip())


def token_bind(redis_=REDIS(), db_num: int = TOKEN_DB_NUM, ip_=ip(), livetime: int = LOGIN_LIMIT):
    """
    主要用于登录时绑定token用，token由后台随机生成
    """
    redis_.select(db_num)
    token = make_token()
    redis_.set(ip_, token)
    redis_.set(token, ip_)
    redis_.expire(ip_, livetime)
    redis_.expire(token, livetime)


def get_token(redis_=REDIS, db_num: int = TOKEN_DB_NUM, ip_=ip()):
    """
    获取响应IP地址的token
    """
    redis_ = redis_()
    redis_.live_connect()
    redis_.select(db_num)
    return redis_.get(ip_)


def token_live(redis_=REDIS, db_num: int = TOKEN_DB_NUM, ip_=ip(), livetime: int = LOGIN_LIMIT):
    """
    主要意义是为了给token续命，主要用于持续操作的时候
    """
    redis_ = redis_()
    redis_.live_connect()
    redis_.select(db_num)
    redis_.expire(ip_, livetime)


def token_unbind(redis_=REDIS(), db_num: int = TOKEN_DB_NUM, ip_=ip()):
    """
    在退出登录的时候执行该函数（请提前销毁对应的session）
    """
    token = get_token(ip_=ip_)
    redis_.select(db_num)
    redis_.del_(token)
    redis_.del_(ip_)

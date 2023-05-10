from flask import Flask, session
from flask_redis import FlaskRedis
from flask_session import Session


app = Flask(__name__)

redis = FlaskRedis()
session_store = Session()


class Config():
    # DEBUG调试模式
    DEBUG = True
    # json多字节转unicode编码
    JSON_AS_ASCII = False
    # 数据库链接配置
    SECRET_KEY = "123456"
    # session存储方式为redis
    SESSION_TYPE = "redis"
    # session保存数据到redis时启用的链接对象
    SESSION_REDIS = redis
    # 如果设置session的生命周期是否是会话期, 为True，则关闭浏览器session就失效
    SESSION_PERMANENT = True
    # 是否对发送到浏览器上session的cookie值进行加密
    SESSION_USE_SIGNER = True
    # 保存到redis的session数的名称前缀
    SESSION_KEY_PREFIX = "session:"
    # redis的链接配置
    REDIS_URL = "redis://:123456@192.168.99.254:56379/1"


app.config.from_object(Config)
# 初始化redis
redis.init_app(app)
# 初始化session_store
session_store.init_app(app)


@app.route('/')
def index():
    session['username'] = 'xiaohui'
    return 'ok'


@app.route('/get_session')
def get_session():
    print(session['username'])
    return 'ok'


@app.route('/redis1')
def set_redis():
    redis.set('username', 'xiaohuihui')
    redis.hset('brother', 'zhangfei', '17')
    return 'ok'


@app.route('/redis2')
def get_redis():
    user = redis.get('username').decode()
    print(user)
    bother = redis.hgetall('brother')
    print(bother)
    print(bother['zhangfei'.encode()].decode())

    return 'ok'


if __name__ == '__main__':
    app.run()

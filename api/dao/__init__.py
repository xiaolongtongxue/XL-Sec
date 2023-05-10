from dao.mysql.Connection import MySQL
from dao.redis.Connection import Redis

# Other Config
MYSQL = MySQL()


# REDIS = Redis()
def REDIS():
    return Redis()

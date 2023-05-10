# -*- coding:utf-8 -*-

# About Panel
PANEL_TITLE = "XL SEC"    # 该参数主要在邮箱中使用，可自行调整

# About API Host
PORT = 4567     # 占用端口，可根据实际情况进行调整
HOSTS = "0.0.0.0"
LOGIN_LIMIT = 150 * 60
SECERT_KEY = "UQCyU29PN=>>JvDH_uH>9%zB!.,]o^=ahYKGL2@a!su-"  # 自带Session的加密Key
STATIC_FOLDER = "STATIC"
TEMPLATE_FOLDER = "TEMPLATE"
CHILD_PROTOCOL = "http"     # 静态部分使用的协议，http协议也是可以接受的
CHILD_HOST = "static.xlsec.com"     # 静态部分使用的域名，一定要完整正确

# About MySQL Host
MYSQL_HOST = "127.0.0.1"    # MySQL数据库主机地址
MYSQL_PORT = "3306"         # MySQL数据库端口
MYSQL_USER = "root"         # MySQL数据库用户
MYSQL_PASSWORD = "123456"   # MySQL用户密码
MYSQL_DATABASE = "xlsec"    # MySQL数据库库名

# About Redis Host
REDIS_HOST = "127.0.0.1"    # Redis主机地址
REDIS_PORT = "6379"         # Redis端口
REDIS_PASSWORD = "123456"   # Redis使用密码

# About DB_NUM in Redis
SESSION_DB_NUM = 10  # SESSION记录用的Redis数据库，可从0-16中选择一个数字
TOKEN_DB_NUM = 11  # TOKEN 记录用的Redis数据库，可从0-16中选择一个数字
PANEL_DB_NUM = 12  # 面板专用的Redis数据库，可从0-16中选择一个数字
PANEL_LUA_DB_NUM = 6  # 面板和LUA过滤器通用的Redis数据库，可从0-16中选择一个数字，但需要和Lua相关配置一致，不建议修改
LUA_BLACK_RULES = 5  # 面板用的自动封禁IP可能存在的Redis数据库，可从0-16中选择一个数字，但需要和Lua相关配置一致，不建议修改

# About Lua Data（下边的为一些Nginx自开端口服务的一些URL及其BasicAuth的信息，如果主Nginx设备和Api设备不在同意设备请注意修改下边的host）
LUA_SET_DATA_URL = "http://127.0.0.1:81/setdata"
LUA_UNLOCK_DATA_URL = "http://127.0.0.1:81/unlockip?ip="
LUA_SET_DATA_URL_HEADERS = (
    'Authorization', 'Basic YWRtaW46YWRtaW43NDEyNTg5NjMvKi0=')

# About SMTP
SMTP_KEY = ""               # 请修改自己的SMTP Key，如果不修改则无法进行邮件发送
SMTP_SERVER = "smtp.qq.com" # 请修改自己的SMTP Server，如果不修改则无法进行邮件发送
SMTP_PORT = "465"   # 无特殊需求请勿修改，Smtp的发送端口【注意，不会占用本机端口】
SMTP_SENDING_EMAIL = "123@qq.com"  # Smtp Key的登陆邮箱
SMTP_LOGIN_EMAIL = SMTP_SENDING_EMAIL

# Panel rules upload
UPLOAD_LOG_PATH = 'upload_log/'

# Panel Security
MAX_CHANGE_PASSWD_TIME = 120
EMAIL_SEND_CYCLE = 10

# Config List
TYPES_LIST = ['others', 'iplist']
INJECTIONS = ['get', 'post', 'ua', 'cookie','form-data']
WHITE_LIST = ['ip-white', 'ip-black', 'url-white']

# Something for
TOTAL_TYPES = ['cc', 'injection', 'form-data', '总']

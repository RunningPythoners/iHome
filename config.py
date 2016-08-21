# coding:utf-8
import os

# mongodb_options = {
#     'host':'127.0.0.1',
#     'port':27017,
#     'db':'test_database',
#     'user':'kdh',
#     'pwd':'root'
# }

#mysql 主库配置
MYSQL_CONFIG_MASTER = {
    "server": "127.0.0.1",
    "username": "root",
    "password": "itcast",
    "dbname": "ihome"
}

MYSQL_CONFIG_SLAVER = [{
    "server": "127.0.0.1",
    "username": "root",
    "password": "itcast",
    "dbname": "ihome"
}]

redis_options = {
    'redis_host':'127.0.0.1',
    'redis_port':6379,
    'redis_pass':'',
}

REDIS_CONFIG_CACHE = [
    {'name': 'server1', 'host': '127.0.0.1', 'port': 6379, 'db': 0},
    {'name': 'server2', 'host': '127.0.0.1', 'port': 6379, 'db': 1}
]

#redis 事件通知地址
REDIS_CONFIG_EVENT = {
    "server": "127.0.0.1",
    "port": 6379,
    "db": 0
}

REDIS_CONFIG_STAT = {
    "server": "127.0.0.1",
    "port": 6379,
    "db": 2
}

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret':'0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies':False,
    'login_url':'/login',
    'debug':True,
}

passwd_hash_key = "ihome@$^*"
session_secret = "PgzRjediR/Op8jVyhElZ3Gp/aoUrmEQ9jw7KdBEEuIY="
session_timeout = 86400

log_path = os.path.join(os.path.dirname(__file__), 'logs/log')

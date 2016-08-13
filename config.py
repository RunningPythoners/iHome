# coding:utf-8
import os

mongodb_options = {
    'host':'127.0.0.1',
    'port':27017,
    'db':'test_database',
    'user':'kdh',
    'pwd':'root'
}

redis_options = {
    'redis_host':'127.0.0.1',
    'redis_port':6379,
    'redis_pass':'',
}

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'cookie_secret':'0Q1AKOKTQHqaa+N80XhYW7KCGskOUE2snCW06UIxXgI=',
    'xsrf_cookies':True,
    'login_url':'/login',
    'debug':True,
}

passwd_hash_key = "ihome@$^*"
session_secret = "PgzRjediR/Op8jVyhElZ3Gp/aoUrmEQ9jw7KdBEEuIY="
session_timeout = 86400

log_path = os.path.join(os.path.dirname(__file__), 'logs/log')

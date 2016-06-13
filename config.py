# coding:utf-8
import os

mongodb_options = {
    'host':'127.0.0.1',
    'port':27017,
    'db':'test_database'
}

settings = {
    'template_path': os.path.join(os.path.dirname(__file__), 'Templates'),
    'static_path': os.path.join(os.path.dirname(__file__), 'statics'),
    'debug':True,
}

passwd_hash_key = "ihome@$^*"
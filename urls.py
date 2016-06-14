# coding:utf-8

from Handler.BaseHandler import *

urls = [
    (r'^/$', IndexHandler),
    (r'^/register$', RegisterHandler),
    (r'^/login$', LoginHandler),
    (r'^/(.*)$', IndexHandler),
]
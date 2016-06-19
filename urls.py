# coding:utf-8

from handlers.BaseHandler import *

urls = [
    (r'^/$', IndexHandler),
    (r'^/register$', RegisterHandler),
    (r'^/login$', LoginHandler),
    (r'^/profile$', ProfileHandler),
    (r'^/orders$', OrdersHandler),
    (r'^/.*$', IndexHandler),
]
# coding:utf-8

from handlers.BaseHandler import *

urls = [
    (r'^/$', IndexHandler),
    (r'^/register$', RegisterHandler),
    (r'^/login$', LoginHandler),
    (r'^/profile$', ProfileHandler),
    (r'^/orders$', OrdersHandler),
    (r'^/sync$', SyncHandler),
    (r'^/async$', AsyncHandler),
    (r'^/enterProfilePageNotify$', EnterProfilePageNotifyHandler),
    (r'^/house/(?P<hid1>.+)/(?P<hid2>.+)$', HouseHandler),
    (r'^/taobaoip/*$', TaobaoIPHandler),
    (r'^/asynctaobaoip/*$', AsyncTaobaoIPHandler),
    (r'^/.*$', IndexHandler),
]
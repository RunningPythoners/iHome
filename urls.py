# coding:utf-8

from handlers.BaseHandler import *
from handlers.MailTool.sendmail import *
from tornado.web import StaticFileHandler
from config import settings
from handlers import VerifyCode, Passport

import os


ihome_api_urls = [
    (r'^/api/imagecode?', VerifyCode.ImageCodeHandler),
    (r'^/api/smscode?', VerifyCode.SMSCodeHandler),
    (r'^/api/register$', Passport.RegisterHandler),
    (r'^/api/login$', Passport.LoginHandler),
    (r'^/api/check-login$', Passport.CheckLoginHandler),
]

mis_api_urls = [
]

urls = [
    (r'^/()$', StaticFileHandler, {'path':os.path.join(settings['static_path'], 'html/ihome'), 'default_filename':'index.html'}),
    (r'^/view/(.+)$', StaticFileHandler, {'path':os.path.join(settings['static_path'], 'html/ihome')}),
    (r'^/mis/()$', StaticFileHandler, {'path':os.path.join(settings['static_path'], 'html/mis'), 'default_filename':'index.html'}),
    (r'^/mis/view/(.+)$', StaticFileHandler, {'path':os.path.join(settings['static_path'], 'html/mis')}),
]

urls.extend(ihome_api_urls)
urls.extend(mis_api_urls)

# urls = [
#     (r'^/$', IndexHandler),
#     (r'^/register$', RegisterHandler),
#     (r'^/login$', LoginHandler),
#     (r'^/profile$', ProfileHandler),
#     (r'^/orders$', OrdersHandler),
#     (r'^/sync$', SyncHandler),
#     (r'^/async$', AsyncHandler),
#     (r'^/enterProfilePageNotify$', EnterProfilePageNotifyHandler),
#     (r'^/house/(?P<hid1>.+)/(?P<hid2>.+)$', HouseHandler),
#     (r'^/taobaoip/*$', TaobaoIPHandler),
#     (r'^/asynctaobaoip/*$', AsyncTaobaoIPHandler),
#     (r'^/search*$', SearchHandler),
#     (r'^/sendmail*$', SendMailHandler),
#     (r'^/order*$', OrderHandler),
#     (r'^/.*$', IndexHandler),
# ]
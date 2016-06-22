# coding:utf-8

from tornado.web import RequestHandler, authenticated, asynchronous
import re
import hashlib, binascii
import config
from utils import session
import os
from tornado import gen
from tornado.websocket import WebSocketHandler
import logging
import requests
from tornado.httpclient import AsyncHTTPClient

class IndexHandler(RequestHandler):

    def get(self):
        logging.error('file:%s,  this is error' % __file__)
        logging.info('this is info')
        logging.debug('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        logging.warning('this is warning')
        logging.debug('this is warning')
        self.render("index_base.html", is_login=False)

    def post(self):
        self.render("index.html")

class LoginHandler(RequestHandler):
    def get(self):
        self.write("enter login html")

class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(BaseHandler, self).__init__(*args, **kwargs)
        self.session = session.Session(self.application.session_manager, self)

    def get_current_user(self):
        return self.session.get('name')

class ProfileHandler(BaseHandler):
    @authenticated
    def get(self):
        # self.write("进入个人主页")
        message = '%s entered profile page' % self.session.get('name', u'aaa')
        EnterProfilePageNotifyHandler.notify(message)
        logging.info(message)
        self.render('profile.html', is_login=True, user_name=self.session.get('name', u'亲'))

class OrdersHandler(BaseHandler):
    @authenticated
    def get(self):
        # self.write("进入个人主页")
        self.render('orders.html', is_login=True, user_name=self.session.get('name', u'亲'))


class RegisterHandler(RequestHandler):
    def get(self):
        self.render("register.html", error_msg="注册")

    def post(self):
        name = self.get_argument('name')
        mobile = self.get_argument('mobile')
        passwd = self.get_argument('passwd1')

        # files = self.request.files
        # avatar_file = files.get('avatar')
        # upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        # if avatar_file:
        #     avatar_file = avatar_file[0].get('body')
        #     file = open(os.path.join(upload_path, 'a1'), 'w+')
        #     file.write(avatar_file)
        #     file.close()
        if name in (None, '') or not re.match(r'^1[3|4|5|7|8]\d{9}$', mobile) or passwd in (None, ''):
            #self.write('{"status":"E01"}')
            self.render("register.html", error_msg="手机号格式错误!")
            return
        #passwd = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', passwd, config.passwd_hash_key, 100000))
        passwd = hashlib.sha256( config.passwd_hash_key + passwd ).hexdigest()
        user = {'name':name, 'mobile':mobile, 'passwd':passwd}
        try:
            ret = self.application.db.users.insert(user)
        except Exception as e:
            self.render("register.html", error_msg="用户名已存在!")
        try:
            self.session = session.Session(self.application.session_manager, self)
            self.session['name'] = name
            self.session['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error("catch session error:" + e)
        #self.write('{"status":"00"}')
        self.redirect("/") 


class SyncHandler(RegisterHandler):
    def get(self):
        os.system('ping -c 1 www.baidu.com')        
        self.finish('finished')

class AsyncHandler(RegisterHandler):
    @gen.coroutine
    def get(self):
        ret = yield gen.Task(lambda x:os.system('ping -c 1 www.baidu.com'))
        # ret = yield gen.Task(self.task)
        # self.write(ret)
        self.finish('OK')

    @gen.coroutine
    def task(self):
        os.system('ping -c 1 www.baidu.com')
        return 'task finished'

# class LoginNotifyHandler(WebSocketHandler):
#     users = set()
#     def open(self):
#         LoginNotifyHandler.users.add(self)

#     def on_close(self):
#         LoginNotifyHandler.users.remove(self)

#     def on_message(self):
#         pass

#     @classmethod
#     def send_message(cls, message):
#         for user in cls.users:
#             try:
#                 user.write_message(message)
#             except Exception as e:
#                 print e

class HouseHandler(RequestHandler):
    def get(self, hid1, hid2):
        hid3 = self.get_argument('hid3', 'a')
        self.write('this is hid: %s hid2: %s hid3:%s' % (hid1, hid2, hid3))

class TaobaoIPHandler(RequestHandler):
    def get(self):
        url = 'http://ip.taobao.com/service/getIpInfo.php?ip=210.75.225.254'
        ret = requests.get(url)
        self.write(str(dir(ret)))
        # self.write(ret.content)

class AsyncTaobaoIPHandler(RequestHandler):

    # @asynchronous
    # def get(self):
    #     url = 'http://ip.taobao.com/service/getIpInfo.php?ip=210.75.225.254'
    #     client = AsyncHTTPClient()
    #     client.fetch(url, self.callback)
    #     self.write('after fetch')

    # def callback(self, response):
    #     self.write(str(dir(response)))
    #     self.write(response.body)
    #     self.finish('finished')

    @gen.coroutine
    def get(self):
        url = 'http://ip.taobao.com/service/getIpInfo.php?ip=210.75.225.254'
        client = AsyncHTTPClient()
    #     self.write('after fetch')
        response = yield client.fetch(url)
        self.write('after fetch')
        self.write(response.body)
        self.finish('finished')

class EnterProfilePageNotifyHandler(WebSocketHandler):
    users = set()
    # a = [2,1,3,1]
    # list(set(a)).sort(a.index)
    def open(self):
        EnterProfilePageNotifyHandler.users.add(self) 
        logging.error(EnterProfilePageNotifyHandler.users)

    def on_close(self):
        EnterProfilePageNotifyHandler.users.remove(self)

    def on_message(self):
        pass

    @classmethod
    def notify(cls, message):
        logging.error(cls.users)
        for user in cls.users:
            user.write_message(message)
            logging.error(message)

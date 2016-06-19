# coding:utf-8

from tornado.web import RequestHandler, authenticated
import re
import hashlib, binascii
import config
import logging
from utils import session
import os

class IndexHandler(RequestHandler):

    def get(self):
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

        files = self.request.files
        avatar_file = files.get('avatar')
        upload_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
        if avatar_file:
            avatar_file = avatar_file[0].get('body')
            file = open(os.path.join(upload_path, 'a1'), 'w+')
            file.write(avatar_file)
            file.close()
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
            pass
        #self.write('{"status":"00"}')
        self.redirect("/") 

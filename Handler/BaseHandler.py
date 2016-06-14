# coding:utf-8

from tornado.web import RequestHandler, authenticated
import re
import hashlib, binascii
import config
from utils import session

class IndexHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super(IndexHandler, self).__init__(*args, **kwargs)
        self.session = session.Session(self.application.session_manager, self)

    def get_current_user(self):
        return self.session.get('name')

    @authenticated
    def get(self):
        self.render("index.html")

    def post(self):
        self.render("index.html")

class LoginHandler(RequestHandler):
    def get(self):
        self.write("enter login html")

class RegisterHandler(RequestHandler):
    def get(self):
        self.render("register.html", error_msg="注册")

    def post(self):
        name = self.get_argument('name')
        mobile = self.get_argument('mobile')
        passwd = self.get_argument('passwd1')
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

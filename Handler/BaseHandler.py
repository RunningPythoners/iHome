# coding:utf-8

from tornado.web import RequestHandler
import re
import hashlib, binascii
import config

class IndexHandler(RequestHandler):
    def get(self):
        self.render("index.html")

    def post(self):
        self.render("index.html")

class RegisterHandler(RequestHandler):
    def get(self):
        self.render("register.html", error_msg="Welcome!")

    def post(self):
        name = self.get_argument('name')
        mobile = self.get_argument('mobile')
        passwd = self.get_argument('passwd1')
        if name in (None, '') or not re.match(r'^1[3|4|5|7|8]\d{9}$', mobile) or passwd in (None, ''):
            self.write('{"status":"E01"}')
            return
        passwd = binascii.hexlify(hashlib.pbkdf2_hmac('sha256', passwd, config.passwd_hash_key, 100000))
        user = {'name':name, 'mobile':mobile, 'passwd':passwd}
        try:
            ret = self.application.db.users.insert(user)
        except Exception as e:
            self.render("register.html", error_msg="name exist!")
        self.write('{"status":"00"}')

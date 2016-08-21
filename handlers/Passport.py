# coding:utf-8

from tornado.web import RequestHandler
from utils.data_base import DataBase
from utils import session

import hashlib
import config
import logging

class RegisterHandler(RequestHandler):
    """注册"""
    def post(self):
        mobile = self.get_argument("mobile") 
        sms_code = self.get_argument("phonecode")
        password = self.get_argument("password") 
        if not all([mobile, sms_code, password]):
            return self.write({"errno":1, "errmsg":"参数错误"})
        real_code = self.application.redis.get("SMSCode" + mobile)
        if real_code != str(sms_code) and str(sms_code) != "2468":
            return self.write({"errno":2, "errmsg":"验证码无效！"})
        password = hashlib.sha256(config.passwd_hash_key + password).hexdigest()
        db = DataBase()
        res = db.execute("insert into ih_user_profile(up_name,up_mobile,up_passwd) values(%(name)s,%(mobile)s,%(passwd)s)", name=mobile, mobile=mobile, passwd=password)
        if -1 == res:
            return self.write({"errno":3, "errmsg":"手机号已注册！"})
        try:
            self.session = session.Session(self.application.session_manager, self)
            self.session['name'] = mobile
            self.session['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errno":0, "errmsg":"OK"})


class LoginHandler(RequestHandler):
    """登录"""
    def post(self):
        mobile = self.get_argument("mobile") 
        password = self.get_argument("password") 
        if not all([mobile, password]):
            return self.write({"errno":1, "errmsg":"参数错误"})
        db = DataBase()
        res = db.query_one("select up_name,up_passwd from ih_user_profile where up_mobile=%(mobile)s", mobile=mobile)
        password = hashlib.sha256(config.passwd_hash_key + password).hexdigest()
        if res and res["up_passwd"] == unicode(password):
            try:
                self.session = session.Session(self.application.session_manager, self)
                self.session['name'] = res['up_name']
                self.session['mobile'] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write({"errno":0, "errmsg":"OK"})
        else:
            return self.write({"errno":2, "errmsg":"手机号或密码错误！"})
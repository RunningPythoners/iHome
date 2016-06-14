#!/usr/bin/env python
#coding:utf-8

import tornado.web
import hmac
import json
import hashlib
import redis
import uuid

#继承字典，session存取模仿字典使用
class SessionData(dict):
    #初始化提供session_id和hmac_key
    def __init__(self, session_id, hmac_key):
        self.session_id = session_id
        self.hmac_key = hmac_key

#继承SessionData
class Session(SessionData):
    #初始化，绑定session_manager和tornado对应的handler
    def __init__(self, session_manager, request_handler):
        self.session_manager = session_manager
        self.request_handler = request_handler

        try:
            #正常访问
            current_session = session_manager.get(request_handler) 
        except InvalidSessionException:
            current_session = session_manager.get()

        #取出current_session中的数据
        for key, data in current_session.iteritems(): 
            self[key] = data 
        # 保存下 session_id 
        self.session_id = current_session.session_id 
        # 以及对应的 hmac_key 
        self.hmac_key = current_session.hmac_key 

    # 定义 save 方法，用于 session 修改后的保存，实际调用 session_manager 的 set 方法 
    def save(self): 
        self.session_manager.set(self.request_handler, self)

class SessionManager(object):
    def __init__(self, secret, store_options, session_timeout):
        self.secret = secret   
        self.session_timeout = session_timeout   
        try:   
            if store_options['redis_pass']:   
                self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'], password=store_options['redis_pass'])   
            else:   
                self.redis = redis.StrictRedis(host=store_options['redis_host'], port=store_options['redis_port'])   
        except Exception as e:   
            print e

    def _fetch(self, session_id):   
        try:   
            session_data = raw_data = self.redis.get(session_id)   
            if raw_data != None:   
                self.redis.setex(session_id, self.session_timeout, raw_data)   
                session_data = json.loads(raw_data)   
            if type(session_data) == type({}):   
                return session_data   
            else:   
                return {}   
        except IOError:   
            return {}   

    def get(self, request_handler = None):   
        if (request_handler == None):   
            session_id = None   
            hmac_key = None   
        else:   
            session_id = request_handler.get_secure_cookie("session_id")   
            hmac_key = request_handler.get_secure_cookie("verification")   
        if session_id == None:   
            session_exists = False   
            session_id = self._generate_id()   
            hmac_key = self._generate_hmac(session_id)   
        else:   
            session_exists = True   
        check_hmac = self._generate_hmac(session_id)   
        if hmac_key != check_hmac:   
            raise InvalidSessionException()   
        session = SessionData(session_id, hmac_key)   
        if session_exists:   
            session_data = self._fetch(session_id)   
            for key, data in session_data.iteritems():   
                session[key] = data   
        return session 
 
    def set(self, request_handler, session):   
        request_handler.set_secure_cookie("session_id", session.session_id)   
        request_handler.set_secure_cookie("verification", session.hmac_key)   
        session_data = json.dumps(dict(session.items()))   
        self.redis.setex(session.session_id, self.session_timeout, session_data)   

    def _generate_id(self):   
        new_id = hashlib.sha256(self.secret + str(uuid.uuid4()))   
        return new_id.hexdigest()   

    def _generate_hmac(self, session_id):   
        return hmac.new(session_id, self.secret, hashlib.sha256).hexdigest()   

class InvalidSessionException(Exception):   
    pass 

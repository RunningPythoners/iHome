# -*- coding: utf-8 -*-


from Cookie import SimpleCookie, CookieError
import urllib
import logging
import base64
import time
import hashlib

COOKIE_SALT = "1ed913d5-2a6f-4dae-90e6-e203ff8c693d"
class UserCookie(SimpleCookie):


    def __init__(self):
        SimpleCookie.__init__(self)
        self.token = ''
        self.userid = ''
        self.passport = ''
        self._loaded = False

    def generate(self, expire):
        data = "id:{0},passport:{1}".format(self.userid,
                                            self.passport,)
        head = "{0}|{1}|{2}".format(int(time.time()), expire, base64.encodestring(data))
        s = "{0}&{1}".format(head, COOKIE_SALT)
        m = hashlib.md5(s).hexdigest().lower()
        self.token = "{0}|{1}".format(head, m)
        self._loaded = True
        
    def client_load(self, rawdata):
        assert not self._loaded
        try:
            # FIXME: 解决某些客户端会在cookie最前面加一个逗号的问题
            rawdata = rawdata.strip(',')
            self.load(rawdata)
        except CookieError as e:
            logging.exception(e)
            self.load('')
        if 'zhjttk' in self:
            self.token = self._decode('zhjttk')
        self.split_token()
        self._loaded = True

    def client_output(self, handler):
        """ return list of cookie value """
        assert self._loaded
        data = self
        data['zhjttk'] = self._urlencode(self.token)
        #return ['{0}={1}; path=/; domain=.zhjt.com'.format(c.key, c.coded_value) for c in data.values()]
        for c in data.values():
            handler.set_cookie(c.key, c.coded_value)


    def _decode(self, key):
        value = self[key].coded_value
        return urllib.unquote(value).decode('utf-8')

    def _urlencode(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        return urllib.quote(value, '')

    def valid_token(self):
        if not self.token:
            return False
        info = self.token.split('|')
        cookie_time = int(info[0])
        expire = int(info[1])
        data = info[2]
        check_code = info[3]
        if (cookie_time + expire) < int(time.time()):
            return False
        s = "{0}|{1}|{2}&{3}".format(cookie_time, expire, data, COOKIE_SALT)
        m = hashlib.md5(s).hexdigest().lower()
        return check_code == m


    def split_token(self):
        """ 
        1389059260|3600|aWQ6MTAwMDcxMTY0LG5uOuS8mOmFtzExLHZpcDpmYWxzZSx5dGlkOjMwMDA3MTE3MCx0aWQ6MTUwMDAxNDAw|
        1fdea957043501ab5c5f33a6c8a32fe8 
        """
        if not self.token:
            return None
        info = self.token.split('|')
        result = base64.decodestring(info[2]).split(',')
        for rs in result:
            if rs.startswith('id:'):
                self.userid = rs.replace('id:', '') 
            if rs.startswith('passport:'):
                self.passport = rs.replace('passport:', '')
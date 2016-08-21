#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from utils.common import CJsonEncoder

class ResponseData(object):

    def __init__(self):
        self._status = 200
        self._errorCode = 0
        self._message = ""
        self._response = ""

    def set_header(self, reqHandler):
        reqHandler.set_header('Content-Type', 'application/json; charset=UTF-8')

    def responseData(self, reqHandler):
        reqHandler.set_status(self._status)
        self.set_header(reqHandler)
        reqHandler.write(self._response)
        reqHandler.finish()


class ResponseHtml(ResponseData):

    def setResponseData(self, message):
        self._response = message

    def set_header(self, reqHandler):
        reqHandler.set_header('Content-Type', 'text/html; charset=UTF-8')

    def responseData(self, reqHandler):
        super(ResponseHtml, self).responseData(reqHandler)


class ResponseJson(ResponseData):

    def setResponseData(self, message):
        self._message = message

    def responseData(self, reqHandler):
        self._response = json.dumps(self._message, ensure_ascii=False, cls=CJsonEncoder)
        super(ResponseJson, self).responseData(reqHandler)


class ResponseError(ResponseData):

    def setResponseData(self, status, errorCode, message):
        self._status = status
        self._errorCode = errorCode
        self._message = message

    def responseData(self, reqHandler):
        self._response = json.dumps({"error":self._errorCode, 
                                     "message":self._message
                                     }, 
                                     ensure_ascii=False,
                                     cls=CJsonEncoder)
        super(ResponseError, self).responseData(reqHandler)


class ResponseRedirect(ResponseData):

    def setResponseData(self, redirectUrl):
        self._redirectUrl = redirectUrl

    def responseData(self, reqHandler):
        reqHandler.redirect(self._redirectUrl)


class ResponseImage(ResponseData):

    def set_header(self, reqHandler):
        reqHandler.set_header('Content-type', 'image/jpg')

    def setResponseData(self, image):
        self._response = image

    def responseData(self, reqHandler):
        super(ResponseImage, self).responseData(reqHandler)

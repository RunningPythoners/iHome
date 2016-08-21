#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import logging
import random
import urllib
from tornado import httpclient


class _RPC(object):

    def __init__(self):
        pass

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
            cls.__logger = logging.getLogger("RPC")
        return cls._instance

    @classmethod
    def random_server(cls, servers):
        i = random.randint(0, len(servers)-1)
        return servers[i]

    @classmethod
    def http_get(cls, url, to_json=True, headers={}):
        for i in xrange(3):
            try:
                http_request = httpclient.HTTPRequest(url=url,
                                                      method='GET',
                                                      headers=headers,
                                                      connect_timeout=5, 
                                                      request_timeout=10)
                http_client = httpclient.HTTPClient()
                http_response = http_client.fetch(http_request)
                if to_json == True:
                    return json.loads(http_response.body)
                else:
                    return http_response.body
            except Exception as ex:
                print "http_get ", ex
                cls.__logger.error("http_get error url %s ex %s" % (url, ex))
        return None

    @classmethod
    def http_post(cls, url, data, to_json=True, cookie=""):
        for i in xrange(3):
            try:
                http_request = httpclient.HTTPRequest(url=url,
                                                      headers={"Cookie":cookie},
                                                      method='POST',
                                                      body=data,
                                                      connect_timeout=5, 
                                                      request_timeout=10)
                http_client = httpclient.HTTPClient()
                http_response = http_client.fetch(http_request)
                if to_json == True:
                    return json.loads(http_response.body)
                else:
                    return http_response.body
            except Exception as ex:
                print "http_post ", ex
                cls.__logger.error("http_post error url %s ex %s" % (url, ex))
        return None

RPC = _RPC().instance()

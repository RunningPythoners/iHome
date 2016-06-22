# coding:utf-8

import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
import pymongo
import config

from tornado.options import options, define
from urls import urls
from utils import session

define("port", default=8000, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        mongoClient = pymongo.MongoClient(config.mongodb_options['host'], config.mongodb_options['port'])
        self.db = mongoClient[config.mongodb_options['db']]
        settings = config.settings
        self.session_manager = session.SessionManager(config.session_secret, config.redis_options, config.session_timeout)
        tornado.web.Application.__init__(self, urls, **settings)


if __name__ == '__main__':
    options.log_file_prefix = config.log_path
    options.logging = 'debug'
    tornado.options.parse_command_line()
    app = Application()
    httpServer = tornado.httpserver.HTTPServer(app)
    httpServer.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
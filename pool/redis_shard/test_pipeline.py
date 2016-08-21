#!/usr/bin/python
# -*- coding: utf-8 -*-
import unittest

from nose.tools import eq_
from redis.exceptions import WatchError

from shard import RedisShardAPI
from _compat import b, xrange
from conf.settings import REDIS_CONFIG_SESSION


class TestShard(unittest.TestCase):

    def setUp(self):
        self.client = RedisShardAPI(REDIS_CONFIG_SESSION)
        self.clear_db()

    def tearDown(self):
        pass

    def clear_db(self):
        self.client.delete('testset')
        self.client.delete('testzset')
        self.client.delete('testlist')

    def test_pipeline(self):
        self.client.set('test', '3')

        with self.client.pipeline() as pipe:
            pipe.watch('test')
            eq_(self.client.get('test'), b'3')
            pipe.multi()
            pipe.incr('test')
            eq_(pipe.execute(), [4])
        eq_(self.client.get('test'), b'4')

        with self.client.pipeline() as pipe:
            pipe.watch('test')
            pipe.multi()
            pipe.incr('test')
            self.client.decr('test')
            self.assertRaises(WatchError, pipe.execute)
        eq_(self.client.get('test'), b'3')

        keys_of_names = {}
        with self.client.pipeline() as pipe:
            for key in xrange(100):
                key = str(key)
                name = pipe.shard_api.get_server_name(key)
                if name not in keys_of_names:
                    keys_of_names[name] = key
                else:
                    key1 = key
                    key2 = keys_of_names[name]

                    pipe.watch(key1, key2)
                    pipe.multi()
                    pipe.set(key1, 1)
                    pipe.set(key2, 2)
                    pipe.execute()

                    eq_(self.client.get(key1), b'1')
                    eq_(self.client.get(key2), b'2')
                    break

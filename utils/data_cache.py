#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#
import os
import json
import logging
import time
from utils.common import CJsonEncoder
from utils.common import get_cache_redis_conn 
from utils.asyncrun import AsyncRunRemoteCache


class DataCache(object):

    def __init__(self, f, **args):
        f = os.path.basename(f)
        name, ext = os.path.splitext(f)
        self._py = name
        self._args = args
        self._logging = logging.getLogger(self.__class__.__name__)
        self._cache_conn = get_cache_redis_conn()

    def _redis_expire(self):
        return 3600

    def _update_expire(self):
        return 180

    def _redis_key(self, **args):
        return None

    def _use_hash(self):
        return False

    def _hash_name(self):
        return "default"

    def _get_data_from_cache(self, **args):
        if self._use_hash():
            redis_data = self._cache_conn.hget(self._hash_name(), self._redis_key(**args))
        else:
            redis_data = self._cache_conn.get(self._redis_key(**args))
        if redis_data:
            data = json.loads(redis_data)
            if (time.time()) - data["time"] > self._update_expire():
                AsyncRunRemoteCache.add_task({"py":"data.{0}".format(self._py), 
                    "module":self.__class__.__name__, 
                    "fun":"update_data", 
                    "param":self._args})
            else:
                pass
            return data["data"]
        else:
            return None

    def _get_data_from_original(self, **args):
        return {}

    def _set_data_to_cache(self, data, **args):
        redis_data = {"time":int(time.time()), "data":data}
        if self._use_hash():
            self._cache_conn.hset(self._hash_name(), self._redis_key(**args),
                                  json.dumps(redis_data, cls=CJsonEncoder))
            #self._cache_conn.expire(self._hash_name(), self._redis_expire())
        else:
            self._cache_conn.setex(self._redis_key(**args),
                                   json.dumps(redis_data, cls=CJsonEncoder),
                                   self._redis_expire())

    def get_data(self):
        try:
            data = self._get_data_from_cache()
            if data is None:
                data = self._get_data_from_original()
                if data is None:
                    data = {}
                self._set_data_to_cache(data)
        except Exception as ex:
            data = {}
            self._logging.error("get_data error %s" % ex)
        finally:
            return data

    def update_cache_data(self, force=False):
        if not force:
            if self._use_hash():
                redis_data = self._cache_conn.hget(self._hash_name(), self._redis_key())
            else:
                redis_data = self._cache_conn.get(self._redis_key())
            if redis_data:
                data = json.loads(redis_data)
                if (time.time()) - data["time"] < self._update_expire():
                    return
        data = self._get_data_from_original()
        if data is None:
            data = {}
        self._set_data_to_cache(data)

    @classmethod
    def update_data(cls, **args):
        o = cls(**args)
        force = args.get("force", False)
        o.update_cache_data(force=force)

    def delete_cache(self, **args):
        if self._use_hash():
            self._cache_conn.hdel(self._hash_name(), self._redis_key())
        else:
            self._cache_conn.delete(self._redis_key())

    def delete_cache_by_name(self):
        if self._use_hash():
            self._cache_conn.delete(self._hash_name())


class DatasCache(DataCache):

    def __init__(self, f, **args):
        super(DatasCache, self).__init__(f, **args)
        self._objects = {}

    def get_object(self, arg):
        obj = self._objects.get(arg, None)
        if not obj:
            obj = self.new_object(arg)
            self._objects[arg] = obj
        return obj

    def new_object(self, arg):
        pass

    def _transform_datas(self, datas):
        pass

    def _transform_arg(self, arg):
        return arg

    def _args_key_name(self):
        pass

    def _find_data_arg(self, data):
        pass

    def _get_data_from_cache(self, **args):
        t = self.get_object(args["arg"])
        return t._get_data_from_cache()

    def _set_data_to_cache(self, data, **args):
        t = self.get_object(args["arg"])
        t._set_data_to_cache(data, **args)

    def get_data(self):
        uncache = []
        results = []
        for arg in self._args[self._args_key_name()]:
            t_arg = self._transform_arg(arg)
            data = self._get_data_from_cache(arg=t_arg)
            if data:
                results.append(data)
            else:
                uncache.append(t_arg)
        if uncache:
            original_datas = self._get_data_from_original(uncache=uncache)
            if not original_datas:
                original_datas = []
            for data in original_datas:
                self._set_data_to_cache(data, arg=self._find_data_arg(data))
                results.append(data)
        return self._transform_datas(results)
            

class ExecuteData(object):

    def __init__(self, f, **args):
        f = os.path.basename(f)
        name, ext = os.path.splitext(f)
        self._py = name
        self._args = args
        self._logging = logging.getLogger(self.__class__.__name__)
        self._cache_conn = get_cache_redis_conn()

    def operate_data(self):
        pass

    @classmethod
    def execute_data(cls, **args):
        o = cls(**args)
        o.operate_data()

    def set_data(self):
        AsyncRunRemoteCache.add_task({"py":"data.{0}".format(self._py), 
            "module":self.__class__.__name__, 
            "fun":"execute_data", 
            "param":self._args})

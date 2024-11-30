#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/10/4 18:50
# redis-server
from redis.cluster import RedisCluster
from Library.Common.Utils.SingletonTypeUtil import SingletonType
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.Contexts import *

redis_path_dic = {"room": "roomList::roomInfo::", "token": "userInfo::token", "room_id_list": "roomIdList",
                  "sid_uid": "sid::uid", "uid_sid": "uid::sid", "uid_room_id": "uid::rid",
                  "system_config": "systemConfig", "round_data": "game::roundData::"}


class RedisBase(object, metaclass=SingletonType):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        # super().__init__()
        server = YamlUtil().load_common_config('redis')

        self.connect = RedisCluster(host=server["ip"], port=server["port"], password=server["password"])
        self.connect_origin = RedisCluster(host=server["ip"], port=server["port"], password=server["password"],
                                           decode_responses=False)
        rds_context.set(self)

    def set_expire_time(self, key: str, expire_time: int):
        self.connect.expire(key, expire_time)

    def set_string(self, name, value, ex=0, nx=True, xx=False):
        """
        普通键值类型，值为一个整体文本
        set(name, value, ex=None, px=None, nx=False, xx=False)
        ex：过期时间（秒），时间到了后redis会自动删除
        nx：如果设置为True，则只有name不存在时，当前set操作才执行
        xx：如果设置为True，则只有name存在时，当前set操作才执行
        :return:
        """
        if ex:
            self.connect.set(name, value, ex=ex, nx=nx, xx=xx)
        else:
            self.connect.set(name, value, nx=nx, xx=xx)

    def get_string(self, name):
        try:
            data = self.connect.get(name)
            return data.decode() if data else data
        except AttributeError:
            return ""

    def get_strings(self, name):
        try:
            data = self.connect.mget(name)
            return data.decode() if data else data
        except AttributeError:
            return ""

    def get_string_not_decode(self, name):
        return self.connect_origin.get(name)

    def hash_set(self, name: str, key, value):
        self.connect.hset(name, key, value)

    def hash_multi_set(self, name: str, mapping: dict):
        for key, value in mapping.items():
            self.hash_set(name, key, value)

    def hash_get(self, name: str, key):
        data = self.connect.hget(name, key)
        return data.decode() if data else data

    def hash_multi_get(self, name: str, *args):
        return self.connect.hmget(name, *args)

    def delete_key(self, name: str):
        self.connect.delete(name)

    def delete_key_like(self, name: str, batch_size=1000):
        try:
            cursor = '0'
            while cursor != 0:
                cursor, keys = self.connect.scan(cursor=cursor, match=f'{name}*', count=batch_size)
                if keys:
                    self.connect.delete(*keys)
        except Exception as e:
            raise AssertionError(f"删除匹配键失败: {e}")

    def hash_del(self, name: str, key):
        self.connect.hdel(name, key)

    def hash_get_all(self, name: str):
        return self.connect.hgetall(name)

    def hash_get_all_keys(self, name: str):
        return self.connect.hkeys(name)


if __name__ == "__main__":
    env_context.set('sit')
    rc = RedisBase()

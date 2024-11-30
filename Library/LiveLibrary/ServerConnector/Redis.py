#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/10/4 18:50
# redis-server
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from redis.cluster import RedisCluster
from Library.LiveLibrary.CommonUtil import SingletonType
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.Contexts import *

redis_path_dic = {"room": "roomList::roomInfo::", "token": "userInfo::token", "room_id_list": "roomIdList",
                  "sid_uid": "sid::uid", "uid_sid": "uid::sid", "uid_room_id": "uid::rid",
                  "system_config": "systemConfig", "round_data": "game::roundData::"}


class RedisBase(object, metaclass=SingletonType):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        server_info = YamlUtil().load_common_config('redis', 'live')
        self.connect = RedisCluster(host=server_info['host'], port=server_info['port'],
                                    password=server_info['password'])
        self.connect_origin = RedisCluster(host=server_info['host'], port=server_info['port'],
                                           password=server_info['password'], decode_responses=False)
        live_rds_context.set(self)

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
        
    def delete_key_like(self, name: str):
        try:
            self.connect.delete(*self.connect.keys(pattern=f'{name}*'))
        except Exception as e:
            pass

    def hash_del(self, name: str, key):
        self.connect.hdel(name, key)

    def hash_get_all(self, name: str):
        return self.connect.hgetall(name)

    def hash_get_all_keys(self, name: str):
        return self.connect.hkeys(name)


if __name__ == "__main__":
    rc = RedisBase()
    # print(rc.get_string("GA05"))
    # print(rc.get_string_not_decode("GA08"))
    # rc.set_string("TempGameNo", "GA08432432")
    # rc.set_string("TempGameNo", "GA08411111")
    # rc.hash_multi_set("TempGameNo", {"GA081": "aaa"})
    # print(rc.hash_get("TempGameNo", "GA08"))
    print(rc.get_string("websocket*"))

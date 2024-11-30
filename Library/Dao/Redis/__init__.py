#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:25
from Library.Dao.Redis.RedisClient import RedisClient


class Redis(RedisClient):
    def __init__(self):
        RedisClient.__init__(self)

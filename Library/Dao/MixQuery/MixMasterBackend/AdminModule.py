#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:38
from Library.Dao.Redis.RedisClient import RedisClient
from Library.Dao.Mysql.ChainQery.Admin import Admin


class AdminModule(object):

    @staticmethod
    def unlock_backend_account(account, site_code='0'):
        """
        后台账号解锁
        :return:
        """
        RedisClient.delete_backend_account_lock_key(account)
        Admin.modify_account_lock_status_sql(site_code, account)

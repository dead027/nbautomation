#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:25
from Library.Common.Utils.Contexts import rds_context
from Library.Common.ServerConnector.Redis import RedisBase


class RedisClient(object):
    @staticmethod
    def delete_backend_account_lock_key(backend_account):
        rds_context.get().delete_key(f'pwd_err_cnt::{backend_account}')

    @staticmethod
    def get_msg_code_rds(site_code, user_account, msg_type='短信'):
        """
        获取手机或邮箱验证码
        @return:
        """
        return 666666
        # rds: RedisBase = rds_context.get()
        # data = rds.connect.keys(f'{site_code}:{key}')
        # # data = rds.connect.keys(f'Vd438R:gameMember:venueList')
        # if data:
        #     for item in data:
        #         item = item.decode()
        #         if "frequency" not in item.split(':')[-1]:
        #             msg = rds.get_string(item)
        #             if msg:
        #                 return msg[-6:]

    @staticmethod
    def reset_msg_code(key):
        rds: RedisBase = rds_context.get()
        data = rds.connect.keys(key)
        rtn_bind = rds.connect.keys(f"phoneVerify::*frequency")
        for item in rtn_bind:
            item = item.decode()
            rds.delete_key(item)





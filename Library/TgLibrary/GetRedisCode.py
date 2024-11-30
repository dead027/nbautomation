#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:25
from Library.Common.Utils.Contexts import rds_context
from Library.Common.ServerConnector.Redis import RedisBase
from Library.Common.Utils.YamlUtil import YamlUtil


class RedisClient(object):
    @staticmethod
    def delete_backend_account_lock_key(backend_account):
        rds_context.get().delete_key(f'pwd_err_cnt::{backend_account}')

    # @staticmethod
    # def get_msg_code(user_account, site_index):
    #     site_code = YamlUtil.get_site_code(site_index)
    #     rds: RedisBase = rds_context.get()
    #     data = rds.connect.keys(f'{site_code}:{user_account}')
    #     result_list = []
    #     if data:
    #         for item in data:
    #             item = item.decode()
    #             if "frequency" not in item.split(':')[-1]:
    #                 msg = rds.get_string(item)
    #                 if msg:
    #                     result_list.append(f"【{item.split(':')[-1]}】: {msg[2:]}")
    #         return "\n".join(result_list) if result_list else "暂无数据，请稍后重试"
    #     else:
    #         return "暂无数据，请稍后重试"

    @staticmethod
    def get_msg_code(site_code, user_account):
        # site_code = YamlUtil.get_site_code(site_index)
        rds: RedisBase = rds_context.get()
        # data = rds.connect.keys(f'{site_code}:{user_account}')
        msg = rds.get_string(f'verify:{site_code}:{user_account}')
        if msg:
            return msg
        else:
            raise AssertionError("暂无数据，请稍后重试")

    # @staticmethod
    # def reset_msg_code(key):
    #     rds: RedisBase = rds_context.get()
    #     data = rds.connect.keys(key)
    #     rtn_bind = rds.connect.keys(f"phoneVerify::*frequency")
    #     for item in rtn_bind:
    #         item = item.decode()
    #         rds.delete_key(item)





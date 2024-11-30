#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:30
from enum import Enum


# 后台账号
class BackendUserEnum(Enum):
    user_status_cn_to_num_dic = {"正常": '1', "登录锁定": '2', "游戏锁定": '3', "充提锁定": '4'}
    user_status_num_to_cn_dic = {value: key for key, value in user_status_cn_to_num_dic.items()}
    # 状态
    account_status_dic = {"正常": 0, "禁用": 1}
    # 锁定状态
    account_lock_status_dic = {"未锁定": 0, "已锁定": 1}
    c = 1
    print(type(user_status_cn_to_num_dic))
    # print(user_status_cn_to_num_dic.items())


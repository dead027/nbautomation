#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/11/5 12:07

class PlatformEnum(object):
    # 业务类型
    business_type_f_zh = {"VIP福利": '1', "活动优惠": '2', "勋章奖励": '3', '平台币转换': '4', "任务": '5'}
    business_type_t_zh = {value: key for key, value in business_type_f_zh.items()}
    # 账变类型
    coin_type_f_zh = {"VIP福利": '1', "活动优惠": '2', "勋章奖励": '3', '平台币转换': '4', "任务": '5'}
    coin_type_t_zh = {value: key for key, value in coin_type_f_zh.items()}
    # 收支类型
    balance_type_f_zh = {"收入": '1', "支出": '2', "冻结": '3', '解冻': '4'}
    balance_type_t_zh = {value: key for key, value in balance_type_f_zh.items()}

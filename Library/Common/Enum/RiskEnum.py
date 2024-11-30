#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/24 16:05
from enum import Enum


class RiskEnum(Enum):
    # 黑名单类型
    risk_type_dic = {"注册IP黑名单": 1, "登录IP黑名单": 2, "注册设备黑名单": 3, "登录设备黑名单": 4}


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/14 14:25
from enum import Enum


class MedalEnum(Enum):
    # 状态
    status_f_zh = {"停用": '0', "启用": "1"}
    status_t_zh = {value: key for key, value in status_f_zh.items()}

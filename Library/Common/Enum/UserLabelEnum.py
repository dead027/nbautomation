#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/14 10:57

from enum import Enum


class UserLabelEnum(Enum):
    # 定制类型
    customize_status_f_zh = {"非定制": '0', "定制": '1'}
    customize_status_t_zh = {value: key for key, value in customize_status_f_zh.items()}
    # 状态
    status_f_zh = {"停用": '0', "启用": "1"}
    status_t_zh = {value: key for key, value in status_f_zh.items()}
    # 记录变更类型
    change_type_f_zh = {"标签名称": '1', "标签描述": '2', "删除": '3'}
    change_type_t_zh = {value: key for key, value in change_type_f_zh.items()}

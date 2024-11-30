#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/13 17:04
from enum import Enum


# 站点
class SiteEnum(Enum):
    # 状态
    status_dic_f_zh = {"启用": 1, "禁用": 0}
    status_dic_t_zh = {value: key for key, value in status_dic_f_zh.items()}
    # 站点模式
    model_dic_f_zh = {"全包": 0, "包风控": 1, "包财务": 2, "不包": 3}
    model_dic_t_zh = {value: key for key, value in model_dic_f_zh.items()}
    # 站点类型
    site_type_dic_f_zh = {"外部": 0, "直营": 1, "测试": 2, "预发": 3}
    site_type_dic_t_zh = {value: key for key, value in site_type_dic_f_zh.items()}


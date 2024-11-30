#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:13
from enum import Enum


class AgentEnum(Enum):
    # 代理类型
    agent_type_dic_f_zh = {"正式": 1, "测试": 2, "合作": 3}
    agent_type_dic_t_zh = {value: key for key, value in agent_type_dic_f_zh.items()}
    # 代理归属
    agent_attribution_dic_f_zh = {"推广": 1, "招商": 2, "官资": 3}
    agent_attribution_dic_t_zh = {value: key for key, value in agent_attribution_dic_f_zh.items()}
    # 代理进阶分类
    agent_category_dic_f_zh = {"常规代理": 1, "流量代理": 2}
    agent_category_dic_t_zh = {value: key for key, value in agent_category_dic_f_zh.items()}
    # 锁单状态
    lock_status_dic_f_zh = {"锁定": 1, "未锁定": 0}
    lock_status_dic_t_zh = {value: key for key, value in lock_status_dic_f_zh.items()}
    # 代理状态
    agent_status_dic_f_zh = {'正常': 1, "登录锁定": 2, "充提锁定": 3}
    agent_status_dic_t_zh = {value: key for key, value in agent_status_dic_f_zh.items()}
    # 代理注册方式
    agent_register_type_dic_f_zh = {'手动': 1, "自动": 2}
    agent_register_type_dic_t_zh = {value: key for key, value in agent_register_type_dic_f_zh.items()}

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/22 17:13

class UserEnum(object):
    # 登录状态
    login_type_dic_f_zh = {"成功": 0, "失败": 1}
    login_type_dic_t_zh = {value: key for key, value in login_type_dic_f_zh.items()}
    # 会员信息变更类型
    change_type_dic_f_zh = {"账号状态": 1, "风控层级": 2, "手机号码": 3, "邮箱": 4, "VIP等级": 5}
    change_type_dic_t_zh = {value: key for key, value in login_type_dic_f_zh.items()}
    # 升降级状态
    vip_level_change_status_f_zh = {"升级": 0, "降级": 1, "保级": 3}
    vip_level_change_status_t_zh = {value: key for key, value in vip_level_change_status_f_zh.items()}
    # 审核操作
    audit_operation_dic_f_zh = {"一审审核": 1, "结单查看": 2}
    audit_operation_dic_t_zh = {value: key for key, value in audit_operation_dic_f_zh.items()}
    # Vip奖励类型
    vip_award_type_dic_f_zh = {"升级礼金": 0, "周流水": 1, "月流水": 2, "周体育流水": 3}
    vip_award_type_dic_t_zh = {value: key for key, value in audit_operation_dic_f_zh.items()}

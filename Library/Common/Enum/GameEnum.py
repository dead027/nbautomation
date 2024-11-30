#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: davis
# datetime: 2024/5/22 12:14
from enum import Enum


class GameEnum(Enum):
    # 游戏平台
    game_platform_f_cn = {"金喜真人": 'SH', "PG平台": 'PG', "金喜彩票": 'ACELT', "UG电子": 'UGSLOT', "沙巴体育": "SBA"}
    game_platform_t_cn = {value: key for key, value in game_platform_f_cn.items()}
    # 账号类型
    account_type_f_cn = {"测试": 1, "正式": 2}
    account_type_t_cn = {value: key for key, value in account_type_f_cn.items()}
    # 注单状态
    order_classify_status_f_cn = {"未结算": 0, "已结算": 1, "已取消": 2, "重结算": 3}
    order_classify_status_t_cn = {value: key for key, value in order_classify_status_f_cn.items()}
    # 通用 0，1，2，4；真人特殊 3，17；彩票电竞5，6，7，8，20，21，电竞9，10；体育电竞拒单：11，12，13，14，15，16
    order_status_f_cn = {"未结算": 0, "已结算": 1, "已取消": 2, "跳局": 3, "重结算": 4, "待开奖": 5, "已中奖": 6, "未中奖": 7,
                         "挂起": 8, "待结算": 9, "彩票撤销": 10, "待处理": 11, "手动取消": 12, "待确认": 13, "风控拒单": 14,
                         "赛事取消": 15, "已确认": 16, "投降": 17, "电竞撤销": 20, "和局": 21}
    order_status_t_cn = {value: key for key, value in order_status_f_cn.items()}
    # 投注终端
    device_type_f_cn = {"PC": 1, "IOS_H5": 2, "IOS_APP": 3, "Android_H5": 4, "Android_APP": 5}
    device_type_t_cn = {value: key for key, value in device_type_f_cn.items()}
    # 游戏状态
    game_status_f_cn = {"开启中": 1, "维护中": 2, "已禁用": 3}
    game_status_t_cn = {value: key for key, value in game_status_f_cn.items()}
    # 变更状态
    change_status_f_cn = {"未变更": 0, "已变更": 1}
    change_status_t_cn = {value: key for key, value in change_status_f_cn.items()}
    # 显示状态
    display_status_f_cn = {"开启中": 1, "已禁用": 0, "维护中": 2}
    display_status_t_cn = {value: key for key, value in display_status_f_cn.items()}
    # 游戏分类
    game_category_dic = {}
    # 模板分类
    game_module_f_cn = {"体育": "PE", "赌场": "CA", "彩票": "LT"}
    game_module_t_cn = {value: key for key, value in game_module_f_cn.items()}
    # 场馆名称
    venue_platform_f_cn = {"PG游戏": 'PG', "视界真人": 'SH', "王牌彩票": 'ACELT', "UG电子": 'UGSLOT', "沙巴体育": "SBA",
                           "吉利电子": "JILI", "TADA电子": "TADA"}
    venue_platform_t_cn = {value: key for key, value in venue_platform_f_cn.items()}
    # 场馆类别
    venue_platform_type_f_cn = {"体育": '1', "视讯": '2', "棋牌": '3', "电子": '4', "彩票": "5",
                           "斗鸡": "6", "电竞": "7"}
    venue_platform_type_t_cn = {value: key for key, value in venue_platform_type_f_cn.items()}

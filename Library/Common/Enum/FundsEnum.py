#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/23 20:17


# 资金
class FundsEnum(object):
    # 锁单状态
    lock_status_dic_f_zh = {"锁定": 1, "未锁定": 0}
    lock_status_reverse_dic_t_zh = {1: "锁定", 0: "未锁定"}
    # 会员人工加额调整类型
    user_manual_adjust_type_dic_f_zh = {"会员存款(后台)": 3, "会员活动": 1, "不存在的调整类型": 999, "会员VIP优惠": 5}
    user_manual_adjust_type_dic_t_zh = {value: key for key, value in user_manual_adjust_type_dic_f_zh.items()}
    # 会员人工减额调整类型
    user_manual_adjust_down_type_dic_f_zh = {"会员提款(后台)": 4, "会员VIP优惠": 5, "不存在的调整类型": 999, "会员活动": 6}
    user_manual_adjust_down_type_dic_t_zh = {value: key for key, value in user_manual_adjust_down_type_dic_f_zh.items()}
    # 会员人工加减额订单状态
    user_manual_order_status_dic_f_zh = {"待处理": 1, "处理中": 2, "审核通过": 3, "审核拒绝": 4}
    user_manual_order_status_dic_t_zh = {value: key for key, value in user_manual_order_status_dic_f_zh.items()}
    # 会员人工调整方向
    adjust_way_dic_f_zh = {"加额": 1, "减额": 2}
    adjust_way_dic_t_zh = {value: key for key, value in adjust_way_dic_f_zh.items()}
    # 账变 - 收支类型
    user_balance_type_dic_f_zh = {"收入": '1', "支出": '2', "冻结": '3', "解冻": '4'}
    user_balance_type_dic_t_zh = {value: key for key, value in user_balance_type_dic_f_zh.items()}
    # 钱包类型
    wallet_type_dic_f_zh = {"中心钱包": 1}
    wallet_type_dic_t_zh = {value: key for key, value in wallet_type_dic_f_zh.items()}
    # 币种
    currency_dic_f_zh = {'美国美元': '0', '中国人民币': '1', '印度卢比': '2', '印尼盾': '3', '巴西雷亚尔': '4',
                         '泰达币': '5', '币安币': '6', '波场币': '7', '以太坊': '8', '比特币': '9'}
    currency_dic_t_zh = {value: key for key, value in currency_dic_f_zh.items()}
    # 币种符号
    currency_symbol_dic_f_zh = {'美国美元': 'USD', '中国人民币': 'CNY', '印度卢比': 'INR', '印尼盾': 'IDR', '巴西雷亚尔': 'BRL',
                                '泰达币': 'USDT', '币安币': 'BNB', '波场币': 'TRX', '以太坊': 'ETH', '比特币': 'BTC'}
    currency_symbol_dic_t_zh = {value: key for key, value in currency_symbol_dic_f_zh.items()}
    # 支付方式
    pay_type_dic_f_zh = {"数字币转账": 'local_virtual_currency', "银行卡转卡": "local_bank_card",
                         "支付宝转账": "local_alipay"}
    pay_type_dic_t_zh = {value: key for key, value in pay_type_dic_f_zh.items()}
    # 代理钱包类型
    agent_wallet_type_dic_f_zh = {"佣金钱包": "1", "额度钱包": "2"}
    agent_wallet_type_dic_t_zh = {value: key for key, value in agent_wallet_type_dic_f_zh.items()}
    # 代理人工调整类型 - 加额
    agent_adjust_way_dic_f_zh = {"代理存款(后台)": '1', "佣金": '2', "返点": '3', "代理活动": '4', "其他调整": '5'}
    agent_adjust_way_dic_t_zh = {value: key for key, value in agent_adjust_way_dic_f_zh.items()}
    # 代理人工调整类型 - 减额
    agent_adjust_way_down_dic_f_zh = {"代理提款(后台)": '1', "佣金": '2', "返点": '3', "代理活动": '4', "其他调整": '5'}
    agent_adjust_way_down_dic_t_zh = {value: key for key, value in agent_adjust_way_down_dic_f_zh.items()}
    # 代理调整类型-加额
    agent_adjust_type_dic_f_zh = {"其他调整": '0', "会员活动": '1', "会员返水": '2', "加额会员存款(后台)": '3',
                                  "加额代客充值": '4', "会员VIP福利": "5", "加额线下红利": '6'}
    agent_adjust_type_dic_t_zh = {value: key for key, value in agent_adjust_type_dic_f_zh.items()}
    # 代理调整类型-减额
    agent_adjust_type_down_dic_f_zh = {"其他调整": '0', "会员活动": '1', "会员返水": '2', "减额其他调整": '3',
                                       "减额会员提款(后台)": '4', "会员VIP福利": "5", "加额线下红利": '6'}
    agent_adjust_type_down_dic_t_zh = {value: key for key, value in agent_adjust_type_down_dic_f_zh.items()}
    # 打码量 调整方式
    typing_adjust_way_dic_f_zh = {"增加": 1, "扣除": 2}
    typing_adjust_way_dic_t_zh = {value: key for key, value in typing_adjust_way_dic_f_zh.items()}
    # 打码量 调整类型
    typing_adjust_type_dic_f_zh = {"人工增加流水": 1, "人工清除流水": 2, "系统自动清除": 3, "投注扣减流水": 4,
                                   "活动增加流水": 5, "充值添加流水": 6, "反水添加流水": 7, "VIP奖励添加流水": 8}
    typing_adjust_type_dic_t_zh = {value: key for key, value in typing_adjust_type_dic_f_zh.items()}
    # 会员客户端存取款审核状态
    deposit_withdraw_status_f_zh = {"待一审": 1, "一审审核": 2, "一审拒绝": 3, "待二审": 4, "二审审核": 5, "二审拒绝": 6,
                                    "待三审": 7, "三审审核": 8, "三审拒绝": 9, "待出款": 10, "待处理": 20, "处理中": 21,
                                    "已关闭": 90, "出款失败": 96, "出款取消": 97, "取消订单(申请人)": 98, "失败": 100,
                                    "成功": 101}
    deposit_withdraw_status_t_zh = {value: key for key, value in deposit_withdraw_status_f_zh.items()}
    # 会员人工存取款审核状态
    manual_deposit_withdraw_status_f_zh = {"待一审": 0, "一审审核": 1, "一审拒绝": 2, "待二审": 3, "二审审核": 4, "二审拒绝": 5,
                                           "审核通过": 6}
    manual_deposit_withdraw_status_t_zh = {value: key for key, value in manual_deposit_withdraw_status_f_zh.items()}

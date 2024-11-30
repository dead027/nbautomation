#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/29 11:58

from sqlalchemy import func
from decimal import Decimal
from collections import defaultdict
from Library.Dao import Dao
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil


class Report(object):
    """
    报表相关
    """

    @staticmethod
    def _calc_used_profit(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        计算已使用优惠 - 已按代理叠加，手动转换 + 自动获取 的主货币
        @return: {"agent_account": {"活动优惠": Decimal(0), "VIP福利": Decimal(0)}}
        """
        used_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
                                                             date_type).subquery()
        used_profit_data = ms_context.get().session.query(used_data.c.date, used_data.c.user_account,
                                                          used_data.c.agent_account,
                                                          used_data.c.currency,
                                                          func.sum(used_data.c.amount).label('amount')). \
            group_by(used_data.c.date, used_data.c.user_account, used_data.c.agent_account, used_data.c.currency)
        return used_profit_data

    # @staticmethod
    # def _calc_received_vip_act_discount(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
    #     """
    #     领取到的主货币部分的 VIP + 活动优惠
    #     @return:
    #     """
    #     data = Dao.get_vip_act_discount_data_base(site_code, start_diff, end_diff, stop_diff, date_type).subquery()
    #     data = ms_context.get().session.query(data.c.date, data.c.user_account, data.c.agent_name, data.c.currency,
    #                                           func.sum(data.c.amount).label("amount")). \
    #         group_by(data.c.date, data.c.user_account, data.c.agent_name, data.c.currency)
    #     return data

    @staticmethod
    def calc_used_profit_detail_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        计算已使用优惠,详情 - 已按代理叠加，包括： 手动转换的主货币 + 领取时直接发的主货币
        @return:
        """
        data = Report._calc_used_profit(site_code, start_diff, end_diff, stop_diff, date_type).all()

        used_profit_dic = defaultdict(Decimal)
        # data_1 = Report._calc_used_profit(site_code, start_diff, end_diff, stop_diff, date_type).all()
        # data_2 = Report._calc_received_vip_act_discount(site_code, start_diff, end_diff, stop_diff, date_type).all()
        for _ in data:
            used_profit_dic[(_[0], _[1], _[3], _[2])] += _[4]
        # for _ in data_2:
        #     used_profit_dic[(_[0], _[1], _[3], _[2])] += _[4]
        return used_profit_dic

    @staticmethod
    def calc_used_profit_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        计算已使用优惠,外层统计 - 已按代理叠加，包括： 手动转换的主货币 + 领取时直接发的主货币
        @return:
        """
        used_profit_dic = defaultdict(Decimal)
        # 手动转换的主货币 + 领取时直接发的主货币
        data_1 = Report._calc_used_profit(site_code, start_diff, end_diff, stop_diff, date_type).subquery()
        data_1 = ms_context.get().session.query(data_1.c.user_account, data_1.c.agent_account, data_1.c.currency,
                                                func.sum(data_1.c.amount).label("amount")).\
            group_by(data_1.c.user_account, data_1.c.agent_account, data_1.c.currency).all()
        # # 领取时直接发的主货币
        # data_2 = Report._calc_received_vip_act_discount(site_code, start_diff, end_diff, stop_diff, date_type).\
        #     subquery()
        # data_2 = ms_context.get().session.query(data_2.c.user_account, data_2.c.agent_name, data_2.c.currency,
        #                                         func.sum(data_2.c.amount).label("amount")).\
        #     group_by(data_2.c.user_account, data_2.c.agent_name, data_2.c.currency).all()
        for _ in data_1:
            used_profit_dic[(_[0], _[1])] += _[3]
        # for _ in data_2:
        #     used_profit_dic[(_[0], _[1])] += _[3]
        return used_profit_dic

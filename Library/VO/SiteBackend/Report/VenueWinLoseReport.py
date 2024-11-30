#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/1 10:55
from decimal import Decimal
from collections import defaultdict
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.medal_info_model import MedalInfo
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.Common.Enum.UserLabelEnum import UserLabelEnum
from Library.MysqlTableModel.medal_reward_config_model import MedalRewardConfig
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Enum.MedalEnum import MedalEnum

from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func


class VenueWinLoseReport(object):
    """
    场馆盈亏报表
    """

    @staticmethod
    def get_venue_report_detail_vo(site_code, venue_name=None, start_diff=0, end_diff=0, currency=None,
                                   stop_diff=0, date_type='日', to_site_coin=False):
        """
        场馆盈亏报表，详情
        @return: {场馆类型: {日期:data}}
        """
        venue_info = Dao.get_venue_info_sql()
        venue_dic = {_.venue_code: _.venue_name for _ in venue_info}
        data = Dao.get_game_report_base(site_code, start_diff, end_diff, date_type, stop_diff, currency=currency). \
            subquery()
        data = ms_context.get().session.query(data.c.venue_code, data.c.currency, data.c.user_account, data.c.date,
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.venue_code, data.c.currency, data.c.user_account, data.c.date).subquery()
        data = ms_context.get().session.query(data.c.venue_code, data.c.currency, data.c.date,
                                              func.count(1).label("user_cnt"),
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.venue_code, data.c.currency, data.c.date).all()
        currency_info = Dao.get_currency_dic(to_zh=True)
        currency_rate = Dao.currency_rate(site_code)
        result_dic = defaultdict(list)
        for item in data:
            rate = currency_rate[item[1]]
            sub_data = {"日期": item[2], "币种": currency_info[item[1]], "投注人数": item[3], "注单量": item[4],
                        "投注金额": round(item[5] / rate, 2) if to_site_coin else item[5],
                        "有效投注": round(item[6] / rate, 2) if to_site_coin else item[6],
                        "投注盈亏": round(item[7] / rate, 2) if to_site_coin else item[7]}
            result_dic[venue_dic[item[0]]].append(sub_data)
        return result_dic if not venue_name else result_dic[venue_name]

    @staticmethod
    def get_venue_report_vo(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=0, date_type='日',
                            to_site_coin=False):
        """
        场馆盈亏报表，外层    - 会员角度
        @return: {场馆类型: {日期:data}}
        """
        venue_dic = Dao.get_venue_code_param(to_zh=True)
        data = Dao.get_venue_win_lose_data_dao(site_code, start_diff, end_diff, currency, stop_diff, date_type)
        # currency_info = Dao.get_currency_dic(to_zh=True)
        currency_rate = Dao.currency_rate(site_code)
        result_list = []
        for item in data:
            if item[1] not in currency_rate:
                continue
            rate = currency_rate[item[1]]
            sub_data = {"场馆": venue_dic[item[0]], "主币种": item[1], "投注人数": item[2], "注单量": item[3],
                        "投注金额": round(item[4] / rate, 2) if to_site_coin else item[4],
                        "有效投注": round(item[5] / rate, 2) if to_site_coin else item[5],
                        "平台输赢": round(item[6] / rate, 2) if to_site_coin else item[6]}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_venue_report_total_vo(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=0, date_type='日',
                                  to_site_coin=False):
        """
        场馆盈亏报表, 统计，外层    - 会员角度
        @return: {场馆类型: {日期:data}}
        """
        currency_rate = Dao.currency_rate(site_code)
        data = Dao.query_order_data_sql(site_code, settle_start_diff=start_diff, settle_end_diff=end_diff,
                                        date_type=date_type, stop_diff=stop_diff, currency=currency).subquery()

        data = ms_context.get().session.query(data.c.user_account, data.c.currency, func.count(1).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(-data.c.win_loss_amount).label("win_lose_amount")). \
            group_by(data.c.user_account, data.c.currency).subquery()
        if not to_site_coin:
            data = ms_context.get().session.query(func.sum(1), func.sum(data.c.bet_cnt),
                                                  func.sum(data.c.bet_amount),
                                                  func.sum(data.c.valid_amount), func.sum(data.c.win_lose_amount)).\
                first()
            total_dic = {"投注人数": data[0], "注单量": data[1], "投注金额": data[2], "有效投注": data[3],
                         "平台输赢": data[4]}
        else:
            data = ms_context.get().session.query(data.c.currency, func.sum(1), func.sum(data.c.bet_cnt),
                                                  func.sum(data.c.bet_amount),
                                                  func.sum(data.c.valid_amount), func.sum(data.c.win_lose_amount)).\
                group_by(data.c.currency).all()
            total_dic = {"投注人数": 0, "注单量": 0, "投注金额": Decimal(0), "有效投注": Decimal(0), "平台输赢": Decimal(0)}
            for _ in data:
                total_dic["投注人数"] += _[1]
                total_dic["注单量"] += _[2]
                total_dic["投注金额"] += round(_[3] / currency_rate[_[0]], 2)
                total_dic["有效投注"] += round(_[4] / currency_rate[_[0]], 2)
                total_dic["平台输赢"] += round(_[5] / currency_rate[_[0]], 2)
        return total_dic

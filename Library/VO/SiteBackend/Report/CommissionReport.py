#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/30 11:21
from collections import defaultdict
from Library.Common.Utils.Contexts import *

from Library.Dao import Dao
from sqlalchemy.sql.functions import func


class CommissionReport(object):
    """
    佣金发放记录表
    """

    @staticmethod
    def get_commission_report_vo(site_code, venue_name=None, start_diff=0, end_diff=0, currency=None,
                                 stop_diff=0, date_type='日', to_site_coin=False):
        """
        游戏报表，详情 - 按场馆分组
        @return: {场馆类型: 场馆数据}
        """
        venue_info = Dao.get_venue_info_sql()
        venue_dic = {_.venue_code: _.venue_name for _ in venue_info}
        data = Dao.get_game_report_base(site_code, start_diff, end_diff, date_type, stop_diff, currency=currency). \
            subquery()
        data = ms_context.get().session.query(data.c.venue_type, data.c.venue_code, data.c.currency,
                                              data.c.game_name, data.c.user_account,
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.game_name, data.c.user_account). \
            subquery()
        data = ms_context.get().session.query(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.game_name,
                                              func.count(1).label("user_cnt"),
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.game_name).all()
        currency_info = Dao.get_currency_dic(to_zh=True)
        currency_rate = Dao.currency_rate(site_code)
        result_dic = defaultdict(list)
        for item in data:
            if item[2] not in currency_rate:
                continue
            rate = currency_rate[item[2]]
            sub_data = {"游戏名": item[3], "游戏场馆": venue_dic[item[1]], "币种": currency_info[item[2]],
                        "投注人数": item[4], "注单量": item[5],
                        "投注金额": round(item[6] / rate, 2) if to_site_coin else item[6],
                        "有效投注": round(item[7] / rate, 2) if to_site_coin else item[7],
                        "平台输赢": round(item[8] / rate, 2) if to_site_coin else item[8]}
            result_dic[venue_dic[item[1]]].append(sub_data)
        return result_dic if not venue_name else result_dic[venue_name]

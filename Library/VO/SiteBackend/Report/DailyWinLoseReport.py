#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:35
from collections import defaultdict
from decimal import Decimal
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.site_info_model import SiteInfo

from Library.Dao import Dao
from sqlalchemy.sql.functions import func


class DailyWinLoseReport(object):
    """
    每日盈亏报表
    """

    @staticmethod
    def get_daily_report_vo(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=None, to_site_coin=False,
                            date_type='日'):
        """
        每日盈亏报表
        @return:
        """
        # site_info: SiteInfo = Dao.get_site_info_sql(site_code=site_code)[0]
        currency_rate = Dao.currency_rate(site_code)
        # 1.投注数据
        bet_data = Dao.get_user_bet_summary_by_user_sql(site_code, start_diff=start_diff, end_diff=end_diff,
                                                        stop_diff=stop_diff, date_type=date_type, currency=currency). \
            subquery()
        # 先合并代理数据
        bet_data = ms_context.get().session.query(bet_data.c.date, bet_data.c.currency, bet_data.c.user_account,
                                                  func.sum(bet_data.c.win_loss_amount).label("win_loss_amount"),
                                                  func.sum(bet_data.c.bet_amount).label("bet_amount"),
                                                  func.sum(bet_data.c.valid_amount).label("valid_amount"),
                                                  func.sum(bet_data.c.order_amount).label("order_amount")). \
            group_by(bet_data.c.date, bet_data.c.currency, bet_data.c.user_account).subquery()
        # 合并会员数据
        bet_data = ms_context.get().session.query(bet_data.c.date, bet_data.c.currency, func.count(1).label('user_cnt'),
                                                  func.sum(bet_data.c.win_loss_amount).label("win_loss_amount"),
                                                  func.sum(bet_data.c.bet_amount).label("bet_amount"),
                                                  func.sum(bet_data.c.valid_amount).label("valid_amount"),
                                                  func.sum(bet_data.c.order_amount).label("order_amount")). \
            group_by(bet_data.c.date, bet_data.c.currency).all()
        bet_dic = defaultdict(dict)
        [bet_dic.__setitem__((_[0], _[1]), _) for _ in bet_data]

        # 2.其他调整
        adjust_data = Dao.get_user_io_summary_data_base(site_code, start_diff=start_diff, end_diff=end_diff,
                                                        currency=currency, stop_diff=stop_diff, date_type='日'). \
            subquery()

        adjust_data = ms_context.get().session.query(adjust_data.c.date, adjust_data.c.currency,
                                                     func.sum(adjust_data.c.other_adjust).label("other_adjust")). \
            group_by(adjust_data.c.date, adjust_data.c.currency).all()
        adjust_dic = defaultdict(Decimal)
        [adjust_dic.__setitem__((_[0], _[1]), _[2]) for _ in adjust_data if _[2]]

        # 3.已使用优惠
        used_profit_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
                                                                    date_type, currency).subquery()
        used_profit_data = ms_context.get().session.query(used_profit_data.c.date, used_profit_data.c.currency,
                                                          func.sum(used_profit_data.c.amount)). \
            group_by(used_profit_data.c.date, used_profit_data.c.currency).all()
        used_profit_dic = defaultdict(Decimal)
        [used_profit_dic.__setitem__((_[0], _[1]), _[2]) for _ in used_profit_data]

        # 4.VIP福利和活动优惠
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff,
                                                               date_type, currency).subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.date, vip_act_data.c.main_currency,
                                                      func.sum(vip_act_data.c.vip), func.sum(vip_act_data.c.act)). \
            group_by(vip_act_data.c.date, vip_act_data.c.main_currency).all()
        vip_dic = defaultdict(Decimal)
        act_dic = defaultdict(Decimal)
        [vip_dic.__setitem__((_[0], _[1]), _[2]) for _ in vip_act_data]
        [act_dic.__setitem__((_[0], _[1]), _[3]) for _ in vip_act_data]

        data_list = []
        for key in list(set(list(bet_dic.keys()) + list(adjust_dic.keys()) + list(used_profit_dic.keys()) +
                            list(vip_dic.keys()) + list(act_dic.keys()))):
            date, main_currency = key
            if main_currency not in currency_rate:
                continue
            rate = currency_rate[main_currency]
            bet_data_dic = bet_dic[key]
            used_amount = used_profit_dic[key]

            win_lose_amount = bet_data_dic[3] if bet_data_dic else 0
            adjust_amount = adjust_dic[key]
            vip_amount = vip_dic[key]
            activity_amount = act_dic[key]
            # 净盈利=平台输赢-已使用优惠
            net_profit_amount = -win_lose_amount - used_amount
            bet_amount = bet_data_dic[4] if bet_data_dic else 0
            valid_amount = bet_data_dic[5] if bet_data_dic else 0

            sub_data = {"日期": date, "主币种": main_currency,
                        "VIP福利": vip_amount,
                        "活动优惠": activity_amount,
                        "其他调整": round(adjust_amount / rate, 2) if to_site_coin else adjust_amount,
                        "投注人数": bet_data_dic[2] if bet_data_dic else 0,
                        "注单量": bet_data_dic[6] if bet_data_dic else 0,
                        "投注金额": round(bet_amount / rate, 2) if to_site_coin else bet_amount,
                        "有效投注": round(valid_amount / rate, 2) if to_site_coin else valid_amount,
                        "会员输赢": round(win_lose_amount / rate, 2) if to_site_coin else win_lose_amount,
                        "净盈利": round(net_profit_amount / rate, 2) if to_site_coin else net_profit_amount,
                        "已使用优惠": round(used_amount / rate, 2) if to_site_coin else used_amount}
            data_list.append(sub_data)
        return data_list

    @staticmethod
    def get_daily_report_total_vo(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=None,
                                  to_site_coin=False, date_type='日'):
        """
        每日盈亏报表 - 汇总数据
        @return:
        """
        data = DailyWinLoseReport.get_daily_report_vo(site_code, start_diff, end_diff, currency, stop_diff,
                                                      to_site_coin, date_type)
        total_dic = {"VIP福利": Decimal(0), "活动优惠": Decimal(0), "已使用优惠": Decimal(0), "其他调整": Decimal(0),
                     "投注人数": Decimal(0), "注单量": Decimal(0), "投注金额": Decimal(0), "有效投注": Decimal(0),
                     "会员输赢": Decimal(0), "净盈利": Decimal(0)}
        for _ in data:
            for key in total_dic:
                total_dic[key] += _[key]
        return total_dic

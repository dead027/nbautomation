#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/30 11:21
from Library.Common.Utils.Contexts import *
from collections import defaultdict
from decimal import Decimal

from Library.Dao import Dao
from sqlalchemy.sql.functions import func


class UserIoReport(object):
    @staticmethod
    def get_user_io_report_vo(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=0, date_type='月',
                              to_site_coin=False, user_account=None):
        """
        会员存取报表
        @return:
        """
        data = Dao.get_user_io_summary_data_base(site_code, start_diff=start_diff, end_diff=end_diff,
                                                 currency=currency, stop_diff=stop_diff, date_type=date_type,
                                                 user_account=user_account).subquery()
        data = ms_context.get().session.query(data.c.date, data.c.currency, data.c.user_account,
                                              func.sum(data.c.deposit_amount).label("deposit_amount"),
                                              func.sum(data.c.deposit_cnt).label("deposit_cnt"),
                                              func.sum(data.c.transfer_amount).label("transfer_amount"),
                                              func.sum(data.c.transfer_cnt).label("transfer_cnt"),
                                              func.sum(data.c.withdraw_amount).label("withdraw_amount"),
                                              func.sum(data.c.withdraw_cnt).label("withdraw_cnt"),
                                              func.sum(data.c.io_diff).label("io_diff"),
                                              func.sum(data.c.vip_amount).label("vip_amount"),
                                              func.sum(data.c.activity_amount).label("activity_amount"),
                                              func.sum(data.c.adjust_amount).label("adjust_amount"),
                                              func.sum(data.c.other_adjust).label("other_adjust"), ). \
            group_by(data.c.date, data.c.currency, data.c.user_account).subquery()
        data = ms_context.get().session.query(data.c.date, data.c.currency,
                                              func.sum(func.if_(data.c.deposit_cnt > 0, 1, 0)).label("存款人数"),
                                              func.sum(data.c.deposit_cnt).label("存款次数"),
                                              func.sum(data.c.deposit_amount).label("存款总额"),
                                              func.sum(func.if_(data.c.withdraw_cnt > 0, 1, 0)).label("取款人数"),
                                              func.sum(data.c.withdraw_cnt).label("取款次数"),
                                              func.sum(data.c.withdraw_amount).label("取款总额"),
                                              func.sum(data.c.io_diff).label("存取差")). \
            group_by(data.c.date, data.c.currency).all()
        # 大额数据
        big = Dao.get_user_big_io_data_base(site_code, user_account, start_diff, end_diff, currency,
                                            stop_diff=stop_diff, date_type=date_type).subquery()
        big = ms_context.get().session.query(big.c.date, big.c.user_account, big.c.currency_code,
                                             func.sum(big.c.big_cnt).label("big_cnt"),
                                             func.sum(big.c.big_amount).label("big_amount")). \
            group_by(big.c.date, big.c.user_account, big.c.currency_code).subquery()
        big = ms_context.get().session.query(big.c.date, big.c.currency_code, func.sum(1),
                                             func.sum(big.c.big_cnt), func.sum(big.c.big_amount)). \
            group_by(big.c.date, big.c.user_account, big.c.currency_code).all()
        result_dic = defaultdict(lambda: {"日期": "", "主币种": "", "存款人数": 0, "存款次数": 0,
                                          "存款总额": Decimal(0), "取款人数": 0, "取款次数": 0, "取款总额": Decimal(0),
                                          "大额取款人数": 0, "大额取款次数": 0, "大额取款金额": Decimal(0), "存取差": Decimal(0)})
        currency_rate = Dao.currency_rate(site_code)
        for item in data:
            if item[1] not in currency_rate:
                continue
            if not list(filter(lambda _: _ != 0, item[2:])):
                continue
            rate = currency_rate[item[1]]
            result_dic[(item[0], item[1])]["日期"] = item[0]
            result_dic[(item[0], item[1])]["主币种"] = item[1]
            result_dic[(item[0], item[1])]["存款人数"] = item[2]
            result_dic[(item[0], item[1])]["存款次数"] = item[3]
            result_dic[(item[0], item[1])]["存款总额"] = round(item[4] / rate, 2) if to_site_coin else item[4]
            result_dic[(item[0], item[1])]["取款人数"] = item[5]
            result_dic[(item[0], item[1])]["取款次数"] = item[6]
            result_dic[(item[0], item[1])]["取款总额"] = round(item[7] / rate, 2) if to_site_coin else item[7]
            result_dic[(item[0], item[1])]["存取差"] = round(item[8] / rate, 2) if to_site_coin else item[8]
        for _ in big:
            if _[1] not in currency_rate:
                continue
            rate = currency_rate[_[1]]
            result_dic[(_[0], _[1])]["大额取款人数"] = _[2]
            result_dic[(_[0], _[1])]["大额取款次数"] = _[3]
            result_dic[(_[0], _[1])]["大额取款金额"] = round(_[4] / rate, 2) if to_site_coin else _[4]

        return result_dic

    @staticmethod
    def get_user_io_report_total_vo(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=0, date_type='月',
                                    to_site_coin=False, user_account=None):
        """
        会员存取报表 - 总计
        @return:
        """
        data = Dao.get_user_io_summary_data_base(site_code, start_diff=start_diff, end_diff=end_diff,
                                                 currency=currency, stop_diff=stop_diff, date_type=date_type,
                                                 user_account=user_account).subquery()
        data = ms_context.get().session.query(data.c.currency, data.c.user_account,
                                              func.sum(data.c.deposit_amount).label("deposit_amount"),
                                              func.sum(data.c.deposit_cnt).label("deposit_cnt"),
                                              func.sum(data.c.transfer_amount).label("transfer_amount"),
                                              func.sum(data.c.transfer_cnt).label("transfer_cnt"),
                                              func.sum(data.c.withdraw_amount).label("withdraw_amount"),
                                              func.sum(data.c.withdraw_cnt).label("withdraw_cnt"),
                                              func.sum(data.c.io_diff).label("io_diff"),
                                              func.sum(data.c.vip_amount).label("vip_amount"),
                                              func.sum(data.c.activity_amount).label("activity_amount"),
                                              func.sum(data.c.adjust_amount).label("adjust_amount"),
                                              func.sum(data.c.other_adjust).label("other_adjust"), ). \
            group_by(data.c.currency, data.c.user_account).subquery()
        big = Dao.get_user_big_io_data_base(site_code, user_account, start_diff, end_diff, currency,
                                            stop_diff=stop_diff, date_type=date_type).subquery()
        result = {"存款人数": 0, "存款次数": 0, "存款总额": Decimal(0), "取款人数": 0, "取款次数": 0, "取款总额": Decimal(0),
                  "大额取款人数": 0, "大额取款次数": 0, "大额取款金额": Decimal(0), "存取差": Decimal(0)}

        if to_site_coin:

            data = ms_context.get().session.query(data.c.currency,
                                                  func.sum(func.if_(data.c.deposit_cnt > 0, 1, 0)).label("存款人数"),
                                                  func.sum(data.c.deposit_cnt).label("存款次数"),
                                                  func.sum(data.c.deposit_amount).label("存款总额"),
                                                  func.sum(func.if_(data.c.withdraw_cnt > 0, 1, 0)).label("取款人数"),
                                                  func.sum(data.c.withdraw_cnt).label("取款次数"),
                                                  func.sum(data.c.withdraw_amount).label("取款总额"),
                                                  func.sum(data.c.io_diff).label("存取差")). \
                group_by(data.c.currency).all()
            # 大额数据
            big = ms_context.get().session.query(big.c.user_account, big.c.currency_code,
                                                 func.sum(big.c.big_cnt).label("big_cnt"),
                                                 func.sum(big.c.big_amount).label("big_amount")). \
                group_by(big.c.user_account, big.c.currency_code).subquery()
            big = ms_context.get().session.query(big.c.currency_code, func.sum(1),
                                                 func.sum(big.c.big_cnt), func.sum(big.c.big_amount)). \
                group_by(big.c.user_account, big.c.currency_code).all()
            currency_rate = Dao.currency_rate(site_code)

            for _ in data:
                rate = currency_rate[_[0]]
                result["存款人数"] += _[1]
                result["存款次数"] += _[2]
                result["存款总额"] += _[3] / rate if to_site_coin else _[3]
                result["取款人数"] += _[4]
                result["取款次数"] += _[5]
                result["取款总额"] += _[6] / rate if to_site_coin else _[6]
                result["存取差"] += _[7] / rate if to_site_coin else _[7]
            for _ in big:
                rate = currency_rate[_[0]]
                result["大额取款人数"] += _[1]
                result["大额取款次数"] += _[2]
                result["大额取款金额"] += _[3] / rate if to_site_coin else _[3]
            for _ in result:
                result[_] = round(result[_], 2)
        else:
            data = ms_context.get().session.query(func.sum(func.if_(data.c.deposit_cnt > 0, 1, 0)).label("存款人数"),
                                                  func.sum(data.c.deposit_cnt).label("存款次数"),
                                                  func.sum(data.c.deposit_amount).label("存款总额"),
                                                  func.sum(func.if_(data.c.withdraw_cnt > 0, 1, 0)).label("取款人数"),
                                                  func.sum(data.c.withdraw_cnt).label("取款次数"),
                                                  func.sum(data.c.withdraw_amount).label("取款总额"),
                                                  func.sum(data.c.io_diff).label("存取差")).all()
            # 大额数据
            big = ms_context.get().session.query(big.c.user_account, func.sum(big.c.big_cnt).label("big_cnt"),
                                                 func.sum(big.c.big_amount).label("big_amount")). \
                group_by(big.c.user_account).subquery()
            big = ms_context.get().session.query(func.sum(1), func.sum(big.c.big_cnt), func.sum(big.c.big_amount)).all()
            if data:
                data = data[0]
                result["存款人数"] = data[0]
                result["存款次数"] = data[1]
                result["存款总额"] = data[2]
                result["取款人数"] = data[3]
                result["取款次数"] = data[4]
                result["取款总额"] = data[5]
                result["存取差"] = data[6]
            if big:
                big = big[0]
                result["大额取款人数"] = big[0]
                result["大额取款次数"] = big[1]
                result["大额取款金额"] = big[2]
        return result

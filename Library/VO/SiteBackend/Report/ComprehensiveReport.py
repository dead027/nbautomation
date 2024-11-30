#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/8 18:08

from Library.Dao import Dao
from Library.BO import BO
from sqlalchemy.orm.session import Session
from Library.Common.Utils.Contexts import *
from sqlalchemy.sql.functions import func
from Library.VO.SiteBackend.Report.DailyWinLoseReport import DailyWinLoseReport
from Library.MysqlTableModel.user_registration_info_model import UserRegistrationInfo
from Library.VO.SiteBackend.Report.UserIoReport import UserIoReport
from decimal import Decimal
from Library.MysqlTableModel.user_coin_record_model import UserCoinRecord
from Library.Common.Utils.DateUtil import DateUtil
from Library.Dao.Mysql.ChainQery.SiteBackend.User import UserInfo
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo

from collections import defaultdict


class ComprehensiveReport(object):
    """
    活动报表
    """

    @staticmethod
    def _user_register_summary(site_code, currency=None, start_diff=0, end_diff=0, grep_has_agent=False):
        """
        综合报表 - 会员注册人数
        @return:
        """
        data = Dao.get_registration_info_sql(site_code, register_start_diff=start_diff, register_end_diff=end_diff,
                                             currency=currency, grep_has_agent=grep_has_agent).subquery()
        data = ms_context.get().session.query(data.c.date, data.c.main_currency, data.c.register_terminal,
                                              func.sum(1)). \
            group_by(data.c.date, data.c.main_currency, data.c.register_terminal).all()
        terminal_dic = Dao.get_user_register_client(to_zh=True)
        return [(_[0], str(_[1]), terminal_dic[int(_[2])], _[3]) for _ in data]

    @staticmethod
    def _user_first_deposit_summary(site_code, currency=None, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                                    to_site_coin=False):
        """
        综合报表 - 会员首存
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session.query(func.date_format(func.convert_tz(func.from_unixtime(
            UserInfo.first_deposit_time / 1000), '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                              UserInfo.main_currency, func.sum(1).label("cnt"),
                                              func.sum(UserInfo.first_deposit_amount)). \
            filter(UserInfo.site_code == site_code, UserInfo.first_deposit_time.between(_start, _end))
        if currency:
            data = data.filter(UserInfo.main_currency == Dao.get_currency_dic(currency))
        data = data.group_by(UserInfo.main_currency, "date").all()
        # currency_dic = Dao.get_currency_dic(to_zh=True)

        currency_rate = Dao.currency_rate(site_code)
        result = []
        for _ in data:
            rate = currency_rate[_[1]]
            amount = round(_[3] / rate, 2) if to_site_coin else _[3]
            result.append((_[0], _[1], _[2], amount))
        return result

    @staticmethod
    def _user_login_summary(site_code, currency=None, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        综合报表 - 会员登录统计
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session.query(func.date_format(func.convert_tz(func.from_unixtime(
            UserLoginInfo.login_time / 1000), '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                              UserInfo.main_currency, UserLoginInfo.user_account,
                                              UserLoginInfo.login_terminal). \
            join(UserInfo, UserInfo.user_account == UserLoginInfo.user_account). \
            filter(UserInfo.site_code == site_code, UserLoginInfo.login_time.between(_start, _end))
        if currency:
            data = data.filter(UserInfo.main_currency == Dao.get_currency_dic(currency))
        data = data.group_by(UserInfo.main_currency, UserLoginInfo.user_account, UserLoginInfo.login_terminal, "date"). \
            subquery()
        data = ms_context.get().session.query(data.c.date, data.c.main_currency, data.c.login_terminal, func.count(1)). \
            group_by(data.c.date, data.c.main_currency, data.c.login_terminal)

        terminal_dic = Dao.get_user_register_client(to_zh=True)
        return [(_[0], _[1], terminal_dic[int(_[2])], _[3]) for _ in data]

    @staticmethod
    def _user_bet_summary(site_code, currency=None, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                          to_site_coin=False):
        """
        综合报表 - 会员投注统计
        @return:
        """
        data = Dao.get_game_report_base(site_code, start_diff, end_diff, date_type, stop_diff, currency).subquery()
        data = ms_context.get().session.query(data.c.date, data.c.currency, data.c.user_account,
                                              func.sum(data.c.bet_amount).label('bet_amount'),
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.date, data.c.currency, data.c.user_account).subquery()
        data = ms_context.get().session.query(data.c.date, data.c.currency, func.count(1).label("user_cnt"),
                                              func.sum(data.c.bet_amount).label('bet_amount'),
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.date, data.c.currency)

        # currency_dic = Dao.get_currency_dic(to_zh=True)
        result = []
        currency_rate = Dao.currency_rate(site_code)
        for _ in data:
            rate = currency_rate[_[1]]
            bet_amount = round(_[3] / rate, 2) if to_site_coin else _[3]
            valid_amount = round(_[5] / rate, 2) if to_site_coin else _[5]
            win_lose_amount = round(_[6] / rate, 2) if to_site_coin else _[6]
            result.append((_[0], _[1], _[2], bet_amount, _[4], valid_amount, win_lose_amount))

        return result

    @staticmethod
    def get_comprehensive_report_vo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日', currency=None,
                                    to_site_coin=False):
        """
        获取综合报表
        @return:
        """
        io_type = Dao.get_coin_record_io_type()
        result_dic = defaultdict(lambda: {"日期": None, "币种": None,
                                          "会员注册人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                                              "IOS_APP", "IOS_H5"], [0 for _ in range(7)])),
                                          "会员登录人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                                              "IOS_APP", "IOS_H5"], [0 for _ in range(7)])),
                                          "会员总存款": {"总额": 0, "存款人数": 0, "存款次数": 0},
                                          "会员总取款": {"总额": 0, "取款人数": 0, "取款次数": 0, "大额取款人数": 0,
                                                    "大额取款次数": 0},
                                          "会员存取差": 0, "会员首存": {"总额": 0, "首存人数": 0},
                                          "会员投注": dict(zip(["投注金额", "有效投注", "投注人数", "注单量"],
                                                           [0 for _ in range(4)])),
                                          "会员输赢": 0, "会员VIP福利": {"总额": 0, "人数": 0},
                                          "会员活动优惠": {"总额": 0, "人数": 0},
                                          "已使用优惠": 0,
                                          "会员调整": {"总额": 0, "加额": 0, "加额人数": 0, "减额": 0, "减额人数": 0},
                                          "代理下注册人数": dict(
                                              zip(["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP", "IOS_H5"],
                                                  [0 for _ in range(7)])),
                                          "代存会员": {"人数": 0, "次数": 0, "额度": 0}
                                          })
        # 会员注册人数
        data_1 = ComprehensiveReport._user_register_summary(site_code, currency, start_diff, end_diff)
        for _ in data_1:
            result_dic[(_[0], _[1])]["会员注册人数"]["总数"] += _[3]
            result_dic[(_[0], _[1])]["会员注册人数"][_[2]] += _[3]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 会员登录人数
        data_2 = ComprehensiveReport._user_login_summary(site_code, currency, start_diff, end_diff, stop_diff,
                                                         date_type)
        for _ in data_2:
            result_dic[(_[0], _[1])]["会员登录人数"]["总数"] += _[3]
            result_dic[(_[0], _[1])]["会员登录人数"][_[2]] += _[3]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 会员首存
        data_3 = ComprehensiveReport._user_first_deposit_summary(site_code, currency, start_diff, end_diff,
                                                                 stop_diff, date_type, to_site_coin)
        for _ in data_3:
            result_dic[(_[0], _[1])]["会员首存"]["总额"] += _[3]
            result_dic[(_[0], _[1])]["会员首存"]["首存人数"] += _[2]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 会员总存款、会员总取款、会员存取差
        data_4 = Dao.get_user_io_summary_data_base(site_code, currency=currency, start_diff=start_diff,
                                                   end_diff=end_diff, stop_diff=stop_diff, date_type=date_type). \
            subquery()
        data_4 = ms_context.get().session.query(data_4.c.date, data_4.c.currency, data_4.c.user_account,
                                                func.sum(data_4.c.deposit_amount + data_4.c.transfer_amount).label(
                                                    "deposit_amount"),
                                                func.sum(data_4.c.deposit_cnt + data_4.c.transfer_cnt).label(
                                                    "deposit_cnt"),
                                                func.sum(data_4.c.withdraw_amount).label("withdraw_amount"),
                                                func.sum(data_4.c.withdraw_cnt).label("withdraw_cnt")). \
            group_by(data_4.c.date, data_4.c.currency, data_4.c.user_account).subquery()
        data_4 = ms_context.get().session.query(data_4.c.date, data_4.c.currency,
                                                func.sum(data_4.c.deposit_amount).label("deposit_amount"),
                                                func.sum(data_4.c.deposit_cnt).label("deposit_cnt"),
                                                func.sum(data_4.c.withdraw_amount).label("withdraw_amount"),
                                                func.sum(data_4.c.withdraw_cnt).label("withdraw_cnt"),
                                                func.sum(func.if_(data_4.c.deposit_amount > 0, 1, 0)).label(
                                                    "deposit_user_cnt"),
                                                func.sum(func.if_(data_4.c.withdraw_amount > 0, 1, 0)).label(
                                                    "withdraw_user_cnt")). \
            group_by(data_4.c.date, data_4.c.currency).all()
        for _ in data_4:
            result_dic[(_[0], _[1])]["会员总存款"]["总额"] += _[2]
            result_dic[(_[0], _[1])]["会员总存款"]["存款人数"] += _[6]
            result_dic[(_[0], _[1])]["会员总存款"]["存款次数"] += _[3]
            result_dic[(_[0], _[1])]["会员总取款"]["总额"] += _[4]
            result_dic[(_[0], _[1])]["会员总取款"]["取款次数"] += _[5]
            result_dic[(_[0], _[1])]["会员总取款"]["取款人数"] += _[7]
            result_dic[(_[0], _[1])]["会员存取差"] += _[2] - _[4]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]
        # 大额
        big = Dao.get_user_big_io_data_base(site_code, None, start_diff, end_diff, currency, stop_diff=stop_diff,
                                            date_type=date_type).subquery()
        big = ms_context.get().session.query(big.c.user_account, big.c.date, big.c.currency_code,
                                             func.sum(big.c.big_cnt).label("big_cnt")). \
            group_by(big.c.date, big.c.currency_code, big.c.user_account).subquery()
        big = ms_context.get().session.query(big.c.date, big.c.currency_code, func.sum(1).label("big_user_cnt"),
                                             func.sum(big.c.big_cnt)). \
            group_by(big.c.date, big.c.currency_code).all()
        for _ in big:
            result_dic[(_[0], _[1])]["会员总取款"]["大额取款人数"] += _[2]
            result_dic[(_[0], _[1])]["会员总取款"]["大额取款次数"] += _[3]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 会员投注、会员输赢
        data_5 = ComprehensiveReport._user_bet_summary(site_code, currency, start_diff, end_diff, stop_diff,
                                                       date_type, to_site_coin)
        for _ in data_5:
            result_dic[(_[0], _[1])]["会员投注"]["投注金额"] += _[3]
            result_dic[(_[0], _[1])]["会员投注"]["有效投注"] += _[5]
            result_dic[(_[0], _[1])]["会员投注"]["投注人数"] += _[2]
            result_dic[(_[0], _[1])]["会员投注"]["注单量"] += _[4]
            result_dic[(_[0], _[1])]["会员输赢"] += _[6]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 会员VIP福利，会员活动优惠
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff,
                                                               date_type).subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.user_account, vip_act_data.c.date,
                                                      vip_act_data.c.main_currency,
                                                      func.sum(vip_act_data.c.vip).label('vip'),
                                                      func.sum(vip_act_data.c.act).label('act')). \
            group_by(vip_act_data.c.user_account, vip_act_data.c.main_currency, vip_act_data.c.date).subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.date, vip_act_data.c.main_currency,
                                                      func.sum(vip_act_data.c.vip), func.sum(vip_act_data.c.act),
                                                      func.sum(func.if_(vip_act_data.c.vip > 0, 1, 0)),
                                                      func.sum(func.if_(vip_act_data.c.act > 0, 1, 0))). \
            group_by(vip_act_data.c.date, vip_act_data.c.main_currency).all()
        for _ in vip_act_data:
            result_dic[(_[0], _[1])]["会员VIP福利"]["总额"] += _[2]
            result_dic[(_[0], _[1])]["会员活动优惠"]["总额"] += _[3]
            result_dic[(_[0], _[1])]["会员VIP福利"]["人数"] += _[4]
            result_dic[(_[0], _[1])]["会员活动优惠"]["人数"] += _[5]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]
        # 已使用优惠
        used_profit_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
                                                                    date_type).subquery()
        used_profit_data = ms_context.get().session.query(used_profit_data.c.date, used_profit_data.c.currency,
                                                          func.sum(used_profit_data.c.amount)). \
            group_by(used_profit_data.c.date, used_profit_data.c.currency).all()
        for _ in used_profit_data:
            result_dic[(_[0], _[1])]["已使用优惠"] += _[2]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 会员调整
        adjust_data = Dao.get_user_io_summary_data_base(site_code, start_diff=start_diff, end_diff=end_diff,
                                                        currency=currency, stop_diff=stop_diff, date_type='日'). \
            subquery()

        adjust_data = ms_context.get().session.query(adjust_data.c.date, adjust_data.c.currency,
                                                     adjust_data.c.coin_type, adjust_data.c.user_account,
                                                     func.sum(adjust_data.c.other_adjust).label("amount")). \
            group_by(adjust_data.c.date, adjust_data.c.currency, adjust_data.c.coin_type, adjust_data.c.user_account). \
            subquery()
        adjust_data = ms_context.get().session.query(adjust_data.c.date, adjust_data.c.currency,
                                                     adjust_data.c.user_account,
                                                     func.sum(func.if_(adjust_data.c.coin_type == io_type["收入"],
                                                                       adjust_data.c.amount, 0)).label("in_amount"),
                                                     func.sum(func.if_(adjust_data.c.coin_type == io_type["支出"],
                                                                       adjust_data.c.amount, 0)).label("out_amount")
                                                     ). \
            group_by(adjust_data.c.date, adjust_data.c.currency, adjust_data.c.user_account).subquery()
        adjust_data = ms_context.get().session.query(adjust_data.c.date, adjust_data.c.currency,
                                                     func.sum(func.if_(adjust_data.c.in_amount > 0, 1, 0)),
                                                     func.sum(func.if_(adjust_data.c.out_amount > 0, 1, 0)),
                                                     func.sum(adjust_data.c.in_amount),
                                                     func.sum(adjust_data.c.out_amount),
                                                     func.sum(adjust_data.c.in_amount + adjust_data.c.out_amount)). \
            group_by(adjust_data.c.date, adjust_data.c.currency)
        for _ in adjust_data:
            result_dic[(_[0], _[1])]["会员调整"]["总额"] += _[6]
            result_dic[(_[0], _[1])]["会员调整"]["加额"] += _[4]
            result_dic[(_[0], _[1])]["会员调整"]["加额人数"] += _[2]
            result_dic[(_[0], _[1])]["会员调整"]["减额"] += _[5]
            result_dic[(_[0], _[1])]["会员调整"]["减额人数"] += _[3]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 代理下注册人数 - 与转代溢出没关系
        data_1 = ComprehensiveReport._user_register_summary(site_code, currency, start_diff, end_diff,
                                                            grep_has_agent=True)
        for _ in data_1:
            result_dic[(_[0], _[1])]["代理下注册人数"]["总数"] += _[3]
            result_dic[(_[0], _[1])]["代理下注册人数"][_[2]] += _[3]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]

        # 代存会员
        currency_rate = Dao.currency_rate(site_code)
        # 后台人工充值 + 客户端充值 + 代理代存
        coin_type_dic = Dao.get_coin_type()
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, date_type=date_type,
                                                            timezone=timezone)
        data = ms_context.get().session.query(
            func.date_format(func.convert_tz(func.from_unixtime(UserCoinRecord.created_time / 1000),
                                             '+00:00', f'{timezone_sql}:00'), "%Y-%m-%d").label("date"),
            UserCoinRecord.currency, UserCoinRecord.user_account, func.sum(UserCoinRecord.coin_value).label("amount"),
            func.sum(1).label("deposit_cnt")). \
            filter(UserCoinRecord.created_time.between(start_time, end_time),
                   UserCoinRecord.business_coin_type == coin_type_dic['代理代存'],
                   UserCoinRecord.agent_name.is_not(None), UserCoinRecord.site_code == site_code)
        if currency != '平台币':
            data = data.filter(UserCoinRecord.currency == currency)
        data = data.group_by("date", UserCoinRecord.currency, UserCoinRecord.user_account).subquery()
        data = ms_context.get().session.query(data.c.date, data.c.currency, func.sum(1).label("user_cnt"),
                                              func.sum(data.c.deposit_cnt), func.sum(data.c.amount)). \
            group_by(data.c.date, data.c.currency).all()
        for _ in data:
            if currency != '平台币':
                result_dic[(_[0], _[1])]["代存会员"]["额度"] = _[1]
            else:
                result_dic[(_[0], _[1])]["代存会员"]["额度"] = _[1] / currency_rate[_[2]]
            result_dic[(_[0], _[1])]["代存会员"]["人数"] = _[1]
            result_dic[(_[0], _[1])]["代存会员"]["次数"] = _[1]
            result_dic[(_[0], _[1])]["日期"] = _[0]
            result_dic[(_[0], _[1])]["币种"] = _[1]
        return list(result_dic.values())

    @staticmethod
    def get_comprehensive_total_report_vo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日',
                                          currency=None, to_site_coin=False):
        """
        获取综合报表
        @return:
        """
        result_dic = {"会员注册人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                          "IOS_APP", "IOS_H5"], [0 for _ in range(7)])),
                      "会员登录人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                          "IOS_APP", "IOS_H5"], [0 for _ in range(7)])),
                      "会员总存款": {"总额": 0, "存款人数": 0, "存款次数": 0},
                      "会员总取款": {"总额": 0, "取款人数": 0, "取款次数": 0, "大额取款人数": 0, "大额取款次数": 0},
                      "会员存取差": 0, "会员首存": {"总额": 0, "首存人数": 0},
                      "会员投注": dict(zip(["投注金额", "有效投注", "投注人数", "注单量"], [0 for _ in range(4)])),
                      "会员输赢": 0, "会员VIP福利": {"总额": 0, "人数": 0},
                      "会员活动优惠": {"总额": 0, "人数": 0},
                      "已使用优惠": 0,
                      "会员调整": {"总额": 0, "加额": 0, "加额人数": 0, "减额": 0, "减额人数": 0},
                      "代理下注册人数": dict(
                          zip(["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP", "IOS_H5"],
                              [0 for _ in range(7)])),
                      "代存会员": {"人数": 0, "次数": 0, "额度": 0}}
        data = ComprehensiveReport.get_comprehensive_report_vo(site_code, start_diff, end_diff, stop_diff,
                                                               date_type, currency, to_site_coin)
        for _ in data:
            for k in ["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP", "IOS_H5"]:
                result_dic["会员注册人数"][k] += _["会员注册人数"][k]
            for k in ["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP", "IOS_H5"]:
                result_dic["会员登录人数"][k] += _["会员登录人数"][k]
            for k in ["总额", "存款人数", "存款次数"]:
                result_dic["会员总存款"][k] += _["会员总存款"][k]
            for k in ["总额", "取款人数", "取款次数", "大额取款人数", "大额取款次数"]:
                result_dic["会员总取款"][k] += _["会员总取款"][k]
            for k in ["总额", "首存人数"]:
                result_dic["会员首存"][k] += _["会员首存"][k]

            for k in ["投注金额", "有效投注", "投注人数", "注单量"]:
                result_dic["会员投注"][k] += _["会员投注"][k]
            for k in ["总额", "人数"]:
                result_dic["会员VIP福利"][k] += _["会员VIP福利"][k]
            for k in ["总额", "人数"]:
                result_dic["会员活动优惠"][k] += _["会员活动优惠"][k]
            for k in ["总额", "加额", "加额人数", "减额", "减额人数"]:
                result_dic["会员调整"][k] += _["会员调整"][k]
            for k in ["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP", "IOS_H5"]:
                result_dic["代理下注册人数"][k] += _["代理下注册人数"][k]
            for k in ["人数", "次数", "额度"]:
                result_dic["代存会员"][k] += _["代存会员"][k]

            result_dic["会员存取差"] += _["会员存取差"]
            result_dic["会员输赢"] += _["会员输赢"]
            result_dic["已使用优惠"] = +_["已使用优惠"]
        return result_dic



#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:36
from collections import defaultdict

from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.Dao.Mysql.ChainQery.Order import Order
from Library.MysqlTableModel.user_coin_record_model import UserCoinRecord
from Library.MysqlTableModel.user_deposit_withdrawal_model import UserDepositWithdrawal

from Library.MysqlTableModel.site_activity_order_record_model import SiteActivityOrderRecord
from Library.MysqlTableModel.site_activity_free_game_record_model import SiteActivityFreeGameRecord
from Library.MysqlTableModel.site_task_order_record_model import SiteTaskOrderRecord
from Library.MysqlTableModel.site_task_config_model import SiteTaskConfig
from Library.MysqlTableModel.i18n_message_model import I18nMessage

from sqlalchemy import func, and_, case, null
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import Funds
from Library.Dao.Mysql.ChainQery.SiteBackend.User import UserInfo
from Library.Dao.Mysql.ChainQery.SiteBackend.Agent import Agent, AgentInfo


class Report(object):

    @staticmethod
    def get_game_report_base(site_code, start_diff=0, end_diff=0, date_type='日', stop_diff=0, venue_type=None,
                             currency=None):
        """
        游戏报表: 输赢金额已取反
        @return:
        """
        data = Order.query_order_data_sql(site_code, settle_start_diff=start_diff, settle_end_diff=end_diff,
                                          date_type=date_type, stop_diff=stop_diff, venue_type=venue_type,
                                          currency=currency, only_settled=True).subquery()
        data = ms_context.get().session.query(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.game_name,
                                              data.c.user_account, data.c.date, func.count(1).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(-data.c.win_loss_amount).label("win_lose_amount")). \
            group_by(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.user_account, data.c.game_name,
                     data.c.date)
        return data

    @staticmethod
    def get_user_big_io_data_base(site_code, user_account=None, start_diff=0, end_diff=0, currency=None,
                                  agent_account=None, stop_diff=0, date_type='月'):
        """
        获取用户大额存取数据
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, stop_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserDepositWithdrawal.updated_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                              UserDepositWithdrawal.user_account, UserDepositWithdrawal.agent_account,
                                              func.sum(func.if_(
                                                  UserDepositWithdrawal.is_big_money, 1, 0)).label("big_cnt"),
                                              func.sum(func.if_(
                                                  UserDepositWithdrawal.is_big_money,
                                                  UserDepositWithdrawal.apply_amount, 0)).label("big_amount"),
                                              UserDepositWithdrawal.currency_code). \
            filter(UserDepositWithdrawal.site_code == site_code,
                   UserDepositWithdrawal.status == 101, UserDepositWithdrawal.type == 2,
                   UserDepositWithdrawal.updated_time.between(start_time, stop_time))
        if user_account:
            data = data.filter(UserDepositWithdrawal.user_account == user_account)
        if agent_account:
            data = data.filter(UserDepositWithdrawal.agent_account == agent_account)
        if currency:
            data = data.filter(UserDepositWithdrawal.currency_code == currency)
        data = data.group_by("date", UserDepositWithdrawal.user_account, UserDepositWithdrawal.agent_account,
                             UserDepositWithdrawal.currency_code)
        return data

    @staticmethod
    def get_user_io_summary_data_base(site_code, user_account=None, start_diff=0, end_diff=0, currency=None,
                                      agent_account=None, stop_diff=0, date_type='月', register_start_diff=None,
                                      register_end_diff=None):
        """
        获取会员账变记录中的各项基础查询
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        # 大额标记，等功能做好了再自动取
        huge_amount_limit = 1000
        io_coin_type = System.get_coin_record_type()
        business_type = System.get_business_coin_type()
        # 收支类型
        io_type = System.get_coin_record_io_type()
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        recharge_type = [io_coin_type[_] for _ in ("会员存款", "会员存款(后台)", "代理代存")]
        transfer_type = io_coin_type["代理代存"]
        withdraw_type = [io_coin_type[_] for _ in ("会员提款", "会员提款(后台)")]
        data = ms_context.get().session. \
            query(UserCoinRecord.user_account, UserCoinRecord.agent_name, UserCoinRecord.currency,
                  UserCoinRecord.coin_type,
                  func.date_format(func.convert_tz(func.from_unixtime(UserCoinRecord.created_time / 1000), '+00:00',
                                                   f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(func.if_(UserCoinRecord.coin_type.in_(recharge_type), UserCoinRecord.coin_value, 0)).label(
                      "deposit_amount"),
                  func.sum(func.if_(UserCoinRecord.coin_type.in_(recharge_type), 1, 0)).label("deposit_cnt"),
                  func.sum(func.if_(UserCoinRecord.coin_type == transfer_type, UserCoinRecord.coin_value, 0)).label(
                      "transfer_amount"),
                  func.sum(func.if_(UserCoinRecord.coin_type == transfer_type, 1, 0)).label("transfer_cnt"),
                  func.sum(func.if_(UserCoinRecord.coin_type.in_(withdraw_type), UserCoinRecord.coin_value, 0)).label(
                      "withdraw_amount"),
                  func.sum(func.if_(UserCoinRecord.coin_type.in_(withdraw_type), 1, 0)).label("withdraw_cnt"),
                  func.sum(func.if_(
                      and_(UserCoinRecord.coin_type.in_(withdraw_type), UserCoinRecord.coin_value >= huge_amount_limit),
                      UserCoinRecord.coin_value, 0)).label("big_amount"),
                  func.sum(func.if_(
                      and_(UserCoinRecord.coin_type.in_(withdraw_type), UserCoinRecord.coin_value >= huge_amount_limit),
                      1, 0)).label("big_cnt"),
                  func.sum(case([(and_(UserCoinRecord.balance_type == 1, UserCoinRecord.coin_type.in_(
                      recharge_type + [transfer_type] + withdraw_type)), UserCoinRecord.coin_value),
                                 (and_(UserCoinRecord.balance_type == 2, UserCoinRecord.coin_type.in_(
                                     recharge_type + [transfer_type] + withdraw_type)), -UserCoinRecord.coin_value)],
                                else_=0)).label("io_diff"),
                  func.sum(case([(and_(UserCoinRecord.business_coin_type == business_type["VIP福利"],
                                       UserCoinRecord.balance_type == 1), UserCoinRecord.coin_value), (
                                     and_(UserCoinRecord.business_coin_type == business_type["VIP福利"],
                                          UserCoinRecord.balance_type == 2),
                                     -UserCoinRecord.coin_value)], else_=0)).label("vip_amount"),
                  func.sum(case([(and_(UserCoinRecord.business_coin_type == business_type["活动优惠"],
                                       UserCoinRecord.balance_type == 1), UserCoinRecord.coin_value), (
                                     and_(UserCoinRecord.business_coin_type == business_type["活动优惠"],
                                          UserCoinRecord.balance_type == 2),
                                     -UserCoinRecord.coin_value)], else_=0)).label("activity_amount"),
                  func.sum(case([(and_(UserCoinRecord.business_coin_type.in_([business_type['活动优惠'],
                                                                              business_type['VIP福利']]),
                                       UserCoinRecord.balance_type == 1), UserCoinRecord.coin_value), (
                                     and_(UserCoinRecord.business_coin_type.in_([business_type['活动优惠'],
                                                                                 business_type['VIP福利']]),
                                          UserCoinRecord.balance_type == 2),
                                     -UserCoinRecord.coin_value)], else_=0)).label("adjust_amount"),
                  func.sum(case([(and_(UserCoinRecord.business_coin_type.in_([business_type['其他调整']]),
                                       UserCoinRecord.balance_type == 1), UserCoinRecord.coin_value), (
                                     and_(UserCoinRecord.business_coin_type.in_([business_type['其他调整']]),
                                          UserCoinRecord.balance_type == 2),
                                     -UserCoinRecord.coin_value)], else_=0)).label("other_adjust")
                  ). \
            join(UserInfo, and_(UserCoinRecord.user_account == UserInfo.user_account,
                                UserCoinRecord.site_code == UserInfo.site_code)). \
            filter(UserCoinRecord.site_code == site_code, UserCoinRecord.created_time.between(start_time, end_time),
                   UserInfo.account_type == System.get_user_account_type("正式"),
                   UserCoinRecord.balance_type.in_([io_type["收入"], io_type["支出"]]))
        if agent_account:
            data = data.filter(UserCoinRecord.agent_name == agent_account)
        if register_start_diff:
            _start, _end = DateUtil.get_timestamp_range(register_start_diff, register_end_diff)
            data = data.filter(UserInfo.register_time.between(_start, _end))
        if currency:
            data = data.filter(UserInfo.main_currency == currency)
        if user_account:
            data = data.filter(UserCoinRecord.user_account == user_account)
        return data.group_by("date", UserCoinRecord.user_account, UserCoinRecord.currency, UserCoinRecord.agent_name,
                             UserCoinRecord.coin_type)

    @staticmethod
    def get_act_report(site_code, start_diff=0, end_diff=0, act_no=None, act_name=None, stop_diff=0, date_type='日'):
        """
        活动报表
        @return:
        """
        result_data = defaultdict(lambda: {"发放彩金的人数": 0, "发放彩金金额": 0, "发放旋转次数": 0, "参与人数": 0,
                                           "已领取人数": 0, "已领取彩金金额": 0})
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        received_status = System.get_activity_receive_status()

        data_1 = ms_context.get().session. \
            query(SiteActivityOrderRecord.activity_no, SiteTaskOrderRecord.user_account, I18nMessage.message,
                  func.date_format(func.convert_tz(func.from_unixtime(SiteActivityOrderRecord.created_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(SiteActivityOrderRecord.activity_amount / SiteActivityOrderRecord.final_rate).
                  label("amount")). \
            join(I18nMessage, SiteActivityOrderRecord.activity_name_i18n_code == I18nMessage.message_key). \
            filter(SiteActivityOrderRecord.site_code == site_code,
                   SiteActivityOrderRecord.created_time.between(_start, _end), I18nMessage.language == 'zh-CN')
        if act_no:
            data_1 = data_1.filter(SiteActivityOrderRecord.activity_no == act_no)
        if act_name:
            data_1 = data_1.filter(I18nMessage.message == act_name)
        data_1 = data_1.group_by("date", SiteActivityOrderRecord.activity_no, SiteActivityOrderRecord.user_account,
                                 I18nMessage.message).subquery()
        data_1 = ms_context.get().session.query(data_1.c.date, data_1.c.message, data_1.c.activity_no,
                                                func.sum(1).label("give_cnt"),
                                                func.sum(data_1.c.amount).label('give_amount'),
                                                null().label("free_dance_cnt"), null().label("apply_cnt"),
                                                null().label("receive_cnt"), null().label("receive_amount")). \
            group_by(data_1.c.task_id, data_1.c.message, data_1.c.task_type, data_1.c.date)

        data_2 = ms_context.get().session. \
            query(SiteActivityOrderRecord.activity_no, SiteTaskOrderRecord.user_account, I18nMessage.message,
                  func.date_format(func.convert_tz(func.from_unixtime(SiteActivityOrderRecord.receive_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(SiteActivityOrderRecord.activity_amount / SiteActivityOrderRecord.final_rate).
                  label("amount")). \
            join(I18nMessage, SiteActivityOrderRecord.activity_name_i18n_code == I18nMessage.message_key). \
            filter(SiteActivityOrderRecord.site_code == site_code,
                   SiteActivityOrderRecord.receive_time.between(_start, _end), I18nMessage.language == 'zh-CN',
                   SiteActivityOrderRecord.receive_status == received_status["已领取"])
        if act_no:
            data_2 = data_2.filter(SiteActivityOrderRecord.activity_no == act_no)
        if act_name:
            data_2 = data_2.filter(I18nMessage.message == act_name)
        data_2 = data_2.group_by("date", SiteActivityOrderRecord.activity_no, SiteActivityOrderRecord.user_account,
                                 I18nMessage.message).subquery()
        data_2 = ms_context.get().session.query(data_2.c.date, data_2.c.message, data_2.c.activity_no,
                                                func.sum(1).label("give_cnt"),
                                                func.sum(data_2.c.amount).label('give_amount'),
                                                null().label("free_dance_cnt"), null().label("apply_cnt"),
                                                null().label("receive_cnt"), null().label("receive_amount")). \
            group_by(data_2.c.task_id, data_2.c.message, data_2.c.task_type, data_2.c.date)

        # 3.免费旋转
        type_dic = {"增加": 1, "减少": 2}
        data = ms_context.get().session. \
            query(func.date_format(func.convert_tz(func.from_unixtime(SiteActivityFreeGameRecord.created_time / 1000),
                                                   '+00:00', f'{timezone}:00'), '%Y-%m-%d').label("date"),
                  I18nMessage.message, SiteActivityFreeGameRecord.activity_no, SiteActivityFreeGameRecord.user_account,

                  func.sum(SiteActivityFreeGameRecord.acquire_num).label("give_cnt")). \
            filter(SiteActivityFreeGameRecord.site_code == site_code,
                   SiteActivityFreeGameRecord.created_time.between(_start, _end),
                   SiteActivityFreeGameRecord.type == type_dic["增加"])
        if act_no:
            data = data.filter(SiteActivityFreeGameRecord.activity_no == act_no)
        data = data.group_by("date", SiteActivityFreeGameRecord.activity_no,
                             SiteActivityFreeGameRecord.user_account).subquery()

        data_6 = ms_context.get().session.query(data.c.date, data.c.activity_no, func.count(1),
                                                func.sum(data.c.give_cnt), func.sum(data.c.used_cnt),
                                                func.sum(data.c.give_cnt - data.c.used_cnt)). \
            group_by(data.c.activity_no, data.c.date).all()
        for _ in data_6:
            result_data[(_[0], _[1])]["参与人数"] += _[2]
            # result_data[(_[0], _[1])]["参与人数"] += _[2]
            result_data[(_[0], _[1])]["发放免费旋转次数"] += _[3]
            result_data[(_[0], _[1])]["使用免费旋转次数"] += _[4]
            result_data[(_[0], _[1])]["未使用免费旋转次数"] += _[5]
        return result_data

    @staticmethod
    def get_task_report(site_code, start_diff=0, end_diff=0, task_id=None, stop_diff=0, task_type=None, date_type='月'):
        """
        任务报表
        @return:
        """

        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        task_type_dic = System.get_task_type()

        data_1 = ms_context.get().session. \
            query(SiteTaskOrderRecord.task_id, SiteTaskOrderRecord.user_account,
                  I18nMessage.message, SiteTaskOrderRecord.task_type,
                  func.date_format(func.convert_tz(func.from_unixtime(SiteTaskOrderRecord.created_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(SiteTaskOrderRecord.task_amount).label("amount")). \
            join(SiteTaskConfig, SiteTaskOrderRecord.task_id == SiteTaskConfig.id). \
            join(I18nMessage, SiteTaskConfig.task_name_i18n_code == I18nMessage.message_key). \
            filter(SiteTaskOrderRecord.site_code == site_code,
                   SiteTaskOrderRecord.created_time.between(_start, _end), I18nMessage.language == 'zh-CN')
        if task_id:
            data_1 = data_1.filter(SiteTaskOrderRecord.task_id == task_id)
        if task_type:
            data_1 = data_1.filter(SiteTaskOrderRecord.task_type == task_type_dic[task_type])
        data_1 = data_1.group_by("date", SiteTaskOrderRecord.task_id, SiteTaskOrderRecord.user_account,
                                 I18nMessage.message, SiteTaskOrderRecord.task_type).subquery()
        data_1 = ms_context.get().session.query(data_1.c.task_id, data_1.c.message, data_1.c.task_type,
                                                data_1.c.date, func.sum(data_1.c.amount).label('give_amount'),
                                                func.sum(1).label("give_cnt"),
                                                null().label("receive_cnt"), null().label("receive_amount")). \
            group_by(data_1.c.task_id, data_1.c.message, data_1.c.task_type, data_1.c.date)

        data_2 = ms_context.get().session. \
            query(SiteTaskOrderRecord.task_id, SiteTaskOrderRecord.user_account,
                  I18nMessage.message, SiteTaskOrderRecord.task_type,
                  func.date_format(func.convert_tz(func.from_unixtime(SiteTaskOrderRecord.receive_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(SiteTaskOrderRecord.task_amount).label("amount")). \
            join(SiteTaskConfig, SiteTaskOrderRecord.task_id == SiteTaskConfig.id). \
            join(I18nMessage, SiteTaskConfig.task_name_i18n_code == I18nMessage.message_key). \
            filter(SiteTaskOrderRecord.site_code == site_code,
                   SiteTaskOrderRecord.receive_time.between(_start, _end), I18nMessage.language == 'zh-CN')
        if task_id:
            data_2 = data_2.filter(SiteTaskOrderRecord.task_id == task_id)
        if task_type:
            data_2 = data_2.filter(SiteTaskOrderRecord.task_type == task_type_dic[task_type])
        data_2 = data_2.group_by("date", SiteTaskOrderRecord.task_id, SiteTaskOrderRecord.user_account,
                                 I18nMessage.message, SiteTaskOrderRecord.task_type).subquery()
        data_2 = ms_context.get().session.query(data_2.c.task_id, data_2.c.message, data_2.c.task_type,
                                                data_2.c.date, null().label('give_amount'), null().label("give_cnt"),
                                                func.sum(1).label("receive_cnt"),
                                                func.sum(data_2.c.amount).label("receive_amount")). \
            group_by(data_2.c.task_id, data_2.c.message, data_2.c.task_type, data_2.c.date)

        return data_1.union_all(data_2).all()

    @staticmethod
    def get_task_total_report(site_code, start_diff=0, end_diff=0, task_id=None, stop_diff=0, task_type=None,
                              date_type='月'):
        """
        任务报表 - 合计
        @return:
        """

        timezone = Site.get_site_timezone(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        task_type_dic = System.get_task_type()

        data_1 = ms_context.get().session. \
            query(SiteTaskOrderRecord.user_account,
                  func.sum(SiteTaskOrderRecord.task_amount).label("amount")). \
            filter(SiteTaskOrderRecord.site_code == site_code,
                   SiteTaskOrderRecord.created_time.between(_start, _end))
        if task_id:
            data_1 = data_1.filter(SiteTaskOrderRecord.task_id == task_id)
        if task_type:
            data_1 = data_1.filter(SiteTaskOrderRecord.task_type == task_type_dic[task_type])
        data_1 = data_1.group_by(SiteTaskOrderRecord.user_account).subquery()
        data_1 = ms_context.get().session.query(func.sum(data_1.c.amount).label('give_amount'),
                                                func.sum(1).label("give_cnt"),
                                                null().label("receive_cnt"), null().label("receive_amount"))

        data_2 = ms_context.get().session. \
            query(SiteTaskOrderRecord.user_account,
                  func.sum(SiteTaskOrderRecord.task_amount).label("amount")). \
            filter(SiteTaskOrderRecord.site_code == site_code,
                   SiteTaskOrderRecord.receive_time.between(_start, _end))
        if task_id:
            data_2 = data_2.filter(SiteTaskOrderRecord.task_id == task_id)
        if task_type:
            data_2 = data_2.filter(SiteTaskOrderRecord.task_type == task_type_dic[task_type])
        data_2 = data_2.group_by(SiteTaskOrderRecord.user_account).subquery()
        data_2 = ms_context.get().session.query(null().label('give_amount'), null().label("give_cnt"),
                                                func.sum(1).label("receive_cnt"),
                                                func.sum(data_2.c.amount).label("receive_amount"))
        data = data_1.union_all(data_2).subquery()
        data = ms_context.get().session.query(func.sum(data.c.give_amount), func.sum(data.c.give_cnt),
                                              func.sum(data.c.receive_cnt), func.sum(data.c.receive_amount))
        return data.first()

    @staticmethod
    def get_venue_win_lose_data_dao(site_code, start_diff=0, end_diff=0, currency=None, stop_diff=0, date_type='日'):
        """
        场馆投注盈亏数据
        @return:
        """
        data = Report.get_game_report_base(site_code, start_diff, end_diff, date_type, stop_diff, currency=currency). \
            subquery()
        data = ms_context.get().session.query(data.c.venue_code, data.c.currency, data.c.user_account,
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(-data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.venue_code, data.c.currency, data.c.user_account).subquery()
        data = ms_context.get().session.query(data.c.venue_code, data.c.currency, func.count(1).label("user_cnt"),
                                              func.sum(data.c.bet_cnt).label("bet_cnt"),
                                              func.sum(data.c.bet_amount).label("bet_amount"),
                                              func.sum(data.c.valid_amount).label("valid_amount"),
                                              func.sum(-data.c.win_lose_amount).label("win_lose_amount")). \
            group_by(data.c.venue_code, data.c.currency).all()
        return data

    @staticmethod
    def get_venue_win_lose_data_of_agent_dao(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日',
                                             currency='平台币'):
        """
        基于代理的场馆投注盈亏数据     - 可转换为平台币
        @return:
        """
        data = Order.query_order_data_sql(site_code, settle_start_diff=start_diff, settle_end_diff=end_diff,
                                          date_type=date_type, stop_diff=stop_diff).subquery()
        data_result = ms_context.get().session.query(data.c.currency, data.c.agent_acct, data.c.venue_code,
                                                     func.sum(data.c.valid_amount).label("valid_amount"),
                                                     func.sum(-data.c.win_loss_amount).label("win_lose_amount")). \
            filter(data.c.agent_acct.isnot(None)).group_by(data.c.agent_acct, data.c.currency, data.c.venue_code)
        if currency != '平台币':
            data_result = data_result.filter(data.c.currency == currency)
        return {_[1]: _ for _ in data_result.all()}

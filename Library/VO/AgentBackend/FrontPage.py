#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/27 22:49
from Library.Common.Utils.Contexts import *
from collections import defaultdict
from decimal import Decimal, ROUND_HALF_UP
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.FundsEnum import FundsEnum
from sqlalchemy import func, desc
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.user_review_model import UserReview
from Library.MysqlTableModel.user_account_update_review_model import UserAccountUpdateReview
from Library.MysqlTableModel.agent_review_model import AgentReview
from Library.MysqlTableModel.agent_info_modify_review_model import AgentInfoModifyReview
from Library.MysqlTableModel.user_deposit_withdrawal_model import UserDepositWithdrawal
from Library.MysqlTableModel.user_coin_record_model import UserCoinRecord
from Library.MysqlTableModel.user_manual_up_down_record_model import UserManualUpDownRecord

from Library.Dao import Dao
from Library.BO import BO


class FrontPage(object):
    @staticmethod
    def _get_first_recharge_user_count_sql(site_code, agent_account):
        """
        获取本周期首存会员数量 , 全站点级别
        @return:
        """
        cycle_type = BO.get_agent_commission_plan_bo(site_code, agent_account)[agent_account]["结算周期"][-1]
        start_time, end_time = DateUtil.get_timestamp_range(date_type=cycle_type)
        data = ms_context.get().session.query(func.count(1)). \
            filter(UserInfo.site_code == site_code, UserInfo.first_deposit_time.between(start_time, end_time)).all()
        return data[0][0] if data else 0

    @staticmethod
    def _get_bet_user_count_sql(site_code, agent_account):
        """
        获取周期投注会员数量
        @return:
        """
        cycle_type = BO.get_agent_commission_plan_bo(site_code, agent_account)[agent_account]["结算周期"][-1]

        start_time, end_time = DateUtil.get_timestamp_range(date_type=cycle_type)
        data = ms_context.get().session.query(func.count(1)). \
            filter(OrderRecord.site_code == site_code, OrderRecord.settle_time.between(start_time, end_time)). \
            group_by(OrderRecord.user_account)
        return data[0][0] if data else 0

    @staticmethod
    def get_head_summary_vo(site_code, agent_account, currency='平台币'):
        """
        获取上方统计项 -
        :param currency: 指定传对应的主货币简称，也可传 平台币
        @return:
        """
        cycle_type = BO.get_agent_commission_plan_bo(site_code, agent_account)[agent_account]["结算周期"]
        # a = BO.calc_win_loss_commission_dao(site_code, cycle_type, currency=currency)
        commission_data = BO.calc_win_loss_commission_dao(site_code, cycle_type, currency=currency)[agent_account]
        print("佣金基础数据")
        # print(commission_data)

        c_sum_data = FrontPage._get_user_sum_data(site_code, agent_account, 0, 0, 0, cycle_type[-1])
        last_sum_data = FrontPage._get_user_sum_data(site_code, agent_account, -1, -1, 0, cycle_type[-1])

        result_data = defaultdict(Decimal)
        # 1.本期净输赢
        result_data['本期净输赢'] = commission_data['本期会员净输赢']
        # 2.本期新增下级
        result_data["本期新增下级"] = c_sum_data['本期新增下级'][agent_account]["直属代理"]
        # 3.本期首存人数
        c_amount = c_sum_data['本期首存人数']
        last_amount = last_sum_data['本期首存人数']
        if c_amount == 0 and last_amount > 0:
            first_deposit_rate = -100
        elif last_amount == 0:
            if c_amount == 0:
                first_deposit_rate = 0
            else:
                first_deposit_rate = 100
        else:
            first_deposit_rate = round((c_amount - last_amount) * 100 / last_amount, 2)

        result_data["本期首存人数"] = c_amount
        result_data["首存人数变化率"] = first_deposit_rate
        # 4.本期新注册会员
        c_amount = c_sum_data['本期新注册会员']
        last_amount = last_sum_data['本期新注册会员']
        if c_amount == 0 and last_amount > 0:
            new_register_rate = -100
        elif last_amount == 0:
            if c_amount == 0:
                new_register_rate = 0
            else:
                new_register_rate = 100
        else:
            new_register_rate = round((c_amount - last_amount) * 100 / last_amount, 2)

        result_data["本期新注册会员"] = c_amount
        result_data["新注册会员变化率"] = new_register_rate
        # 5.本期有效新增会员
        result_data['本期有效新增会员'] = commission_data['有效新增']
        # 6.本期有效活跃会员
        result_data['本期有效活跃会员'] = commission_data['有效活跃']
        return result_data

    @staticmethod
    def _get_user_sum_data(site_code, agent_account, start_diff, end_diff, stop_diff, date_type):
        """
        获取首页用户数据概览
        @return:
        """
        return {"本期新增下级": Dao.get_new_agent_count_sql(site_code, start_diff, end_diff, stop_diff, date_type),
                "本期新注册会员": Dao.get_new_user_count_sql(site_code, start_diff, end_diff, stop_diff,
                                                      date_type)[agent_account],
                "新增充值会员": Dao.get_new_recharge_user_count_sql(site_code, start_diff, end_diff, stop_diff,
                                                              date_type)[agent_account],
                "登录会员": Dao.get_login_user_count_sql(site_code, start_diff, end_diff, stop_diff,
                                                     date_type)[agent_account],
                "本期首存人数": Dao.get_first_deposit_user_count(site_code, start_diff, end_diff, stop_diff,
                                                           date_type)["直属首存玩家数量"][agent_account],
                "投注人数": Dao.get_bet_user_count_sql(site_code, start_diff, end_diff, stop_diff,
                                                   date_type)[agent_account]}

    @staticmethod
    def get_new_register_chart_vo(site_code, agent_account, date_diff=0, date_type='月'):
        """
        新注册人数 - 走势图统计
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, date_type=date_type,
                                                            timezone=timezone)
        format_dic = {"日": "%H", "月": "%d", "年": "%m"}
        data = ms_context.get().session.query(func.date_format(func.convert_tz(
            func.from_unixtime(UserInfo.register_time / 1000),
            '+00:00', f'{timezone_sql}:00'), format_dic[date_type]).label("date"),
                                              func.count(1)). \
            filter(UserInfo.register_time.between(start_time, end_time),
                   UserInfo.super_agent_account == agent_account, UserInfo.site_code == site_code). \
            group_by("date").order_by("date")
        return data.all()

    @staticmethod
    def get_first_deposit_chart_vo(site_code, agent_account, date_diff=0, date_type='月'):
        """
        首存人数 - 走势图统计
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, date_type=date_type,
                                                            timezone=timezone)
        format_dic = {"日": "%H", "月": "%d", "年": "%m"}
        data = ms_context.get().session.query(func.date_format(func.convert_tz(
            func.from_unixtime(UserInfo.first_deposit_time / 1000),
            '+00:00', f'{timezone_sql}:00'), format_dic[date_type]).label("date"), func.count(1)). \
            filter(UserInfo.first_deposit_time.between(start_time, end_time),
                   UserInfo.super_agent_account == agent_account, UserInfo.site_code == site_code). \
            group_by("date").order_by("date")
        return data.all()

    @staticmethod
    def get_todo_count_vo(site_code):
        """
        获取首页待办事项
        @param site_code:
        @return:
        """
        review_status_dic = Dao.get_review_status()
        todo_count_dic = {}
        data = ms_context.get().session.query(func.count(1)). \
            filter(UserAccountUpdateReview.site_code == site_code,
                   UserAccountUpdateReview.review_status.notin_(review_status_dic["审核通过"],
                                                                review_status_dic["一审拒绝"])).all()
        todo_count_dic['会员账户修改审核'] = data[0][0]

        data = ms_context.get().session.query(func.count(1)). \
            filter(UserReview.site_code == site_code,
                   UserReview.review_status.notin_(review_status_dic["审核通过"],
                                                   review_status_dic["一审拒绝"])).all()
        todo_count_dic['新增会员审核'] = data[0][0]

        data = ms_context.get().session.query(func.count(1)). \
            filter(AgentReview.site_code == site_code,
                   AgentReview.review_status.notin_(review_status_dic["审核通过"],
                                                    review_status_dic["一审拒绝"])).all()
        todo_count_dic['新增代理审核'] = data[0][0]

        data = ms_context.get().session.query(func.count(1)). \
            filter(AgentInfoModifyReview.site_code == site_code,
                   AgentInfoModifyReview.review_status.notin_(review_status_dic["审核通过"],
                                                              review_status_dic["一审拒绝"])).all()
        todo_count_dic['代理账户修改审核'] = data[0][0]

        data = ms_context.get().session.query(func.count(1)). \
            filter(UserDepositWithdrawal.site_code == site_code, UserDepositWithdrawal.type == 1,
                   UserDepositWithdrawal.audit_status.in_(FundsEnum.deposit_withdraw_status_f_zh.value["待一审"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["一审审核"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["待二审"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["二审审核"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["待三审"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["三审审核"]))
        todo_count_dic['会员充值审核'] = data.all()[0][0]

        data = ms_context.get().session.query(func.count(1)). \
            filter(UserDepositWithdrawal.site_code == site_code, UserDepositWithdrawal.type == 2,
                   UserDepositWithdrawal.audit_status.in_(FundsEnum.deposit_withdraw_status_f_zh.value["待一审"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["一审审核"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["待二审"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["二审审核"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["待三审"],
                                                          FundsEnum.deposit_withdraw_status_f_zh.value["三审审核"]))
        todo_count_dic['会员提款审核'] = data.all()[0][0]

        agent_review_status_dic = Dao.get_agent_review_status()
        data = ms_context.get().session.query(func.count(1)). \
            filter(UserManualUpDownRecord.site_code == site_code,
                   UserManualUpDownRecord.order_status.in_((agent_review_status_dic["待一审"],
                                                            agent_review_status_dic["一审审核"],
                                                            agent_review_status_dic["二审审核"]))).all()

        todo_count_dic['会员人工加额审核'] = data[0][0]
        # 代理充值审核
        # 代理提款审核
        # 佣金审核
        # 代理人工加额审核
        return todo_count_dic

    # @staticmethod
    # def win_lose_overview(site_code, start_diff, end_diff):
    #     """
    #     输赢概览
    #     @param site_code:
    #     @param start_diff:
    #     @param end_diff:
    #     @return:
    #     """
    #     timezone = Dao.get_site_timezone(site_code)
    #     start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, timezone=timezone)
    #     # 平台游戏输赢
    #     data = ms_context.get().session.query(func.sum(OrderRecord.win_loss_amount)). \
    #         filter(OrderRecord.site_code == site_code, OrderRecord.first_settle_time.between(start_time, end_time))
    #     value_1 = -data.first()[0]
    #     # 平台净输赢
    #     # 用户充值总额
    #     # 用户提款总额
    #     return {"平台游戏输赢": value_1, "平台净输赢": 1, "用户充值总额": 2, "用户提款总额": 3}

    @staticmethod
    def get_io_chart_vo(site_code, agent_account, io_type, date_diff=0, currency='平台币', date_type='月'):
        """
        存取金额 - 走势图统计
        :param io_type: 会员存款 ｜ 会员取款
        @return:
        """
        currency_rate = Dao.currency_rate(site_code)
        # 后台人工充值 + 客户端充值 + 代理代存
        business_type_dic = Dao.get_business_coin_type()
        balance_type_dic = Dao.get_coin_record_io_type()
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, date_type=date_type,
                                                            timezone=timezone)
        format_dic = {"日": "%H", "月": "%d", "年": "%m"}
        data = ms_context.get().session.query(
            func.date_format(func.convert_tz(func.from_unixtime(UserCoinRecord.created_time / 1000),
                                             '+00:00', f'{timezone_sql}:00'), format_dic[date_type]).label("date"),
            func.sum(UserCoinRecord.coin_value), UserCoinRecord.currency). \
            filter(UserCoinRecord.created_time.between(start_time, end_time),
                   UserCoinRecord.business_coin_type == business_type_dic[io_type],
                   UserCoinRecord.agent_name == agent_account, UserCoinRecord.site_code == site_code,
                   UserCoinRecord.balance_type.in_([balance_type_dic["收入"], balance_type_dic["支出"]]))
        if currency != '平台币':
            data = data.filter(UserCoinRecord.currency == currency)
        data = data.group_by("date", UserCoinRecord.currency).order_by("date").all()
        result_dic = defaultdict(Decimal)
        for _ in data:
            if currency != '平台币':
                result_dic[_[0]] = _[1]
            else:
                result_dic[_[0]] += _[1] / currency_rate[_[2]]
        for key, value in result_dic.items():
            result_dic[key] = result_dic[key].quantize(Decimal("0.00"))
        return result_dic

    # @staticmethod
    # def get_withdraw_chart(date_type, date_diff, site_code=None):
    #     """
    #     取款金额 - 走势图统计
    #     @param site_code:
    #     @param date_type: 日 ｜ 月 ｜ 年
    #     @param date_diff:
    #     @return:
    #     """
    #     # 后台人工提款 + 客户端提款
    #     coin_type_dic = System.get_coin_type()
    #     start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, date_type=date_type)
    #     format_dic = {"日": "%H", "月": "%d", "年": "%m"}
    #     data = ms_context.get().session.query(UserCoinRecord.site_code, func.date_format(
    #         func.from_unixtime(UserCoinRecord.created_time / 1000),
    #         format_dic[date_type]).label("date"), func.count(1)). \
    #         filter(UserCoinRecord.created_time.between(start_time, end_time),
    #                UserCoinRecord.business_coin_type.in_(coin_type_dic["会员提款"], coin_type_dic["会员提款(后台)"])). \
    #         group_by("date", UserCoinRecord.site_code).order_by("date")
    #     if site_code:
    #         data = data.filter(OrderRecord.site_code == site_code)
    #     return data.all()

    @staticmethod
    def get_win_lose_chart_vo(site_code, agent_account, date_diff=0, currency='平台币', date_type='月'):
        """
        总输赢 - 走势图统计
        @return:
        """
        currency_rate = Dao.currency_rate(site_code)
        timezone = Dao.get_site_timezone(site_code)
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, date_type=date_type,
                                                            timezone=timezone)
        format_dic = {"日": "%H", "月": "%d", "年": "%m"}
        data = ms_context.get().session.query(func.date_format(func.convert_tz(
            func.from_unixtime(OrderRecord.settle_time / 1000),
            '+00:00', f'{timezone_sql}:00'), format_dic[date_type]).label("date"),
                                              func.sum(OrderRecord.win_loss_amount), OrderRecord.currency). \
            filter(OrderRecord.settle_time.between(start_time, end_time),
                   OrderRecord.site_code == site_code, OrderRecord.agent_acct == agent_account)
        if currency != '平台币':
            data = data.filter(OrderRecord.currency == currency)
        data = data.group_by("date", OrderRecord.currency).order_by("date").all()
        result_dic = defaultdict(Decimal)
        for _ in data:
            if currency != '平台币':
                result_dic[_[0]] = _[1]
            else:
                result_dic[_[0]] += _[1] / currency_rate[_[2]]
        for key, value in result_dic.items():
            result_dic[key] = result_dic[key].quantize(Decimal("0.00"))
        return result_dic

    @staticmethod
    def get_deposit_5_vo(site_code, agent_account, currency='平台币'):
        """
        最新存款
        @return:
        """
        currency_rate = Dao.currency_rate(site_code)
        customer_status_dic = {'1': "成功", '2': "失败"}
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        data = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserDepositWithdrawal.updated_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d %H:%i:%s').label("date"),
                                              UserDepositWithdrawal.user_account,
                                              UserDepositWithdrawal.arrive_amount, UserDepositWithdrawal.currency_code,
                                              UserDepositWithdrawal.customer_status). \
            filter(UserDepositWithdrawal.type == 1, UserDepositWithdrawal.site_code == site_code,
                   UserDepositWithdrawal.agent_account == agent_account,
                   UserDepositWithdrawal.customer_status.in_([1, 2]))
        if currency != '平台币':
            data = data.filter(UserDepositWithdrawal.currency_code == currency)
        data = data.order_by(desc("date")).limit(5).all()
        result = []
        for _ in data:
            result.append({"会员账号": _[1],
                           "存款金额": _[2] if currency != '平台币' else round(_[2] / currency_rate[currency], 2),
                           "状态": customer_status_dic[_[4]], "时间": _[0], "币种": _[3]})
        return result

    @staticmethod
    def get_game_record_5_vo(site_code, agent_account, currency='平台币'):
        """
        游戏输赢
        @return:
        """
        currency_rate = Dao.currency_rate(site_code)
        venue_name_dic = Dao.get_venue_name_dic(to_zh=True)
        order_status = Dao.get_order_status()
        timezone_sql = Dao.get_site_timezone_for_sql(site_code)
        data = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(OrderRecord.bet_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d %H:%i:%s').label("date"), OrderRecord.user_account,
                                              OrderRecord.venue_code, OrderRecord.win_loss_amount,
                                              OrderRecord.currency). \
            filter(OrderRecord.site_code == site_code, OrderRecord.agent_acct == agent_account,
                   OrderRecord.order_status != order_status["未结算"])
        if currency != '平台币':
            data = data.filter(OrderRecord.currency == currency)
        data = data.order_by(desc("date")).limit(5).all()
        result = []
        for _ in data:
            result.append({"会员账号": _[1], "场馆名称": venue_name_dic[_[2]],
                           "输赢金额": _[3] if currency != '平台币' else currency_rate[currency],
                           "时间": _[0], "币种": _[4]})
        return result

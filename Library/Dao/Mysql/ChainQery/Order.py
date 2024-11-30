#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 17:41
import time
from sqlalchemy import func, desc
from sqlalchemy.orm import session
from collections import defaultdict

from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo

from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.GameEnum import GameEnum
from Library.Dao.Mysql.ChainQery.SiteBackend.Agent import Agent
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import Funds
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Dao.Mysql.ChainQery.MasterBackend.Game import Game, GameInfo


class Order(object):
    """
    原始注单查询相关
    """

    @staticmethod
    def get_user_valid_amount(user_account, group_by_venue=False):
        """
        获取用户有效投注金额
        :param user_account:
        :param group_by_venue: 是否按场馆分组
        :return:
        """
        if not group_by_venue:
            data = ms_context.get().session.query(func.sum(OrderRecord.valid_amount)). \
                filter(OrderRecord.user_account == user_account).group_by(OrderRecord.user_account)
            if list(data):
                return data.first()[0]
            else:
                return 0
        else:
            data = ms_context.get().session.query(OrderRecord.venue_code, func.sum(OrderRecord.valid_amount)). \
                filter(OrderRecord.user_account == user_account).group_by(OrderRecord.user_account,
                                                                          OrderRecord.venue_code)
            return data.all()

    @staticmethod
    def get_agent_valid_amount(site_code, agent_account=""):
        """
        获取用户有效投注金额,按代理分组
        :return:
        """
        currency_rate = Funds.currency_rate(site_code)
        # 代理数据
        agent_data = Agent.get_agent_list_data(site_code)
        # 生成代理id与account\path的映射表
        agent_dic = {_.id: (_.agent_account, _.path.split(",")) for _ in agent_data}

        result = ms_context.get().session.query(OrderRecord.agent_acct, OrderRecord.currency,
                                                func.sum(OrderRecord.valid_amount))
        if agent_account:
            result = result.filter(OrderRecord.agent_acct == agent_account)
        result = result.group_by(OrderRecord.agent_acct, OrderRecord.currency).all()
        agent_data_dic = defaultdict(int)
        # 转换金额为平台币
        for data in result.all():
            # 优先满足条件, 转为平台币
            platform_amount = data[2] / currency_rate[data[1]]
            # 代理下会员
            if data[0]:
                agent_path = agent_dic[data[0]][1]
                for agent_id in agent_path:
                    agent_data_dic[agent_dic[agent_id][0]] += platform_amount
            # 直营会员
            else:
                agent_data_dic["直营"] += platform_amount
        return agent_data_dic

    @staticmethod
    def wait_until_order_exist(order_no, timeout=5):
        """
        等待三方订单号生成
        @param order_no:
        @param timeout:
        @return:
        """
        session_obj: session = ms_context.get().session
        begin_time = time.time()
        while time.time() - begin_time < timeout:
            data = session_obj.query(OrderRecord).filter(OrderRecord.third_order_id == order_no)
            if list(data):
                return data.one()
            time.sleep(0.2)
        raise AssertionError(f"超过{timeout}秒，注单未生成")

    @staticmethod
    def check_if_order_exist(order_no):
        """
        查看注单是否存在
        @return:
        """
        session_obj: session = ms_context.get().session
        data = session_obj.query(OrderRecord).filter(OrderRecord.third_order_id == order_no)
        if list(data):
            return data.one()
        else:
            return

    @staticmethod
    def query_order_data_sql(site_code="", venue_code=None, order_no="", third_order_no="", bet_start_diff=None,
                             bet_end_diff=None, settle_start_diff=None, settle_end_diff=None,
                             first_settle_start_diff=None, first_settle_end_diff=None,
                             venue_type="", game_platform="", game_no="", game_name="", user_account="",
                             account_type="", vip_rank="", vip_grade="", agent_account="", game_account="",
                             betting_ip="", change_status="", order_status="", currency="", bet_amount_min="",
                             bet_amount_max=None, win_lose_min=None, win_lose_max=None, date_type='日', stop_diff=0,
                             only_settled=False):
        """
        获取游戏注单基础数据
        :return:
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        game_info_data = Game.get_game_info_dao()
        game_info_dic = {_.game_name: _.game_id for _ in game_info_data}
        rsp = ms_context.get().session.query(OrderRecord, func.date_format(
            func.convert_tz(func.from_unixtime(OrderRecord.settle_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d').label("date")).filter(OrderRecord.site_code == site_code)
        if bet_start_diff or bet_start_diff == 0:
            start_bet_time, stop_bet_time = DateUtil.get_timestamp_range(bet_start_diff, bet_end_diff,
                                                                         stop_diff, date_type, timezone)
            rsp = rsp.filter(OrderRecord.bet_time.between(start_bet_time, stop_bet_time))
        if venue_code:
            rsp = rsp.filter(OrderRecord.venue_code == venue_code)
        if order_no:
            rsp = rsp.filter(OrderRecord.order_id == order_no)
        if third_order_no:
            rsp = rsp.filter(OrderRecord.third_order_id == third_order_no)
        if only_settled:
            rsp = rsp.filter(OrderRecord.settle_time.isnot(None))
        if settle_start_diff or settle_start_diff == 0:
            start_settle_time, stop_settle_time = DateUtil.get_timestamp_range(settle_start_diff, settle_end_diff,
                                                                               stop_diff, date_type, timezone)
            rsp = rsp.filter(OrderRecord.settle_time.between(start_settle_time, stop_settle_time))
        if first_settle_start_diff or first_settle_start_diff == 0:
            start_settle_time, stop_settle_time = DateUtil.get_timestamp_range(first_settle_start_diff,
                                                                               first_settle_end_diff,
                                                                               stop_diff, date_type, timezone)
            rsp = rsp.filter(OrderRecord.settle_time.between(start_settle_time, stop_settle_time))
        if venue_type:
            rsp = rsp.filter(System.get_venue_type(venue_type) == OrderRecord.venue_type)
        if game_platform:
            rsp = rsp.filter(OrderRecord.venue_code.in_([game_info_dic[_] for _ in game_platform.split(",")]))
        if game_no:
            rsp = rsp.filter(OrderRecord.game_no == game_no)
        if game_name:
            rsp = rsp.filter(OrderRecord.game_name == game_name)
        if user_account:
            rsp = rsp.filter(OrderRecord.user_account == user_account)
        if account_type:
            rsp = rsp.filter(OrderRecord.account_type.in_([System.get_user_account_type(_) for _ in
                                                           account_type.split(",")]))
        if vip_rank:
            rsp = rsp.filter(OrderRecord.vip_rank == vip_rank)
        if vip_grade:
            rsp = rsp.filter(OrderRecord.vip_grade_code == vip_grade)
        if agent_account:
            rsp = rsp.filter(OrderRecord.agent_acct == agent_account)
        if game_account:
            rsp = rsp.filter(OrderRecord.user_name == agent_account)
        if betting_ip:
            rsp = rsp.filter(OrderRecord.bet_ip == betting_ip)
        if change_status:
            rsp = rsp.filter(OrderRecord.change_status == System.get_order_change_status(change_status))
        if order_status:
            rsp = rsp.filter(OrderRecord.order_status.in_([System.get_order_status(_) for _ in
                                                           order_status.split(",")]))
        if currency:
            # rsp = rsp.filter(OrderRecord.currency.in_([System.get_currency_dic(_) for _ in currency.split(",")]))
            rsp = rsp.filter(OrderRecord.currency.in_(currency.split(",")))
        if bet_amount_min:
            rsp = rsp.filter(OrderRecord.bet_amount.between(bet_amount_min, bet_amount_max))
        if win_lose_min:
            rsp = rsp.filter(OrderRecord.win_loss_amount.between(win_lose_min, win_lose_max))
        return rsp

    @staticmethod
    def get_agent_order_summary(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', currency='平台币'):
        """
        代理维度统计注单信息： 投注单数，总投注金额，有效投注金额，负盈利 - 可转换为平台币    - 输赢已取反
        @return: order_amount_dic, bet_amount_dic, valid_amount_dic, win_loss_amount_dic
        """
        agent_data = Agent.get_agent_list_data(site_code)
        win_loss_amount_dic = defaultdict(int)
        bet_amount_dic = defaultdict(int)
        valid_amount_dic = defaultdict(int)
        # 注单数量
        order_amount_dic = defaultdict(int)
        agent_account_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.agent_id: _.agent_account for _ in agent_data}

        order_data = Order.get_user_bet_summary_by_user_sql(site_code, start_diff=start_diff, end_diff=end_diff,
                                                            stop_diff=stop_diff, date_type=date_type).subquery()
        # 先合并代理数据
        order_result = ms_context.get().session.query(order_data.c.agent_acct, order_data.c.currency,
                                                      func.sum(-order_data.c.win_loss_amount).label("win_loss_amount"),
                                                      func.sum(order_data.c.bet_amount).label("bet_amount"),
                                                      func.sum(order_data.c.valid_amount).label("valid_amount"),
                                                      func.sum(order_data.c.order_amount).label("order_amount")). \
            group_by(order_data.c.currency, order_data.c.agent_acct)
        if currency != '平台币':
            order_result = order_result.filter(order_data.c.currency == currency)
        currency_rate = Funds.currency_rate(site_code)

        for data in order_result.all():
            if data.agent_acct:
                # agent_path = agent_dic[data.super_agent_id][1]
                agent_path = agent_account_dic[data.agent_acct]
                if currency != '平台币':
                    win_loss = data.win_loss_amount
                    bet_amount = data.bet_amount
                    valid_amount = data.valid_amount
                else:
                    win_loss = data.win_loss_amount / currency_rate[data[1]]
                    bet_amount = data.bet_amount / currency_rate[data[1]]
                    valid_amount = data.valid_amount / currency_rate[data[1]]

                for agent_id in agent_path:
                    if agent_id not in agent_id_dic:
                        continue
                    sub_agent_account = agent_id_dic[agent_id]
                    order_amount_dic[sub_agent_account] += 1
                    win_loss_amount_dic[sub_agent_account] += win_loss
                    bet_amount_dic[sub_agent_account] += bet_amount
                    valid_amount_dic[sub_agent_account] += valid_amount
        return order_amount_dic, bet_amount_dic, valid_amount_dic, win_loss_amount_dic

    @staticmethod
    def get_user_bet_summary_by_user_sql(site_code, user_account="", account_type="正式", agent_account=None,
                                         currency=None, start_diff=None, end_diff=0, register_start_diff=None,
                                         register_end_diff=None, stop_diff=0, date_type='月'):
        """
        获取用户投注汇总信息
        :param account_type: 正式 ｜ 测试，可多选，逗号分割  - 输赢未取反
        @return: 会员账号，账号类型，代理账号, 币种, 总输赢，总投注金额，有效金额，注单量
        """
        user_type = System.get_user_account_type()
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        order_data = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(OrderRecord.settle_time / 1000), '+00:00', f'{timezone_sql}:00'),
            '%Y-%m-%d').label("date"), OrderRecord.user_account, OrderRecord.account_type,
                                                    OrderRecord.agent_acct, OrderRecord.currency,
                                                    func.sum(OrderRecord.win_loss_amount).label("win_loss_amount"),
                                                    func.sum(OrderRecord.bet_amount).label("bet_amount"),
                                                    func.sum(OrderRecord.valid_amount).label("valid_amount"),
                                                    func.sum(1).label("order_amount")). \
            filter(OrderRecord.site_code == site_code, OrderRecord.account_type.in_([user_type["正式"]]))
        if register_start_diff or register_start_diff == 0:
            order_data = order_data.join(UserInfo, OrderRecord.user_account == UserInfo.user_account)
        if user_account:
            order_data = order_data.filter(OrderRecord.user_account == user_account)
        if agent_account:
            order_data = order_data.filter(OrderRecord.agent_acct == agent_account)
        if start_diff or start_diff == 0:
            _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone=timezone)
            order_data = order_data.filter(OrderRecord.settle_time.between(_start, _end))
        # if account_type:
        #     account_type_dic = System.get_user_account_type()
        #     account_type_list = [account_type_dic[_] for _ in account_type.split(",")]
        #     order_data = order_data.filter(OrderRecord.account_type.in_(account_type_list))
        if register_start_diff or register_start_diff == 0:
            _start, _end = DateUtil.get_timestamp_range(register_start_diff, register_end_diff, timezone=timezone)
            order_data = order_data.filter(UserInfo.register_time.between(_start, _end))
        if currency:
            order_data = order_data.filter(OrderRecord.currency == currency)
        order_data = order_data.group_by(OrderRecord.user_account, OrderRecord.agent_acct, OrderRecord.account_type,
                                         OrderRecord.currency, "date")
        return order_data

    @staticmethod
    def get_user_bet_top_3_sql(site_code, user_account, start_diff=None, end_diff=0, stop_diff=0, date_type='月'):
        """
        用户投注top3平台统计
        @return: 总输赢，总投注金额，有效金额，注单量
        """
        order_data = ms_context.get().session.query(OrderRecord.venue_code,
                                                    func.sum(OrderRecord.win_loss_amount).label("win_loss_amount"),
                                                    func.sum(OrderRecord.bet_amount).label("bet_amount"),
                                                    func.sum(OrderRecord.valid_amount).label("valid_amount"),
                                                    func.sum(1).label("order_amount")). \
            filter(OrderRecord.site_code == site_code, OrderRecord.user_account == user_account)
        if start_diff:
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type)
            order_data = order_data.filter(OrderRecord.settle_time.between(start_time, end_time))
        order_data = order_data.group_by(OrderRecord.venue_code).order_by(desc("win_loss_amount")).limit(3)
        return order_data

    # @staticmethod
    # def get_comprehensive_report_dao(site_code, start_diff=0, end_diff=0, stop_day=0, date_type='月'):
    #     """
    #     获取综合报表
    #     @return:
    #     """
    #
    #     # 会员注册人数、会员首存
    #     # 会员登录人数
    #     # 会员总存款、会员总取款、会员存取差
    #     # 会员投注、会员输赢
    #     # 会员VIP福利、会员活动优惠、已使用优惠
    #     # 会员调整
    #     # 代理注册人数
    #     # 代理总存款、代理总取款、代理存取差
    #     # 代存会员
    #     # 代理转账
    #     # 代理总优惠
    #     # 代理调整
    #
    #     agent_data = Agent.get_agent_list_data(site_code)
    #     login_count_dic = defaultdict(int)
    #     # 生成代理id与account\path的映射表
    #     agent_dic = {_.id: (_.agent_account, _.path.split(",")) for _ in agent_data}
    #
    #     start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_day, date_type)
    #     user_data = ms_context.get().session.query(func.count(1)). \
    #         filter(UserInfo.site_code == site_code, UserInfo.last_login_time.between(start_time, end_time))
    #
    #     for data in user_data:
    #         data: UserInfo
    #         # 代理下会员
    #         if data.super_agent_id:
    #             agent_path = agent_dic[data.super_agent_id][1]
    #             for agent_id in agent_path:
    #                 login_count_dic[agent_dic[agent_id][0]] += 1
    #         # 直营会员
    #         else:
    #             login_count_dic["直营"] += 1
    #
    #     return login_count_dic

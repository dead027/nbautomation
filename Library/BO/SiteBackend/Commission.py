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

from Library.MysqlTableModel.agent_commission_final_report_model import AgentCommissionFinalReport
from Library.MysqlTableModel.agent_commission_ladder_model import AgentCommissionLadder
from Library.MysqlTableModel.agent_commission_plan_model import AgentCommissionPlan
from Library.MysqlTableModel.agent_info_model import AgentInfo
from Library.MysqlTableModel.user_coin_record_model import UserCoinRecord
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.MysqlTableModel.user_deposit_withdrawal_model import UserDepositWithdrawal
from Library.MysqlTableModel.agent_deposit_withdrawal_model import AgentDepositWithdrawal
from Library.MysqlTableModel.agent_rebate_config_model import AgentRebateConfig


class Commission(object):
    """
    佣金相关
    """

    @staticmethod
    def _get_deposit_valid_user(site_code, query_type, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取代理下 充值金额达到限制 的有效活跃用户列表，转为平台币进行判定
        :param query_type: 有效活跃 | 有效新增
        @return: {"agent_account": [user_account1, user_account2, ...]}
        """
        timezone = Dao.get_site_timezone(site_code)
        # 获取所有代理的佣金方案中的用户充值金额和有效投注金额限制
        limit_dic = Commission.get_agent_commission_plan_bo(site_code)
        # 汇率
        currency_rate = Dao.currency_rate(site_code)
        # 代理数据
        agent_data = Dao.get_agent_list_data(site_code)
        # 生成代理id与account\path的映射表
        agent_account_dic = {_.agent_account: (_.agent_account, _.path.split(",")) for _ in agent_data}
        agent_id_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}
        user_dic = defaultdict(list)
        # 账变类型
        business_type = Dao.get_business_coin_type()
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)

        result = ms_context.get().session.query(UserCoinRecord.currency, UserCoinRecord.user_account,
                                                UserCoinRecord.agent_name, func.sum(UserCoinRecord.coin_value)). \
            filter(UserCoinRecord.site_code == site_code, UserCoinRecord.created_time.between(start_time, end_time),
                   UserCoinRecord.business_coin_type == business_type['会员存款'],
                   UserCoinRecord.agent_name.isnot(None)). \
            group_by(UserCoinRecord.currency, UserCoinRecord.user_account, UserCoinRecord.agent_name)
        for data in result.all():
            # 优先满足条件, 转为平台币
            platform_amount = data[3] / currency_rate[data[0]]
            limit = limit_dic[data[2]][query_type]["充值金额"]
            if platform_amount >= limit:
                if data[2] not in agent_account_dic:
                    continue
                agent_path = agent_account_dic[data[2]][1]
                for agent_id in agent_path:
                    user_dic[agent_id_dic[agent_id][0]].append(data[1])
        return user_dic

    @staticmethod
    def _get_bet_valid_user(site_code, query_type, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取投注达到某个值的用户列表 - 用于投注 有效会员，转为平台币进行判定
        :param query_type: 有效活跃 | 有效新增
        @return: {"agent_account": [user_account1, user_account2, ...]}
        """
        timezone_sql = Dao.get_site_timezone(site_code)
        # 获取所有代理的佣金方案中的用户充值金额和有效投注金额限制
        limit_dic = Commission.get_agent_commission_plan_bo(site_code)

        currency_rate = Dao.currency_rate(site_code)
        agent_data = Dao.get_agent_list_data(site_code)
        user_dic = defaultdict(list)
        # 生成代理id与account\path的映射表
        agent_dic_1 = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_dic_2 = {_.agent_id: _.agent_account for _ in agent_data}

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone_sql)
        order_data = ms_context.get().session.query(OrderRecord.user_account, OrderRecord.currency,
                                                    OrderRecord.agent_acct,
                                                    func.sum(OrderRecord.valid_amount).label("valid_amount")). \
            filter(OrderRecord.site_code == site_code, OrderRecord.settle_time.between(start_time, end_time),
                   OrderRecord.agent_acct.isnot(None)). \
            group_by(OrderRecord.user_account, OrderRecord.agent_acct, OrderRecord.currency).all()

        for data in order_data:
            # 优先满足条件, 转为平台币
            platform_amount = data[3] / currency_rate[data[1]]
            limit = limit_dic[data[2]][query_type]["有效投注金额"]
            if platform_amount >= limit:
                agent_path = agent_dic_1[data[2]]
                for agent_id in agent_path:
                    user_dic[agent_dic_2[agent_id]].append(data[0])
        return user_dic

    @staticmethod
    def get_agent_venue_bet_data_dao(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日'):
        """
        查询基于代理和场馆维度的有效投注金额数据
        @return: {agent_acct: data_list}
        """
        data = Dao.query_order_data_sql(site_code, settle_start_diff=start_diff, settle_end_diff=end_diff,
                                        date_type=date_type, stop_diff=stop_diff). \
            filter(OrderRecord.agent_acct.isnot(None)).subquery()
        data = ms_context.get().session.query(data.c.venue_code, data.c.currency, data.c.agent_acct,
                                              func.sum(data.c.valid_amount).label("valid_amount")). \
            group_by(data.c.venue_code, data.c.currency, data.c.agent_acct).all()
        result = defaultdict(list)
        [result[_[2]].append(_) for _ in data]
        return result

    @staticmethod
    def get_valid_user_amount(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        有效活跃会员数量 - 充值和有效投注金额均满足条件
        :param query_type: 有效活跃 | 有效新增
        @return: {agent_account: 活跃会员数量}
        """
        # 充值满足条件的用户
        recharge_data = Commission._get_deposit_valid_user(site_code, '有效活跃', start_diff, end_diff, stop_diff,
                                                           date_type)
        # 打码满足条件的用户
        bet_data = Commission._get_bet_valid_user(site_code, '有效活跃', start_diff, end_diff, stop_diff, date_type)
        valid_user_dic = defaultdict(set)
        for name in set(recharge_data.keys()) & set(bet_data.keys()):
            valid_user_dic[name] = set(recharge_data[name]) & set(bet_data[name])
        data_dic = defaultdict(int)
        for name, value in valid_user_dic.items():
            data_dic[name] = len(value)
        return data_dic

    @staticmethod
    def get_new_valid_user_amount(site_code, date_diff=0, stop_diff=0, date_type='月'):
        """
        新增有效会员数 - 充值或流水满足条件
        @param site_code:
        @param date_diff:
        @param stop_diff:
        @param date_type:
        @return:
        """

        def get_data(diff=0):
            # 充值满足条件的用户
            recharge_data = Commission._get_deposit_valid_user(site_code, '有效新增', diff, diff, stop_diff, date_type)
            # 打码满足条件的用户
            bet_data = Commission._get_bet_valid_user(site_code, '有效新增', diff, diff, stop_diff, date_type)
            valid_dic = defaultdict(set)
            for _ in set(recharge_data.keys()) & set(bet_data.keys()):
                valid_dic[_] = set(recharge_data[_]) & set(bet_data[_])
            return valid_dic

        last_user_dic = get_data(date_diff - 1)
        current_user_dic = get_data(date_diff)
        valid_user_dic = defaultdict(int)
        for name in set(list(last_user_dic.keys()) + list(current_user_dic.keys())):
            valid_user_dic[name] = len(set(current_user_dic[name]) - set(last_user_dic[name]))
        return valid_user_dic

    @staticmethod
    def get_agent_commission_plan_bo(site_code, agent_account=""):
        """
        获取代理佣金方案配置中的有效活跃和有效新增限制条件
        @return: {agent_account: {"有效活跃": {"充值金额": 1, "有效投注金额": 2}}
        """
        cycle_dic = Dao.get_settle_cycle(to_zh=True)
        query_data = ms_context.get().session.query(AgentInfo.agent_account, AgentCommissionPlan). \
            join(AgentInfo, AgentInfo.plan_code == AgentCommissionPlan.plan_code). \
            filter(AgentCommissionPlan.site_code == site_code, AgentInfo.site_code == site_code).subquery()
        query_data_data = ms_context.get().session.query(AgentCommissionLadder.settle_cycle,
                                                         query_data.c.active_deposit,
                                                         query_data.c.active_bet, query_data.c.valid_deposit,
                                                         query_data.c.valid_bet, query_data.c.agent_account). \
            join(AgentCommissionLadder, AgentCommissionLadder.plan_id == query_data.c.id)
        if agent_account:
            query_data_data = query_data_data.filter(query_data.c.agent_account == agent_account)

        limit_dic = defaultdict(lambda: {"有效活跃": {"充值金额": Decimal(0), "有效投注金额": Decimal(0)},
                                         "有效新增": {"充值金额": Decimal(0), "有效投注金额": Decimal(0)}, "结算周期": ""})
        for _ in query_data_data.all():
            limit_dic[_[-1]] = {"有效活跃": {"充值金额": _[1], "有效投注金额": _[2]},
                                "有效新增": {"充值金额": _[3], "有效投注金额": _[4]}, "结算周期": cycle_dic[_[0]]}
        return limit_dic

    @staticmethod
    def get_agent_commission_ladder_dao(site_code, cycle_type, agent_account=""):
        """
        获取代理佣金方案配置中的分成阶梯配置
        :param cycle_type: 自然日 ｜ 自然月 ｜ 自然周
        @return: {agent_account: 阶梯配置记录}
        """
        cycle_type_dic = Dao.get_settle_cycle()
        query_data = ms_context.get().session.query(AgentInfo.agent_account, AgentCommissionPlan). \
            join(AgentInfo, AgentInfo.plan_code == AgentCommissionPlan.plan_code). \
            filter(AgentInfo.site_code == site_code).subquery()
        query_data = ms_context.get().session.query(query_data.c.agent_account, AgentCommissionLadder). \
            join(AgentCommissionLadder, query_data.c.id == AgentCommissionLadder.plan_id). \
            filter(AgentCommissionLadder.settle_cycle == cycle_type_dic[cycle_type])
        if agent_account:
            query_data = query_data.filter(AgentInfo.agent_account == agent_account)
        data = query_data.order_by(AgentCommissionLadder.rate.desc()).all()
        ladder_dic = defaultdict(list)
        [ladder_dic[agent_account].append(_) for agent_account, _ in data]

        return ladder_dic

    @staticmethod
    def get_agent_rebate_config_dao(site_code, cycle_type, agent_account=""):
        """
        获取代理佣金返点配置
        :param cycle_type: 自然日 ｜ 自然月 ｜ 自然周
        @return:
        """
        cycle_type_dic = Dao.get_settle_cycle()
        query_data = ms_context.get().session.query(AgentInfo.agent_account, AgentCommissionPlan). \
            join(AgentInfo, AgentInfo.plan_code == AgentCommissionPlan.plan_code). \
            filter(AgentInfo.site_code == site_code).subquery()
        query_data = ms_context.get().session.query(query_data.c.agent_account, AgentRebateConfig). \
            join(AgentRebateConfig, query_data.c.id == AgentRebateConfig.plan_id). \
            filter(AgentRebateConfig.settle_cycle == cycle_type_dic[cycle_type])
        if agent_account:
            query_data = query_data.filter(AgentInfo.agent_account == agent_account)
        return {agent_account: _ for agent_account, _ in query_data.all()}

    @staticmethod
    def get_last_commission_report_dao(site_code):
        """
        获取上个周期代理佣金结算表数据
        @return:
        """
        data = ms_context.get().session.query(func.row_number().over(
            partition_by=[AgentCommissionFinalReport.agent_account],
            order_by=AgentCommissionFinalReport.start_time.desc()).
                                              label('index'), AgentCommissionFinalReport.agent_account,
                                              AgentCommissionFinalReport.last_month_remain). \
            filter(AgentCommissionFinalReport.site_code == site_code).subquery()
        data = ms_context.get().session.query(data).filter(data.c.index == 1).all()
        result_data = defaultdict(Decimal)
        result_data.update({_[1]: _[2] for _ in data})
        return result_data

    @staticmethod
    def get_user_io_fee(site_code, fee_type, start_diff=None, end_diff=None, stop_diff=0, date_type='日',
                        currency='平台币'):
        """
        获取会员充提手续费    - 可转换为平台币
        :param fee_type: 佣金手续费 ｜ 方式手续费
        @return: defaultdict(lambda: {"充值手续费": Decimal(0), "提款手续费": Decimal(0), "总手续费": Decimal(0)})
        """
        trade_type = Dao.get_trade_type()
        # 平台币与主货币汇率
        coin_rate_dic = Dao.currency_rate(site_code)
        # 会员手续费
        if fee_type == '方式手续费':
            user_fee_data = ms_context.get().session.query(func.sum(UserDepositWithdrawal.way_fee_amount).
                                                           label('amount'), UserDepositWithdrawal.currency_code,
                                                           UserDepositWithdrawal.agent_account,
                                                           UserDepositWithdrawal.type)
        else:
            user_fee_data = ms_context.get().session.query(func.sum(UserDepositWithdrawal.settlement_fee_amount -
                                                                    UserDepositWithdrawal.fee_amount).label('amount'),
                                                           UserDepositWithdrawal.currency_code,
                                                           UserDepositWithdrawal.agent_account,
                                                           UserDepositWithdrawal.type)
        user_fee_data = user_fee_data.filter(UserDepositWithdrawal.site_code == site_code,
                                             UserDepositWithdrawal.status == 101,
                                             UserDepositWithdrawal.agent_account.isnot(None))
        if currency != '平台币':
            user_fee_data = user_fee_data.filter(UserDepositWithdrawal.currency_code == currency)
        if start_diff or start_diff == 0:
            timezone = Dao.get_site_timezone(site_code)
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            user_fee_data = user_fee_data.filter(UserDepositWithdrawal.updated_time.between(start_time, end_time))
        user_fee_data = user_fee_data.group_by(UserDepositWithdrawal.agent_account, UserDepositWithdrawal.currency_code,
                                               UserDepositWithdrawal.type)
        fee_dic = defaultdict(lambda: {"充值手续费": Decimal(0), "提款手续费": Decimal(0), "总手续费": Decimal(0)})
        for _ in user_fee_data:
            # 转为平台币
            fee = Decimal(_[0] / coin_rate_dic[_[1]]) if currency == '平台币' else _[0]

            fee_dic[_[2]]["总手续费"] += fee
            if _[3] == trade_type["存款"]:
                fee_dic[_[2]]["充值手续费"] += fee
            if _[3] == trade_type["取款"]:
                fee_dic[_[2]]["提款手续费"] += fee
        return fee_dic

    @staticmethod
    def get_agent_io_fee(site_code, fee_type, start_diff=None, end_diff=None, stop_diff=0, date_type='日',
                         currency='平台币'):
        """
        获取代理充提手续费
        :param fee_type: 佣金手续费 ｜方式手续费
        @return: defaultdict(lambda: {"充值手续费": Decimal(0), "提款手续费": Decimal(0), "总手续费": Decimal(0)})
        """
        trade_type = Dao.get_trade_type()
        # 平台币与主货币汇率
        coin_rate_dic = Dao.currency_rate(site_code)
        # 代理手续费
        if fee_type == '方式手续费':
            user_fee_data = ms_context.get().session.query(func.sum(AgentDepositWithdrawal.way_fee_amount).
                                                           label('amount'), AgentDepositWithdrawal.currency_code,
                                                           AgentDepositWithdrawal.agent_account,
                                                           AgentDepositWithdrawal.type)
        else:
            user_fee_data = ms_context.get().session.query(func.sum(AgentDepositWithdrawal.settlement_fee_amount -
                                                                    AgentDepositWithdrawal.fee_amount).label('amount'),
                                                           AgentDepositWithdrawal.currency_code,
                                                           AgentDepositWithdrawal.agent_account,
                                                           AgentDepositWithdrawal.type)
        user_fee_data = user_fee_data.filter(AgentDepositWithdrawal.site_code == site_code,
                                             AgentDepositWithdrawal.status == 101)
        if currency != '平台币':
            user_fee_data = user_fee_data.filter(AgentDepositWithdrawal.currency_code == currency)
        if start_diff or start_diff == 0:
            timezone = Dao.get_site_timezone(site_code)
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            user_fee_data = user_fee_data.filter(AgentDepositWithdrawal.updated_time.between(start_time, end_time))
        user_fee_data = user_fee_data.group_by(AgentDepositWithdrawal.agent_account,
                                               AgentDepositWithdrawal.currency_code, AgentDepositWithdrawal.type)
        fee_dic = defaultdict(lambda: {"充值手续费": Decimal(0), "提款手续费": Decimal(0), "总手续费": Decimal(0)})
        for _ in user_fee_data:
            # 转为平台币
            fee = Decimal(_[0]) / coin_rate_dic[_[1]] if currency != '平台币' else Decimal(_[0])
            fee_dic[_[2]]["总手续费"] += fee
            if _[3] == trade_type["存款"]:
                fee_dic[_[2]]["充值手续费"] += fee
            if _[3] == trade_type["取款"]:
                fee_dic[_[2]]["提款手续费"] += fee
        return fee_dic

    @staticmethod
    def get_agent_fee_for_commission(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日', currency='平台币'):
        """
        获取代理手续费总计，用充提方式算出的手续费 - 代理、会员已给的手续费    - 已叠加   - 可转换为平台币
        @return:
        """
        agent_data = Dao.get_agent_list_data(site_code)
        agent_account_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.agent_id: _.agent_account for _ in agent_data}

        fee_dic = defaultdict(lambda: {"会员存款手续费": Decimal(0), "会员提款手续费": Decimal(0),
                                       "代理存款手续费": Decimal(0), "代理提款手续费": Decimal(0),
                                       "总手续费": Decimal(0)})
        # 会员手续费
        user_fee_dic = Commission.get_user_io_fee(site_code, '佣金手续费', start_diff, end_diff, stop_diff, date_type,
                                                  currency)
        for agent_acct, value in user_fee_dic.items():
            fee_dic[agent_acct]["会员存款手续费"] += value["充值手续费"]
            fee_dic[agent_acct]["会员提款手续费"] += value["提款手续费"]
            fee_dic[agent_acct]["总手续费"] += value["总手续费"]
        agent_fee_dic = Commission.get_agent_io_fee(site_code, '佣金手续费', start_diff, end_diff, stop_diff, date_type,
                                                    currency)
        for agent_acct, value in agent_fee_dic.items():
            fee_dic[agent_acct]["代理存款手续费"] += value["充值手续费"]
            fee_dic[agent_acct]["代理提款手续费"] += value["提款手续费"]
            fee_dic[agent_acct]["总手续费"] += value["总手续费"]

        final_dic = defaultdict(lambda: {"会员存款手续费": Decimal(0), "会员提款手续费": Decimal(0),
                                         "代理存款手续费": Decimal(0), "代理提款手续费": Decimal(0), "总手续费": Decimal(0)})
        for agent_acct, value in fee_dic.items():
            agent_path = agent_account_dic[agent_acct]
            for agent_id in agent_path:
                sub_agent_account = agent_id_dic[agent_id]
                final_dic[sub_agent_account]["会员存款手续费"] += value["会员存款手续费"]
                final_dic[sub_agent_account]["会员提款手续费"] += value["会员提款手续费"]
                final_dic[sub_agent_account]["代理存款手续费"] += value["代理存款手续费"]
                final_dic[sub_agent_account]["代理提款手续费"] += value["代理提款手续费"]
                final_dic[sub_agent_account]["总手续费"] += value["总手续费"]
        return fee_dic

    @staticmethod
    def _get_commission_rate(site_code, bet_data, cycle_type, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取代理佣金比例
        @return:
        """
        ladder_dic = Commission.get_agent_commission_ladder_dao(site_code, cycle_type)
        # 1.有效活跃
        valid_live_user = Commission.get_valid_user_amount(site_code, start_diff, end_diff, stop_diff, date_type)
        # 2.有效新增
        new_valid_user = Commission.get_new_valid_user_amount(site_code, 0, stop_diff, date_type)
        # 3.输赢金额
        win_lose = bet_data[3]
        # 4.有效投注金额
        valid_amount_data = bet_data[2]
        # 5.计算
        agent_rate_dic = defaultdict(lambda: {"负盈利佣金比例": Decimal(0), "有效活跃": 0, "有效新增": 0, "输赢金额": 0,
                                              "有效投注金额": Decimal(0)})
        for agent_account in set(list(valid_live_user.keys()) + list(new_valid_user.keys()) + list(valid_amount_data)):
            agent_rate_dic[agent_account]["有效活跃"] = valid_live_user[agent_account]
            agent_rate_dic[agent_account]["有效新增"] = new_valid_user[agent_account]
            agent_rate_dic[agent_account]["输赢金额"] = round(win_lose[agent_account], 2)
            agent_rate_dic[agent_account]["有效投注金额"] = round(valid_amount_data[agent_account], 2)
            for ladder in ladder_dic[agent_account]:
                ladder: AgentCommissionLadder
                if win_lose[agent_account] >= ladder.win_loss_amount and \
                        valid_amount_data[agent_account] >= ladder.valid_amount and \
                        valid_live_user[agent_account] >= ladder.active_number and \
                        new_valid_user[agent_account] >= ladder.new_valid_number:
                    agent_rate_dic[agent_account]["负盈利佣金比例"] = Decimal(ladder.rate)
                    break
        return agent_rate_dic

    @staticmethod
    def _calc_venue_win_lose_by_agent(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                                      currency='平台币'):
        """
        计算出每个代理叠加后的输赢金额,平台币     - 可转换为平台币
        @return: {"agent_acct": {"venue_code": value}}
        """
        agent_data = Dao.get_agent_list_data(site_code)
        currency_rate = Dao.currency_rate(site_code)
        agent_account_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.id: _.agent_account for _ in agent_data}
        venue_bet_data = Dao.get_venue_win_lose_data_of_agent_dao(site_code, start_diff, end_diff, stop_diff,
                                                                  date_type, currency)

        # 统计场馆、币种数据 代理 - 场馆 - 币种
        venue_win_lose_dic = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: {"有效投注": Decimal(0),
                                                                                          "输赢金额": Decimal(0)})))
        final_dic = defaultdict(lambda: defaultdict(lambda: {"有效投注": Decimal(0), "输赢金额": Decimal(0)}))
        for agent_acct, value in venue_bet_data.items():
            # 币种不存在则跳过，脏数据
            if value[0] not in currency_rate:
                continue
            temp_currency = value[0]
            win_lose_amount = value[4]
            valid_amount = value[3]
            venue_code = value[2]
            agent_path = agent_account_dic[agent_acct]
            for agent_id in agent_path:
                if agent_id not in agent_id_dic:
                    continue
                sub_agent_account = agent_id_dic[agent_id]
                venue_win_lose_dic[sub_agent_account][venue_code][temp_currency]["输赢金额"] += win_lose_amount
                venue_win_lose_dic[sub_agent_account][venue_code][temp_currency]["有效投注"] += valid_amount
        # 将输赢金额转为平台币 代理 - 场馆
        for agent_acct, data_1 in venue_win_lose_dic.items():
            for venue_code, data_2 in data_1.items():
                for temp_currency, value in data_2.items():
                    if currency == '平台币':
                        final_dic[agent_acct][venue_code]["输赢金额"] += value["输赢金额"] / currency_rate[temp_currency]
                        final_dic[agent_acct][venue_code]["有效投注"] += value["有效投注"] / currency_rate[temp_currency]
                    else:
                        final_dic[agent_acct][venue_code]["输赢金额"] += value["输赢金额"]
                        final_dic[agent_acct][venue_code]["有效投注"] += value["有效投注"]
        return final_dic

    @staticmethod
    def calc_venue_fee_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', currency='平台币'):
        """
        计算场馆费 - 已按代理叠加   - 可转换为平台币
        @return: {"agent_acct": {"场馆费": 1, "明细": {场馆, 有效投注, 场馆费比例,场馆费金额}}}
        """
        venue_win_lose_dic = Commission._calc_venue_win_lose_by_agent(site_code, start_diff, end_diff, stop_diff,
                                                                      date_type, currency)
        venue_data = Dao.get_venue_info_dao()
        venue_name_dic = {_.venue_code: _.venue_name for _ in venue_data}

        # 场馆费率
        venue_rate_dic = {_.venue_code: _.handling_fee for _ in Dao.get_site_venue_rate_dao(site_code)}
        venue_fee_dic = defaultdict(lambda: {"场馆费": Decimal(0), "场馆费明细": []})
        for agent_acct, venue_data in venue_win_lose_dic.items():
            for venue_code, value in venue_data.items():
                win_lose_amount = value["输赢金额"]
                valid_amount = value["有效投注"]
                # 手续费
                fee = win_lose_amount * venue_rate_dic[venue_code]
                # 小于0 则无手续费
                if fee <= 0:
                    continue
                venue_fee_dic[agent_acct]["场馆费"] += fee
                venue_fee_dic[agent_acct]["场馆费明细"].append({"场馆": venue_name_dic[venue_code],
                                                           "有效投注": valid_amount,
                                                           "场馆费比例": venue_rate_dic[value[2]], "场馆费金额": fee})
        return venue_fee_dic

    @staticmethod
    def calc_vip_act_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', currency='平台币'):
        """
        计算VIP优惠和活动优惠数据 - 已按代理叠加    - 可转换为平台币
        @return: {"agent_account": {"活动优惠": Decimal(0), "VIP福利": Decimal(0)}}
        """
        currency_rate = Dao.currency_rate(site_code)
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff, date_type). \
            subquery()
        data = ms_context.get().session.query(vip_act_data.c.agent_name, vip_act_data.c.main_currency,
                                              func.sum(vip_act_data.c.vip), func.sum(vip_act_data.c.act))
        if currency != '平台币':
            data = data.filter(vip_act_data.c.main_currency == currency)
        data = data.group_by(vip_act_data.c.agent_name, vip_act_data.c.main_currency).all()

        result_dic = defaultdict(lambda: {"活动优惠": Decimal(0), "VIP福利": Decimal(0)})
        for _ in data:
            act_amount = _[3] if currency != '平台币' else _[3] / currency_rate[_[1]]
            vip_amount = _[2] if currency != '平台币' else _[2] / currency_rate[_[1]]
            result_dic[_[0]]["活动优惠"] = act_amount
            result_dic[_[0]]["VIP福利"] = vip_amount
        return result_dic

    # @staticmethod
    # def _calc_used_profit(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', currency='平台币'):
    #     """
    #     计算已使用优惠 - 已按代理叠加，手动转换的主货币
    #     @return: {"agent_account": {"活动优惠": Decimal(0), "VIP福利": Decimal(0)}}
    #     """
    #     currency_rate = Dao.currency_rate(site_code)
    #
    #     used_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
    #                                                          date_type).subquery()
    #     used_profit_data = ms_context.get().session.query(used_data.c.agent_account, used_data.c.currency,
    #                                                       func.sum(used_data.c.amount)). \
    #         group_by(used_data.c.agent_account, used_data.c.currency).all()
    #     used_profit_dic = defaultdict(Decimal)
    #     # 将主货币转为平台币
    #     for _ in used_profit_data:
    #         value = _[2] if currency != '平台币' else _[2] / currency_rate[_[1]]
    #         used_profit_dic[_[0]] += value
    #     return used_profit_dic
    #
    # @staticmethod
    # def _calc_received_vip_act_discount(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
    #                                     currency='平台币'):
    #     """
    #     领取到的主货币部分的 VIP + 活动优惠
    #     @return:
    #     """
    #     data = Dao.get_vip_act_discount_data_base(site_code, start_diff, end_diff, stop_diff, date_type, currency). \
    #         subquery()
    #     data = ms_context.get().session.query(data.c.agent_name, data.c.currency,
    #                                           func.sum(data.c.amount).label("amount")). \
    #         group_by(data.c.agent_name, data.c.currency).all()
    #     main_currency_profit_dic = defaultdict(Decimal)
    #     currency_rate = Dao.currency_rate(site_code)
    #     # 将主货币转为平台币
    #     for _ in data:
    #         value = _[2] if currency != '平台币' else _[2] / currency_rate[_[1]]
    #         main_currency_profit_dic[_[0]] += value
    #     return main_currency_profit_dic
    #
    # @staticmethod
    # def calc_used_profit_commission_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
    #                                    currency='平台币'):
    #     """
    #     计算已使用优惠 - 已按代理叠加，包括： 手动转换的主货币 + 领取时直接发的主货币
    #     @return: {"agent_account": {"活动优惠": Decimal(0), "VIP福利": Decimal(0)}}
    #     """
    #     used_profit_dic = defaultdict(Decimal)
    #     data_1 = Commission._calc_used_profit(site_code, start_diff, end_diff, stop_diff, date_type, currency)
    #     data_2 = Commission._calc_received_vip_act_discount(site_code, start_diff, end_diff, stop_diff, date_type,
    #                                                         currency)
    #     for _, value in data_1.items():
    #         used_profit_dic[_] += value
    #     for _, value in data_2.items():
    #         used_profit_dic[_] += value
    #     return used_profit_dic

    @staticmethod
    def calc_used_profit_commission_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                                       currency='平台币'):
        """
        计算已使用优惠 - 已按代理叠加，包括： 手动转换的主货币 + 领取时直接发的主货币    - 可转换为平台币
        @return: {"agent_account": {"活动优惠": Decimal(0), "VIP福利": Decimal(0)}}
        """
        used_profit_dic = defaultdict(Decimal)
        currency_rate = Dao.currency_rate(site_code)
        used_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
                                                             date_type).subquery()
        used_profit_data = ms_context.get().session.query(used_data.c.agent_account, used_data.c.currency,
                                                          func.sum(used_data.c.amount).label('amount'))
        if currency != '平台币':
            used_profit_data = used_profit_data.filter(used_data.c.currency == currency)
        used_profit_data = used_profit_data.group_by(used_data.c.agent_account, used_data.c.currency)
        for _ in used_profit_data:
            used_profit_dic[_[0]] = _[2] if currency != '平台币' else _[2] / currency_rate[_[1]]
        return used_profit_dic

    @staticmethod
    def calc_adjust_data_bo(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', currency='平台币'):
        """
        计算调整金额 - 已按代理叠加: VIP福利、活动优惠, 不包括 其他调整
        @return: {"agent_account": Decimal(0)}
        """
        currency_rate = Dao.currency_rate(site_code)
        adjust_dic = defaultdict(Decimal)
        adjust = Dao.get_adjust_data_base(site_code, start_diff, end_diff, stop_diff, date_type).subquery()
        adjust_data = ms_context.get().session.query(adjust.c.agent_name, adjust.c.currency, func.sum(adjust.c.amount))
        if currency != '平台币':
            adjust_data = adjust_data.filter(adjust.c.currency == currency)
        adjust_data = adjust_data.group_by(adjust.c.agent_name, adjust.c.currency).all()
        for _ in adjust_data:
            value = _[2] if currency != '平台币' else _[2] / currency_rate[_[1]]
            adjust_dic[_[0]] += value
        return adjust_dic

    @staticmethod
    def _get_vip_act_data_for_commission(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        VIP福利和活动优惠 - 按代理叠加
        @return:
        """
        agent_data = Dao.get_agent_list_data(site_code)
        agent_account_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.id: _.agent_account for _ in agent_data}
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff, date_type). \
            subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.agent_name,
                                                      func.sum(vip_act_data.c.vip), func.sum(vip_act_data.c.act)). \
            group_by(vip_act_data.c.date).all()

        vip_data_dic = defaultdict(Decimal)
        act_data_dic = defaultdict(Decimal)
        for _ in vip_act_data:
            agent_path = agent_account_dic[_[0]]
            for agent_id in agent_path:
                sub_agent_account = agent_id_dic[agent_id]
                vip_data_dic[sub_agent_account] += _[3]
                act_data_dic[sub_agent_account] += _[2]
        return vip_data_dic, act_data_dic

    @staticmethod
    def calc_win_loss_commission_dao(site_code, cycle_type=None, specify_agent=None, start_diff=0, end_diff=0,
                                     stop_diff=0, currency="平台币"):
        """
        负盈利佣金
        :param cycle_type  自然日 ｜ 自然月 ｜ 自然周
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        if cycle_type:
            date_type = cycle_type[-1]
        else:
            cycle_type = Commission.get_agent_commission_plan_bo(site_code, specify_agent)[specify_agent]["结算周期"]
            date_type = cycle_type[-1]
        result_dic = defaultdict(lambda: {"平台总输赢": Decimal(0), "场馆费": Decimal(0), "总手续费": Decimal(0),
                                          "上期待冲正金额": Decimal(0), "VIP福利": Decimal(0), "活动优惠": Decimal(0),
                                          "负盈利佣金比例": Decimal(0), "已使用优惠": Decimal(0),
                                          "负盈利佣金": Decimal(0), "账号类型": None, "总投注金额": Decimal(0),
                                          "总注单量": Decimal(0), "本期会员净输赢": Decimal(0), "本期待冲正金额": Decimal(0),
                                          "有效活跃": Decimal(0), "有效新增": Decimal(0), "会员总输赢": Decimal(0),
                                          "有效投注金额": Decimal(0), "会员存款手续费": Decimal(0),
                                          "代理类型": "负盈利代理", "会员提款手续费": Decimal(0), "会员调整": Decimal(0),
                                          "代理存款手续费": Decimal(0), "代理提款手续费": Decimal(0),
                                          "场馆费明细": [], "结算时间范围": []})
        # 1.平台总输赢 ： -(会员输赢 + 提前结算)
        win_lose_dic = Dao.get_agent_order_summary(site_code, start_diff, end_diff, stop_diff, date_type, currency)
        for _ in win_lose_dic[3].items():
            result_dic[_[0]]["平台总输赢"] = round(-_[1], 2)
            result_dic[_[0]]["会员总输赢"] = round(_[1], 2)

        for _ in win_lose_dic[1].items():
            result_dic[_[0]]["总投注金额"] = round(_[1], 2)
        for _ in win_lose_dic[0].items():
            result_dic[_[0]]["总注单量"] = _[1]
        win_lose_dic = win_lose_dic[3]
        # 2.场馆费
        venue_fee_dic = Commission.calc_venue_fee_bo(site_code, start_diff, end_diff, stop_diff, date_type, currency)
        for _ in venue_fee_dic.items():
            result_dic[_[0]]["场馆费"] = round(_[1]["场馆费"], 2)
            result_dic[_[0]]["场馆费明细"] = _[1]["场馆费明细"]
        # 3.存提手续费
        io_fee = Commission.get_agent_fee_for_commission(site_code, start_diff, end_diff, stop_diff, date_type,
                                                         currency)
        for _ in io_fee.items():
            result_dic[_[0]]["总手续费"] = round(_[1]["总手续费"], 2)
            result_dic[_[0]]["会员存款手续费"] = round(_[1]["会员存款手续费"], 2)
            result_dic[_[0]]["会员提款手续费"] = round(_[1]["会员提款手续费"], 2)
            result_dic[_[0]]["代理存款手续费"] = round(_[1]["代理存款手续费"], 2)
            result_dic[_[0]]["代理提款手续费"] = round(_[1]["代理提款手续费"], 2)
        # 4.上期待冲正金额
        last_remain = Commission.get_last_commission_report_dao(site_code)
        # 5.VIP福利和活动优惠
        vip_act_data = Commission.calc_vip_act_bo(site_code, start_diff, end_diff, stop_diff, date_type, currency)
        for _ in vip_act_data.items():
            result_dic[_[0]]["活动优惠"] = round(_[1]["活动优惠"], 2)
            result_dic[_[0]]["VIP福利"] = round(_[1]["VIP福利"], 2)
        # 6.已使用优惠
        used_profit_dic = Commission.calc_used_profit_commission_bo(site_code, start_diff, end_diff, stop_diff,
                                                                    date_type, currency)
        for _ in used_profit_dic.items():
            result_dic[_[0]]["已使用优惠"] = _[1]
        # 7.调整金额,包括: VIP福利、活动优惠   不包括：其他调整
        adjust_dic = Commission.calc_adjust_data_bo(site_code, start_diff, end_diff, stop_diff, date_type, currency)
        for _ in adjust_dic.items():
            result_dic[_[0]]["会员调整"] = round(_[1], 2)
        # 8.本期会员净输赢
        for _, data in result_dic.items():
            # 会员总输赢-场馆费-平台币钱包转化金额-存提手续费-会员调整（VIP福利、活动优惠、其他调整）
            result_dic[_]["本期会员净输赢"] = round(data["平台总输赢"] - data["场馆费"] - data["已使用优惠"] -
                                             data["总手续费"] - data["会员调整"], 2)

        # 9.各代理的佣金比例
        bet_data = Dao.get_agent_order_summary(site_code, start_diff, end_diff, stop_diff, date_type)
        agent_rate_dic = Commission._get_commission_rate(site_code, bet_data, cycle_type, start_diff, end_diff,
                                                         stop_diff, date_type)
        [result_dic[acct].update(data) for acct, data in agent_rate_dic.items() if acct in agent_rate_dic]

        # 10.挑选出负盈利指定周期的代理
        ladder_list = Commission.get_agent_commission_ladder_dao(site_code, cycle_type)
        agent_list = list(ladder_list.keys())

        # 11.计算佣金  （平台总输赢 - 平台币转化金额 - 场馆费 - 存提手续费 + 上期待冲正金额 - 调整金额）* 返佣比例
        for agent_account in agent_list:
            start_day, end_day = DateUtil.get_day_range(date_type, start_diff, stop_diff, timezone)
            result_dic[agent_account]["结算时间范围"] = [start_day, end_day]

            final_net_win_lose = win_lose_dic[agent_account] - used_profit_dic[agent_account] - venue_fee_dic[
                agent_account]["场馆费"] - io_fee[agent_account]["总手续费"] + last_remain[agent_account]
            result_dic[agent_account]["上期待冲正金额"] = last_remain[agent_account]
            result_dic[agent_account]["负盈利佣金比例"] = agent_rate_dic[agent_account]['负盈利佣金比例']
            result_dic[agent_account]["平台总输赢"] = round(win_lose_dic[agent_account], 2)
            result_dic[agent_account]["已使用优惠"] = used_profit_dic[agent_account]
            # 冲正净输赢为负，则遗留到待充正金额
            if final_net_win_lose <= 0:
                result_dic[agent_account]["负盈利佣金"] = Decimal(0)
                result_dic[agent_account]["本期待冲正金额"] = final_net_win_lose.quantize(Decimal("0.00"))
            else:
                # print('*' * 10)
                # print(final_net_win_lose)
                # print(type(final_net_win_lose))
                # print(type(agent_rate_dic[agent_account]['负盈利佣金比例']))
                result_dic[agent_account]["负盈利佣金"] = final_net_win_lose * agent_rate_dic[agent_account][
                    '负盈利佣金比例']
                result_dic[agent_account]["本期待冲正金额"] = Decimal(0)
        return {k: v for k, v in result_dic.items() if k in agent_list}

    # @staticmethod
    # def get_win_loss_commission_by_cycle_dao(site_code, ):

    @staticmethod
    def _calc_head_rebate_commission(site_code, cycle_type, date_diff=0, stop_diff=0, date_type='日'):
        """
        计算代理有效新增人头费
        @return:
        """
        calc_type = Dao.get_settle_cycle(to_zh=True)
        result_dic = defaultdict(lambda: {"有效新增人头费": Decimal(0), "结算周期": "", "有效新增人头费/人": Decimal(0),
                                          "有效新增人数": Decimal(0)})
        # 返点配置
        rebate_config = Commission.get_agent_rebate_config_dao(site_code, cycle_type)
        # 有效新增人头费
        new_valid_user = Commission.get_new_valid_user_amount(site_code, date_diff, stop_diff, date_type)
        for agent_acct in new_valid_user:
            if agent_acct in rebate_config:
                agent_config = rebate_config[agent_acct]
                if agent_config:
                    agent_config: AgentRebateConfig
                    new_cnt = new_valid_user[agent_acct]
                    result_dic[agent_acct].update({"有效新增人头费": agent_config.new_user_amount * new_cnt,
                                                   "结算周期": calc_type[agent_config.settle_cycle],
                                                   "有效新增人头费/人": agent_config.new_user_amount,
                                                   "有效新增人数": new_cnt})
        return result_dic

    @staticmethod
    def _calc_venue_rebate_commission(site_code, cycle_type, date_diff=0, stop_diff=0, date_type='月'):
        """
        计算代理场馆返点佣金
        @return: 汇总值，包括明细值
        """
        # date_type = cycle_type[-1]
        # 平台币与主货币汇率
        coin_rate_dic = Dao.currency_rate(site_code)
        calc_type = Dao.get_settle_cycle(to_zh=True)
        result_dic = defaultdict(lambda: {"各场馆有效流水": defaultdict(Decimal), "结算周期": "",
                                          "有效流水返点": Decimal(0), "有效流水": Decimal(0), "返点明细": []})
        # 返点配置
        rebate_config = Commission.get_agent_rebate_config_dao(site_code, cycle_type)
        # 各场馆有效流水
        venue_valid_amount_data = Commission.get_agent_venue_bet_data_dao(site_code, date_diff, date_diff, stop_diff,
                                                                          date_type)
        # 场馆分类
        venue_data = Dao.get_venue_info_dao()
        venue_type_dic = {_.venue_code: _.venue_type for _ in venue_data}
        venue_type_name_dic = Dao.get_venue_type(to_zh=True)

        # 遍历所有代理数据
        for agent_acct, data in venue_valid_amount_data.items():
            # 代理打码配置
            if agent_acct not in rebate_config:
                continue
            agent_config = rebate_config[agent_acct]
            if agent_config:
                agent_config: AgentRebateConfig
                # 遍历代理下所有场馆数据
                for _ in data:
                    venue_type = venue_type_dic[_[0]]
                    valid_amount = _[3] / coin_rate_dic[_[1]]
                    result_dic[agent_acct]["各场馆有效流水"][venue_type] += valid_amount
                    result_dic[agent_acct]["有效流水"] += valid_amount
                    result_dic[agent_acct]["结算周期"] = calc_type[agent_config.settle_cycle]
        # 算佣金
        for agent_acct in result_dic:
            # 代理打码配置
            agent_config = rebate_config[agent_acct]
            rate_dic = {"1": agent_config.sports_rate, "2": agent_config.live_rate, "3": agent_config.chess_rate,
                        "4": agent_config.slot_rate, "5": agent_config.lottery_rate,
                        "6": agent_config.cockfight_rate, "7": agent_config.esports_rate}
            venue_data_dic = result_dic[agent_acct]["各场馆有效流水"]
            for venue_type, valid_amount in venue_data_dic.items():
                venue_type_name = venue_type_name_dic[venue_type]
                rate = rate_dic[venue_type]
                amount = valid_amount * rate
                result_dic[agent_acct]['返点明细'][venue_type_name]. \
                    append({"场馆类型": venue_type_name, "有效流水": valid_amount, "返点比例": rate, "返点金额": amount})
                result_dic[agent_acct]["有效流水返点"] += amount  # 看是否需要处以100
        return result_dic

    @staticmethod
    def calc_rebate_commission_dao(site_code, cycle_type=None, specify_agent=None, date_diff=0, stop_diff=0):
        """
        计算代理返点佣金
        @return:
        """
        if cycle_type:
            date_type = cycle_type[-1]
        else:
            cycle_type = Commission.get_agent_commission_plan_bo(site_code, specify_agent)[specify_agent]["结算周期"]
            date_type = cycle_type[-1]

        head_rebate = Commission._calc_head_rebate_commission(site_code, cycle_type, date_diff, stop_diff, date_type)
        venue_rebate = Commission._calc_venue_rebate_commission(site_code, cycle_type, date_diff, stop_diff, date_type)
        result_data = defaultdict(lambda: {"有效新增人头费": Decimal(0), "结算周期": "", "有效新增人头费/人": Decimal(0),
                                           "有效新增人数": Decimal(0), "各场馆有效流水": defaultdict(Decimal),
                                           "有效流水返点": Decimal(0), "有效流水": Decimal(0), "返点明细": [],
                                           "总返点": Decimal(0)})
        for agent_acct, data in head_rebate.items():
            result_data[agent_acct]['总返点'] += data['有效新增人头费']
            for key, value in data.items():
                result_data[agent_acct][key] = value
        for agent_acct, data in venue_rebate.items():
            result_data[agent_acct]["各场馆有效流水"] = data['各场馆有效流水']
            result_data[agent_acct]["结算周期"] = data['结算周期']
            result_data[agent_acct]["有效流水返点"] += data['有效流水返点']
            result_data[agent_acct]["有效流水"] = data['有效流水']
            result_data[agent_acct]['总返点'] += data['有效流水返点']
            result_data[agent_acct]['返点明细'] += data['返点明细']
        return result_data

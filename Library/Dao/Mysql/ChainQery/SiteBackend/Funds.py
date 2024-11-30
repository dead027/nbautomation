#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 17:41
import time
from collections import defaultdict
from decimal import Decimal

from Library.MysqlTableModel.system_currency_info_model import SystemCurrencyInfo
from Library.MysqlTableModel.user_typing_amount_model import UserTypingAmount
from Library.MysqlTableModel.user_coin_model import UserCoin
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.user_coin_record_model import UserCoinRecord
from Library.MysqlTableModel.site_currency_info_model import SiteCurrencyInfo
from Library.MysqlTableModel.agent_commission_coin_model import AgentCommissionCoin
from Library.MysqlTableModel.agent_quota_coin_model import AgentQuotaCoin
from Library.MysqlTableModel.user_typing_amount_record_model import UserTypingAmountRecord
from Library.MysqlTableModel.user_manual_up_down_record_model import UserManualUpDownRecord
from Library.MysqlTableModel.agent_manual_up_down_record_model import AgentManualUpDownRecord
from Library.MysqlTableModel.user_deposit_withdrawal_model import UserDepositWithdrawal
from Library.MysqlTableModel.user_withdraw_config_model import UserWithdrawConfig
from Library.MysqlTableModel.user_platform_coin_model import UserPlatformCoin
from Library.MysqlTableModel.user_platform_coin_record_model import UserPlatformCoinRecord
from Library.MysqlTableModel.user_platform_transfer_record_model import UserPlatformTransferRecord

from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from sqlalchemy import update, insert, func, and_
from Library.Common.Enum.FundsEnum import FundsEnum
from Library.Common.Enum.PlatformEnum import PlatformEnum
from sqlalchemy.orm import Session
from Library.Dao.Mysql.ChainQery.SiteBackend.Agent import Agent
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site


class Funds(object):

    @staticmethod
    def get_crypto_rate_sql(currency="", io_direct=""):
        """
        获取虚拟币汇率
        :param currency: 币种
        :param io_direct: 取款 ｜ 存款
        :return:
        """
        io_dic = {"存款": 1, "取款": 2}
        data = ms_context.get().session.query(SystemCurrencyInfo)
        if currency:
            data = data.filter(SystemCurrencyInfo.currency_code == currency)
        if io_direct:
            data = data.filter(SystemCurrencyInfo.adjust_way == io_dic[io_direct])
        return data.all()

    @staticmethod
    def get_user_typing_amount_dao(site_code, user_account):
        """
        获取会员剩余打码量
        :return:
        """
        data: UserTypingAmount = ms_context.get().session.query(UserTypingAmount). \
            filter(UserTypingAmount.site_code == site_code, UserTypingAmount.user_account == user_account).first()
        return data.typing_amount

    @staticmethod
    def wait_until_user_typing_amount_change_to(site_code, user_account, amount, timeout=5):
        """
        等待会员剩余打码量变为指定值
        @return:
        """
        end_time = start_time = int(time.time())
        current_balance = 0
        while end_time - start_time < timeout:
            balance = Funds.get_user_typing_amount_dao(site_code, user_account)
            current_balance = balance
            if balance == amount:
                return
            end_time = int(time.time())
            time.sleep(0.2)
        raise AssertionError(f'{user_account} 在 {timeout}内余额未变为: {amount}, 当前余额: {current_balance}')

    @staticmethod
    def get_user_typing_record(site_code, start_diff, end_diff, register_info=None, order_no=None, adjust_way=None,
                               adjust_type=None, value_min=None, value_max=None):
        """
        获取会员打码量记录
        @param start_diff:
        @param end_diff:
        @param register_info:
        @param order_no:
        @param site_code:
        @param adjust_way: 增加 ｜ 扣除
        @param adjust_type:  1人工增加流水 2人工清除流水 3系统自动清除 4投注扣减流水 5活动增加流水 6充值添加流水 7返水添加流水
                            8VIP奖励添加流水
        @param value_min:
        @param value_max:
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, timezone=timezone)
        data: UserTypingAmountRecord = ms_context.get().session.query(UserTypingAmountRecord). \
            filter(UserTypingAmountRecord.created_time.between(start_time, end_time),
                   UserTypingAmountRecord.site_code == site_code)
        if register_info:
            data.filter(UserTypingAmountRecord.user_register == register_info)
        if order_no:
            data.filter(UserTypingAmountRecord.order_no == order_no)
        if register_info:
            data.filter(UserTypingAmountRecord.user_register == register_info)
        if adjust_way:
            data.filter(UserTypingAmountRecord.user_register == FundsEnum.typing_adjust_way_dic_f_zh.value[adjust_way])
        if adjust_type:
            data.filter(UserTypingAmountRecord.adjust_type == FundsEnum.typing_adjust_type_dic_f_zh.value[adjust_type])
        if value_min:
            data.filter(UserTypingAmountRecord.coin_value >= value_min)
        if value_max:
            data.filter(UserTypingAmountRecord.coin_value <= value_max)
        return data.all()

    @staticmethod
    def get_user_manual_order_list_sql(site_code, adjust_way=None, order_no=None, user_account=None, user_name=None,
                                       order_status=None, adjust_type=None, amount_min=None, amount_max=None,
                                       apply_start_diff=0, apply_end_diff=0, stop_diff=0, date_type='日'):
        """
        获取会员人工加减额记录
        adjust_way: 调整方向： 人工增加额度 ｜ 人工扣除额度
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(apply_start_diff, apply_end_diff, stop_diff, date_type,
                                                            timezone)
        data = ms_context.get().session.query(UserManualUpDownRecord). \
            filter(UserManualUpDownRecord.site_code == site_code)
        if adjust_way == "人工增加额度":
            data = data.filter(UserManualUpDownRecord.apply_time.between(start_time, end_time),
                               UserManualUpDownRecord.adjust_way == System.get_manual_adjust_way(adjust_way))
        elif adjust_way == "人工扣除额度":
            data = data.filter(UserManualUpDownRecord.created_time.between(start_time, end_time),
                               UserManualUpDownRecord.adjust_way == System.get_manual_adjust_way(adjust_way))

        if order_no:
            data = data.filter(UserManualUpDownRecord.order_no == order_no)
        if user_account:
            data = data.filter(UserManualUpDownRecord.user_account == user_account)
        if user_name:
            data = data.filter(UserManualUpDownRecord.user_name == user_name)
        if order_status:
            data = data.filter(UserManualUpDownRecord.order_status == System.get_review_status(order_status))
        if adjust_type:
            data = data.filter(UserManualUpDownRecord.adjust_type == System.get_manual_up_type(adjust_type))
        if amount_min:
            data = data.filter(UserManualUpDownRecord.adjust_amount >= amount_min)
        if amount_max:
            data = data.filter(UserManualUpDownRecord.adjust_amount <= amount_max)
        data = data.order_by(UserManualUpDownRecord.apply_time.desc())
        return data.all()

    @staticmethod
    def get_agent_manual_order_list_sql(site_code, adjust_way=None, order_no=None, agent_account=None,
                                        order_status=None, adjust_type=None, amount_min=None, amount_max=None,
                                        apply_start_diff=0, apply_end_diff=0, stop_diff=0, date_type='日'):
        """
        获取代理人工加减额记录
        adjust_way: 调整方向： 人工增加额度 ｜ 人工扣除额度
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(apply_start_diff, apply_end_diff, stop_diff, date_type,
                                                            timezone)
        data = ms_context.get().session.query(AgentManualUpDownRecord). \
            filter(AgentManualUpDownRecord.site_code == site_code)
        if adjust_way == "人工增加额度":
            data = data.filter(AgentManualUpDownRecord.apply_time.between(start_time, end_time),
                               AgentManualUpDownRecord.adjust_way == System.get_manual_adjust_way(adjust_way))
        elif adjust_way == "人工扣除额度":
            data = data.filter(AgentManualUpDownRecord.created_time.between(start_time, end_time),
                               AgentManualUpDownRecord.adjust_way == System.get_manual_adjust_way(adjust_way))

        if order_no:
            data = data.filter(AgentManualUpDownRecord.order_no == order_no)
        if agent_account:
            data = data.filter(AgentManualUpDownRecord.agent_account == agent_account)
        if order_status:
            data = data.filter(AgentManualUpDownRecord.order_status == System.get_review_status(order_status))
        if adjust_type:
            data = data.filter(AgentManualUpDownRecord.adjust_type == System.get_manual_up_type(adjust_type))
        if amount_min:
            data = data.filter(AgentManualUpDownRecord.adjust_amount >= amount_min)
        if amount_max:
            data = data.filter(AgentManualUpDownRecord.adjust_amount <= amount_max)
        data = data.order_by(AgentManualUpDownRecord.apply_time.desc())
        return data.all()

    #
    # @staticmethod
    # def get_user_manual_order_info_sql(order_no):
    #     """
    #     获取会员人工加减额订单详情
    #     :param order_no:
    #     :return:
    #     """
    #     data = ms_context.get().session.query(UserManualUpDownRecord). \
    #         filter(UserManualUpDownRecord.order_no == order_no)
    #     return data.first()
    #
    # @staticmethod
    # def wait_until_manual_order_exists(order_no, timeout=5):
    #     """
    #     等待人工审核订单产生
    #     @param order_no:
    #     @param timeout:
    #     @return:
    #     """
    #     session: Session = ms_context.get().session
    #     end_time = start_time = int(time.time())
    #     while end_time - start_time < timeout:
    #         session.expire_all()
    #         data = session.query(UserManualUpDownRecord).filter(UserManualUpDownRecord.order_no == order_no).all()
    #         if list(data):
    #             return
    #         end_time = int(time.time())
    #         time.sleep(0.2)
    #     raise AssertionError(f'{order_no} 在 {timeout}内未生成')

    @staticmethod
    def get_agent_commission_balance(site_code, agent_account=""):
        """
        获取佣金钱包余额
        @return: 总额，冻结金额，可用金额
        """
        session: Session = ms_context.get().session
        data: UserCoin = session.query(AgentCommissionCoin).filter(AgentCommissionCoin.site_code == site_code)
        if agent_account:
            data = data.filter(AgentCommissionCoin.agent_account == agent_account).first()
            return data.total_amount, data.freeze_amount, data.available_amount
        else:
            return {_.agent_account: (data.total_amount, data.freeze_amount, data.available_amount) for _ in data.all()}

    @staticmethod
    def wait_until_agent_commission_balance_change_to(site_code, agent_account, amount, timeout=5):
        """
        等待代理佣金余额变为指定值
        @return:
        """
        end_time = start_time = int(time.time())
        current_balance = 0
        while end_time - start_time < timeout:
            balance = Funds.get_agent_commission_balance(site_code, agent_account)[2]
            current_balance = balance
            if balance[0] == amount:
                return
            end_time = int(time.time())
            time.sleep(0.2)
        raise AssertionError(f'{agent_account} 在 {timeout}内余额未变为: {amount}, 当前余额: {current_balance}')

    @staticmethod
    def get_agent_quota_balance(site_code, agent_account=""):
        """
        获取额度钱包余额
        @return: 总额，冻结金额，可用金额
        """
        session: Session = ms_context.get().session
        data: UserCoin = session.query(AgentQuotaCoin).filter(AgentQuotaCoin.site_code == site_code)
        if agent_account:
            data = data.filter(AgentQuotaCoin.agent_account == agent_account).first()
            return data.total_amount, data.freeze_amount, data.available_amount
        else:
            return {_.agent_account: (data.total_amount, data.freeze_amount, data.available_amount) for _ in data.all()}

    @staticmethod
    def wait_until_agent_quota_balance_change_to(site_code, agent_account, amount, timeout=5):
        """
        等待代理额度钱包余额变为指定值
        @return:
        """
        end_time = start_time = int(time.time())
        current_balance = 0
        while end_time - start_time < timeout:
            balance = Funds.get_agent_quota_balance(site_code, agent_account)[2]
            current_balance = balance
            if balance[0] == amount:
                return
            end_time = int(time.time())
            time.sleep(0.2)
        raise AssertionError(f'{agent_account} 在 {timeout}内余额未变为: {amount}, 当前余额: {current_balance}')

    @staticmethod
    def get_user_balance_dao(site_code, user_account):
        """
        获取会员余额
        @param site_code:
        @param user_account:
        @return: 总额，冻结金额，可用金额
        """
        session: Session = ms_context.get().session
        data: UserCoin = session.query(UserCoin).filter(UserCoin.user_account == user_account,
                                                        UserCoin.site_code == site_code).first()
        if data:
            return data.total_amount, data.freeze_amount, data.available_amount
        else:
            return 0, 0, 0

    @staticmethod
    def wait_until_user_balance_change_to_dao(site_code, user_account, amount, timeout=5):
        """
        等待会员余额变为指定值
        @return:
        """
        end_time = start_time = int(time.time())
        current_balance = 0
        while end_time - start_time < timeout:
            balance = Funds.get_user_balance_dao(site_code, user_account)[0]
            current_balance = balance
            if balance == amount:
                return
            end_time = int(time.time())
            time.sleep(0.2)
        raise AssertionError(f'{user_account} 在 {timeout}内余额未变为: {amount}, 当前余额: {current_balance}')

    @staticmethod
    def get_user_coin_change_record_sql(site_code, order_no="", user_id=None, register_info=None, risk_level=None,
                                        business_type=None, coin_type=None, balance_type=None, amount_min=None,
                                        amount_max=None, start_diff=0, end_diff=0, stop_diff=0, date_type='日'):
        """
        获取会员账变记录
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session.query(UserCoinRecord). \
            filter(UserCoinRecord.created_time.between(start_time, end_time))
        if order_no:
            data = data.filter(UserCoinRecord.order_no == order_no)
        if user_id:
            data = data.filter(UserCoinRecord.user_account == user_id)
        if register_info:
            data = data.filter(UserCoinRecord.user_register == register_info)
        if risk_level:
            data = data.filter(UserCoinRecord.risk_control_level == risk_level)
        if business_type:
            data = data.filter(UserCoinRecord.business_coin_type ==
                               FundsEnum.user_business_type_dic_f_zh.value[business_type])
        if coin_type:
            data = data.filter(UserCoinRecord.coin_type == FundsEnum.user_coin_type_dic_f_zh.value[coin_type])
        if balance_type:
            data = data.filter(UserCoinRecord.balance_type == FundsEnum.user_balance_type_dic_f_zh.value[balance_type])
        if amount_min:
            data = data.filter(UserCoinRecord.coin_value == amount_min)
        if amount_max:
            data = data.filter(UserCoinRecord.coin_value == amount_max)

        result_list = []
        for item in data.all():
            item: UserCoinRecord
            sub_data = {"关联订单号": item.order_no, "会员ID": item.user_account, "注册信息": item.user_register,
                        "上级代理": item.agent_name, "风控层级": item.risk_control_level,
                        "账号状态": FundsEnum.account_status_dic_t_zh.value[item.account_status],
                        "VIP等级": item.vip_rank,
                        "业务类型": FundsEnum.user_business_type_dic_t_zh.value[item.business_coin_type],
                        "账变类型": FundsEnum.user_coin_type_dic_t_zh.value[item.coin_type],
                        "收支类型": FundsEnum.user_balance_type_dic_f_zh.value[item.balance_type],
                        "账变前余额": item.coin_from, "账变金额": item.coin_value,
                        "账变后余额": item.coin_to, "账变时间": item.created_time, "备注": item.remark,
                        "用户名称": item.user_name, "钱包类型": "", "币种": None, "当前金额": item.coin_amount,
                        "支付方式": None}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def wait_until_has_coin_change_record(site_code, order_no, timeout=5):
        """
        等待会员账变记录产生
        @return:
        """
        end_time = start_time = int(time.time())
        while end_time - start_time < timeout:
            record = Funds.get_user_coin_change_record_sql(site_code, order_no)
            if record:
                return
            end_time = int(time.time())
            time.sleep(0.2)
        raise AssertionError(f'{order_no} 在 {timeout}内余额未生成')

    @staticmethod
    def currency_rate(site_code):
        """
        平台币与其它币的转换汇率,实际使用时需用 法币 / 汇率 = 平台币, 平台币 * 汇率 = 法币
        @return:
        """
        data = ms_context.get().session.query(SiteCurrencyInfo).filter(SiteCurrencyInfo.site_code == site_code).all()
        currency_dic = {_.currency_code: _.final_rate for _ in data}
        # 填充自身的汇率
        currency_dic['WTC'] = 1
        return {_.currency_code: _.final_rate for _ in data}

    @staticmethod
    def get_user_manual_act_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日'):
        """
        获取会员人工活动调整数据
        @return: 按日期，user_account, agent_account, currency_code 分组
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        adjust_type = System.get_manual_adjust_type()
        adjust_way = System.get_manual_adjust_way()
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session. \
            query(func.date_format(func.convert_tz(func.from_unixtime(UserManualUpDownRecord.audit_datetime / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  UserManualUpDownRecord.user_account, UserManualUpDownRecord.agent_account,
                  UserManualUpDownRecord.currency_code,
                  func.sum(func.if_(UserManualUpDownRecord.adjust_way == adjust_way["加额"],
                                    UserManualUpDownRecord.adjust_amount, -UserManualUpDownRecord.adjust_amount).
                           label("amount"))). \
            filter(UserManualUpDownRecord.site_code == site_code,
                   UserManualUpDownRecord.audit_status == FundsEnum.user_manual_order_status_dic_f_zh["审核通过"],
                   UserManualUpDownRecord.adjust_type == adjust_type["会员活动"],
                   UserManualUpDownRecord.audit_datetime.between(start_time, end_time)). \
            group_by("date", UserManualUpDownRecord.user_account, UserManualUpDownRecord.agent_account,
                     UserManualUpDownRecord.currency_code)

    @staticmethod
    def get_user_manual_vip_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日'):
        """
        获取会员人工vip调整数据
        @return: 按日期，user_account, agent_account, currency_code 分组
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        adjust_type = System.get_manual_adjust_type()
        adjust_way = System.get_manual_adjust_way()
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session. \
            query(func.date_format(func.convert_tz(func.from_unixtime(UserManualUpDownRecord.audit_datetime / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  UserManualUpDownRecord.user_account, UserManualUpDownRecord.agent_account,
                  UserManualUpDownRecord.currency_code,
                  func.sum(func.if_(UserManualUpDownRecord.adjust_way == adjust_way["加额"],
                                    UserManualUpDownRecord.adjust_amount, -UserManualUpDownRecord.adjust_amount).
                           label("amount"))). \
            filter(UserManualUpDownRecord.site_code == site_code,
                   UserManualUpDownRecord.audit_status == FundsEnum.user_manual_order_status_dic_f_zh["审核通过"],
                   UserManualUpDownRecord.adjust_type == adjust_type["会员VIP优惠"],
                   UserManualUpDownRecord.audit_datetime.between(start_time, end_time)). \
            group_by("date", UserManualUpDownRecord.user_account, UserManualUpDownRecord.agent_account,
                     UserManualUpDownRecord.currency_code)

    @staticmethod
    def _get_user_manual_io_data_by_agent(site_code, order_type='充值', start_diff=0, end_diff=0, stop_diff=0,
                                          date_type='月', if_all=False):
        """
        获取后台人工充值/提款 统计数据 - 按代理统计
        :param order_type: 充值 ｜ 提款
        :param if_all: 是否忽略日期范围，获取所有数据
        @return: 笔数，总额
        """
        agent_data = Agent.get_agent_list_data(site_code)
        order_count_dic = defaultdict(int)
        order_amount_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.id: _.agent_account for _ in agent_data}

        if order_type == '充值':
            adjust_type = FundsEnum.user_manual_adjust_type_dic_f_zh.value["会员存款(后台)"]
            adjust_way = FundsEnum.adjust_way_dic_f_zh.value['加额']
        else:
            adjust_type = FundsEnum.user_manual_adjust_down_type_dic_f_zh["会员提款(后台)"]
            adjust_way = FundsEnum.adjust_way_dic_f_zh.value['减额']

        data = ms_context.get().session.query(UserManualUpDownRecord.user_account,
                                              UserManualUpDownRecord.agent_account,
                                              func.sum(UserManualUpDownRecord.adjust_amount),
                                              func.sum(1)). \
            filter(UserManualUpDownRecord.site_code == site_code,
                   UserManualUpDownRecord.adjust_type == adjust_type,
                   UserManualUpDownRecord.order_status == FundsEnum.user_manual_order_status_dic_f_zh.value["审核通过"],
                   UserManualUpDownRecord.adjust_way == adjust_way)
        if not if_all:
            timezone = Site.get_site_timezone(site_code)
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            data = data.filter(UserManualUpDownRecord.updated_time.between(start_time, end_time))

        data = data.group(UserManualUpDownRecord.user_account, UserManualUpDownRecord.agent_account).all()
        for item in data:
            # 代理下会员
            if data[1]:
                agent_path = agent_dic[data[1]]
                for agent_id in agent_path:
                    order_count_dic[agent_id_dic[agent_id]] += item[3]
                    order_amount_dic[agent_id_dic[agent_id]] += item[2]
            # 直营会员
            else:
                order_count_dic['直营'] += item[3]
                order_amount_dic['直营'] += item[2]
        return order_count_dic, order_amount_dic

    @staticmethod
    def _get_user_manual_io_data_by_user(site_code, order_type='充值', user_account=None, start_diff=0, end_diff=0,
                                         stop_diff=0, date_type='月', if_all=False):
        """
        获取后台人工充值/提款 统计数据 - 按会员统计, 假设加减都是主货币
        :param order_type: 充值 ｜ 提款
        :param if_all: 是否忽略日期范围，获取所有数据
        @return: 笔数，总额
        """
        order_count_dic = defaultdict(int)
        order_amount_dic = defaultdict(int)

        if order_type == '充值':
            adjust_type = FundsEnum.user_manual_adjust_type_dic_f_zh.value["会员存款(后台)"]
            adjust_way = FundsEnum.adjust_way_dic_f_zh.value['加额']
        else:
            adjust_type = FundsEnum.user_manual_adjust_down_type_dic_f_zh.value["会员提款(后台)"]
            adjust_way = FundsEnum.adjust_way_dic_f_zh.value['减额']

        data = ms_context.get().session.query(UserManualUpDownRecord.user_account,
                                              func.sum(UserManualUpDownRecord.adjust_amount),
                                              func.sum(1)). \
            filter(UserManualUpDownRecord.site_code == site_code,
                   UserManualUpDownRecord.adjust_type == adjust_type,
                   UserManualUpDownRecord.order_status == FundsEnum.user_manual_order_status_dic_f_zh.value["审核通过"],
                   UserManualUpDownRecord.adjust_way == adjust_way)
        if user_account:
            data = data.filter(UserManualUpDownRecord.user_account == user_account)
        if not if_all:
            timezone = Site.get_site_timezone(site_code)
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            data = data.filter(UserManualUpDownRecord.updated_time.between(start_time, end_time))

        data = data.group(UserManualUpDownRecord.user_account).all()
        for item in data:
            order_count_dic[item[0]] += item[2]
            order_amount_dic[item[0]] += item[1]
        return order_count_dic, order_amount_dic

    @staticmethod
    def _get_client_user_io_data_by_agent(site_code, order_type='充值', start_diff=0, end_diff=0, stop_diff=0,
                                          date_type='月', if_all=False):
        """
        获取会员 客户端充值/提款 统计数据 - 按代理统计
        :param order_type: 充值 ｜ 提款
        :param if_all: 是否忽略日期范围，获取所有数据
        @return: 笔数，总额, 金额都转为平台币
        """
        timezone = Site.get_site_timezone(site_code)

        currency_rate = Funds.currency_rate(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        # order_count_dic = defaultdict(dict)
        # order_amount_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.id: _.agent_account for _ in agent_data}
        order_amount_dic = {_: defaultdict(int) for _ in agent_data}
        order_count_dic = {_: defaultdict(int) for _ in agent_data}

        io_type = FundsEnum.adjust_way_dic_f_zh.value['加额' if order_type == '充值' else "减额"]
        order_status_dic = System.get_io_order_status()

        data = ms_context.get().session.query(UserDepositWithdrawal.user_account,
                                              UserDepositWithdrawal.agent_account,
                                              UserDepositWithdrawal.currency,
                                              UserDepositWithdrawal.deposit_withdraw_type,
                                              func.sum(UserDepositWithdrawal.arrive_amount),
                                              func.sum(1)). \
            filter(UserDepositWithdrawal.site_code == site_code,
                   UserDepositWithdrawal.type == io_type,
                   UserDepositWithdrawal.status == order_status_dic["成功"])
        if not if_all:
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            data = data.filter(UserDepositWithdrawal.updated_time.between(start_time, end_time))

        data = data.group(UserDepositWithdrawal.user_account, UserDepositWithdrawal.agent_account,
                          UserDepositWithdrawal.currency, UserDepositWithdrawal.deposit_withdraw_type).all()
        for item in data:
            # 代理下会员
            if data[1]:
                agent_path = agent_dic[data[1]]
                for agent_id in agent_path:
                    order_count_dic[agent_id_dic[agent_id]][item[3]] += item[5]
                    # 都转为平台币
                    order_amount_dic[agent_id_dic[agent_id]][item[3]] += item[4] / currency_rate[item[2]]
            # 直营会员
            else:
                order_count_dic['直营'][item[3]] += item[5]
                # 都转为平台币
                order_amount_dic['直营'][item[3]] += item[4] / currency_rate[item[2]]
        return order_count_dic, order_amount_dic

    @staticmethod
    def _get_client_user_io_data_by_user(site_code, order_type='充值', user_account=None, start_diff=0, end_diff=0,
                                         stop_diff=0, date_type='月', if_all=False):
        """
        获取会员 客户端充值/提款 统计数据 - 按会员统计
        :param order_type: 充值 ｜ 提款
        :param if_all: 是否忽略日期范围，获取所有数据
        @return: 笔数，总额, 金额都转为平台币
        """
        timezone = Site.get_site_timezone(site_code)
        currency_rate = Funds.currency_rate(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        order_amount_dic = {_: defaultdict(int) for _ in agent_data}
        order_count_dic = {_: defaultdict(int) for _ in agent_data}

        io_type = FundsEnum.adjust_way_dic_f_zh.value['加额' if order_type == '充值' else "减额"]
        order_status_dic = System.get_io_order_status()

        data = ms_context.get().session.query(UserDepositWithdrawal.user_account,
                                              UserDepositWithdrawal.currency,
                                              UserDepositWithdrawal.deposit_withdraw_type,
                                              func.sum(UserDepositWithdrawal.arrive_amount),
                                              func.sum(1)). \
            filter(UserDepositWithdrawal.site_code == site_code,
                   UserDepositWithdrawal.type == io_type,
                   UserDepositWithdrawal.status == order_status_dic["成功"])
        if user_account:
            data = data.filter(UserDepositWithdrawal.user_account == user_account)
        if not if_all:
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            data = data.filter(UserDepositWithdrawal.updated_time.between(start_time, end_time))

        data = data.group(UserDepositWithdrawal.user_account,
                          UserDepositWithdrawal.currency, UserDepositWithdrawal.deposit_withdraw_type).all()
        for item in data:
            order_count_dic[item[0]][item[2]] += item[4]
            # 都转为平台币
            order_amount_dic[item[0]][item[2]] += item[3] / currency_rate[item[2]]
        return order_count_dic, order_amount_dic

    @staticmethod
    def get_user_io_detail_data_by_user(site_code, order_type='充值', user_account=None, start_diff=0, end_diff=0,
                                        stop_diff=0, date_type='月', if_all=False):
        """
        获取会员充提详细数据
        :param order_type: 充值 ｜ 提款
        :param if_all: 是否忽略日期范围，获取所有数据
        @return:
        """
        manual_data = Funds._get_user_manual_io_data_by_user(site_code, order_type, user_account, start_diff,
                                                             end_diff, stop_diff, date_type, if_all)
        client_data = Funds._get_client_user_io_data_by_user(site_code, order_type, user_account, start_diff,
                                                             end_diff, stop_diff, date_type, if_all)

    @staticmethod
    def get_agent_manual_deposit_data(site_code, order_type='充值', start_diff=0, end_diff=0, stop_diff=0,
                                      date_type='月', if_all=False):
        """
        获取后台代理人工充值/提款数据    todo    等代理人工充提表有了再改
        :param order_type: 充值 ｜ 提款
        :param if_all: 是否忽略日期范围，获取所有数据
        @return: 笔数，总额
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        order_count_dic = defaultdict(int)
        order_amount_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_account: _.path.split(",") for _ in agent_data}
        agent_id_dic = {_.id: _.agent_account for _ in agent_data}

        if order_type == '充值':
            adjust_type = FundsEnum.user_manual_adjust_type_dic_f_zh.value["会员存款(后台)"]
            adjust_way = FundsEnum.adjust_way_dic_f_zh.value['加额']
        else:
            adjust_type = FundsEnum.user_manual_adjust_down_type_dic_f_zh["会员提款(后台)"]
            adjust_way = FundsEnum.adjust_way_dic_f_zh.value['减额']

        data = ms_context.get().session.query(UserManualUpDownRecord.user_account,
                                              UserManualUpDownRecord.agent_account,
                                              func.sum(UserManualUpDownRecord.adjust_amount),
                                              func.sum(1)). \
            filter(UserManualUpDownRecord.site_code == site_code,
                   UserManualUpDownRecord.adjust_type == adjust_type,
                   UserManualUpDownRecord.order_status == FundsEnum.user_manual_order_status_dic_f_zh.value["审核通过"],
                   UserManualUpDownRecord.adjust_way == adjust_way)
        if not if_all:
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            data = data.filter(UserManualUpDownRecord.updated_time.between(start_time, end_time))

        data = data.group(UserManualUpDownRecord.user_account, UserManualUpDownRecord.agent_account).all()
        for item in data:
            # 代理下会员
            if data[1]:
                agent_path = agent_dic[data[1]]
                for agent_id in agent_path:
                    order_count_dic[agent_id_dic[agent_id]] += item[3]
                    order_amount_dic[agent_id_dic[agent_id]] += item[2]
            # 直营会员
            else:
                order_count_dic['直营'] += item[3]
                order_amount_dic['直营'] += item[2]
        return order_count_dic, order_amount_dic

    @staticmethod
    def get_user_platform_balance_dao(site_code, user_account):
        """
        获取会员平台币余额
        @param site_code:
        @param user_account:
        @return: 总额，冻结金额，可用金额
        """
        session: Session = ms_context.get().session
        data: UserPlatformCoin = session.query(UserPlatformCoin).filter(UserPlatformCoin.user_account == user_account,
                                                                        UserPlatformCoin.site_code == site_code).first()
        if not data:
            from Library.Dao.Mysql.ChainQery.SiteBackend.User import User
            user_info: UserInfo = User.get_user_info_sql(site_code, user_account)[0][0]
            now = int(time.time() * 1000)
            insert_item = insert(UserPlatformCoin).values(id=now, site_code=site_code, user_account=user_account,
                                                          user_id=user_info.user_id, currency=user_info.main_currency,
                                                          total_amount=0, freeze_amount=0, available_amount=0,
                                                          created_time=now, updated_time=now, creator='xy',
                                                          updater='xy')
            session.execute(insert_item)
            return 0, 0, 0
        else:
            return data.total_amount, data.freeze_amount, data.available_amount

    @staticmethod
    def sql_update_user_platform_coin_dao(site_code, user_account, amount):
        """
        会员平台币余额加减钱，通过sql，临时用一下
        @return:
        """
        session_obj = ms_context.get().session
        sql = update(UserPlatformCoin).where(UserPlatformCoin.site_code == site_code,
                                             UserPlatformCoin.user_account == user_account). \
            values({UserPlatformCoin.total_amount: UserPlatformCoin.total_amount + amount,
                    UserPlatformCoin.available_amount: UserPlatformCoin.available_amount + amount})
        session_obj.execute(sql)
        session_obj.commit()
        return Funds.get_user_platform_balance_dao(site_code, user_account)[2]

    @staticmethod
    def get_user_withdraw_config_dao(site_code):
        """
        获取会员提款设置
        @return:
        """
        return ms_context.get().session.query(UserWithdrawConfig). \
            filter(UserWithdrawConfig.site_code == site_code).all()

    @staticmethod
    def get_user_deposit_base(site_code="", start_diff=0, end_diff=0, stop_diff=0, date_type='日', order_no=None,
                              user_account=None, user_name=None, order_source=None, order_status=None, ip=None,
                              pay_method=None):
        """
        会员存款记录统计，基础数据
        @param site_code:
        @param start_diff:
        @param end_diff:
        @param stop_diff:
        @param date_type:
        @param order_no:
        @param user_account:
        @param user_name:
        @param order_source:
        @param order_status: 待处理 ｜ 失败 ｜ 已关闭 ｜ 成功
        @param ip:
        @param pay_method:
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserDepositWithdrawal.updated_time / 1000), '+00:00',
                            f'{timezone_sql}:00'),
            '%Y-%m-%d').label("date"), UserDepositWithdrawal.site_code, UserDepositWithdrawal.user_account,
                                              UserDepositWithdrawal.deposit_withdraw_type_code,
                                              UserDepositWithdrawal.deposit_withdraw_way,
                                              UserDepositWithdrawal.deposit_withdraw_channel_code,
                                              UserDepositWithdrawal.deposit_withdraw_channel_type,
                                              UserDepositWithdrawal.currency,
                                              UserDepositWithdrawal.customer_status, UserDepositWithdrawal.device_type,
                                              UserDepositWithdrawal.agent_account,
                                              UserDepositWithdrawal.activity_base_id,
                                              UserDepositWithdrawal.fee_rate,
                                              func.sum(UserDepositWithdrawal.fee_amount).label("fee_amount"),
                                              func.count(1).label("recharge_cnt"),
                                              func.sum(UserDepositWithdrawal.arrive_amount).label("recharge_amount"),
                                              func.sum(func.if_(UserDepositWithdrawal.status == 1, 1, 0)).label(
                                                  'success_cnt'), ). \
            filter(UserDepositWithdrawal.created_time.between(start_time, end_time), UserDepositWithdrawal.type == 1,
                   UserDepositWithdrawal.status.in_([1, 2]))
        if site_code:
            data = data.filter(UserDepositWithdrawal.site_code == site_code)
        if user_account:
            data = data.filter(UserDepositWithdrawal.user_account == user_account)
        data = data.group_by("date",
                             UserDepositWithdrawal.site_code, UserDepositWithdrawal.user_account,
                             UserDepositWithdrawal.deposit_withdraw_type_code,
                             UserDepositWithdrawal.deposit_withdraw_way,
                             UserDepositWithdrawal.deposit_withdraw_channel_code,
                             UserDepositWithdrawal.deposit_withdraw_channel_type, UserDepositWithdrawal.currency,
                             UserDepositWithdrawal.customer_status, UserDepositWithdrawal.device_type,
                             UserDepositWithdrawal.agent_account, UserDepositWithdrawal.activity_base_id,
                             UserDepositWithdrawal.fee_rate)
        return data

    @staticmethod
    def get_user_manual_data_base(adjust_type, site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='日',
                                  user_account=None):
        """
        会员人工存款记录统计，基础数据
        :param adjust_type: 会员存款(后台) | 会员活动 | 会员VIP优惠
        @return:
        """
        adjust_way = {"加额": 1, "减额": 2}
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        data = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserManualUpDownRecord.updated_time / 1000), '+00:00',
                            f'{timezone_sql}:00'),
            '%Y-%m-%d').label("date"), UserManualUpDownRecord.site_code, UserManualUpDownRecord.user_account,
                                              UserManualUpDownRecord.agent_account,
                                              UserManualUpDownRecord.activity_id,
                                              UserManualUpDownRecord.currency_code,
                                              UserManualUpDownRecord.deposit_withdraw_channel_type,
                                              UserManualUpDownRecord.currency,
                                              func.sum(func.if_(UserManualUpDownRecord.adjust_way == adjust_way["加额"],
                                                                UserManualUpDownRecord.adjust_amount,
                                                                -UserManualUpDownRecord.adjust_amount)).label(
                                                  "adjust_amount"),
                                              func.sum(UserManualUpDownRecord.fee_amount).label("fee_amount"),
                                              func.count(1).label("adjust_cnt")). \
            filter(UserManualUpDownRecord.created_time.between(start_time, end_time),
                   UserManualUpDownRecord.adjust_type == System.get_manual_up_type(adjust_type),
                   UserManualUpDownRecord.audit_status == System.get_review_status("审核通过"))
        if site_code:
            data = data.filter(UserManualUpDownRecord.site_code == site_code)
        if user_account:
            data = data.filter(UserManualUpDownRecord.user_account == user_account)
        data = data.group_by("date",
                             UserManualUpDownRecord.site_code, UserManualUpDownRecord.user_account,
                             UserManualUpDownRecord.agent_account,
                             UserManualUpDownRecord.activity_id,
                             UserManualUpDownRecord.currency_code,
                             UserManualUpDownRecord.deposit_withdraw_channel_type,
                             UserManualUpDownRecord.currency)
        return data

    @staticmethod
    def get_vip_welfare_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        VIP福利数据 - 基础数据，可自行再分组处理
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        business_type = System.get_business_coin_type()
        data = ms_context.get().session.query(UserCoinRecord.user_account, UserCoinRecord.agent_name,
                                              UserCoinRecord.currency,
                                              func.sum(func.if_(UserCoinRecord.balance_type == 1,
                                                                UserCoinRecord.coin_value,
                                                                -UserCoinRecord.coin_value)).label('amount')). \
            filter(UserCoinRecord.site_code == site_code,
                   UserCoinRecord.business_coin_type == business_type["VIP福利"],
                   UserCoinRecord.updated_time.between(start_time, end_time)). \
            group_by(UserCoinRecord.user_account, UserCoinRecord.agent_name, UserCoinRecord.currency)
        return data

    @staticmethod
    def get_act_discount_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        活动优惠数据 - 基础数据，可自行再分组处理
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        business_type = System.get_business_coin_type()
        data = ms_context.get().session.query(UserCoinRecord.user_account, UserCoinRecord.agent_name,
                                              UserCoinRecord.currency,
                                              func.sum(func.if_(UserCoinRecord.balance_type == 1,
                                                                UserCoinRecord.coin_value,
                                                                -UserCoinRecord.coin_value)).label('amount')). \
            filter(UserCoinRecord.site_code == site_code,
                   UserCoinRecord.business_coin_type == business_type["活动优惠"],
                   UserCoinRecord.updated_time.between(start_time, end_time)). \
            group_by(UserCoinRecord.user_account, UserCoinRecord.agent_name, UserCoinRecord.currency)
        return data

    @staticmethod
    def get_vip_act_discount_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', currency=None):
        """
        VIP福利 + 活动优惠，领取的主货币部分 - 基础数据，可自行再分组处理  - 废弃
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        business_type = System.get_business_coin_type()
        data = ms_context.get().session.query(func.date_format(func.convert_tz(func.from_unixtime(
            UserCoinRecord.created_time / 1000), '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                              UserCoinRecord.user_account, UserCoinRecord.agent_name,
                                              UserCoinRecord.currency,
                                              func.sum(func.if_(UserCoinRecord.balance_type == 1,
                                                                UserCoinRecord.coin_value,
                                                                -UserCoinRecord.coin_value)).label('amount')). \
            filter(UserCoinRecord.site_code == site_code,
                   UserCoinRecord.business_coin_type.in_([business_type["VIP福利"], business_type["活动优惠"]]),
                   UserCoinRecord.updated_time.between(start_time, end_time))
        if currency and currency != '平台币':
            data = data.filter(UserCoinRecord.currency == currency)
        data = data.group_by("date", UserCoinRecord.user_account, UserCoinRecord.agent_name, UserCoinRecord.currency)
        return data

    @staticmethod
    def get_adjust_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        会员调整金额 - 基础数据，可自行再分组处理: VIP福利、活动优惠
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        business_type = System.get_business_coin_type()
        data = ms_context.get().session.query(func.date_format(func.convert_tz(func.from_unixtime(
            UserCoinRecord.created_time / 1000), '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                              UserCoinRecord.user_account, UserCoinRecord.agent_name,
                                              UserCoinRecord.currency,
                                              func.sum(func.if_(UserCoinRecord.balance_type == 1,
                                                                UserCoinRecord.coin_value,
                                                                -UserCoinRecord.coin_value)).label('amount')). \
            filter(UserCoinRecord.site_code == site_code,
                   UserCoinRecord.business_coin_type.in_([business_type["活动优惠"], business_type["VIP福利"]]),
                   UserCoinRecord.created_time.between(start_time, end_time)). \
            group_by(UserCoinRecord.user_account, UserCoinRecord.agent_name, UserCoinRecord.currency, "date")
        return data

    @staticmethod
    def get_used_platform_coin_sum_data_base(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                                             currency=None):
        """
        已使用优惠 - 基础数据，可自行再分组处理 . 包括：转换记录里面的部分，和账变记录中发放的主货币部分
        :param to_site_coin: 返回平台币还是主货币
        :param if_site_coin_type: 返回平台币简称还是主货币简称
        @return: 日期,会员,代理,主货币币种 分组
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        business_type = System.get_business_coin_type()
        # 转换记录表数据
        q1 = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserPlatformTransferRecord.order_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                            UserPlatformTransferRecord.user_account.label("user_account"),
                                            UserPlatformTransferRecord.agent_account.label("agent_account"),
                                            UserPlatformTransferRecord.target_currency_code.label("currency"),
                                            UserPlatformTransferRecord.target_amount.label('amount')). \
            filter(UserPlatformTransferRecord.site_code == site_code,
                   UserPlatformTransferRecord.order_time.between(start_time, end_time)). \
            join(UserInfo, UserInfo.user_account == UserPlatformTransferRecord.user_account)
        # 账变记录表数据
        q2 = ms_context.get().session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserCoinRecord.created_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                                            UserCoinRecord.user_account.label('user_account'),
                                            UserCoinRecord.agent_name.label("agent_account"),
                                            UserCoinRecord.currency,
                                            func.if_(UserCoinRecord.balance_type == 1, UserCoinRecord.coin_amount,
                                                     -UserCoinRecord.coin_amount).label('amount')). \
            filter(UserCoinRecord.site_code == site_code,
                   UserCoinRecord.business_coin_type.in_([business_type["VIP福利"], business_type["活动优惠"]]),
                   UserCoinRecord.balance_type.in_([1, 2]),
                   UserCoinRecord.created_time.between(start_time, end_time))
        data_1 = q1.union_all(q2).subquery()
        data = ms_context.get().session.query(data_1.c.date, data_1.c.user_account, data_1.c.agent_account,
                                              data_1.c.currency, func.sum(data_1.c.amount).label("amount"))
        if currency:
            data = data.filter(data_1.c.currency == currency)
        data = data.group_by(data_1.c.date, data_1.c.user_account, data_1.c.agent_account, data_1.c.currency)
        return data

    @staticmethod
    def get_user_platform_coin_sum_data_dao(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                                            currency=None):
        """
        获取会员平台币统计数据，VIP福利，活动优惠
        @return: 分组： date,user_account,agent_account
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        session: Session = ms_context.get().session
        data = session.query(func.date_format(
            func.convert_tz(func.from_unixtime(UserPlatformCoinRecord.created_time / 1000), '+00:00',
                            f'{timezone_sql}:00'), '%Y-%m-%d').label("date"), UserPlatformCoinRecord.user_account,
                             UserPlatformCoinRecord.agent_name, UserInfo.main_currency,
                             func.sum(func.if_(UserPlatformCoinRecord.business_coin_type ==
                                               PlatformEnum.business_type_f_zh["VIP福利"],
                                               UserPlatformCoinRecord.coin_value, 0)).label("vip"),
                             func.sum(func.if_(UserPlatformCoinRecord.business_coin_type ==
                                               PlatformEnum.business_type_f_zh["勋章奖励"],
                                               UserPlatformCoinRecord.coin_value, 0)).label("medal"),
                             func.sum(func.if_(UserPlatformCoinRecord.business_coin_type ==
                                               PlatformEnum.business_type_f_zh["任务"],
                                               UserPlatformCoinRecord.coin_value, 0)).label("task"),
                             func.sum(func.if_(UserPlatformCoinRecord.business_coin_type ==
                                               PlatformEnum.business_type_f_zh["活动优惠"],
                                               UserPlatformCoinRecord.coin_value, 0)).label("act")
                             ).join(UserInfo, and_(UserInfo.user_account == UserPlatformCoinRecord.user_account,
                                                   UserInfo.site_code == UserPlatformCoinRecord.site_code)). \
            filter(UserPlatformCoinRecord.site_code == site_code,
                   UserPlatformCoinRecord.balance_type == PlatformEnum.balance_type_f_zh['收入'],
                   UserPlatformCoinRecord.created_time.between(start_time, end_time))
        data_1 = data.group_by("date", UserPlatformCoinRecord.user_account, UserPlatformCoinRecord.agent_name,
                               UserInfo.main_currency).subquery()
        data = session.query(data_1.c.date, data_1.c.user_account, data_1.c.main_currency, data_1.c.agent_name,
                             data_1.c.vip, (data_1.c.medal + data_1.c.task + data_1.c.act).label('act'))
        if currency:
            data = data.filter(data_1.c.main_currency == currency)
        return data

    @staticmethod
    def get_latest_withdraw_order_dao(site_code, user_account):
        """
        获取会员最新提款订单
        @return:
        """
        session: Session = ms_context.get().session
        data = session.query(UserDepositWithdrawal.id). \
            filter(UserDepositWithdrawal.site_code == site_code,
                   UserDepositWithdrawal.type == 2, UserDepositWithdrawal.status == 1,
                   UserDepositWithdrawal.user_account == user_account)
        return data.first()

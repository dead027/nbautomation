#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 17:41
from Library.MysqlTableModel.system_param_model import SystemParam
from Library.MysqlTableModel.system_currency_info_model import SystemCurrencyInfo
from Library.MysqlTableModel.i18n_message_model import I18nMessage
from Library.Common.Utils.Contexts import *


class System(object):

    @staticmethod
    def get_i18_dic(message_key=None):
        data = ms_context.get().session.query(I18nMessage).filter(I18nMessage.language == 'zh-CN')
        if message_key:
            data = data.filter(I18nMessage.message_key == message_key)
        return {_.message_key: _.message for _ in data.all()}

    @staticmethod
    def _get_system_params(param_type, value_desc="", to_zh=False):
        """
        获取后台系统参数的值
        :param value_desc:
        :param param_type: 配置类型
        :param to_zh: True 数值转中文，False 中文转数值
        :return:
        """
        data = ms_context.get().session.query(SystemParam)
        if param_type:
            data = data.filter(SystemParam.type == param_type)
        try:
            data_dic = {_.value_desc: int(_.code) for _ in data.all()}
        except ValueError:
            data_dic = {_.value_desc: _.code for _ in data.all()}
        if to_zh:
            data_dic = {value: key for key, value in data_dic.items()}
        print(data_dic)
        return data_dic if not value_desc else data_dic[value_desc]

    @staticmethod
    def get_venue_type(value_desc="", to_zh=False):
        """
        获取平台类型  体育 ｜ 视讯 ｜ 棋牌 ｜ 电子 ｜ 彩票 ｜ 斗鸡 ｜ 电竞
        @return:
        """
        return System._get_system_params('venue_type', value_desc, to_zh)

    @staticmethod
    def get_venue_type_name_list(value_desc="", to_zh=False):
        """
        获取平台类型  体育 ｜ 视讯 ｜ 棋牌 ｜ 电子 ｜ 彩票 ｜ 斗鸡 ｜ 电竞
        @return:
        """
        return list(System._get_system_params('venue_type', value_desc, to_zh).keys())

    @staticmethod
    def get_site_type(value_desc="", to_zh=False):
        """
        获取平台类型
        @return:
        """
        return System._get_system_params('site_type', value_desc, to_zh)

    @staticmethod
    def get_order_change_status(value_desc="", to_zh=False):
        """
        获取注单变更状态
        @return:
        """
        return System._get_system_params('change_status', value_desc, to_zh)

    @staticmethod
    def get_online_status(value_desc="", to_zh=False):
        """
        获取会员状态
        @return:
        """
        return System._get_system_params('online_status', value_desc, to_zh)

    @staticmethod
    def get_sport_recommend_type(value_desc="", to_zh=False):
        """
        获取体育推荐类型
        @return:
        """
        return System._get_system_params('sport_recommend_type', value_desc, to_zh)

    @staticmethod
    def get_site_model(value_desc="", to_zh=False):
        """
        获取站点模式
        @return:
        """
        return System._get_system_params('site_model', value_desc, to_zh)

    @staticmethod
    def get_agent_overflow_audit_status(value_desc="", to_zh=False):
        """
        代理调线申请-审核状态
        @return:
        """
        return System._get_system_params('agent_overflow_audit_status', value_desc, to_zh)

    @staticmethod
    def get_profit_status(value_desc="", to_zh=False):
        """
        用户红利-红利状态
        @return:
        """
        return System._get_system_params('dividend_receive_type', value_desc, to_zh)

    @staticmethod
    def get_profit_type(value_desc="", to_zh=False):
        """
        用户红利-红利类型
        @return:
        """
        return System._get_system_params('dividend_type', value_desc, to_zh)

    @staticmethod
    def get_agent_customer_show_type(value_desc="", to_zh=False):
        """
        代理PC,H5账变显示-账变类型
        @return:
        """
        return System._get_system_params('agent_customer_show_type', value_desc, to_zh)

    @staticmethod
    def get_agent_customer_coin_type(value_desc="", to_zh=False):
        """
        代理账变记录-客户端类型
        @return:
        """
        return System._get_system_params('agent_customer_coin_type', value_desc, to_zh)

    @staticmethod
    def get_agent_coin_type(value_desc="", to_zh=False):
        """
        代理账变记录-账变类型
        @return:
        """
        return System._get_system_params('agent_coin_type', value_desc, to_zh)

    @staticmethod
    def get_agent_business_coin_type(value_desc=None, to_zh=False):
        """
        代理账变记录-业务类型
        @return:
        """
        return System._get_system_params('agent_business_coin_type', value_desc, to_zh)

    # @staticmethod
    # def get_active_judgement(value_desc="", to_zh=False):
    #     """
    #     活跃用户判定
    #     @param value_desc: 充值活跃用户标准 | 有效投注活跃用户标准 | 充值有效活跃用户标准 | 有效投注有效活跃用户标准
    #     @param to_zh: True 数值转中文，False 中文转数值
    #     @return:
    #     """
    #     data = ms_context.get().session.query(SystemParam).filter(SystemParam.type == 'agent_active_config')
    #     data_dic = {_.description: int(_.value_desc) for _ in data.all()}
    #     if to_zh:
    #         data_dic = {value: key for key, value in data_dic.items()}
    #     return data_dic if not value_desc else data_dic[value_desc]

    @staticmethod
    def get_domain_status(value_desc="", to_zh=False):
        """
        域名-状态
        @return:
        """
        return System._get_system_params('domain_state', value_desc, to_zh)

    # @staticmethod
    # def get_agent_belong(value_desc="", to_zh=False):
    #     """
    #     代理归属 1推广 2招商 3官资
    #     @return:
    #     """
    #     return System._get_system_params('agent_attribution', value_desc, to_zh)

    @staticmethod
    def get_agent_status(value_desc="", to_zh=False):
        """
        代理状态
        @return:
        """
        return System._get_system_params('agent_status', value_desc, to_zh)

    @staticmethod
    def get_agent_type(value_desc="", to_zh=False):
        """
        代理类型
        @param value_desc: 正式 ｜ 测试 ｜ 合作
        @param to_zh: True 数值转中文，False 中文转数值
        @return:
        """
        return System._get_system_params('agent_type', value_desc, to_zh)

    @staticmethod
    def get_agent_review_status(value_desc="", to_zh=False):
        """
        代理信息修改审核状态
        @return:
        """
        return System._get_system_params('agent_review_status', value_desc, to_zh)

    @staticmethod
    def get_user_change_type(value_desc="", to_zh=False):
        """
        会员信息变更类型
        @return:
        """
        return System._get_system_params('change_type', value_desc, to_zh)

    @staticmethod
    def get_agent_change_type(value_desc="", to_zh=False):
        """
        代理信息变更类型
        @return:
        """
        return System._get_system_params('agent_change_type', value_desc, to_zh)

    @staticmethod
    def get_agent_category(value_desc="", to_zh=False):
        """
        代理类别  常规代理 ｜ 流量代理
        @return:
        """
        return System._get_system_params('agent_category', value_desc, to_zh)

    @staticmethod
    def get_withdraw_type(value_desc="", to_zh=False):
        """
        提款-提款类型
        @return:
        """
        return System._get_system_params('withdraw_type', value_desc, to_zh)

    @staticmethod
    def get_recharge_type(value_desc="", to_zh=False):
        """
        充值-充值类型
        @return:
        """
        return System._get_system_params('recharge_type', value_desc, to_zh)

    @staticmethod
    def get_business_coin_type(value_desc="", to_zh=False):
        """
        账变记录-业务类型 会员存款 | 会员取款 | VIP福利 | 活动优惠 | 投注 | 派彩 | 派彩取消 | 平台币转换 | 其他调整
        @return:
        """
        return System._get_system_params('business_coin_type', value_desc, to_zh)

    @staticmethod
    def get_coin_type(value_desc="", to_zh=False):
        """
        账变记录-账变类型 会员存款 | 会员存款(后台) | 会员提款 | 会员提款(后台) | VIP福利 | 代理代存 .....
        @return:
        """
        return System._get_system_params('coin_type', value_desc, to_zh)

    @staticmethod
    def get_io_pay_process_status(value_desc="", to_zh=False):
        """
        会员存取款-三方消息状态
        @return:
        """
        return System._get_system_params('deposit_withdraw_pay_process_status', value_desc, to_zh)

    @staticmethod
    def get_io_pay_customer_status(value_desc="", to_zh=False):
        """
        会员存取款-客户端状态
        @return:
        """
        return System._get_system_params('deposit_withdraw_customer_status', value_desc, to_zh)

    @staticmethod
    def get_io_pay_customer_channel(value_desc="", to_zh=False):
        """
        会员存取款-存取通道
        @return:
        """
        return System._get_system_params('deposit_withdraw_channel', value_desc, to_zh)

    @staticmethod
    def get_io_order_status(value_desc="", to_zh=False):
        """
        会员存取款-订单状态
        @return:
        """
        return System._get_system_params('deposit_withdraw_status', value_desc, to_zh)

    @staticmethod
    def get_coin_record_type(value_desc="", to_zh=False):
        """
        账变记录-账变类型
        @return:
        """
        return System._get_system_params('coin_type', value_desc, to_zh)

    @staticmethod
    def get_coin_record_business_type(value_desc="", to_zh=False):
        """
        账变记录-业务类型
        @return:
        """
        return System._get_system_params('business_coin_type', value_desc, to_zh)

    @staticmethod
    def get_coin_record_io_type(value_desc="", to_zh=False):
        """
        账变记录-收支类型  收入 ｜ 支出 ｜ 冻结 ｜ 解冻
        @return:
        """
        return System._get_system_params('coin_balance_type', value_desc, to_zh)

    @staticmethod
    def get_manual_adjust_type(value_desc="", to_zh=False):
        """
        会员人工资金调整，操作类型  其他调整 | 会员存款(后台) | 会员VIP优惠 | 会员活动
        @return:
        """
        return System._get_system_params('manual_adjust_type', value_desc, to_zh)

    @staticmethod
    def get_vip_record_operate_type(value_desc="", to_zh=False):
        """
        VIP操作记录-操作类型
        @return:
        """
        return System._get_system_params('vip_benefit', value_desc, to_zh)

    @staticmethod
    def get_order_select_status(value_desc="", to_zh=False):
        """
        注单状态-下拉框
        @return:
        """
        return System._get_system_params('order_classify_lookup', value_desc, to_zh)

    @staticmethod
    def get_order_status(value_desc="", to_zh=False):
        """
        注单状态: 未结算 ｜ 已结算 ｜ 已取消 ｜ 重结算
        @return:
        """
        return System._get_system_params('order_classify', value_desc, to_zh)

    @staticmethod
    def get_user_register_client(value_desc="", to_zh=False):
        """
        会员注册终端
        :param value_desc PC | IOS_H5 | IOS_APP | Android_H5 | Android_APP
        @return:
        """
        return System._get_system_params('registry', value_desc, to_zh)

    @staticmethod
    def get_user_account_status(value_desc="", to_zh=False):
        """
        会员账号状态
        @return:
        """
        return System._get_system_params('account_status', value_desc, to_zh)

    @staticmethod
    def get_risk_type(value_desc="", to_zh=False):
        """
        风险类型
        @return:
        """
        return System._get_system_params('risk_control_type', value_desc, to_zh)

    @staticmethod
    def get_review_status(value_desc="", to_zh=False):
        """
        审核状态, 待处理 ｜ 处理中 ｜ 审核通过 ｜ 一审拒绝  人工上线分审核
        @param value_desc:
        @param to_zh: True 数值转中文，False 中文转数值
        @return:
        """
        return System._get_system_params('review_status', value_desc, to_zh)

    @staticmethod
    def get_platform_status(value_desc="", to_zh=False):
        """
        场馆状态, 游戏状态 通用
        @return:
        """
        return System._get_system_params('platform_class_status_type', value_desc, to_zh)

    @staticmethod
    def get_user_login_status(value_desc="", to_zh=False):
        """
        用户登录状态 - 登录日志中的
        @return:
        """
        return System._get_system_params('login_type', value_desc, to_zh)

    @staticmethod
    def get_user_account_type(value_desc="", to_zh=False):
        """
        用户账号类型
        @return:
        """
        return System._get_system_params('account_type', value_desc, to_zh)

    @staticmethod
    def get_currency_dic(currency_code="", to_zh=False, language='zh-CN'):
        """
        获取币种字典
        :return: 币种符号与币种名称
        """
        data = ms_context.get().session.query(SystemCurrencyInfo.currency_code, I18nMessage.message).\
            join(I18nMessage, SystemCurrencyInfo.currency_name_i18 == I18nMessage.message_key).\
            filter(I18nMessage.language == language)
        if to_zh:
            data_dic = {_[0]: _[1] for _ in data.all()}
        else:
            data_dic = {_[1]: _[0] for _ in data.all()}
        print(data_dic)
        return data_dic if not currency_code else data_dic[str(currency_code)]

    @staticmethod
    def get_device(value_desc="", to_zh=False):
        """
        获取终端类型
        @return:
        """
        return System._get_system_params('device_terminal', value_desc, to_zh)

    @staticmethod
    def get_sex(value_desc="", to_zh=False):
        """
        获取性别
        @return:
        """
        return System._get_system_params('gender', value_desc, to_zh)

    @staticmethod
    def get_audit_lock_status(value_desc="", to_zh=False):
        """
        获取审核锁定状态 已锁 ｜ 未锁
        @return:
        """
        return System._get_system_params('lock_status', value_desc, to_zh)

    @staticmethod
    def get_audit_operate(value_desc="", to_zh=False):
        """
        获取审核操作类型
        @return:
        """
        return System._get_system_params('review_operation', value_desc, to_zh)

    @staticmethod
    def get_activity_template(value_desc="", to_zh=False):
        """
        获取活动模版
        @return:
        """
        return System._get_system_params('activity_template', value_desc, to_zh)

    @staticmethod
    def get_activity_prescription_type(value_desc="", to_zh=False):
        """
        获取活动时效
        @return:
        """
        return System._get_system_params('activity_prescription_type', value_desc, to_zh)

    @staticmethod
    def get_activity_discount_type(value_desc="", to_zh=False):
        """
        获取活动优惠方式
        @return:
        """
        return System._get_system_params('activity_discount_type', value_desc, to_zh)

    @staticmethod
    def get_activity_participation_type(value_desc="", to_zh=False):
        """
        活动参与方式
        @return:
        """
        return System._get_system_params('activity_participation_type', value_desc, to_zh)

    @staticmethod
    def get_activity_distribution_type(value_desc="", to_zh=False):
        """
        活动派发方式
        @return:
        """
        return System._get_system_params('activity_distribution_type', value_desc, to_zh)

    @staticmethod
    def get_activity_eligibility(value_desc="", to_zh=False):
        """
        活动参与资格
        @return:
        """
        return System._get_system_params('activity_eligibility', value_desc, to_zh)

    @staticmethod
    def get_enable_status(value_desc="", to_zh=False):
        """
        通用开启、关闭状态
        @return:   启用｜禁用
        """
        return System._get_system_params('ENABLE_DISABLE_TYPE', value_desc, to_zh)

    @staticmethod
    def get_activity_receive_status(value_desc="", to_zh=False):
        """
        活动奖励领取状态
        @return:   启用｜禁用
        """
        return System._get_system_params('activity_receive_status', value_desc, to_zh)

    @staticmethod
    def get_task_type(value_desc="", to_zh=False):
        """
        任务类型
        @return:   启用｜禁用
        """
        return System._get_system_params('task_type', value_desc, to_zh)

    @staticmethod
    def get_manual_up_type(value_desc="", to_zh=False):
        """
        人工加额调整类型: 其他调整 | 会员存款(后台) | 会员VIP优惠 | 会员活动
        @return:
        """
        return System._get_system_params('manual_adjust_type', value_desc, to_zh)

    @staticmethod
    def get_manual_down_type(value_desc="", to_zh=False):
        """
        人工减额调整类型: 其他调整 | 会员提款(后台) | 会员VIP优惠 | 会员活动
        @return:
        """
        return System._get_system_params('manual_adjust_down_type', value_desc, to_zh)

    @staticmethod
    def get_manual_adjust_way(value_desc="", to_zh=False):
        """
        人工加减额调整方式： 人工添加额度 ｜ 人工扣除额度
        @return:   启用｜禁用
        """
        return System._get_system_params('manual_adjust_way', value_desc, to_zh)

    @staticmethod
    def get_settle_cycle(value_desc="", to_zh=False):
        """
        佣金结算周期
        @return:   日 ｜ 周 ｜ 月
        """
        return System._get_system_params('settle_cycle', value_desc, to_zh)

    @staticmethod
    def get_trade_type(value_desc="", to_zh=False):
        """
        交易类型
        @return:   存款 ｜ 取款 ｜ 平台币转换
        """
        return System._get_system_params('trade_type', value_desc, to_zh)

    @staticmethod
    def get_agent_wallet_type(value_desc="", to_zh=False):
        """
        代理钱包类型： 佣金钱包 ｜ 额度钱包
        @return:
        """
        return System._get_system_params('agent_wallet_type', value_desc, to_zh)

    @staticmethod
    def get_order_status_client(value_desc="", to_zh=False):
        """
        注单客户端状态： 未结算 ｜ 已结算
        @return:
        """
        return System._get_system_params('order_status_client', value_desc, to_zh)

    @staticmethod
    def get_venue_code_param(value_desc="", to_zh=False):
        """
        场馆名称
        @return:
        """
        return System._get_system_params('venue_code', value_desc, to_zh)


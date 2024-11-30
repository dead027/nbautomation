#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/10 21:28
from os import path
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.ApiRequests.CommonFunc import CommonFunc
from Library.Dao import Dao
from Library.Dao.Mysql.ChainQery.System import System
from Library.MysqlTableModel.site_activity_labs_model import SiteActivityLab
from Library.MysqlTableModel.site_activity_base_model import SiteActivityBase
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.user_manual_up_down_record_model import UserManualUpDownRecord
from Library.MysqlTableModel.agent_manual_up_down_record_model import AgentManualUpDownRecord


class FundsApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def increase_user_balance_manually_api(site_code, user_account, adjust_type, amount, rate, reason='By test',
                                           act_template=None, act_id=None, check_code=True, site_index='1'):
        """
        会员人工添加额度
        :return: order_no
        """
        act_info: SiteActivityBase = Dao.get_activity_list_dao(site_code, template=act_template, status="启用")[0]
        url = YamlUtil.get_site_host() + '/site/user-manual/api/submit'
        user_info: UserInfo = Dao.get_user_info_sql(site_code, user_account)[0][0]
        params = {"userAccounts": user_account.split(","), "currencyCode": user_info.main_currency,
                  "adjustType": System.get_manual_up_type(adjust_type), "adjustAmount": amount,
                  "applyReason": reason, "runningWaterMultiple": rate}
        if adjust_type == '会员活动':
            params['activityType'] = act_info.activity_template
            params['activityId'] = act_id if act_id else act_info.activity_no
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        latest_order_info: UserManualUpDownRecord = Dao.get_user_manual_order_list_sql(site_code,
                                                                                       adjust_way="人工增加额度")[0]
        if check_code:
            return latest_order_info.order_no
        else:
            return resp['message']

    @staticmethod
    def decrease_user_balance_manually_api(site_code, user_account, adjust_type, amount, reason='By test',
                                           act_template=None, act_id=None, check_code=True, site_index='1'):
        """
        会员人工扣除额度
        :return: order_no
        """
        act_info: SiteActivityBase = Dao.get_activity_list_dao(site_code, template=act_template, status="启用")[0]
        url = YamlUtil.get_site_host() + '/site/user-manual/api/saveManualDown'
        user_info: UserInfo = Dao.get_user_info_sql(site_code, user_account)[0][0]
        params = {"userAccounts": user_account.split(","), "currencyCode": user_info.main_currency,
                  "adjustType": System.get_manual_down_type(adjust_type), "adjustAmount": amount, "applyReason": reason}
        if adjust_type == '会员活动':
            params['activityType'] = act_info.activity_template
            params['activityId'] = act_id if act_id else act_info.activity_no
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        latest_order_info: UserManualUpDownRecord = Dao.get_user_manual_order_list_sql(site_code,
                                                                                       adjust_way="人工扣除额度")[0]
        if check_code:
            return latest_order_info.order_no
        else:
            return resp['message']

    @staticmethod
    def lock_user_manual_order_api(site_code, order_no, lock_status, audit_level, check_code=True):
        """
        人工加减额审核锁定
        @param site_code:
        @param order_no:
        @param lock_status: 未锁 ｜ 已锁
        @param audit_level:
        @param check_code:
        @return:
        """
        order_info: UserManualUpDownRecord = Dao.get_user_manual_order_list_sql(site_code, order_no=order_no,
                                                                                apply_start_diff=-10,
                                                                                apply_end_diff=0)[0]
        url_dic = {"一审": "/site/user-manual-up-review/api/lock",
                   "二审": "/admin-foreign/user-manual-up-review/api/twoLock"}
        url = YamlUtil.get_site_host() + url_dic[audit_level]
        params = {"id": [str(order_info.id)], "status": System.get_audit_lock_status(lock_status)}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def audit_manual_increase_order_api(site_code, order_no, audit_result, remark="By script", check_code=True):
        """
        人工加额审核
        @param site_code:
        @param order_no:
        @param audit_result: 审核结果，通过｜不通过
        @param check_code:
        @param remark:
        @return:
        """
        order_info: UserManualUpDownRecord = Dao.get_user_manual_order_list_sql(site_code, order_no=order_no)[0]
        # url_dic = {"一审通过": "/site/user-manual-up-review/api/oneReviewSuccess",
        #            "二审通过": "/site/user-manual-up-review/api/twoReviewSuccess",
        #            "一审不通过": '/site/user-manual-up-review/api/oneReviewFail',
        #            "二审不通过": '/site/user-manual-up-review/api/twoReviewFail'}
        # url = YamlUtil.get_site_host() + url_dic[f"{audit_level}{audit_result}"]
        name = 'oneReviewFail' if audit_result == '不通过' else 'oneReviewSuccess'
        url = YamlUtil.get_site_host() + f"/site/user-manual-up-review/api/{name}"
        params = {"id": [order_info.id], "reviewRemark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def increase_agent_balance_manually_api(site_code, agent_account, amount, reason='By test', wallet_type='额度钱包',
                                            check_code=True, site_index='1'):
        """
        代理人工添加额度
        :return: order_id
        """
        url = YamlUtil.get_site_host() + '/site/agent-manual-up/api/agentSubmit'
        params = {"userAccounts": agent_account, "walletTypeCode": System.get_agent_wallet_type(wallet_type),
                  "adjustType": "1", "adjustAmount": amount, "applyReason": reason, "agentAccountList": [agent_account]}

        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        latest_order_info: AgentManualUpDownRecord = Dao.get_agent_manual_order_list_sql(site_code,
                                                                                         adjust_way="人工增加额度")[0]
        if check_code:
            return latest_order_info.id
        else:
            return resp['message']

    @staticmethod
    def lock_agent_manual_order_api(order_id, lock_status, check_code=True):
        """
        代理加减额审核锁定
        @param order_id:
        @param lock_status: 未锁 ｜ 已锁
        @param check_code:
        @return:
        """
        url = YamlUtil.get_site_host() + '/site/agent-manual-up-review/api/lockManualUp'
        params = {"id": [order_id], "status": System.get_audit_lock_status(lock_status)}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def audit_agent_manual_increase_order_api(order_id, audit_result, remark="By script", check_code=True):
        """
        代理加额审核
        @param order_id:
        @param audit_result: 审核结果，通过｜不通过
        @param check_code:
        @param remark:
        @return:
        """
        name = 'oneReviewFailManualUp' if audit_result == '不通过' else 'oneReviewSuccessManualUp'
        url = YamlUtil.get_site_host() + f"/site/agent-manual-up-review/api/{name}"
        params = {"id": [order_id], "reviewRemark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    # @staticmethod
    # def _upload_file():
    #     """
    #     上传文件
    #     @return:
    #     """
    #     file_path = path.dirname(path.dirname(path.dirname(path.dirname(__file__))))
    #     file_name = 'Gary.png'
    #     url = YamlUtil.get_backend_host() + '/admin-foreign/file/api/upload/baowang'
    #     files = {'file': (file_name, open(f'{file_path}/images/{file_name}', 'rb'), 'image/png')}
    #     header = header_backend_context.get()
    #     header.pop('Content-Type')
    #     resp = HttpRequestUtil.post(url, files=files, headers=header)
    #     return resp['data']['fileKey'], resp['data']['url']
    #
    # @staticmethod
    # def decrease_agent_balance_manually_api(change_type, amount, agent_account, wallet_type='佣金钱包',
    #                                         reason='By script', check_code=True):
    #     """
    #     代理人工扣除额度
    #     :param agent_account:
    #     :param change_type: 代理存款(后台) | 佣金 | 返点 | 代理活动 | 其他调整
    #     :param amount:
    #     :param wallet_type: 佣金钱包 ｜ 额度钱包
    #     :param reason:
    #     :param check_code:
    #     :return: order_no
    #     """
    #     url = YamlUtil.get_backend_host() + '/admin-foreign/agent-manual-down/api/saveManualDown'
    #     img_address, img_url = FundsModuleAgentApi._upload_file()
    #     params = {"agentAccount": agent_account, "agentName": "",
    #               "walletTypeCode": FundsEnum.agent_wallet_type_dic_f_zh.value[wallet_type],
    #               "adjustType": FundsEnum.agent_adjust_way_down_dic_f_zh.value[change_type],
    #               "adjustAmount": amount, "applyReason": reason,
    #               "certificateAddress": img_address,
    #               "certificateAddressUrl": img_url}
    #     resp = HttpRequestUtil.post(url, params, check_code=check_code)
    #     if check_code:
    #         return resp["data"]
    #     else:
    #         return resp['message']

    # @staticmethod
    # def lock_agent_manual_order_api(order_no, lock_status, audit_level, check_code=True):
    #     """
    #     人工加减额审核
    #     @param order_no:
    #     @param lock_status:  锁定 ｜ 未锁定
    #     @param audit_level: 一审 ｜ 二审
    #     @param check_code:
    #     @return:
    #     """
    #     order_info: OrderRecord = Dao.get_agent_manual_order_info_sql(order_no)
    #     url_dic = {"一审": "/admin-foreign/agent-manual-up-review/api/lockManualUp",
    #                "二审": "/admin-foreign/agent-manual-up-review/api/twoLockManualUp"}
    #     url = YamlUtil.get_backend_host() + url_dic[audit_level]
    #     params = {"id": order_info.id, "status": FundsEnum.lock_status_dic_f_zh.value[lock_status]}
    #     resp = HttpRequestUtil.post(url, params, check_code=check_code)
    #     return resp['message']
    #
    # @staticmethod
    # def audit_agent_manual_increase_order_api(order_no, audit_result, audit_level, remark="By script", check_code=True):
    #     """
    #     人工加额审核
    #     @param order_no:
    #     @param audit_result: 审核结果，通过｜不通过
    #     @param audit_level: 一审 ｜ 二审
    #     @param check_code:
    #     @param remark:
    #     @return:
    #     """
    #     order_info: OrderRecord = Dao.get_agent_manual_order_info_sql(order_no)
    #     url_dic = {"一审通过": "/admin-foreign/agent-manual-up-review/api/oneReviewSuccessManualUp",
    #                "二审通过": "/admin-foreign/agent-manual-up-review/api/twoReviewSuccessManualUp",
    #                "一审不通过": '/admin-foreign/agent-manual-up-review/api/oneReviewFailManualUp',
    #                "二审不通过": '/admin-foreign/agent-manual-up-review/api/twoReviewFailManualUp'}
    #     url = YamlUtil.get_backend_host() + url_dic[f"{audit_level}{audit_result}"]
    #     params = {"id": order_info.id, "reviewRemark": remark}
    #     resp = HttpRequestUtil.post(url, params, check_code=check_code)
    #     return resp['message']

    # @staticmethod
    # def get_user_manual_increase_list_api(site_code, order_no=None, user_id=None, register_info=None,
    #                                       order_status=None, adjust_type=None, amount_min=None, amount_max=None,
    #                                       apply_start_diff=0, apply_end_diff=0, check_code=True, site_index='0'):
    #     """
    #     获取会员人工加额记录
    #     param order_status: 待一审 | 一审审核 | 一审拒绝 | 待二审 | 二审审核 | 二审拒绝 | 审核通过
    #     param adjust_type:  会员存款(后台) | 会员活动
    #     :return:
    #     """
    #     url = YamlUtil.get_backend_host() + '/admin-foreign/user-manual-up-record/api/getUpRecordPage'
    #     start_time, end_time = DateUtil.get_timestamp_range(apply_start_diff, apply_end_diff, date_type='日')
    #     params = {"applyStartTime": start_time, "applyEndTime": end_time, "pageNumber": 1,
    #               "pageSize": 100}
    #     if order_no:
    #         params['orderNo'] = order_no
    #     if user_id:
    #         params['userId'] = user_id
    #     if register_info:
    #         params['userRegister'] = register_info
    #     if order_status:
    #         params['orderStatus'] = FundsEnum.user_manual_order_status_dic_f_zh.value[order_status]
    #     if adjust_type:
    #         params['adjustType'] = FundsEnum.user_manual_adjust_type_dic_f_zh.value[adjust_type]
    #     if amount_min:
    #         params['adjustAmountMin'] = amount_min
    #     if amount_max:
    #         params['adjustAmountMax'] = amount_max
    #     resp = HttpRequestUtil.post(url, params, check_code=check_code, all_page=True)
    #     map_dic = {"订单号": "orderNo", "会员ID": "userId", "会员注册信息": "userAccount", "VIP等级": "vipRank",
    #                "调整方式": "adjustWayName", "订单状态": "orderStatusName", "调整类型": "adjustTypeName",
    #                "调整金额": "adjustAmount", "申请人": "applicant", "申请时间": "applyTime", "备注": "applyReason"}
    #     return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_manual_decrease_list_api(order_no=None, user_id=None, register_info=None, adjust_type=None,
                                          amount_min=None, amount_max=None, start_diff=0, end_diff=0, check_code=True):
        """
        获取会员人工加减额记录
        :param check_code:
        :param order_no:
        :param user_id:
        :param register_info:
        :param adjust_type:
        :param amount_min:
        :param amount_max:
        :param start_diff:
        :param end_diff:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-manual-down-record/api/listUserManualDownRecordPage'
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, date_type='日')
        params = {"creatorStartTime": start_time, "creatorEndTime": end_time, "pageNumber": 1, "pageSize": 100}
        if order_no:
            params['orderNo'] = order_no
        if user_id:
            params['userId'] = user_id
        if register_info:
            params['userRegister'] = register_info
        if adjust_type:
            params['adjustType'] = FundsEnum.user_manual_adjust_down_type_dic_t_zh.value[adjust_type]
        if amount_min:
            params['minAdjustAmount'] = amount_min
        if amount_max:
            params['maxAdjustAmount'] = amount_max
        resp = HttpRequestUtil.post(url, params, check_code=check_code, all_page=True)
        map_dic = {"订单号": "orderNo", "会员ID": "userAccount", "会员注册信息": "userRegister",
                   "VIP等级": "vipRankName",
                   "调整方式": "adjustWayText", "调整类型": "adjustTypeText", "调整金额": "adjustAmount",
                   "操作时间": "time", "备注": "applyReason"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_withdraw_deposit_fiat_currency_allocation_list_api(ShowWayEnum="", CurrencyCode="", AdjustWay=""):
        """
        存款/取款法定会员配置信息
        :param ShowWayEnum 必填 1 | 提款 2| 存款
        :param CurrencyCode:
        :param AdjustWay:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/exchange/rate/selectPage'
        if ShowWayEnum == 1:
            params = {"showWayEnum": "WITHDRAW", "currencyCode": "", "adjustWay": "", "pageNumber": 1, " pageSize": 10}
            if CurrencyCode:
                params["currencyCode"] = CurrencyCode
            if AdjustWay:
                params["adjustWay"] = AdjustWay
            resp = HttpRequestUtil.post(url, params, all_page=True)
            map_dic = {"法定货币": "currencyName", "货币代码": "currencyCode", "货币符号": "currencySymbol",
                       "三方汇率": "thirdRate",
                       "汇率调整方式": "adjustWayName",
                       "调整数值": "adjustNum", "调整后汇率": "finalRate", "最近操作人": "updater",
                       "最近操作时间": "updatedTime"}
            return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]
        else:
            params = {"showWayEnum": "RECHARGE", "currencyCode": "", "adjustWay": "", "pageNumber": 1, "pageSize": 10}
        if CurrencyCode:
            params["currencyCode"] = CurrencyCode
        if AdjustWay:
            params["adjustWay"] = AdjustWay
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"法定货币": "currencyName", "货币代码": "currencyCode", "货币符号": "currencySymbol",
                   "三方汇率": "thirdRate",
                   "汇率调整方式": "adjustWayName",
                   "调整数值": "adjustNum", "调整后汇率": "finalRate", "最近操作人": "updater",
                   "最近操作时间": "updatedTime"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_withdraw_deposit_rate_settings_info_list_api(ShowWayEnum="", CurrencyCode="", AdjustWay=""):
        """
        取款/存款加密货币汇率设置
        :param ShowWayEnum 必填 1 | 提款 2| 存款
        :param CurrencyCode:
        :param AdjustWay:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/encrypt/rate/selectPage'
        if ShowWayEnum == 1:
            params = {"showWayEnum": "WITHDRAW", "currencyCode": "", "adjustWay": "", "pageNumber": 1, "pageSize": 10}
            if CurrencyCode:
                params["currencyCode"] = CurrencyCode
            if AdjustWay:
                params["adjustWay"] = AdjustWay
            resp = HttpRequestUtil.post(url, params, all_page=True)
            map_dic = {"加密货币": "currencyName", "缩写": "currencyCode", "标志": "currencySymbol",
                       "三方汇率": "thirdRate",
                       "汇率调整方式": "adjustWayName",
                       "调整数值": "adjustNum", "调整后汇率": "finalRate", "最近操作人": "updater",
                       "最近操作时间": "updatedTime"}
            return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]
        else:
            params = {"showWayEnum": "RECHARGE", "currencyCode": "", "adjustWay": "", "pageNumber": 1, "pageSize": 10}
            if CurrencyCode:
                params["currencyCode"] = CurrencyCode
            if AdjustWay:
                params["adjustWay"] = AdjustWay
            resp = HttpRequestUtil.post(url, params, all_page=True)
            map_dic = {"加密货币": "currencyName", "缩写": "currencyCode", "标志": "currencySymbol",
                       "三方汇率": "thirdRate",
                       "汇率调整方式": "adjustWayName",
                       "调整数值": "adjustNum", "调整后汇率": "finalRate", "最近操作人": "updater",
                       "最近操作时间": "updatedTime"}
            return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_member_account_change_records_info_list_api(OrderNo="",
                                                        UserAccount="", UserName="", UserRegister="", AccountStatus="",
                                                        RiskLevel="", MinVipRank="",
                                                        MaxVipRank="", BusinessCoinType="", CoinTypeList="",
                                                        BalanceType="", MinCoinValue="",
                                                        MaxCoinValue="", coinRecordStartTime=0, coinRecordEndTime=0):
        """
        获取会员账变记录
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-coin-record/api/listUserCoinRecordPage'
        start_time, end_time = DateUtil.get_timestamp_range(coinRecordStartTime, coinRecordEndTime, date_type='日')
        params = {"coinRecordStartTime": start_time, "coinRecordEndTime": end_time, "orderNo": OrderNo,
                  "userAccount": UserAccount,
                  "userName": UserName, "userRegister": UserRegister, "accountStatus": AccountStatus,
                  "riskLevel": RiskLevel, "minVipRank": MinVipRank,
                  "maxVipRank": MaxVipRank, "businessCoinType": BusinessCoinType, "coinTypeList": CoinTypeList,
                  "balanceType": BalanceType,
                  "minCoinValue": MinCoinValue, "maxCoinValue": MaxCoinValue, "pageNumber": 1, "pageSize": 10}
        if OrderNo:
            params["orderNo"] = OrderNo
        if UserAccount:
            params["userAccount"] = UserAccount
        if UserName:
            params["userName"] = UserName
        if UserRegister:
            params["userRegister"] = UserRegister
        if AccountStatus:
            params["accountStatus"] = AccountStatus
        if RiskLevel:
            params["riskLevel"] = RiskLevel
        if MinVipRank:
            params["minVipRank"] = MinVipRank
        if MaxVipRank:
            params["maxVipRank"] = MaxVipRank
        if BusinessCoinType:
            params["businessCoinType"] = BusinessCoinType
        if CoinTypeList:
            params["coinTypeList"] = CoinTypeList
        if BalanceType:
            params["balanceType"] = BalanceType
        if MinCoinValue:
            params["minCoinValue"] = MinCoinValue
        if MaxCoinValue:
            params["maxCoinValue"] = MaxCoinValue
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"关联订单号": "orderNo", "会员ID": "userAccount", "注册信息": "userRegister",
                   "上级代理": "agentName",
                   "风控层级": "riskControlLevel",
                   "账号状态": "accountStatus", "VIP等级": "vipRankName", "业务类型": "businessCoinTypeText",
                   "账变类型": "coinTypeText", "收支类型": "balanceTypeText", "账变前余额": "coinFrom",
                   "账变金额": "coinValue", "账变后余额": "coinTo",
                   "账变时间": "createdTime", "备注": "remark"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_deposit_records_info_list_api(OrderNo="",
                                               UserAccount="", UserRegister="", DeviceType="", Status="",
                                               CustomerStatus="", ApplyIp="",
                                               DepositType="", DepositMethod="", CreateStartTime=0, CreateEndTime=0):
        """
        获取会员存款记录
        :param OrderNo:
        :param UserAccount:
        :param UserRegister:
        :param DeviceType:
        :param Status:
        :param CustomerStatus:
        :param ApplyIp:
        :param DepositType:
        :param DepositMethod:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-deposit-record/api/getUserDepositRecordPage'
        start_time, end_time = DateUtil.get_timestamp_range(CreateStartTime, CreateEndTime, date_type='日')
        params = {"createStartTime": start_time, "createEndTime": end_time, "orderNo": OrderNo,
                  "userAccount": UserAccount,
                  "userRegister": UserRegister, "deviceType": DeviceType, "status": Status,
                  "customerStatus": CustomerStatus,
                  "applyIp": ApplyIp, "depositType": DepositType,
                  "depositMethod": DepositMethod, "pageNumber": 1, "pageSize": 10}
        if OrderNo:
            params["orderNo"] = OrderNo
        if UserAccount:
            params["userAccount"] = UserAccount
        if UserRegister:
            params["userRegister"] = UserRegister
        if DeviceType:
            params["accountStatus"] = DeviceType
        if Status:
            params["riskLevel"] = Status
        if CustomerStatus:
            params["minVipRank"] = CustomerStatus
        if ApplyIp:
            params["maxVipRank"] = ApplyIp
        if DepositType:
            params["businessCoinType"] = DepositType
        if DepositMethod:
            params["coinTypeList"] = DepositMethod
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"订单号": "orderNo", "会员ID": "userAccount", "注册信息": "userRegister",
                   "订单来源": "deviceTypeText",
                   "订单状态": "statusText",
                   "客户端状态": "customerStatusText", "存款IP": "applyIp", "风控等级": "ipRiskLevel",
                   "存款终端设备号": "depositType", "充值金额": "applyAmount",
                   "充值类型": "depositType", "充值方式": "depositMethod", "充值币种": "currency",
                   "充值币种金额": "tradeCurrencyAmount",
                   "汇率": "exchangeRate", "实际到账金额": "arriveAmount", "存款时间": "createdTime",
                   "成功时间": "updatedTime",
                   "备注": "remark"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_withdrawals_records_info_list_api(OrderNo="",
                                                   UserAccount="", UserRegister="", DepositWithdrawType="",
                                                   DeviceType="", Status="", CustomerStatus="", ApplyIp="",
                                                   DeviceName="",
                                                   DepositWithdrawMethod="", IsBigMoney="", IsFirstOut="",
                                                   WithdrawalStartTime=0, WithdrawalEndTime=0):
        """
        获取会员提款记录
        :param OrderNo:
        :param UserAccount:
        :param UserRegister:
        :param DepositWithdrawType:
        :param DeviceType:
        :param Status:
        :param ApplyIp:
        :param ApplyIp:
        :param DeviceName:
        :param DepositWithdrawMethod:
        :param IsBigMoney:
        :param IsFirstOut:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-withdraw-record/api/withdrawalRecordPageList'
        start_time, end_time = DateUtil.get_timestamp_range(WithdrawalStartTime, WithdrawalEndTime, date_type='日')
        params = {"withdrawalStartTime": start_time, "withdrawalEndTime": end_time, "orderNo": OrderNo,
                  "userAccount": UserAccount,
                  "userRegister": UserRegister, "depositWithdrawType": DepositWithdrawType,
                  "deviceType": DeviceType, "status": Status,
                  "customerStatus": CustomerStatus,
                  "applyIp": ApplyIp, "deviceName": DeviceName,
                  "depositWithdrawMethod": DepositWithdrawMethod, "isFirstOut": IsFirstOut,
                  "isBigMoney": IsBigMoney, "pageNumber": 1, "pageSize": 10, "type": "2"}
        if OrderNo:
            params["orderNo"] = OrderNo
        if UserAccount:
            params["userAccount"] = UserAccount
        if UserRegister:
            params["userRegister"] = UserRegister
        if DeviceType:
            params["accountStatus"] = DeviceType
        if Status:
            params["riskLevel"] = Status
        if CustomerStatus:
            params["minVipRank"] = CustomerStatus
        if ApplyIp:
            params["maxVipRank"] = ApplyIp
        if DeviceName:
            params["deviceName"] = DeviceName
        if DepositWithdrawMethod:
            params["depositWithdrawMethod"] = DepositWithdrawMethod
        if IsFirstOut:
            params["isFirstOut"] = IsFirstOut
        if IsBigMoney:
            params["isBigMoney"] = IsBigMoney
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"订单号": "orderNo", "会员ID": "userAccount", "会员注册信息": "userRegister",
                   "订单来源": "deviceTypeText",
                   "订单状态": "statusText",
                   "客户端状态": "customerStatusText", "提款IP": "applyIp", "风控层级": "ipRiskLevel",
                   "提款终端设备号": "depositType", "提款金额": "applyAmount",
                   "提款类型": "depositType", "提款方式": "depositMethod", "提款币种": "currency",
                   "提款币种金额": "tradeCurrencyAmount",
                   "汇率": "exchangeRate", "提款账号信息": "arriveAmount", "是否为大额提款": "createdTime",
                   "是否为首提": "updatedTime", "提款时间": "", "图片预览": "",
                   "后台备注": "remark"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def lock_user_withdraw_order_api(order_no, check_code=True):
        """
        会员提款审核锁定
        @return:
        """
        url = YamlUtil.get_site_host() + '/site/user-withdraw-review/api/oneLockOrUnLock'
        params = {"id": order_no}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def audit_user_withdraw_order_api(order_no, audit_result, check_code=True):
        """
        人工加额审核
        @param order_no:
        @param audit_result: 审核结果，通过｜不通过
        @param check_code:
        @return:
        """
        url = YamlUtil.get_site_host() + f"/site/user-withdraw-review/api/withdrawReviewPage"
        params = {"orderNo": order_no, "reviewOperation": {"通过": 0, "不通过": 1}[audit_result]}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def lock_payment_order_api(order_no, check_code=True):
        """
        会员提款分配锁定
        @return:
        """
        url = YamlUtil.get_site_host() + '/site/user-withdraw-review/api/paymentLockOrUnLock'
        params = {"id": order_no}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def audit_payment_order_api(order_no, audit_result, remark="By script", check_code=True):
        """
        会员提款分配审核
        @param order_no:
        @param audit_result: 审核结果，通过｜不通过
        @param check_code:
        @param remark:
        @return:
        """
        name = 'paymentReviewFail' if audit_result == '不通过' else 'paymentReviewSuccess'
        url = YamlUtil.get_site_host() + f"/site/user-withdraw-review/api/{name}"
        params = {"id": order_no, "reviewStatus": {"通过": 1, "不通过": 2}[audit_result],
                  "payPayCodeId": "1848245519760150529"}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

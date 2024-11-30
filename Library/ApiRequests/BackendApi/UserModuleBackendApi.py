#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/1/25 11:47
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Enum.UserEnum import UserEnum
from Library.Common.Enum.FundsEnum import *


class UserModuleBackendApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def get_user_label_record_api(start_update_time_diff=-7, stop_update_time_diff=0, user_id="", operator=""):
        """
        会员标签记录
        :param start_update_time_diff:
        :param stop_update_time_diff:
        :param user_id:
        :param operator:
        """
        update_start, update_end = DateUtil.get_timestamp_range(start_update_time_diff, stop_update_time_diff,
                                                                date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-label-record/api/selectLabelRecord'

        params = {"startUpdatedTime": update_start, "endUpdatedTime": update_end, "memberAccount": "",
                  "updater": "", "pageNumber": 1, "pageSize": 10}

        if user_id:
            params["memberAccount"] = user_id
        if operator:
            params["updater"] = operator
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"变更时间": "updatedTime", "变更前": "beforeChange", "变更后": "afterChange", "会员ID": "memberAccount",
                   "账号类型": "accountTypeName", "风控层级": "riskControlLevel",
                   "账号状态": "accountStatusName", "操作人": "operator"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_registration_info_api(user_id="", account_type="", register_client="", parent_agent="", register_ip="",
                                  ipAttribution="", register_info="", register_start_diff=-7, register_end_diff=0):
        """
        会员注册信息
        :param user_id 会员ID
        :param account_type 账号类型
        :param register_client 注册终端
        :param parent_agent 上级代理
        :param register_ip 注册IP
        :param ipAttribution IP归属地
        :param register_info 注册信息
        :param register_start_diff 注册开始时间
        :param register_end_diff 注册结束时间
        """
        update_start, update_end = DateUtil.get_timestamp_range(register_start_diff, register_end_diff,
                                                                date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-registration-info/api/getRegistrationInfo'

        params = {"startRegistrationTime": update_start, "endRegistrationTime": update_end, "memberType": [],
                  "memberAccount": "", "memberId": "", "registerTerminal": [], "superiorAgent": "", "registerIp": "",
                  "ipAttribution": "", "orderField": "", "orderType": "", "orderName": "", "orderValue": "",
                  "pageNumber": 1, "pageSize": 10}

        if user_id:
            params["memberId"] = user_id
        if account_type:
            params["memberType"] = [UserEnum.account_type_dic_f_zh.value[item] for item in account_type.split(",")]
        if register_client:
            params["registerTerminal"] = [UserEnum.register_type_dic_f_zh.value[item] for item in
                                          register_client.split(",")]
        if parent_agent:
            params["superiorAgent"] = parent_agent
        if register_ip:
            params["registerIp"] = register_ip
        if ipAttribution:
            params["ipAttribution"] = ipAttribution
        if register_info:
            params["memberAccount"] = register_info

        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"注册时间": "registrationTime", "会员ID": "memberId",
                   "账号类型": "memberType", "主货币": "mainCurrency",
                   "上级代理": "superiorAgent", "注册信息": "memberAccount",
                   "注册ip/风控层级": "registerIp", "IP归属地": "ipAttribution", "注册终端": "registerTerminal",
                   "终端设备号": "terminalDeviceNumber"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_login_record_api(user_id="", account_type="", login_type="", login_ip="",
                                  ipAddress="", login_client="", deviceNo="", login_start_diff=-1, login_end_diff=0):
        """
        会员登录记录
        :param user_id 会员ID
        :param account_type 账号类型
        :param login_type 登录状态
        :param login_ip 登录IP
        :param ipAddress IP归属地
        :param login_client 登录终端
        :param deviceNo 终端设备号
        :param login_start_diff 登录开始时间
        :param login_end_diff 登录结束时间
        """
        login_start, login_end = DateUtil.get_timestamp_range(login_start_diff, login_end_diff,
                                                              date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-login-log/api/queryUserLogin'

        params = {
            "loginStartTime": login_start, "loginEndTime": login_end, "userAccount": "",
            "accountType": [], "loginType": "", "ip": "", "ipAddress": "", "loginTerminal": [],
            "deviceNo": "", "orderField": "", "orderType": "", "orderName": "", "orderValue": "",
            "pageNumber": 1, "pageSize": 10}

        if user_id:
            params["userAccount"] = user_id
        if account_type:
            params["accountType"] = [UserEnum.account_type_dic_f_zh.value[item] for item in account_type.split(",")]
        if login_type:
            params["loginType"] = [UserEnum.login_type_dic_f_zh.value[item] for item in login_type.split(",")]
        if login_ip:
            params["ip"] = login_ip
        if login_client:
            params["loginTerminal"] = [UserEnum.register_terminal_dic_f_zh.value[item]
                                       for item in login_client.split(",")]
        if ipAddress:
            params["ipAddress"] = ipAddress
        if deviceNo:
            params["deviceNo"] = deviceNo

        resp = HttpRequestUtil.post(url, params, all_page=True)

        map_dic = {"登录时间": "loginTime", "登录状态": "loginTypeText", "会员ID": "userAccount",
                   "账号类型": "accountTypeText", "登录IP风控层级": "ipControl",
                   "IP归属地": "ipAddress", "登录终端": "loginTerminalText",
                   "终端设备号风控层级": "deviceNo", "登录地址": "loginAddress", "设备版本": "deviceVersion",
                   "备注": "remark"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def user_label_config_api(label_name, desc="test", check_code=True):
        """
        新增标签
        :param label_name 标签名
        :param desc 标签描述
        :param check_code: 是否检查状态码
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-label-config/api/addLabel'
        params = {"labelName": label_name, "labelDescribe": desc}

        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def get_user_label_config_list_api(label_name="", creator_name=""):
        """
        标签配置list
        :param label_name 标签名
        :param creator_name 创建人
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-label-config/api/getLabelConfigPage'
        params = {"labelName": "", "creatorName": "", "pageNumber": 1, "pageSize": 10}
        if label_name:
            params["labelName"] = label_name
        if creator_name:
            params["creatorName"] = creator_name
        resp = HttpRequestUtil.post(url, params, all_page=True)

        map_dic = {"标签名称": "labelName", "标签描述": "labelDescribe", "标签人数": "labelCount",
                   "创建人": "creatorName", "创建时间": "createdTime",
                   "最近操作人": "updaterName", "最近操作时间": "updatedTime"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_label_config_record_api(label_name="", change_type="", updater_name="",
                                    update_start_diff=-1, update_end_diff=0):
        """
        会员标签配置记录
        :param label_name 标签名称
        :param change_type 变更类型
        :param updater_name 操作人
        :param update_start_diff 操作开始时间
        :param update_end_diff 操作结束时间
        """
        upd_start, upd_end = DateUtil.get_timestamp_range(update_start_diff, update_end_diff,
                                                          date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-label-config-record/api/getLabelConfigRecordPage'

        params = {"updateTimeStart": upd_start, "updateTimeEnd": upd_end, "updaterName": "", "changeType": "",
                  "labelName": "", "pageNumber": 1, "pageSize": 10}

        if label_name:
            params["labelName"] = label_name
        if change_type:
            params["changeType"] = change_type
        if updater_name:
            params["updaterName"] = updater_name

        resp = HttpRequestUtil.post(url, params, all_page=True)

        map_dic = {"操作时间": "updatedTime", "标签名称": "labelName", "变更类型": "changeType",
                   "变更前": "beforeChange", "变更后": "afterChange",
                   "操作人": "updaterName"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_info_change_api(user_id="", account_type="", change_type="", operator="",
                                 opera_start_diff=-7, opera_end_diff=0):
        """
        会员信息变更记录
        :param user_id 会员ID
        :param account_type 账号类型
        :param change_type 变更类型
        :param operator 操作人
        :param opera_start_diff 登录开始时间
        :param opera_end_diff 登录结束时间
        """
        upd_start, upd_end = DateUtil.get_timestamp_range(opera_start_diff, opera_end_diff,
                                                          date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-info-change/api/getUserInformationChange'

        params = {"startOperatingTime": upd_start, "endReOperatingTime": upd_end, "memberAccount": "",
                  "accountType": [], "changeType": [], "operator": "", "pageNumber": 1, "pageSize": 10}

        if user_id:
            params["memberAccount"] = user_id
        if account_type:
            params["accountType"] = [UserEnum.account_type_dic_f_zh.value[item] for item in account_type.split(",")]
        if change_type:
            params["changeType"] = [UserEnum.change_type_dic_f_zh.value[item] for item in change_type.split(",")]
        if operator:
            params["operator"] = operator

        resp = HttpRequestUtil.post(url, params, all_page=True)

        map_dic = {"操作时间": "operatingTime", "会员ID": "memberAccount", "账号类型": "accountType",
                   "变更类型": "changeTypeName", "变更前信息": "informationBeforeChange",
                   "变更后信息": "informationAfterChange", "提交信息": "submitInformation",
                   "操作人": "operator"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_basic_info_api(user_id="", register_info=""):
        """
        获取会员详情-基本信息
        @param user_id 会员ID
        @param register_info 注册信息
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-info/api/queryBasicUser'
        params = {"userAccount": user_id, "userRegister": register_info}
        if user_id:
            params["userAccount"] = user_id
        if register_info:
            params["userRegister"] = register_info

        resp = HttpRequestUtil.post(url, params, all_page=False)

        map_dic = {"会员ID": "userAccount", "账号类型": "accountTypeName", "账号状态": "accountStatusName.value",
                   "风控层级": "riskLevel", "首存时间": "firstDepositTime", "首存金额": "firstDepositAmount",
                   "最后登录时间": "lastLoginTime", "离线天数": "offlineDays", "注册时间": "registerTime",
                   "注册IP": "registerIp", "注册端": "registryName", "上级代理": "superAgentName",
                   "会员标签": "userLabelName", "主货币": "mainCurrency",
                   "手机号码": "phone", "邮箱": "mail",
                   "当前VIP等级": "vipRank"}

        # return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_wallet_info_api(user_id="", register_info=""):
        """
        获取会员详情-财务信息(中心钱包)
        @param user_id 会员ID
        @param register_info 注册信息
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-finance/api/queryWalletInfo'
        params = {"userAccount": user_id, "userRegister": register_info}
        if user_id:
            params["userAccount"] = user_id
        if register_info:
            params["userRegister"] = register_info

        resp = HttpRequestUtil.post(url, params, all_page=False)

        map_dic = {"钱包余额": "centerAmount", "取款冻结金额": "centerFreezeAmount"}

        # return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_withdraw_running_water_api(user_id="", register_info=""):
        """
        获取会员详情-财务信息(提现流水信息)
        @param user_id 会员ID
        @param register_info 注册信息
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-finance/api/queryWithdrawRunningWater'
        params = {"userAccount": user_id, "userRegister": register_info}
        if user_id:
            params["userAccount"] = user_id
        if register_info:
            params["userRegister"] = register_info

        resp = HttpRequestUtil.post(url, params, all_page=False)

        map_dic = {"用户余额": "userBalance", "所需流水": "needRunningWater",
                   "已完成投注流水": "completedRunningWater", "剩余流水": "remainingRunningWater",
                   "流水开始统计时间": "runningWaterStartTime"}

        # return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_finance_info_api(user_id="", register_info=""):
        """
        获取会员详情-财务信息(充提、投注信息)
        @param user_id 会员ID
        @param register_info 注册信息
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-finance/api/queryUserFinance'
        params = {"userAccount": user_id, "userRegister": register_info}
        if user_id:
            params["userAccount"] = user_id
        if register_info:
            params["userRegister"] = register_info

        resp = HttpRequestUtil.post(url, params, all_page=False)

        map_dic = {"存款总额": "depositTotalAmount", "存款总次数": "depositTotalNum",
                   "取款总额": "withdrawTotalAmount", "取款总次数": "withdrawTotalNum",
                   "总投注": "totalBetsAmount", "玩家输赢": "playerWinLose", "活动获得金额": "activityAmount",
                   "返水": "rebateAmount", "公司总输赢": "companyWinLose"}

        # return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_login_info_api(user_id="", register_info=""):
        """
        获取会员详情-登录信息
        @param user_id 会员ID
        @param register_info 注册信息
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-info/api/queryUserLoginInfo'
        params = {"userAccount": user_id, "userRegister": register_info}
        if user_id:
            params["userAccount"] = user_id
        if register_info:
            params["userRegister"] = register_info

        resp = HttpRequestUtil.post(url, params, all_page=True)

        map_dic = {"登录时间": "loginTime", "状态": "loginTypeText",
                   "IP地址风控层级": "ip",
                   "IP归属地": "ipAddress", "登录网址": "loginAddress", "登录终端": "loginTerminalText",
                   "设备号风控层级": "deviceNo", "设备版本": "deviceVersion"}

        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]



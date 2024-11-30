#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/9 15:07
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.Contexts import *
from Library.Common.Enum.UserEnum import UserEnum
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao import Dao


class UserModuleSiteApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def create_user_api(user_account, password, account_type="正式", currency="CNY", area="", phone="",
                        parent_agent=None, vip_grade=None, email="", apply_info="", check_code=True, site_index='1'):
        """
        创建会员
        @param user_account:
        @param password:
        @param account_type: 正式 | 测试
        @param currency: 人民币 ｜ 美元 ....
        @param area:
        @param phone:
        @param parent_agent:
        @param vip_grade:
        @param email:
        @param apply_info:
        @param check_code:
        @param site_index: '1' | '2'
        @return:
        """
        url = YamlUtil.get_site_host() + '/site/user-add/api/addUser'
        params = {"areaCode": area, "accountType": Dao.get_user_account_type(account_type), "registerType": "1",
                  "userAccount": user_account, "password": password, "phone": phone,
                  "superAgentAccount": parent_agent, "gender": "", "vipGrade": vip_grade, "email": email,
                  "userName": "", "applyInfo": apply_info, "mainCurrency": currency}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def get_user_list_api(user_id="", register_info="", status="", risk_level=None,
                          first_deposit_time_start_diff=None, first_deposit_time_end_diff=None, account_type=None,
                          register_client=None, parent_agent="", user_tag="", last_login_time_start_diff=None,
                          last_login_time_end_diff=None, offline_days_min=None, offline_days_max=None,
                          vip_level_min=None, vip_level_max=None, register_start_diff=-7, register_end_diff=0):
        """
        获取会员列表
        :return:
        """
        register_start, register_end = DateUtil.get_timestamp_range(register_start_diff, register_end_diff,
                                                                    date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/user-info/api/getPage'

        params = {"registerTimeStart": register_start, "registerTimeEnd": register_end, "userAccount": "",
                  "accountStatus": [], "riskLevelId": "", "offlineDaysStart": "", "offlineDaysEnd": "",
                  "vipRankStart": "",
                  "vipRankEnd": "", "accountType": [], "registry": "", "superAgentAccount": "", "userLabelId": "",
                  "transAgentTimeStart": "", "transAgentTimeEnd": "", "orderField": "", "orderType": "",
                  "orderName": "", "orderValue": "", "pageNumber": 1, "pageSize": 10}
        if user_id:
            params["userId"] = user_id
        if register_info:
            params["userAccount"] = register_info
        if risk_level:
            params["riskLevelId"] = risk_level
        if parent_agent:
            params["superAgentAccount"] = parent_agent
        if status:
            params["accountStatus"] = [UserEnum.user_status_dic_f_zh.value[item] for item in status.split(",")]
        if account_type:
            params['accountType'] = [UserEnum.account_type_dic_f_zh.value[item] for item in account_type.split(",")]
        if offline_days_min:
            params["offlineDaysStart"] = offline_days_min
            params["offlineDaysEnd"] = offline_days_max
        if register_start_diff and register_end_diff:
            register_start, register_end = DateUtil.get_timestamp_range(register_start_diff,
                                                                        register_end_diff, date_type='日')
            params["registerTimeStart"] = register_start
            params["registerTimeEnd"] = register_end

        if first_deposit_time_start_diff and first_deposit_time_end_diff:
            start_time, end_time = DateUtil.get_timestamp_range(first_deposit_time_start_diff,
                                                                first_deposit_time_end_diff, date_type='日')
            params["firstDepositTimeStart"] = start_time
            params["firstDepositTimeEnd"] = end_time

        if last_login_time_start_diff and last_login_time_end_diff:
            login_start_time, login_end_time = DateUtil.get_timestamp_range(last_login_time_start_diff,
                                                                            last_login_time_end_diff, date_type='日')
            params["lastLoginTimeStart"] = login_start_time
            params["lastLoginTimeEnd"] = login_end_time

        if vip_level_min and vip_level_max:
            params["vipRankStart"] = vip_level_min
            params["vipRankEnd"] = vip_level_max

        if user_tag:
            params["userLabelId"] = user_tag
        if register_client:
            params["registry"] = register_client

        resp = HttpRequestUtil.post(url, params, all_page=True)

        map_dic = {"会员ID": "userId", "注册信息": "userAccount", "上级代理ID": "superAgentId", "总代": "generalAgentId",
                   "主货币": "mainCurrency", "账号类型": "accountTypeText",
                   "会员标签": "userLabel", "风控层级": "riskLevel", "账号状态": "accountStatusText",
                   "VIP等级": "vipRankCode", "注册时间": "registerTimeStr", "首存时间": "firstDepositTimeStr",
                   "首存金额": "firstDepositAmount", "最后登录时间": "lastLoginTimeStr", "钱包": "centerWalletAmount",
                   "离线天数": "offlineDays", "注册终端": "registryText"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_new_user_audit_list_api(apply_start_diff=0, apply_end_diff=0, audit_start_diff=None, audit_end_diff=None,
                                    audit_status=None, lock_status=None, audit_operate=None, apply_account=None,
                                    audit_account=None, site_index='1', stop_day=0, date_type='日'):
        """
        获取新增会员审核列表
        @param apply_start_diff:
        @param apply_end_diff:
        @param audit_start_diff:
        @param audit_end_diff:
        @param audit_status: 待处理 ｜ 处理中 ｜ 审核通过 ｜ 一审拒绝
        @param lock_status: 未锁 ｜ 已锁
        @param audit_operate:  一审审核 ｜ 结单查看
        @param apply_account:
        @param audit_account:
        @param site_index:
        @param stop_day:
        @param date_type:
        @return:
        """
        apply_start_time, apply_end_time = DateUtil.get_timestamp_range(apply_start_diff, apply_end_diff, stop_day,
                                                                        date_type)
        if audit_start_diff:
            audit_start_time, audit_end_time = DateUtil.get_timestamp_range(audit_start_diff, audit_end_diff, stop_day,
                                                                            date_type)
        else:
            audit_start_time = audit_end_time = ""
        url = YamlUtil.get_site_host(site_index) + '/site/user-review/api/getReviewPage'
        params = {"applyTimeStart": apply_start_time, "applyTimeEnd": apply_end_time,
                  "pageNumber": 1, "pageSize": 200}
        if lock_status:
            params["lockStatus"] = UserEnum.lock_status_dic_f_zh[lock_status]
        if audit_start_diff:
            params["oneReviewFinishTimeStart"] = audit_start_time
            params["oneReviewFinishTimeEnd"] = audit_end_time
        if audit_account:
            params["reviewer"] = audit_account
        if audit_operate:
            params["reviewOperation"] = UserEnum.audit_operation_dic_f_zh[audit_operate]
        if apply_account:
            params['applicant'] = apply_account
        if audit_status:
            params['reviewStatus'] = [System.get_review_status(_) for _ in audit_status.split(",")]
        resp = HttpRequestUtil.post(url, params, all_page=True, site_index=site_index)
        map_dic = {"审核单号": "reviewOrderNo", "申请人": "applicant", "申请时间": "applyTime", "申请信息": "applyInfo",
                   "审核状态": "reviewStatus", "一审审核人": "reviewer", "一审完成时间": "oneReviewFinishTime"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_new_user_audit_detail_api(order_id, check_code=True, site_index='1'):
        """
        新增会员审核详情
        @return:
        """
        url = YamlUtil.get_site_host() + '/site/user-review/api/getReviewDetails'
        params = {"id": order_id}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        map_dic = {"账号类型": "accountTypeText", "会员账号": "userAccount", "上级代理": "superAgentAccount",
                   "主货币": "mainCurrency", "VIP等级": "vipGradeCode", "邮箱": "email", "手机号码": "phone",
                   "申请人": "applicant", "申请时间": "applyTime", "申请信息": "applyInfo"}
        return map_dic

    @staticmethod
    def lock_register_order_api(order_id, lock_status, check_code=True, site_index='1'):
        """
        新用户一审锁单
        :param order_id:
        :param lock_status: 已锁 ｜ 未锁
        :param check_code:
        :param site_index:
        :return:
        """
        url = YamlUtil.get_site_host(site_index) + '/site/user-review/api/lock'
        params = {"id": order_id, "status": System.get_audit_lock_status()[lock_status]}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def audit_register_order_api(order_id, comment='Audit by scripts', if_pass="通过", check_code=True, site_index='1'):
        """
        新注册会员审核
        :param order_id
        :param comment
        :param check_code
        :param site_index
        :param if_pass: 通过 ｜ 不通过
        :return:
        """
        url = YamlUtil.get_site_host(site_index) + '/site/user-review/api/' + 'reviewSuccess' if if_pass == '通过' \
            else 'reviewFail'
        params = {"id": order_id, "reviewRemark": comment}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def lock_user_modify_order_api(order_id, check_code=True, site_index='1'):
        """
        用户信息变更订单锁单
        :param order_id:
        :param lock_status: 锁定 ｜ 未锁定
        :param check_code:
        :param site_index:
        :return:
        """
        url = YamlUtil.get_site_host(site_index) + '/site/user_account_update_review/api/userLocks'
        params = {"id": order_id}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def audit_user_modify_order_api(order_id, comment='Audit by scripts', if_pass="通过", check_code=True,
                                    site_index='1'):
        """
        会员信息修改审核
        :return:
        """
        url = YamlUtil.get_site_host(
            site_index) + '/site/user_account_update_review/api/' + 'ReviewSuccess' if if_pass == '通过' else 'ReviewFail'
        params = {"id": order_id, "reviewRemark": comment}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_status_api(user_info_id, user_account, modify_type, remark='', check_code=True):
        """
        修改会员账号状态
        :param user_info_id: user info 的id
        :param user_account:
        :param modify_type: 正常 | 登录锁定 | 游戏锁定 | 充提锁定
        :param remark:
        :param check_code:
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "1",
                  "accountStatus": System.get_user_account_status(modify_type), "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_risk_level_api(user_info_id, user_account, vip_rank, remark='', check_code=True):
        """
        修改会员风控层级状态 todo
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "10", "vipRank": vip_rank,
                  "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_phone_api(user_info_id, user_account, area_code, phone, remark='', check_code=True):
        """
        修改会员手机号码
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "5", "phoneNumber": phone,
                  "remark": remark, "areaCode": area_code}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_email_api(user_info_id, user_account, email, remark='', check_code=True):
        """
        修改会员邮箱
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "8", "mail": email, "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_vip_level_api(user_info_id, user_account, vip_rank, remark='', check_code=True):
        """
        修改会员VIP等级
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "10", "vipRank": vip_rank,
                  "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_comment_api(user_info_id, user_account, remark='', check_code=True):
        """
        修改会员账号备注
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "9", "accountRemark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def modify_user_label_api(user_info_id, user_account, label_str, remark='', check_code=True):
        """
        修改会员账号标签
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-details/api/informationEditings'
        label_data = Dao.get_user_label_info()
        label_dic = {_.label_name: _.label_id for _ in label_data}
        params = {"id": user_info_id, "userAccount": user_account, "changeType": "3",
                  "memberLabel": [label_dic[_] for _ in label_str.split(",")], "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def get_user_verify_msg_api(site_code, user_account, phone="", check_code=True):
        """
        修改会员验证码
        :param site_code:
        :param user_account:
        :param phone:
        :param check_code:
        :return:
        """
        user_info = Dao.get_user_info_sql(site_code, user_account)[0][0]
        url = YamlUtil.get_client_host() + '/site/user-info/api/queryVerifyCode'
        params = {"phone": user_info.phone if not phone else phone, "userAccount": user_account}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def clear_flow_amount_api(user_account, check_code=True):
        """
        清除流水
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-finance/api/cleanWithdrawRunningWater'
        params = {"userAccount": user_account}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def add_flow_amount_api(user_account, amount, remark="By script", check_code=True):
        """
        增加流水
        :return:
        """
        url = YamlUtil.get_client_host() + '/site/user-finance/api/addWithdrawRunningWater'
        params = {"userAccount": user_account, "addTypingAmount": amount, "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

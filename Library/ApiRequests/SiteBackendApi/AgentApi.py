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


class AgentApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def user_overflow_apply_api(user_account, agent_account, link="http://www.link", remark="By script",
                                check_code=True):
        """
        会员溢出申请
        @return:
        """
        url = YamlUtil.get_client_host() + '/site/agentUserOverflow/apply'
        params = {"memberName": user_account, "transferAgentName": agent_account, "image": ["baowang/off=on.png"],
                  "device": "1", "link": link, "applyRemark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def lock_overflow_order_api(order_id, lock_status='已锁', check_code=True, site_index='1'):
        """
        溢出一审锁单
        :param order_id:
        :param lock_status: 已锁 ｜ 未锁
        :param check_code:
        :param site_index:
        :return:
        """
        lock_status_dic = System.get_audit_lock_status()
        url = YamlUtil.get_site_host(site_index) + '/site/agentUserOverflow/lockOrder'
        params = {"id": order_id, "lockStatus": lock_status_dic[lock_status]}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def audit_overflow_order_api(order_id, comment='Audit by scripts', if_pass="通过", check_code=True, site_index='1'):
        """
        溢出审核
        :param order_id
        :param comment
        :param check_code
        :param site_index
        :param if_pass: 通过 ｜ 不通过
        :return:
        """
        url = YamlUtil.get_site_host(site_index) + '/site/agentUserOverflow/audit'
        params = {"id": order_id, "auditStatus": 3, "auditRemark": ""}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def transfer_agent_apply_api(user_account, agent_account, remark="By script", check_code=True):
        """
        会员转代申请
        @return:
        """
        url = YamlUtil.get_client_host() + '/site/userTransferAgent/apply'
        params = {"userAccount": user_account, "transferAgentName": agent_account, "applyRemark": remark,
                  "memberName": user_account}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def lock_transfer_agent_order_api(order_id, lock_status='已锁', check_code=True, site_index='1'):
        """
        转代一审锁单
        :param order_id:
        :param lock_status: 已锁 ｜ 未锁
        :param check_code:
        :param site_index:
        :return:
        """
        lock_status_dic = System.get_audit_lock_status()
        url = YamlUtil.get_site_host(site_index) + '/site/userTransferAgent/lockOrder'
        params = {"id": order_id, "lockStatus": lock_status_dic[lock_status]}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def audit_transfer_agent_order_api(order_id, comment='Audit by scripts', if_pass="通过", check_code=True,
                                       site_index='1'):
        """
        转代审核
        :param order_id
        :param comment
        :param check_code
        :param site_index
        :param if_pass: 通过 ｜ 不通过
        :return:
        """
        url = YamlUtil.get_site_host(site_index) + '/site/userTransferAgent/audit'
        params = {"id": order_id, "auditStatus": 3, "auditRemark": ""}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

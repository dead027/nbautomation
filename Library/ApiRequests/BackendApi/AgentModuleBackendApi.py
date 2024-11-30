#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/1/25 12:56
import requests
from Library.Common.Utils.Contexts import header_backend_context
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Enum.AgentEnum import AgentEnum
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil

session = requests.session()


class AgentModuleAgentApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    backend_host = YamlUtil.get_backend_host()

    @staticmethod
    def create_agent_api(account, agent_ype='正式', agent_attribution='官资', agent_category='常规代理',
                         password="abcd1234", remark="", super_agent_account='', check_code=True):
        """
        新增代理
        @param agent_ype: 正式 | 测试 | 合作
        @param agent_attribution: 推广 | 招商 | 官资
        @param agent_category: 常规代理 | 流量代理
        @param account:
        @param password:
        @param remark:
        @param super_agent_account:
        @param check_code:
        @return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/agent-add/api/getDownBox'
        params = {"agentType": AgentEnum.agent_type_dic_f_zh.value[agent_ype],
                  "agentAttribution": AgentEnum.agent_attribution_dic_f_zh.value[agent_attribution],
                  "agentCategory": AgentEnum.agent_attribution_dic_f_zh.value[agent_category],
                  "upAgentAccount": super_agent_account,
                  "agentAccount": account, "agentPassword": password, "remark": remark}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def lock_agent_register_order_api(order_no, lock_status, check_code=True):
        """
        新代理锁定
        :param order_no:
        :param lock_status: 锁定 ｜ 未锁定
        :param check_code:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/agent-review/api/lock'
        params = {"id": order_no, "status": AgentEnum.lock_status_dic_f_zh.value[lock_status]}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']

    @staticmethod
    def audit_register_order_api(order_no, comment='Audit by scripts', if_pass="通过", check_code=True):
        """
        新代理审核
        :param order_no:
        :param comment:
        :param if_pass:
        :param check_code:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/agent-review/api/' + 'reviewSuccess' if if_pass == '通过' \
            else 'reviewFail'
        params = {"id": order_no, "reviewRemark": comment}
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp['message']


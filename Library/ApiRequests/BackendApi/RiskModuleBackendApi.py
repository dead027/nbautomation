#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/24 16:00
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Enum.RiskEnum import RiskEnum
from Library.Dao.Mysql.ChainQery.Risk import Risk, RiskCtrlBlackAccount


# 风控模块
class RiskModuleBackendApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def add_black_item(query_content, remark, risk_type, check_code=True):
        """
        添加黑名单
        :param query_content:
        :param remark:
        :param risk_type:  黑名单类型: 注册IP黑名单 | 登录IP黑名单 | 注册设备黑名单 | 登录设备黑名单"
        :param check_code:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/risk/black/addBlackAccount'
        params = {"riskControlAccount": query_content, "remark": remark,
                  "riskControlTypeCode": RiskEnum.risk_type_dic.value[risk_type]}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code)
        return resp['message']

    @staticmethod
    def edit_black_item(query_content, risk_type, new_content, new_remark, check_code=True):
        """
        编辑黑名单
        :param query_content:
        :param risk_type:  黑名单类型: 注册IP黑名单 | 登录IP黑名单 | 注册设备黑名单 | 登录设备黑名单"
        :param new_content:
        :param new_remark:
        :param check_code:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/risk/black/updateBlackAccount'
        risk_info: RiskCtrlBlackAccount = Risk.get_risk_info(risk_type, query_content)
        content = new_content if new_content else risk_info.risk_control_account
        remark = new_remark if new_remark else risk_info.remark
        params = {"id": risk_info.id, "riskControlAccount": content, "remark": remark,
                  "riskControlTypeCode": RiskEnum.risk_type_dic.value[risk_type]}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code)
        return resp['message']

    @staticmethod
    def delete_black_item(query_content, risk_type, check_code=True):
        """
        删除黑名单
        :param query_content:
        :param risk_type:  黑名单类型: 注册IP黑名单 | 登录IP黑名单 | 注册设备黑名单 | 登录设备黑名单"
        :param check_code:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/risk/black/removeBlackAccount'
        risk_info: RiskCtrlBlackAccount = Risk.get_risk_info(risk_type, query_content)
        params = {"id": risk_info.id}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code)
        return resp['message']

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/24 16:13
from Library.MysqlTableModel.risk_ctrl_black_account_model import RiskCtrlBlackAccount
from Library.Common.Utils.Contexts import *
from Library.Common.Enum.RiskEnum import RiskEnum


# 风控模块
class Risk(object):

    @staticmethod
    def get_risk_info(query_type, query_content=None):
        """
        获取后台系统参数的值
        :param query_type: 注册IP黑名单 | 登录IP黑名单 | 注册设备黑名单 | 登录设备黑名单
        :param query_content: 要查的名称
        :return:
        """
        result = ms_context.get().session.query(RiskCtrlBlackAccount.risk_control_type_code == RiskEnum.risk_type_dic.
                                                value[query_type])
        if query_content:
            result = result.filter(RiskCtrlBlackAccount.risk_control_account == query_content).first()
        else:
            result = result.all()
        return result

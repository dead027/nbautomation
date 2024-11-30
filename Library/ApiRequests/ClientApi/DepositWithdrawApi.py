#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:09
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.Dao import Dao
from Library.Common.Enum.UserEnum import UserEnum
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil


class DepositWithdrawApi(object):
    """
    充提功能
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def f(check_code=True):
        """
        申请首存活动
        @return: 报错信息
        """
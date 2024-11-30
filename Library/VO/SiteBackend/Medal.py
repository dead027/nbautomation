#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/14 14:19

from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.medal_info_model import MedalInfo
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.Common.Enum.UserLabelEnum import UserLabelEnum
from Library.MysqlTableModel.medal_reward_config_model import MedalRewardConfig
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Enum.MedalEnum import MedalEnum

from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func


class Medal(object):

    @staticmethod
    def get_medal_list(name=None, condition=None, status=None):
        """
        获取勋章列表
        @param condition:
        @param name:
        @param status:
        @return:
        """
        result = Dao.get_medal_info(name, condition, status)
        result_list = []
        for item, balance in result:
            item: MedalInfo
            sub_data = {"勋章ID": item.id, "勋章名称": item.medal_name, "解锁条件": item.unlock_cond_name,
                        "解锁条件值": item.cond_num1, "规则说明": item.medal_desc, "奖励金额": item.reward_amount,
                        "打码倍数": item.typing_multiple}
            result_list.append(sub_data)
        return result_list

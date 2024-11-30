#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/5 17:46
from collections import defaultdict
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.medal_info_model import MedalInfo
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.Common.Enum.UserLabelEnum import UserLabelEnum
from Library.MysqlTableModel.medal_reward_config_model import MedalRewardConfig
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Enum.MedalEnum import MedalEnum
from Library.MysqlTableModel.user_coin_record_model import UserCoinRecord
from Library.MysqlTableModel.site_info_model import SiteInfo
from Library.MysqlTableModel.user_info_model import UserInfo

from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func


class ActReport(object):
    """
    活动报表
    """
    @staticmethod
    def get_act_report_vo(site_code, start_diff=0, end_diff=0, act_no=None, stop_diff=0, date_type='日'):
        """
        活动报表
        @return:
        """
        data = Dao.get_act_report(site_code, start_diff, end_diff, act_no, stop_diff, date_type)
        act_name_dic = {_[0].activity_no: _[1] for _ in Dao.get_activity_list_dao(site_code)}
        result_dic = []
        for key, value in data.items():
            if not value:
                continue
            sub_data = {"统计日期": key[0], "活动名称": act_name_dic[key[1]] if key[1] in act_name_dic else "",
                        "活动ID": key[1],
                        "发放彩金金额": value["发放彩金金额"],
                        "发放免费旋转次数": value["发放免费旋转次数"], "参与人数": value["参与人数"],
                        "已领取人数": value["已领取人数"], "已领取彩金金额": value["已领取彩金金额"],
                        "使用免费旋转次数": value["使用免费旋转次数"], "未领取人数": value["未领取人数"],
                        "未领取彩金金额": value["未领取彩金金额"], "未使用免费旋转次数": value["未使用免费旋转次数"]}
            result_dic.append(sub_data)
        return result_dic

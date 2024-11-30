#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/10 22:56
from Library.Dao.Mysql.ChainQery.System import System
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from sqlalchemy import func, desc
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.Dao.Mysql.ChainQery.User import User, UserInfo
from Library.MysqlTableModel.user_manual_up_down_record_model import UserManualUpDownRecord
from Library.Dao import Dao


class UserManualIncreaseRecord(object):
    """
    会员人工加额记录
    """

    @staticmethod
    def get_user_manual_increase_record_vo(site_code, adjust_way, order_no=None, user_account=None, user_name=None,
                                           order_status=None, adjust_type=None, amount_min=None, amount_max=None,
                                           apply_start_diff=0, apply_end_diff=0):
        """
        获取会员人工加额记录
        :return:
        """
        timezone = Dao.get_site_timezone(site_code)
        data = Dao.get_user_manual_order_list_sql(site_code, adjust_way, order_no, user_account, user_name,
                                                  order_status, adjust_type, amount_min, amount_max, apply_start_diff,
                                                  apply_end_diff)
        result_list = []
        adjust_type_dic = System.get_manual_up_type(to_zh=True)
        order_status_dic = System.get_review_status(to_zh=True)
        adjust_method_dic = System.get_manual_up_type()
        for _ in data:
            _: UserManualUpDownRecord
            sub_data = {"订单号": _.order_no, "会员账号": _.user_account, "会员姓名": _.user_name,
                        "VIP等级": _.vip_grade_code, "调整方式": System.get_user_account_type(_.account_type, True),
                        "订单状态": order_status_dic[_.audit_status], "调整类型": adjust_type_dic[adjust_type],
                        "调整金额": _.adjust_amount, "申请人": _.applicant,
                        "申请时间": DateUtil.timestamp_to_date(_.apply_time, timezone, '秒'), "备注": _.apply_reason}
            result_list.append(sub_data)
        return result_list

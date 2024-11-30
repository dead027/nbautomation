#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:06
from Library.MysqlTableModel.site_task_order_record_model import SiteTaskOrderRecord
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.Common.Utils.Contexts import *
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Common.Utils.DateUtil import DateUtil
from sqlalchemy import func


class Task(object):
    """
    任务
    """

    @staticmethod
    def get_task_receive_data_base(site_code, start_diff, end_diff, stop_diff, date_type='日'):
        """
        获取活动记录中已领取的平台币数据 - 活动优惠使用
        :return: 按user_account,agent_account,currency_code,date分组
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        received_status = System.get_activity_receive_status()
        platform_currency = Site.get_site_platform_currency(site_code)

        data = ms_context.get().session. \
            query(SiteTaskOrderRecord.user_account, UserInfo.super_agent_account,
                  SiteTaskOrderRecord.currency_code,
                  func.date_format(func.convert_tz(func.from_unixtime(SiteTaskOrderRecord.receive_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(SiteTaskOrderRecord.task_amount / SiteTaskOrderRecord.final_rate).label(
                      "receive_amount")). \
            join(UserInfo, UserInfo.super_agent_id == SiteTaskOrderRecord.super_agent_id). \
            filter(SiteTaskOrderRecord.site_code == site_code,
                   SiteTaskOrderRecord.receive_time.between(_start, _end),
                   SiteTaskOrderRecord.receive_status == received_status["已领取"],
                   SiteTaskOrderRecord.currency_code == platform_currency)
        return data.group_by("date", SiteTaskOrderRecord.currency_code,
                             SiteTaskOrderRecord.user_account, UserInfo.super_agent_account)





#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:06
from Library.MysqlTableModel.site_activity_base_model import SiteActivityBase
from Library.MysqlTableModel.site_activity_first_recharge_model import SiteActivityFirstRecharge
from Library.MysqlTableModel.site_activity_second_recharge_model import SiteActivitySecondRecharge
from Library.MysqlTableModel.site_activity_labs_model import SiteActivityLab
from Library.MysqlTableModel.site_activity_free_wheel_model import SiteActivityFreeWheel
from Library.MysqlTableModel.site_activity_assign_day_model import SiteActivityAssignDay
from Library.MysqlTableModel.site_activity_spin_wheel_model import SiteActivitySpinWheel
from Library.MysqlTableModel.site_activity_order_record_model import SiteActivityOrderRecord
from Library.MysqlTableModel.i18n_message_model import I18nMessage
from Library.Common.Utils.Contexts import *
from Library.Dao.Mysql.ChainQery.System import System
from sqlalchemy import func
from Library.Common.Utils.DateUtil import DateUtil
from collections import defaultdict
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Dao.Mysql.ChainQery.SiteBackend.User import UserInfo


class Activity(object):
    """
    活动
    """

    @staticmethod
    def get_activity_list_dao(site_code, activity_name=None, template=None, status=None):
        """
        获取活动列表
        :param status: 启用 ｜ 禁用
        :param template: 首次充值｜二次充值｜免费旋转｜指定日期存款｜体育负盈利｜每日竞赛｜转盘｜红包雨
        @return:
        """
        data = ms_context.get().session.query(SiteActivityBase, I18nMessage.message).\
            join(I18nMessage, SiteActivityBase.activity_name_i18n_code == I18nMessage.message_key).\
            filter(SiteActivityBase.site_code == site_code, I18nMessage.language == 'zh-CN')
        if activity_name:
            data = data.filter(I18nMessage.message == activity_name)
        if template:
            data = data.filter(SiteActivityBase.activity_template == System.get_activity_template(template))
        if status:
            data = data.filter(SiteActivityBase.status == System.get_enable_status(status))
        rtn = data.all() if not activity_name else data.first()
        return rtn

    @staticmethod
    def get_activity_label_list_dao(site_code, name=None, status=None, operator=None):
        """
        获取活动页签列表
        @param site_code:
        @param name:
        @param status: 开启中 ｜ 已禁用
        @param operator:
        @return:
        """
        data = ms_context.get().session.query(SiteActivityLab, I18nMessage).\
            join(I18nMessage, SiteActivityLab.lab_name_i18_code == I18nMessage.message_key).\
            filter(SiteActivityLab.site_code == site_code, I18nMessage.language == 'zh-CN')
        if name:
            data = data.filter(I18nMessage.message == name)
        if status:
            data = data.filter(SiteActivityLab.status == System.get_platform_status(status))
        if operator:
            data = data.filter(SiteActivityLab.updater == operator)
        return data.all()

    @staticmethod
    def get_random_enable_activity_label(site_code):
        """
        获取一个开启中的活动标签
        @return: 标签名称
        """
        name: I18nMessage = Activity.get_activity_label_list_dao(site_code, status='开启中')[0][1]
        return name.message

    @staticmethod
    def _get_first_deposit_activity_cfg(site_code):
        """
        获取首存活动配置
        :return:
        """
        data = ms_context.get().session.query(SiteActivityBase, SiteActivityFirstRecharge).\
            join(SiteActivityFirstRecharge, SiteActivityBase.id == SiteActivityFirstRecharge.activity_id).\
            filter(SiteActivityBase.site_code == site_code, SiteActivityFirstRecharge.status == 1).first()
        return data

    @staticmethod
    def _get_second_deposit_activity_cfg(site_code):
        """
        获取次存活动配置
        :return:
        """
        data = ms_context.get().session.query(SiteActivityBase, SiteActivitySecondRecharge). \
            join(SiteActivitySecondRecharge, SiteActivityBase.id == SiteActivitySecondRecharge.activity_id). \
            filter(SiteActivityBase.site_code == site_code, SiteActivitySecondRecharge.status == 1).first()
        return data

    @staticmethod
    def _get_free_rotate_activity_cfg(site_code):
        """
        获取免费旋转配置
        :return:
        """
        data = ms_context.get().session.query(SiteActivityBase, SiteActivityFreeWheel). \
            join(SiteActivityFreeWheel, SiteActivityBase.id == SiteActivityFreeWheel.activity_id). \
            filter(SiteActivityBase.site_code == site_code, SiteActivityFreeWheel.status == 1).first()
        return data

    @staticmethod
    def _get_specify_deposit_cfg(site_code):
        """
        获取指定日期存款配置
        :return:
        """
        data = ms_context.get().session.query(SiteActivityBase, SiteActivityAssignDay). \
            join(SiteActivityAssignDay, SiteActivityBase.id == SiteActivityAssignDay.activity_id). \
            filter(SiteActivityBase.site_code == site_code, SiteActivityAssignDay.status == 1).first()
        return data

    @staticmethod
    def _get_wheel_activity_cfg(site_code):
        """
        获取转盘配置
        :return:
        """
        data = ms_context.get().session.query(SiteActivityBase, SiteActivitySpinWheel). \
            join(SiteActivitySpinWheel, SiteActivityBase.id == SiteActivitySpinWheel.activity_id). \
            filter(SiteActivityBase.site_code == site_code, SiteActivitySpinWheel.status == 1).first()
        return data

    @staticmethod
    def get_act_receive_data_base(site_code, start_diff, end_diff, stop_diff, date_type='日'):
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
            query(SiteActivityOrderRecord.user_account, UserInfo.super_agent_account,
                  SiteActivityOrderRecord.currency_code,
                  func.date_format(func.convert_tz(func.from_unixtime(SiteActivityOrderRecord.receive_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(SiteActivityOrderRecord.activity_amount / SiteActivityOrderRecord.final_rate).label(
                      "receive_amount")).\
            join(UserInfo, UserInfo.super_agent_id == SiteActivityOrderRecord.super_agent_id). \
            filter(SiteActivityOrderRecord.site_code == site_code,
                   SiteActivityOrderRecord.receive_time.between(_start, _end),
                   SiteActivityOrderRecord.receive_status == received_status["已领取"],
                   SiteActivityOrderRecord.currency_code == platform_currency)
        return data.group_by("date", SiteActivityOrderRecord.currency_code,
                             SiteActivityOrderRecord.user_account, UserInfo.super_agent_account)



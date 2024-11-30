#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/24 16:13
from Library.MysqlTableModel.site_admin_model import SiteAdmin
from Library.MysqlTableModel.site_info_model import SiteInfo
from Library.MysqlTableModel.language_manager_model import LanguageManager
from Library.MysqlTableModel.site_recharge_way_model import SiteRechargeWay
from Library.MysqlTableModel.site_withdraw_way_model import SiteWithdrawWay
from Library.MysqlTableModel.site_venue_model import SiteVenue
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.SiteEnum import SiteEnum


# 风控模块
class Site(object):

    @staticmethod
    def get_site_language_dao(site_code):
        """
        获取站点语言列表
        @return: {name: code}
        """
        result = ms_context.get().session.query(LanguageManager).\
            filter(LanguageManager.site_code == site_code)
        return {_.name: _.code for _ in result.all()}

    @staticmethod
    def get_site_admin_info_sql(site_code=None, username=None):
        """
        获取站点后台用户信息
        @param site_code:
        @param username:
        @return:
        """
        result = ms_context.get().session.query(SiteAdmin)
        if site_code:
            result = result.filter(SiteAdmin.site_code == site_code)
        if username:
            result = result.filter(SiteAdmin.user_name == username)
        return result.all()

    @staticmethod
    def get_site_info_sql(create_start_diff=None, create_end_diff=None, site_code=None, site_name=None, company=None,
                          model=None, status=None):
        """
        获取站点信息
        @param create_start_diff:
        @param create_end_diff:
        @param site_code:
        @param site_name:
        @param company:
        @param model:
        @param status:
        @return:
        """
        result = ms_context.get().session.query(SiteInfo)
        if create_start_diff or create_end_diff:
            start_time, end_time = DateUtil.get_timestamp_range(create_start_diff, create_end_diff)
        else:
            start_time = end_time = None
        if start_time:
            result = result.filter(SiteInfo.created_time >= start_time)
        if end_time:
            result = result.filter(SiteInfo.created_time <= start_time)
        if site_code:
            result = result.filter(SiteInfo.site_code == site_code)
        if site_name:
            result = result.filter(SiteInfo.site_name == site_name)
        if company:
            result = result.filter(SiteInfo.company == company)
        if model:
            result = result.filter(SiteInfo.site_model == SiteEnum.model_dic_f_zh.value[model])
        if site_name:
            result = result.filter(SiteInfo.site_name == site_name)
        if status:
            result = result.filter(SiteInfo.status == SiteEnum.status_dic_f_zh.value[status])
        return result.all()

    @staticmethod
    def get_site_timezone(site_code):
        """
        获取站点时区
        @param site_code:
        @return:
        """
        data: SiteInfo = Site.get_site_info_sql(site_code=site_code)[0]
        return data.timezone.split("UTC")[1]

    @staticmethod
    def get_site_timezone_for_sql(site_code):
        """
        获取站点时区
        @param site_code:
        @return:
        """
        data: SiteInfo = Site.get_site_info_sql(site_code=site_code)[0]
        zone = data.timezone.split("UTC")[1]
        return f'{zone[0]}{int(zone[1:]) + 5}'

    @staticmethod
    def get_site_platform_currency(site_code):
        """
        获取站点平台币
        @param site_code:
        @return:
        """
        data: SiteInfo = Site.get_site_info_sql(site_code=site_code)[0]
        return data.plat_currency_code

    @staticmethod
    def get_sit_list_info_sql(create_start_diff=None, create_end_diff=None, site_code=None, site_name=None,
                              company=None, model=None, status=None):
        """
        获取站点信息列表
        @param create_start_diff:
        @param create_end_diff:
        @param site_code:
        @param site_name:
        @param company:
        @param model:
        @param status:
        @return:
        """
        data = Site.get_site_info_sql(create_start_diff, create_end_diff, site_code, site_name, company, model, status)
        result_list = []
        for item in data:
            item: SiteInfo
            sub_data = {"站点编号": item.site_code, "站点名称": item.site_name, "所属公司": item.company,
                        "站点类型": SiteEnum.site_type_dic_t_zh.value[item.site_type],
                        "站点模式": SiteEnum.model_dic_t_zh.value[item.site_model],
                        "状态": SiteEnum.site_type_dic_t_zh.value[item.status],
                        "支持语言": item.language, "支持币种": item.currency,
                        "管理员账号": item.site_admin_account, "备注": item.remark,
                        "创建时间": DateUtil.timestamp_to_date(item.created_time),
                        "最近操作时间": DateUtil.timestamp_to_date(item.updated_time),
                        "最近操作人": item.updater}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_site_recharge_way_dao(site_code):
        """
        获取站点充值方式与手续费率映射字典
        @return:
        """
        result = ms_context.get().session.query(SiteRechargeWay).filter(SiteRechargeWay.site_code == site_code)
        return {_.recharge_way_id: _.way_fee / 100 for _ in result.all()}

    @staticmethod
    def get_site_withdraw_way_dao(site_code):
        """
        获取站点充值方式与手续费率映射字典
        @return:
        """
        result = ms_context.get().session.query(SiteWithdrawWay).filter(SiteWithdrawWay.site_code == site_code)
        return {_.withdraw_id: _.way_fee / 100 for _ in result.all()}

    @staticmethod
    def get_site_venue_rate_dao(site_code):
        """
        获取站点场馆费率
        @return:
        """
        result = ms_context.get().session.query(SiteVenue)
        if site_code:
            result = result.filter(SiteVenue.site_code == site_code)
        return result.all()



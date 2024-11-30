#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:09
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.Dao import Dao
from Library.Common.Enum.UserEnum import UserEnum
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.site_activity_labs_model import SiteActivityLab


class ActivityApi(object):
    """
    活动
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def get_activity_list_api(site_code, label_name=None, check_code=True, site_index='1'):
        """
        获取活动列表
        @return: 活动名称列表
        """
        url = YamlUtil.get_client_host() + '/app/activityParticipate/api/activityPageList'
        if label_name:
            label_info: SiteActivityLab = Dao.get_activity_label_list_dao(site_code, label_name)[0]
            label_id = label_info.id
        else:
            label_id = None
        params = {"pageNumber": 1, "pageSize": 100, "labelId": label_id}
        resp = HttpRequestUtil.post(url, params, headers=header_client_context_1.get(), check_code=check_code,
                                    site_index=site_index, all_page=True)
        return resp['message'] if not check_code else [_["activityNameI18nCode"] for _ in resp]

    @staticmethod
    def apply_first_deposit_activity_api(check_code=True, site_index='1'):
        """
        申请首存活动
        @return: 报错信息
        """

    @staticmethod
    def apply_second_deposit_activity_api(check_code=True, site_index='1'):
        """
        申请次存活动
        @return: 报错信息
        """

    @staticmethod
    def apply_specify_deposit_activity_api(check_code=True, site_index='1'):
        """
        申请指定日期充值活动
        @return: 报错信息
        """

    @staticmethod
    def apply_free_rotate_activity_api(check_code=True, site_index='1'):
        """
        申请免费选择活动
        @return: 报错信息
        """

    @staticmethod
    def apply_lucky_turntable_activity_api(check_code=True, site_index='1'):
        """
        申请幸运转盘活动
        @return: 报错信息
        """

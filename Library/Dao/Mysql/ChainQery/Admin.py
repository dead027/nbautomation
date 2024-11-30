#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:07
from Library.MysqlTableModel.business_admin_model import BusinessAdmin
from Library.Common.Utils.Contexts import *
from Library.Common.Enum.BackendUserEnum import BackendUserEnum


class Admin(object):

    @staticmethod
    def get_admin_info_sql(account, site_code=""):
        """
        获取后台管理员信息
        :return:
        """
        admin = ms_context.get().session.query(BusinessAdmin).filter(BusinessAdmin.user_name == account)
        if site_code:
            admin = admin.filter(BusinessAdmin.site_code == site_code)
        return admin.first()

    @staticmethod
    def modify_account_lock_status_sql(site_code="", account="", status='未锁定'):
        """
        修改后台账号锁定状态
        :param site_code:
        :param account:
        :param status: 未锁定 | 已锁定
        :return:
        """
        data = ms_context.get().session.query(BusinessAdmin).filter(BusinessAdmin.user_name == account)
        if site_code:
            data = data.filter(BusinessAdmin.site_code == site_code)
        user: BusinessAdmin = data.first()
        user.lock_status = BackendUserEnum.account_lock_status_dic.value[status]
        ms_context.get().session.commit()



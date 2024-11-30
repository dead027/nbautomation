#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/16 15:20

from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from Library.MysqlTableModel.user_review_model import UserReview
from Library.Dao.Mysql.ChainQery.System import System
from Library.MysqlTableModel.user_account_update_review_model import UserAccountUpdateReview
from Library.Common.Utils.DateUtil import DateUtil


class UserUpdateAuditPage(object):

    @staticmethod
    def get_user_update_audit_list_vo(site_code, apply_start_diff=0, apply_end_diff=0, audit_start_diff=None,
                                      audit_end_diff=None, user_account=None, account_type=None, apply_type=None,
                                      audit_operate=None, audit_status=None, applicant=None, audit_account=None,
                                      lock_status=None, order_no=None, stop_day=0, date_type='日'):
        """
        获取会员信息变更审核列表
        @param apply_start_diff:
        @param apply_end_diff:
        @param audit_start_diff:
        @param audit_end_diff:
        @param audit_status: 待处理 ｜ 处理中 ｜ 审核通过 ｜ 一审拒绝
        @param lock_status: 未锁 ｜ 已锁
        @param audit_operate:  一审审核 ｜ 结单查看
        @param applicant:
        @param audit_account:
        @param site_code:
        @param stop_day:
        @param date_type:
        @param user_account:
        @param account_type:
        @param apply_type:
        @param order_no:
        @return:
        """
        data = Dao.get_user_change_audit_list_sql(site_code, apply_start_diff, apply_end_diff, audit_start_diff,
                                                  audit_end_diff, user_account, account_type, apply_type,
                                                  audit_operate, audit_status, applicant, audit_account, lock_status,
                                                  order_no, stop_day, date_type)
        result_list = []
        apply_type_dic = System.get_user_change_type()
        lock_status_dic = System.get_audit_lock_status()
        account_type_dic = System.get_user_account_type()
        audit_status_dic = System.get_review_status()
        for item in data:
            item: UserAccountUpdateReview
            sub_data = {"锁单状态": lock_status_dic[item.lock_status], "审核单号": item.review_order_number,
                        "审核申请类型": apply_type_dic[item.review_application_type],
                        "修改前": item.before_fixing, "修改后": item.after_modification,
                        "会员账号": item.member_account, "账号类型": account_type_dic[item.account_type],
                        "申请人": item.applicant, "申请备注": item.application_information,
                        "审核状态": audit_status_dic[item.review_status], "申请时间": item.application_time,
                        "一审审核人": item.first_instance, "一审完成时间": item.first_review_time}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_user_update_audit_detail_vo(site_code, order_id):
        """
        获取会员信息变更订单明细
        @return:
        """
        data: UserAccountUpdateReview = Dao.get_user_change_audit_list_sql(site_code, order_id=order_id)[0]
        apply_type_dic = System.get_user_change_type(to_zh=True)
        status_dic = System.get_user_account_status(to_zh=True)
        rtn = {"申请人": data.applicant, "申请时间": data.application_time,
               "审核申请类型": apply_type_dic[data.review_application_type], "申请原因": data.application_information,
               "修改前": status_dic[data.before_fixing], "修改后": status_dic[data.after_modification],
               "一审人": data.first_instance, "一审时间": data.first_review_time,
               "一审备注": data.review_remark}
        return rtn

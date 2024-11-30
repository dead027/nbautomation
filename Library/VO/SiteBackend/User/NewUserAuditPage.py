#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/15 16:00

from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from Library.MysqlTableModel.user_review_model import UserReview
from Library.Dao.Mysql.ChainQery.System import System


class NewUserAuditPage(object):

    @staticmethod
    def get_new_user_audit_list_sql(site_code, apply_start_diff=0, apply_end_diff=0, audit_start_diff=None,
                                    audit_end_diff=None, audit_status=None, lock_status=None, audit_operate=None,
                                    apply_account=None, audit_account=None, stop_day=0, date_type='日'):
        """
        获取新增会员审核列表
        @param apply_start_diff:
        @param apply_end_diff:
        @param audit_start_diff:
        @param audit_end_diff:
        @param audit_status: 待处理 ｜ 处理中 ｜ 审核通过 ｜ 一审拒绝
        @param lock_status: 未锁 ｜ 已锁
        @param audit_operate:  一审审核 ｜ 结单查看
        @param apply_account:
        @param audit_account:
        @param site_code:
        @param stop_day:
        @param date_type:
        @return:
        """
        data = Dao.get_new_user_audit_list_data(site_code, apply_start_diff, apply_end_diff, audit_start_diff,
                                                audit_end_diff, audit_status, lock_status, audit_operate,
                                                apply_account, audit_account, stop_day, date_type)
        result_list = []
        for item in data:
            item: UserReview
            sub_data = {"审核单号": item.review_order_no, "申请人": item.applicant, "申请时间": item.apply_time,
                        "申请信息": item.apply_info, "审核状态": System.get_review_status(item.review_status),
                        "一审审核人": item.reviewer, "一审完成时间": item.one_review_finish_time}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_new_user_audit_detail_sql(site_code, user_account):
        """
        后台注册会员审核详情
        @return:
        """
        data: UserReview = Dao.get_new_user_audit_list_data(site_code, -100, user_account=user_account)[0]
        return {"账号类型": System.get_user_account_type(data.account_type, True), "会员账号": data.user_account,
                "上级代理": data.super_agent_account, "主货币": data.main_currency, "VIP等级": data.vip_grade,
                "邮箱": data.email, "手机号码": data.phone, "申请人": data.applicant, "申请时间": data.apply_time,
                "申请信息": data.apply_info, "手机区号": data.area_code,
                "锁单状态": System.get_audit_lock_status(data.lock_status, True), "锁单人": data.locker,
                "一审人": data.reviewer, "一审时间": data.one_review_finish_time, "一审备注": data.review_remark,
                "审核状态": System.get_review_status(data.review_status, True)}


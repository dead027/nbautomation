#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:06
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.site_user_label_config_model import SiteUserLabelConfig
from Library.MysqlTableModel.site_user_label_config_record_model import SiteUserLabelConfigRecord
from Library.MysqlTableModel.site_user_label_record_model import SiteUserLabelRecord
from Library.Common.Enum.UserLabelEnum import UserLabelEnum
from Library.Common.Enum.UserEnum import UserEnum


class UserLabel(object):
    @staticmethod
    def get_user_label_info(label_id=None, name=None, status=None):
        """
        获取会员标签信息
        @param label_id:
        @param name:
        @param status:
        @return:
        """
        data = ms_context.get().session.query(SiteUserLabelConfig)
        if label_id:
            data = data.filter(SiteUserLabelConfig.label_id == label_id)
        if name:
            data = data.filter(SiteUserLabelConfig.label_name == name)
        if status:
            data = data.filter(SiteUserLabelConfig.status == UserLabelEnum.status_f_zh.value[status])
        return data.all()

    @staticmethod
    def get_user_label_list(label_id=None, name=None, status=None):
        """
        获取用户标签列表
        @param label_id:
        @param name:
        @param status:
        @return: [(标签信息,(关联的会员账号, 账号类型)]
        """
        from Library.Dao.Mysql.ChainQery.MasterBackend.User import User

        user_list = User.get_user_list_sql()
        result = UserLabel.get_user_label_info(label_id, name, status)
        result_list = []
        related_user_list = [(_["会员账号"], _["账号状态"]) for _ in filter(
            lambda _: label_info.label_id in _["标签"], user_list)]
        for label_info, balance in result:
            label_info: SiteUserLabelConfig
            sub_data = {"标签ID": label_info.label_id,
                        "标签名称": label_info.label_name, "标签描述": label_info.label_describe,
                        "会员数": len(related_user_list),
                        "状态": UserLabelEnum.status_t_zh.value[label_info.status],
                        "创建时间": DateUtil.timestamp_to_time(label_info.created_time),
                        "最后操作人": label_info.last_operator,
                        "最后操作时间": DateUtil.timestamp_to_time(label_info.updated_time)}
            result_list.append((sub_data, related_user_list))
        return result_list

    @staticmethod
    def get_user_label_config_change_list(start_diff, end_diff, change_type=None, operator=None):
        """
        标签配置变更记录
        @param start_diff:
        @param end_diff:
        @param change_type:
        @param operator:
        @return:
        """
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, date_type='日')
        data = ms_context.get().session.query(SiteUserLabelConfigRecord).\
            filter(SiteUserLabelConfigRecord.created_time.between(start_time, end_time))
        if change_type:
            data = data.filter(SiteUserLabelConfigRecord.change_type ==
                               UserLabelEnum.change_type_f_zh.value['change_type'])
        if operator:
            data = data.filter(SiteUserLabelConfigRecord.operator == operator)
        result = data.all
        result_list = []
        for item in result:
            item: SiteUserLabelConfigRecord
            sub_data = {"变更时间": DateUtil.timestamp_to_time(item.updated_time),
                        "标签名称": item.label_name,
                        "变更类型": UserLabelEnum.change_type_t_zh.value[item.change_type],
                        "变更前信息": item.before_change,
                        "变更后信息": item.after_change,
                        "操作人": item.creator}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_user_label_change_list(start_diff, end_diff, user_account=None, operator=None):
        """
        标签会员标签变更记录
        @param start_diff:
        @param end_diff:
        @param user_account:
        @param operator:
        @return:
        """
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, date_type='日')
        data = ms_context.get().session.query(SiteUserLabelRecord). \
            filter(SiteUserLabelRecord.created_time.between(start_time, end_time))
        if user_account:
            data = data.filter(SiteUserLabelRecord.member_account == user_account)
        if operator:
            data = data.filter(SiteUserLabelRecord.operator == operator)
        result = data.all
        result_list = []
        for item in result:
            item: SiteUserLabelRecord
            sub_data = {"变更时间": DateUtil.timestamp_to_time(item.updated_time),
                        "变更前": item.before_change,
                        "变更后": item.after_change,
                        "会员账号": item.member_account,
                        "账号类型": UserEnum.account_type_dic_t_zh.value[item.account_type],
                        "风控层级": item.risk_control_level,
                        "账号状态": UserEnum.user_status_dic_t_zh.value[item.account_status],
                        "操作人": item.creator}
            result_list.append(sub_data)
        return result_list


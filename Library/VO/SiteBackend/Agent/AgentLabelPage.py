#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/9 16:48
from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from Library.Common.Utils.DateUtil import DateUtil


class AgentLabelPage(object):
    @staticmethod
    def get_agent_label_list(site_code, name="", creator="", order_by="", order_type=""):
        """
        代理标签列表
        :param order_by  创建时间 ｜ 最近操作人
        :param order_type 升序 ｜ 降序
        @return:
        """
        label_data = Dao.get_agent_label_info(site_code, name, creator, order_by, order_type)
        # 使用人数字典，使用人字典
        label_use_count_dic, label_use_agent_dic = Dao.get_agent_label_use_count(site_code)
        result_list = []
        for item in label_data:
            sub_data = {"标签名称": item.name, "标签描述": item.description, "标签人数": label_use_count_dic[item.id],
                        "创建人": item.creator, "创建时间": DateUtil.timestamp_to_time(item.created_time),
                        "最近操作人": item.updater,
                        "最近操作时间": DateUtil.timestamp_to_time(item.updated_time)}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_label_use_agent_list(site_code, name):
        """
        代理标签使用人列表
        @param site_code:
        @param name:
        @return:
        """
        label_data = Dao.get_agent_label_info(site_code, name)
        # 使用人数字典，使用人字典
        _, label_use_agent_dic = Dao.get_agent_label_use_count(site_code)
        agent_list = label_use_agent_dic[label_data[0].id]
        return [{"代理账号": item[0], "账号类型": item[1]} for item in agent_list]



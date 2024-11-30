#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/6 21:15
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
# from sqlalchemy import or_, update
from sqlalchemy.orm import Session
from Library.Common.Enum.AgentEnum import AgentEnum
from Library.Dao.Mysql.ChainQery.System import System
from sqlalchemy import func, select, desc
from collections import defaultdict
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.MysqlTableModel.agent_commission_final_report_model import AgentCommissionFinalReport
from Library.MysqlTableModel.agent_commission_expect_report_model import AgentCommissionExpectReport
from Library.MysqlTableModel.agent_user_overflow_model import AgentUserOverflow
from Library.MysqlTableModel.user_transfer_agent_model import UserTransferAgent
from Library.MysqlTableModel.agent_label_model import t_agent_label
from Library.MysqlTableModel.agent_login_record_model import AgentLoginRecord
from Library.MysqlTableModel.agent_withdraw_config_model import AgentWithdrawConfig
from Library.MysqlTableModel.agent_info_model import AgentInfo


class Agent(object):
    # @staticmethod
    # def get_direct_agent_count(agent_account=""):
    #     """
    #     获取直属代理数量 - 此项保留，可做批量查询使用，一次性生成所有有下级代理的数据
    #     @return:
    #     """
    #     sub_data = ms_context.get().session.query(AgentInfo.parent_id.label("id"), func.count(1).label("sub_count")).\
    #         filter(AgentInfo.parent_id.is_not(None))
    #     if agent_account:
    #         agent_info: AgentInfo = Agent.get_agent_info(agent_account)
    #         sub_data = sub_data.filter(AgentInfo.parent_id == agent_info.id)
    #     sub_data = sub_data.group_by(AgentInfo.parent_id).subquery()
    #     data = ms_context.get().session.query(AgentInfo.agent_account, sub_data.c.sub_count).\
    #         join(sub_data, AgentInfo.id == sub_data.c.id)
    #     return data.all()

    @staticmethod
    def get_sub_agent_list(site_code, agent_account="", key='id'):
        """
        获取下级代理数量 - 此项保留，可做批量查询使用，一次性生成所有有下级代理的数据
        @return:
        """
        data = ms_context.get().session.query(AgentInfo).filter(AgentInfo.parent_id.is_not(None),
                                                                AgentInfo.site_code == site_code).all()
        data_dic = defaultdict(dict)
        agent_dic = {_.id: _.agent_account for _ in data}
        for _ in agent_dic.values():
            data_dic[_] = defaultdict(list)
        for item in data:
            item: AgentInfo
            path_list = item.path.split(",")
            value = item.agent_account if key == 'agent_account' else item.id
            if len(path_list) == 3:
                data_dic[agent_dic[path_list[0]]]["团队包括自己"].append(value)
                data_dic[agent_dic[path_list[0]]]["团队不包括自己"].append(value)
                data_dic[agent_dic[path_list[0]]]["非直属"].append(value)
                data_dic[agent_dic[path_list[1]]]["团队包括自己"].append(value)
                data_dic[agent_dic[path_list[1]]]["团队不包括自己"].append(value)
                data_dic[agent_dic[path_list[1]]]["直属"].append(value)
                data_dic[agent_dic[path_list[2]]]["团队包括自己"].append(value)
            elif len(path_list) == 2:
                data_dic[agent_dic[path_list[0]]]["团队包括自己"].append(value)
                data_dic[agent_dic[path_list[0]]]["团队不包括自己"].append(value)
                data_dic[agent_dic[path_list[0]]]["直属"].append(value)
                data_dic[agent_dic[path_list[1]]]["团队包括自己"].append(value)
            elif len(path_list) == 1:
                data_dic[agent_dic[path_list[0]]]["团队包括自己"].append(value)
        return data_dic if not agent_account else data_dic[agent_account]

    @staticmethod
    def get_sub_agents(site_code, agent_account=None, query_type=1, key="id", level=None, agent_type=None,
                       direct_agent_acc="", date_type="月", date_diff=None, stop_day=0):
        """
        获取代理下所有子代理id列表,主要是供其它报表类查询使用  - 废弃
        :param site_code:
        :param agent_account:
        :param query_type: 1 返回团体所有代理，包括自己，2 返回自己，3 所有直属代理，4 返回下级所有代理
        :param key: 代理某个属性 默认id,    id | name | agent_account
        :param level: 代理层级
        :param agent_type: 正式 ｜ 置换 ｜ 商务
        :param direct_agent_acc
        :param stop_day: 若统计本月，指定截止日期
        :param date_type:
        :param date_diff:
        :return: agent_id 列表
        """
        agent_info = ms_context.get().session.query(AgentInfo).filter(AgentInfo.site_code == site_code)
        if agent_account:
            agent_id = Agent.get_agent_info(site_code, agent_account).id
            if query_type != 3:
                if query_type == 1:
                    regexp_str = f'(^.*,{agent_id},.*$)|(^{agent_id},.*$)|(^.*,{agent_id}$)|(^{agent_id}$)'
                elif query_type == 2:
                    regexp_str = f'(^.*,{agent_id}$)|(^{agent_id}$)'
                else:
                    regexp_str = f'(^.*,{agent_id},.*$)|(^{agent_id},.*$)'
                agent_info = agent_info.filter(AgentInfo.path.regexp_match(regexp_str))
            else:
                agent_info = agent_info.filter(AgentInfo.parent_id == agent_info.id)
        if level:
            agent_info = agent_info.filter(AgentInfo.level == level)
        if agent_type:
            agent_info = agent_info.filter(AgentInfo.agent_type == System.get_agent_type([agent_type]))
        if direct_agent_acc:
            parent_agent_info = Agent.get_agent_info(site_code, direct_agent_acc)
            agent_info = agent_info.filter(AgentInfo.parent_id == parent_agent_info.id)
        if date_diff:
            timezone = Site.get_site_timezone(site_code)
            start_timestamp, end_timestamp = DateUtil.get_timestamp_range(date_diff, date_diff, stop_day, date_type,
                                                                          timezone)
            agent_info = agent_info.filter(start_timestamp <= AgentInfo.register_time <= end_timestamp)
        agent_info = agent_info.with_entities(eval(f"AgentInfo.{key}")).all()
        return [item[0] for item in agent_info]

    @staticmethod
    def get_agent_info(site_code, agent_account):
        """
        获取代理信息
        @return:
        """
        session: Session = ms_context.get().session
        return session.query(AgentInfo).filter(AgentInfo.agent_account == agent_account,
                                               AgentInfo.site_code == site_code).first()

    @staticmethod
    def get_agent_label_info(site_code, name="", creator="", order_by="创建时间", order_type="降序"):
        """
        获取代理标签列表
        :param order_by  创建时间 ｜ 最近操作人
        :param order_type 升序 ｜ 降序
        @return:
        """
        sql = select(t_agent_label).where(t_agent_label.c.site_code == site_code)
        if name:
            sql = sql.where(t_agent_label.c.name == name)
        if creator:
            sql = sql.where(t_agent_label.c.creator == creator)
        if order_type == '升序':
            sql = sql.order_by(t_agent_label.c.created_time if order_by == '创建时间' else t_agent_label.c.updater)
        else:
            sql = sql.order_by(desc(t_agent_label.c.created_time if order_by == '创建时间' else t_agent_label.c.updater))
        data = ms_context.get().cursor.execute(sql).all()
        return data

    @staticmethod
    def get_agent_label_use_count(site_code, label_id=""):
        """
        获取代理标签使用数量和使用人列表
        @return: 使用数量，使用人列表(agent_account, agent_type)
        """
        data = ms_context.get().session.query(AgentInfo).filter(AgentInfo.site_code == site_code)
        if label_id:
            data = data.filter(func.find_in_set(label_id, AgentInfo.agent_label_id))
        label_use_count_dic = defaultdict(int)
        label_use_agent_dic = defaultdict(list)
        for agent_info in data.all():
            label_id_str = agent_info.agent_label_id
            label_id_list = label_id_str.split(",")
            for lid in label_id_list:
                label_use_count_dic[lid] += 1
                label_use_agent_dic[lid].append((agent_info.agent_account,
                                                 System.get_agent_type(agent_info.agent_type, True)))
        return label_use_count_dic, label_use_agent_dic

    @staticmethod
    def get_agent_list_data(site_code, register_start_diff=None, register_end_diff=None, agent_account="",
                            only_direct=False, account_type="", account_status="", risk_level="", label="",
                            register_type="", parent_account=None, agent_category=None):
        """
        获取下级代理的列表，主要供代理列表模块使用
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        data = ms_context.get().session.query(AgentInfo)
        if register_start_diff or register_start_diff == 0:
            start_time, end_time = DateUtil.get_timestamp_range(register_start_diff, register_end_diff,
                                                                timezone=timezone)
            data = data.filter(AgentInfo.register_time.between(start_time, end_time), AgentInfo.site_code == site_code)
        if agent_account:
            data = data.filter(AgentInfo.agent_account == agent_account)
            if only_direct:
                agent_info: AgentInfo = Agent.get_agent_info(site_code, agent_account)
                data = data.filter(AgentInfo.parent_id == agent_info.id)
        if account_type:
            data = data.filter(AgentInfo.agent_type == System.get_agent_type(account_type))
        if account_status:
            data = data.filter(AgentInfo.status == System.get_agent_status(account_status))
        if risk_level:
            data = data.filter(AgentInfo.risk_level_id == risk_level)
        if parent_account:
            data = data.filter(AgentInfo.parent_account == parent_account)
        if agent_category:
            data = data.filter(AgentInfo.agent_category == System.get_agent_category(agent_category))
        if label:
            label_info = Agent.get_agent_label_info(label)
            data = data.filter(func.find_in_set(label_info.id, AgentInfo.agent_label_id) > 0)
        if register_type:
            data = data.filter(AgentInfo.register_way == AgentEnum.agent_register_type_dic_f_zh.value[register_type])
        return data.all()

    @staticmethod
    def get_agent_login_info(site_code, agent_account):
        """
        代理详情 - 代理登录记录
        @param site_code:
        @param agent_account:
        @return:
        """
        data = ms_context.get().session.query(AgentLoginRecord).filter(AgentLoginRecord.site_code == site_code,
                                                                       AgentLoginRecord.agent_account == agent_account)
        return data.all()

    @staticmethod
    def get_new_agent_count_sql(site_code, start_diff=0, end_diff=0, stop_day=0, date_type='月'):
        """
        获取本月新增代理数量 - 直属代理
        @return: {"agent": {"直属代理": 0, "团队代理": 0}}
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        new_count_dic = defaultdict(lambda: {"直属代理": 0, "团队代理": 0})
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_day, date_type, timezone)
        query_data = ms_context.get().session.query(AgentInfo). \
            filter(AgentInfo.site_code == site_code, AgentInfo.register_time.between(start_time, end_time)).all()

        # 通过path给所有代理增加数据
        for data in query_data:
            data: AgentInfo
            agent_path = agent_dic[data.agent_id][1][:-1]
            if data.parent_id:
                new_count_dic[agent_dic[data.parent_id][0]]["直属代理"] += 1
            for agent_id in agent_path:
                new_count_dic[agent_dic[agent_id][0]]["团队代理"] += 1
            new_count_dic["站点总计"]["团队代理"] += 1

        return new_count_dic

    @staticmethod
    def get_agent_withdraw_config_dao(site_code, agent_account=""):
        """
        获取代理提款配置
        @param site_code:
        @param agent_account:
        @return:
        """
        data = ms_context.get().session.query(AgentWithdrawConfig).filter(AgentWithdrawConfig.site_code == site_code)
        if agent_account:
            data = data.filter(AgentWithdrawConfig.agent_account == agent_account)
        return data.all()

    @staticmethod
    def get_agent_commission_final_report_sql(site_code, settle_cycle, agent_account=None, date_diff=0, stop_diff=0):
        """
        获取代理佣金报表， 从数据库查询
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        calc_type = System.get_settle_cycle()
        date_type = settle_cycle[-1]
        start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, stop_diff, date_type, timezone)

        data = ms_context.get().session.query(AgentCommissionFinalReport). \
            filter(AgentCommissionFinalReport.site_code == site_code,
                   AgentCommissionFinalReport.settle_cycle == calc_type[settle_cycle],
                   AgentCommissionFinalReport.start_time == start_time,
                   AgentCommissionFinalReport.end_time == end_time)
        if agent_account:
            data = data.filter(AgentCommissionFinalReport.agent_account == agent_account)
        return data.all()

    @staticmethod
    def get_agent_commission_expect_report_sql(site_code, settle_cycle, agent_account=None, date_diff=0, stop_diff=0):
        """
        获取代理佣金报表， 从数据库查询
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        calc_type = System.get_settle_cycle()
        date_type = settle_cycle[-1]
        start_time, end_time = DateUtil.get_timestamp_range(date_diff, date_diff, stop_diff, date_type, timezone)

        data = ms_context.get().session.query(AgentCommissionExpectReport). \
            filter(AgentCommissionExpectReport.site_code == site_code,
                   AgentCommissionExpectReport.settle_cycle == calc_type[settle_cycle],
                   AgentCommissionExpectReport.start_time == start_time,
                   AgentCommissionExpectReport.end_time == end_time)
        if agent_account:
            data = data.filter(AgentCommissionExpectReport.agent_account == agent_account)
        return data.all()

    @staticmethod
    def get_user_overflow_record_sql(site_code, user_account):
        """
        获取会员溢出记录
        @return:
        """
        data = ms_context.get().session.query(AgentUserOverflow). \
            filter(AgentUserOverflow.site_code == site_code, AgentUserOverflow.member_name == user_account,
                   AgentUserOverflow.audit_status == 1).first()
        return data.id

    @staticmethod
    def get_transfer_agent_record_sql(site_code, user_account):
        """
        获取会员转代记录
        @return:
        """
        data = ms_context.get().session.query(UserTransferAgent). \
            filter(UserTransferAgent.site_code == site_code, UserTransferAgent.user_account == user_account,
                   UserTransferAgent.audit_status == 1).first()
        return data.id

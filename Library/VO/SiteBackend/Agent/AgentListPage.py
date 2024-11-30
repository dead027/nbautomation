#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/9 21:29
from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.agent_info_model import AgentInfo


class AgentListPage(object):
    @staticmethod
    def get_agent_list(site_code, register_start_diff=0, register_end_diff=0, agent_account="", only_direct=False,
                       account_type="", account_status="", risk_level="", label="", register_type=""):
        """
        代理列表
        :param order_by  创建时间 ｜ 最近操作人
        :param order_type 升序 ｜ 降序
        @return:
        """
        # 基础数据
        agent_data = Dao.get_agent_list_data(site_code, register_start_diff, register_end_diff, agent_account,
                                             only_direct, account_type, account_status, risk_level, label,
                                             register_type)
        # 下级代理人数
        sub_agent_data = Dao.get_sub_agent_list(key='agent_account')
        result_list = []
        account_status_dic = Dao.get_agent_status(to_zh=True)
        agent_label_dic = {_.c.id: _.c.name for _ in Dao.get_agent_label_info(site_code)}
        register_type = Dao.get_user_register_client(to_zh=True)
        level_dic = {1: "总代", 2: "一级代理", 3: "二级代理"}
        account_type_dic = Dao.get_agent_type(to_zh=True)
        commission_dic = Dao.get_agent_commission_balance(site_code)
        quota_dic = Dao.get_agent_quota_balance(site_code)
        for item in agent_data:
            account = item.agent_account
            item: AgentInfo
            # 下级代理人数
            sub_agent_amount = len(sub_agent_data(account)["团队不包括自己"])
            # 直属代理人数
            direct_agent_amount = len(sub_agent_data(account)["直属"])
            # 下级会员人数
            sub_user_amount = Dao.get_users_of_agent(site_code)[account]

            sub_data = {"代理账号": account, "代理层级": item.level, "层级名称": level_dic[item.level],
                        "直属上级": item.creator, "账号类型": account_type_dic[item.agent_type],
                        "账号状态": account_status_dic[item.status], "风控等级": item.risk_level_id,
                        "标签": ",".join([agent_label_dic[_] for _ in item.agent_label_id.split(",")]),
                        "注册方式": register_type[item.register_way], "下级代理人数": sub_agent_amount,
                        "下级会员人数": len(sub_user_amount["团队不包括自己"]), "直属代理人数": direct_agent_amount,
                        "直属会员人数": len(sub_user_amount["直属"]),
                        "最后登录时间": DateUtil.timestamp_to_time(item.last_login_time),
                        "注册时间": DateUtil.timestamp_to_time(item.register_time),
                        "佣金钱包余额": commission_dic[account][2], "额度钱包余额": quota_dic[account][2], }
                        # "总存款金额": , "总存款次数": , "总提款金额": , "总提款次数": }
            result_list.append(sub_data)
        return result_list


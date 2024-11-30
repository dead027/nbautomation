#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 11:22
from Library.Common.Utils.DateUtil import DateUtil
from Library.Dao.Mysql.ChainQery import ChainQuery
from Library.Common.Utils.Contexts import ms_context


class Agent(object):

    @staticmethod
    def get_team_total_center_wallet_money(agent_account, query_type=1):
        """
        获取团队所有会员的中心钱包余额总额
        @param agent_account:
        @param query_type: 1 返回团体所有会员，2 返回直属会员，3 返回直属外所有会员
        @return:
        """
        users = [str(item[0]) for item in Agent.get_users_of_agent(agent_account, query_type)]
        users_str = '"' + '","'.join(users) + '"'
        sql = f'select sum(total_amount) from user_coin where user_account in ({users_str})'
        value = ms_context.get().query(sql)[0][0]
        return float(str(value)) if value else 0



#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 22:54
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Library.Common.Utils.Contexts import *
from Library.Dao.Mysql import Mysql as MysqlDao
from Library.Dao.MixQuery import MixQuery
from Library.Dao.Redis import Redis
from Library.Common.ServerConnector.Redis import RedisBase
from Library.Common.ServerConnector.Mysql import MysqlBase
from Library.Dao.Mysql.ChainQery.MasterBackend.Game import Game
from Library.Dao.Mysql.ChainQery.SiteBackend.Vip import Vip


class Dao(MysqlDao, Redis, MixQuery, Game):

    def __init__(self, env):
        self.env_setup(env)
        super().__init__()

    @staticmethod
    def env_setup(env):
        env_context.set(env)
        MysqlBase()
        RedisBase()
        Game()


if __name__ == '__main__':
    env_context.set('sit')
    dao = Dao('sit')

    # print(dao.get_lose_max(0))
    # print(dao.get_game_one_class_info_list_sql())
    # print(dao.get_venue_info_list_sql())

    site_code = 'Vd438R'
    # print(dao.get_user_vip_rank_config_sql(11))

    # 综合报表
    # data = dao.get_comprehensive_report_dao(site_code)
    # print(data)
    # 存取
    # data = dao.get_user_balance_dao(site_code, 'xyuser3')
    # print(data)

    # data = dao.get_level_up_required_valid_amount('xyuser7', site_code, level=3)

    # 返点佣金
    # data = dao.calc_rebate_commission_dao(site_code, "自然日")
    # print(data)

    # 负盈利佣金
    data = dao.calc_win_loss_commission(site_code, "自然日")
    print(data)


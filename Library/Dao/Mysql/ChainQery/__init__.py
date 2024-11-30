#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:00

# 基于链式查询
from Library.Dao.Mysql.ChainQery.SiteBackend import SiteBackend
from Library.Dao.Mysql.ChainQery.MasterBackend import MasterBackend
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import Funds
from Library.Dao.Mysql.ChainQery.SiteBackend.User import User
from Library.Dao.Mysql.ChainQery.SiteBackend.Game import Game
from Library.Dao.Mysql.ChainQery.Order import Order
from Library.Common.Utils.Contexts import *
from Library.Dao.Mysql.ChainQery.Admin import Admin


class ChainQuery(SiteBackend, MasterBackend, System, Funds, User, Game, Order, Admin):
    """
    链式mysql查询
    """
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    env_context.set('sit')
    print(ChainQuery.get_agent_label_info())

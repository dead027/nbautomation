#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 22:54
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from Library.Common.Utils.Contexts import *
from Library.BO.SiteBackend import SiteBackend

from Library.Common.ServerConnector.Redis import RedisBase
from Library.Common.ServerConnector.Mysql import MysqlBase


class BO(SiteBackend):

    def __init__(self, env):
        self.env_setup(env)
        super().__init__()

    @staticmethod
    def env_setup(env):
        env_context.set(env)
        MysqlBase()
        RedisBase()


if __name__ == '__main__':
    env_context.set('sit')
    bo = BO('sit')

    site_code = 'Vd438R'

    # 负盈利佣金
    data = bo.calc_win_loss_commission_dao(site_code, "自然日")
    print(data)


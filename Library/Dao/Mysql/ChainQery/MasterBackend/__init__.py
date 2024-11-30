#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/14 10:47
from Library.Dao.Mysql.ChainQery.MasterBackend.Game import Game
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Common.Utils.Contexts import *


class MasterBackend(Game, Site):
    """
    链式mysql查询
    """
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    env_context.set('dev')
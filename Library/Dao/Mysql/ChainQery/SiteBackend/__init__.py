#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/14 10:46
from Library.Dao.Mysql.ChainQery.SiteBackend.UserLabel import UserLabel
from Library.Dao.Mysql.ChainQery.SiteBackend.Vip import Vip
from Library.Dao.Mysql.ChainQery.SiteBackend.Medal import Medal
from Library.Dao.Mysql.ChainQery.SiteBackend.Agent import Agent
from Library.Dao.Mysql.ChainQery.SiteBackend.Report import Report
from Library.Dao.Mysql.ChainQery.SiteBackend.Activity import Activity
from Library.Dao.Mysql.ChainQery.SiteBackend.Game import Game
from Library.Common.Utils.Contexts import *


class SiteBackend(UserLabel, Vip, Medal, Agent, Report, Activity, Game):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    env_context.set('dev')
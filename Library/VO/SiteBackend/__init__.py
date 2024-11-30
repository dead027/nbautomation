#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/28 16:30
from Library.VO.SiteBackend.Agent import Agent
from Library.VO.SiteBackend.User import User
from Library.VO.SiteBackend.Report import Report
from Library.Common.Utils.Contexts import *


class SiteBackend(Agent, User, Report):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    env_context.set('dev')
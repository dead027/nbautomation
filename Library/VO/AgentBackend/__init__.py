#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/11/15 21:56
from Library.VO.AgentBackend.FrontPage import FrontPage
from Library.Common.Utils.Contexts import *


class AgentBackend(FrontPage):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    env_context.set('dev')
    site_code = 'Vd438R'
    agent_account = 'zscg1'
    rtn = AgentBackend.get_head_summary_vo(site_code, agent_account)
    print(rtn)

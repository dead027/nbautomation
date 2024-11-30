#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/1/25 11:27
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.ApiRequests.AgentApi.FrontModuleAgentApi import FrontModuleAgentApi
from Library.ApiRequests.AgentApi.ReportsModuleAgentApi import ReportsModuleAgentApi


class AgentApi(ReportsModuleAgentApi, FrontModuleAgentApi):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        ReportsModuleAgentApi.__init__(self)
        FrontModuleAgentApi.__init__(self)


if __name__ == "__main__":
    # m4 = MainBackendLibrary("sit")
    pass

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/1/25 11:27
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.ApiRequests.BackendApi.UserModuleBackendApi import UserModuleBackendApi
from Library.ApiRequests.BackendApi.FundsModuleBackendApi import FundsModuleAgentApi
from Library.ApiRequests.BackendApi.GameModuleBackendApi import GameModuleBackendApi
# from Library.ApiRequests.BackendApi.AgentModuleBackendApi import AgentModuleAgentApi


class BackendApi(UserModuleBackendApi, FundsModuleAgentApi, GameModuleBackendApi):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        UserModuleBackendApi.__init__(self)
        FundsModuleAgentApi.__init__(self)
        GameModuleBackendApi.__init__(self)
        # AgentModuleAgentApi.__init__(self)


if __name__ == "__main__":
    # m4 = MainBackendLibrary("sit")
    pass

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/8 14:47
from Library.ApiRequests.ClientApi.LoginPageApi import LoginPageApi
from Library.ApiRequests.ClientApi.ActivityApi import ActivityApi
from Library.ApiRequests.ClientApi.UserApi import UserApi


class ClientApi(LoginPageApi, ActivityApi, UserApi):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        LoginPageApi.__init__(self)


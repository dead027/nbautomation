#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/9 15:03
from Library.ApiRequests.SiteBackendApi.UserModuleSiteApi import UserModuleSiteApi
from Library.ApiRequests.SiteBackendApi.ActivityApi import ActivityApi
from Library.ApiRequests.SiteBackendApi.FundsApi import FundsApi
from Library.ApiRequests.SiteBackendApi.AgentApi import AgentApi
from Library.ApiRequests.SiteBackendApi.ReportApi import ReportApi


class SiteBackendApi(UserModuleSiteApi, ActivityApi, FundsApi, AgentApi, ReportApi):
    def __init__(self):
        super().__init__()


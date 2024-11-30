#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/15 16:08
from Library.VO.SiteBackend.User.NewUserAuditPage import NewUserAuditPage
from Library.VO.SiteBackend.User.UserDetail import UserDetail
from Library.VO.SiteBackend.User.UserUpdateAuditPage import UserUpdateAuditPage


class User(NewUserAuditPage, UserDetail, UserUpdateAuditPage):
    def __init__(self):
        super().__init__()

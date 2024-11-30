#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/11/2 11:15
from Library.BO.SiteBackend.Commission import Commission
from Library.BO.SiteBackend.Report import Report


class SiteBackend(Commission, Report):
    """
    链式mysql查询
    """
    def __init__(self):
        super().__init__()

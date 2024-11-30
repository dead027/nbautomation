#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/31 22:19

from Library.ApiRequests.SbApi.BaseOperation import BaseOperation
from Library.ApiRequests.SbApi.BusinessOperation import BusinessOperation


class SbApi(BaseOperation, BusinessOperation):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        BaseOperation.__init__(self)
        BusinessOperation.__init__(self)


if __name__ == '__main__':
    pass

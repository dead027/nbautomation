#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/1/25 11:47
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Dao.Mysql import Mysql
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil


class ReportsModuleAgentApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    backend_host = YamlUtil.get_backend_host()


if __name__ == '__main__':
    pass

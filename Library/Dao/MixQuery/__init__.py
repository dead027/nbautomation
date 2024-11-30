#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/9 14:52
from Library.Dao.MixQuery.MixMasterBackend import MixMasterBackend
from Library.Common.Utils.Contexts import *


class MixQuery(MixMasterBackend):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    from Library.Common.ServerConnector.Mysql import MysqlBase
    from Library.Common.ServerConnector.Redis import RedisBase
    env_context.set('dev')
    MysqlBase()
    RedisBase()
    mq = MixQuery()
    rtn = mq.unlock_backend_account('superAdmin01')
    print(rtn)

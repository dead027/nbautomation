#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/9 14:46

# from Library.Dao.Mysql.OriginQuery import OriginQuery
from Library.Dao.Mysql.ChainQery import ChainQuery


class Mysql(ChainQuery):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    from Library.Common.Utils.Contexts import *
    from Library.Common.ServerConnector.Mysql import MysqlBase as Mysql1

    env_context.set('sit')
    Mysql1().__init__()
    # print(ChainQuery.get_new_register_chart('月', -1))
    print(ChainQuery.get_level_up_required_valid_amount('年', 0))




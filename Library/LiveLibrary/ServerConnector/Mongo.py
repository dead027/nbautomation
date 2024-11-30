import time

import pymongo
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from Library.Common.Utils.Contexts import *
from Library.LiveLibrary.CommonUtil import CommonFunc
from Library.Common.Utils.YamlUtil import YamlUtil


class MongoBase(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        server_info = YamlUtil().load_common_config('mongo', 'live')
        self.client = pymongo.MongoClient('mongodb://{}:{}@{}:{}/mydb?authSource={}'.format(server_info['username'],
                                                                                            server_info['password'],
                                                                                            server_info['host'],
                                                                                            server_info['port'],
                                                                                            server_info['db']))
        self.my_db = self.client[server_info['db']]
        self.cf = CommonFunc()
        live_mg_context.set(self)

    def switch_database(self, db_name):
        self.my_db = self.client[db_name]

    def mg_select(self, table, condition_sql=None, choose_sql=None, sort=None, limit=10000):
        """
        mongo 通用查询
        :param table:
        :param condition_sql:
        :param choose_sql:
        :param sort:
        :param limit:
        :return:
        """
        return list(self.my_db[table].find(filter=condition_sql, projection=choose_sql, sort=sort, limit=limit))

    def mg_aggregate(self, table, sql):
        """
        mongo 聚合查询
        :param table:
        :param sql:
        :return:
        """
        return list(self.my_db[table].aggregate(sql))

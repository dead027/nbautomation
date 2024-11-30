import pymysql
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.LiveLibrary.CommonUtil import SingletonType


class MysqlBase(object, metaclass=SingletonType):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        server_info = YamlUtil().load_common_config('mysql', 'live')
        print(server_info)
        self.connect = pymysql.connect(host=server_info['host'], port=server_info['port'], user=server_info['username'],
                                       password=server_info['password'], charset='utf8', autocommit=True,
                                       database=server_info['db_name'])
        self.cursor = self.connect.cursor()

    # 关闭数据库
    def close_db(self):
        """
        关闭数据库
        :return:
        """
        self.cursor.close()
        self.connect.close()

    def query_data(self, sql, db_name=""):
        """
        数据查询
        :param sql:
        :param db_name:
        :return:
        """
        # print(sql)
        try:
            if db_name:
                self.change_db(db_name)
            self.cursor.execute(sql)
            res = self.cursor.fetchall()
        except pymysql.Error as e:
            print(e)
            print(AssertionError, "查询结果为空")
            return
        return res

    def update_data(self, sql, db_name=""):
        """
        修改
        :param sql:
        :param db_name:
        :return:
        """
        try:
            self.change_db(db_name)
            self.cursor.execute(sql)
            self.connect.commit()
        except Exception:
            raise(AssertionError, "修改失败！")

    def change_db(self, db_name):
        try:
            self.connect.select_db(db_name)
        except Exception as e:
            print(e)


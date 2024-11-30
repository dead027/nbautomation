# import pymysql
# from Library.Common.Utils.SingletonTypeUtil import SingletonType
# from Library.Common.Utils.YamlUtil import YamlUtil
# from Library.Common.Utils.Contexts import ms_context
#
#
# class MysqlBase(metaclass=SingletonType):
#     ROBOT_LIBRARY_SCOPE = 'GLOBAL'
#
#     def __init__(self, *args, **kwargs):
#         try:
#             super().__init__()
#         except TypeError:
#             super().__init__()
#         server = YamlUtil().load_common_config('mysql')
#         self.connect = pymysql.connect(host=server.ip, port=server.port, user=server.username,
#                                        password=server.password, charset='utf8', autocommit=True,
#                                        database=server.database)
#         self.cursor = self.connect.cursor()
#
#     # 关闭数据库
#     def close_db(self):
#         """
#         关闭数据库
#         :return:
#         """
#         self.cursor.close()
#         self.connect.close()
#
#     def execute_many(self, sql, data_list, db_name=""):
#         if db_name:
#             self.change_db(db_name)
#         self.cursor.executemany(sql, data_list)
#         res = self.cursor.fetchall()
#         return res
#
#     def query_data(self, sql, db_name=""):
#         """
#         数据查询
#         :param sql:
#         :param db_name:
#         :return:
#         """
#         # print(sql)
#         if db_name:
#             self.change_db(db_name)
#         self.cursor.execute(sql)
#         res = self.cursor.fetchall()
#         return res
#
#     def update_data(self, sql, db_name=""):
#         """
#         修改
#         :param sql:
#         :param db_name:
#         :return:
#         """
#         try:
#             self.change_db(db_name)
#             self.cursor.execute(sql)
#             self.connect.commit()
#         except Exception:
#             raise(AssertionError, "修改失败！")
#
#     def change_db(self, db_name):
#         try:
#             self.connect.select_db(db_name)
#         except Exception as e:
#             print(e)
#
#
# if __name__ == '__main__':
#     a = MysqlBase('uat')

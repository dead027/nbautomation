#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/31 11:13
import csv
from Library.Common.Utils.Contexts import *
from sqlalchemy.sql import text


class ReloadMenuTable(object):
    @staticmethod
    def export_menu():
        result = ms_context.get().query(f"SELECT * FROM business_menu")
        # 将结果导出为CSV文件 - 总控后台
        with open('output_main.csv', 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(("id", "business_system", "menu_key", "name", "parent_id", "order_num", "path",
                             "api_url", "url", "type", "level", "visible", "status", "created_time", "updated_time",
                             "remark", "super_admin_only_visible", "business_id", "creator", "updater"))
            # print(result)
            writer.writerows(result)
        # result = ms_context.get().query(f"SELECT * FROM site_menu")
        # 将结果导出为CSV文件 - 站点后台
        # with open('output_site.csv', 'w', newline='', encoding='utf-8') as f:
        #     writer = csv.writer(f)
        #     writer.writerow(("id", "site_code", "menu_key", "name", "parent_id", "order_num", "path", "api_url",
        #                      "url", "type", "level", "visible", "status", "creator", "updater", "created_time",
        #                      "updated_time", "remark", "super_admin_only_visible", "site_id"))
        #     # print(result)
        #     writer.writerows(result)

    @staticmethod
    def import_menu():
        with open('output_main.csv', mode='r') as file:
            reader = list(csv.DictReader(file))
            insert_query = text("INSERT INTO business_menu VALUES (:id, :business_system, :menu_key, :name, "
                                ":parent_id, :order_num, :path, :api_url, :url, :type, :level, :visible, :status, "
                                ":created_time, :updated_time, :remark, :super_admin_only_visible, :business_id, "
                                ":creator, :updater)")
            for index, item in enumerate(reader):
                for key, value in item.items():
                    if value == "" and value != 0:
                        reader[index][key] = None
            print("INSERT INTO business_menu VALUES (:id, :business_system, :menu_key, :name, "
                  ":parent_id, :order_num, :path, :api_url, :url, :type, :level, :visible, :status, "
                  ":created_time, :updated_time, :remark, :super_admin_only_visible, :business_id, "
                  ":creator, :updater)")
            print(reader)
            print(ms_context.get().cursor_dic['baowang_sit'].execute(insert_query, reader))
        # with open('output_site.csv', mode='r') as file:
        #     reader = list(csv.DictReader(file))
        #     insert_query = text("INSERT INTO site_menu VALUES (:id, :site_code, :menu_key, :name, :parent_id, "
        #                         ":order_num, :path, :api_url," ":url, :type, :level, :visible, :status, :creator, "
        #                         ":updater, :created_time,:updated_time, :remark, :super_admin_only_visible, :site_id)")
        #     for index, item in enumerate(reader):
        #         for key, value in item.items():
        #             if value == "":
        #                 reader[index][key] = None
        #     print(ms_context.get().cursor_dic['baowang_sit'].execute(insert_query, reader))

    @staticmethod
    def truncate_table():
        ms_context.get().update("truncate table baowang_sit.business_menu")
        # ms_context.get().update("truncate table baowang_sit.site_menu")


if __name__ == '__main__':
    from Library.Common.ServerConnector.Mysql import MysqlBase
    import time

    csv_path = 'output.csv'
    env_context.set('dev')
    MysqlBase()
    ReloadMenuTable.export_menu()
    print("================")
    time.sleep(2)
    env_context.set('sit')
    ms_context.get().__init__()
    ReloadMenuTable.truncate_table()
    ReloadMenuTable.import_menu()

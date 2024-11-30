#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 15:53
from Library.Common.Utils.DateUtil import DateUtil
from Library.Dao.Mysql import Mysql


class ReportModule(object):
    """
    报表模块
    """

    @staticmethod
    def foo(start_diff=-7, end_diff=-1, date_type='日'):
        """
        返水报表
        :param start_diff:
        :param end_diff:
        :param date_type:
        :return:
        """
        # 人工调整
        start_timestamp, end_timestamp = DateUtil.get_timestamp_range(start_diff, end_diff, date_type=date_type)
        sql = f'select count(1),sum(amount) from (select user_account,sum(if(adjust_way=1,adjust_amount,' \
              f'-adjust_amount)) as amount from user_manual_up_down_record where order_status=6 and' \
              f' adjust_type=2 and updated_time between {start_timestamp} and {end_timestamp} group by ' \
              f'user_account) a '
        data = ms_context.get().query(sql)[0]
        if data == (0, None):
            data = []
        # 注单返水
        data_list = Mongo.get_rebate_report_mg(start_diff, end_diff, date_type)
        data_list = [list(item) for item in data_list]
        full_data = []
        sum_data = [0] * 2
        if data:
            full_data.append(["人工调整", float(str(data[1])) if data[1] else 0,
                              float(str(data[0])) if data[0] else 0])
            sum_data[0] += float(data[1]) if data[1] else 0
            sum_data[1] += float(data[0]) if data[0] else 0

        venue_dic = Mysql.get_venue_dic()
        for data in data_list:
            data[0] = venue_dic[data[0]]
            data[1] = round(data[1], 2)
            full_data.append(data)
            for index in range(2):
                sum_data[index] = round(sum_data[index] + data[index + 1], 2)

        return full_data, sum_data

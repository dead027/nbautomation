#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/5 18:16
from decimal import Decimal
from Library.Dao import Dao
from collections import defaultdict


class TaskReport(object):
    """
    任务报表
    """

    @staticmethod
    def get_task_report_vo(site_code, start_diff=0, end_diff=0, task_id=None, task_type=None, stop_diff=0,
                           date_type='日'):
        """
        任务报表
        @return:
        """
        data = Dao.get_task_report(site_code, start_diff, end_diff, task_id, stop_diff, task_type, date_type)

        result_data = defaultdict(lambda: {"统计日期": "", "任务ID": "", "任务名称": "", "任务类型": "", "发放人数": 0,
                                           "发放彩金金额": 0, "已领取人数": 0, "已领取彩金金额": 0})
        task_type_dic = Dao.get_task_type(to_zh=True)
        for _ in data:
            result_data[(_[0], _[1])]["统计日期"] = _[3]
            result_data[(_[0], _[1])]["任务ID"] = _[0]
            result_data[(_[0], _[1])]["任务名称"] = _[1]
            result_data[(_[0], _[1])]["任务类型"] = task_type_dic[_[2]]
            result_data[(_[0], _[1])]["发放人数"] = _[5] if _[5] else 0
            result_data[(_[0], _[1])]["发放彩金金额"] += _[4] if _[4] else 0
            result_data[(_[0], _[1])]["已领取人数"] += _[6] if _[6] else 0
            result_data[(_[0], _[1])]["已领取彩金金额"] += _[7] if _[7] else 0
        return list(result_data.values())

    @staticmethod
    def get_task_report_total_vo(site_code, start_diff=0, end_diff=0, task_id=None, task_type=None, stop_diff=0,
                                 date_type='日'):
        """
        任务报表 - 总计
        @return:
        """
        data = Dao.get_task_total_report(site_code, start_diff, end_diff, task_id, task_type, stop_diff, date_type)
        print(data)
        return {"发放人数": 0 if not data[1] else data[1],
                "发放彩金金额": Decimal(0) if not data[0] else data[0],
                "已领取人数": Decimal(0) if not data[2] else data[2],
                "已领取彩金金额": Decimal(0) if not data[3] else data[3]}

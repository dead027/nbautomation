#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/12 22:18
import time
import json

import requests
from urllib.parse import urlencode
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.DateUtil import DateUtil

session = requests.session()


class BaseOperation(object):

    @staticmethod
    def _execute_job(job_id, param=None):
        """
        执行定时任务
        @param job_id:
        @return:
        """
        server = YamlUtil().load_common_config('job')
        url = server['host'] + '/xxl-job-admin/jobinfo/trigger'
        params = {"id": job_id,
                  "executorParam": str(param),
                  'addressList': ""}
        rsp = HttpRequestUtil.post(url, data=params, headers=job_client_header_context.get(),
                                   check_code=False, return_origin=True)
        if rsp.status_code != 200:
            raise AssertionError(f"job 执行失败: {rsp.status_code}")

    @staticmethod
    def trigger_task(name, timeout=4, param=None):
        task_id = BaseOperation._get_task_info(name)[0]
        # 执行前获取执行id
        data_before = BaseOperation._get_current_job_id_list(name)
        data_before = [item[0] for item in data_before]
        BaseOperation._execute_job(task_id, param)
        start_time = current_time = int(time.time())
        while current_time - start_time < timeout:
            time.sleep(0.2)
            data_after = BaseOperation._get_current_job_id_list(name)
            data_after = [item[0] for item in data_after]
            diff = set(data_after) - set(data_before)
            if diff:
                print(f"------- {list(diff)}")
                return list(diff)[0]
            current_time = int(time.time())
        raise AssertionError(f"xxl job 执行超时: {timeout}秒")

    @staticmethod
    def _get_task_info(name):
        """
        获取定时任务信息
        @param name:
        @return: job id  | job group
        """
        server = YamlUtil().load_common_config('job')
        url = server['host'] + '/xxl-job-admin/jobinfo/pageList'
        params = {"jobGroup": 60002,
                  "triggerStatus": -1,
                  "jobDesc": name,
                  "executorHandler": "",
                  "author": "",
                  "start": 0,
                  "length": 10}
        rsp = HttpRequestUtil.post(url, params=params, headers=job_client_header_context.get(), check_code=False)
        if rsp['recordsFiltered'] >= 0:
            return rsp['data'][0]['id'], rsp['data'][0]['jobGroup']
        raise AssertionError('没查到对应到任务，请检查任务名称是否正确')

    @staticmethod
    def _get_current_job_id_list(name, limit=10):
        """
        获取最新的执行任务id
        @param name:
        @return:
        """
        server = YamlUtil().load_common_config('job')
        task_id, task_group = BaseOperation._get_task_info(name)
        url = server['host'] + '/xxl-job-admin/joblog/pageList'
        start_day = DateUtil.get_sb_search_time(0, '日')
        params = {"jobGroup": task_group,
                  "jobId": task_id,
                  "logStatus": -1,
                  "filterTime": f'{start_day} 00:00:00 - {start_day} 23:59:59',
                  'start': 0,
                  'length': limit}
        rsp = HttpRequestUtil.post(url, params=params, headers=job_client_header_context.get(), check_code=False)
        return [(item['id'], item['handleCode']) for item in rsp['data']]

    @staticmethod
    def wait_until_job_success(name, exec_id, timeout=5):
        start_time = current_time = int(time.time())
        while current_time - start_time < timeout:
            data = BaseOperation._get_current_job_id_list(name)
            for item in data:
                if item[0] == exec_id:
                    if item[1] == 200:
                        return
                    else:
                        break
            time.sleep(0.4)
            current_time = int(time.time())
        raise AssertionError(f"xxl job 执行超时: {timeout}秒")


if __name__ == '__main__':
    from Library.Common.Utils.LoginUtil import LoginUtil
    env_context.set('sit')
    LoginUtil.login_job()
    job_dic = {'VIP升级定时任务', '沙巴体育拉单', 'PG电子自动拉单', '神话视讯平台拉取订单',
               'VIP等级配置凌晨0点10秒刷新', 'VIP权益配置凌晨0点20秒刷新定时任务'}
    BaseOperation.trigger_task('神话视讯平台拉取订单')



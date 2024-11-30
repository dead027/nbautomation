#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/1 12:51
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.Contexts import *
import requests


class BaseOperation(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    session = requests.Session()
    session.verify = False

    @staticmethod
    def register_sb(account):
        host = YamlUtil().load_common_config('sb')
        url = host['register_host'] + '/api/CreateMember'
        params = {"vendor_id": host['vendor_id'],
                  "vendor_member_id": host['prefix'] + account,
                  "operatorId": host['operatorId'],
                  "username": account,
                  "oddstype": 1,
                  "currency": 20,
                  "maxtransfer": 10000,
                  "mintransfer": 0}
        rtn = BaseOperation.session.post(url, data=params).json()
        if rtn["error_code"] != 0:
            raise AssertionError(f"注册失败：{rtn}")

    @staticmethod
    def login_sb(account):
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + '/login'
        params = {"vendor_id": host['vendor_id'],
                  "vendor_member_id": host['prefix'] + account}
        header = HttpRequestUtil.build_headers(url)
        response = HttpRequestUtil.post(url, json=params, headers=header, check_code=False)
        token = response['access_token']
        # 登录后
        header.update({"Authorization": 'Bearer ' + token, 'Accept': 'appilcation/json, text/plain, */*',
                       "X-Forwarded-For": "202.178.124.126", "Accept-Encoding": 'br,gzip,deflate',
                       "Accept-Language": "zh-CN,zh;q=0.9"})
        sb_client_header_context.set(header)
        sb_token_context.set(token)

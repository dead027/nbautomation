# -*- coding: UTF-8 -*-

"""
@Project : AutomatedTest-Bw 
@File    : login_util
@Author  : xy
@Date    : 2024/4/25 14:35
@Describe: 登陆工具
"""
import requests
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.CaptchaUtil import CaptchaUtil
from Library.Dao.Mysql.ChainQery.Admin import Admin, BusinessAdmin
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.AesUtil import AesUtil


class LoginUtil:

    @classmethod
    def login_backend(cls, username, password, check_code=True):
        """
        谷歌密钥登录 - 总台
        :return:
        """
        admin = Admin.get_admin_info_sql(username)
        google_verify_code = CaptchaUtil.get_google_code(admin.google_auth_key)
        host = YamlUtil.get_backend_host()
        url = host + "/api/admin-center/business_admin_login/api/login"
        request_data = {"userName": username, "password": password, "verifyCode": google_verify_code}
        header = HttpRequestUtil.build_headers(url)
        resp = HttpRequestUtil.post(url, json=request_data, headers=header, check_code=check_code)
        if not check_code:
            return resp
        header.update({"Sign": f'Bearer {resp["data"]["token"]}'})
        header_backend_context.set(header)

    @classmethod
    def login_site_backend(cls, site_code, username, password, site_index='1', check_code=True):
        """
        谷歌密钥登录 - 站点后台
        :return:
        """
        admin: BusinessAdmin = Admin.get_admin_info_sql(username, site_code)
        google_verify_code = CaptchaUtil.get_google_code(admin.google_auth_key)
        host = YamlUtil.get_site_host(site_index)
        url = host + "/site/site_admin_login/api/login"
        request_data = {"userName": username, "password": password, "verifyCode": google_verify_code,
                        "siteCode": admin.site_code}
        # 登录前
        header = HttpRequestUtil.build_headers(url)
        header.update({"Sign": AesUtil().encrypt_before_login_get_sign()})
        resp = HttpRequestUtil.post(url, json=request_data, headers=header, check_code=check_code)
        if not check_code:
            return resp
        header.update({"Sign": AesUtil().encrypt_after_get_sign(resp["data"]["token"])})
        header_site_context_1.set(header) if int(site_index) == 1 else header_site_context_2.set(header)

    @staticmethod
    def login_agent(username, password, site_index='1'):
        """
        登陆代理
        :return:
        """
        host = YamlUtil.get_agent_host(site_index)
        url = host + '/api/admin-agent/agent/login'
        get_code_url = host + '/api/admin-agent/agent/captcha'
        uuid, code = CaptchaUtil.get_captcha(get_code_url)
        request_data = {"agentAccount": username, "password": password,
                        "verifyCode": code,
                        "codeKey": uuid}
        # 登录前
        header = HttpRequestUtil.build_headers(url)
        header.update({"Sign": AesUtil().encrypt_before_login_get_sign()})
        response = HttpRequestUtil.post(url, json=request_data, headers=header)
        token = response['data']['token']
        # 登录后
        header.update({"Sign": AesUtil().encrypt_after_get_sign(token)})
        header_agent_context_1.set(header) if int(site_index) == 1 else header_agent_context_2.set(header)

    @staticmethod
    def login_client(username, password='abcd1234', check_code=True, site_index='1'):
        """
        登录客户端
        @return:
        """
        host = YamlUtil.get_client_host(site_index)
        url = host + '/app/login/api/userLogin'
        request_data = {"userAccount": username, "password": password, "verifyToken": True}
        # 登录前
        header = HttpRequestUtil.build_headers(url)
        header.update({"Sign": AesUtil().encrypt_before_login_get_sign()})
        response = HttpRequestUtil.post(url, json=request_data, headers=header, check_code=check_code)
        if not check_code:
            return response
        token = response['data']['token']
        # 登录后
        header.update({"Sign": AesUtil().encrypt_after_get_sign(token)})
        header_client_context_1.set(header) if int(site_index) == 1 else header_client_context_2.set(header)

    @staticmethod
    def login_job():
        server = YamlUtil().load_common_config('job')
        url = server['host'] + '/xxl-job-admin/login'
        params = {"userName": server['username'],
                  "password": server['password']}
        header = HttpRequestUtil.build_headers(url, content_type='params')
        response = HttpRequestUtil.post(url, params=params, headers=header, check_code=False, return_origin=True)
        # 登录后
        header.update({'Accept': 'appilcation/json, text/plain, */*',
                       "X-Forwarded-For": "202.178.124.126", "Accept-Encoding": 'br,gzip,deflate',
                       "Accept-Language": "zh-CN,zh;q=0.9",
                       'Cookie': f'XXL_JOB_LOGIN_IDENTITY={response.cookies.get("XXL_JOB_LOGIN_IDENTITY")}'})
        job_client_header_context.set(header)


if __name__ == '__main__':
    from Library.Common.ServerConnector.Mysql import MysqlBase
    from Library.Common.ServerConnector.Redis import RedisBase

    env_context.set("sit")
    MysqlBase()
    RedisBase()
    # LoginUtil.login_client('testuser1', 'abcd1234')
    # LoginUtil.login_backend('xingyao1', 'abcd1234')
    LoginUtil.login_site_backend('MNtniq', 'xingyao11', 'abcd1234')

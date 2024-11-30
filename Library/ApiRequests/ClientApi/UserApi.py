#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/16 11:16
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Enum.FundsEnum import FundsEnum
from Library.Common.Utils.AesUtil import AesUtil
from Library.MysqlTableModel.venue_info_model import VenueInfo
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.agent_info_model import AgentInfo
from Library.MysqlTableModel.game_info_model import GameInfo
from Library.Dao import Dao
from Library.Common.Utils.Contexts import *
from Library.Dao.Mysql.ChainQery.System import System


class UserApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def send_user_sms_code_api(area_code, phone, check_code=True, site_index='1'):
        """
        获取手机验证码
        :return:
        """
        url = YamlUtil.get_client_host() + '/app/user-info/global/sendSms'
        params = {"areaCode": area_code, "phone": phone}
        resp = HttpRequestUtil.post(url, params, headers=header_client_context_1.get(), check_code=check_code,
                                    site_index=site_index)
        return resp['message']

    @staticmethod
    def send_user_email_code_api(email, check_code=True, site_index='1'):
        """
        获取邮箱验证码
        :return:
        """
        url = YamlUtil.get_client_host() + '/app/user-info/global/sendMail'
        params = {"email": email}
        resp = HttpRequestUtil.post(url, params, headers=header_client_context_1.get(), check_code=check_code,
                                    site_index=site_index)
        return resp['message']

    @staticmethod
    def bind_account_api(account, bind_type, code, area="", check_code=True, site_index='1'):
        """
        绑定会员账号，手机、邮箱
        @param account:
        @param bind_type: 手机号码 ｜ 邮箱
        @param code:
        @param area:
        @param check_code:
        @param site_index:
        @return:
        """
        url = YamlUtil.get_client_host() + '/app/user-info/global/bindAccount'
        bind_type_dic = {"手机号码": 2, "邮箱": 1}
        params = {"areaCode": area, "account": account, "type": bind_type_dic[bind_type], "verifyCode": code}
        resp = HttpRequestUtil.post(url, params, headers=header_client_context_1.get(), check_code=check_code,
                                    site_index=site_index)
        return resp['message']



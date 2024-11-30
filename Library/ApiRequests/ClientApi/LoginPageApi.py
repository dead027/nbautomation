#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/1 11:04
import hashlib

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


class LoginPageApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def register_from_client(site_code, user_account, password="abcd1234", currency='CNY',
                             agent_account="", device_no="iphone", check_code=True, site_index='1'):
        """
        客户端注册会员并登录
        @return:
        """

        url = YamlUtil.get_client_host(site_index) + '/app/login/api/userRegister'
        header = HttpRequestUtil.build_headers(url)
        header.update({"Sign": AesUtil().encrypt_before_login_get_sign()})
        params = {"verifyToken": "test", "userAccount": user_account, "password": password, "inviteCode": "",
                  "confirmPassword": password, "mainCurrency": currency, "deviceNo": device_no}
        if agent_account:
            agent_info: AgentInfo = Dao.get_agent_info(site_code, agent_account)
            params["inviteCode"] = agent_info.invite_code
        # 发起注册请求
        resp = HttpRequestUtil.post(url, params, check_code=check_code, headers=header, site_index=site_index)
        if not check_code:
            return resp['message']
        # 获取验证码
        # LoginPageApi.send_user_verify_code(f'{area_code}{account}', register_type, headers=header)
        # verify_code = Redis.get_msg_code_rds(f'{area_code}{account}')
        # params['verifyCode'] = verify_code
        # 提交注册申请
        # url = YamlUtil.get_client_host() + '/app/login/api/userRegister'
        # resp = HttpRequestUtil.post(url, params, check_code=check_code, headers=header, site_index=site_index)
        # print(resp)
        # token = resp['data']['token']
        # 登录后
        # header.update({"Sign": AesUtil().encrypt_after_get_sign(token)})
        # header_client_context.set(header)
        # return register_account

    @staticmethod
    def enter_game_sh(game_code, device_type="H5", check_code=True):
        """
        进入金喜真人游戏
        @return:
        """
        venue_name = '视界真人'
        url = YamlUtil.get_client_host() + '/app/third/api/loginGame'
        game_info: GameInfo = Dao.get_game_info_dao(venue=venue_name)[0]
        params = {"device": device_type, "venueCode": game_info.venue_code, "gameCode": game_code}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, headers=header_client_context_1.get())

        if not check_code:
            return resp['message']
        source_url = resp["data"]["source"]
        return source_url[source_url.find("token=") + 6:].split("&")[0]

    @staticmethod
    def _get_sign(merchant_sign, merchant_no, time_stamp, user_id):
        origin_str = f"{merchant_sign}|{merchant_no}|{user_id}"
        md5_sign = hashlib.md5(origin_str.encode()).hexdigest().upper()
        hash_sign = hashlib.sha256(
            f"{merchant_no}{time_stamp}{merchant_sign}".encode()).hexdigest()
        return md5_sign, hash_sign

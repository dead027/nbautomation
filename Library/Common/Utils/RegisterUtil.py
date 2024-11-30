# -*- coding: UTF-8 -*-

"""
@Project : AutomatedTest-Bw 
@File    : register_util.py
@Author  : 带篮子
@Date    : 2024/4/13 15:42
"""
import json
from dataclasses import asdict

from common.config.redis_config import RedisConfig
from common.utils.aes_util import AesEncryptionUtil
from common.utils.captcha_util import CaptchaUtil
from common.utils.excel_chain_util import ExcelDataChain
from common.utils.grequests_util import GRequestsUtil
from common.utils.login_util import LoginUtil, LoginUtilAdminTokenVar
from constant.admin import BW_ADMIN_AUTHORIZATION, BW_ADMIN_SHEET_NAME, BW_ADMIN_LOGIN_GROUP
from pojo.bo.agent.register_agent_batch_bo import RegisterAgentBatchBo
from pojo.bo.user.register_user_batch_bo import RegisterUserBatchBo

# 初始化配置和工具类实例
REDIS = RedisConfig()
AES = AesEncryptionUtil()


class RegisterUtil:
    """
    注册用户工具类，提供单个和批量注册功能。
    """

    @staticmethod
    def register(register_url: str, json_data: dict):
        """
        发送单个用户注册请求。
        :param register_url: 注册API的URL。
        :param json_data: 包含注册信息的字典。
        :return: None
        """
        if not register_url:
            raise ValueError("register_url 不能为空")
        sign = AES.encrypt_before_login_get_sign()
        request = GRequestsUtil.common_post(register_url, json=json_data, extra_headers={"Sign": sign})
        GRequestsUtil.send_request(request)

    @staticmethod
    def register_user_batch(param: RegisterUserBatchBo):
        """
        批量注册用户
        :param param: RegisterUserBatchBo
        :return:
        """
        if not param.registerUrl:
            raise ValueError("register_url 不能为空")
        request_list = []
        for index, (uuid, code) in enumerate(param.uuidCode.items(), start=1):
            json_data = {
                "userAccount": f"{param.userAccountPrefix}{param.baseSuffix + index - 1}",
                "password": "admin123",
                "password2": "admin123",
                "inviteCode": param.inviteCode,
                "friendInviteCode": param.friendInviteCode,
                "verifyCode": code,
                "codeKey": uuid
            }
            request_list.append(GRequestsUtil.common_post(param.registerUrl, json=json_data,
                                                          extra_headers={"Sign": AES.encrypt_before_login_get_sign()}))
        GRequestsUtil.map_requests(request_list, len(param.uuidCode))

    @staticmethod
    def register_agent_batch(param: RegisterAgentBatchBo):
        """
        批量注册代理
        :param param: RegisterAgentBatchBo
        :return:
        """
        request_list = []
        for index in range(1, 201):  # 固定200次
            param.agentAccount = f"{param.userAccountPrefix}{param.baseSuffix + index - 1}"
            json = asdict(param)
            request_list.append(
                GRequestsUtil.common_post(param.registerUrl, json=json,
                                          extra_headers={BW_ADMIN_AUTHORIZATION: param.token}))
        GRequestsUtil.map_requests(request_list, 200)


if __name__ == '__main__':
    # 示例用法
    for i in range(1, 400, 200):
        uuid_code = CaptchaUtil.get_captcha_batch("https://h5.playes.bar/api/user-api/login/captcha")
        param = RegisterUserBatchBo(
            registerUrl="https://h5.playes.bar/api/user-api/login/userRegister",
            uuidCode=uuid_code,
        )
        RegisterUtil.register_user_batch(param)

    # 示例用法
    param = RegisterAgentBatchBo(
        registerUrl="https://gw2.playes.bar/admin-center/agent-add/api/addGeneralAgent",
    )

    case = ExcelDataChain().get_sheet(BW_ADMIN_SHEET_NAME).filter(BW_ADMIN_LOGIN_GROUP, 1).first()
    LoginUtil.login_admin(case)
    param.token = LoginUtilAdminTokenVar.get()

    for i in range(1, 401, 200):
        param.baseSuffix = i
        RegisterUtil.register_agent_batch(param)

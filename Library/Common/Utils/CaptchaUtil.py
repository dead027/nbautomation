import logging
import re
import time
import uuid
import pyotp
from datetime import datetime
from Library.Common.Utils.AesUtil import AesUtil
import requests
from Library.Common.Utils.Contexts import rds_context, env_context
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from nopecha.api.requests import RequestsAPIClient
from Library.Common.Utils.YamlUtil import YamlUtil


# 获取验证码工具类
class CaptchaUtil:
    @staticmethod
    def get_google_code(google_auth_key: str):
        """
        获取谷歌验证码
        :param google_auth_key: 谷歌key
        :return: code
        """
        totp = pyotp.TOTP(google_auth_key)
        return totp.now()

    @staticmethod
    def get_captcha(captcha_url: str):
        """
        获取客户端-captcha [适用于 key = uuid]
        :param captcha_url: 地址
        :return: {}
        """
        uuid_ = str(uuid.uuid1())  # 组装请求
        params = {"codeKey": uuid_}
        sign = AesUtil().encrypt_before_login_get_sign()
        header = HttpRequestUtil.build_headers(captcha_url)
        header.update({"Sign": sign})
        requests.get(captcha_url, params=params, headers=header)

        header.pop('Content-Type')
        redis_code = rds_context.get().get_string(uuid_)  # 获取对应的缓存值
        logging.info(f"获取对应的缓存值-redis_code: {redis_code}")
        return uuid_, re.sub(r'\D', '', str(redis_code))

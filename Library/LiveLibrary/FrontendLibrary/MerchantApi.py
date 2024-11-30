import time
import hashlib
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.LiveLibrary.CommonUtil import CommonFunc
from Library.LiveLibrary.PublicVariables import *
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.YamlUtil import YamlUtil

currency_dic = {"人民币": "CNY", "美元": "USD"}
language_dic = {"中文": "CN", "英文": "EN"}


class MerchantApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def login_client_live(self, venue_user_account, venue_user_id, pwd=player_password):
        """
        正式用户登录
        :return: (name, token)
        """
        timestamp = int(time.time() * 1000)
        # url = f'{client_token_server_dic[self.env].ip}:{client_token_server_dic[self.env].port}' + "/game/api/login"
        host = YamlUtil().load_common_config("merchant", "live")["login_host"]
        if env_context.get() == "uat":
            host += "/gw"
        url = f'{host}/sit/game/api/login'
        sign = YamlUtil().load_common_config('merchant', 'live')["sign"]
        merchant_no = YamlUtil().load_common_config('merchant', 'live')["merchant_no"]
        md5_sign, hash_sign = self._get_sign(sign, merchant_no, timestamp, venue_user_id)
        data = {
            "userName": venue_user_account,
            "password": pwd,
            "language": "zh",
            "merchantNo": merchant_no,
            "timeStamp": timestamp,
            "hashSign": hash_sign,
            "md5Sign": md5_sign,
            "version": "1.0",
            "loginIp": "1.1.1.1",
            "userId": venue_user_id
        }
        rtn = requests.post(url, json=data).json()
        print(rtn)
        # print(data)
        if rtn["message"] not in ["success", "成功"]:
            raise AssertionError(f"登录失败：{rtn['message']}")
        url = rtn["data"]["gameUrl"]
        token = url[url.find("token=") + 6:].split("&")[0]
        return token

    @staticmethod
    def _get_sign(merchant_sign, merchant_no, time_stamp, user_id):
        origin_str = f"{merchant_sign}|{merchant_no}|{user_id}"
        md5_sign = hashlib.md5(origin_str.encode()).hexdigest().upper()
        hash_sign = hashlib.sha256(
            f"{merchant_no}{time_stamp}{merchant_sign}".encode()).hexdigest()
        return md5_sign, hash_sign


if __name__ == "__main__":
    mc = MerchantApi("sit")
    # print(mc.get_merchant_bet_orders("星耀免转普商1", -2, 0))
    # print(mc.transfer('星耀转账普商1', 'SZ237_tWHfbsuwB', 0.15, '转出'))
    # print(mc.get_merchant_balance_change_record('星耀转账普商1'))
    # print(mc.login_direct_formal_player("dXdcU4eMo", "abcd1234"))
    print(mc.login_formal_player("星耀转账普商2", "tOW6ir5ju"))

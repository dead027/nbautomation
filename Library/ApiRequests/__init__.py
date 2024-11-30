#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/8 14:47
import sys
import os
import brotli
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from Library.Common.Utils.Contexts import env_context, header_client_context_1
# from Library.ApiRequests.BackendApi import BackendApi
from Library.Common.ServerConnector.Mysql import MysqlBase
from Library.Common.ServerConnector.Redis import RedisBase
from Library.ApiRequests.ClientApi import ClientApi
# from Library.ApiRequests.SbApi import SbApi
from Library.ApiRequests.SiteBackendApi import SiteBackendApi
from Library.ApiRequests.CommonFunc import CommonFunc


class ApiRequests(SiteBackendApi, ClientApi, CommonFunc):
    def __init__(self, env):
        super().__init__()
        self.env = env
        self.env_setup()

    def env_setup(self):
        env_context.set(self.env)
        MysqlBase()
        RedisBase()


if __name__ == '__main__':
    from Library.Common.Utils.LoginUtil import LoginUtil
    from Library.ApiRequests.SbApi.BusinessOperation import BusinessOperation

    ar = ApiRequests('sit')
    site_code = 'Vd438R'
    LoginUtil().login_site_backend(site_code, 'xingyao3', 'abcd1234')
    # print(ar.decrease_agent_balance_manually_api('xingyao4@gmail.com', '正式', '电子邮箱'))
    # ar.create_user_api("zzzzzzzz2", "abcd1234", check_code=False)
    # ar.lock_register_order_api('1834175833644916737', '锁定')
    # ar.audit_register_order_api('1834175833644916737', if_pass='通过')
    # ar.register_from_client('testuser14')
    # ar.modify_user_status_api('Haiv01', '登录锁定')
    # LoginUtil.login_client('testuser1')
    # print(ar.upload_file_api('poker.png'))
    # print(ar.create_first_deposit_activity_api('Vd438R', "aaaa12", 2, 7, 2, 7, discount_type='百分比'))
    # print(ar.delete_activity('Vd438R', "aaaa12"))
    # print(ar.get_activity_list_api(site_code))
    # print(ar.set_activity_status(site_code, "首次充值", "启用"))

    # 人工充值
    # print(ar.increase_user_balance_manually_api(site_code, 'xyuser1', '会员存款(后台)', 2, 5))
    # ar.lock_user_manual_order_api(site_code, 'R307359507464998912', "已锁", "一审")
    # ar.audit_manual_increase_order_api(site_code, 'R307359507464998912', '通过', '一审')
    # ar.clear_flow_amount_api('xyuser1')
    ar.get_user_report_api(site_code, -1, -1)

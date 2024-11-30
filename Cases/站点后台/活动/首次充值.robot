*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  login_site_backend  ${站点信息_1["站点编号"]}  ${站点信息_1["用户名1"]}  ${通用密码}


*** Test Cases ***
自动参与_自动派发
    [Teardown]  删除活动  首次充值
    # 创建活动
    ${活动名称}  generate_string  10
    创建首存活动  ${活动名称}  3  1000  3  1000
    # 参加活动




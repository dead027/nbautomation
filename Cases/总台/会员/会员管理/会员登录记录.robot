*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
会员登录记录
    ${api_data}  get_user_login_record_api
    log  ${api_data}
    ${sql_data}  get_user_login_record_sql
    log  ${sql_data}
    list_data_should_be_equal  ${api_data}  ${sql_data}  dict_key=会员ID
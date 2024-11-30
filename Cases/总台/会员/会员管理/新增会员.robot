*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
新增会员
    ${api_data}  create_user_api  fy1@163.com
    ${api_data}  audit_register_order_api
    log  ${api_data}
    ${api_data}  get_user_list_api
    ${sql_data}  get_user_list_sql
    log  ${sql_data}
    list_data_should_be_equal  ${api_data}  ${sql_data}  dict_key=''
*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
默认条件查询
    ${api_data}  get_user_list_api
    ${sql_data}  get_user_list_sql
    list_data_should_be_equal  ${api_data}  ${sql_data}  dict_key=MXpwackq

*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
配置标签
    ${api_data}  user_label_config_api  labe001
    log  ${api_data}
    ${api_data}  get_user_label_config_list_api  labe001
    ${sql_data}  get_user_label_config_list_sql  labe001
    log  ${sql_data}
    list_data_should_be_equal  ${api_data}  ${sql_data}

配置标签list
    ${api_data}  user_label_config_list_api
    log  ${api_data}
    ${sql_data}  user_label_config_list_sql
    log  ${sql_data}
    list_data_should_be_equal  ${api_data}  ${sql_data}
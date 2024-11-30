*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}


*** Test Cases ***


默认查询条件

    ${api_data}    get_vip_level_config_list_api    ${}
    ${sql_data}    get_vip_level_config_sql    ${}
    should be equal    ${api_data}    ${sql_data}


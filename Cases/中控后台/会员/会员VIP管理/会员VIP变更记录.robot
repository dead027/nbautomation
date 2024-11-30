*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
默认条件查询
    # 获取VIP变更列表
    ${api_data}    get_user_vip_level_change_aip   ${查询范围}
    ${sql_data}    get_user_vip_level_change_sql   ${查询范围}
    should be equal  ${api_data}  ${sql_data}




*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
默认条件查询

    ${api_data}    get_usser_vip_rank_config_sql   ${查询范围}    # 获取VIP变更列表
    ${sql_data}    get_user_vip_rank_config_aip    ${查询范围}    # 同理
    should be equal  ${api_data}  ${sql_data}    # should be equal 这个是对比的标准格式
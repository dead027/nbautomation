*** Settings ***
Resource  ../基础关键字/Resources.robot

*** Keywords ***
创建会员_后台
    [Documentation]  会员类型: 正式 ｜ 测试
    [Arguments]  ${上级代理}=  ${VIP等级}=  ${主货币}=CNY  ${密码}=${通用密码}  ${会员类型}=正式  ${手机区号}=${手机区号1}
    ...  ${电话}=  ${邮箱}=  ${备注}=
    [Teardown]  登录站点后台
    ${会员账号}  生成会员账号
    # 创建新增会员订单
    create_user_api  ${会员账号}  ${密码}  ${会员类型}  ${主货币}  ${手机区号}  ${电话}  parent_agent=${上级代理}  vip_grade=${VIP等级}
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    登录站点后台  ${站点信息_1["用户名2"]}
    # 锁单
    lock_register_order_api  ${order_id}  锁定
    # 审核
    audit_register_order_api  ${order_id}  备注信息  通过
    RETURN  ${会员账号}

创建会员_客户端
    [Documentation]  注册方式: 手机号码 ｜ 电子邮箱  主货币: 美元 | 中国人民币 | 印度卢比 | 印尼盾 | 巴西雷亚尔 | 泰达币 | 币安币 | 波场币 | 以太坊 | 比特币
    [Arguments]  ${站点编号}=${站点信息_1["站点编号"]}  ${会员账号}=  ${密码}=${通用密码}  ${币种}=CNY  ${代理}=
    ${会员账号}  Run Keyword If  "${会员账号}"  set variable  ${会员账号}  ELSE  生成会员账号
    # 创建新增会员订单
    register_from_client  ${站点信息_1["站点编号"]}  ${会员账号}  ${通用密码}  ${币种}  ${代理}
#    wait_until_user_exists_sql  ${会员账号}
    RETURN  ${会员账号}
    
获取会员VIP权益配置
    [Documentation]  字段名包括: 日提款次数、每日累计提款额度、每周返还奖金比例、每周最低下注金额、每月返还奖金比例、每月最低下注金额、升级奖金、幸运转盘
    [Arguments]  ${会员注册信息}  ${字段名}
    ${会员信息}  get_user_info_sql  ${会员注册信息}
    ${}  get_vip_benefit_config_sql  ${会员信息.vip_rank_code}  日提款次数
    RETURN  ${会员账号}

获取会员信息
    [Arguments]  ${会员账号}  ${站点编号}=${站点信息_1["站点编号"]}
    ${会员信息}  get_user_detail_base_info  ${站点编号}  ${会员账号}
    RETURN  ${会员信息}
    

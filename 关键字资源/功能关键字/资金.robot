*** Settings ***
Resource  ../基础关键字/Resources.robot
Resource  ./登录.robot

*** Keywords ***
会员订单审核通过
    [Arguments]  ${订单编号}
    [Teardown]  login_backend  ${站点管理员_1[0]}  ${通用密码}
    登录站点后台  ${站点信息_1["用户名2"]}
    lock_user_manual_order_api  ${站点编号}  ${订单编号}  已锁  一审
    audit_manual_increase_order_api  ${站点编号}  ${订单编号}  通过

会员订单审核不通过
    [Arguments]  ${订单编号}
    [Teardown]  login_backend  ${站点管理员_1[0]}  ${通用密码}
    登录站点后台  ${站点信息_1["用户名2"]}
    lock_user_manual_order_api  ${站点编号}  ${订单编号}  已锁  一审
    audit_manual_increase_order_api  ${站点编号}  ${订单编号}  不通过
    
会员后台人工加额
    [Arguments]  ${会员账号}  ${调整类型}  ${充值金额}  ${流水倍数}=1  ${活动模版}=  ${备注}=ByTest  ${活动id}=
    [Documentation]
    ...  调整类型: 会员活动 ｜ 会员存款(后台)  ｜ 会员VIP优惠 ｜ 其他调整
    ...  活动模版:  首次充值 | 二次充值 | 免费旋转 ｜ 指定日期存款 ｜ 体育负盈利 ｜ 每日竞赛 ｜ 转盘 ｜ 红包雨
    [Teardown]  登录站点后台
    ${余额_充值前}  get_user_balance_dao  ${站点编号}  ${会员账号}
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  ${调整类型}  ${充值金额}  ${流水倍数}  ${备注}  ${活动模版}  ${活动id}
    会员订单审核通过  ${订单编号}
    ${余额_期望}  evaluate  ${余额_充值前[0]}+${充值金额}
    wait_until_user_balance_change_to_dao  ${站点编号}  ${会员账号}  ${余额_期望}

会员后台人工减额
    [Arguments]  ${会员账号}  ${调整类型}  ${金额}  ${流水倍数}=1  ${活动模版}=  ${备注}=ByTest  ${活动id}=
    [Documentation]
    ...  调整类型: 会员活动 ｜ 会员提款(后台)  ｜ 会员VIP优惠 ｜ 其他调整
    ...  活动模版:  首次充值 | 二次充值 | 免费旋转 ｜ 指定日期存款 ｜ 体育负盈利 ｜ 每日竞赛 ｜ 转盘 ｜ 红包雨
    [Teardown]  登录站点后台
    ${余额_减额前}  get_user_balance_dao  ${站点编号}  ${会员账号}
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  ${调整类型}  ${金额}  ${活动模版}  ${活动id}
    会员订单审核通过  ${订单编号}
    ${余额_期望}  evaluate  ${余额_减额前[0]}-${金额}
    wait_until_user_balance_change_to_dao  ${站点编号}  ${会员账号}  ${余额_期望}

代理订单审核通过
    [Arguments]  ${订单编号}
    [Teardown]  login_backend  ${站点管理员_1[0]}  ${通用密码}
    login_backend  ${站点管理员_1[1]}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  二审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  二审


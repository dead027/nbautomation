*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
佣金_审核通过
    [Tags]  充提
    ${业务类型}  Set Variable  代理佣金
    ${帐变类型}  Set Variable  佣金扣除调整
    ${收支类型}  Set Variable  支出
    ${调整类型}  Set Variable  佣金
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_扣除前}  get_agent_balance  ${总代}  ${钱包类型}
    ${扣除金额}  Set Variable  100
    ${订单信息_操作前_sql}  get_agent_manual_order_list_sql  人工扣除额度  agent_account=${总代}  order_status=审核通过
    ${记录条数_操作前}  Get Length  ${订单信息_操作前_sql}
    decrease_agent_balance_manually_api  佣金  ${扣除金额}  ${总代}  ${钱包类型}
    ${订单信息_操作后_sql}  get_agent_manual_order_list_sql  人工扣除额度  agent_account=${总代}  order_status=审核通过
    ${记录条数_操作后}  Get Length  ${订单信息_操作后_sql}
    ${预期记录条数}  evaluate  ${记录条数_操作前}+1
    Should Be Equal As Integers  ${预期记录条数}  ${记录条数_操作后}
    # 1.校验余额
    ${余额_扣除后}  evaluate  ${余额_扣除前[0]}-${扣除金额}
    wait_until_agent_balance_change_to  ${总代}  ${余额_扣除后}  ${钱包类型}
    # 2.校验人工加额记录
    ${订单信息_操作后_sql}  set variable  ${订单信息_操作后_sql[0]}
    should be equal  ${订单信息_操作后_sql["代理账号"]}  ${总代}
    should be equal  ${订单信息_操作后_sql["调整方式"]}  人工扣除额度
    should be equal  ${订单信息_操作后_sql["订单状态"]}  审核通过
    should be equal  ${订单信息_操作后_sql["调整类型"]}  ${调整类型}
    Should Be Equal As Numbers  ${订单信息_操作后_sql["调整金额"]}  ${扣除金额}
    should be equal  ${订单信息_操作后_sql["操作人"]}  ${中控后台账号1}
    should be equal  ${订单信息_操作后_sql["备注"]}  By script
    ${订单编号}  Set Variable  ${订单信息_操作后_sql["订单号"]}
    # 3.校验人工加额审核记录-详情 todo
    # 4.校验账变
    ${账变记录_sql}  get_agent_coin_change_record_sql  ${订单编号}
    # 只产生一条账变
    ${账变记录长度}  get length  ${账变记录_sql}
    should be equal  ${账变记录长度}  ${1}
    ${账变记录_sql}  set variable  ${账变记录_sql[0]}
    # 比对每一项值
    # 代理
    should be equal  ${账变记录_sql["代理账号"]}  ${总代}
    # 账变业务类型
    should be equal  ${账变记录_sql["业务类型"]}   ${业务类型}
    # 账变类型
    should be equal  ${账变记录_sql["账变类型"]}  ${帐变类型}
    # 收支类型
    should be equal  ${账变记录_sql["收支类型"]}  ${收支类型}
    # 金额改变数量
    should be equal as numbers  ${账变记录_sql["账变金额"]}  ${扣除金额}
    # 账变后
    should be equal  ${账变记录_sql["账变前余额"]}  ${余额_扣除前[2]}
    # 账变后
    should be equal as numbers  ${账变记录_sql["账变后余额"]}  ${余额_扣除后}
    # 备注
    should be equal  ${账变记录_sql["备注"]}  By script


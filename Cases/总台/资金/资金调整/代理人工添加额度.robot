*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
佣金_审核通过
    [Tags]  充提
    ${业务类型}  Set Variable  代理佣金
    ${帐变类型}  Set Variable  佣金增加调整
    ${收支类型}  Set Variable  收入
    ${调整类型}  Set Variable  佣金
    ${钱包类型}  set variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    代理订单审核通过  ${订单编号}
    # 1.校验余额
    ${余额_充值后}  evaluate  ${余额_充值前[0]}+${充值金额}
    wait_until_agent_balance_change_to  ${总代}  ${余额_充值后}  ${钱包类型}
    # 2.校验人工加额记录
    ${人工加额记录_sql}  get_agent_manual_order_list_sql  人工增加额度  ${订单编号}
    ${记录条数}  Get Length  ${人工加额记录_sql}
    Should Be Equal As Integers  ${记录条数}  1
    ${人工加额记录_sql}  set variable  ${人工加额记录_sql[0]}
    should be equal  ${人工加额记录_sql["订单号"]}  ${订单编号}
    should be equal  ${人工加额记录_sql["代理账号"]}  ${总代}
    should be equal  ${人工加额记录_sql["调整方式"]}  人工增加额度
    should be equal  ${人工加额记录_sql["订单状态"]}  审核通过
    should be equal  ${人工加额记录_sql["调整类型"]}  ${调整类型}
    Should Be Equal As Numbers  ${人工加额记录_sql["调整金额"]}  ${充值金额}
    should be equal  ${人工加额记录_sql["申请人"]}  ${中控后台账号1}
    should be equal  ${人工加额记录_sql["备注"]}  By script
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
    # 关联订单号
    should be equal  ${账变记录_sql["关联订单号"]}  ${订单编号}
    # 账变业务类型
    should be equal  ${账变记录_sql["业务类型"]}   ${业务类型}
    # 账变类型
    should be equal  ${账变记录_sql["账变类型"]}  ${帐变类型}
    # 收支类型
    should be equal  ${账变记录_sql["收支类型"]}  ${收支类型}
    # 金额改变数量
    should be equal as numbers  ${账变记录_sql["账变金额"]}  ${充值金额}
    # 账变后
    should be equal  ${账变记录_sql["账变前余额"]}  ${余额_充值前[2]}
    # 账变后
    should be equal as numbers  ${账变记录_sql["账变后余额"]}  ${余额_充值后}
    # 备注
    should be equal  ${账变记录_sql["备注"]}  By script


佣金_存款后台_代理账号为空
    ${充值金额}  Set Variable  10
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${None}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  Invalid argument

佣金_存款后台_代理账号不存在
    ${充值金额}  Set Variable  11
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${充值金额}  dfsfds  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  Invalid argument

佣金_存款后台_钱包类型为空
    ${充值金额}  Set Variable  11
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${None}  check_code=${False}
    should be equal  ${返回信息}  钱包类型不能为空

佣金_存款后台_钱包类型不存在
    ${充值金额}  Set Variable  11
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  dfdsfsd  check_code=${False}
    should be equal  ${返回信息}  Invalid argument

佣金_存款后台_调整类型为空
    ${充值金额}  Set Variable  11
    ${返回信息}  increase_agent_balance_manually_api  ${None}  ${充值金额}  ${总代}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  调整类型不能为空

佣金_存款后台_调整类型不存在
    ${充值金额}  Set Variable  11
    ${返回信息}  increase_agent_balance_manually_api  定时发送多福多寿  ${充值金额}  ${总代}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  Invalid argument

佣金_存款后台_金额为负数
    ${充值金额}  Set Variable  -11
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  The adjustment amount is a positive number, supporting two decimal places

佣金_存款后台_金额为空
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${None}  ${总代}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  调整金额不能为空

佣金_存款后台_金额为0
    ${返回信息}  increase_agent_balance_manually_api  佣金  0  ${总代}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  The adjustment amount is a positive number, supporting two decimal places

佣金_存款后台_金额大于11位
    ${返回信息}  increase_agent_balance_manually_api  佣金  111111111111  ${总代}  佣金钱包  check_code=${False}
    should be equal  ${返回信息}  调整金额最大11位

佣金_存款后台_申请原因为空
    ${充值金额}  Set Variable  11
    ${返回信息}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  佣金钱包  reason=${Empty}  check_code=${False}
    should be equal  ${返回信息}  申请原因不能为空

佣金_存款后台_申请人不能进行一审锁单
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    ${返回信息}  lock_agent_manual_order_api  ${订单编号}  锁定  一审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}

佣金_存款后台_申请人不能进行二审锁单
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
        login_backend  ${中控后台账号1}  ${通用密码}
    ${返回信息}  lock_agent_manual_order_api  ${订单编号}  锁定  二审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}


佣金_存款后台_申请人不能进行一审审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    login_backend  ${中控后台账号1}  ${通用密码}
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}


佣金_存款后台_申请人不能进行二审审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    ${返回信息}  lock_agent_manual_order_api  ${订单编号}  锁定  二审
    login_backend  ${中控后台账号1}  ${通用密码}
    audit_agent_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}

佣金_存款后台_一审锁单人和一审审核人不一致
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}


佣金_存款后台_一审人不能进行二审锁单
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  lock_agent_manual_order_api  ${订单编号}  锁定  二审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}

佣金_存款后台_一审人不能进行二审审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  二审
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}



佣金_存款后台_二审锁单人和二审审核人不一致
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  二审
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}


佣金_存款后台_一审未锁单进行审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}

佣金_存款后台_二审未锁单进行审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}


佣金_存款后台_重复进行一审审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status
    Sleep    5
    # 1.校验余额
    ${余额_充值后}  get_agent_balance  ${总代}  ${钱包类型}
    should be equal   ${余额_充值前}  ${余额_充值后}

佣金_存款后台_重复进行二审审核
    ${钱包类型}  Set Variable  佣金钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  佣金  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  二审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  二审
    ${返回信息}  audit_agent_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status

佣金_存款后台_一审驳回
    ${钱包类型}  Set Variable  佣金钱包
    ${充值金额}  Set Variable  100
    ${调整类型}  set variable  佣金
    ${订单编号}  increase_agent_balance_manually_api  ${调整类型}  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  不通过  一审
    # 2.校验人工加额记录
    ${人工加额记录_sql}  get_agent_manual_order_list_sql  人工增加额度  ${订单编号}
    ${记录条数}  Get Length  ${人工加额记录_sql}
    Should Be Equal As Integers  ${记录条数}  1
    ${人工加额记录_sql}  set variable  ${人工加额记录_sql[0]}
    should be equal  ${人工加额记录_sql["订单号"]}  ${订单编号}
    should be equal  ${人工加额记录_sql["代理账号"]}  ${总代}
    should be equal  ${人工加额记录_sql["调整方式"]}  人工增加额度
    should be equal  ${人工加额记录_sql["订单状态"]}  一审拒绝
    should be equal  ${人工加额记录_sql["调整类型"]}  ${调整类型}
    Should Be Equal As Numbers  ${人工加额记录_sql["调整金额"]}  ${充值金额}
    should be equal  ${人工加额记录_sql["申请人"]}  ${中控后台账号1}
    should be equal  ${人工加额记录_sql["备注"]}  By script

佣金_存款后台_二审驳回
    ${钱包类型}  Set Variable  佣金钱包
    ${充值金额}  Set Variable  100
    ${调整类型}  set variable  佣金
    ${订单编号}  increase_agent_balance_manually_api  ${调整类型}  ${充值金额}  ${总代}  ${钱包类型}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  一审
    audit_agent_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_agent_manual_order_api  ${订单编号}  锁定  二审
    audit_agent_manual_increase_order_api  ${订单编号}  不通过  二审
    # 2.校验人工加额记录
    ${人工加额记录_sql}  get_agent_manual_order_list_sql  人工增加额度  ${订单编号}
    ${记录条数}  Get Length  ${人工加额记录_sql}
    Should Be Equal As Integers  ${记录条数}  1
    ${人工加额记录_sql}  set variable  ${人工加额记录_sql[0]}
    should be equal  ${人工加额记录_sql["订单号"]}  ${订单编号}
    should be equal  ${人工加额记录_sql["代理账号"]}  ${总代}
    should be equal  ${人工加额记录_sql["调整方式"]}  人工增加额度
    should be equal  ${人工加额记录_sql["订单状态"]}  二审拒绝
    should be equal  ${人工加额记录_sql["调整类型"]}  ${调整类型}
    Should Be Equal As Numbers  ${人工加额记录_sql["调整金额"]}  ${充值金额}
    should be equal  ${人工加额记录_sql["申请人"]}  ${中控后台账号1}
    should be equal  ${人工加额记录_sql["备注"]}  By script

额度钱包_审核通过
    [Tags]  充提
    ${业务类型}  Set Variable  代理存款
    ${帐变类型}  Set Variable  代理存款(后台)
    ${收支类型}  Set Variable  收入
    ${调整类型}  Set Variable  代理存款(后台)
    ${钱包类型}  Set Variable  额度钱包
    ${余额_充值前}  get_agent_balance  ${总代}  ${钱包类型}
    ${充值金额}  Set Variable  100
    ${订单编号}  increase_agent_balance_manually_api  代理存款(后台)  ${充值金额}  ${总代}  ${钱包类型}
    代理订单审核通过  ${订单编号}
    # 1.校验余额
    ${余额_充值后}  evaluate  ${余额_充值前[0]}+${充值金额}
    wait_until_agent_balance_change_to  ${总代}  ${余额_充值后}  ${钱包类型}
    # 2.校验人工加额记录
    ${人工加额记录_sql}  get_agent_manual_order_list_sql  人工增加额度  ${订单编号}
    ${记录条数}  Get Length  ${人工加额记录_sql}
    Should Be Equal As Integers  ${记录条数}  1
    ${人工加额记录_sql}  set variable  ${人工加额记录_sql[0]}
    should be equal  ${人工加额记录_sql["订单号"]}  ${订单编号}
    should be equal  ${人工加额记录_sql["代理账号"]}  ${总代}
    should be equal  ${人工加额记录_sql["调整方式"]}  人工增加额度
    should be equal  ${人工加额记录_sql["订单状态"]}  审核通过
    should be equal  ${人工加额记录_sql["调整类型"]}  ${调整类型}
    Should Be Equal As Numbers  ${人工加额记录_sql["调整金额"]}  ${充值金额}
    should be equal  ${人工加额记录_sql["申请人"]}  ${中控后台账号1}
    should be equal  ${人工加额记录_sql["备注"]}  By script
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
    # 关联订单号
    should be equal  ${账变记录_sql["关联订单号"]}  ${订单编号}
    # 账变业务类型
    should be equal  ${账变记录_sql["业务类型"]}   ${业务类型}
    # 账变类型
    should be equal  ${账变记录_sql["账变类型"]}  ${帐变类型}
    # 收支类型
    should be equal  ${账变记录_sql["收支类型"]}  ${收支类型}
    # 金额改变数量
    should be equal as numbers  ${账变记录_sql["账变金额"]}  ${充值金额}
    # 账变后
    should be equal  ${账变记录_sql["账变前余额"]}  ${余额_充值前[2]}
    # 账变后
    should be equal as numbers  ${账变记录_sql["账变后余额"]}  ${余额_充值后}
    # 备注
    should be equal  ${账变记录_sql["备注"]}  By script







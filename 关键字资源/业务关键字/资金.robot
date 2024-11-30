*** Settings ***
Resource  ../功能关键字/Resources.robot

*** Keywords ***
会员人工添加额度
	[Arguments]  ${会员账号}  ${充值金额}  ${流水倍数}  ${调整类型}=会员存款(后台)  ${业务类型}=会员存款  ${帐变类型}=会员存款(后台)  ${调整方式}=人工增加额度
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${会员账号}  set variable  ${会员账号1[0]}
    ${会员信息}  get_user_info_sql  ${会员账号}
    log  ${会员信息}
    # 1.创建存款订单
    ${订单编号}  increase_user_balance_manually_api  ${调整类型}  ${充值金额}  ${流水倍数}  user_register=${会员账号}
    wait_until_manual_order_exists  ${订单编号}
    ${余额_充值前}  get_user_balance  ${会员账号}
    ${打码量_充值前}  get_user_typing_amount_sql  ${会员账号}
    # 2.审核通过
    会员订单审核通过  ${订单编号}
    # 3.校验余额
    ${余额_期望}  evaluate  ${余额_充值前[0]}+${充值金额}
    wait_until_user_balance_change_to  ${会员账号}  ${余额_期望}
    # 4.校验人工加额记录
    ${人工加额记录_sql}  get_user_manual_order_list_sql  人工增加额度  ${订单编号}
    ${记录长度}  Get Length  ${人工加额记录_sql}
    Should Be Equal As Numbers  ${记录长度}  1
    ${人工加额记录_sql}  Set Variable  ${人工加额记录_sql[0]}
    log  ${人工加额记录_sql}
    should be equal  ${人工加额记录_sql["订单号"]}  ${订单编号}
    should be equal  ${人工加额记录_sql["会员ID"]}  ${会员信息.user_account}
    should be equal  ${人工加额记录_sql["会员注册信息"]}  ${会员账号}
    should be equal  ${人工加额记录_sql["VIP等级"]}  VIP${会员信息.vip_rank_code}
    should be equal  ${人工加额记录_sql["调整方式"]}  ${调整方式}
    should be equal  ${人工加额记录_sql["订单状态"]}  审核通过
    should be equal  ${人工加额记录_sql["调整类型"]}  ${调整类型}
    Should Be Equal As Numbers  ${人工加额记录_sql["调整金额"]}  ${充值金额}
    should be equal  ${人工加额记录_sql["申请人"]}  ${中控后台账号1}
    should be equal  ${人工加额记录_sql["备注"]}  By script
    # 5.校验人工加额审核记录-详情 todo
    # 7.校验流水
    ${打码量_预期}  evaluate  ${打码量_充值前}+${充值金额}*${流水倍数}
    wait_until_user_typing_amount_change_to  ${会员账号}  ${打码量_预期}  3
    # 8.校验账变
    ${账变记录_sql}  get_user_coin_change_record_sql  ${站点编号}  ${订单编号}
    # 只产生一条账变
    ${账变记录长度}  get length  ${账变记录_sql}
    should be equal  ${账变记录长度}  ${1}
    ${账变记录_sql}  set variable  ${账变记录_sql[0]}
    # 比对每一项值
    # 代理
    should be equal  ${账变记录_sql["上级代理"]}  ${会员信息.super_agent_account}
    # 关联订单号
    should be equal  ${账变记录_sql["关联订单号"]}  ${订单编号}
    # 账变业务类型
    should be equal  ${账变记录_sql["业务类型"]}   ${业务类型}
    # 账变类型
    should be equal  ${账变记录_sql["账变类型"]}  ${帐变类型}
    # 收支类型
    should be equal  ${账变记录_sql["收支类型"]}  收入
    # 金额改变数量
    should be equal as numbers  ${账变记录_sql["账变金额"]}  ${充值金额}
    # 账变前
    ${余额_期望}  evaluate  ${余额_充值前[2]}+${充值金额}
    should be equal  ${账变记录_sql["账变前余额"]}  ${余额_充值前[2]}
    # 账变后
    should be equal as numbers  ${账变记录_sql["账变后余额"]}  ${余额_期望}
    # 当前金额
    should be equal as numbers  ${账变记录_sql["当前金额"]}  ${充值金额}
    # 备注
    should be equal  ${账变记录_sql["备注"]}  By script
    # 汇率 todo
    # 支付方式

会员人工扣除额度
	[Arguments]  ${会员账号}  ${金额}  ${调整类型}=会员提款(后台)  ${业务类型}=会员取款  ${帐变类型}=会员提款(后台)
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${会员信息}  get_user_info_sql  ${会员账号}
    ${余额_扣除前}  get_user_balance  ${会员账号}
    # 1.创建提款订单
    decrease_user_balance_manually_api  ${会员账号}  ${调整类型}  ${金额}
    ${订单编号}  get_user_manual_decrease_latest_order_sql  ${会员账号}
    wait_until_manual_order_exists  ${订单编号}
    # 3.校验余额
    ${余额_期望}  evaluate  ${余额_扣除前[0]}-${金额}
    wait_until_user_balance_change_to  ${会员账号1}  ${余额_期望}
    # 4.校验人工加额记录
    ${人工扣除记录_sql}  get_user_manual_order_list_sql  人工扣除额度  ${订单编号}
    ${人工扣除记录_api}  get_user_manual_decrease_list_api  ${订单编号}
    log  ${人工扣除记录_sql}
    log  ${人工扣除记录_api}
    list_data_should_be_equal  ${人工扣除记录_sql}  ${人工扣除记录_api}  dict_key=订单号
    # 5.校验人工加额审核记录-详情 todo
    # 8.校验账变
    wait_until_has_coin_change_record_sql  ${站点编号}  ${订单编号}
    ${账变记录_sql}  get_user_coin_change_record_sql  ${站点编号}  ${订单编号}
    # 只产生一条账变
    ${账变记录长度}  get length  ${账变记录_sql}
    should be equal  ${账变记录长度}  ${1}
    ${账变记录_sql}  set variable  ${账变记录_sql[0]}
    # 比对每一项值
    # 代理
    should be equal  ${账变记录_sql["上级代理"]}  ${会员信息.super_agent_account}
    # 关联订单号
    should be equal  ${账变记录_sql["关联订单号"]}  ${订单编号}
    # 账变业务类型
    should be equal  ${账变记录_sql["业务类型"]}  ${业务类型}
    # 账变类型
    should be equal  ${账变记录_sql["账变类型"]}  ${帐变类型}
    # 收支类型
    should be equal  ${账变记录_sql["收支类型"]}  支出
    # 金额改变数量
    should be equal as numbers  ${账变记录_sql["账变金额"]}  ${金额}
    # 账变前
    ${余额_期望}  evaluate  ${余额_扣除前[2]}-${金额}
    should be equal  ${账变记录_sql["账变前余额"]}  ${余额_扣除前[2]}
    # 账变后
    should be equal as numbers  ${账变记录_sql["账变后余额"]}  ${余额_期望}
    # 当前金额
    should be equal as numbers  ${账变记录_sql["当前金额"]}  ${金额}
    # 备注
    should be equal  ${账变记录_sql["备注"]}  by script
    # 汇率 todo
    # 支付方式
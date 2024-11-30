*** Settings ***
Resource  ../../关键字资源/Resources.robot
Suite Setup  Set Suite Variable  ${站点编号}  ${站点信息_1["站点编号"]}

*** Test Cases ***
造数据_客户端创建会员_无代理
    [Tags]  造数据
    ${会员账号}  创建会员_客户端  币种=VND  代理=${一级代理[0]}

造数据_后台创建会员_待审核订单
    [Tags]  造数据  PASS
    登录站点后台
    ${会员账号}  生成会员账号
    # 创建新增会员订单
    create_user_api  ${会员账号}  ${通用密码}  正式

造数据_后台创建会员_驳回
    [Tags]  造数据  PASS
    登录站点后台
    ${会员账号}  生成会员账号
    # 创建新增会员订单
#    create_user_api  ${会员账号}  ${通用密码}  正式  VND
    register_from_client  ${站点信息_1["站点编号"]}  ${会员账号}  ${通用密码}  VND  ${一级代理[0]}
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    # 锁单
    lock_register_order_api  ${order_id}  锁定
    # 审核
    audit_register_order_api  ${order_id}  备注信息  不通过

造数据_后台创建会员_待审核订单
    [Tags]  造数据  PASS
    登录站点后台
    ${会员账号}  生成会员账号
    # 创建新增会员订单
    create_user_api  ${会员账号}  ${通用密码}  正式

造数据_修改账号状态_待审核订单
    [Tags]  造数据  PASS
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    modify_user_status_api  ${用户ID}  ${会员账号} 登录锁定

造数据_会员人工加额_会员存款_后台_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工加额  ${会员账号}  会员存款(后台)  ${充值金额}

造数据_会员人工加额_会员存款(后台)_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  会员存款(后台)  ${充值金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工加额_会员存款(后台)_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  会员存款(后台)  ${充值金额}

造数据_会员人工加额_其他调整_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工加额  ${会员账号}  其他调整  ${充值金额}

造数据_会员人工加额_其他调整_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  其他调整  ${充值金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工加额_其他调整_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  其他调整  ${充值金额}

造数据_会员人工加额_会员VIP优惠_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工加额  ${会员账号}  会员VIP优惠  ${充值金额}

造数据_会员人工加额_会员VIP优惠_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${充值金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工加额_会员VIP优惠_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${充值金额}

造数据_会员人工加额_会员活动_首次充值_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${活动信息}  get_activity_list_dao  ${站点编号}  template=首次充值
    会员后台人工加额  ${会员账号}  会员VIP优惠  ${充值金额}  活动模版=首次充值  活动id=${活动信息[0][0].id}

造数据_会员人工加额_会员活动_首次充值_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${活动信息}  get_activity_list_dao  ${站点编号}  template=首次充值
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${充值金额}  act_template=首次充值  act_id=${活动信息[0][0].id}
    会员订单审核不通过  ${订单编号}

造数据_会员人工加额_会员活动_首次充值_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(20,1000)  random
    ${活动信息}  get_activity_list_dao  ${站点编号}  template=首次充值
    ${订单编号}  increase_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${充值金额}  act_template=首次充值  act_id=${活动信息[0][0].id}

造数据_会员人工减额_会员取款(后台)_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工减额  ${会员账号}  会员提款(后台)  ${取款金额}

造数据_会员人工减额_会员取款(后台)_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员提款(后台)  ${取款金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工减额_会员取款(后台)_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员提款(后台)  ${取款金额}

造数据_会员人工减额_其他调整_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工减额  ${会员账号}  其他调整  ${取款金额}

造数据_会员人工减额_其他调整_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  其他调整  ${取款金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工减额_其他调整_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  其他调整  ${取款金额}

造数据_会员人工减额_会员VIP优惠_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工减额  ${会员账号}  会员VIP优惠  ${取款金额}

造数据_会员人工减额_会员VIP优惠_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${取款金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工减额_会员VIP优惠_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${取款金额}

造数据_会员人工减额_会员活动_首次取款_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    会员后台人工减额  ${会员账号}  会员VIP优惠  ${取款金额}

造数据_会员人工减额_会员活动_首次取款_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${取款金额}
    会员订单审核不通过  ${订单编号}

造数据_会员人工减额_会员活动_首次取款_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${取款金额}  Evaluate  random.randint(20,1000)  random
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${取款金额}

造数据_会员人工减额_会员活动_首次充值_成功
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(1,10)  random
    ${活动信息}  get_activity_list_dao  ${站点编号}  template=首次充值
    会员后台人工减额  ${会员账号}  会员VIP优惠  ${充值金额}  活动模版=首次充值  活动id=${活动信息[0][0].id}

造数据_会员人工减额_会员活动_首次充值_失败
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(1,10)  random
    ${活动信息}  get_activity_list_dao  ${站点编号}  template=首次充值
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${充值金额}  act_template=首次充值  act_id=${活动信息[0][0].id}
    会员订单审核不通过  ${订单编号}

造数据_会员人工减额_会员活动_首次充值_待审核
    [Tags]  造数据
    登录站点后台
    ${会员账号}  set variable  ${会员账号1[0]}
    ${用户信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${充值金额}  Evaluate  random.randint(1,10)  random
    ${活动信息}  get_activity_list_dao  ${站点编号}  template=首次充值
    ${订单编号}  decrease_user_balance_manually_api  ${站点编号}  ${会员账号}  会员VIP优惠  ${充值金额}  act_template=首次充值  act_id=${活动信息[0][0].id}


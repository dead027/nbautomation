*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Test Setup  登录站点后台

*** Test Cases ***
后台创建会员_测试
    [Tags]  造数据
    ${会员账号}  生成会员账号
    # 创建新增会员订单
    create_user_api  ${会员账号}  ${通用密码}  测试
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    # 锁单
    lock_register_order_api  ${order_id}  锁定
    # 审核
    audit_register_order_api  ${order_id}  备注信息  通过
    # 校验
    ${会员信息}  获取会员信息
    Should Be Equal As Strings  ${会员信息["站点编号"]}  ${站点信息_1["站点编号"]}
    Should Be Equal As Strings  ${会员信息["会员账号"]}  ${会员账号}
    Should Be Equal As Strings  ${会员信息["会员状态"]}  正常
    Should Be Equal As Strings  ${会员信息["主货币"]}  RMB
    Should Be Equal As Strings  ${会员信息["账号类型"]}  测试
    Should Be Empty  ${会员信息["上级代理"]}
    Should Be Empty  ${会员信息["上级代理id"]}

后台创建会员_审核_锁单状态_正常逻辑
    [Tags]  PASS
    ${会员账号}  生成会员账号
    # 1.创建新增会员订单
    create_user_api  ${会员账号}  ${通用密码}
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    # 2.审核订单详情校验
    ${审核订单详情}  get_new_user_audit_detail_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${审核订单详情["锁单状态"]}  未锁
    should be equal  ${审核订单详情["锁单人"]}  ${None}
    # 3.锁单,校验审核订单状态
    # 登录第二个后台账号
    login_site_backend  ${站点信息_1["站点编号"]}  ${站点信息_1["用户名2"]}  ${通用密码}
    lock_register_order_api  ${order_id}  锁定
    ${审核订单详情}  get_new_user_audit_detail_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${审核订单详情["锁单状态"]}  已锁
    should be equal  ${审核订单详情["锁单人"]}  ${站点信息_1["用户名2"]}
    # 4.解锁
    lock_register_order_api  ${order_id}  未锁定
    ${审核订单详情}  get_new_user_audit_detail_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${审核订单详情["锁单状态"]}  未锁
    should be equal  ${审核订单详情["锁单人"]}  ${None}

后台创建会员_审核_锁单状态_锁单人同申请人
    [Tags]
    ${会员账号}  生成会员账号
    # 1.创建新增会员订单
    create_user_api  ${会员账号}  ${通用密码}
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    # 3.锁单,校验审核订单状态
    ${返回信息}  lock_register_order_api  ${order_id}  锁定  check_code=${False}
    should contain  ${返回信息}  申请人不能与审核人相同

后台创建会员_审核_锁单状态_多次锁单
    [Tags]  PASS
    ${会员账号}  生成会员账号
    # 1.创建新增会员订单
    create_user_api  ${会员账号}  ${通用密码}
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    # 3.锁单,校验审核订单状态
    login_site_backend  ${站点信息_1["站点编号"]}  ${站点信息_1["用户名2"]}  ${通用密码}
    lock_register_order_api  ${order_id}  锁定
    ${审核订单详情}  get_new_user_audit_detail_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${审核订单详情["锁单状态"]}  已锁
    ${返回信息}  lock_register_order_api  ${order_id}  锁定  check_code=${False}
    should contain  ${返回信息}  Lock order exception

后台创建会员_审核_锁单状态_结单后锁单
    [Tags]  PASS
    ${会员账号}  创建会员_后台
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    login_site_backend  ${站点信息_1["站点编号"]}  ${站点信息_1["用户名2"]}  ${通用密码}
    ${返回信息}  lock_register_order_api  ${order_id}  锁定  check_code=${False}
    should contain  ${返回信息}  Lock order exception

后台创建会员_结果校验_正式_审核通过
    [Tags]  造数据  冒烟
    ${会员账号}  生成会员账号
    # 1.创建新增会员订单
    ${手机区号}  set variable  86
    ${手机号码}  生成随机手机号码  ${手机区号}
    ${邮箱}  生成随机邮箱
    ${主货币}  set variable  美元
    ${主货币符号}  set variable  USD
    ${申请信息}  set variable
    # 创建申请
    create_user_api  ${会员账号}  ${通用密码}  正式  美元  ${手机区号}  ${手机号码}  email=${邮箱}  apply_info=${申请信息}
    # 等待订单生成，并获取订单id
    ${order_id}  wait_has_new_user_audit_order  ${会员账号}
    # 2.审核订单详情校验
    ${审核订单详情}  get_new_user_audit_detail_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${审核订单详情["账号类型"]}  正式
    should be equal  ${审核订单详情["会员账号"]}  ${会员账号}
    Should Be equal  ${审核订单详情["上级代理"]}  ${None}
    should be equal  ${审核订单详情["主货币"]}  ${主货币符号}
    Should Be Equal As Strings  ${审核订单详情["VIP等级"]}  0
    should be equal  ${审核订单详情["邮箱"]}  ${邮箱}
    should be equal  ${审核订单详情["手机号码"]}  ${手机号码}
    should be equal  ${审核订单详情["手机区号"]}  ${手机区号}
    should be equal  ${审核订单详情["申请人"]}  ${站点信息_1["用户名1"]}
    should be equal  ${审核订单详情["申请信息"]}  ${申请信息}
    should be equal  ${审核订单详情["锁单状态"]}  未锁
    should not be equal  ${审核订单详情["申请时间"]}  ${None}
    should be equal  ${审核订单详情["一审人"]}  ${None}
    should be equal  ${审核订单详情["一审时间"]}  ${None}
    should be equal  ${审核订单详情["一审备注"]}  ${None}
    should be equal  ${审核订单详情["锁单人"]}  ${None}
    should be equal  ${审核订单详情["审核状态"]}  待处理
    # 3.锁单
    # 登录第二个后台账号
    login_site_backend  ${站点信息_1["站点编号"]}  ${站点信息_1["用户名2"]}  ${通用密码}
    lock_register_order_api  ${order_id}  锁定
    # 4.审核,审核订单验证
    ${审核备注信息}  set variable  这是备注信息
    audit_register_order_api  ${order_id}  ${审核备注信息}  通过
    ${审核订单详情}  get_new_user_audit_detail_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${审核订单详情["一审人"]}  ${站点信息_1["用户名2"]}
    should not be equal  ${审核订单详情["一审时间"]}  ${None}
    should be equal  ${审核订单详情["一审备注"]}  ${审核备注信息}
    should be equal  ${审核订单详情["审核状态"]}  审核通过
    # 5.会员信息校验
    ${会员信息}  获取会员信息  ${会员账号}
    Should Be Equal As Strings  ${会员信息["站点编号"]}  ${站点信息_1["站点编号"]}
    Should Be Equal As Strings  ${会员信息["会员账号"]}  ${会员账号}
    Should Be Equal As Strings  ${会员信息["账号状态"]}  正常
    Should Be Equal As Strings  ${会员信息["主币种"]}  ${主货币符号}
    Should Be Equal As Strings  ${会员信息["账号类型"]}  正式
    Should Be Equal As Strings  ${会员信息["手机号码"]}  ${手机号码}
    Should Be Equal As Strings  ${会员信息["手机区号"]}  ${手机区号}
    Should Be Equal As Strings  ${会员信息["邮箱"]}  ${邮箱}
    Should Be equal  ${会员信息["上级代理"]}  ${None}
    Should Be equal  ${会员信息["上级代理id"]}  ${None}
    Should Be empty  ${会员信息["会员标签"]}
    Should Be equal  ${会员信息["首存时间"]}  ${None}
    Should Be equal as numbers  ${会员信息["首存金额"]}  0
    Should Be equal  ${会员信息["最后登录时间"]}  ${None}
    Should Be equal  ${会员信息["推荐人"]}  ${None}
    Should not be equal  ${会员信息["注册时间"]}  ${None}
    Should Not Be equal  ${会员信息["注册IP"]}  ${None}
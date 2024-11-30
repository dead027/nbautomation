*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Test Setup  登录站点后台

*** Test Cases ***
修改账号状态_正常改登录锁定
    ${会员账号}  创建会员_后台
    ${用户信息}  get_user_info_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${申请备注信息}  set variable  This is test comment
    ${审核备注信息}  set variable  This is audit test comment
    ${账号状态}  set variable  登录锁定
    # 创建订单
    modify_user_status_api  ${用户ID}  ${会员账号}  ${账号状态}  ${申请备注信息}
    # 等待订单生成
    ${订单ID}  ${订单NO}  wait_until_has_user_change_audit_order  ${站点信息_1["站点编号"]}  ${会员账号}  账号状态
    登录站点后台  ${站点信息_1["用户名2"]}
    # 锁单
    lock_user_modify_order_api  ${订单ID}  锁定
    # 审核
    audit_user_modify_order_api  ${订单ID}  ${审核备注信息}  通过
    # 校验订单属性
    ${订单信息}  get_user_update_audit_detail_vo  ${站点信息_1["站点编号"]}  ${订单ID}
    should be equal  ${订单信息["申请人"]}  ${站点信息_1["用户名1"]}
    should not be equal  ${订单信息["申请时间"]}  ${None}
    should be equal  ${订单信息["审核申请类型"]}  账号状态
    should be equal  ${订单信息["申请原因"]}  ${申请备注信息}
    should be equal  ${订单信息["修改前"]}  正常
    should be equal  ${订单信息["修改后"]}  ${账号状态}
    should be equal  ${订单信息["一审人"]}  ${站点信息_1["用户名2"]}
    should not be equal  ${订单信息["一审时间"]}  ${None}
    should be equal  ${订单信息["一审备注"]}  ${审核备注信息}
    # 登录结果验证
    ${错误信息}  登录客户端  ${会员账号}  需要报错信息=是
    should contain  ${错误信息['message']}  The account has been deactivated

修改账号状态_登录锁定改正常
    ${会员账号}  创建会员_后台
    ${用户信息}  get_user_info_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${申请备注信息}  set variable  This is test comment
    ${审核备注信息}  set variable  This is audit test comment
    ${账号状态}  set variable  登录锁定
    # 预置锁定状态
    modify_user_status_api  ${用户ID}  ${会员账号}  ${账号状态}  ${申请备注信息}
    ${订单ID}  ${订单NO}  wait_until_has_user_change_audit_order  ${站点信息_1["站点编号"]}  ${会员账号}  账号状态
    登录站点后台  ${站点信息_1["用户名2"]}
    lock_user_modify_order_api  ${订单ID}  锁定
    audit_user_modify_order_api  ${订单ID}  ${审核备注信息}  通过
    # 将状态改为正常
    modify_user_status_api  ${用户ID}  ${会员账号}  正常  ${申请备注信息}
    ${订单ID}  ${订单NO}  wait_until_has_user_change_audit_order  ${站点信息_1["站点编号"]}  ${会员账号}  账号状态
    登录站点后台
    lock_user_modify_order_api  ${订单ID}  锁定
    audit_user_modify_order_api  ${订单ID}  ${审核备注信息}  通过
    # 校验订单属性
    ${订单信息}  get_user_update_audit_detail_vo  ${站点信息_1["站点编号"]}  ${订单ID}
    should be equal  ${订单信息["申请人"]}  ${站点信息_1["用户名2"]}
    should not be equal  ${订单信息["申请时间"]}  ${None}
    should be equal  ${订单信息["审核申请类型"]}  账号状态
    should be equal  ${订单信息["申请原因"]}  ${申请备注信息}
    should be equal  ${订单信息["修改前"]}  ${账号状态}
    should be equal  ${订单信息["修改后"]}  正常
    should be equal  ${订单信息["一审人"]}  ${站点信息_1["用户名1"]}
    should not be equal  ${订单信息["一审时间"]}  ${None}
    should be equal  ${订单信息["一审备注"]}  ${审核备注信息}
    # 登录结果验证
    登录客户端  ${会员账号}
    
修改手机号码_审核通过
    ${手机号码_修改前}  生成随机手机号码  长度=6
    ${手机号码_修改后}  生成随机手机号码  长度=6
    ${会员账号}  创建会员_后台  手机区号=${手机区号1}  电话=${手机号码_修改前}
    ${用户信息}  get_user_info_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${申请备注信息}  set variable  这是申请备注信息
    ${审核备注信息}  set variable  This is audit test comment
    modify_user_phone_api  ${用户ID}  ${会员账号}  ${手机区号2}  ${手机号码_修改后}  ${申请备注信息}
    # 等待订单生成
    ${订单ID}  ${订单NO}  wait_until_has_user_change_audit_order  ${站点信息_1["站点编号"]}  ${会员账号}  手机号码
    登录站点后台  ${站点信息_1["用户名2"]}
    # 锁单
    lock_user_modify_order_api  ${订单ID}  锁定
    # 审核
    audit_user_modify_order_api  ${订单ID}  ${审核备注信息}  通过
    # 校验订单属性
    ${订单信息}  get_user_update_audit_detail_vo  ${站点信息_1["站点编号"]}  ${订单ID}
    should be equal  ${订单信息["申请人"]}  ${站点信息_1["用户名1"]}
    should not be equal  ${订单信息["申请时间"]}  ${None}
    should be equal  ${订单信息["审核申请类型"]}  账号状态
    should be equal  ${订单信息["申请原因"]}  ${申请备注信息}
    should be equal  ${订单信息["修改前"]}  ${手机区号1}${手机号码_修改前}
    should be equal  ${订单信息["修改后"]}  ${手机区号2}${手机号码_修改后}
    should be equal  ${订单信息["一审人"]}  ${站点信息_1["用户名2"]}
    should not be equal  ${订单信息["一审时间"]}  ${None}
    should be equal  ${订单信息["一审备注"]}  ${审核备注信息}
    # 结果验证
    ${用户详情}  get_user_detail_base_info_vo  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${用户详情["手机区号"]}  ${手机区号2}
    should be equal  ${用户详情["手机号码"]}  ${手机号码_修改后}

修改邮箱_审核通过
    ${邮箱_修改前}  生成随机邮箱
    ${邮箱_修改后}  生成随机邮箱
    ${会员账号}  创建会员_后台  邮箱=${邮箱_修改前}
    ${用户信息}  get_user_info_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${申请备注信息}  set variable  这是申请备注信息
    ${审核备注信息}  set variable  This is audit test comment
    modify_user_email_api  ${用户ID}  ${会员账号}  ${邮箱_修改前}  ${申请备注信息}
    # 等待订单生成
    ${订单ID}  ${订单NO}  wait_until_has_user_change_audit_order  ${站点信息_1["站点编号"]}  ${会员账号}  邮箱
    登录站点后台  ${站点信息_1["用户名2"]}
    # 锁单
    lock_user_modify_order_api  ${订单ID}  锁定
    # 审核
    audit_user_modify_order_api  ${订单ID}  ${审核备注信息}  通过
    # 校验订单属性
    ${订单信息}  get_user_update_audit_detail_vo  ${站点信息_1["站点编号"]}  ${订单ID}
    should be equal  ${订单信息["申请人"]}  ${站点信息_1["用户名1"]}
    should not be equal  ${订单信息["申请时间"]}  ${None}
    should be equal  ${订单信息["审核申请类型"]}  账号状态
    should be equal  ${订单信息["申请原因"]}  ${申请备注信息}
    should be equal  ${订单信息["修改前"]}  ${邮箱_修改前}
    should be equal  ${订单信息["修改后"]}  ${邮箱_修改后}
    should be equal  ${订单信息["一审人"]}  ${站点信息_1["用户名2"]}
    should not be equal  ${订单信息["一审时间"]}  ${None}
    should be equal  ${订单信息["一审备注"]}  ${审核备注信息}
    # 结果验证
    ${用户详情}  get_user_detail_base_info_vo  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${用户详情["邮箱"]}  ${邮箱_修改后}

修改VIP等级_审核通过
    ${VIP等级_修改前}  set variable  0
    ${VIP等级_修改后}  set variable  20
    ${会员账号}  创建会员_后台
    ${用户信息}  get_user_info_sql  ${站点信息_1["站点编号"]}  ${会员账号}
    ${用户ID}  set variable  ${用户信息[0][0].id}
    ${申请备注信息}  set variable  这是申请备注信息
    ${审核备注信息}  set variable  This is audit test comment
    modify_user_vip_level_api  ${用户ID}  ${会员账号}  ${VIP等级_修改前}  ${申请备注信息}
    # 等待订单生成
    ${订单ID}  ${订单NO}  wait_until_has_user_change_audit_order  ${站点信息_1["站点编号"]}  ${会员账号}  VIP等级
    登录站点后台  ${站点信息_1["用户名2"]}
    # 锁单
    lock_user_modify_order_api  ${订单ID}  锁定
    # 审核
    audit_user_modify_order_api  ${订单ID}  ${审核备注信息}  通过
    # 校验订单属性
    ${订单信息}  get_user_update_audit_detail_vo  ${站点信息_1["站点编号"]}  ${订单ID}
    should be equal  ${订单信息["申请人"]}  ${站点信息_1["用户名1"]}
    should not be equal  ${订单信息["申请时间"]}  ${None}
    should be equal  ${订单信息["审核申请类型"]}  账号状态
    should be equal  ${订单信息["申请原因"]}  ${申请备注信息}
    should be equal  ${订单信息["修改前"]}  ${VIP等级_修改前}
    should be equal  ${订单信息["修改后"]}  ${VIP等级_修改后}
    should be equal  ${订单信息["一审人"]}  ${站点信息_1["用户名2"]}
    should not be equal  ${订单信息["一审时间"]}  ${None}
    should be equal  ${订单信息["一审备注"]}  ${审核备注信息}
    # 结果验证
    ${用户详情}  get_user_detail_base_info_vo  ${站点信息_1["站点编号"]}  ${会员账号}
    should be equal  ${用户详情["VIP等级"]}  ${VIP等级_修改后}
    ${段位预期}  get_vip_rank_of_level_dao  ${站点信息_1["站点编号"]}  ${VIP等级_修改后}
    should be equal  ${用户详情["VIP等级"]}  ${段位预期}


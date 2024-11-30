*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
会员存款后台_审核通过_流水倍数为1
    [Tags]  PASS  充提
    会员人工添加额度  ${会员账号1}  100  1  会员存款(后台)  会员存款  会员存款(后台)

会员存款后台_流水倍数为负数-1
    [Tags]  PASS  充提
    ${返回信息}  increase_user_balance_manually_api  会员存款(后台)  100  -1  user_register=${会员账号1[0]}  check_code=${False}
    should be equal  ${返回信息}  The maximum length of the running multiple is 5 characters, and supports two decimal places.

会员存款后台_审核通过_金额为11位
    [Tags]  PASS  充提
    会员人工添加额度  ${会员账号1}  11111111111  1  会员存款(后台)  会员存款  会员存款(后台)

会员存款后台_审核通过_充值金额大于0
    [Tags]  PASS  充提
    会员人工添加额度  ${会员账号1}  100  1  会员存款(后台)  会员存款  会员存款(后台)

会员存款后台_充值金额小于0
    [Tags]  PASS  充提
    ${返回信息}  increase_user_balance_manually_api  会员存款(后台)  -1  1  user_register=${会员账号1[0]}  check_code=${False}
    should be equal  ${返回信息}  The adjustment amount is a positive number, supporting two decimal places

会员存款后台_用户不存在
    [Tags]  PASS  充提
    ${会员账号}  set variable  adsdsdsa
    ${返回信息}  increase_user_balance_manually_api  会员存款(后台)  2  1  user_register=${会员账号}  check_code=${False}
    should be equal  ${返回信息}  Member information error

会员存款后台_调整类型不存在（废弃）
    [Tags]  False  充提
    ${返回信息}  increase_user_balance_manually_api  不存在的调整类型  2  1  user_register=${会员账号1[0]}  check_code=${False}
    should be equal  ${返回信息}  Member information error

会员存款后台_申请原因为空
    [Tags]  PASS  充提
    ${返回信息}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}  reason=${Empty}  check_code=${False}
    should be equal  ${返回信息}  申请原因不能为空

会员VIP优惠_审核通过_流水倍数为0
    [Tags]  PASS  充提
    会员人工添加额度  ${会员账号1}  100  0  会员VIP优惠  会员VIP优惠  会员VIP优惠增加调整

会员存款后台_申请人不能进行一审锁单
    [Tags]  PASS  充提
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  100  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    ${返回信息}  lock_manual_order_api  ${订单编号}  锁定  一审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate

会员存款后台_一审锁单人和一审审核人不一致
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    ${返回信息}  audit_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Only the locked person can review

会员存款后台_申请人不能进行二审锁单
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    audit_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号1}  ${通用密码}
    ${返回信息}  lock_manual_order_api  ${订单编号}  锁定  二审  check_code=${False}
    should be equal  ${返回信息}  Applicant cannot operate

会员存款后台_一审人不能进行二审审核锁单
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    audit_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  lock_manual_order_api  ${订单编号}  锁定  二审  check_code=${False}
    should be equal  ${返回信息}  The first instance judge cannot operate

会员存款后台_一审人不能进行二审审核
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    audit_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  二审
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  audit_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Only the locked person can review

会员存款后台_一审未锁单，进行审核
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    ${返回信息}  audit_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status

会员存款后台_二审未锁单，进行审核
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    audit_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    ${返回信息}  audit_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status

会员存款后台_重复进行一审审核
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    audit_manual_increase_order_api  ${订单编号}  通过  一审
    ${返回信息}  audit_manual_increase_order_api  ${订单编号}  通过  一审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status

会员存款后台_重复进行二审审核
    [Tags]  PASS  充提
    [Teardown]  login_backend  ${中控后台账号1}  ${通用密码}
    ${订单编号}  increase_user_balance_manually_api  会员存款(后台)  10  1  user_register=${会员账号1[0]}
    wait_until_manual_order_exists  ${订单编号}
    login_backend  ${中控后台账号2}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  一审
    audit_manual_increase_order_api  ${订单编号}  通过  一审
    login_backend  ${中控后台账号3}  ${通用密码}
    lock_manual_order_api  ${订单编号}  锁定  二审
    audit_manual_increase_order_api  ${订单编号}  通过  二审
    ${返回信息}  audit_manual_increase_order_api  ${订单编号}  通过  二审  check_code=${False}
    should be equal  ${返回信息}  Abnormal review status
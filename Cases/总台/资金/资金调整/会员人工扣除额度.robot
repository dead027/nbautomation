*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}

*** Test Cases ***
会员提款后台_成功
    [Tags]  PASS  充提
    会员人工扣除额度  ${会员账号1[0]}  100  会员提款(后台)  会员取款  会员提款(后台)

会员活动_成功
    [Tags]  False  充提
    会员人工扣除额度  ${会员账号1[0]}  100  会员活动  会员活动  活动优惠扣除金额

会员VIP优惠_成功
    [Tags]  False  充提
    会员人工扣除额度  ${会员账号1[0]}  100  会员VIP优惠  会员VIP优惠  会员VIP优惠扣除调整

会员提款后台_打码量不足
    [Tags]  PASS  充提
    ${会员账号}  set variable  ${会员账号2[0]}
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ${会员账号}  会员提款(后台)  10  check_code=${False}
    should be equal  ${msg}  The turnover required for withdrawal is insufficient!!!

会员提款后台_发起申请_测试余额不足
    [Tags]  PASS  充提
    ${会员账号}  set variable  ${会员账号1[0]}
    ${会员信息}  get_user_info_sql  ${会员账号}
    ${余额_扣除前}  get_user_balance  ${会员账号}
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ${会员账号}  会员提款(后台)  99999999999  check_code=${False}
    should be equal  ${msg}  Insufficient wallet balance!!!
    ${余额_扣除后}  get_user_balance  ${会员账号}
    should be equal  ${余额_扣除前}  ${余额_扣除后}

会员提款后台_发起申请_测试调整金额为负数
    [Tags]  PASS  充提
    ${会员账号}  set variable  ${会员账号1}
    ${会员信息}  get_user_info_sql  ${会员账号}
    ${余额_扣除前}  get_user_balance  ${会员账号}
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ${会员账号}  会员提款(后台)  -10  check_code=${False}
    should be equal  ${msg}  The adjustment amount must be greater than 0!!!
    ${余额_扣除后}  get_user_balance  ${会员账号}
    should be equal  ${余额_扣除前}  ${余额_扣除后}

会员提款后台_发起申请_测试调整金额为空
    [Tags]  PASS  充提
    ${会员账号}  set variable  ${会员账号1}
    ${会员信息}  get_user_info_sql  ${会员账号}
    ${余额_扣除前}  get_user_balance  ${会员账号}
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ${会员账号}  会员提款(后台)  ${None}  check_code=${False}
    should be equal  ${msg}  调整金额不能为空
    ${余额_扣除后}  get_user_balance  ${会员账号}
    should be equal  ${余额_扣除前}  ${余额_扣除后}

会员提款后台_发起申请_测试会员不存在
    [Tags]  PASS  充提
    ${会员账号}  set variable
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ds48489984s  会员提款(后台)  10  check_code=${False}
    should be equal  ${msg}  Member information error

会员提款后台_发起申请_测试调整类型为空
    [Tags]  PASS  充提
    ${会员账号}  set variable
    ${余额_扣除前}  get_user_balance  ${会员账号}
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ${会员账号1[0]}  ${None}  10  check_code=${False}
    should be equal  ${msg}  调整类型不能为空
    ${余额_扣除后}  get_user_balance  ${会员账号}
    should be equal  ${余额_扣除前}  ${余额_扣除后}

会员提款后台_发起申请_测试申请原因为空111
    [Tags]  PASS  充提
    ${会员账号}  set variable
    ${余额_扣除前}  get_user_balance  ${会员账号}
    # 1.创建提款订单
    ${msg}  decrease_user_balance_manually_api  ${会员账号1[0]}  会员提款(后台)  10  ${None}  check_code=${False}
    should be equal  ${msg}  申请原因不能为空
    ${余额_扣除后}  get_user_balance  ${会员账号}
    should be equal  ${余额_扣除前}  ${余额_扣除后}

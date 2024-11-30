*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}


*** Test Cases ***
铁粉_累计登录天数比设置的值少一天
    ${勋章名称}  set variable  铁粉
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${设置的登录天数}  evaluate  ${勋章信息.cond_num1}
    ${会员账号}  创建会员并登录_客户端
    FOR  ${天数}  IN RANGE  1  ${设置的登录天数}
        login_client  ${会员账号}
        sleep  0.2
        # 修改登录日期为N天前
        modify_user_login_time  ${会员账号}  -${天数}
    执行定时任务  派发奖章
    ${status}  wait_until_has_medal  ${会员账号}  ${勋章名称}  ${TRUE}
    Should Not Be True  ${status}

铁粉_累计登录天数等于设置的值
    ${勋章名称}  set variable  铁粉
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${设置的登录天数}  evaluate  ${勋章信息.cond_num1}+1
    ${会员账号}  创建会员并登录_客户端
    FOR  ${天数}  IN RANGE  1  ${设置的登录天数}
        login_client  ${会员账号}
        sleep  0.2
        # 修改登录日期为N天前
        modify_user_login_time  ${会员账号}  -${天数}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

铁粉_累计登录天数等于设置的值_但非连续

铁粉_累计登录天数等于设置的值_但有登录失败
    ${勋章名称}  set variable  铁粉
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${设置的登录天数}  evaluate  ${勋章信息.cond_num1}
    ${会员账号}  创建会员并登录_客户端
    FOR  ${天数}  IN RANGE  1  ${设置的登录天数}
        login_client  ${会员账号}
        sleep  0.2
        # 修改登录日期为N天前
        modify_user_login_time  ${会员账号}  -${天数}
    login_client  ${会员账号}  aaabbb123
    sleep  1
    执行定时任务  派发奖章
    ${status}  wait_until_has_medal  ${会员账号}  ${勋章名称}  ${TRUE}
    Should Not Be True  ${status}

孤勇者_单月负盈利最多
    ${勋章名称}  set variable  孤勇者
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    # 本月最大亏损
    ${当前最大亏损}  get_lose_max  0
    ${投注金额}  evaluate  ${当前最大亏损}+20
    会员后台人工充值  ${会员账号}  ${投注金额}
    登录客户端并进入视讯场馆龙虎房间
    开一局并投注_输_龙虎  ${投注金额}
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

功勋卓著_单月流水最多
    ${勋章名称}  set variable  功勋卓著
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    # 本月最大亏损
    ${当前最大流水}  get_valid_amount_max  0
    ${投注金额}  evaluate  ${当前最大流水}+20
    会员后台人工充值  ${会员账号}  ${投注金额}
    登录客户端并进入视讯场馆龙虎房间
    开一局并投注_赢_龙虎  ${投注金额}
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

独上高楼_达到最高等级
    ${勋章名称}  set variable  呼朋唤友
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    ${最高等级}  set variable  int(${勋章信息.cond_num1})
    # 获取升到该等级需要多少场馆打码量
    ${场馆打码量}  get_level_up_required_valid_amount  ${会员账号}  ${场馆编号}  level=${最高等级}
    会员后台人工充值  ${会员账号}  ${场馆打码量}
    登录客户端并进入视讯场馆龙虎房间
    开一局并投注_赢_龙虎  ${场馆打码量}
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}
    # 执行升级定时任务
    FOR  ${loop}  IN RANGE  int(${勋章信息.cond_num1})
        执行定时任务  VIP升级定时任务
        sleep  0.2
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

无敌幸运星_单笔注单盈利等于设置的值
    ${勋章名称}  set variable  无敌幸运星
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    ${投注金额}  evaluate  int(${勋章信息.cond_num1})+20
    会员后台人工充值  ${会员账号}  ${投注金额}
    登录客户端并进入视讯场馆龙虎房间
    开一局并投注_赢_龙虎  ${投注金额}
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

叫我有钱人_平台投注量等于指定值
    ${勋章名称}  set variable  叫我有钱人
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    ${投注金额}  evaluate  int(${勋章信息.cond_num1})+20
    会员后台人工充值  ${会员账号}  ${投注金额}
    登录客户端并进入视讯场馆龙虎房间
    开一局并投注_赢_龙虎  ${投注金额}
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

小有所成_平台投注量等于指定值
    ${勋章名称}  set variable  小有所成
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    ${投注金额}  evaluate  int(${勋章信息.cond_num1})+20
    会员后台人工充值  ${会员账号}  ${投注金额}
    登录客户端并进入视讯场馆龙虎房间
    开一局并投注_赢_龙虎  ${投注金额}
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

老前辈_注册刚好满一年
    ${勋章名称}  set variable  小有所成
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    modify_user_register_time  ${会员账号}  year_diff=-1
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

呼朋唤友_邀请好友人数刚好_且都有充值记录_充值方式为后台人工充值
    ${勋章名称}  set variable  呼朋唤友
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    FOR  ${loop}  IN RANGE  int(${勋章信息.cond_num1})
        ${被邀请都会员账号}  创建会员并登录_客户端
        后台人工充值  ${被邀请都会员账号}  100
    执行定时任务  派发奖章
    wait_until_has_medal  ${会员账号}  ${勋章名称}

呼朋唤友_邀请好友人数刚好_且都有充值记录_充值方式为后台人工充值_只创建了申请未审批完成
    ${勋章名称}  set variable  呼朋唤友
    ${勋章信息}  get_medal_info  ${勋章名称}
    ${会员账号}  创建会员并登录_客户端
    sleep  0.5
    FOR  ${loop}  IN RANGE  int(${勋章信息.cond_num1})
        ${被邀请的会员账号}  创建会员并登录_客户端
        deposit_by_backend_manual_sql  ${被邀请的会员账号}  100
    执行定时任务  派发奖章
    ${status}  wait_until_has_medal  ${会员账号}  ${勋章名称}  ${TRUE}
    Should Not Be True  ${status}

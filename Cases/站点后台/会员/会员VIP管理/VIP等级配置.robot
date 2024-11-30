`*** Settings ***
Resource  ../../../../关键字资源/Resources.robot
Suite Setup  登录站点后台


*** Test Cases ***
VIP_升级_1级升2级
    ${会员账号}  创建会员_客户端  币种=人民币
#    ${会员账号}  set variable  xyuser3
    会员后台人工加额  ${会员账号}  会员存款(后台)  10000
    登录客户端并进入视讯场馆龙虎房间  ${会员账号}
    # 获取vip最大等级
    ${vip最大等级}  get_max_vip_grade  ${站点编号}
    ${升级需要的打码量}  get_level_up_required_valid_amount  ${会员账号}  ${站点编号}  increase_level=1
    # 剩余打码量还需要考虑低于最低投注限红的情况，目前人为控制不会低于限红，否则还需要去查询视讯对应房间的限红
    ${game_no}  ${boot_no}  ${order_no}  开一局并投注_赢_龙虎  ${升级需要的打码量}
    # 等待拉单完成
#    wait_until_order_exist  ${order_no}  30
    ${VIP等级}  set variable  1
    # 等待vip等级变化
    ${VIP下一级}  evaluate  ${VIP等级}+1
    wait_until_user_vip_level_changed_sql  ${会员账号}  ${站点编号}  ${VIP下一级}
    # 校验user_info
    ${会员信息}  get_user_info_sql  ${站点编号}  ${会员账号}
    ${会员信息}  set variable  ${会员信息[0][0]}
    ${下一级}  evaluate  ${VIP等级}+1
    ${下下级}  evaluate  ${VIP等级}+2
    ${vip_grade_code}  set variable  ${下一级}
    ${vip_grade_up}  Set Variable If  ${下一级}==${vip最大等级}  ${下一级}  ${下下级}
    Should Be Equal As Numbers  ${会员信息.vip_grade_code}  ${vip_grade_code}
    Should Be Equal As Numbers  ${会员信息.vip_grade_up}  ${vip_grade_up}
    # 校验vip等级变更记录
    ${change_info}  get_latest_vip_change_info_sql  ${会员账号[0]}  ${会员账号[1]}  ${下一级}
    Should Be Equal As Numbers  ${change_info.change_before}  ${VIP等级}  ${下一级}

VIP_升级_VIP0升到最高等级_边界值_满足最低升级金额
    # 创建新会员，并充值
    #${会员账号}  set variable  8618008093465
    ${会员账号}  创建会员并登录_客户端  手机号码
    sleep  0.50
    后台人工充值  ${会员账号}  2000
    sleep  0.5
    登录客户端并进入视讯场馆龙虎房间  ${会员账号}  手机号码
    # 获取vip最大等级
    ${vip最大等级}  get_max_vip_rank
    FOR  ${VIP等级}  IN RANGE  ${vip最大等级}
        ${升级需要的打码量}  get_user_upgrade_require  ${会员账号}
        # 剩余打码量还需要考虑低于最低投注限红的情况，目前人为控制不会低于限红，否则还需要去查询视讯对应房间的限红
        ${game_no}  ${boot_no}  ${order_no}  开一局并投注_赢_龙虎  ${升级需要的打码量}
        # 拉单
        执行定时任务  神话视讯平台拉取订单
        # 等待拉单完成
        wait_until_order_exist  ${order_no}
        # 修改user_vip_flow_record的update为美东昨天
        modify_flow_record  ${会员账号}  vip_rank_code=${VIP等级}  update_time_diff=-1
        # 修改 vip_change_info ，change_time为美东昨天
        run keyword if  ${VIP等级}!=0  modify_change_info  ${会员账号}  ${VIP等级}  -1
        执行定时任务  VIP升级定时任务
        # 等待vip等级变化
        ${VIP下一级}  evaluate  ${VIP等级}+1
        wait_until_user_vip_rank_changed_sql  ${会员账号}  ${VIP下一级}
        # 校验user_info
        ${会员信息}  get_user_info_sql  ${会员账号}
        ${下一级}  evaluate  ${VIP等级}+1
        ${下下级}  evaluate  ${VIP等级}+2
        ${vip_rank_code}  set variable  ${下一级}
        ${vip_rank_up}  Set Variable If  ${下一级}==${vip最大等级}  ${下一级}  ${下下级}
        Should Be Equal As Numbers  ${会员信息.vip_rank_code}  ${vip_rank_code}
        Should Be Equal As Numbers  ${会员信息.vip_rank_up}  ${vip_rank_up}
        # 校验vip_change_info
        ${change_info}  get_latest_vip_change_info_sql  ${会员账号}  ${下一级}
        Should Be Equal As Numbers  ${change_info.change_before}  ${VIP等级}  ${下一级}
    END

VIP_升级_VIP0升到1级_边界值_差一块钱
    ${VIP当前等级}  set variable  0
    ${会员账号}  创建会员并登录_客户端  手机号码
    sleep  0.50
    后台人工充值  ${会员账号}  10000
#    sleep  0.5
    登录客户端并进入视讯场馆龙虎房间  ${会员账号}  手机号码
    ${升级需要的打码量}  get_user_upgrade_require  ${会员账号}
    # 剩余打码量还需要考虑低于最低投注限红的情况，目前人为控制不会低于限红，否则还需要去查询视讯对应房间的限红
    ${投注金额}  evaluate   ${升级需要的打码量}-1
    ${game_no}  ${boot_no}  ${order_no}  开一局并投注_赢_龙虎  ${投注金额}
    # 拉单
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    # 修改user_vip_flow_record的update为美东昨天
    modify_flow_record  ${会员账号}  vip_rank_code=${VIP当前等级}  update_time_diff=-1
    # 修改 vip_change_info ，change_time为美东昨天
    run keyword if  ${VIP当前等级}!=0  modify_change_info  ${会员账号}  ${VIP当前等级}  -1
    执行定时任务  VIP升级定时任务
    # 等待vip等级变化
    ${VIP下一级}  evaluate  ${VIP当前等级}+1
    sleep  5
    # 校验user_info
    ${会员信息}  get_user_info_sql  ${会员账号}
    Should Be Equal As Numbers  ${会员信息.vip_rank_code}  ${VIP当前等级}
    Should Be Equal As Numbers  ${会员信息.vip_rank_up}  ${VIP下一级}
    # 校验vip_change_info
    ${change_info}  get_latest_vip_change_info_sql  ${会员账号}  ${VIP下一级}
    Should Be equal  ${None}  ${change_info}

VIP_升级_VIP1升到2级_边界值_差一块钱
    ${VIP当前等级}  set variable  1
    ${会员账号}  创建会员并登录_客户端  手机号码
    sleep  0.50
    后台人工充值  ${会员账号}  10000
#    sleep  0.5
    登录客户端并进入视讯场馆龙虎房间  ${会员账号}  手机号码
    ${vip最大等级}  get_max_vip_rank
    FOR  ${VIP等级}  IN RANGE  ${1}
        ${升级需要的打码量}  get_user_upgrade_require  ${会员账号}
        # 剩余打码量还需要考虑低于最低投注限红的情况，目前人为控制不会低于限红，否则还需要去查询视讯对应房间的限红
        ${game_no}  ${boot_no}  ${order_no}  开一局并投注_赢_龙虎  ${升级需要的打码量}
        # 拉单
        执行定时任务  神话视讯平台拉取订单
        # 等待拉单完成
        wait_until_order_exist  ${order_no}
        # 修改user_vip_flow_record的update为美东昨天
        modify_flow_record  ${会员账号}  vip_rank_code=${VIP等级}  update_time_diff=-1
        # 修改 vip_change_info ，change_time为美东昨天
        run keyword if  ${VIP等级}!=0  modify_change_info  ${会员账号}  ${VIP等级}  -1
        执行定时任务  VIP升级定时任务
        # 等待vip等级变化
        ${VIP下一级}  evaluate  ${VIP等级}+1
        wait_until_user_vip_rank_changed_sql  ${会员账号}  ${VIP下一级}
        # 校验user_info
        ${会员信息}  get_user_info_sql  ${会员账号}
        ${下一级}  evaluate  ${VIP等级}+1
        ${下下级}  evaluate  ${VIP等级}+2
        ${vip_rank_code}  set variable  ${下一级}
        ${vip_rank_up}  Set Variable If  ${下一级}==${vip最大等级}  ${下一级}  ${下下级}
        Should Be Equal As Numbers  ${会员信息.vip_rank_code}  ${vip_rank_code}
        Should Be Equal As Numbers  ${会员信息.vip_rank_up}  ${vip_rank_up}
        # 校验vip_change_info
        ${change_info}  get_latest_vip_change_info_sql  ${会员账号}  ${下一级}
        Should Be Equal As Numbers  ${change_info.change_before}  ${VIP等级}  ${下一级}
    END
    ${升级需要的打码量}  get_user_upgrade_require  ${会员账号}
    # 剩余打码量还需要考虑低于最低投注限红的情况，目前人为控制不会低于限红，否则还需要去查询视讯对应房间的限红
    ${投注金额}  evaluate   ${升级需要的打码量}-1
    ${game_no}  ${boot_no}  ${order_no}  开一局并投注_赢_龙虎  ${投注金额}
    # 拉单
    执行定时任务  神话视讯平台拉取订单
    # 等待拉单完成
    wait_until_order_exist  ${order_no}
    # 修改user_vip_flow_record的update为美东昨天
    modify_flow_record  ${会员账号}  vip_rank_code=${VIP当前等级}  update_time_diff=-1
    # 修改 vip_change_info ，change_time为美东昨天
    run keyword if  ${VIP当前等级}!=0  modify_change_info  ${会员账号}  ${VIP当前等级}
    执行定时任务  VIP升级定时任务
    # 等待vip等级变化
    ${VIP下一级}  evaluate  ${VIP当前等级}+1
    sleep  5
    # 校验user_info
    ${会员信息}  get_user_info_sql  ${会员账号}
    log  ${会员信息}
    Should Be Equal As Numbers  ${会员信息.vip_rank_code}  ${VIP当前等级}
    Should Be Equal As Numbers  ${会员信息.vip_rank_up}  ${VIP下一级}
    # 校验vip_change_info
    ${change_info}  get_latest_vip_change_info_sql  ${会员账号}  ${VIP下一级}
    Should Be equal  ${None}  ${change_info}

VIP_升级_VIP0升到最高等级_边界值+1_满足最低升级金额
    # 创建新会员，并充值
    #${会员账号}  set variable  8618008093465
    ${会员账号}  创建会员并登录_客户端  手机号码
    sleep  0.50
    后台人工充值  ${会员账号}  2000
    sleep  0.5
    登录客户端并进入视讯场馆龙虎房间  ${会员账号}  手机号码
    # 获取vip最大等级
    ${vip最大等级}  get_max_vip_rank
    FOR  ${VIP等级}  IN RANGE  ${vip最大等级}
        ${升级需要的打码量}  get_user_upgrade_require  ${会员账号}
        # 剩余打码量还需要考虑低于最低投注限红的情况，目前人为控制不会低于限红，否则还需要去查询视讯对应房间的限红
        ${投注金额}  evaluate   ${升级需要的打码量}+1
        ${game_no}  ${boot_no}  ${order_no}  开一局并投注_赢_龙虎  ${投注金额}
        # 拉单
        执行定时任务  神话视讯平台拉取订单
        # 等待拉单完成
        wait_until_order_exist  ${order_no}
        # 修改user_vip_flow_record的update为美东昨天
        modify_flow_record  ${会员账号}  vip_rank_code=${VIP等级}  update_time_diff=-1
        # 修改 vip_change_info ，change_time为美东昨天
        run keyword if  ${VIP等级}!=0  modify_change_info  ${会员账号}  ${VIP等级}  -1
        执行定时任务  VIP升级定时任务
        # 等待vip等级变化
        ${VIP下一级}  evaluate  ${VIP等级}+1
        sleep  0.50
        wait_until_user_vip_rank_changed_sql  ${会员账号}  ${VIP下一级}
        # 校验user_info
        ${会员信息}  get_user_info_sql  ${会员账号}
        ${下一级}  evaluate  ${VIP等级}+1
        ${下下级}  evaluate  ${VIP等级}+2
        ${vip_rank_code}  set variable  ${下一级}
        ${vip_rank_up}  Set Variable If  ${下一级}==${vip最大等级}  ${下一级}  ${下下级}
        Should Be Equal As Numbers  ${会员信息.vip_rank_code}  ${vip_rank_code}
        Should Be Equal As Numbers  ${会员信息.vip_rank_up}  ${vip_rank_up}
        # 校验vip_change_info
        ${change_info}  get_latest_vip_change_info_sql  ${会员账号}  ${下一级}
        Should Be Equal As Numbers  ${change_info.change_before}  ${VIP等级}  ${下一级}
    END






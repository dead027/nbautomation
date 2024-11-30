*** Settings ***
Resource  荷官端基础指令.robot
Library    String

*** Keywords ***
开牌_龙虎
	[Arguments]  ${dragon_card}  ${tiger_card}  ${game_no}  ${boot_no}
	发牌_龙虎  ${game_no}  ${boot_no}  ${dragon_card}  ${tiger_card}
	发牌完毕_龙虎  ${game_no}  ${boot_no}  ${dragon_card}  ${tiger_card}
	sleep  1
	本局结束_龙虎  ${game_no}  ${boot_no}  ${dragon_card}  ${tiger_card}

开一局_龙虎
	[Arguments]  ${dragon_card}  ${tiger_card}
	${game_no}  ${boot_no}  开新局_龙虎
	开牌_龙虎  ${dragon_card}  ${tiger_card}  ${game_no}  ${boot_no}
	RETURN  ${game_no}  ${boot_no}

开一局并投注_龙虎
	[Arguments]  ${dragon_card}  ${tiger_card}  ${投注内容}  ${bet_wait_time}=0.2  ${if_settlement}=${TRUE}
	${game_no}  ${boot_no}  开新局_龙虎
	wait_until_game_status_changed  ${默认场馆及游戏["龙虎房间"]}  ${game_no}
	do bet  ${视讯系统会员ID}  ${默认场馆及游戏["龙虎房间"]} ${投注内容}  ${game_no}  ${boot_no}
	sleep  ${bet_wait_time}
	run keyword if  ${if_settlement}==${TRUE}  开牌_龙虎  ${dragon_card}  ${tiger_card}  ${game_no}  ${boot_no}
	RETURN  ${game_no}  ${boot_no}
	
开一局并投注_赢_龙虎
	[Arguments]  ${投注金额}  ${投注时间}=2  ${if_settlement}=${TRUE}
	${game_no}  ${boot_no}  开新局_龙虎  ${投注时间}
	wait_until_game_status_changed  ${默认场馆及游戏["龙虎房间"]}  ${game_no}
	sleep  0.2
	do bet  ${视讯系统会员ID}  ${默认场馆及游戏["龙虎房间"]}  龙-${投注金额}  ${game_no}  ${boot_no}
	${等待时间}  evaluate  ${投注时间}-1
	sleep  ${等待时间}
	run keyword if  ${if_settlement}==${TRUE}  开牌_龙虎  18  42  ${game_no}  ${boot_no}
	${rtn}  get_order_info_by_game_no  ${game_no}  ${视讯系统会员ID}
	${order_no}  set variable  ${rtn.order_id}
#	sleep  5
	FOR  ${i}  IN  ${30}
	    执行定时任务  神话视讯平台拉取订单  30
	    ${是否存在}  check_if_order_exist  ${order_no}
	    Exit For Loop If  ${是否存在}!=${False}
	    sleep  1
	END
	RETURN  ${game_no}  ${boot_no}  ${order_no}

开一局并投注_输_龙虎
	[Arguments]  ${投注金额}  ${bet_wait_time}=0.2  ${if_settlement}=${TRUE}
	${game_no}  ${boot_no}  开新局_龙虎
	wait_until_game_status_changed  ${默认场馆及游戏["龙虎房间"]}  ${game_no}
	do bet  ${视讯系统会员ID}  ${默认场馆及游戏["龙虎房间"]}  虎-${投注金额}  ${game_no}  ${boot_no}
	sleep  ${bet_wait_time}
	run keyword if  ${if_settlement}==${TRUE}  开牌_龙虎  19  42  ${game_no}  ${boot_no}
	${rtn}  get_order_info_by_game_no  ${game_no}  ${视讯系统会员ID}
	${order_no}  set variable  ${rtn.order_id}
	执行定时任务  神话视讯平台拉取订单
	RETURN  ${game_no}  ${boot_no}  ${order_no}

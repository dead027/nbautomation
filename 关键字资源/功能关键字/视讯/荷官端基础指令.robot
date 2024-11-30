*** Settings ***
Resource  ../../基础关键字/Resources.robot

*** Keywords ***
开新局_龙虎
	[Arguments]  ${投注时间}
	${rtn}  send_game_start_dt  ${默认场馆及游戏["龙虎房间"]}  ${投注时间}
	RETURN  ${rtn["game_no"]}  ${rtn["boot_no"]}

开新靴
	[Arguments]  ${desk_no}  ${游戏类型}
	send change boot  ${desk_no}  ${游戏类型}

发牌_龙虎
	[Arguments]  ${game_no}  ${boot_no}  ${dragon_card}  ${tiger_card}=
	send card identify dt  ${game_no}  ${默认场馆及游戏["龙虎房间"]}  ${boot_no}  ${dragon_card}  ${tiger_card}

发牌完毕_龙虎
	[Arguments]  ${game_no}  ${boot_no}  ${dragon_card}  ${tiger_card}
	send card identify dt  ${game_no}  ${默认场馆及游戏["龙虎房间"]}  ${boot_no}  ${dragon_card}  ${tiger_card}  is_finish=${TRUE}

本局结束_龙虎
	[Arguments]  ${game_no}  ${boot_no}  ${dragon_card}  ${tiger_card}
	send game end dt  ${game_no}  ${默认场馆及游戏["龙虎房间"]}  ${boot_no}  ${dragon_card}  ${tiger_card}

所有桌台换靴
	send change boot  ${默认场馆及游戏["龙虎房间"]}  龙虎
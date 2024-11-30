*** Settings ***
Resource  ../功能关键字/Resources.robot

*** Keywords ***
校验游戏报表详情_按场馆
	[Arguments]  ${场馆类型}  ${开始时间}  ${结束时间}  ${币种}=  ${时间单位}=日  ${是否转换为平台币}=${FALSE}
	${场馆列表}  get_venue_list_of_venue_type  ${场馆类型}
	FOR  ${场馆}  IN  @{场馆列表}
        ${预期数据}  get_game_report_by_venue_vo  ${站点编号}  ${场馆}  ${开始时间}  ${结束时间}  ${币种}  0  ${时间单位}  ${是否转换为平台币}
        ${接口数据}
        dict_data_should_be_equal  ${预期数据}  ${接口数据}
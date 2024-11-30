*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  登录站点后台


*** Test Cases ***
外层数据校验_主货币_今日
    ${日期}  set variable  -1
    ${预期结果}  get_game_report_vo  ${站点编号}  start_diff=${日期}  end_diff=${日期}
    ${实际结果}  get_game_report_api  ${站点编号}  start_diff=${日期}  end_diff=${日期}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=游戏类型  dict_key_2=币种  ignore_sort=${TRUE}
    
外层数据校验_平台币_今日
    ${预期结果}  get_game_report_vo  ${站点编号}  start_diff=0  end_diff=0  to_site_coin=${TRUE}
    ${实际结果}  get_game_report_api  ${站点编号}  start_diff=0  end_diff=0  to_site_coin=${TRUE}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  0.02  dict_key_1=游戏类型  dict_key_2=币种  ignore_sort=${TRUE}

外层数据校验_主货币_指定游戏类型
    ${场馆列表}  get_venue_type_name_list
    FOR  ${场馆类型}  IN  @{场馆列表}
        ${预期结果}  get_game_report_vo  ${站点编号}  start_diff=0  end_diff=0  venue_type=${场馆类型}
        ${实际结果}  get_game_report_api  ${站点编号}  start_diff=0  end_diff=0  venue_type=${场馆类型}
        list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=游戏类型  dict_key_2=币种  ignore_sort=${TRUE}
    END

外层数据校验_平台币_指定游戏类型
    ${场馆列表}  get_venue_type_name_list
    FOR  ${场馆类型}  IN  @{场馆列表}
        ${预期结果}  get_game_report_vo  ${站点编号}  start_diff=0  end_diff=0  to_site_coin=${TRUE}  venue_type=${场馆类型}
        ${实际结果}  get_game_report_api  ${站点编号}  start_diff=0  end_diff=0  to_site_coin=${TRUE}  venue_type=${场馆类型}
        list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=游戏类型  dict_key_2=币种  ignore_sort=${TRUE}
    END

#外层数据校验_主货币_指定游戏类型_指定币种
    

明细数据校验_按场馆类型_主货币_昨日
    ${场馆列表}  get_venue_type_name_list
    FOR  ${场馆类型}  IN  @{场馆列表}
        ${预期结果}  get_game_report_vo  ${站点编号}  start_diff=0  end_diff=0  venue_type=${场馆类型}
        ${实际结果}  get_game_report_api  ${站点编号}  start_diff=0  end_diff=0  venue_type=${场馆类型}
        list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=游戏类型  dict_key_2=币种  ignore_sort=${TRUE}
    END

明细数据校验_按场馆类型_平台币_昨日
    FOR  ${场馆类型}  IN  @{场馆类型列表}
        ${预期数据}  get_game_report_by_venue_type_vo  ${站点编号}  ${场馆类型}  start_diff=-1  end_diff=-1  to_site_coin=${TRUE}
#        ${接口数据}
#        dict_data_should_be_equal  ${预期数据}  ${接口数据}

明细数据校验_按游戏_主货币_昨日
    FOR  ${场馆类型}  IN  @{场馆类型列表}
        校验游戏报表详情_按场馆  ${场馆类型}  start_diff=-1  end_diff=-1

明细数据校验_按游戏_平台币_昨日
    FOR  ${场馆类型}  IN  @{场馆类型列表}
        校验游戏报表详情_按场馆  ${场馆类型}  start_diff=-1  end_diff=-1  是否转换为平台币=${TRUE}


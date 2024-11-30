*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  登录站点后台

*** Test Cases ***
昨日_默认查询
    ${起始日期}  set variable  -1
    ${结束日期}  set variable  -1
    ${预期结果}  get_user_win_lose_report_vo  ${站点编号}  ${起始日期}  ${结束日期}
    ${预期汇总数据}  get_user_win_lose_report_total_vo  ${站点编号}  ${起始日期}  ${结束日期}
    ${实际结果}  ${汇总数据}  get_user_win_lose_report_api  ${站点编号}  ${起始日期}  ${结束日期}
    log  ${预期汇总数据}
    log  ${汇总数据}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=会员账号  dict_key_2=上级代理  ignore_sort=${TRUE}
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}

昨日_默认查询_转换为平台币
    ${起始日期}  set variable  -1
    ${结束日期}  set variable  -1
    ${预期结果}  get_user_win_lose_report_vo  ${站点编号}  ${起始日期}  ${结束日期}  to_site_coin=${TRUE}
    ${预期汇总数据}  get_user_win_lose_report_total_vo  ${站点编号}  ${起始日期}  ${结束日期}  to_site_coin=${TRUE}
    ${实际结果}  ${汇总数据}  get_user_win_lose_report_api  ${站点编号}  ${起始日期}  ${结束日期}  to_site_coin=${TRUE}
    log  ${预期结果}
    log  ${实际结果}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=会员账号  dict_key_2=上级代理  ignore_sort=${TRUE}  ignore_value=0.011
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}  ignore=0.1

今日_默认查询
    ${起始日期}  set variable  0
    ${结束日期}  set variable  0
    ${预期结果}  get_user_win_lose_report_vo  ${站点编号}  ${起始日期}  ${结束日期}
    ${预期汇总数据}  get_user_win_lose_report_total_vo  ${站点编号}  ${起始日期}  ${结束日期}
    ${实际结果}  ${汇总数据}  get_user_win_lose_report_api  ${站点编号}  ${起始日期}  ${结束日期}
    Log  ${预期结果}
    log  ${实际结果}
    log  ${预期汇总数据}
    log  ${汇总数据}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=会员账号  dict_key_2=上级代理  ignore_sort=${TRUE}
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}
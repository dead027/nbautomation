*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  登录站点后台

*** Test Cases ***
今日_默认查询_列表
    [Tags]  PASS
    ${日期}  set variable  -1
    ${预期结果}  get_venue_report_vo  ${站点编号}  ${日期}  ${日期}
    ${预期汇总数据}  get_venue_report_total_vo  ${站点编号}  ${日期}  ${日期}
    ${实际结果}  ${汇总数据}  get_venue_report_api  ${站点编号}  ${日期}  ${日期}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=场馆  dict_key_2=主币种  ignore_sort=${TRUE}
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}
*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  登录站点后台

*** Test Cases ***
今日_默认查询_列表
    [Tags]  PASS
    ${开始日期}  set variable  -1
    ${结束日期}  set variable  -1
    ${预期结果}  get_daily_report_vo  ${站点编号}  ${开始日期}  ${结束日期}
    ${预期汇总数据}  get_daily_report_total_vo  ${站点编号}  ${开始日期}  ${结束日期}
    ${实际结果}  ${汇总数据}  get_daily_report_api  ${站点编号}  ${开始日期}  ${结束日期}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=日期  dict_key_2=主币种  ignore_sort=${TRUE}
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}
    
今日_指定币种_列表
    [Tags]  PASS
    ${开始日期}  set variable  0
    ${结束日期}  set variable  0
    FOR  ${币种}  IN  VND  USDT  MYR  CNY  PHP
        ${预期结果}  get_daily_report_vo  ${站点编号}  ${开始日期}  ${结束日期}  currency=${币种}
        log  ${预期结果}
        ${预期汇总数据}  get_daily_report_total_vo  ${站点编号}  ${开始日期}  ${结束日期}  currency=${币种}
        ${实际结果}  ${汇总数据}  get_daily_report_api  ${站点编号}  ${开始日期}  ${结束日期}  currency=${币种}
        log  ${实际结果}
        list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=日期  dict_key_2=主币种  ignore_sort=${TRUE}
        dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}
    END

今日_默认查询_列表_转为平台币
    [Tags]  PASS
    ${开始日期}  set variable  0
    ${结束日期}  set variable  0
    ${预期结果}  get_daily_report_vo  ${站点编号}  ${开始日期}  ${结束日期}  to_site_coin=${TRUE}
    ${预期汇总数据}  get_daily_report_total_vo  ${站点编号}  ${开始日期}  ${结束日期}  to_site_coin=${TRUE}
    ${实际结果}  ${汇总数据}  get_daily_report_api  ${站点编号}  ${开始日期}  ${结束日期}  to_site_coin=${TRUE}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=日期  dict_key_2=主币种  ignore_sort=${TRUE}
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}
    
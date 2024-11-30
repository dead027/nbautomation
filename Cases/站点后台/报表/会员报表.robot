*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  登录站点后台

*** Test Cases ***
昨日_默认查询
    ${起始日期}  set variable  -2
    ${结束日期}  set variable  -2
    ${预期结果}  get_user_report_vo  ${站点编号}  ${起始日期}  ${结束日期}
    log  ${预期结果}
    ${预期汇总数据}  get_user_report_total_vo  ${站点编号}  ${起始日期}  ${结束日期}
    ${实际结果}  ${汇总数据}  get_user_report_api  ${站点编号}  ${起始日期}  ${结束日期}
    log  ${预期汇总数据}
    log  ${汇总数据}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=会员账号  ignore_sort=${TRUE}
    dict_data_should_be_equal  ${预期汇总数据}  ${汇总数据}
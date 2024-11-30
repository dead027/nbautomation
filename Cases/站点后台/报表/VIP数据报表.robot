*** Settings ***
Resource  ../../../关键字资源/Resources.robot
Suite Setup  登录站点后台

*** Test Cases ***
昨日_默认查询
    [Tags]  PASS
    ${预期结果}  ${预期汇总数据}  get_vip_data_report_vo  ${站点编号}  -1
    ${实际结果}  ${汇总数据}  get_vip_data_report_api  ${站点编号}  -1
    log  ${预期结果}
    log  ${实际结果}
    list_data_should_be_equal  ${预期结果}  ${实际结果}  dict_key_1=VIP等级  ignore_sort=${TRUE}
    ${diff}  evaluate  abs(${预期汇总数据} -${汇总数据})
    should be true  ${diff} <= 0.01

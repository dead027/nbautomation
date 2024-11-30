*** Settings ***
Resource  ../基础关键字/Resources.robot

*** Keywords ***
执行定时任务
    [Documentation]  总台-VIP升级定时任务 ｜ 沙巴体育拉单 ｜ PG电子自动拉单 ｜ 神话视讯平台拉取订单 ｜ VIP等级配置凌晨0点10秒刷新'
    ...  | 派发奖章 ｜ VIP权益配置凌晨0点20秒刷新定时任务
    [Arguments]  ${定时任务名称}  ${超时时间}=5
    login_job
    ${id}  trigger_task  ${定时任务名称}
    wait_until_job_success  ${定时任务名称}  ${id}  ${超时时间}
*** Settings ***
Resource  ../../../../../关键字资源/Resources.robot
Suite Setup  login_backend  ${中控后台账号1}  ${通用密码}


*** Test Cases ***
VIP权益配置_每日提款次数_后台人工提款不计入提款次数
    ${每日提款次数}  获取会员VIP权益配置  ${会员账号_vip0}  每日提款次数
    各个提款渠道提款  ${会员账号_vip0}  ${每日提款次数}
    后台人工提款

VIP权益配置_每日提款次数_VIP0_未超过提款次数_虚拟币提款
    ${每日提款次数}  获取会员VIP权益配置  ${会员账号_vip0}  每日提款次数
    ${每日提款次数-1}  evaluate  ${每日提款次数}-1
    各个提款渠道提款  ${会员账号_vip0}  ${每日提款次数}
    ${返回值}  虚拟币提款  ${会员账号_vip0}  100
    should be equal  ${返回值}  成功

VIP权益配置_每日提款次数_VIP0_超过提款次数_虚拟币提款
    ${每日提款次数}  get_vip_benefit_config_sql  ${会员账号_vip0}  每日提款次数
    各个提款渠道提款  ${会员账号_vip0}  ${每日提款次数}
    ${返回值}  虚拟币提款  ${会员1}  100  check_code=${False}
    should be equal  ${返回值}  超过提款次数限制
    执行定时任务  VIP升级奖励
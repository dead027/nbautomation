*** Settings ***
Resource  ../功能关键字/Resources.robot

*** Keywords ***
校验佣金报表数据库的值
    [Documentation]  表名： 代理佣金预期表 | 代理佣金结算表
	[Arguments]  ${结算周期}  ${表名}  ${验证的周期}=0
    ${数据库数据}  run keyword if  "${表名}"=="代理佣金结算表"  get_agent_commission_final_report_sql  ${站点编号}  ${结算周期}  date_diff=${验证的周期}
    ...  ELSE  get_agent_commission_expect_report_sql  ${站点编号}  ${结算周期}  date_diff=${验证的周期}
    ${预期数据字典}  calc_win_loss_commission_dao  ${站点编号}  ${结算周期}  ${验证的周期}  ${验证的周期}
    ${len1}  get length  ${数据库数据}
    ${len2}  get length  ${预期数据字典}
    should be equal  ${len1}  ${len2}
    FOR  ${DB数据}  IN  @{数据库数据}
        ${代理账号}  Set Variable  ${DB数据.agent_account}
        ${预期数据}  set variable  ${预期数据字典["${代理账号}"]}
        should be equal  ${DB数据.site_code}  ${站点编号}
        should be equal  ${DB数据.start_time}  ${站点编号}
        should be equal  ${DB数据.end_time}  ${站点编号}
        Should Be Equal As Numbers  ${DB数据.early_settle}  0
        Should Be Equal As Numbers  ${DB数据.user_win_loss}  ${预期数据["本期会员净输赢"]}
        Should Be Equal As Numbers  ${DB数据.user_win_loss_total}  ${预期数据["会员净输赢"]}
        Should Be Equal As Numbers  ${DB数据.venue_fee}  ${预期数据["场馆费"]}
        Should Be Equal As Numbers  ${DB数据.transfer_amount}  ${预期数据["平台币钱包转换金额"]}
        Should Be Equal As Numbers  ${DB数据.access_fee}  ${预期数据["总手续费"]}
        Should Be Equal As Numbers  ${DB数据.adjust_amount}  ${预期数据["其他调整"]}
        Should Be Equal As Numbers  ${DB数据.discount_amount}  ${预期数据["活动优惠"]}
        Should Be Equal As Numbers  ${DB数据.vip_amount}  ${预期数据["VIP福利"]}
        Should Be Equal As Numbers  ${DB数据.valid_bet_amount}  ${预期数据["有效投注金额"]}
        Should Be Equal As Numbers  ${DB数据.last_month_remain}  ${预期数据["上期待冲正金额"]}
        Should Be Equal As Numbers  ${DB数据.net_win_loss}  ${预期数据["会员净输赢"]}
        Should Be Equal As Numbers  ${DB数据.active_number}  ${预期数据["有效活跃"]}
        Should Be Equal As Numbers  ${DB数据.new_valid_number}  ${预期数据["有效新增"]}
        Should Be Equal As Numbers  ${DB数据.agent_rate}  ${预期数据["负盈利佣金比例"]}
        Should Be Equal As Numbers  ${DB数据.commission_amount}  ${预期数据["负盈利佣金"]}
        Should Be Equal As Numbers  ${DB数据.plan_code}  0
    END
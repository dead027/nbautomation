#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/28 16:29
from Library.Common.Utils.Contexts import *
from Library.Common.ServerConnector.Redis import RedisBase
from Library.Common.ServerConnector.Mysql import MysqlBase
from Library.VO.MasterBackend import MasterBackend
from Library.VO.SiteBackend import SiteBackend
from Library.VO.AgentBackend import AgentBackend
from collections import defaultdict
from Library.BO import BO


class VO(MasterBackend, SiteBackend, AgentBackend):
    def __init__(self, env):
        self.env_setup(env)
        super().__init__()

    @staticmethod
    def env_setup(env):
        env_context.set(env)
        MysqlBase()
        RedisBase()


if __name__ == '__main__':
    env_context.set('sit')
    VO.env_setup('sit')

    site_code = 'Vd438R'
    start_diff = 0
    end_diff = 0
    agent_account = 'zscg2a'

    # =============== 报表  ===============

    # VO.get_agent_label_list('aaa', 'bb', 'cc', '创建时间', '降序')
    # rtn = VO.get_new_user_audit_detail_sql(site_code, "sitYJDkxf0")
    # rtn = VO.get_user_update_audit_detail_vo(site_code, "1836618884401315841")
    # 1.会员盈亏
    # rtn = VO.get_user_win_lose_report_vo(site_code, start_diff, end_diff, user_account='yichu001')
    # rtn = VO.get_user_win_lose_report_vo(site_code, start_diff, end_diff, to_site_coin=True, user_account='faye01')
    # 总计
    # rtn = VO.get_user_win_lose_report_total_vo(site_code, start_diff, end_diff)
    # rtn = VO.get_user_win_lose_report_total_vo(site_code, start_diff, end_diff, to_site_coin=True)

    # 2.会员盈亏详情
    # rtn = VO.get_user_win_lose_detail_report_vo(site_code, start_diff=start_diff, end_diff=end_diff,
    #                                             user_account='zscg1u3')

    # 3.活动报表
    # rtn = VO.get_act_report_vo(site_code, start_diff, end_diff)

    # 4.游戏报表
    # rtn = VO.get_game_report_vo(site_code, start_diff=start_diff, end_diff=end_diff, to_site_coin=True)
    # rtn = VO.get_game_report_vo(site_code, start_diff=start_diff, end_diff=end_diff)
    # rtn = VO.get_game_report_vo(site_code, '视讯', start_diff=start_diff, end_diff=end_diff)
    # 游戏类型报表
    # rtn = VO.get_game_report_by_venue_type_vo(site_code, "彩票", currency='CNY', start_diff=start_diff,
    #                                           end_diff=end_diff)
    # rtn = VO.get_game_report_by_venue_type_vo(site_code, "电子", currency='CNY', start_diff=start_diff,
    #                                           end_diff=end_diff, to_site_coin=True)
    # 场馆类型报表
    # rtn = VO.get_game_report_by_venue_vo(site_code, start_diff=start_diff, end_diff=end_diff, to_site_coin=True)

    # 5.每日盈亏
    # rtn = VO.get_daily_report_vo(site_code, start_diff, end_diff, to_site_coin=True)
    # rtn = VO.get_daily_report_vo(site_code, start_diff, end_diff, currency='PHP')
    # 汇总
    # rtn = VO.get_daily_report_total_vo(site_code, start_diff, end_diff)

    # 6.任务报表
    # rtn = VO.get_task_report_vo(site_code, start_diff, end_diff)
    # 总计
    # rtn = VO.get_task_report_total_vo(site_code, start_diff, end_diff)
    # rtn = VO.get_daily_report_vo(site_code, start_diff=-30)

    # 7.会员存取报表
    # rtn = VO.get_user_io_report_vo(site_code, start_diff, end_diff, date_type='日')
    # rtn = VO.get_user_io_report_vo(site_code, start_diff, end_diff, to_site_coin=False, date_type='日')
    # 总计
    # rtn = VO.get_user_io_report_total_vo(site_code, start_diff, end_diff, date_type='日', to_site_coin=True)
    # rtn = VO.get_head_summary_vo(site_code, 'zscg1')

    # 8.场馆盈亏
    # 详情
    # rtn = VO.get_venue_report_detail_vo(site_code, 'PG平台', -5, end_diff, to_site_coin=True)
    # 外层
    # rtn = VO.get_venue_report_vo(site_code, start_diff, end_diff)
    # rtn = VO.get_venue_report_vo(site_code, start_diff, end_diff, to_site_coin=True)
    # 外层总计
    # rtn = VO.get_venue_report_total_vo(site_code, start_diff, end_diff)
    # rtn = VO.get_venue_report_total_vo(site_code, start_diff, end_diff, to_site_coin=True)

    # 9.会员报表
    # rtn = VO.get_user_report_vo(site_code, start_diff, end_diff, user_account='shuke03')

    # 10.综合报表
    # rtn = VO.get_comprehensive_report_dao(site_code, None, start_diff, end_diff, date_type='日')

    # 11.VIP数据报表
    # rtn = VO.get_vip_data_report_vo(site_code, start_diff)
    # print(rtn)
    # print(len(rtn[0]))

    # =============== 2.PC代理后台  ===============
    # 首页上方
    # rtn = VO.get_head_summary_vo(site_code, agent_account, "CNY")
    rtn = VO.get_head_summary_vo(site_code, agent_account)

    # 首页数据对比
    # 1.存款金额
    # rtn = VO.get_io_chart_vo(site_code, agent_account, "会员存款", 0)
    # 2.取款金额
    # rtn = VO.get_io_chart_vo(site_code, agent_account, "会员取款", 0)
    # 3.总输赢
    # rtn = VO.get_win_lose_chart_vo(site_code, agent_account)
    # 4.新注册人数
    # rtn = VO.get_new_register_chart_vo(site_code, agent_account)
    # 5. 首充人数
    # rtn = VO.get_first_deposit_chart_vo(site_code, agent_account)

    # 最新存款
    # rtn = VO.get_deposit_5_vo(site_code, agent_account)
    # 游戏输赢
    # rtn = VO.get_game_record_5_vo(site_code, agent_account)

    # 负盈利佣金比例
    # rtn = BO.calc_win_loss_commission_dao(site_code, specify_agent=agent_account)[agent_account]
    # 返点佣金比例
    # rtn = BO.calc_rebate_commission_dao(site_code, specify_agent=agent_account)[agent_account]

    # =============== 3.H5代理后台  ===============
    # 1.会员管理
    # rtn = VO.get_head_summary_vo(site_code, agent_account)

    # for items in rtn.items():
    #     print(items)

    if type(rtn) in (list, tuple):
        print(len(rtn))
        for _ in rtn:
            print(_)
    elif type(rtn) in (dict, defaultdict):
        for _ in rtn.items():
            print(_)
    else:
        print(rtn)

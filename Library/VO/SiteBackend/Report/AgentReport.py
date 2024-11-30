#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/23 15:03
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:35
from collections import defaultdict
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.site_vip_change_record_model import SiteVipChangeRecord
from Library.MysqlTableModel.site_vip_grade_model import SiteVipGrade
from Library.MysqlTableModel.site_vip_rank_model import SiteVipRank

from Library.Dao import Dao
from sqlalchemy.sql.functions import func
from Library.Common.Utils.DateUtil import DateUtil
from decimal import Decimal


class AgentReport(object):
    """
    代理报表
    """

    @staticmethod
    def get_agent_daily_report_vo(site_code, start_diff=0, end_diff=0, register_start_diff=None,
                                  register_end_diff=None, agent_account=None, parent_account=None,
                                  account_type=None, agent_category=None, commission_min=None, commission_max=None,
                                  currency=None, io_direct=None, to_site_coin=False, date_type='日', stop_diff=0):
        """
        获取代理报表 - 日报
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        agent_list = Dao.get_agent_list_data(site_code, register_start_diff, register_end_diff, agent_account,
                                             parent_account=parent_account, account_type=account_type,
                                             agent_category=agent_category)
        agent_dic = {_.agent_account: _ for _ in agent_list}

        result_dic = defaultdict(lambda: {"统计日期": None, "代理账号": None, "代理层级": None, "账号类型": None,
                                          "代理类别": None, "直属上级": None, "风控层级": None, "代理标签": None,
                                          "注册时间": None,
                                          "团队代理人数": Decimal(0), "直属下级人数": Decimal(0), "注册人数": Decimal(0),
                                          "首存人数": Decimal(0), "首存转化率": Decimal(0), "投注人数": Decimal(0),
                                          "币种": None, "投注额": Decimal(0), "有效投注额": Decimal(0),
                                          "会员输赢": Decimal(0), "平台总输赢": Decimal(0), "调整金额": Decimal(0),
                                          "盈亏比例": Decimal(0), "活动优惠": Decimal(0), "VIP福利": Decimal(0),
                                          "已使用优惠": Decimal(0), "代理佣金": Decimal(0), "平台收入": Decimal(0)})

        agent_summary = Dao.get_sub_agent_list(site_code, key='agent_account')

        # 投注数据
        bet_data = Dao.query_order_data_sql(site_code, settle_start_diff=start_diff, settle_end_diff=end_diff,
                                            date_type=date_type, stop_diff=stop_diff, currency=currency).subquery()

        bet_data = ms_context.get().session.query(bet_data.c.date, bet_data.c.agent_account, bet_data.c.currency,
                                                  bet_data.c.user_account,
                                                  func.sum(bet_data.c.bet_amount).label("bet_amount"),
                                                  func.sum(bet_data.c.valid_amount).label("valid_amount"),
                                                  func.sum(bet_data.c.win_loss_amount).label("win_lose_amount")). \
            group_by(bet_data.c.agent_account, bet_data.c.currency, bet_data.c.date, bet_data.c.user_account).subquery()
        bet_data = ms_context.get().session.query(bet_data.c.date, bet_data.c.agent_account, bet_data.c.currency,
                                                  func.sum(1).label("bet_user_cnt"),
                                                  func.sum(bet_data.c.bet_amount).label("bet_amount"),
                                                  func.sum(bet_data.c.valid_amount).label("valid_amount"),
                                                  func.sum(bet_data.c.win_loss_amount).label("win_lose_amount")).\
            group_by(bet_data.c.agent_account, bet_data.c.currency, bet_data.c.date).all()
        bet_data_dic = defaultdict(Decimal)
        [bet_data_dic.__setitem__((_[0], _[1], _[2]), _) for _ in bet_data]
        # 活动、优惠数据
        used_profit_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
                                                                    date_type).subquery()
        used_profit_data = ms_context.get().session.query(used_profit_data.c.currency, used_profit_data.c.date,
                                                          used_profit_data.c.agent_account,
                                                          func.sum(used_profit_data.c.amount)). \
            group_by(used_profit_data.c.currency, used_profit_data.c.agent_account, used_profit_data.c.date).all()
        used_profit_dic = defaultdict(Decimal)
        [used_profit_dic.__setitem__((_[1], _[2], _[0]), _[3]) for _ in used_profit_data]

        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff,
                                                               date_type).subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.currency, vip_act_data.c.agent_name,
                                                      vip_act_data.c.currency.date,
                                                      func.sum(vip_act_data.c.vip), func.sum(vip_act_data.c.act)). \
            group_by(vip_act_data.c.currency, vip_act_data.c.agent_name, vip_act_data.c.currency.date).all()
        vip_dic = defaultdict(Decimal)
        act_dic = defaultdict(Decimal)
        [vip_dic.__setitem__((_[2], _[1], _[0]), _[3]) for _ in vip_act_data]
        [act_dic.__setitem__((_[2], _[1], _[0]), _[4]) for _ in vip_act_data]

        # 其他调整
        io_data = Dao.get_user_io_summary_data_base(site_code, None, start_diff, end_diff, currency,
                                                    agent_account, stop_diff, date_type).subquery()

        io_data = ms_context.get().session.query(io_data.c.currency, io_data.c.agent_name, io_data.c.date,
                                                 func.sum(io_data.c.adjust_amount).label("调整金额")). \
            group_by(io_data.c.date, io_data.c.agent_name, io_data.c.currency).all()
        io_data_dic = defaultdict(list)
        [io_data_dic.__setitem__((_[2], _[1], _[0]), _[3]) for _ in io_data]

        for key, value in bet_data_dic.items():
            result_dic[key]["统计日期"] = value[0]
            result_dic[key]["代理账号"] = value[0]
            result_dic[key]["代理层级"] = value[0]
            result_dic[key]["账号类型"] = value[0]
            result_dic[key]["代理类别"] = value[0]
            result_dic[key]["直属上级"] = value[0]
            result_dic[key]["风控层级"] = value[0]
            result_dic[key]["代理标签"] = value[0]
            result_dic[key]["注册时间"] = value[0]
            result_dic[key]["团队代理人数"] = value[0]
            result_dic[key]["直属下级人数"] = value[0]
            result_dic[key]["注册人数"] = value[0]
            result_dic[key]["首存人数"] = value[0]
            result_dic[key]["首存转化率"] = value[0]
            result_dic[key]["投注人数"] = value[0]
            result_dic[key]["币种"] = value[0]
            result_dic[key]["投注额"] = value[0]
            result_dic[key]["有效投注额"] = value[0]
            result_dic[key]["会员输赢"] = value[0]
            result_dic[key]["平台总输赢"] = value[0]

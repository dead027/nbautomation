#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/8 21:22
from collections import defaultdict

from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.Dao.Mysql.ChainQery.Order import Order

from sqlalchemy import func, and_, case, distinct
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import Funds


# class Report(object):
#
#     @staticmethod
#     def get_recharge_channel_report(site_code=None, start_diff=0, end_diff=0, date_type='日', stop_diff=0,
#                                     channel_name=None, currency=None, recharge_type=None, recharge_method=None):
#         """
#         游戏报表: 输赢金额已取反
#         @return:
#         """
#         recharge_data = Funds.get_user_deposit_record(site_code, start_diff, end_diff, stop_diff, date_type)
#         data = Order.query_order_data_sql(site_code, settle_start_diff=start_diff, settle_end_diff=end_diff,
#                                           date_type=date_type, stop_diff=stop_diff,
#                                           venue_type=venue_type, currency=currency).subquery()
#         data = ms_context.get().session.query(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.game_name,
#                                               data.c.user_account, data.c.date, func.count(1).label("bet_cnt"),
#                                               func.sum(data.c.bet_amount).label("bet_amount"),
#                                               func.sum(data.c.valid_amount).label("valid_amount"),
#                                               func.sum(-data.c.win_loss_amount).label("win_lose_amount")). \
#             group_by(data.c.venue_type, data.c.venue_code, data.c.currency, data.c.user_account, data.c.game_name,
#                      data.c.date)
#         return data

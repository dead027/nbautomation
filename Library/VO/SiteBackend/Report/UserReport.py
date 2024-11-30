#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:35
from collections import defaultdict
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.site_info_model import SiteInfo
from Library.MysqlTableModel.user_info_model import UserInfo

from Library.Dao import Dao
from sqlalchemy.sql.functions import func
from decimal import Decimal


class UserReport(object):
    """
    会员报表
    """

    @staticmethod
    def get_user_report_vo(site_code, start_diff=0, end_diff=0, register_start_diff=None, register_end_diff=None,
                           user_account=None, agent_account=None, account_type="正式", order_quantity_min=None,
                           order_quantity_max=None, bet_amount_min=None, bet_amount_max=None, valid_amount_min=None,
                           valid_amount_max=None, win_lose_amount_min=None, win_lose_amount_max=None,
                           deposit_amount_min=None, deposit_amount_max=None, withdraw_amount_min=None,
                           withdraw_amount_max=None, currency=None, stop_diff=None, to_site_coin=False, date_type='日'):
        """
        获取会员报表
        :param account_type: 正式 ｜ 测试
        :param sort_by: 首存金额 ｜ 总存款 ｜ 存款次数 ｜ 上级转入 ｜ 转入次数 ｜ 总取款 ｜ 取款次数 ｜ 大额取款次数
        @return:
        """
        start_diff = int(start_diff)
        end_diff = int(end_diff)
        user_account_type = Dao.get_user_account_type(to_zh=True)
        timezone = Dao.get_site_timezone(site_code, )
        # 汇率
        currency_rate = Dao.currency_rate(site_code)
        # 1.会员信息
        user_data = Dao.get_user_info_sql(site_code, register_start_diff=register_start_diff,
                                          register_end_diff=register_end_diff, account_type=account_type)
        user_info_dic = {user_info.user_account: user_info for user_info, _ in user_data}
        # 2.投注数据
        bet_data = Dao.get_user_bet_summary_by_user_sql(site_code, account_type=account_type,
                                                        start_diff=start_diff,
                                                        end_diff=end_diff, stop_diff=stop_diff,
                                                        date_type=date_type).subquery()
        bet_data = ms_context.get().session.query(bet_data.c.user_account, bet_data.c.agent_acct,
                                                  func.sum(bet_data.c.order_amount), func.sum(bet_data.c.bet_amount),
                                                  func.sum(bet_data.c.valid_amount),
                                                  func.sum(bet_data.c.win_loss_amount)). \
            group_by(bet_data.c.user_account, bet_data.c.agent_acct).all()
        bet_dic = defaultdict(list)
        [bet_dic.__setitem__((_[0], _[1]), _) for _ in bet_data]
        # 3.充提数据
        io_data = Dao.get_user_io_summary_data_base(site_code, user_account, start_diff, end_diff, currency,
                                                    agent_account, stop_diff, date_type).subquery()

        io_data = ms_context.get().session.query(io_data.c.user_account, io_data.c.currency, io_data.c.agent_name,
                                                 func.sum(io_data.c.deposit_cnt).label("存款次数"),
                                                 func.sum(io_data.c.deposit_amount).label("总存款"),
                                                 func.sum(io_data.c.withdraw_cnt).label("取款次数"),
                                                 func.sum(io_data.c.withdraw_amount).label("总取款"),
                                                 func.sum(io_data.c.transfer_amount).label("上级转入"),
                                                 func.sum(io_data.c.transfer_cnt).label("转入次数"),
                                                 func.sum(io_data.c.big_cnt).label("大额取款次数"),
                                                 func.sum(io_data.c.other_adjust).label("其他调整"),
                                                 func.sum(io_data.c.io_diff).label("存取差")). \
            group_by(io_data.c.user_account, io_data.c.agent_name, io_data.c.currency).all()
        io_data_dic = defaultdict(list)
        io_data = list(filter(lambda _: any(_[3:]), io_data))
        [io_data_dic.__setitem__((_[0], _[2]), _) for _ in io_data]

        # 4.已使用优惠
        used_profit_data = Dao.get_used_platform_coin_sum_data_base(site_code, start_diff, end_diff, stop_diff,
                                                                    date_type).subquery()
        used_profit_data = ms_context.get().session.query(used_profit_data.c.user_account,
                                                          used_profit_data.c.agent_account,
                                                          func.sum(used_profit_data.c.amount)). \
            group_by(used_profit_data.c.user_account, used_profit_data.c.agent_account).all()
        used_profit_dic = defaultdict(Decimal)
        [used_profit_dic.__setitem__((_[0], _[1]), _[2]) for _ in used_profit_data]

        # 5.VIP福利和活动优惠
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff,
                                                               date_type).subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.user_account, vip_act_data.c.agent_name,
                                                      func.sum(vip_act_data.c.vip), func.sum(vip_act_data.c.act)). \
            group_by(vip_act_data.c.user_account, vip_act_data.c.agent_name).all()
        vip_dic = defaultdict(Decimal)
        act_dic = defaultdict(Decimal)
        [vip_dic.__setitem__((_[0], _[1]), _[2]) for _ in vip_act_data]
        [act_dic.__setitem__((_[0], _[1]), _[3]) for _ in vip_act_data]

        # 6.大额
        # 大额数据
        big = Dao.get_user_big_io_data_base(site_code, user_account, start_diff, end_diff, currency,
                                            stop_diff=stop_diff, date_type=date_type).subquery()
        big = ms_context.get().session.query(big.c.user_account, big.c.agent_account,
                                             func.sum(big.c.big_cnt).label("big_cnt")). \
            group_by(big.c.user_account, big.c.agent_account).all()
        big_dic = defaultdict(Decimal)
        [big_dic.__setitem__((_[0], _[1]), _[2]) for _ in big]

        data_list = []
        rank_dic = {_.vip_rank_code: _.vip_rank_name for _ in Dao.get_site_vip_rank_sql(site_code)}
        for user_account, agent_account in set(list(io_data_dic.keys()) + list(used_profit_dic.keys()) +
                                               list(vip_dic.keys()) + list(act_dic.keys()) + list(bet_dic.keys())):
            user_info: UserInfo = user_info_dic[user_account]
            key = (user_account, agent_account)
            sub_io_data = io_data_dic[key]
            sub_bet_data = bet_dic[key]

            rate = currency_rate[user_info.main_currency]

            adjust_amount = sub_io_data[10] if sub_io_data else 0
            first_deposit_amount = user_info.first_deposit_amount
            deposit_amount = sub_io_data[4] if sub_io_data else 0
            withdraw_amount = sub_io_data[6] if sub_io_data else 0
            io_diff_amount = sub_io_data[11] if sub_io_data else 0
            order_amount = sub_bet_data[2] if sub_bet_data else 0
            bet_amount = sub_bet_data[3] if sub_bet_data else 0
            valid_amount = sub_bet_data[4] if sub_bet_data else 0
            user_win_lose = sub_bet_data[5] if sub_bet_data else 0
            used_amount = used_profit_dic[key]
            if user_account == 'ford2024001':
                pass

            sub_data = {"会员账号": user_account, "账号类型": user_account_type[int(user_info.account_type)],
                        "主币种": user_info.main_currency,
                        "VIP段位": rank_dic[user_info.vip_rank],
                        "VIP等级": user_info.vip_grade_code, "会员标签": user_info.user_label_id,
                        "上级代理": agent_account, "转代次数": user_info.trans_agent_time,
                        "注册时间": DateUtil.timestamp_to_date(user_info.register_time, timezone, '秒'),
                        "首存金额": round(first_deposit_amount / rate, 2) if to_site_coin else first_deposit_amount,
                        "总存款": round(deposit_amount / rate, 2) if to_site_coin else deposit_amount,
                        "存款次数": sub_io_data[3] if sub_io_data else 0,
                        "上级转入": sub_io_data[7] if sub_io_data else 0,
                        "转入次数": sub_io_data[8] if sub_io_data else 0,
                        "总取款": round(withdraw_amount / rate, 2) if to_site_coin else withdraw_amount,
                        "取款次数": sub_io_data[5] if sub_io_data else 0,
                        "大额取款次数": big_dic[key] if sub_io_data else 0,
                        "存取差": round(io_diff_amount / rate, 2) if to_site_coin else io_diff_amount,
                        "VIP福利": vip_dic[key],
                        "活动优惠": act_dic[key],
                        "已使用优惠": round(used_amount / rate, 2) if to_site_coin else used_amount,
                        "其他调整": round(adjust_amount / rate, 2) if to_site_coin else adjust_amount,
                        "注单量": order_amount,
                        "投注金额": round(bet_amount / rate, 2) if to_site_coin else bet_amount,
                        "有效投注": round(valid_amount / rate, 2) if to_site_coin else valid_amount,
                        "会员输赢": round(user_win_lose / rate, 2) if to_site_coin else user_win_lose,
                        "会员净盈利": round((user_win_lose + + used_amount) / rate,
                                       2) if to_site_coin else user_win_lose + used_amount}
            data_list.append(sub_data)
        if order_quantity_min:
            data_list = list(filter(lambda x: x["注单量"] >= order_quantity_min, data_list))
        if order_quantity_max:
            data_list = list(filter(lambda x: x["注单量"] <= order_quantity_max, data_list))
        if bet_amount_min:
            data_list = list(filter(lambda x: x["投注金额"] >= bet_amount_min, data_list))
        if bet_amount_max:
            data_list = list(filter(lambda x: x["投注金额"] <= bet_amount_max, data_list))
        if valid_amount_min:
            data_list = list(filter(lambda x: x["有效投注"] >= valid_amount_min, data_list))
        if valid_amount_max:
            data_list = list(filter(lambda x: x["有效投注"] <= valid_amount_max, data_list))
        if win_lose_amount_min:
            data_list = list(filter(lambda x: x["会员输赢"] >= win_lose_amount_min, data_list))
        if win_lose_amount_max:
            data_list = list(filter(lambda x: x["会员输赢"] <= win_lose_amount_max, data_list))
        if deposit_amount_min:
            data_list = list(filter(lambda x: x["总存款"] >= deposit_amount_min, data_list))
        if deposit_amount_max:
            data_list = list(filter(lambda x: x["总存款"] <= deposit_amount_max, data_list))
        if withdraw_amount_min:
            data_list = list(filter(lambda x: x["总取款"] >= withdraw_amount_min, data_list))
        if withdraw_amount_max:
            data_list = list(filter(lambda x: x["总取款"] <= withdraw_amount_max, data_list))
        return data_list

    @staticmethod
    def get_user_report_total_vo(site_code, start_diff=0, end_diff=0, register_start_diff=None, register_end_diff=None,
                                 user_account=None, agent_account=None, account_type="正式", order_quantity_min=None,
                                 order_quantity_max=None, bet_amount_min=None, bet_amount_max=None,
                                 valid_amount_min=None,
                                 valid_amount_max=None, win_lose_amount_min=None, win_lose_amount_max=None,
                                 deposit_amount_min=None, deposit_amount_max=None, withdraw_amount_min=None,
                                 withdraw_amount_max=None, currency=None, stop_diff=None, to_site_coin=False,
                                 date_type='日'):
        data = UserReport.get_user_report_vo(site_code, start_diff, end_diff, register_start_diff, register_end_diff,
                                             user_account, agent_account, account_type, order_quantity_min,
                                             order_quantity_max, bet_amount_min, bet_amount_max, valid_amount_min,
                                             valid_amount_max, win_lose_amount_min, win_lose_amount_max,
                                             deposit_amount_min, deposit_amount_max, withdraw_amount_min,
                                             withdraw_amount_max, currency, stop_diff, to_site_coin, date_type)
        result = {"首存金额": Decimal(0), "总存款": Decimal(0), "存款次数": 0, "上级转入": Decimal(0), "转入次数": 0,
                  "总取款": Decimal(0), "取款次数": 0, "大额取款次数": 0, "存取差": Decimal(0), "VIP福利": Decimal(0),
                  "活动优惠": Decimal(0), "已使用优惠": Decimal(0), "其他调整": Decimal(0), "注单量": 0,
                  "投注金额": Decimal(0), "有效投注": Decimal(0), "会员输赢": Decimal(0), "会员净盈利": Decimal(0)}
        for _ in data:
            for key in result:
                result[key] += _[key]
        return result


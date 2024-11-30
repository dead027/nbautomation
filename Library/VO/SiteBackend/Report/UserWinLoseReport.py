#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:35
import copy
from collections import defaultdict
from decimal import Decimal
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.user_info_model import UserInfo

from Library.Dao import Dao
from Library.BO import BO
from sqlalchemy.sql.functions import func


class UserWinLoseReport(object):
    """
    会员盈亏报表
    """

    @staticmethod
    def get_user_win_lose_detail_report_vo(site_code, start_diff=0, end_diff=0, user_account=None, agent_account=None,
                                           account_type=None, currency=None, stop_diff=None, to_site_coin=False,
                                           date_type='日'):
        """
        获取会员盈亏报表 - 详情
        :param account_type: 正式 ｜ 测试
        :param sort_by: 首存金额 ｜ 总存款 ｜ 存款次数 ｜ 上级转入 ｜ 转入次数 ｜ 总取款 ｜ 取款次数 ｜ 大额取款次数
        @return:
        """
        # 1.投注数据
        bet_data = Dao.get_user_bet_summary_by_user_sql(site_code, account_type=account_type, start_diff=start_diff,
                                                        end_diff=end_diff, stop_diff=stop_diff, date_type=date_type). \
            all()
        bet_dic = defaultdict(list)
        # 日期，user_account,currency,agent_acct
        [bet_dic.__setitem__((_[0], _[1], _[4], _[3]), _) for _ in bet_data]
        # 2.已使用优惠
        used_data_dic = BO.calc_used_profit_detail_bo(site_code, start_diff, end_diff, stop_diff, date_type)
        # used_data_dic = defaultdict(Decimal)
        # [used_data_dic.__setitem__((_[0], _[1], _[3], _[2]), _[4]) for _ in used_profit_data]
        # 3.VIP福利和活动优惠
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff, date_type)
        vip_data_dic = defaultdict(Decimal)
        [vip_data_dic.__setitem__((_[0], _[1], _[2], _[3]), _) for _ in vip_act_data]

        # 4.调整金额
        adjust_data = Dao.get_user_io_summary_data_base(site_code, user_account, start_diff, end_diff, currency,
                                                        agent_account, stop_diff, '日').subquery()

        adjust_data = ms_context.get().session.query(adjust_data.c.date, adjust_data.c.user_account,
                                                     adjust_data.c.currency, adjust_data.c.agent_name,
                                                     func.sum(adjust_data.c.other_amount).label("调整金额")). \
            group_by(adjust_data.c.date, adjust_data.c.user_account, adjust_data.c.agent_name,
                     adjust_data.c.currency).all()
        adjust_dic = defaultdict(Decimal)
        [adjust_dic.__setitem__((_[0], _[1], _[2], _[3]), _[4]) for _ in adjust_data]
        # 汇率
        currency_rate = Dao.currency_rate(site_code)

        result_dic = defaultdict(list)
        for keys in list(set(list(bet_dic.keys()) + list(used_data_dic.keys()) + list(vip_data_dic.keys()) +
                             list(adjust_dic.keys()))):
            date, u_account, main_currency, u_agent_account = keys
            bet_data_dic = bet_dic[keys]
            if main_currency not in currency_rate:
                continue
            rate = currency_rate[main_currency]
            user_win_lose = bet_data_dic[5] if bet_data_dic else 0
            user_win_lose = round(user_win_lose / rate, 2) if to_site_coin else user_win_lose
            other_adjust = adjust_dic[keys] if adjust_dic[keys] else 0
            other_adjust = round(other_adjust / rate, 2) if to_site_coin else other_adjust
            bet_amount = bet_data_dic[6] if bet_data_dic else 0
            bet_amount = round(bet_amount / rate, 2) if to_site_coin else bet_amount
            valid_amount = bet_data_dic[7] if bet_data_dic else 0
            valid_amount = round(valid_amount / rate, 2) if to_site_coin else valid_amount
            used_data = used_data_dic[keys]
            used_data = round(used_data / rate, 2) if to_site_coin else used_data
            sub_vip_act_data = vip_data_dic[keys] if keys in vip_data_dic else [0, 0, 0, 0, 0, 0]
            sub_vip_amount = sub_vip_act_data[4]
            sub_act_amount = sub_vip_act_data[5]

            # 净盈利 = 会员输赢 + 其他调整 + 已使用优惠 + 邀请好友人头费 + 邀请好友佣金返利
            net_win_lose = user_win_lose + other_adjust + used_data
            sub_data = {"日期": date, "上级代理": u_agent_account,
                        "注单量": bet_data_dic[8] if bet_data_dic else 0,
                        "投注金额": bet_amount,
                        "有效投注": valid_amount,
                        "会员输赢": user_win_lose,
                        "VIP福利": sub_vip_amount,
                        "活动优惠": sub_act_amount,
                        "调整金额": other_adjust,
                        "净盈利": net_win_lose,
                        "已使用优惠": used_data}
            result_dic[u_account].append(sub_data)
        return result_dic

    @staticmethod
    def get_user_win_lose_report_vo(site_code, start_diff=0, end_diff=0, user_account=None, agent_account=None,
                                    account_type=None, order_quantity_min=None, order_quantity_max=None,
                                    bet_amount_min=None, bet_amount_max=None, win_lose_amount_min=None,
                                    win_lose_amount_max=None, profit_amount_min=None, profit_amount_max=None,
                                    currency=None, stop_diff=None, to_site_coin=False, date_type='日'):
        """
        获取会员盈亏报表
        :param account_type: 正式 ｜ 测试
        :param sort_by: 首存金额 ｜ 总存款 ｜ 存款次数 ｜ 上级转入 ｜ 转入次数 ｜ 总取款 ｜ 取款次数 ｜ 大额取款次数
        @return:
        """
        grade_dic = Dao.get_grade_name_dic_dao()
        # 会员信息
        user_data = Dao.get_user_info_sql(site_code, user_account=user_account, parent_agent=agent_account,
                                          account_type=account_type, main_currency=currency)
        user_info_dic = {user_info.user_account: user_info for user_info, _ in user_data}
        # 已使用优惠
        used_profit_data = BO.calc_used_profit_bo(site_code, start_diff, end_diff, stop_diff, date_type)
        # VIP福利和活动优惠
        vip_act_data = Dao.get_user_platform_coin_sum_data_dao(site_code, start_diff, end_diff, stop_diff,
                                                               date_type).subquery()
        vip_act_data = ms_context.get().session.query(vip_act_data.c.user_account, vip_act_data.c.agent_name,
                                                      vip_act_data.c.main_currency,
                                                      func.sum(vip_act_data.c.vip).label('vip'),
                                                      func.sum(vip_act_data.c.act).label('act')). \
            group_by(vip_act_data.c.user_account, vip_act_data.c.agent_name, vip_act_data.c.main_currency).all()
        # 投注数据
        bet_data = Dao.get_user_bet_summary_by_user_sql(site_code, account_type=account_type, start_diff=start_diff,
                                                        end_diff=end_diff, stop_diff=stop_diff, date_type=date_type). \
            subquery()
        bet_data = ms_context.get().session.query(bet_data.c.user_account, bet_data.c.agent_acct, bet_data.c.currency,
                                                  func.sum(bet_data.c.win_loss_amount).label("win_loss_amount"),
                                                  func.sum(bet_data.c.bet_amount).label("bet_amount"),
                                                  func.sum(bet_data.c.valid_amount).label("valid_amount"),
                                                  func.sum(bet_data.c.order_amount).label("order_amount")). \
            group_by(bet_data.c.user_account, bet_data.c.agent_acct, bet_data.c.currency).all()
        # 调整金额
        adjust_data = Dao.get_user_io_summary_data_base(site_code, user_account, start_diff, end_diff, currency,
                                                        agent_account, stop_diff, '日').subquery()

        adjust_data = ms_context.get().session.query(adjust_data.c.user_account, adjust_data.c.agent_name,
                                                     adjust_data.c.currency,
                                                     func.sum(adjust_data.c.other_adjust).label("其他调整")). \
            group_by(adjust_data.c.user_account, adjust_data.c.agent_name, adjust_data.c.currency).all()

        bet_dic = defaultdict(list)
        [bet_dic.__setitem__((_[0], _[1]), _) for _ in bet_data]
        adjust_dic = defaultdict(Decimal)
        [adjust_dic.__setitem__((_[0], _[1]), _) for _ in adjust_data]
        used_profit_dic = defaultdict(Decimal)
        [used_profit_dic.__setitem__((_[0], _[1]), value) for _, value in used_profit_data.items()]
        vip_act_dic = defaultdict(list)
        [vip_act_dic.__setitem__((_[0], _[1]), _) for _ in vip_act_data]

        # 有数据的会员字典
        has_data_user_dic = defaultdict(list)
        [has_data_user_dic[_[0]].append(_) for _ in list(set(list(bet_dic.keys()) + list(adjust_dic.keys()) +
                                                             list(used_profit_dic.keys()) +
                                                             list(vip_act_dic.keys())))]

        # 汇总充提数据，
        currency_rate = Dao.currency_rate(site_code)
        final_data_list = []
        rank_dic = {_.vip_rank_code: _.vip_rank_name for _ in Dao.get_site_vip_rank_sql(site_code)}

        account_type_dic = Dao.get_user_account_type(to_zh=True)
        for user_account, user_info in user_info_dic.items():
            user_info: UserInfo
            sub_data = {"会员账号": user_account, "账号类型": account_type_dic[int(user_info.account_type)],
                        "主币种": user_info.main_currency,
                        "VIP段位": rank_dic[user_info.vip_rank],
                        "VIP等级": grade_dic[user_info.vip_grade_code], "会员标签": user_info.user_label_id,
                        "上级代理": user_info.super_agent_account}
            if user_account in has_data_user_dic:
                for sub_key in has_data_user_dic[user_account]:
                    rate = currency_rate[user_info.main_currency]
                    sub_user_account, sub_agent_account = sub_key
                    sub_bet_data = bet_dic[sub_key]
                    sub_adjust_data = adjust_dic[sub_key]
                    sub_vip_act_data = vip_act_dic[sub_key]
                    sub_used_profit_data = used_profit_dic[sub_key]

                    bet_amount = sub_bet_data[4] if sub_bet_data else 0
                    valid_amount = sub_bet_data[5] if sub_bet_data else 0
                    user_win_lose = sub_bet_data[3] if sub_bet_data else 0
                    adjust_amount = sub_adjust_data[3] if sub_adjust_data else 0
                    vip_amount = sub_vip_act_data[3] if sub_vip_act_data else 0
                    activity_amount = sub_vip_act_data[4] if sub_vip_act_data else 0
                    used_profit_amount = sub_used_profit_data

                    sub_data_1 = copy.deepcopy(sub_data)
                    sub_data_1["上级代理"] = sub_agent_account
                    sub_data_1["注单量"] = sub_bet_data[6] if sub_bet_data else 0
                    sub_data_1["投注金额"] = round(bet_amount / rate, 2) if to_site_coin else bet_amount
                    sub_data_1["有效投注"] = round(valid_amount / rate, 2) if to_site_coin else valid_amount
                    sub_data_1["会员输赢"] = round(user_win_lose / rate, 2) if to_site_coin else user_win_lose
                    sub_data_1["VIP福利"] = vip_amount
                    sub_data_1["活动优惠"] = activity_amount
                    sub_data_1["其他调整"] = round(adjust_amount / rate, 2) if to_site_coin else adjust_amount
                    # 会员输赢+已使用优惠+邀请好友人头费+邀请好友佣金返利
                    sub_data_1["会员净盈利"] = round((user_win_lose + used_profit_amount) / rate, 2) if to_site_coin \
                        else user_win_lose + used_profit_amount
                    sub_data_1["已使用优惠"] = round(used_profit_amount / rate, 2) if to_site_coin else used_profit_amount
                    final_data_list.append(sub_data_1)
        if order_quantity_min:
            final_data_list = list(filter(lambda x: x["注单量"] >= order_quantity_min, final_data_list))
        if order_quantity_max:
            final_data_list = list(filter(lambda x: x["注单量"] <= order_quantity_max, final_data_list))
        if bet_amount_min:
            final_data_list = list(filter(lambda x: x["投注金额"] >= bet_amount_min, final_data_list))
        if bet_amount_max:
            final_data_list = list(filter(lambda x: x["投注金额"] <= bet_amount_max, final_data_list))
        if win_lose_amount_min:
            final_data_list = list(filter(lambda x: x["会员输赢"] >= win_lose_amount_min, final_data_list))
        if win_lose_amount_max:
            final_data_list = list(filter(lambda x: x["会员输赢"] <= win_lose_amount_max, final_data_list))
        if profit_amount_min:
            final_data_list = list(filter(lambda x: x["会员净盈利"] >= profit_amount_min, final_data_list))
        if profit_amount_max:
            final_data_list = list(filter(lambda x: x["会员净盈利"] <= profit_amount_max, final_data_list))
        rtn = filter(lambda x: any([x[_] for _ in ["注单量", "投注金额", "会员输赢", "VIP福利", "活动优惠", "其他调整",
                                                   "会员净盈利", "已使用优惠"]]), final_data_list)
        return list(rtn)

    @staticmethod
    def get_user_win_lose_report_total_vo(site_code, start_diff=0, end_diff=0, user_account=None, agent_account=None,
                                          account_type=None, order_quantity_min=None, order_quantity_max=None,
                                          bet_amount_min=None, bet_amount_max=None, win_lose_amount_min=None,
                                          win_lose_amount_max=None, profit_amount_min=None, profit_amount_max=None,
                                          currency=None, stop_diff=None, to_site_coin=False, date_type='日'):
        """
        获取会员盈亏报表 - 总计
        @return:
        """
        data = UserWinLoseReport.get_user_win_lose_report_vo(site_code, start_diff, end_diff, user_account,
                                                             agent_account, account_type, order_quantity_min,
                                                             order_quantity_max, bet_amount_min, bet_amount_max,
                                                             win_lose_amount_min, win_lose_amount_max,
                                                             profit_amount_min, profit_amount_max, currency,
                                                             stop_diff, to_site_coin, date_type)
        result = {"注单量": Decimal(0), "投注金额": Decimal(0), "有效投注": Decimal(0), "会员输赢": Decimal(0),
                  "VIP福利": Decimal(0), "活动优惠": Decimal(0), "已使用优惠": Decimal(0), "其他调整": Decimal(0),
                  "会员净盈利": Decimal(0)}
        for _ in data:
            for key in result:
                result[key] += _[key]
        return result

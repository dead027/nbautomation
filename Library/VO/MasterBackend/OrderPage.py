#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/29 14:21
from Library.Dao.Mysql.ChainQery.System import System
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.GameEnum import GameEnum
from sqlalchemy import func, desc
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.Dao.Mysql.ChainQery.User import User, UserInfo
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao import Dao


class OrderPage(object):
    @staticmethod
    def get_order_list_sql(bet_number="", third_party_order_number="", start_settle_time_diff=None,
                           stop_settle_time_diff=None, game_platform="", game_name="", member_account="",
                           account_type="", superior_agent="", game_account="", event_id="", bet_status="",
                           start_bet_amount="", stop_bet_amount="", start_members_win_lose="",
                           stop_members_win_lose="", start_valid_amount="", stop_valid_amount="", betting_ip="",
                           start_vip_level="", stop_vip_level="", change_status="", device_type="",
                           start_change_time="", stop_change_time="", start_bet_time_diff=-7,
                           stop_bet_time_diff=0):
        """
        获取游戏注单信息
        :param bet_number 注单号
        :param third_party_order_number 三方订单号
        :param start_bet_time_diff 开始下注时间
        :param stop_bet_time_diff 结束下注时间
        :param start_settle_time_diff 结算开始时间
        :param stop_settle_time_diff 结算结束时间
        :param game_platform 游戏平台
        :param game_name 游戏名称
        :param member_account 会员账户
        :param account_type 账号类型
        :param superior_agent 上级代理
        :param game_account 游戏账号
        :param event_id 赛事ID/局号
        :param bet_status 注单状态
        :param start_bet_amount 投注金额开始值
        :param stop_bet_amount 投注金额截至值
        :param start_members_win_lose 会员输赢开始值
        :param stop_members_win_lose 会员输赢截至值
        :param start_valid_amount 有效投注开始值
        :param stop_valid_amount 有效投注截至值
        :param betting_ip 投注IP
        :param start_vip_level VIP等级开始值
        :param stop_vip_level VIP等级截至值
        :param change_status 变更状态
        :param device_type 投注终端
        :param start_change_time 变更时间开始值
        :param stop_change_time 变更时间截至值
        :return:
        """
        result = Dao.query_order_data_sql(bet_number, third_party_order_number, start_settle_time_diff,
                                          stop_settle_time_diff, game_platform, game_name, member_account,
                                          account_type, superior_agent, game_account, event_id, bet_status,
                                          start_bet_amount, stop_bet_amount, start_members_win_lose,
                                          stop_members_win_lose, start_valid_amount, stop_valid_amount, betting_ip,
                                          start_vip_level, stop_vip_level, change_status, device_type,
                                          start_change_time, stop_change_time, start_bet_time_diff,
                                          stop_bet_time_diff)
        result_list = []
        for item, _ in result:
            sub_data = {"注单号": item.order_id, "三方订单号": item.third_order_id, "游戏平台": item.venue_code,
                        "游戏分类": item.game_name, "赛事ID/局号": item.game_no,
                        "会员账号": item.user_account, "游戏账号": item.casino_user_name,
                        "上级代理": item.agent_acct,
                        "账号类型": System.get_user_account_type(item.account_type, True),
                        "VIP等级": item.vip_rank_code, "游戏名称": item.game_name,
                        "玩法": item.parlay_info, "注单详情": item.order_info,
                        "投注金额": item.bet_amount, "会员输赢": item.win_loss_amount, "有效投注": item.valid_amount,
                        "注单状态": System.get_order_status(item.order_status, True), "投注时间": item.bet_time,
                        "结算时间": item.settle_time,
                        "同步时间": item.settle_time, "投注IP": item.bet_ip,
                        "投注终端": System.get_user_register_client(item.device_type, True)}
            result_list.append(sub_data)
        return result_list

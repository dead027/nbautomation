#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/28 18:00
from Library.Dao.Mysql.ChainQery.System import System
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from sqlalchemy import func, desc
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.Dao.Mysql.ChainQery.SiteBackend.User import User, UserInfo
from Library.Dao import Dao


class UserDetail(object):

    @staticmethod
    def get_user_detail_base_info_vo(site_code, user_account):
        """
        基本信息
        :param site_code:
        :param user_account:
        :return:
        """
        user_info: UserInfo = User.get_user_info_sql(site_code, user_account)[0][0]
        if user_info.user_label_id:
            label_name = [Dao.get_user_label_info(label_id)[0].label_name for label_id in
                          user_info.user_label_id.split(",")]
        else:
            label_name = ""
        return {"会员账号": user_info.user_account,
                "账号类型": System.get_user_account_type(user_info.account_type, True),
                "账号状态": System.get_user_account_status(user_info.account_status, True), "会员标签": label_name,
                "主币种": user_info.main_currency, "首存时间": user_info.first_deposit_time,
                "首存金额": user_info.first_deposit_amount, "离线天数": user_info.offline_days,
                "注册时间": user_info.register_time, "注册IP": user_info.register_ip,
                "最后登录时间": user_info.last_login_time,
                "上级代理": user_info.super_agent_account, "推荐人": user_info.inviter, "手机号码": user_info.phone,
                "邮箱": user_info.email, "站点编号": user_info.site_code, "上级代理id": user_info.super_agent_id,
                "手机区号": user_info.area_code}

    @staticmethod
    def get_user_detail_vip_info_vo(site_code, user_account):
        """
        获取会员VIP信息
        @param site_code:
        @param user_account:
        @return:
        """
        user_info: UserInfo = User.get_user_info_sql(site_code, user_account)[0]
        current_exp = Dao.get_user_exp(site_code, user_account)
        upgrade_exp = Dao.get_vip_level_config_sql(site_code=site_code, level_code=user_info.vip_grade_code)
        return {"VIP段位": "", "VIP等级": "", "升级要求": f"{current_exp}/{upgrade_exp}"}

    @staticmethod
    def get_user_detail_balance_vo(site_code, user_account):
        """
        获取会员钱包余额信息
        @param site_code:
        @param user_account:
        @return:
        """
        balance = Dao.get_user_balance(site_code, user_account)
        return {"钱包余额": balance[0], "提现冻结金额": balance[1]}

    @staticmethod
    def _get_user_detail_bet_info_vo(site_code, user_account):
        """
        查询会员详情页面的投注信息
        @param site_code:
        @param user_account:
        @return:
        """
        data = ms_context.get().session.query(func.sum(OrderRecord.bet_amount),
                                              func.sum(OrderRecord.win_loss_amount)). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code). \
            group_by(OrderRecord.user_account).first()
        return data

    @staticmethod
    def get_user_detail_bet_info_vo(site_code, user_account):
        """
        查询会员详情页面的投注信息 todo
        @param site_code:
        @param user_account:
        @return:
        """
        # 总投注、玩家输赢
        bet_data = UserDetail._get_user_detail_bet_info(site_code, user_account)
        # 红利
        profit = 1
        # 总输赢
        total_win_lose = bet_data[1] + profit
        return {"总投注": bet_data[0], "玩家输赢": bet_data[1], "总输赢": total_win_lose, "红利": profit}

    @staticmethod
    def get_user_detail_bet_top_3_vo(site_code, user_account, month_diff=0, sort_by="会员输赢"):
        """
        会员详情 - top3
        @param site_code:
        @param user_account:
        @param month_diff:
        @param sort_by:
        @return:
        """
        sort_dic = {"会员输赢": "win_loss", "投注": "bet_amount", "有效投注": "valid"}
        start_time, end_time = DateUtil.get_timestamp_range(month_diff, month_diff, date_type='月')
        data = ms_context.get().session.query(OrderRecord.venue_code,
                                              func.sum(OrderRecord.bet_amount).label("bet_amount"),
                                              func.sum(OrderRecord.win_loss_amount).label("win_loss"),
                                              func.sum(OrderRecord.valid_amount).label("valid")). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code,
                   OrderRecord.settle_time.between(start_time, end_time)). \
            group_by(OrderRecord.venue_code). \
            order_by(desc(sort_dic[sort_by])). \
            limit(3).all()
        return [{"平台": _[0], "会员输赢": _[2], "投注": _[1], "有效投注": _[3], } for _ in data]

    @staticmethod
    def get_user_detail_login_log_vo(site_code, user_account):
        """
        会员详情 - 登录日志
        @param site_code:
        @param user_account:
        @return:
        """
        data = ms_context.get().session.query(UserLoginInfo). \
            filter(UserLoginInfo.user_account == user_account, UserLoginInfo.site_code == site_code). \
            order_by(UserLoginInfo.created_time.desc()).all()
        return [{"登录时间": DateUtil.timestamp_to_time(_.login_time),
                 "状态": Dao.get_user_login_status(_.login_type, True),
                 "ip地址": _.ip, "IP归属地": _.ip_address, "登录网址": _.login_address,
                 "登录终端": System.get_device(_.login_terminal, True),
                 "设备号": _.device_no, "设备版本": _.device_version} for _ in data]

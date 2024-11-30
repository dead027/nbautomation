#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/14 14:19

import time
import arrow
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.DateUtil import DateUtil
from Library.MysqlTableModel.medal_info_model import MedalInfo
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo
from Library.MysqlTableModel.medal_reward_record_model import MedalRewardRecord
from Library.MysqlTableModel.medal_reward_config_model import MedalRewardConfig
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Enum.MedalEnum import MedalEnum
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.SiteBackend.User import User, UserInfo
from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import Funds


class Medal(object):
    @staticmethod
    def get_medal_info(name=None, condition=None, status=None):
        """
        获取勋章信息
        @param condition:
        @param name:
        @param status:
        @return:
        """
        data = ms_context.get().session.query(MedalInfo)
        if condition:
            data = data.filter(MedalInfo.unlock_cond_name == condition)
        if name:
            data = data.filter(MedalInfo.medal_name == name)
        if status:
            data = data.filter(MedalInfo.status == MedalEnum.status_f_zh.value[status])
        return data.first()

    @staticmethod
    def get_medal_receive_data_base(site_code, start_diff, end_diff, stop_diff, date_type='日'):
        """
        获取勋章奖励记录中已领取数据
        :return: 按user_account,agent_account,currency_code,date分组
        """
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        _start, _end = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)

        data = ms_context.get().session. \
            query(MedalRewardRecord.user_account, MedalRewardRecord.super_agent_account,
                  func.date_format(func.convert_tz(func.from_unixtime(MedalRewardRecord.complete_time / 1000),
                                                   '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date"),
                  func.sum(MedalRewardRecord.reward_amount).label("amount")). \
            filter(MedalRewardRecord.site_code == site_code,
                   MedalRewardRecord.complete_time.between(_start, _end))
        return data.group_by("date", MedalRewardRecord.user_account, MedalRewardRecord.super_agent_account)

    @staticmethod
    def get_medal_reward_info(reward_id=None, site_code=None, unlock_num=None):
        """
        获取勋章奖励配置
        @param reward_id:
        @param site_code:
        @param unlock_num:
        @return:
        """
        data = ms_context.get().session.query(MedalRewardConfig)
        if reward_id:
            data = data.filter(MedalRewardConfig.id == reward_id)
        if site_code:
            data = data.filter(MedalRewardConfig.site_code == site_code)
        if unlock_num:
            data = data.filter(MedalRewardConfig.unlock_medal_num == unlock_num)
        return data.all()

    @staticmethod
    def cond_iron_fen(user_account):
        """
        铁粉，累计登录平台200天
        @param user_account:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("铁粉")
        ms: Session = ms_context.get().session
        data = ms.query(
            func.date_format(func.from_unixtime(UserLoginInfo.login_time / 1000), '%Y-%m-%d').label('date')). \
            filter(UserLoginInfo.user_account == user_account,
                   UserLoginInfo.login_type == System.get_user_login_status("成功")). \
            group_by(
            func.date_format(func.from_unixtime(UserLoginInfo.login_time / 1000), '%Y-%m-%d')).all()
        return True if len(data) >= int(medal_info.cond_num1) else False

    # @staticmethod
    # def cond_iron_fen(user_account, site_code):
    #     """
    #     铁粉，连续登录平台200天
    #     @param user_account:
    #     @param site_code:
    #     @return:
    #     """
    #     medal_info: MedalInfo = Medal.get_medal_info("铁粉")
    #     ms: Session = ms_context.get().session
    #     data = ms.query(func.max(UserLoginInfo.login_time),
    #                     func.date_format(func.from_unixtime(UserLoginInfo.login_time / 1000), '%Y-%m-%d').
    #                     label('date')).filter(UserLoginInfo.user_account == user_account,
    #                                           UserLoginInfo.login_type == System.get_user_login_status("成功"),
    #                                           UserLoginInfo.site_code == site_code). \
    #         group_by(func.date_format(func.from_unixtime(UserLoginInfo.login_time / 1000), '%Y-%m-%d')).all()
    #     continuous_list = []
    #     for item in data:
    #         if not continuous_list:
    #             continuous_list.append(item[0])
    #             if medal_info.cond_num1 <= 1:
    #                 return True
    #         else:
    #             next_day_str = DateUtil.timestamp_to_date(item[0])
    #             next_day_str_expect = DateUtil.timestamp_to_date(continuous_list[-1], day_diff=1)
    #             if next_day_str == next_day_str_expect:
    #                 continuous_list.append(item[0])
    #                 if len(continuous_list) >= medal_info.cond_num1:
    #                     return True
    #             else:
    #                 continuous_list = []
    #     return False

    @staticmethod
    def cond_2(user_account, site_code):
        """
        体育达人,累计登录总天数 n天
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("体育达人")
        ms: Session = ms_context.get().session
        data = ms.query(
            func.date_format(func.from_unixtime(UserLoginInfo.login_time / 1000), '%Y-%m-%d').label('date')).\
            filter(UserLoginInfo.user_account == user_account,
                   UserLoginInfo.login_type == System.get_user_login_status("成功"),
                   UserLoginInfo.site_code == site_code). \
            group_by(func.date_format(func.from_unixtime(UserLoginInfo.login_time / 1000), '%Y-%m-%d')).all()
        return True if len(data) >= medal_info.cond_num1 else False

    @staticmethod
    def get_lose_max(month_diff=0):
        """
        获取指定月负盈利最多的值
        @param month_diff:
        @return:
        """
        start_timestamp, end_timestamp = DateUtil.get_timestamp_range(month_diff, month_diff, date_type='月')
        ms: Session = ms_context.get().session
        data = ms.query(OrderRecord.user_account, func.sum(OrderRecord.win_loss_amount).label('value')). \
            filter(OrderRecord.settle_time.between(start_timestamp, end_timestamp)). \
            group_by(OrderRecord.user_account).order_by(desc("value")).first()
        return 0 if not data or data[0][1] > 0 else data[0][1]

    @staticmethod
    def cond_loser_no_1(user_account):
        """
        孤勇者,任意单个自然月全平台负盈利最多的一个人
        @param user_account:
        @return:
        """
        ms: Session = ms_context.get().session
        data = ms.query(OrderRecord.user_account, func.date_format(
            func.from_unixtime(OrderRecord.settle_time / 1000), '%Y-%m').label('date'),
                        func.sum(OrderRecord.win_loss_amount).label('value')). \
            group_by('date', OrderRecord.user_account). \
            subquery()
        data = ms.query(data.c.user_account, data.c.value, data.c.date,
                        func.row_number().over(partition_by=['date'], order_by=data.c.value.desc()).label('index')). \
            subquery()
        data = ms.query(data).filter(data.c.index == 1).all()
        user_list = set([_[0] for _ in data])
        return True if user_account in user_list else False

    @staticmethod
    def get_valid_amount_max(month_diff=0):
        """
        功勋卓著： 任意单个自然月全平台流水最多的值
        @param month_diff:
        @return:
        """
        ms: Session = ms_context.get().session
        start_timestamp, end_timestamp = DateUtil.get_timestamp_range(month_diff, month_diff, date_type='月')
        data = ms.query(OrderRecord.user_account, func.sum(OrderRecord.valid_amount).label('value')). \
            filter(OrderRecord.settle_time.between(start_timestamp, end_timestamp)). \
            group_by(OrderRecord.user_account).order_by(desc("value")).first()
        return 0 if not data or data[0][1] > 0 else data[0][1]

    @staticmethod
    def cond_valid_amount_max(user_account):
        """
        功勋卓著： 任意单个自然月全平台流水最多的一个人
        @param user_account:
        @return:
        """
        ms: Session = ms_context.get().session

        data = ms.query(OrderRecord.user_account, func.date_format(
            func.from_unixtime(OrderRecord.settle_time / 1000), '%Y-%m').label('date'),
                        func.sum(OrderRecord.valid_amount).label('value')). \
            group_by('date', OrderRecord.user_account). \
            subquery()
        data = ms.query(data.c.user_account, data.c.value, data.c.date,
                        func.row_number().over(partition_by=['date'], order_by=data.c.value.desc()).label('index')). \
            subquery()
        data = ms.query(data).filter(data.c.index == 1).all()
        user_list = set([_[0] for _ in data])
        return True if user_account in user_list else False

    @staticmethod
    def cond_call_me_rich_man(user_account, site_code):
        """
        叫我有钱人
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("叫我有钱人")
        data = ms_context.get().session.query(func.sum(OrderRecord.valid_amount)). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code).first()
        return True if data[0] >= medal_info.cond_num1 else False

    @staticmethod
    def cond_nb_boy(user_account, site_code):
        """
        小有所成
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("小有所成")
        data = ms_context.get().session.query(func.sum(OrderRecord.valid_amount)). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code).first()
        return True if data[0] >= medal_info.cond_num1 else False

    @staticmethod
    def cond_lucy_cat(user_account, site_code):
        """
        招财猫
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("招财猫")
        data = ms_context.get().session.query(func.sum(OrderRecord.win_loss_amount)). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code).first()
        return True if data[0] >= medal_info.cond_num1 else False

    @staticmethod
    def cond_old_brother(user_account, site_code):
        """
        老前辈
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("老前辈")
        expect_time = DateUtil.get_current_time("md").shift(years=-medal_info.cond_num1, days=1).strftime("%Y-%m-%d")
        data: UserInfo = User.get_user_info_sql(user_account, site_code=site_code)
        register_time = DateUtil.timestamp_to_date(data.created_time)
        return True if register_time < expect_time else False

    @staticmethod
    def foo():
        data = ms_context.get().session.query(UserInfo.area_code.label('code'), func.date_format(
            func.from_unixtime(UserInfo.register_time / 1000), '%Y-%m-%d').label('date'),
                                              func.sum(UserInfo.account_type).label('value')). \
            group_by('date', UserInfo.area_code). \
            subquery()
        data = ms_context.get().session.query(data.c.code, data.c.value, data.c.date,
                                              func.row_number().over(partition_by=['date'],
                                                                     order_by=data.c.value.desc()).label('index')). \
            subquery()
        data = ms_context.get().session.query(data).filter(data.c.index == 1)

        print(data.all())

    @staticmethod
    def cond_level_max(user_account, site_code):
        """
        独上高楼： 最高等级vip69
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("独上高楼")
        user_info: UserInfo = User.get_user_info_sql(user_account, site_code)
        return True if user_info.vip_grade_code >= medal_info.cond_num1 else False

    @staticmethod
    def cond_lucky_star(user_account, site_code):
        """
        无敌幸运星： 任意游戏单笔注单盈利99000以上
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("无敌幸运星")
        ms: Session = ms_context.get().session
        data = ms.query(OrderRecord).filter(OrderRecord.user_account == user_account,
                                            OrderRecord.site_code == site_code,
                                            OrderRecord.win_loss_amount >= medal_info.cond_num1)
        return True if data.all() else False

    @staticmethod
    def cond_bet_god(user_account, site_code):
        """
        赌神： 每日竞赛-真人排行连续三天排名均在前三 todo
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info("无敌幸运星")
        ms: Session = ms_context.get().session
        data = ms.query(OrderRecord).filter(OrderRecord.user_account == user_account,
                                            OrderRecord.site_code == site_code,
                                            OrderRecord.win_loss_amount >= medal_info.cond_num1)
        return True if data.all() else False

    @staticmethod
    def _cond_daily_man(user_account, site_code, medal_name):
        """
        体育健将,乐透大人
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info(medal_name)
        ms: Session = ms_context.get().session
        venue_type = System.get_venue_type('体育')
        data = ms.query(func.date_format(func.from_unixtime(OrderRecord.settle_time / 1000), '%Y-%m-%d').
                        label('date'),
                        func.sum(OrderRecord.valid_amount).label('value')). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code,
                   OrderRecord.game_type == venue_type). \
            group_by('date').having(func.sum(OrderRecord.valid_amount) >= 1000).all()

        date_list = []
        for item in data:
            if not date_list:
                date_list = [item[0]]
                continue
            tp = int(time.mktime(time.strptime(date_list[-1], "%Y-%m-%d"))) * 1000
            next_day = arrow.get(tp).to('Asia/Shanghai').shift(days=len(date_list)).strftime("%Y-%m-%d")
            if item[0] == next_day:
                date_list.append(item[0])
            else:
                date_list = [item[0]]
            return True if len(date_list) >= medal_info.cond_num1 else False

    @staticmethod
    def cond_sport_man(user_account, site_code):
        """
        体育健将： 体育场馆连续30自然日均有投注，单日流水1000以上
        @param user_account:
        @param site_code:
        @return:
        """
        return Medal._cond_daily_man(user_account, site_code, '运动健将')

    @staticmethod
    def cond_lottery_man(user_account, site_code):
        """
        乐透达人： 彩票场馆连续30自然日均有投注，单日流水1000以上
        @param user_account:
        @param site_code:
        @return:
        """
        return Medal._cond_daily_man(user_account, site_code, '乐透达人')

    @staticmethod
    def cond_universe_rich_man(user_account, site_code):
        """
        元宇宙大富翁：  任意单个自然月虚拟币充值排行第一
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def cond_task_master(user_account, site_code):
        """
        任务大师：任意单个自然周（周一-周日）完成全部每日任务
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def cond_recharge_top1_monthly(user_account, site_code):
        """
        富甲天下：任意单个自然月全平台累积充值金额（非虚拟币）最多的一个人
        @param user_account:
        @param site_code:
        @return:
        """
        medal_info: MedalInfo = Medal.get_medal_info(medal_name)
        ms: Session = ms_context.get().session
        venue_type = System.get_venue_type('体育')
        data = ms.query(func.date_format(func.from_unixtime(OrderRecord.settle_time / 1000), '%Y-%m-%d').
                        label('date'),
                        func.sum(OrderRecord.valid_amount).label('value')). \
            filter(OrderRecord.user_account == user_account, OrderRecord.site_code == site_code,
                   OrderRecord.game_type == venue_type). \
            group_by('date').having(func.sum(OrderRecord.valid_amount) >= 1000).all()

    @staticmethod
    def cond_big_boss(user_account, site_code):
        """
        大老板：任意单个自然月全平台累积提款金额最多的一个人
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def cond_invite_friend(user_account, site_code):
        """
        呼朋唤友：通过个人邀请好友链接邀请好友20人（好友需注册并有充值记录）
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def cond_esport_king(user_account, site_code):
        """
        电子霸王：每日竞赛（电子排行）连续三天排名均在前三
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def cond_roulette_star(user_account, site_code):
        """
        旋转之星：参与轮盘旋转总计200次
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def cond_rain_god(user_account, site_code):
        """
        雨神：参与官方的金币雨活动并收到金币雨99次
        @param user_account:
        @param site_code:
        @return:
        """
        pass

    @staticmethod
    def wait_until_has_medal(user_account, site_code, medal_name, timeout=5, err_msg=False):
        """
        等待会员获得勋章
        @param user_account:
        @param site_code:
        @param medal_name:
        @param timeout:
        @param err_msg: True 返回错误值 ｜ False 无返回
        @return: True | False
        """

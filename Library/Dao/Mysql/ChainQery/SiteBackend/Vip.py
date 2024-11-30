#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:06
import time
import math
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.user_information_change_model import UserInformationChange
from Library.MysqlTableModel.site_vip_benefit_model import SiteVipBenefit
from Library.MysqlTableModel.site_vip_change_record_model import SiteVipChangeRecord
from Library.MysqlTableModel.site_vip_grade_model import SiteVipGrade
from Library.MysqlTableModel.vip_grade_model import VipGrade
# from Library.MysqlTableModel.site_vip_operation import SiteVipOperation
from Library.MysqlTableModel.site_vip_rank_model import SiteVipRank
from Library.MysqlTableModel.site_vip_venue_exe_model import SiteVipVenueExe
from Library.MysqlTableModel.site_vip_rank_change_record_model import SiteVipRankChangeRecord
from Library.MysqlTableModel.site_vip_award_record_model import SiteVipAwardRecord
# from Library.MysqlTableModel.user_vip_flow_record_model import UserVipFlowRecord
from Library.MysqlTableModel.site_vip_rank_currency_config_model import SiteVipRankCurrencyConfig
from Library.Common.Utils.DateUtil import DateUtil
from sqlalchemy import or_, update
from sqlalchemy import func
from Library.Common.Enum.UserEnum import UserEnum
from sqlalchemy.orm import Session, session
from Library.Dao.Mysql.ChainQery.SiteBackend.User import User
from Library.Dao.Mysql.ChainQery.Order import Order
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site, SiteInfo
from Library.Dao.Mysql.ChainQery.MasterBackend.Game import Game, VenueInfo
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import Funds


class Vip(object):
    @staticmethod
    def get_vip_rank_config_sql(site_name="", site_code="", rank_code=None):
        """
        获取vip段位配置
        :param site_name:
        :param site_code:
        :param rank_code: 段位名称
        :return:
        """
        if site_name:
            site_code = Site.get_site_info_sql(site_name=site_name).site_name
        data = ms_context.get().session.query(SiteVipRank).filter(SiteVipRank.site_code == site_code)
        data_dic = {SiteVipRank.vip_rank_code: item for item in data.all()}
        return data_dic[rank_code] if rank_code else data_dic

    @staticmethod
    def get_vip_rank_of_level_dao(site_code, level):
        """
        通过vip等级获取对应段位
        @return:
        """
        rank_data = Vip.get_vip_rank_config_sql(site_code=site_code)
        rank_dic = {}
        for item in rank_data:
            item: SiteVipRank
            level_list = item.vip_grade_codes.splist(",")
            for _ in level_list:
                rank_dic[_] = item.vip_rank_code
        return rank_dic[level]

    @staticmethod
    def get_vip_upgrade_exp_config_sql(site_name="", site_code="", venue_type=None):
        """
        获取各场馆VIP经验获取倍率配置
        :param site_name:
        :param site_code:
        :param venue_type:
        :return:
        """
        if site_name:
            site_code = Site.get_site_info_sql(site_name=site_name).site_name
        data = ms_context.get().session.query(SiteVipVenueExe).filter(SiteVipVenueExe.site_code == site_code)
        if venue_type:
            data.filter(SiteVipVenueExe.venue_type == venue_type)
        return {_.venue_type: _ for _ in data.all()}

    @staticmethod
    def get_vip_level_config_sql(site_name="", site_code="", level_code=None):
        """
        获取vip等级配置
        :param site_name:
        :param site_code:
        :param level_code:
        :return:
        """
        if site_name:
            site_code = Site.get_site_info_sql(site_name=site_name).site_name
        data = ms_context.get().session.query(SiteVipGrade).filter(SiteVipGrade.site_code == site_code).\
            order_by(SiteVipGrade.vip_grade_code.desc())
        if level_code:
            data = data.filter(SiteVipGrade.vip_grade_code == level_code)
        data = data.order_by(SiteVipGrade.vip_grade_code.desc())
        # print(data)
        return {item.vip_grade_code: item for item in data}

    @staticmethod
    def get_grade_name_dic_dao(to_name=True):
        """
        获取等级与等级名称的映射
        @return:
        """
        data = ms_context.get().session.query(VipGrade).all()
        grade_dic = {_.vip_grade_code: _.vip_grade_name for _ in data}
        if not to_name:
            grade_dic = {_[1]: _[0] for _ in grade_dic.items()}
        return grade_dic


    @staticmethod
    def get_vip_profit_config_sql(site_name="", site_code="", level_code=None):
        """
        获取vip权益配置
        :param site_name:
        :param site_code:
        :param level_code:
        :return:
        """
        if site_name:
            site_code = Site.get_site_info_sql(site_name=site_name).site_name
        data = ms_context.get().session.query(SiteVipBenefit).filter(SiteVipBenefit.site_code == site_code)
        if level_code:
            data = data.filter(SiteVipBenefit.vip_grade_code == level_code)
        data = data.order_by(SiteVipGrade.vip_grade_code.desc())
        data_dic = {item.vip_grade_code: item for item in data}
        return data_dic

    @staticmethod
    def get_user_exp(site_code, user_account):
        """
        获取用户当前的经验值
        @return:
        """
        user_info: UserInfo = User.get_user_info_sql(site_code, user_account)[0][0]
        # 获取经验配置
        exp_data_dic = Vip.get_vip_upgrade_exp_config_sql(site_code=site_code)
        # 从注单获取用户当前流水
        valid_amount_data = Order.get_user_valid_amount(user_account, True)
        rate_dic = Funds.currency_rate(site_code)
        rate = rate_dic[user_info.main_currency]
        exp = 0
        # 遍历所有注单
        for item in valid_amount_data:
            venue_code, valid_amount = item
            # 转为平台币计数
            valid_amount = int(valid_amount * 100 / rate) / 100
            # 获取场馆分类
            venue_info: VenueInfo = Game.get_venue_info_sql(venue_code=venue_code)[0]
            # 获取场馆经验倍率
            exp_info: SiteVipVenueExe = exp_data_dic[str(venue_info.venue_type)]
            exp += float(exp_info.experience) * valid_amount
        return round(exp, 2)

    @staticmethod
    def get_level_up_required_exp(user_account, site_code, increase_level=1):
        """
        获取用户等级升级所需经验
        @return:
        """
        max_level = Vip.get_max_vip_grade(site_code)
        user_info: UserInfo = User.get_user_info_sql(site_code, user_account)[0][0]
        # 期望升级后的等级
        expect_level = user_info.vip_grade_code + int(increase_level) if max_level > increase_level else max_level
        # 当前经验
        exp_current = Vip.get_user_exp(site_code, user_account)
        # 获取到指定等级所需经验
        level_info: SiteVipGrade = Vip.get_vip_level_config_sql(site_code=site_code)[expect_level]
        left_amount = float(level_info.upgrade_xp) - exp_current
        return math.ceil(left_amount)  # 向上取整

    @staticmethod
    def get_rank_up_required_exp(user_account, site_code, increase_rank=1):
        """
        获取用户段位升级所需经验
        @param user_account:
        @param increase_rank:
        @param site_code:
        @return:
        """
        user_info: UserInfo = User.get_user_info_sql(user_account)
        expect_rank_code = user_info.vip_rank + int(increase_rank)
        # 获取到指定等级所需经验
        rank_info: SiteVipRank = Vip.get_vip_rank_config_sql(site_code=site_code, rank_code=expect_rank_code)
        level_min = rank_info.vip_grade_codes.split(",")[0]
        return Vip.get_level_up_required_exp(user_account, site_code, level_min - user_info.vip_grade_code)

    @staticmethod
    def get_level_up_required_valid_amount(user_account, site_code, venue_name='视界真人', increase_level=1):
        """
        获取用户升到指定等级在某场馆所需打码量
        @param user_account:
        @param increase_level: 目标等级
        @param venue_name:
        @param site_code:
        @return: 场馆所需打码量
        """
        # 获取经验配置
        exp_data_dic = Vip.get_vip_upgrade_exp_config_sql(site_code=site_code)
        venue_info: VenueInfo = Game.get_venue_info_sql(venue_name)[0]
        # 获取指定场馆的经验倍率
        exp_info: SiteVipVenueExe = exp_data_dic[str(venue_info.venue_type)]
        # 需要的经验
        exp_require = Vip.get_level_up_required_exp(user_account, site_code, increase_level)
        return math.ceil(exp_require / exp_info.experience)  # 向上取整

    @staticmethod
    def get_rank_up_required_valid_amount(user_account, site_code, venue_name='金喜真人', level=1):
        """
        获取用户段位升到指定段位，在某场馆所需打码量
        @param user_account:
        @param venue_name:
        @param site_code:
        @param level:
        @return: 场馆所需打码量
        """
        # 获取经验配置
        exp_data_dic = Vip.get_vip_upgrade_exp_config_sql(site_code=site_code)
        venue_info: VenueInfo = Game.get_venue_info_sql(venue_name)
        exp_info: SiteVipVenueExe = exp_data_dic[venue_info.venue_type]
        exp_require = Vip.get_level_up_required_valid_amount(user_account, site_code, venue_name, level)
        return math.ceil(exp_require / exp_info.experience)  # 向上取整

    @staticmethod
    def get_vip_rank_change_info_sql(user_account="", site_name="", site_code="", if_latest=False):
        """
        获取VIP段位变更记录
        :param user_account:
        :param site_name:
        :param site_code:
        :param if_latest:
        :return:
        """
        if site_name:
            site_code = Site.get_site_info_sql(site_name=site_name).site_name
        change_info = ms_context.get().session.query(SiteVipRankChangeRecord)
        if user_account:
            change_info = change_info.filter(SiteVipRankChangeRecord.user_account == user_account)
        if site_code:
            change_info = change_info.filter(SiteVipRankChangeRecord.site_code == site_code)
        change_info = change_info.order_by(SiteVipChangeRecord.created_time.desc())
        return change_info.all() if not if_latest else change_info.first()

    @staticmethod
    def get_vip_change_info_sql(user_account="", site_name="", site_code="", if_latest=False):
        """
        获取VIP变更记录
        :param user_account:
        :param site_name:
        :param site_code:
        :param if_latest:
        :return:
        """
        if site_name:
            site_code = Site.get_site_info_sql(site_name=site_name).site_name
        change_info = ms_context.get().session.query(SiteVipChangeRecord)
        if user_account:
            change_info = change_info.filter(SiteVipChangeRecord.user_account == user_account)
        if site_code:
            change_info = change_info.filter(SiteVipChangeRecord.site_code == site_code)
        change_info = change_info.order_by(SiteVipChangeRecord.created_time.desc())
        return change_info.all() if not if_latest else change_info.first()

    @staticmethod
    def get_user_latest_level_up_record(user_account, site_code):
        """
        获取用户最新升降级记录, user_vip_flow_record表
        @param user_account:
        @param site_code:
        @return:
        """
        data: SiteVipChangeRecord = ms_context.get().session.query(SiteVipChangeRecord).filter(
            SiteVipChangeRecord.user_account == user_account, SiteVipChangeRecord.site_code == site_code).\
            order_by(SiteVipChangeRecord.created_time.desc()).first()
        return data

    @staticmethod
    def modify_latest_level_change_record(user_account, site_code, operation_type, update_time_diff=-1):
        """
        将用户升级记录表中最后一条的时间往前调，便于用户升级定时任务的执行, 基于只能升级是可以的，如果还能降级就要考虑多条数据了
        @param user_account:
        @param site_code:
        @param operation_type: 段位 ｜ 等级
        @param update_time_diff: 修改后的该VIP等级的更新时间
        @return:
        """
        session_obj: session = ms_context.get().session
        value_dic = {"updated_time": DateUtil.get_timestamp_by_now(update_time_diff) * 1000}
        sql = update(SiteVipChangeRecord).where(
            SiteVipChangeRecord.user_account == user_account,
            SiteVipChangeRecord.site_code == site_code,
            SiteVipChangeRecord.operation_type == 0 if operation_type == '段位' else 1,
            SiteVipChangeRecord.created_time == func.max(SiteVipChangeRecord.created_time)).values(value_dic)
        session_obj.execute(sql)
        session_obj.commit()

    # @staticmethod
    # def modify_rank_change_record(register_info, status="升级", vip_rank_code=None, to_status=None,
    #                               valid_sum_amount=None, update_time_diff=None, modify_all="否"):
    #     """
    #     修改用户升级记录表, user_vip_flow_record表  -- 注意，请先本等级投注一次    基于只能升级是可以的，如果还能降级就要考虑多条数据了
    #     @param register_info:
    #     @param status: 要修改的记录类型，升级 | 降级 | 保级
    #     @param vip_rank_code: 修改后的等级数字
    #     @param to_status: 修改后的记录类型，None ｜ 升级 | 降级 | 保级
    #     @param valid_sum_amount: 修改后的总有效投注金额
    #     @param update_time_diff: 修改后的该VIP等级的更新时间
    #     @param modify_all: 是否修改所有
    #     @return:
    #     """
    #     user_info: UserInfo = User.get_user_info_sql(register_info)
    #     value_dic = {}
    #     session_obj: session = ms_context.get().session
    #     if vip_rank_code:
    #         value_dic['vip_rank_code'] = vip_rank_code
    #     if to_status:
    #         value_dic['status'] = UserEnum.vip_status_dic_f_zh.value[to_status]
    #     if valid_sum_amount:
    #         value_dic['valid_sum_amount'] = valid_sum_amount
    #     if update_time_diff:
    #         value_dic['updated_time'] = DateUtil.get_timestamp_by_now(update_time_diff) * 1000
    #     if modify_all == '否':
    #         sql = update(UserVipFlowRecord).where(
    #             UserVipFlowRecord.user_account == user_info.user_account,
    #             UserVipFlowRecord.vip_rank_code == user_info.vip_rank_code,
    #             UserVipFlowRecord.status == UserEnum.vip_status_dic_f_zh.value[status]).values(value_dic)
    #     else:
    #         sql = update(UserVipFlowRecord).where(
    #             UserVipFlowRecord.user_account == user_info.user_account,
    #             UserVipFlowRecord.status == UserEnum.vip_status_dic_f_zh.value[status]).values(value_dic)
    #     session_obj.execute(sql)
    #     session_obj.commit()

    # @staticmethod
    # def modify_change_info(user_account, site_code, rank_after, change_time_diff=-1):
    #     """
    #     修改用户升级记录表, vip_change_info 表  基于只能升级是可以的，如果还能降级就要考虑多条数据了
    #     @param user_account:
    #     @param site_code:
    #     @param rank_after: 修改后的等级数字, 搜索条件之一
    #     @param change_time_diff: 修改后的该VIP等级的更新时间
    #     @return:
    #     """
    #     user_info: UserInfo = User.get_user_info_sql(user_account, site_code=site_code)
    #     value_dic = {"change_after": rank_after}
    #     session_obj: session = ms_context.get().session
    #     value_dic['change_time'] = DateUtil.get_timestamp_by_now(change_time_diff) * 1000
    #     sql = update(VipChangeInfo).where(
    #         VipChangeInfo.user_account == user_info.user_account,
    #         VipChangeInfo.change_after == rank_after).values(value_dic)
    #     session_obj.execute(sql)
    #     session_obj.commit()

    @staticmethod
    def get_max_vip_rank(site_code):
        """
        获取VIP最大段位
        @return:
        """
        data = ms_context.get().session.query(func.max(SiteVipRank.vip_rank_code)).\
            filter(SiteVipRank.site_code == site_code).first()
        return data[0]

    @staticmethod
    def get_max_vip_grade(site_code):
        """
        获取VIP最大等级
        @return:
        """
        data = ms_context.get().session.query(func.max(SiteVipGrade.vip_grade_code)). \
            filter(SiteVipGrade.site_code == site_code).first()
        return data[0]

    @staticmethod
    def get_site_vip_profit_list_sql(site_name="", site_code="", level_code=""):
        """
        获取vip权益配置
        :return:
        """
        data = Vip.get_vip_profit_config_sql(site_name, site_code, level_code)
        result_list = []
        for item in data.values():
            item: SiteVipBenefit
            value_dic = {"VIP等级": item.vip_grade_code, "单日提现次数": item.daily_withdrawals,
                         "单日提款上限": item.day_withdraw_limit, "周奖励最低流水": item.week_min_bet_amount,
                         "周返奖比例": item.week_rebate, "周流水倍数": item.week_bet_multiple,
                         "月奖励最低流水": item.month_min_bet_amount, "月返奖比例": item.month_rebate,
                         "月流水倍数": item.month_bet_multiple, "周体育最低流水": item.week_sport_min_bet,
                         "周体育流水倍数": item.week_bet_multiple, "周体育奖金": item.week_sport_rebate,
                         "转盘次数": item.luck_time, "晋级奖金": item.upgrade, "提款手续费": item.withdraw_fee}
            result_list.append(value_dic)

    @staticmethod
    def get_site_vip_grade_list_sql(site_name="", site_code="", vip_code=""):
        """
        获取vip等级配置
        :return:
        """
        data = Vip.get_vip_level_config_sql(site_name, site_code, vip_code)
        result_list = []
        for item in data:
            item: SiteVipGrade
            value_dic = {"VIP等级": item.vip_grade_code, "所属段位": item.vip_rank_code,
                         "前端显示名称": item.vip_grade_name, "升级条件所需XP": item.upgrade_experience}
            result_list.append(value_dic)

    @staticmethod
    def get_site_vip_rank_sql(site_code=None, rank_name=""):
        """
        获取vip段位配置
        :param site_code:
        :param rank_name:
        :return:
        """
        data = ms_context.get().session.query(SiteVipRank)
        if rank_name:
            data = data.filter(SiteVipRank.vip_rank_name == rank_name)
        if site_code:
            data = data.filter(SiteVipRank.site_code == site_code)
        return data.all()

    @staticmethod
    def get_site_vip_change_record_sql(start_diff, end_diff, change_type=None, user_account=None, operator=None):
        """
        获取vip变更记录
        @param start_diff:
        @param end_diff:
        @param change_type:
        @param user_account:
        @param operator:
        @return:
        """
        update_start, update_end = DateUtil.get_timestamp_range(start_diff, end_diff, date_type='日')
        data = ms_context.get().session.query(SiteVipChangeRecord).\
            filter(SiteVipChangeRecord.updated_time.between(update_start, update_end))
        if change_type:
            data = data.filter(SiteVipChangeRecord.change_type ==
                               UserEnum.vip_level_change_status_f_zh.value[change_type])
        if user_account:
            data = data.filter(SiteVipChangeRecord.user_account == user_account)
        if operator:
            data = data.filter(SiteVipChangeRecord.operator == operator)
        return data.all()

    @staticmethod
    def wait_until_user_vip_level_changed_sql(user_account, site_code, level, timeout=10):
        """
        等待会员vip等级变为指定值
        @param user_account:
        @param site_code:
        @param level: VIP等级
        @param timeout: 超时时间
        @return:
        """
        session_obj: session = ms_context.get().session
        start_time = time.time()
        while time.time() - start_time < timeout:
            data = session_obj.query(UserInfo).filter(UserInfo.user_account == user_account,
                                                      UserInfo.site_code == site_code,
                                                      UserInfo.vip_grade_code == int(level))
            if list(data):
                return
            time.sleep(0.2)
        raise AssertionError(f"超过{timeout}秒，会员vip等级未变为指定值")

    @staticmethod
    def get_vip_rank_currency_config_sql(site_code):
        """
        获取VIP段位提款配置
        @return:
        """
        data = ms_context.get().session.query(SiteVipRankCurrencyConfig). \
            filter(SiteVipRankCurrencyConfig.site_code == site_code).all()
        return {int(_.vip_rank_code): _ for _ in data}

    @staticmethod
    def get_vip_award_record_base(site_code, start_diff=None, end_diff=None, vip_grade=None, stop_diff=0,
                                  date_type='日', receive_start_diff=None, receive_end_diff=None, award_type=None):
        """
        获取VIP奖励记录
        :param award_type: 升级礼金 ｜ 周流水 ｜ 月流水 ｜ 周体育流水
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        data = ms_context.get().session.query(SiteVipAwardRecord).\
            filter(SiteVipAwardRecord.site_code == site_code, )

        if start_diff or start_diff == 0:
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            data = data.filter(SiteVipAwardRecord.created_time.between(start_time, end_time))
        if receive_start_diff or receive_start_diff == 0:
            start_time, end_time = DateUtil.get_timestamp_range(receive_start_diff, receive_end_diff,
                                                                stop_diff, date_type, timezone)
            data = data.filter(SiteVipAwardRecord.receive_time.between(start_time, end_time))
        if vip_grade:
            data = data.filter(SiteVipAwardRecord.vip_grade_code == vip_grade)
        if award_type:
            data = data.filter(SiteVipAwardRecord.award_type == UserEnum.vip_award_type_dic_f_zh[award_type])
        return data

    @staticmethod
    def get_user_vip_level_change_sql(start_diff,end_diff,user_id,updater):
        """
        获取用户VIP等级变更记录
        @param start_diff:
        @param end_diff:
        @param user_id:
        @param updater:
        @return:
        """
        update_start, update_end = DateUtil.get_timestamp_range(start_diff, end_diff)
        data = ms_context.get().session.query(SiteVipRankChangeRecord).filter(
            SiteVipRankChangeRecord.change_time.between(update_start,update_end),
            SiteVipRankChangeRecord.user_id == user_id,
            SiteVipRankChangeRecord.updater == updater
        ).first()
        return data

    @staticmethod
    def get_user_vip_rank_change_sql(start_diff, end_diff, user_id, updater):
        """
        获取用户VIP段位变更记录
        @param start_diff:
        @param end_diff:
        @param user_id:
        @param updater:
        @return:
        """
        update_start, update_end = DateUtil.get_timestamp_range(start_diff, end_diff)
        data = ms_context.get().session.query(SiteVipRank).filter(
            SiteVipRank.updated_time.between(update_start,end_diff),
            SiteVipRank.id == user_id,
            SiteVipRank.updater == updater
        ).first()
        return data

    # @staticmethod
    # def get_vip_level_config_sql():
    #     """
    #     获取VIP等级配置
    #     @return:
    #     """
    #     data = ms_context.get().session.query(SiteVipGrade).filter(
    #         SiteVipGrade.vip_grade_name,
    #         SiteVipGrade.vip_rank_code,
    #         SiteVipGrade.upgrade_bonus,
    #         SiteVipGrade.upgrade_xp
    #     ).first()
    #     return data

    @staticmethod
    def get_user_vip_rank_config_sql(site_code):
        """
        获取VIP段位配置
        @return:
        """
        data = ms_context.get().session.query(SiteVipRank, SiteVipRankCurrencyConfig).\
            join(SiteVipRankCurrencyConfig, SiteVipRank.vip_rank_code == SiteVipRankCurrencyConfig.vip_rank_code).\
            filter(SiteVipRank.site_code == site_code, SiteVipRankCurrencyConfig.site_code == site_code)
        return data.all()

    @staticmethod
    def get_vip_data_reports_sql(start_diff, end_diff, user_id, updater):
        """
        获取用户VIP段位变更记录
        @param start_diff:
        @param end_diff:
        @param user_id:
        @param updater:
        @return:
        """
        update_start, update_end = DateUtil.get_timestamp_range(start_diff, end_diff)
        data = ms_context.get().session.query(SiteVipRank).filter(
            SiteVipRank.updated_time.between(update_start,end_diff),
            SiteVipRank.id == user_id,
            SiteVipRank.updater == updater
        ).first()
        return data


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 23:06
import time
import arrow
from collections import defaultdict

from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.user_info_model import UserInfo
from Library.MysqlTableModel.user_information_change_model import UserInformationChange
from Library.MysqlTableModel.user_account_update_review_model import UserAccountUpdateReview
from Library.MysqlTableModel.user_registration_info_model import UserRegistrationInfo
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.MysqlTableModel.casino_member_model import CasinoMember
from Library.MysqlTableModel.user_review_model import UserReview
from Library.MysqlTableModel.user_login_info_model import UserLoginInfo

from Library.Common.Utils.DateUtil import DateUtil
from sqlalchemy.orm import session
from sqlalchemy import and_, func
from Library.Common.Enum.UserEnum import UserEnum
from Library.Dao.Mysql.ChainQery.SiteBackend.Funds import UserCoin
from Library.Dao.Mysql.ChainQery.System import System
from Library.Dao.Mysql.ChainQery.SiteBackend.Agent import Agent
from Library.Dao.Mysql.ChainQery.MasterBackend.Site import Site
from Library.Dao.Mysql.ChainQery.MasterBackend.Game import Game, GameInfo


class User(object):
    @staticmethod
    def wait_until_user_exists_sql(register_info, timeout=5):
        """
        等待会员账号生成
        @param register_info:
        @param timeout:
        @return:
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            data = ms_context.get().session.query(UserInfo).filter(UserInfo.user_register == register_info)
            if list(data):
                return
            time.sleep(0.2)
        raise AssertionError(f"在{timeout}秒内会员{register_info}未生成")

    @staticmethod
    def get_users_of_agent(site_code, if_new=False, date_type="月", date_diff=0, stop_diff=0):
        """
        获取代理下的所有会员
        :param site_code:
        :param if_new: 是否筛选新注册用户
        :param date_type:
        :param date_diff:
        :param stop_diff: 若统计本月，指定截止日期
        :return: {agent_account: {"团队包括自己", "团队不包括自己", "非直属", "直属"}}
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        data_dic = defaultdict(dict)
        # 生成代理id与account\path的映射表
        agent_dic = {_.id: (_.agent_account, _.path.split(",")) for _ in agent_data}
        for _ in agent_dic.values():
            data_dic[_[0]] = defaultdict(list)

        data = ms_context.get().session.query(UserInfo).filter(UserInfo.site_code == site_code)
        if if_new:
            start_timestamp, end_timestamp = DateUtil.get_timestamp_range(date_diff, date_diff, stop_diff, date_type,
                                                                          timezone)
            data = data.filter(UserInfo.register_time.between(start_timestamp, end_timestamp))
        for item in data.all():
            item: UserInfo
            agent_path = agent_dic[item.super_agent_id][1]
            value = item.user_account
            if len(agent_path) == 3:
                data_dic[agent_dic[agent_path[0]]]["团队包括自己"].append(value)
                data_dic[agent_dic[agent_path[0]]]["团队不包括自己"].append(value)
                data_dic[agent_dic[agent_path[0]]]["非直属"].append(value)
                data_dic[agent_dic[agent_path[1]]]["团队包括自己"].append(value)
                data_dic[agent_dic[agent_path[1]]]["团队不包括自己"].append(value)
                data_dic[agent_dic[agent_path[1]]]["直属"].append(value)
                data_dic[agent_dic[agent_path[2]]]["团队包括自己"].append(value)
            elif len(agent_path) == 2:
                data_dic[agent_dic[agent_path[0]]]["团队包括自己"].append(value)
                data_dic[agent_dic[agent_path[0]]]["团队不包括自己"].append(value)
                data_dic[agent_dic[agent_path[0]]]["直属"].append(value)
                data_dic[agent_dic[agent_path[1]]]["团队包括自己"].append(value)
            elif len(agent_path) == 1:
                data_dic[agent_dic[agent_path[0]]]["团队包括自己"].append(value)

        return data_dic

    @staticmethod
    def get_new_register_user_amount(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取新注册玩家数量
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        data_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.id: (_.agent_account, _.path.split(",")) for _ in agent_data}
        # 获取所有会员信息
        start_timestamp, end_timestamp = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type,
                                                                      timezone=timezone)
        user_data = ms_context.get().session.query(UserInfo). \
            filter(UserInfo.site_code == site_code, UserInfo.register_time.between(start_timestamp, end_timestamp))
        # 找到会员的代理，通过path给所有代理增加数据
        for data in user_data:
            data: UserInfo
            agent_path = agent_dic[data.super_agent_id][1]
            for agent_id in agent_path:
                data_dic[agent_dic[agent_id][0]] += 1
        return data_dic

    @staticmethod
    def get_user_info_sql(site_code=None, user_account=None, user_id=None, account_type=None, status=None,
                          register_ip=None, login_ip=None, vip_rank=None, vip_level=None,
                          register_client=None, parent_agent=None, user_tag=None, register_start_diff=None,
                          register_end_diff=None, main_currency=None):
        """
        获取会员信息
        @return: [(userInfoStruct, validAmount),....]
        """
        timezone = Site.get_site_timezone(site_code)
        if register_start_diff or register_end_diff:
            register_start, register_end = DateUtil.get_timestamp_range(register_start_diff, register_end_diff,
                                                                        date_type='日', timezone=timezone)
        else:
            register_start = register_end = None
        data = ms_context.get().session.query(UserInfo, UserCoin.available_amount). \
            outerjoin(UserCoin, and_(UserInfo.user_account == UserCoin.user_account,
                                     UserInfo.site_code == UserCoin.site_code))
        user_account_status_dic = System.get_user_account_status()
        account_type_dic = System.get_user_account_type()
        currency_dic = System.get_currency_dic()
        if register_start:
            data = data.filter(UserInfo.register_time >= register_start)
        if register_end:
            data = data.filter(UserInfo.register_time >= register_end)
        if site_code:
            data = data.filter(UserInfo.site_code == site_code)
        if account_type:
            data = data.filter(UserInfo.account_type == account_type_dic[account_type])
        if user_id:
            data = data.filter(UserInfo.user_id == user_id)
        if user_account:
            data = data.filter(UserInfo.user_account == user_account)
        if parent_agent:
            data = data.filter(UserInfo.super_agent_account == parent_agent)
        if register_ip:
            data = data.filter(UserInfo.register_ip == register_ip)
        if login_ip:
            data = data.filter(UserInfo.last_login_ip == login_ip)
        if vip_rank:
            data = data.filter(UserInfo.vip_rank == vip_rank)
        if status:
            data = data.filter(UserInfo.account_status.in_([user_account_status_dic[_] for _ in status.split(",")]))
        if register_client:
            data = data.filter(UserInfo.registry == register_client)
        if user_tag:
            data = data.filter(UserInfo.user_label_id == user_tag)
        if vip_level:
            data = data.filter(UserInfo.vip_grade_code == vip_level)
        if main_currency:
            data = data.filter(UserInfo.main_currency == currency_dic[main_currency])
        return data.all()

    # @staticmethod
    # def get_user_list_sql(register_info="", user_id="", site_name=None, account_type=None, status=None,
    #                       ip_type=None, ip=None, vip_type=None, vip_level=None, register_client=None,
    #                       parent_agent="", user_tag="", register_start_diff=None, register_end_diff=None):
    #     from Library.Dao.Mysql.ChainQery.SiteBackend.UserLabel import UserLabel
    #
    #     result = User.get_user_info_sql(register_info, user_id, site_name, account_type, status, ip_type, ip,
    #                                     vip_type, vip_level, register_client, parent_agent, user_tag,
    #                                     register_start_diff, register_end_diff)
    #     result_list = []
    #     label_list = UserLabel.get_user_label_info()
    #     label_dic = {str(_["label_id"]): _["label_name"] for _ in label_list}
    #     for user_info, balance in result:
    #         user_info: UserInfo
    #         sub_data = {"注册时间": DateUtil.timestamp_to_time(user_info.register_time),
    #                     "站点编号/名称": user_info.site_code, "会员ID": user_info.user_id,
    #                     "会员账号": user_info.user_account,
    #                     "账号类型": UserEnum.account_type_dic_t_zh.value[user_info.account_type],
    #                     "主币种": user_info.main_currency, "钱包余额": balance, "VIP段位": user_info.vip_rank,
    #                     "VIP等级": user_info.vip_grade_code,
    #                     "标签": ",".join([label_dic[_] for _ in
    #                                     user_info.user_label_id.split(",")]) if user_info.user_label_id else "",
    #                     "上级代理": user_info.super_agent_account,
    #                     "账号状态": UserEnum.user_status_dic_t_zh.value[user_info.account_status],
    #                     "在线状态": 1, "首存金额": user_info.first_deposit_amount}
    #         result_list.append(sub_data)
    #     return result_list

    @staticmethod
    def get_new_user_audit_list_data(site_code, apply_start_diff=0, apply_end_diff=0, audit_start_diff=None,
                                     audit_end_diff=None, audit_status=None, lock_status=None, audit_operate=None,
                                     apply_account=None, audit_account=None, user_account=None, stop_diff=0,
                                     date_type='日'):
        """
        获取新增会员审核列表
        @param apply_start_diff:
        @param apply_end_diff:
        @param audit_start_diff:
        @param audit_end_diff:
        @param audit_status: 待处理 ｜ 处理中 ｜ 审核通过 ｜ 一审拒绝
        @param lock_status: 未锁 ｜ 已锁
        @param audit_operate:  一审审核 ｜ 结单查看
        @param apply_account:
        @param audit_account:
        @param user_account:
        @param site_code:
        @param stop_diff:
        @param date_type:
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(apply_start_diff, apply_end_diff, stop_diff, date_type,
                                                            timezone)
        data = ms_context.get().session.query(UserReview).filter(UserReview.apply_time.between(start_time, end_time),
                                                                 UserReview.site_code == site_code)
        if audit_start_diff:
            start_time, end_time = DateUtil.get_timestamp_range(audit_start_diff, audit_end_diff, stop_diff, date_type,
                                                                site_code)
            data = data.filter(UserReview.one_review_finish_time.between(start_time, end_time))
        if audit_status:
            data = data.filter(
                UserReview.review_status in [System.get_review_status(_) for _ in audit_status.split(",")])
        if lock_status:
            data = data.filter(UserReview.lock_status == UserEnum.lock_status_dic_f_zh[lock_status])
        if audit_operate:
            data = data.filter(UserReview.review_operation == UserEnum.audit_operation_dic_f_zh[audit_operate])
        if apply_account:
            data = data.filter(UserReview.applicant == apply_account)
        if audit_account:
            data = data.filter(UserReview.reviewer == audit_account)
        if user_account:
            data = data.filter(UserReview.user_account == user_account)
        return data.all()

    @staticmethod
    def wait_has_new_user_audit_order(user_account, timeout=4):
        """
        等待新注册会员的审核订单生成，返回订单id
        :param user_account:
        :param timeout: 超时时间
        :return:
        """
        start_time = int(time.time())
        diff = 0
        while diff <= timeout:
            resp = ms_context.get().session.query(UserReview).filter(UserReview.user_account == str(user_account),
                                                                     UserReview.review_status == 1). \
                first()
            if resp:
                return resp.id
            else:
                time.sleep(0.5)
                stop_time = int(time.time())
                diff = stop_time - start_time
        raise AssertionError("等待审核订单生成-超时")

    # @staticmethod
    # def get_user_label_record_sql(start_update_time_diff=-1, stop_update_time_diff=0, user_id="", operator=""):
    #     update_start, update_end = DateUtil.get_timestamp_range(start_update_time_diff, stop_update_time_diff,
    #                                                             date_type='日')
    #     rsp = ms_context.get().session.query(UserLabelRecord).filter(UserLabelRecord.updated_time.between(update_start,
    #                                                                                                       update_end))
    #
    #     if user_id:
    #         rsp = rsp.filter(UserLabelRecord.member_account == user_id)
    #     if start_update_time_diff:
    #         start_time, end_time = DateUtil.get_timestamp_range(start_update_time_diff, stop_update_time_diff,
    #                                                             date_type='日')
    #         rsp = rsp.filter(UserLabelRecord.updated_time.between(start_time, end_time))
    #     if operator:
    #         rsp.filter(UserLabelRecord.operator == operator)
    #
    #     result = rsp.all()
    #     result_list = []
    #     for item in result:
    #         sub_data = {"变更时间": item.updated_time, "变更前": item.before_change, "变更后": item.after_change,
    #                     "会员ID": item.member_account, "账号类型": item.account_type, "风控层级": item.risk_control_level,
    #                     "账号状态": item.account_status, "操作人": item.operator}
    #         result_list.append(sub_data)
    #     return result_list

    @staticmethod
    def get_registration_info_sql(site_code, user_id="", account_type="", register_client="", parent_agent="",
                                  register_ip="", ip_attribution="", register_info="", register_start_diff=-7,
                                  register_end_diff=0, currency=None, grep_has_agent=False):
        timezone = Site.get_site_timezone(site_code)
        timezone_sql = Site.get_site_timezone_for_sql(site_code)
        update_start, update_end = DateUtil.get_timestamp_range(register_start_diff, register_end_diff,
                                                                date_type='日', timezone=timezone)
        rsp = ms_context.get().session.query(UserRegistrationInfo,
                                             func.date_format(func.convert_tz(
                                                 func.from_unixtime(UserRegistrationInfo.registration_time / 1000),
                                                 '+00:00', f'{timezone_sql}:00'), '%Y-%m-%d').label("date")).\
            filter(UserRegistrationInfo.site_code == site_code)
        if user_id:
            rsp = rsp.filter(UserRegistrationInfo.member_id == user_id)
        if account_type:
            rsp = rsp.filter(UserRegistrationInfo.member_type.in_([System.get_user_account_type()[item]
                                                                   for item in account_type.split(",")]))
        if register_start_diff and register_end_diff:
            rsp = rsp.filter(UserRegistrationInfo.updated_time.between(update_start, update_end))
        if register_client:
            rsp = rsp.filter(UserRegistrationInfo.register_terminal == register_client)
        if parent_agent:
            rsp = rsp.filter(UserRegistrationInfo.superior_agent == parent_agent)
        if register_ip:
            rsp = rsp.filter(UserRegistrationInfo.register_ip == register_ip)
        if ip_attribution:
            rsp = rsp.filter(UserRegistrationInfo.ip_attribution == ip_attribution)
        if register_info:
            rsp = rsp.filter(UserRegistrationInfo.member_account == register_info)
        if currency:
            rsp = rsp.filter(UserRegistrationInfo.main_currency == currency)
        if grep_has_agent:
            rsp = rsp.filter(UserRegistrationInfo.superior_agent.is_not(None))
        return rsp

    @staticmethod
    def get_user_login_record_sql(user_id="", account_type="", login_type="", login_ip="",
                                  ip_address="", login_client="", device_no="", login_start_diff=-1, login_end_diff=0):
        login_start, login_end = DateUtil.get_timestamp_range(login_start_diff, login_end_diff,
                                                              date_type='日')
        rsp = ms_context.get().session.query(UserLoginInfo).filter(
            UserLoginInfo.login_time.between(login_start, login_end))

        if user_id:
            rsp = rsp.filter(UserLoginInfo.user_account == user_id)
        if account_type:
            rsp = rsp.filter(UserLoginInfo.member_type.in_([UserEnum.account_type_dic_f_zh.value[item]
                                                            for item in account_type.split(",")]))
        # if login_start_diff and login_end_diff:
        #     rsp = rsp.filter(UserLoginInfo.login_time.between(login_start, login_end))
        if login_type:
            rsp = rsp.filter(UserLoginInfo.login_type.in_([UserEnum.login_type_dic_f_zh.value[item]
                                                           for item in login_type.split(",")]))
        if login_ip:
            rsp = rsp.filter(UserLoginInfo.ip == login_ip)
        if ip_address:
            rsp = rsp.filter(UserLoginInfo.ip_address == ip_address)
        if login_client:
            rsp = rsp.filter(UserLoginInfo.login_terminal == login_client)
        if device_no:
            rsp = rsp.filter(UserLoginInfo.device_no == device_no)

        result = rsp.all()
        result_list = []
        for item in result:
            sub_data = {"登录时间": item.login_time, "登录状态": item.login_type, "会员ID": item.user_account,
                        "账号类型": item.account_type, "登录IP风控层级": item.ip,
                        "IP归属地": item.ip_address, "登录终端": item.login_terminal,
                        "终端设备号风控层级": item.device_no, "登录地址": item.login_address, "设备版本": item.device_version,
                        "备注": item.remark}
            result_list.append(sub_data)
        return result_list

    # @staticmethod
    # def get_user_label_config_list_sql(label_name="", creator_name=""):
    #     """
    #     获取标签配置list
    #     :param label_name 标签名称
    #     :param creator_name
    #     :return:
    #     """
    #     rsp = ms_context.get().session.query(UserLabelConfig)
    #     if label_name:
    #         rsp = rsp.filter(UserLabelConfig.label_name == label_name)
    #
    #     if creator_name:
    #         rsp = rsp.filter(UserLabelConfig.create_name == creator_name)
    #
    #     result = rsp.all()
    #     result_list = []
    #     for item in result:
    #         sub_data = {"标签名称": item.label_name, "标签描述": item.label_describe, "标签人数": item.label_count,
    #                     "创建人": item.create_name, "创建时间": item.created_time,
    #                     "最近操作人": item.last_operator, "最近操作时间": item.updated_time}
    #         result_list.append(sub_data)
    #     return result_list

    # @staticmethod
    # def get_label_config_record_sql(label_name="", change_type="", updater_name="",
    #                                 update_start_diff=-1, update_end_diff=0):
    #     """
    #     获取标签配置记录
    #     :param label_name
    #     :param change_type
    #     :param updater_name
    #     :param update_start_diff
    #     :param update_end_diff
    #     :return:
    #     """
    #     update_start, update_end = DateUtil.get_timestamp_range(update_start_diff, update_end_diff,
    #                                                             date_type='日')
    #     rsp = ms_context.get().session.query(UserLabelConfigRecord).filter(
    #         UserLabelConfigRecord.updated_time.between(update_start, update_end))
    #
    #     if label_name:
    #         rsp = rsp.filter(UserLabelConfigRecord.label_name == label_name)
    #     if change_type:
    #         rsp = rsp.filter(UserLabelConfigRecord.change_type == change_type)
    #     if update_start_diff and update_end_diff:
    #         rsp = rsp.filter(UserLabelConfigRecord.updated_time.between(update_start, update_end))
    #     if updater_name:
    #         rsp = rsp.filter(UserLabelConfigRecord.updater == updater_name)
    #
    #     result = rsp.all()
    #     result_list = []
    #     for item in result:
    #         sub_data = {"操作时间": item.updated_time, "标签名称": item.label_name, "变更类型": item.change_type,
    #                     "变更前": item.before_change, "变更后": item.after_change,
    #                     "操作人": item.updater}
    #         result_list.append(sub_data)
    #     return result_list

    @staticmethod
    def get_user_info_change_sql(site_code, user_id="", account_type="", change_type="", operator="",
                                 opera_start_diff=-7, opera_end_diff=0):
        """
        会员信息变更记录
        :param site_code
        :param user_id 会员ID
        :param account_type 账号类型 正式 ｜ 测试
        :param change_type 变更类型 账号状态 ｜ 手机号码 ｜ 邮箱 ｜ vip等级
        :param operator 操作人
        :param opera_start_diff 开始时间
        :param opera_end_diff 结束时间
        """
        timezone = Site.get_site_timezone(site_code)
        upd_start, upd_end = DateUtil.get_timestamp_range(opera_start_diff, opera_end_diff, date_type='日',
                                                          timezone=timezone)
        rsp = ms_context.get().session.query(UserInformationChange).filter(
            UserInformationChange.operating_time.between(upd_start, upd_end))

        if user_id:
            rsp = rsp.filter(UserInformationChange.member_account == user_id)
        if account_type:
            rsp = rsp.filter(UserInformationChange.account_type == System.get_user_account_type(account_type))
        if change_type:
            rsp = rsp.filter(UserInformationChange.change_type == System.get_user_change_type(change_type))
        if operator:
            rsp = rsp.filter(UserInformationChange.operator == operator)

        result = rsp.all()
        result_list = []
        for item in result:
            sub_data = {"操作时间": item.operating_time, "会员ID": item.member_account, "账号类型": item.account_type,
                        "变更类型": item.change_type, "变更前信息": item.Information_before_change,
                        "变更后信息": item.Information_after_change, "提交信息": item.submit_information,
                        "操作人": item.operator}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_user_venue_info_dao(site_code, user_account, venue_name):
        """
        获取会员在某场馆的信息
        @return:
        """
        venue_info: GameInfo = Game.get_venue_info_sql(venue_name)[0]
        session_obj: session = ms_context.get().session
        user_info: UserInfo = User.get_user_info_sql(site_code, user_account)[0][0]
        data: CasinoMember = session_obj.query(CasinoMember). \
            filter(CasinoMember.user_account == user_info.user_account, CasinoMember.site_code == site_code,
                   CasinoMember.venue_code == venue_info.venue_code).first()
        return data.venue_user_account, data.venue_user_id

    # @staticmethod
    # def modify_user_login_time(user_account, day_diff):
    #     """
    #     修改用户最后一条登录记录中的登录时间为指定时间
    #     @param user_account:
    #     @param day_diff:
    #     @return:
    #     """
    #     login_timestamp = DateUtil.get_timestamp_by_now(int(day_diff))
    #     data: UserLoginInfo = ms_context.get().session.query(UserLoginInfo). \
    #         filter(UserLoginInfo.user_account == user_account). \
    #         order_by(UserLoginInfo.login_time.desc()).first()
    #     if data:
    #         data.login_time = login_timestamp
    #         ms_context.get().session.commit()
    #     return True

    # @staticmethod
    # def modify_user_register_time(user_account, year_diff=0, month_diff=0, day_diff=0):
    #     """
    #     修改用户注册时间
    #     @param user_account:
    #     @param year_diff:
    #     @param month_diff:
    #     @param day_diff:
    #     @return:
    #     """
    #     data: UserInfo = ms_context.get().session.query(UserInfo). \
    #         filter(UserLoginInfo.user_account == user_account).first()
    #     register_time = data.register_time
    #     new_time = arrow.get(register_time).to('GMT-5').shift(years=int(year_diff), months=int(month_diff),
    #                                                           days=int(day_diff)).timestamp()
    #     data.register_time = new_time
    #     ms_context.get().session.commit()

    # @staticmethod
    # def get_new_user_count_sql(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
    #     """
    #     获取新增会员数量 - 取注册表，注册的时候是什么代理，就属于谁
    #     @return:
    #     """
    #     timezone = Site.get_site_timezone(site_code)
    #     agent_data = Agent.get_agent_list_data(site_code)
    #     # 生成代理id与account\path的映射表
    #     agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}
    #     new_user_count_dic = defaultdict(int)
    #
    #     start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
    #     user_data = ms_context.get().session.query(UserRegistrationInfo). \
    #         filter(UserRegistrationInfo.site_code == site_code,
    #                UserRegistrationInfo.registration_time.between(start_time, end_time)).all()
    #
    #     # 找到会员的代理，通过path给所有代理增加数据
    #     for data in user_data:
    #         data: UserRegistrationInfo
    #         # 代理下会员
    #         if data.agent_id:
    #             agent_path = agent_dic[data.agent_id][1]
    #             for agent_id in agent_path:
    #                 new_user_count_dic[agent_dic[agent_id][0]] += 1
    #         # 直营会员
    #         else:
    #             new_user_count_dic["直营"] += 1
    #     return new_user_count_dic

    @staticmethod
    def get_new_user_count_sql(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取新增会员数量 - 取注册表，注册的时候是什么代理，就属于谁
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}
        new_user_count_dic = defaultdict(int)

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        user_data = ms_context.get().session.query(UserInfo). \
            filter(UserInfo.site_code == site_code,
                   UserInfo.register_time.between(start_time, end_time)).all()

        # 找到会员的代理，通过path给所有代理增加数据
        for data in user_data:
            data: UserInfo
            # 代理下会员
            if data.super_agent_id:
                new_user_count_dic[agent_dic[data.super_agent_id][0]] += 1
                # agent_path = agent_dic[data.super_agent_id][1]
                # for agent_id in agent_path:
                #     new_user_count_dic[agent_dic[agent_id][0]] += 1
            # 直营会员
            else:
                new_user_count_dic["直营"] += 1
        return new_user_count_dic

    @staticmethod
    def get_new_recharge_user_count_sql(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取本月新增充值会员数量
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}
        new_recharge_count_dic = defaultdict(int)

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        user_data = ms_context.get().session.query(UserInfo). \
            filter(UserInfo.site_code == site_code, UserInfo.register_time.between(start_time, end_time),
                   UserInfo.first_deposit_time.between(start_time, end_time)).all()

        for data in user_data:
            data: UserInfo
            # 代理下会员
            if data.super_agent_id:
                agent_path = agent_dic[data.super_agent_id][1]
                for agent_id in agent_path:
                    new_recharge_count_dic[agent_dic[agent_id][0]] += 1
            # 直营会员
            else:
                new_recharge_count_dic["直营"] += 1

        return new_recharge_count_dic

    @staticmethod
    def get_login_user_count_sql(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取本月登录会员数量
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        login_count_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        user_data = ms_context.get().session.query(UserInfo). \
            filter(UserInfo.site_code == site_code, UserInfo.last_login_time.between(start_time, end_time))

        for data in user_data:
            data: UserInfo
            # 代理下会员
            if data.super_agent_id:
                agent_path = agent_dic[data.super_agent_id][1]
                for agent_id in agent_path:
                    login_count_dic[agent_dic[agent_id][0]] += 1
            # 直营会员
            else:
                login_count_dic["直营"] += 1

        return login_count_dic

    @staticmethod
    def get_first_deposit_user_count(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月', if_all=False):
        """
        获取首存玩家数量和金额
        @return: 首存玩家数量, 首存金额
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        agent_data = Agent.get_agent_list_data(site_code)
        # 直属会员统计
        user_count_dic = defaultdict(int)
        # 团队会员统计
        team_user_count_dic = defaultdict(int)
        team_deposit_amount_dic = defaultdict(int)
        deposit_amount_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}
        # 获取所有会员信息
        user_data = ms_context.get().session.query(UserInfo).filter(UserInfo.site_code == site_code,
                                                                    UserInfo.first_deposit_time.is_not(None))
        if not if_all:
            user_data = user_data.filter(UserInfo.first_deposit_time.between(start_time, end_time))
        # 找到会员的代理，通过path给所有代理增加数据
        for data in user_data.all():
            data: UserInfo
            # 代理下会员
            if data.super_agent_id:
                agent_account = agent_dic[data.super_agent_id][0]
                amount = data.first_deposit_amount
                user_count_dic[agent_account] += 1
                deposit_amount_dic[agent_account] += amount
                agent_path = agent_dic[data.super_agent_id][1]
                for agent_id in agent_path:
                    team_user_count_dic[agent_dic[agent_id][0]] += 1
                    team_deposit_amount_dic[agent_dic[agent_id][0]] += amount
            # 直营会员
            else:
                team_user_count_dic["直营"] += 1
                team_deposit_amount_dic["直营"] += data.first_deposit_amount
        return {"团队首存玩家数量": team_user_count_dic, "团队玩家首存金额": team_deposit_amount_dic,
                "直属首存玩家数量": user_count_dic, "直属玩家首存金额": deposit_amount_dic}

    # @staticmethod
    # def _get_valid_user_data(site_code, date_diff=0, stop_diff=0, date_type='月', valid_type='活跃'):
    #     """
    #     有效会员数据 - 充值和流水均满足条件
    #     @param site_code:
    #     @param date_diff:
    #     @param stop_diff:
    #     @param date_type:
    #     @param valid_type: 活跃 ｜ 有效活跃
    #     @return:
    #     """
    #     recharge_limit = System.get_active_judgement("充值活跃用户标准" if valid_type == "活跃" else "充值有效活跃用户标准")
    #     bet_limit = System.get_active_judgement("有效投注活跃用户标准" if valid_type == "活跃" else "有效投注有效活跃用户标准")
    #     # 充值满足条件的用户
    #     recharge_data = Funds.get_deposit_valid_user(site_code, recharge_limit, date_diff, date_diff, stop_diff,
    #                                                  date_type)
    #     # 打码满足条件的用户
    #     bet_data = Order.get_bet_valid_user(site_code, bet_limit, date_diff, date_diff, stop_diff, date_type)
    #     valid_user_dic = defaultdict(set)
    #     for name in set(list(recharge_data.keys()) + list(bet_data.keys())):
    #         valid_user_dic[name] = set(recharge_data[name] + bet_data[name])
    #     return valid_user_dic

    @staticmethod
    def get_bet_user_count_sql(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月'):
        """
        获取本月投注会员数量
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        agent_data = Agent.get_agent_list_data(site_code)
        bet_count_dic = defaultdict(int)
        # 生成代理id与account\path的映射表
        agent_dic = {_.agent_id: (_.agent_account, _.path.split(",")) for _ in agent_data}

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        order_data = ms_context.get().session.query(OrderRecord.user_account, OrderRecord.agent_id). \
            filter(OrderRecord.site_code == site_code, OrderRecord.settle_time.between(start_time, end_time)). \
            group_by(OrderRecord.user_account, OrderRecord.agent_id)

        for data in order_data:
            # 代理下会员
            if data[1]:
                agent_path = agent_dic[data[1]][1]
                for agent_id in agent_path:
                    bet_count_dic[agent_dic[agent_id][0]] += 1
            # 直营会员
            else:
                bet_count_dic["直营"] += 1

        return bet_count_dic

    @staticmethod
    def get_user_change_audit_list_sql(site_code, apply_start_diff=0, apply_end_diff=0, audit_start_diff=None,
                                       audit_end_diff=None, user_account=None, account_type=None, apply_type=None,
                                       audit_operate=None, audit_status=None, applicant=None, audit_account=None,
                                       lock_status=None, order_no=None, order_id=None, stop_diff=0, date_type='日'):
        """
        会员信息变更审批记录
        @param site_code:
        @param apply_start_diff:
        @param apply_end_diff:
        @param audit_start_diff:
        @param audit_end_diff:
        @param user_account:
        @param account_type: 测试 ｜ 正式
        @param apply_type: 账号状态 ｜ 手机号码 ｜ 邮箱 ｜ vip等级
        @param audit_operate: 一审审核 ｜ 结单查看
        @param audit_status: 待处理 ｜ 处理中 ｜ 审核通过 ｜ 一审拒绝
        @param applicant:
        @param audit_account:
        @param lock_status: 未锁 ｜ 已锁
        @param order_no:
        @param stop_diff:
        @param date_type:
        @param order_id:
        @return:
        """
        timezone = Site.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(apply_start_diff, apply_end_diff, stop_diff, date_type,
                                                            timezone)
        rsp = ms_context.get().session.query(UserAccountUpdateReview). \
            filter(UserAccountUpdateReview.application_time.between(start_time, end_time),
                   UserAccountUpdateReview.site_code == site_code)
        if audit_start_diff:
            start_time, end_time = DateUtil.get_timestamp_range(audit_start_diff, audit_end_diff, stop_diff, date_type,
                                                                timezone)
            rsp = rsp.filter(UserAccountUpdateReview.first_review_time.between(start_time, end_time))
        if user_account:
            rsp = rsp.filter(UserAccountUpdateReview.member_account == user_account)
        if account_type:
            rsp = rsp.filter(UserAccountUpdateReview.account_type == System.get_user_account_type(account_type))
        if apply_type:
            rsp = rsp.filter(UserAccountUpdateReview.review_application_type == System.get_user_change_type(apply_type))
        if applicant:
            rsp = rsp.filter(UserAccountUpdateReview.applicant == applicant)
        if order_no:
            rsp = rsp.filter(UserAccountUpdateReview.review_order_number)
        if lock_status:
            rsp = rsp.filter(UserAccountUpdateReview.lock_status == System.get_audit_lock_status(lock_status))
        if audit_account:
            rsp = rsp.filter(UserAccountUpdateReview.first_instance == audit_account)
        if audit_status:
            rsp = rsp.filter(UserAccountUpdateReview.review_status == System.get_review_status(audit_status))
        if audit_operate:
            rsp = rsp.filter(UserAccountUpdateReview.review_operation == System.get_audit_operate(audit_operate))
        if order_id:
            rsp = rsp.filter(UserAccountUpdateReview.id == order_id)
        rsp = rsp.order_by(UserAccountUpdateReview.application_time.desc())
        return rsp.all()

    @staticmethod
    def wait_until_has_user_change_audit_order(site_code, user_account, apply_type, timeout=5):
        """
        会员信息变更当前待审核的订单号
        @param site_code:
        @param user_account:
        @param apply_type: 账号状态 ｜ 手机号码 ｜ 邮箱 ｜ vip等级
        @param timeout:
        @return: 订单 id, order_no
        """
        start_time = int(time.time())
        audit_status = System.get_review_status("待处理")
        while int(time.time()) - start_time < timeout:
            rsp = ms_context.get().session.query(UserAccountUpdateReview). \
                filter(UserAccountUpdateReview.site_code == site_code,
                       UserAccountUpdateReview.member_account == user_account,
                       UserAccountUpdateReview.review_application_type == System.get_user_change_type(apply_type),
                       UserAccountUpdateReview.review_status == audit_status).first()
            if rsp:
                return rsp.id, rsp.review_order_number
            time.sleep(0.5)
        raise AssertionError(f"未找到{apply_type}类型的待处理订单")

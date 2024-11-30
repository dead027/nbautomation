#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 17:32
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.venue_info_model import VenueInfo
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.GameEnum import GameEnum
from Library.MysqlTableModel.game_info_model import GameInfo
from Library.MysqlTableModel.game_one_class_info_model import GameOneClassInfo
from Library.MysqlTableModel.game_two_class_info_model import GameTwoClassInfo
from Library.Dao.Mysql.ChainQery.System import System


class Game(object):
    @staticmethod
    def get_venue_info_sql(venue_name="", venue_type="", venue_code=""):
        """
        获取场馆信息
        :param venue_name
        :param venue_code
        :param venue_type
        :return:
        """

        data = ms_context.get().session.query(VenueInfo)
        if venue_name:
            data = data.filter(VenueInfo.venue_name == venue_name)
        if venue_type:
            data = data.filter(VenueInfo.venue_type == System.get_venue_type(venue_type)).all()
        if venue_code:
            data = data.filter(VenueInfo.venue_code == venue_code)
        return data.all()

    @staticmethod
    def get_game_bet_list_sql(bet_number="", third_party_order_number="", start_settle_time_diff=None,
                              stop_settle_time_diff=None, game_platform="", game_name="", member_account="",
                              account_type="",
                              superior_agent="", game_account="", event_id="", bet_status="", start_bet_amount="",
                              stop_bet_amount="", start_members_win_lose="", stop_members_win_lose="",
                              start_valid_amount="",
                              stop_valid_amount="", betting_ip="", start_vip_level="", stop_vip_level="",
                              change_status="",
                              device_type="", start_change_time="", stop_change_time="", start_bet_time_diff=-7,
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
        start_bet_time, stop_bet_time = DateUtil.get_timestamp_range(start_bet_time_diff, stop_bet_time_diff,
                                                                     date_type='日')
        rsp = ms_context.get().session.query(OrderRecord).filter(OrderRecord.bet_time.between(start_bet_time,
                                                                                              stop_bet_time))

        if bet_number:
            rsp = rsp.filter(OrderRecord.order_id == bet_number)
        if third_party_order_number:
            rsp = rsp.filter(OrderRecord.third_order_id == third_party_order_number)
        if game_platform:
            rsp = rsp.filter(OrderRecord.venue_code.in_([GameEnum.game_platform_f_cn.value[item] for item in
                                                         game_platform.split(",")]))
        if game_name:
            rsp = rsp.filter(OrderRecord.game_name == game_name)
        if member_account:
            rsp = rsp.filter(OrderRecord.user_account == member_account)
        if account_type:
            rsp = rsp.filter(OrderRecord.account_type.in_([GameEnum.account_type_f_cn.value[item] for item in
                                                           account_type.split(",")]))
        if superior_agent:
            rsp = rsp.filter(OrderRecord.agent_acct == superior_agent)
        if start_settle_time_diff and stop_settle_time_diff:
            start_settle_time, stop_settle_time = DateUtil.get_timestamp_range(start_settle_time_diff,
                                                                               stop_settle_time_diff,
                                                                               date_type='日')
            rsp = rsp.filter(OrderRecord.settle_time.between(start_settle_time, stop_settle_time))
        if game_account:
            rsp = rsp.filter(OrderRecord.casino_user_name == game_account)
        if event_id:
            rsp = rsp.filter(OrderRecord.game_no == event_id)
        if bet_status:
            rsp = rsp.filter(OrderRecord.order_status.in_([GameEnum.bet_status_f_cn.value[item] for item in
                                                           bet_status.split(",")]))
        if start_bet_amount and stop_bet_amount:
            rsp = rsp.filter(OrderRecord.bet_amount.between(start_bet_amount, stop_bet_amount))
        if start_members_win_lose and stop_members_win_lose:
            rsp = rsp.filter(OrderRecord.win_loss_amount.between(start_members_win_lose, stop_members_win_lose))
        if start_valid_amount and stop_valid_amount:
            rsp = rsp.filter(OrderRecord.valid_amount.between(start_valid_amount, stop_valid_amount))
        if betting_ip:
            rsp = rsp.filter(OrderRecord.bet_ip == betting_ip)
        if start_vip_level and stop_vip_level:
            rsp = rsp.filter(OrderRecord.vip_rank_code.between(start_vip_level, stop_vip_level))
        if change_status:
            rsp = rsp.filter(OrderRecord.change_status == change_status)
        if device_type:
            rsp = rsp.filter(OrderRecord.device_type.in_([GameEnum.device_type_f_cn.value[item] for item in
                                                          device_type.split(",")]))
        if start_change_time and stop_change_time:
            rsp = rsp.filter(OrderRecord.change_time.between(start_change_time, stop_change_time))
        result = rsp.all()
        result_list = []
        order_status_dic = System.get_order_status(to_zh=True)
        client_type_dic = System.get_user_register_client(to_zh=True)
        for item in result:
            sub_data = {"注单号": item.order_id, "三方订单号": item.third_order_id, "游戏平台": item.venue_code,
                        "游戏分类": item.game_name, "赛事ID/局号": item.game_no,
                        "会员账号": item.user_account, "游戏账号": item.casino_user_name,
                        "上级代理": item.agent_acct,
                        "账号类型": GameEnum.account_type_t_cn.value[item.account_type],
                        "VIP等级": item.vip_rank_code, "游戏名称": item.game_name,
                        "玩法": item.parlay_info, "注单详情": item.order_info,
                        "投注金额": item.bet_amount, "会员输赢": item.win_loss_amount, "有效投注": item.valid_amount,
                        "注单状态": order_status_dic[item.order_status], "投注时间": item.bet_time,
                        "结算时间": item.settle_time,
                        "同步时间": item.settle_time, "投注IP": item.bet_ip,
                        "投注终端": client_type_dic[item.device_type]}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_game_info_dao(game_id=None, venue=None, game_status=None, operator=None):
        """
        获取总台游戏信息
        :return:
        """
        data = ms_context.get().session.query(GameInfo)
        if game_id:
            data = data.filter(GameInfo.game_id == game_id)
        if venue:
            data = data.filter(GameInfo.venue_name == venue)
        if game_status:
            data = data.filter(GameInfo.status == System.get_platform_status(game_status))
        if operator:
            data = data.filter(GameInfo.updater == operator)
        return data.all()

    @staticmethod
    def get_game_one_class_info_list_sql(TypeName="", status=""):
        """
        获取一级分类配置
        :param TypeName
        :param status
        :return:
        """
        data = ms_context.get().session.query(GameOneClassInfo)
        if TypeName:
            data = data.filter(GameOneClassInfo.type_name == TypeName)
        if status:
            data = data.filter(GameOneClassInfo.status.in_([GameEnum.display_status_t_cn_dic.value[item] for item in
                                                            status.split(",")]))
        result = data.all()
        result_list = []
        for item in result:
            sub_data = {"分类名称": item.type_name, "显示状态": GameEnum.display_status_t_cn_dic.value[item.status],
                        "模板": GameEnum.game_module_t_cn_dic.value[item.model_code],
                        "创建人": item.creator_name, "创建时间": item.created_time, "最近操作人": item.updater_name,
                        "最近操作时间": item.updated_time}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_game_two_class_info_list_sql(TypeName="", status=""):
        """
        获取二级分类配置
        :param typeName
        :param status
        :return:
        """
        data = ms_context.get().session.query(GameTwoClassInfo)
        if TypeName:
            data = data.filter(GameTwoClassInfo.type_name == TypeName)
        if status:
            data = data.filter(GameTwoClassInfo.status.in_([GameEnum.display_status_t_cn_dic.value[item] for item in
                                                            status.split(",")]))
        result = data.all()
        result_list = []
        for item in result:
            sub_data = {"分类名称": item.type_name, "上级分类": item.model_code,
                        "模板": GameEnum.game_module_t_cn_dic.value[item.model_code],
                        "显示状态": GameEnum.display_status_t_cn_dic.value[item.status],
                        "包含子游戏": item.game_one_id,
                        "创建人": item.creator_name, "创建时间": item.created_time, "最近操作人": item.updater_name,
                        "最近操作时间": item.updated_time}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_game_manager_info_list_sql(gameId="", gameName="", status="", venueCode="", gameOneId="", gameTwoId="",
                                       label=""):
        """
        获取游戏管理
        :param gameId
        :param gameName
        :param status
        :param venueCode
        :param gameOneId
        :param gameTwoId
        :param label
        :return:
        """
        data = ms_context.get().session.query(GameTwoClassInfo)
        if gameId:
            data = data.filter(GameInfo.game_id == gameId)
        if gameName:
            data = data.filter(GameInfo.game_name == gameName)
        if status:
            data = data.filter(GameInfo.status.in_([GameEnum.display_status_t_cn_dic.value[item] for item in
                                                    status.split(",")]))
        if venueCode:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_platform_f_cn_dic.value[item] for item in
                                                        venueCode.split(",")]))
        if gameOneId:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_module_f_cn_dic.value[item] for item in
                                                        gameOneId.split(",")]))
        if gameTwoId:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_module_f_cn_dic.value[item] for item in
                                                        gameTwoId.split(",")]))
        if label:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_modle_dic.value[item] for item in
                                                        label.split(",")]))
        result = data.all()
        result_list = []
        for item in result:
            sub_data = {"游戏ID": item.game_id, "游戏名称": item.game_name,
                        "游戏平台": item.venue_name, "一级分类": "", "二级分类": "", "标签": item.label,
                        "支持终端": item.support_device,
                        "显示状态": GameEnum.display_status_t_cn_dic.value[item.status], "游戏图片": item.game_pic,
                        "创建人": item.creator_name, "创建时间": item.created_time, "最近操作人": item.updater_name,
                        "维护开始时间": item.maintenance_start_time, "维护结束时间": item.maintenance_end_time,
                        "最近操作时间": item.updated_time}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def update_order_date_to_yesterday(order_no):
        """
        更新VIP流水记录表的时间为昨日
        @param order_no:
        @return:
        """
        # yesterday_time = DateUtil.

    @staticmethod
    def get_venue_info_list_sql(venue_name_str="", venue_type_str="", operator=""):
        """
        查询场馆详情
        @return:
        """
        venue_type_dic = System.get_venue_type()
        venue_type_zh_dic = System.get_venue_type(to_zh=True)
        data = ms_context.get().session.query(VenueInfo)
        if venue_name_str:
            data = data.filter(VenueInfo.venue_name.in_(venue_name_str.split(",")))
        if venue_type_str:
            data = data.filter(VenueInfo.venue_type.in_([venue_type_dic[_] for _ in venue_type_str.split(",")]))
        if operator:
            data = data.filter(VenueInfo.updater_name == operator)
        result = data.all()
        result_list = []
        for item in result:
            sub_data = {"游戏场馆": item.venue_name,
                        "场馆类别": venue_type_zh_dic[item.venue_name],
                        "场馆费率": item.venue_proportion, "状态": item.status,
                        "维护时间": [item.maintenance_start_time, item.maintenance_end_time],
                        "操作人": item.updater_name,
                        "操作时间": item.updated_time,
                        "备注": item.remark}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_venue_list_of_venue_type(venue_type):
        """
        获取场馆类型下的场馆列表
        @param venue_type:
        @return:
        """
        data = Game.get_venue_info_list_sql(venue_type_str=venue_type)
        return [_["游戏场馆"] for _ in data]

#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/10 17:32
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.venue_info_model import VenueInfo
from Library.MysqlTableModel.site_game_model import SiteGame
from Library.MysqlTableModel.order_record_model import OrderRecord
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.GameEnum import GameEnum
from Library.MysqlTableModel.game_info_model import GameInfo
from Library.MysqlTableModel.game_one_class_info_model import GameOneClassInfo
from Library.MysqlTableModel.game_two_class_info_model import GameTwoClassInfo
from Library.Dao.Mysql.ChainQery.System import System


class Game(object):
    @staticmethod
    def get_venue_info_dao(venue_name="", venue_type="", venue_status="", operator=""):
        """
        获取场馆信息
        @param venue_name:
        @param venue_type:
        @param venue_status:
        @param operator:
        @return:
        """
        data = ms_context.get().session.query(VenueInfo)
        if venue_name:
            data = data.filter(VenueInfo.venue_name == venue_name)
        if venue_type:
            data = data.filter(VenueInfo.venue_type == System.get_venue_type(venue_type))
        if venue_status:
            data = data.filter(VenueInfo.status == System.get_platform_status(venue_status))
        if operator:
            data = data.filter(VenueInfo.updater_name == operator)
        return data.all()

    @staticmethod
    def get_venue_name_dic(to_zh=False):
        """
        获取场馆名称字典
        @return:
        """
        venue_data = Game.get_venue_info_dao()
        if to_zh:
            venue_name_dic = {_.venue_code: _.venue_name for _ in venue_data}
        else:
            venue_name_dic = {_.venue_name: _.venue_code for _ in venue_data}
        return venue_name_dic

    @staticmethod
    def get_site_game_info_dao(game_id=None, venue_name=None, operator=None, tag=None, first_type=None,
                               second_type=None):
        """
        获取站点游戏信息
        :return:
        """
        venue_info: VenueInfo = Game.get_venue_info_sql(venue_name)
        data = ms_context.get().session.query(SiteGame)
        if game_id:
            data = data.filter(SiteGame.id == game_id)
        if venue_name:
            data = data.filter(SiteGame.venue_code == venue_info.venue_code)
        if operator:
            data = data.filter(SiteGame.updater_name == operator)
        if tag:
            data = data.filter(SiteGame.label == tag)
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
            data = data.filter(GameOneClassInfo.status.in_([GameEnum.display_status_t_cn.value[item] for item in
                                                            status.split(",")]))
        result = data.all()
        result_list = []
        for item in result:
            sub_data = {"分类名称": item.type_name, "显示状态": GameEnum.display_status_t_cn.value[item.status],
                        "模板": GameEnum.game_module_t_cn.value[item.model_code],
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
            data = data.filter(GameTwoClassInfo.status.in_([GameEnum.display_status_t_cn.value[item] for item in
                                                            status.split(",")]))
        result = data.all()
        result_list = []
        for item in result:
            sub_data = {"分类名称": item.type_name, "上级分类": item.model_code,
                        "模板": GameEnum.game_module_t_cn.value[item.model_code],
                        "显示状态": GameEnum.display_status_t_cn.value[item.status],
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
            data = data.filter(GameInfo.status.in_([GameEnum.display_status_t_cn.value[item] for item in
                                                    status.split(",")]))
        if venueCode:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_platform_f_cn.value[item] for item in
                                                        venueCode.split(",")]))
        if gameOneId:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_module_f_cn.value[item] for item in
                                                        gameOneId.split(",")]))
        if gameTwoId:
            data = data.filter(GameInfo.venue_code.in_([GameEnum.game_module_f_cn.value[item] for item in
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
                        "显示状态": GameEnum.display_status_t_cn.value[item.status], "游戏图片": item.game_pic,
                        "创建人": item.creator_name, "创建时间": item.created_time, "最近操作人": item.updater_name,
                        "维护开始时间": item.maintenance_start_time, "维护结束时间": item.maintenance_end_time,
                        "最近操作时间": item.updated_time}
            result_list.append(sub_data)
        return result_list

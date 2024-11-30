#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/23 21:16
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Dao.Mysql.ChainQery.Game import Game, GameInfo, VenueInfo
from Library.Common.Enum.GameEnum import GameEnum
from Library.Common.Utils.DateUtil import DateUtil


class GameModuleBackendApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def set_game_status_api(game_name, game_status, start_diff=None, end_diff=None, check_code=True):
        """
        设置游戏状态
        :param game_name:
        :param game_status: 开启 ｜ 禁用 | 维护
        :param check_code:
        :param start_diff:
        :param end_diff:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/venue_info/api/upGameInfoStatus'
        game_info: GameInfo = Game.get_game_info_sql(game_name)
        params = {"id": game_info.game_id, "status": GameEnum.game_status_f_cn_dic.value[game_status]}
        if game_status == '维护':
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, date_type='日')
            params['maintenanceStartTime'] = start_time
            params['maintenanceEndTime'] = end_time
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp["message"]

    @staticmethod
    def set_venue_status_api(venue_name, venue_status, start_diff=None, end_diff=None, check_code=True):
        """
        设置场馆状态
        :param venue_name:
        :param venue_status: 开启 ｜ 禁用 | 维护
        :param check_code:
        :param start_diff:
        :param end_diff:
        :return:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/venue_info/api/upVenueInfoStatus'
        venue_info: VenueInfo = Game.get_venue_info_sql(venue_name)
        params = {"id": venue_info.id, "status": GameEnum.game_status_f_cn_dic.value[venue_status]}
        if venue_status == '维护':
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, date_type='日')
            params['maintenanceStartTime'] = start_time
            params['maintenanceEndTime'] = end_time
        resp = HttpRequestUtil.post(url, params, check_code=check_code)
        return resp["message"]

    @staticmethod
    def get_game_first_level_classification_configuration_list_api(TypeName="", Status= ""):
        """
        一级分类配置
        :param TypeName:
        :param Status:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/venue_info/api/gameOneClassInfoPage'
        params = {"typeName": "", "status": "", "pageNumber": 1, "pageSize": 10}
        if TypeName:
            params["typeName"] = TypeName
        if Status:
            params["status"] = GameEnum.display_status_f_cn_dic[Status]
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"分类名称": "typeName", "显示状态": "statusName", "模板": "modelName",
                   "包含二级分类": "twoClassSize",
                   "创建人": "creatorName", "创建时间": "createdTime", "最近操作人": "updaterName",
                   "最近操作时间": "updatedTime"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_game_two_level_classification_configuration_list_api(TypeName= "", Status= "" ):
        """
        二级分类配置
        :param TypeName:
        :param Status:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/venue_info/api/gameTwoClassInfoPage'
        params = {"typeName": "", "status": "", "pageNumber": 1, "pageSize": 10}
        if TypeName:
            params["typeName"] = TypeName
        if Status:
            params["status"] = GameEnum.display_status_f_cn_dic[Status]
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"分类名称": "typeName", "上级分类": "gameOneName", "显示状态": "statusName",
                   "包含子游戏": "gameSize",
                   "创建人": "creatorName", "创建时间": "createdTime", "最近操作人": "updaterName",
                   "最近操作时间": "updatedTime"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_game_platform_management_list_api(VenueName= "", Status= "", GameOneId= "", Creator= ""):
        """
        游戏平台管理
        :param VenueName:
        :param Status:
        :param GameOneId:
        :param Creator:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/venue_info/api/venueInfoPage'
        params = {"venueName": "", "status": "", "gameOneId": "", "creator": "", "pageNumber": 1, "pageSize": 10}
        if VenueName:
            params["typeName"] = VenueName
        if Status:
            params["status"] = GameEnum.display_status_f_cn_dic[Status]
        if GameOneId:
            params["gameOneId"] = GameEnum.game_category_dic[GameOneId]
        if Creator:
            params["creator"] = Creator
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"游戏平台": "venueName", "游戏分类": "gameOneName", "显示状态": "statusName",
                   "平台图标": "venueIcon",
                   "最近操作人": "updaterName", "平台费率": "venueProportion",
                   "维护开始时间": "maintenanceStartTime",
                   "维护结束时间": "maintenanceEndTime",
                   "最近操作时间": "updatedTime", "备注": "remark"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_game_management_list_api(GameId= "", GameName= "", VenueCode= "", GameOneId= "", GameTwoId= "",
                                     label= "" ):
        """
        游戏管理
        :param GameId:
        :param GameName:
        :param VenueCode:
        :param GameOneId:
        :param GameTwoId:
        :param Label:
        """
        url = YamlUtil.get_backend_host() + '/admin-foreign/venue_info/api/gameInfoPage'
        params = {"gameId": "", "gameName": "", "status": "", "venueCode": "", "gameOneId": "", "gameTwoId": "",
                  "label": "", "pageNumber": 1, "pageSize": 10}
        if GameId:
            params["gameId"] = GameId
        if GameName:
            params["gameName"] = GameName
        if VenueCode:
            params["venueCode"] = VenueCode
        if GameOneId:
            params["gameOneId"] = GameEnum.game_category_dic[GameOneId]
        if GameTwoId:
            params["gameTwoId"] = GameTwoId
        if label:
            params["label"] = label
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"游戏ID": "gameId", "游戏名称": "gameName", "游戏平台": "venueName", "一级分类": "gameOneClassName",
                   "二级分类": "gameTwoClassName", "标签": "labelName", "支持终端": "supportDeviceName",
                   "显示状态": "statusName", "游戏图片": "gamePicUrl", "创建人": "creatorName",
                   "创建时间": "createdTime",
                   "最近操作人": "updaterName", "维护开始时间": "maintenanceStartTime",
                   "维护结束时间": "maintenanceEndTime",
                   "最近操作时间": "updatedTime"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_game_bet_list_api(bet_number="", third_party_order_number="", start_settle_time_diff=None,
                              stop_settle_time_diff=None, game_platform="", game_name="", member_account="",
                              account_type="",
                              superior_agent="", game_account="", event_id="", bet_status="", start_bet_amount="",
                              stop_bet_amount="", start_members_win_lose="", stop_members_win_lose="",
                              start_valid_amount="",
                              stop_valid_amount="", betting_ip="", start_vip_level="", stop_vip_level="",
                              change_status="",
                              device_type="", start_change_time_diff="", stop_change_time_diff="",
                              start_bet_time_diff=-7,
                              stop_bet_time_diff=0):
        """"
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
        :param start_change_time_diff 变更时间开始值
        :param stop_change_time_diff 变更时间截至值
        :return:
        """
        start_bet_time, stop_bet_time = DateUtil.get_timestamp_range(start_bet_time_diff, stop_bet_time_diff,
                                                                     date_type='日')
        url = YamlUtil.get_backend_host() + '/admin-foreign/order-record/api/admin/page'

        params = {"betBeginTime": start_bet_time, "betEndTime": stop_bet_time, "settleBeginTime": "",
                  "settleEndTime": "", "changeBeginTime": "", "changeEndTime": "", "orderId": "", "thirdOrderId": "",
                  "venueCode": [], "gameName": "", "userAccount": "", "accountType": [], "agentAcct": "",
                  "casinoUserName": "", "gameNo": "", "orderStatusList": [], "betAmountMin": "", "betAmountMax": "",
                  "winLossAmountMin": "", "winLossAmountMax": "", "validAmountMin": "", "validAmountMax": "",
                  "betIp": "", "vipRankMin": "", "vipRankMax": "", "rebateRateMin": "", "rebateRateMax": "",
                  "rebateAmountMin": "", "rebateAmountMax": "", "changeStatus": "", "deviceType": [],
                  "registerTime": "", "orderField": "", "orderType": "", "orderName": "", "orderValue": "",
                  "pageNumber": 1, "pageSize": 10}
        if bet_number:
            params["orderId"] = bet_number
        if third_party_order_number:
            params["thirdOrderId"] = third_party_order_number
        if start_settle_time_diff and stop_settle_time_diff:
            start_settle_time, stop_settle_time = DateUtil.get_timestamp_range(start_settle_time_diff,
                                                                               stop_settle_time_diff, date_type='日')
            params["settleBeginTime"] = start_settle_time
            params["settleEndTime"] = stop_settle_time
        if game_platform:
            params["venueCode"] = [GameEnum.game_platform_f_cn_dic.value[item] for item in game_platform.split(",")]
        if game_name:
            params["gameName"] = game_name
        if member_account:
            params["userAccount"] = member_account
        if account_type:
            params["accountType"] = [GameEnum.account_type_f_cn_dic.value[item] for item in game_account.split(",")]
        if superior_agent:
            params["agentAcct"] = superior_agent
        if game_account:
            params["casinoUserName"] = game_account
        if event_id:
            params["gameNo"] = event_id
        if bet_status:
            params["orderStatusList"] = [GameEnum.bet_status_f_cn_dic.value[item] for item in bet_status.split(",")]
        if start_bet_amount and stop_bet_amount:
            params["betAmountMin"] = start_bet_amount
            params["betAmountMax"] = stop_bet_amount
        if start_members_win_lose and stop_members_win_lose:
            params["winLossAmountMin"] = start_members_win_lose
            params["winLossAmountMax"] = stop_members_win_lose
        if start_valid_amount and stop_valid_amount:
            params["validAmountMin"] = start_valid_amount
            params["validAmountMax"] = stop_valid_amount
        if betting_ip:
            params["betIp"] = betting_ip
        if start_vip_level and stop_vip_level:
            params["vipRankMin"] = start_vip_level
            params["vipRankMax"] = stop_vip_level
        if change_status:
            params["changeStatus"] = [GameEnum.change_status_f_cn_dic.value[item] for item in change_status.split(",")]
        if device_type:
            params["deviceType"] = [GameEnum.device_type_f_cn_dic.value[item] for item in device_type.split(",")]
        if start_change_time_diff and stop_change_time_diff:
            start_change_time, stop_change_time = DateUtil.get_timestamp_range(start_change_time_diff,
                                                                               stop_change_time_diff,
                                                                               date_type='日')
            params["changeBeginTime"] = start_change_time
            params["changeEndTime"] = stop_change_time
        resp = HttpRequestUtil.post(url, params, all_page=True)
        map_dic = {"注单号": "orderId", "三方订单号": "thirdOrderId", "游戏平台": "venueName",
                   "游戏分类": "gameTypeName", "赛事ID/局号": "gameNo", "会员账号": "userAccount",
                   "游戏账号": "casinoUserName",
                   "上级代理": "agentAcct", "账号类型": "accountTypeText", "VIP等级": "vipRankName",
                   "游戏名称": "gameName", "玩法": "playInfo", "注单详情": "orderInfo",
                   "投注金额": "betAmount", "会员输赢": "winLossAmount", "有效投注": "validAmount",
                   "注单状态": "orderClassifyText",
                   "投注时间": "betTime", "结算时间": "settleTime", "同步时间": "changeTime", "投注IP": "betIp",
                   "投注终端": "deviceType"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

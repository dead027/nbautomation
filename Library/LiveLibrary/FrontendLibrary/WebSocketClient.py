#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yao x ing
# datetime: 2022/10/24 15:58
import logging
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.LiveLibrary.ServerConnector.Structures import PlayerStruct, GameTypeStruct, DeskStruct
from Library.LiveLibrary.PublicVariables import *
from Library.Common.Utils.Contexts import *
from Library.LiveLibrary.FrontendLibrary.MysqlClient import MysqlClient

logging.basicConfig(level=logging.INFO)

service_dic = {"百家乐": "BaccaratService", "牛牛": "BullService", "三公": "SanGongService", "龙虎": "DragonTigerService",
               "打赏": "PlatformGiftService", "龙凤炸金花": "GoldenFlowerService", "印度炸金花": "IndiaGoldenFlowerService",
               "炸金花": "ThreeCardPokerService", "德州扑克": "TexasService", "骰宝": "SicboService",
               "轮盘": "RouletteService", "番摊": "FtService", "色碟": "ColorDishService"}


class WebSocketClient(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def receive_user_info():
        """
        接收用户信息数据
        :return:
        """
        return live_ws_context.get().receive_msg_ws("getBasicUserInfo")["data"]

    @staticmethod
    def client_connect_to_ws(url):
        """
        客户端建立ws连接
        :param url
        :return:
        """
        live_ws_context.get().connect_to_server_short(url)

    @staticmethod
    def get_desk_list(user_id):
        """
        游戏大厅，获取桌台列表
        :return:
        """
        params = {
            "userId": user_id,
            "deskNo": None,
            "service": "GameHallService",
            "function": "getTableList",
            "data": None
        }
        live_ws_context.get().send_msg_ws(params)
        data = live_ws_context.get().receive_msg_ws("getClassTableList")["data"]["getClassTableList"][0]
        table_list = []
        for item in data:
            if item["gameStatus"] == 1:
                table = DeskStruct(item["deskNo"], "", "", "", "", "", "", "", "", item["dealerName"], "",
                                   item["tableName"], item["minBetAmount"], item["maxBetAmount"],
                                   item["dealerPhotoUrl"], item["dealerCountry"], item["dealerCountyPicture"],
                                   item["totalOnlineCount"], item["identifyStartTime"], item["gameStatus"])
                if item["gameResultVOList"]:
                    result_list = []
                    for result in item["gameResultVOList"]:
                        result_dic = {"game_no": result["gameNo"], "boot_no": result["bootNo"],
                                      "desk_no": result["deskNo"]}
                        play_card_list = ["".join(item.values()) for item in result["playCard"]]
                        banker_card_list = ["".join(item.values()) for item in result["bankerCard"]]
                        result_dic["play_card"] = play_card_list
                        result_dic["banker_card"] = banker_card_list
                        result_list.append(result_dic)
                    table.game_result_vo_list = result_list
                table.reload_json()
                table_list.append(table.json)
        return table_list

    @staticmethod
    def join_room(user_id, desk_no):
        """
        进入房间
        :param user_id:
        :param desk_no:
        :return:
        """
        params = {
            "userId": user_id,
            "deskNo": desk_no,
            "service": "RoomInfoService",
            "function": "getRoomInfo",
            "data": None
        }
        live_ws_context.get().send_msg_ws(params)
        msg = live_ws_context.get().receive_msg_ws("getRoomInfo", table_no=desk_no)
        rtn = msg["data"]["getRoomInfo"][0]["data"]
        table_info_vo = rtn["tableInfoVO"]
        table = DeskStruct(table_info_vo["deskNo"], "", "", "", "", "", "", "", "", table_info_vo["dealerName"], "",
                           "", "", "", "", table_info_vo["dealerCountry"], table_info_vo["dealerCountryPicture"],
                           "", table_info_vo["identifyStartTime"], table_info_vo["gameStatus"])
        return rtn, table

    @staticmethod
    def exit_room(user_id, room_id):
        """
        离开房间
        :param user_id:
        :param room_id:
        :return:
        """
        params = {
            "userId": user_id,
            "deskNo": room_id,
            "service": "RoomInfoService",
            "function": "leaveRoom",
            "data": None
        }
        live_ws_context.get().send_msg_ws(params)
        return live_ws_context.get().receive_msg_ws("leaveRoom", room_id)

    @staticmethod
    def do_bet(user_id, desk_no, bet_str, game_no, boot_no, get_err=False):
        """
        投注
        :param user_id:
        :param desk_no: 桌号
        :param bet_str: 投注项列表，格式：{"百家乐": "庄免佣-100","龙虎": "龙100", "牛牛/三公": "闲1-庄-平倍-100"}
        :param game_no:
        :param boot_no:
        :param get_err: 是否返回错误信息
        # :param period: 阶段，德州扑克第一次开牌为第1阶段，跟注后的开牌为第2阶段，其他游戏可按此逻辑进行
        :return:
        """
        bet_data = [item.split("-") for item in bet_str.split(",")]
        service = service_dic["龙虎"]
        bet_detail = [{"playType": outcome_dic_dt[data[0]], "betAmount": data[1]} for data in bet_data]
        sum_bet_amount = sum([int(item[-1]) for item in bet_data])
        data = {
            "userId": user_id,
            "deskNo": desk_no,
            "service": service,
            "function": "bet",
            "data": {
                "totalAmount": sum_bet_amount,
                "gameType": 'DT',
                "gameTypeId": 4,
                "betDetail": bet_detail,
                "deskNo": desk_no,
                "gameNo": game_no,
                "bootNo": boot_no}
        }
        for loop in range(1):
            try:
                live_ws_context.get().send_msg_ws(data)
                recv_data = live_ws_context.get().receive_msg_ws("BET_RESULT", game_no=game_no)
                if recv_data["data"]["BET_RESULT"][0]["statusCode"] != 0:
                    if get_err:
                        return recv_data["data"]["BET_RESULT"][0]["message"]
                    if recv_data["data"]["BET_RESULT"][0]["statusCode"] == 9999:
                        time.sleep(0.1)
                        continue
                    else:
                        raise AssertionError("投注失败")
                else:
                    return "投注成功"
            except Exception as e:
                print(str(e))
                time.sleep(0.1)
                continue
        else:
            raise AssertionError("失败")

    @staticmethod
    def receive_bet_result_amount(user_id, desk_no=None, timeout=5, game_no=None):
        """
        接收客户端开奖输赢结果
        :param user_id:
        :param desk_no:
        :param game_no:
        :param timeout:
        :return: 赢的金额，输的金额
        """
        user_wins = live_ws_context.get().receive_msg_ws("noticeSettlementWinLost", desk_no, timeout, game_no=game_no)
        user_wins = user_wins["data"]["noticeSettlementWinLost"][0]["data"]
        if not user_wins["userWins"]:
            return 0, 0
        for item in user_wins["userWins"]:
            if item["userId"] == user_id:
                return item["winAmount"] if item["winAmount"] else 0, abs(item["lostAmount"]) if item[
                    "lostAmount"] else 0

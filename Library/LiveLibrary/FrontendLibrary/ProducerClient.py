#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/11/2 15:30
import datetime
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.LiveLibrary.ServerConnector.Structures import DtGameStruct
from Library.LiveLibrary.CommonUtil import CommonFunc
from Library.LiveLibrary.PublicVariables import value_order_dic, game_type_dic, boot_change_queue_name_dic, \
    open_end_queue_dic, identify_cart_queue_dic
from Library.Common.Utils.Contexts import *
from Library.LiveLibrary.FrontendLibrary.RedisClient import RedisClient
from Library.LiveLibrary.FrontendLibrary.MongoClient import MongoClient


class ProducerClient(object):

    @staticmethod
    def _send_game_data_dt(game_no: str, boot_no: str, table_no: str, is_finish: bool, is_game_finish: bool,
                           dragon_card=None, tiger_card=None, count_down=25, start_time=None, end_time=None,
                           queue_name=None):
        """
        发送龙虎数据
        :param game_no:
        :param boot_no:
        :param table_no:
        :param is_finish:
        :param is_game_finish:
        :param dragon_card: 龙牌型列表字符串,第一个字符为颜色，后面为点数
        :param tiger_card: 虎牌型列表字符串,第一个字符为颜色，后面为点数
        :param count_down: 倒计时
        :param start_time:
        :param end_time:
        :return:
        """
        data = {"gameNo": game_no,
                "bootsNo": boot_no,
                "tableNo": table_no,
                "isFinish": is_finish,
                "countdown": count_down,
                "isGameFinish": is_game_finish,
                "identifyStartTime": start_time,
                "identifyEndTime": end_time,
                "dragonCard": {"pokerPattern": dragon_card[0] if dragon_card else {},
                               "pokerNumber": value_order_dic[dragon_card[1:]]} if dragon_card else {},
                "tigerCard": {"pokerPattern": tiger_card[0] if tiger_card else {},
                              "pokerNumber": value_order_dic[tiger_card[1:]]} if tiger_card else {},
                "gameType": game_type_dic["龙虎"],
                "dealerData": {
                    "dealerCode": "001",
                    "dealerName": "lover",
                    "dealerPicture": "http://192.168.26.24:9000/backend/20538035-d668-48b8-95a6-a8ddfccbcc33.png",
                    "status": "1",
                    "countryId": "1"},
                "ip": "XingYao"
                }
        live_mq_context.get().send_msg(data, queue_name=queue_name)

    def auto_change_boot(self, table_no, limit=60):
        cur_boot_no = RedisClient.get_boot_no(table_no)
        game_count = MongoClient.get_game_count_of_boot(cur_boot_no)
        if game_count > limit:
            self.send_change_boot(table_no)

    def send_game_start_dt(self, table_no: str, count_down: int = 40):
        """
        龙虎发送开局信息
        :param table_no:
        :param count_down:
        :return:
        """
        self.auto_change_boot(table_no)
        next_game_info: DtGameStruct = MongoClient.generate_next_game_info(table_no, "龙虎")
        self._send_game_data_dt(next_game_info.game_no, next_game_info.boot_no, table_no, False, False,
                                count_down=count_down, start_time=next_game_info.start_time,
                                queue_name=open_end_queue_dic["龙虎"])
        return next_game_info.json

    def send_card_identify_dt(self, game_no: str, table_no, boot_no, dragon_card=None, tiger_card=None,
                              is_finish=False, is_game_finish=False, count_down: int = 0):
        """
        龙虎发送牌型识别信息-非终态
        :param game_no:
        :param table_no:
        :param boot_no:
        :param dragon_card: 龙牌型列表字符串,牌之间用","分隔，第一个字符为颜色，后面为点数
        :param tiger_card: 虎牌型列表字符串,牌之间用","分隔，第一个字符为颜色，后面为点数
        :param is_finish:
        :param is_game_finish:
        :param count_down:
        :return:
        """
        start_time = MongoClient.get_latest_game_info(table_no)[3]
        self._send_game_data_dt(game_no, boot_no, table_no, is_finish, is_game_finish, dragon_card, tiger_card,
                                count_down=count_down, start_time=start_time, queue_name=identify_cart_queue_dic["龙虎"])

    def send_game_end_dt(self, game_no: str, table_no, boot_no, dragon_card=None, tiger_card=None,
                         count_down: int = 40):
        """
        龙虎发送局结束信息
        :param game_no:
        :param table_no:
        :param boot_no:
        :param dragon_card: 龙牌型列表,第一个字符为颜色，后面为点数
        :param tiger_card: 虎牌型列表,第一个字符为颜色，后面为点数
        :param count_down:
        :return:
        """
        end_time = (CommonFunc.get_current_time() + datetime.timedelta(seconds=count_down)).strftime("%Y-%m-%dT%H:%M:%S")
        start_time = MongoClient.get_latest_game_info(table_no)[3]
        self._send_game_data_dt(game_no, boot_no, table_no, True, True, dragon_card, tiger_card, count_down,
                                start_time, end_time, queue_name=open_end_queue_dic["龙虎"])

    @staticmethod
    def send_change_boot(table_no: str, game_struct_name="龙虎"):
        """
        发送换靴数据
        :param table_no:
        :param game_struct_name: 百家乐 | 龙虎 | 三公 | 牛牛 | 印度炸金花 | 龙凤炸金花 |
        :return:
        """
        try:
            next_boot_info: DtGameStruct = MongoClient.generate_next_boot_info(table_no, game_struct_name)
        except IndexError:
            return
        data = {"gameNo": next_boot_info.game_no,
                "bootsNo": next_boot_info.boot_no,
                "tableNo": table_no,
                "dealerData": {
                    "dealerCode": "001",
                    "dealerName": "lover",
                    "dealerPicture": "http://192.168.26.24:9000/backend/20538035-d668-48b8-95a6-a8ddfccbcc33.png",
                    "status": "1",
                    "countryId": "1"},
                "ip": "XingYaoNbw"}
        live_mq_context.get().send_msg(data, queue_name=boot_change_queue_name_dic[game_struct_name])
        RedisClient.record_boot_no(table_no, next_boot_info.boot_no)


if __name__ == '__main__':
    env_context.set('sit')
    pc = ProducerClient()

    pc.send_game_start_dt('LH01', 1)
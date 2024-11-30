#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yao x ing
# datetime: 2022/10/24 15:58
import time
import websocket
import requests
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
from Libraries.Common.Utils.CommonUtil import CommonFunc, SingletonType
from Libraries.Config import client_websocket_server_dic
from Libraries.Common.ServerConnector.Structures import WsResponseStruct
from Libraries.Common.Utils.MyExceptions import ConnectWsException


class WebSocketClientBase(object, metaclass=SingletonType):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, env):
        try:
            super().__init__(env)
        except TypeError:
            super(WebSocketClientBase, self).__init__()
        self.env = env
        self.ws = websocket.WebSocket()
        self.ws.settimeout(3)
        self.cf = CommonFunc(env)

    def ws_close(self):
        try:
            self.ws.close()
        except AttributeError:
            pass

    def connect_to_server_short(self, token):
        """
        短连接
        :return:
        """
        try:
            self.ws.connect(f"{client_websocket_server_dic[self.env].ip}{token}")
        except requests.exceptions.ConnectionError:
            raise ConnectWsException()

    def receive_msg_ws(self, event_name, table_no=None, timeout=10, token=None, game_no=None):
        """
        接收消息
        :param event_name: event 名称
        :param table_no:
        :param game_no:
        :param timeout: 等待事件的超时时间，秒
        :param token:
        :return:
        """
        start_time = int(time.time())
        event_name_list = [event_name]
        msg_dic = {item: [] for item in event_name_list}
        retry_times = 1
        while True:
            try:
                _, data = self.ws.recv_data()
                if data:
                    data = self.cf.decrypt(token, data)
                    print(f"收到Websocket消息: {data}")
                    if (table_no and data["deskNo"] != table_no) or (game_no and ('data' in data) and 'gameNo' in
                                                                     data["data"] and data["data"]["gameNo"] != game_no):
                        continue
                    for key in ["command", "function"]:
                        if key in data:
                            for event in event_name_list:
                                if data[key] == event:
                                    msg_dic[event].append(data)
                                    break
                            break
                # 均收到消息后停止
                if not list(filter(lambda var: not msg_dic[var], msg_dic)):
                    return WsResponseStruct(True, msg_dic).json
                if int(time.time()) - start_time >= timeout:
                    raise AssertionError("接收消息超时")
            except TypeError:
                time.sleep(0.1)
            except websocket.WebSocketTimeoutException:
                if retry_times <= 3:
                    retry_times += 1
                else:
                    raise AssertionError("WS消息接收异常：WebSocketTimeoutException")

    def send_msg_ws(self, msg, token):
        """
        发送消息
        :param msg:
        :param token:
        :return:
        """
        print(f"ws发送的消息： {msg}")
        try:
            self.ws.send(self.cf.encrypt(token, msg))
        except Exception as e:
            print(str(e))


if __name__ == "__main__":
    # os.system("sh /Users/yaoxing/PycharmProjects/wsLiveAutoTest/reload.sh")
    client = WebSocketClientBase("sit")
    client.receive_msg_ws('winBlock', 'IG01', game_no='GIG01230630DI1')

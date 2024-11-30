#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/10/24 15:33

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.LiveLibrary.FrontendLibrary.MongoClient import MongoClient
from Library.LiveLibrary.FrontendLibrary.RedisClient import RedisClient
from Library.LiveLibrary.FrontendLibrary.WebSocketClient import WebSocketClient
from Library.LiveLibrary.FrontendLibrary.ProducerClient import ProducerClient
from Library.LiveLibrary.FrontendLibrary.MerchantApi import MerchantApi
from Library.LiveLibrary.FrontendLibrary.MysqlClient import MysqlClient
from Library.LiveLibrary.ServerConnector.Mongo import MongoBase
from Library.LiveLibrary.ServerConnector.Producer import ProducerBase
from Library.LiveLibrary.ServerConnector.Redis import RedisBase
from Library.LiveLibrary.ServerConnector.WebSocket import WebSocketClientBase


class FrontendLibrary(RedisClient, MongoClient, WebSocketClient, ProducerClient, WebSocketClientBase, MerchantApi,
                      MysqlClient):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        MongoBase()
        ProducerBase()
        WebSocketClientBase()
        RedisBase()
        RedisClient.__init__(self)
        WebSocketClient.__init__(self)
        ProducerClient.__init__(self)
        MysqlClient.__init__(self)
        MongoClient.__init__(self)
        WebSocketClientBase.__init__(self)
        MerchantApi.__init__(self)


if __name__ == "__main__":
    from Library.Common.Utils.Contexts import env_context

    env_context.set('sit')
    fl = FrontendLibrary()
    fl.send_game_start_dt('LH01', 1)

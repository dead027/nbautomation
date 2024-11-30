#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yao x ing
# datetime: 2022/11/2 15:30
import time

import pika
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))

from Library.LiveLibrary.CommonUtil import SingletonType
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.Contexts import *


class ProducerBase(object, metaclass=SingletonType):
    def __init__(self):
        server_info = YamlUtil().load_common_config('mq', 'live')
        credentials = pika.PlainCredentials(server_info['username'], server_info['password'])
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server_info['host'], port=server_info['port'], virtual_host='/',
                                      credentials=credentials))
        self.channel = self.connection.channel()
        live_mq_context.set(self)

    def declare_exchange(self, exchange_name, is_broadcast=False):
        if is_broadcast:
            self.channel.exchange_declare(exchange_name, exchange_type="fanout", durable=True)
        else:
            self.channel.exchange_declare(exchange_name)

    def bind_queue(self, exchange_name, queue, routing_key_list=None):
        queue_name = queue.method.queue
        for key in routing_key_list:
            self.channel.queue_bind(queue_name, exchange_name, routing_key=key)

    def send_msg(self, msg, exchange_name="", queue_name=""):
        print(f"mq send : {msg}")
        if exchange_name:
            self.declare_exchange(exchange_name)
        self.channel.queue_declare(queue=queue_name, durable=True)
        self.channel.basic_publish(exchange=exchange_name, routing_key=queue_name, body=json.dumps(msg))

    def receive_msg_mq(self, queue_name, call_back, msg_count=None, auto_ack=True):
        self.channel.queue_declare(queue=queue_name, durable=True)
        if msg_count:
            self.channel.basic_qos(prefetch_count=msg_count)
        self.channel.basic_consume(queue=queue_name, on_message_callback=call_back, auto_ack=auto_ack)
        self.channel.start_consuming()


#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yao x ing
# datetime: 2022/11/2 15:30

import pika
import json
from Library.Common.ServerConnector.Structures import ServerStruct

rabbit_mq_server_dic = {"dev": ServerStruct("192.168.26.220", 5672, "baowang", "doYejJnmUerc", ""),
                        "prod": ServerStruct("192.168.26.220", 5672, "guest", "guest", ""),
                        "sit": ServerStruct("192.168.26.220", 5673, "bwsit", "doYejJnmUerc", "")}


class ProducerBase(object):
    def __init__(self, env):
        self.env = env
        server: ServerStruct = rabbit_mq_server_dic[self.env]
        credentials = pika.PlainCredentials(server.user_name, server.password)
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=server.ip, port=server.port, virtual_host='/', credentials=credentials))
        self.channel = self.connection.channel()

    def declare_exchange(self, exchange_name, is_broadcast=False):
        if is_broadcast:
            self.channel.exchange_declare(exchange_name, exchange_type="fanout", durable=False)
        else:
            self.channel.exchange_declare(exchange_name, durable=True)

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




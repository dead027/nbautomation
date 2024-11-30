#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/9 12:08
from contextvars import ContextVar

ms_context = ContextVar('Mysql instance')
rds_context = ContextVar('Redis instance')
backend_context = ContextVar('backend instance')
client_context = ContextVar('Client instance')
agent_context = ContextVar('Agent instance')
header_backend_context = ContextVar('master backend header')
header_site_context_1 = ContextVar('site 1 backend header')
header_site_context_2 = ContextVar('site 1 backend header')
header_agent_context_1 = ContextVar('agent 1 header')
header_agent_context_2 = ContextVar('agent 2 header')
header_client_context_1 = ContextVar('client 1 header')
header_client_context_2 = ContextVar('client 2 header')
agent_token_context = ContextVar('Agent token')
client_token_context = ContextVar('Client token')
yaml_context = ContextVar('Yaml config file data instance')
env_context = ContextVar('env name')
# 沙巴
sb_client_context = ContextVar('sb client instance')
sb_client_header_context = ContextVar('sb header')
sb_token_context = ContextVar('sb token')
# xxl job
job_token_context = ContextVar('xxl job token')
job_client_header_context = ContextVar('job header')
# live
live_ms_context = ContextVar('')
live_mg_context = ContextVar('')
live_rds_context = ContextVar('')
live_ws_context = ContextVar('')
live_mq_context = ContextVar('')


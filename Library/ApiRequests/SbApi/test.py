#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/22 11:09

from Library.Common.Utils.Contexts import *
from Library.ApiRequests.SbApi.BaseOperation import BaseOperation
from Library.ApiRequests.SbApi.BusinessOperation import BusinessOperation
from Library.ApiRequests.SbApi.Display import Display


env_context.set('sit')
BusinessOperation.running_status.set()
BaseOperation.login_sb('xy2')
# BaseOperation.login_sb('xingyao1')

sport_dic_t_zh = {"1": "足球", "2": "篮球", "3": "美式足球", "4": "冰上曲棍球", "5": "网球", "6": "排球", "7": "斯诺克",
                  "8": "棒球", "9": "羽毛球", "43": "电子竞技"}

# 首页
sport_type = sport_dic_t_zh['3']
# 1.上方计数:   sport_name, date_type, league_name="", event_id="", start_diff=0, end_diff=6
# Display.front('今日', start_diff=0, end_diff=0)
# Display.front('今日未开赛', start_diff=0, end_diff=0)
# Display.front('滚球')
# Display.front('早盘', start_diff=1, end_diff=1)
# Display.front('冠军')
# 2.联赛列表  sport_name, date_type, league_name="", event_id="", start_diff=0, end_diff=6
# Display.get_main_page_league_list(sport_type, date_type='滚球', ignore_sport_type='否')
# Display.get_main_page_league_list(sport_type, start_diff=0, end_diff=15)
# Display.get_main_page_league_list(sport_type, date_type='滚球', start_diff=0, end_diff=0, ignore_sport_type='否')
# 3.大厅列表 sport_name, date_type, league_name="", event_id=None, start_diff=0, end_diff=6

# 今日滚球
# Display.main_page(sport_type, '滚球')
# Display.main_page(sport_type, '滚球', event_id=94851034)
# 今日未开赛
# Display.main_page(sport_type, '今日')
# Display.main_page(sport_type, '今日', grep_not_live=True)
# Display.main_page(sport_type, '今日', grep_not_live=True, event_id=93888596)
# 早盘
# Display.main_page(sport_type, '早盘')
# Display.main_page(sport_type, '早盘', start_diff=8)
# Display.main_page(sport_type, '早盘', start_diff=5, end_diff=5)
# Display.main_page(sport_type, '早盘', event_id=93364450)
# 冠军
# Display.main_page_champion(sport_type)
# Display.main_page_champion(sport_type, '2024/2025 英格兰冠军联赛 - 最终首两名')

# 今日滚球-热门
# Display.main_page(sport_type, '滚球', only_hot=True)
# 今日 未开赛 热门
# Display.main_page(sport_type, '今日', grep_not_live=True, only_hot=True)
# 早盘 热门
Display.main_page(sport_type, '早盘', only_hot=True)
# Display.main_page(sport_type, '早盘', only_hot=True, start_diff=2, end_diff=2)
# 5.比赛详情  event_id
# Display.get_match_detail_page(95229383)
# 6.比赛详情页获取联赛下所有比赛列表
# Display.get_event_list_of_league(93330744)
# 7.赛果数量
# BusinessOperation.get_sport_results(0, 0)
# 8.赛果查询
# print(Display.get_event_result(sport_type, start_diff=-6))
# 9.公告
# Display.get_announcement()

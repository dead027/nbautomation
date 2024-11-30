#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/4 12:45
filter_key_dic = {"联赛id": "leagueid",
                  "体育项目名称": 'sportType',
                  "联赛名称": 'leagueName',
                  '赛事id': 'eventId',
                  '盘口id': 'marketId',
                  '是否为滚球赛事': 'isLive',
                  '赛事状态': 'eventStatus',  # running / suspend 暂停 / postponed 推迟 / deleted
                  '盘口状态': 'marketStatus',  # running / suspend / closePrice / closed
                  '投注类型': 'betType',
                  'category': 'category',  # 0主要 1全场 2半场 3角球/罚牌 6选手 7快速盘口 8节 9加时 10点球
                  '串关数量限制': 'combo',  # 0不支持串关 2至少2个 3.4...10
                  '是否是虚拟赛事': 'isVirtualEvent',  # true | false
                  "是否为测试赛事": 'isTest',
                  "视频代码": "channelCode",  # ne null
                  "该体育项目的滚球赛事数量": "liveGameCount",
                  "包括的盘口": "includeMarkets",
                  "游戏状态": 'gameStatus'
                  }


class SbFilterUtil(object):

    @staticmethod
    def generate_query_str(filter_dic=None, limit: int = None, skip: int = None):
        """
        生成沙巴过滤字符串
        @param filter_dic: {'字段名': 过滤字符串} 其中:
                            字段名包括：leagueName，

                            运算符包括: eq,ne,lt,le,gt,ge,
                                in: $filter=sporttype in (1,2)
                                or:$filter=sporttype eq 1 or sporttype eq 2
                                and:$filter=sporttype eq 1 and isparlay eq true
                                contains:1. 基本用法：$filter=contains(leagueName,'NBA')，预设使用?language之语系进行过滤
                                        2. 当需要过滤指定关键字的时候，需使用 eq false
                                            e.g. $filter=contains(leaguename, 'NBA') eq false
                                        3. 如果需要过滤的“name”​​字段，语系与?language 不同，可使用“/”切换语言类型
                                            e.g. ?query=$filter=contains(leaguename/cs, '罚牌') eq false&language=en
                                $filter=contains(toupper(leagueName/en), toupper('nba')) 转大写进行比对
                                $filter=contains(tolower(leagueName/en), tolower('nba')) 转小写进行比对
        @param order_by_dic: {"key": 'desc or asc'}，只传一个
        @param limit: 指定仅回传前几笔信息
        @param skip: 指定略过前几笔信息
        @return:
        """
        query_str = ''

        if filter_dic:
            query_str += f'$filter=' + ' and '.join([f'{filter_key_dic[key]} {value}' for key, value in
                                                     filter_dic.items() if key != '包括的盘口'])
        if limit:
            query_str += f'&$top={limit}'
        # if order_by_dic:
        #     items = order_by_dic.items()
        #     query_str += f'&orderby={items[0][0]} {items[0][1]}'

        if skip:
            query_str += f'&$Skip={skip}'
        if '包括的盘口' in filter_dic:
            query_str += f'&includeMarkets=$filter=bettype in ({filter_dic["包括的盘口"]})'
        return query_str

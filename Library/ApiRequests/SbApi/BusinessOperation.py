#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/1 16:35
import json
import time
from queue import Queue
from collections import defaultdict
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.Contexts import *
from Library.Common.Utils.SbFilterUtil import SbFilterUtil
from Library.Common.Enum.SbSportEnum import SbSportEnum
import requests
import threading

headers_stream = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'text/event-stream',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/123.0.0.0 Safari/537.36',
    "Sign": "",
    "Accept-Encoding": 'br,gzip,deflate',
    "Accept-Language": "zh-CN,zh;q=0.9"
}


class BusinessOperation(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    event = threading.Event()
    stream_type = None
    running_status = threading.Event()
    thread = None
    event_queue = Queue()
    market_queue = Queue()
    sports_queue = Queue()
    league_queue = Queue()
    out_right_queue = Queue()
    event_list = [dict()] * 30
    out_rights_list = [dict()] * 30

    @staticmethod
    def start_stream(stream_type, kwargs):
        stream_type_dic = {"sports": BusinessOperation.get_sports_sse,
                           "leagues": BusinessOperation.get_leagues_sse,
                           "markets": BusinessOperation.get_markets_sse,
                           "events": BusinessOperation.get_events_sse,
                           'champion': BusinessOperation.get_out_rights_sse,
                           'league_list': BusinessOperation.get_leagues}
        BusinessOperation.running_status.set()
        BusinessOperation.thread = threading.Thread(target=stream_type_dic[stream_type], kwargs=kwargs, daemon=True)
        BusinessOperation.thread.start()

    @staticmethod
    def stop_stream():
        BusinessOperation.running_status.clear()

    @staticmethod
    def get_sports():
        """
        获取每个运动项目的赛事数量及串关赛事数量
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetSports'
        params = {"language": "zhcn",
                  'token': sb_token_context.get(),
                  "query": "",
                  'filter': 'sportType in (1,2,3,4,5,6,7,8,9,43) and isLive eq true',
                  "$skip": 750}
        resp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()['sports']
        result_list = []
        for item in resp:
            if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                # print(item)
                result_list.append({"体育类型": item['sportType'], "非滚球赛事数量": item['gameCount'],
                                    "滚球数量": item['liveGameCount'], "滚球串关赛事数量": item['liveParlayGame'],
                                    "非滚球串关赛事数量": item['parlayGame'], "优胜冠军赛事数量": item['outrightGame']})
        return result_list

    @staticmethod
    def get_leagues(filter_dic=None, start_diff=None, end_diff=None):
        """
        获取每个联赛中的赛事数量
        @param filter_dic:
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetLeagues'
        params = {"language": "zhcn",
                  'token': sb_token_context.get()}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_utc_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_utc_search_time(end_diff, is_end=True)
        if filter_dic:
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        print(params)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        data = rsp['leagues']

        result_list = []
        for item in data:
            if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                # print(item)
                result_list.append({"体育类型": item['sportType'], "联赛名称": item['leagueName'],
                                    "非滚球赛事数量": item['gameCount'], "滚球数量": item['liveGameCount'],
                                    "是否支持串关": '是' if item['isParlay'] else '否'})
            else:
                break
        return result_list

    @staticmethod
    def get_markets(event_id=None, start_diff=0, end_diff=0):
        """
        获取盘口相关信息
        @param event_id:
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetMarkets'
        params = {"language": "zhcn",
                  'token': sb_token_context.get()}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_utc_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_utc_search_time(end_diff, is_end=True)
        if event_id:
            params["query"] = SbFilterUtil.generate_query_str({'赛事id': f' eq {event_id}'})
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        print(params)
        # print(rsp)
        data = rsp['markets']
        result_list = []
        for item in data:
            if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                sub_data = {"体育项目ID": item['sportType'], "赛事ID": item['eventId'], "投注类型": item['betType'],
                            "投注类型名称": item['betTypeName'], "盘口ID": item['marketId'], "最大投注限额": item['maxBet'],
                            "是否为滚球赛事": item['isLive'], "盘口状态": item['marketStatus'],
                            "投注类型分类": item['category'], "赛事串关数量限制": item['combo'],
                            "盘口赔率项目列表": [{"投注类型选项": selection['key'], "投注类型选项名称": selection['keyName'],
                                          "球头": selection['point'],
                                          "赔率相关信息": selection['oddsPrice']['decimalPrice']} for selection in
                                         item['selections']]}
                result_list.append(sub_data)
            else:
                break
        return result_list

    @staticmethod
    def get_period_str(sport_name, event_data):
        sport_name = SbSportEnum.sport_dic_t_zh.value[sport_name]
        period_str = f'未开赛:{DateUtil.convert_utc_time_to_local(event_data["开赛时间"])}'
        event_info = event_data['球赛相关信息']
        if sport_name == '足球':
            if event_info['目前进行到第几节'] == 0 and event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '延迟开赛'
            elif event_info['目前进行到第几节'] == 0 and not event_info['赛事是否延迟'] and event_info['是否为中场休息']:
                period_str = '中场休息'
            elif event_info['目前进行到第几节'] == 1 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '上半场'
            elif event_info['目前进行到第几节'] == 2 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '下半场'
            elif event_info['目前进行到第几节'] == 0 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '点球'
            else:
                period_str = f"三方数据不正常： {event_info['目前进行到第几节']},{event_info['赛事是否延迟']}," \
                             f"{event_info['是否为中场休息']}"
        elif sport_name == '篮球':
            if event_info['目前进行到第几节'] == 0 and event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '延迟开赛'
            elif event_info['目前进行到第几节'] == 0 and not event_info['赛事是否延迟'] and event_info['是否为中场休息']:
                period_str = '中场休息'
            elif event_info['目前进行到第几节'] == 99 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '加时赛'
            elif event_info['目前进行到第几节'] == 1 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '第1节'
            elif event_info['目前进行到第几节'] == 2 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '第2节'
            elif event_info['目前进行到第几节'] == 3 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '第3节'
            elif event_info['目前进行到第几节'] == 4 and not event_info['赛事是否延迟'] and not event_info['是否为中场休息']:
                period_str = '第4节'
            else:
                period_str = f"三方数据不正常： {event_info['目前进行到第几节']},{event_info['赛事是否延迟']}," \
                             f"{event_info['是否为中场休息']}"
        elif sport_name == '排球':
            if "排球相关信息" in event_data:
                period_str = f'第{event_data["排球相关信息"][0]["目前进行的节数"]}局'
        elif sport_name == '网球':
            period_str = f'第{event_data["网球相关信息"]["目前盘数"]}盘进行中'
        elif sport_name == '羽毛球':
            period_str = f'第{event_info["目前进行到第几节"]}局'
        elif sport_name == '冰上曲棍球' and event_data["是否为滚球赛事"]:
            period_str = f'第{event_info["目前进行到第几节"]}节'
        elif sport_name in ('电子竞技', '冰上曲棍球', '斯诺克', '美式足球') and event_data["是否为滚球赛事"] and \
                event_info["目前进行到第几节"] > 0:
            period_str = f'第{event_info["目前进行到第几节"]}局'
        elif sport_name == '斯诺克':
            pass
        elif sport_name == '棒球':
            if "棒球相关信息" in event_data:
                period_str = f'第{event_data["棒球相关信息"]["目前局数"]}局'
            # # 有 棒球相关信息 就是滚球了，同时"是否为滚球赛事"的值也会变为True
            # if event_data['是否为滚球赛事']:
            #     if "棒球相关信息" in event_data:
            #         period_str = f'第{event_data["棒球相关信息"]["目前局数"]}局'
            #     else:
            #         period_str = f'转滚球中: {DateUtil.convert_utc_time_to_local(event_data["开赛时间"])}'
            # else:
            #     period_str = f"{DateUtil.convert_utc_time_to_local(event_data['开赛时间'])}"
        elif sport_name in ("手球", "橄榄球"):
            if event_info['目前进行到第几节'] == 0 and event_info['是否为中场休息']:
                period_str = '中场休息'
            elif event_info['目前进行到第几节'] == 1 and not event_info['是否为中场休息']:
                period_str = '上半场'
            elif event_info['目前进行到第几节'] == 2 and not event_info['是否为中场休息']:
                period_str = '下半场'
        elif sport_name == '冰上曲棍球':
            period_str = f"第{event_info['目前进行到第几节']}节"
        return period_str

    @staticmethod
    def get_out_rights(filter_dic=None, start_diff=None, end_diff=None):
        """
        获取优胜冠军赛事信息
        @param filter_dic:
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetOutrights'
        params = {"language": "zhcn",
                  'token': sb_token_context.get()}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_utc_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_utc_search_time(end_diff, is_end=True)
        if filter_dic:
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        print(params)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        data = rsp['outrights']

        result_list = []
        for item in data:
            if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                # print(item['teams'])
                result_list.append({"体育类型": item['sportType'], "联赛名称": item['leagueName'],
                                    "赛事标识符": item['eventCode'], "指定联赛的显示模式": item['lDisplayMode'],
                                    "赛事日期": item['eventDate'], "优胜冠军状态": item['outrightStatus'],
                                    "优胜冠军联赛群组": item['leagueGroup'],
                                    "队伍相关信息": [{"优胜冠军赔率ID": team['orid'],
                                                "队伍ID": team['teamId'], "队伍名称": team['teamName'],
                                                "赔率": team['price'], "最大投注额": team['maxBet'],
                                                "盘口状态": team['oddsStatus'],
                                                "赔率使否异动": team['isUpdate']} for team in item['teams']]})
        return result_list

    @staticmethod
    def get_hot_events():
        """
        获取熱門赛事相关信息包含依熱門成度排序之盘口信息
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetHotEvents'
        params = {"language": "zhcn",
                  'token': sb_token_context.get()}
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()

        result_list = []
        for item in rsp:
            event_data = item['event']
            markets_data = item['markets']

            sub_event_info = {"体育项目": event_data["sportType"], "联赛ID": event_data["leagueId"],
                              "联赛名称": event_data["leagueName"], "赛事ID": event_data["eventId"],
                              "赛事代码": event_data["eventCode"], "赛事状态": event_data["eventStatus"],
                              "是否为主要盘口": event_data["isMainMarket"], "系统开赛时间": event_data["kickOffTime"],
                              "开赛时间": event_data["globalShowTime"], "赛事比赛有多少节": event_data["gameSession"],
                              "该赛事的母赛事ID": event_data["parentId"], "是否为滚球赛事": event_data["isLive"],
                              "是否为串关赛事": event_data["isParlay"], "赛事是否支持实时兑现": event_data["isCashout"],
                              "是否为虚拟赛事": event_data["isVirtualEvent"], "是否有滚球盘口": event_data["hasLiveMarket"],
                              "该赛事的所有盘口数量": event_data["marketCount"],
                              "该赛事的所有盘口投注类型": event_data["marketCategories"],
                              "视频ID": event_data["streamingOption"], "网球相关信息": event_data["tennisInfo"],
                              '团队相关信息': {"主队ID": event_data["teamInfo"]["homeId"],
                                         "主队名称": event_data["teamInfo"]["homeName"],
                                         "客队ID": event_data["teamInfo"]["awayId"],
                                         "客队名称": event_data["teamInfo"]["awayName"]},
                              '球赛相关信息': {"目前进行到第几节": event_data["gameInfo"]["livePeriod"],
                                         "当前赛事时间以秒为单位": event_data["gameInfo"]["seconds"],
                                         "是否为中场休息": event_data["gameInfo"]["isHt"],
                                         "赛事是否中断(休息时间)": event_data["gameInfo"]["isBreak"],
                                         "赛事是否关闭": event_data["gameInfo"]["isClosed"],
                                         "赛事是否延迟": event_data["gameInfo"]["delayLive"],
                                         "球赛状态": event_data["gameInfo"]["gameStatus"],
                                         "目前赛事时间": event_data["gameInfo"]["inPlayTime"],
                                         "主队滚球分数": event_data["gameInfo"]["liveHomeScore"],
                                         "客队滚球分数": event_data["gameInfo"]["liveAwayScore"]}}
            if event_data["soccerInfo"]:
                sub_event_info["足球相关信息"] = {"主场红牌数": event_data["soccerInfo"]['homeRedCard'],
                                            "客场红牌数": event_data["soccerInfo"]['awayRedCard'],
                                            "主场黄牌数": event_data["soccerInfo"]['homeYellowCard'],
                                            "客场黄牌数": event_data["soccerInfo"]['awayYellowCard']}
            if event_data['tennisInfo']:
                sub_event_info["网球相关信息"] = {"主队每盘获得局数": event_data['tennisInfo']["homeGameScore"],
                                            "客队每盘获得局数": event_data['tennisInfo']["awayGameScore"],
                                            "主队目前局数比分": event_data['tennisInfo']["homePointScore"],
                                            "客队目前局数比分": event_data['tennisInfo']["awayPointScore"],
                                            "目前盘数": event_data['tennisInfo']["currentSet"],
                                            "目前发球方": event_data['tennisInfo']["currentServe"]}

            if event_data['beachVolleyBallInfo']:
                sub_event_info["沙滩排球相关信息"] = {"主队每盘获得局数": event_data["beachVolleyBallInfo"]['homeGameScore'],
                                              "客队每盘获得局数": event_data["beachVolleyBallInfo"]['awayGameScore'],
                                              "目前盘数": event_data["beachVolleyBallInfo"]['currentSet'],
                                              "目前发球方": event_data["beachVolleyBallInfo"]['currentServe'],
                                              "哪支队伍有人受伤": event_data["beachVolleyBallInfo"]['playerInjury'],
                                              "是否为雨天": event_data["beachVolleyBallInfo"]['isRain']},
            if event_data['eSportInfo']:
                sub_event_info["电子竞技相关信息"] = {"标识会打几个地图": event_data["eSportInfo"]['bestOfMap'],
                                              "是否即将开赛": event_data["eSportInfo"]['isStartingSoon'],
                                              "游戏名称": event_data["eSportInfo"]['overTimeSession'],
                                              "电子竞技联赛名称": event_data["eSportInfo"]['leagueGroup'],
                                              "电子竞技联赛ID": event_data["eSportInfo"]['leagueGroupId']}
            if event_data['basketballInfo']:
                sub_event_info["篮球相关信息"] = {"主队目前得分": event_data["basketballInfo"]['homeGameScore'],
                                            "客队目前得分": event_data["basketballInfo"]['awayGameScore'],
                                            "目前进行节数": event_data["basketballInfo"]['latestLivePeriod'],
                                            "主隊延長賽得分": event_data["basketballInfo"]['homeOverTimeScore'],
                                            "客队延长赛得分": event_data["basketballInfo"]['awayOverTimeScore']}
            if event_data['baseballInfo']:
                sub_event_info["棒球相关信息"] = {"主队目前得分": event_data["baseballInfo"]['homeGameScore'],
                                            "客队目前得分": event_data["baseballInfo"]['awayGameScore'],
                                            "主隊延長賽比分": event_data["baseballInfo"]['homeOverTimeScore'],
                                            "客队延长赛比分": event_data["baseballInfo"]['awayOverTimeScore'],
                                            "垒上是否有跑者": event_data["baseballInfo"]['baseHasRunner'],
                                            "目前局数": event_data["baseballInfo"]['currentInning'],
                                            "目前打击队伍": event_data["baseballInfo"]['currentBattingTeam'],
                                            "目前出局数": event_data["baseballInfo"]['currentOuts']}

            if event_data['volleyballInfo']:
                sub_event_info["排球相关信息"] = {"主队每盘获得局数": event_data['volleyballInfo']["homeGameScore"],
                                            "客队每盘获得局数": event_data['volleyballInfo']["awayGameScore"],
                                            "主队目前总比分": event_data['volleyballInfo']["homePointScore"],
                                            "客队目前总比分": event_data['volleyballInfo']["awayPointScore"],
                                            "目前发球方": event_data['volleyballInfo']["currentServe"],
                                            "主队目前比分": event_data['volleyballInfo']["homeCurrentPoint"],
                                            "客队目前比分": event_data['volleyballInfo']["awayCurrentPoint"],
                                            "哪支队伍有人受伤": item['volleyballInfo']["playerInjury"],
                                            "目前进行的节数": item['volleyballInfo']["latestLivePeriod"]},
            if 'footballInfo' in event_data and event_data['footballInfo']:
                sub_event_info["美式足球相关信息"] = {"主队每盘获得局数": event_data['footballInfo']["homeGameScore"],
                                              "客队每盘获得局数": event_data['footballInfo']["awayGameScore"],
                                              "主队目前总比分": event_data['footballInfo']["homeCurrentPoint"],
                                              "客队目前总比分": event_data['footballInfo']["awayCurrentPoint"],
                                              "主隊延長賽比分": event_data['footballInfo']["homeOverTimeScore"],
                                              "客隊延長賽比分": event_data['footballInfo']["awayOverTimeScore"]},
            if event_data['tableTennisInfo']:
                sub_event_info["桌球相关信息"] = {"主队每盘获得局数": event_data["tableTennisInfo"]['homeGameScore'],
                                            "客队每盘获得局数": event_data["tableTennisInfo"]['awayGameScore'],
                                            "主队目前比分": event_data["tableTennisInfo"]['homeCurrentPoint'],
                                            "客队目前比分": event_data["tableTennisInfo"]['awayCurrentPoint'],
                                            "主队获得盘数": event_data["tableTennisInfo"]['homeSetScore'],
                                            "客队获得盘数": event_data["tableTennisInfo"]['awaySetScore'],
                                            "哪支队伍有人受伤": event_data["tableTennisInfo"]['playerInjury'],
                                            "目前盘数": event_data["tableTennisInfo"]['CurrentSet'],
                                            "目前发球方": event_data["tableTennisInfo"]['currentServe']},
            if event_data['badmintonInfo']:
                sub_event_info["羽球相关信息"] = {"主队每盘获得局数": event_data["badmintonInfo"]['homeGameScore'],
                                            "客队每盘获得局数": event_data["badmintonInfo"]['awayGameScore'],
                                            "主队目前比分": event_data["badmintonInfo"]['homeCurrentPoint'],
                                            "客队目前比分": event_data["badmintonInfo"]['awayCurrentPoint'],
                                            "主队获得盘数": event_data["badmintonInfo"]['homeSetScore'],
                                            "客队获得盘数": event_data["badmintonInfo"]['awaySetScore'],
                                            "哪支队伍有人受伤": event_data["badmintonInfo"]['playerInjury'],
                                            "目前盘数": event_data["badmintonInfo"]['CurrentSet'],
                                            "目前发球方": event_data["badmintonInfo"]['currentServe']}

            sub_markets_data = [{"体育项目ID": market['sportType'], "赛事ID": market['eventId'],
                                 "投注类型": market['betType'], "投注类型名称": market['betTypeName'],
                                 "盘口ID": market['marketId'], "最大投注限额": market['maxBet'],
                                 "是否为滚球赛事": market['isLive'], "盘口状态": market['marketStatus'],
                                 "投注类型分类": market['category'], "赛事串关数量限制": market['combo'],
                                 "盘口赔率项目列表": [{"投注类型选项": selection['key'],
                                               "投注类型选项名称": selection['keyName'], "球头": selection['point'],
                                               "赔率相关信息": selection['oddsPrice']['decimalPrice']} for selection in
                                              market['selections']]} for market in markets_data]
            result_list.append((sub_event_info, sub_markets_data))
        return result_list

    @staticmethod
    def get_sports_sse(start_diff=None, end_diff=None, env="", token=""):
        """
        建立连接，获取每个运动项目的赛事数量及串关赛事数量
        @param start_diff:
        @param end_diff:
        @param env:
        @param token:
        @return:
        """
        if env:
            env_context.set(env)
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetSports'
        params = {"language": "zhcn",
                  'token': sb_token_context.get() if not token else token,
                  "query": "",
                  'filter': 'sportType in (1,2,3,4,5,6,7,8,9,43) and isLive ne true',
                  "$skip": 750}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_utc_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_utc_search_time(end_diff, is_end=True)
        client = requests.get(url, params=params, stream=True, headers=headers_stream)
        print("1------")
        print(url)
        print(params)
        print("*" * 50)
        full_data = defaultdict(dict)
        while BusinessOperation.running_status.is_set():
            for chunk in client.iter_lines(decode_unicode=False):
                if BusinessOperation.running_status.is_set():
                    msg = chunk.decode().strip()
                    if 'payload' in msg:
                        data = json.loads(msg[6:])

                        for item in data['payload']['sports']['add'] + data['payload']['sports']['change']:
                            # 平台需要的类型
                            if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                                sport_name = SbSportEnum.sport_dic_t_zh.value[str(item['sportType'])]
                                full_data[sport_name] = {
                                    "体育类型": SbSportEnum.sport_dic_t_zh.value[str(item['sportType'])],
                                    "非滚球赛事数量": item['gameCount'],
                                    "滚球数量": item['liveGameCount'],
                                    "滚球串关赛事数量": item['liveParlayGame'],
                                    "非滚球串关赛事数量": item['parlayGame'],
                                    "优胜冠军赛事数量": item['outrightGame']}
                        BusinessOperation.sports_queue.put(full_data)
                else:
                    break

    @staticmethod
    def get_events_sse(filter_dic, start_diff=None, end_diff=None, only_hot=False, env="", token="", page=1,
                       header=None):
        """
        建立连接，获取赛事相关信息包含部分盘口信息
        :param event_id
        :param env
        :param token
        :param only_hot:  只要热门  False | True
        :param filter_dic: 至少要包括对体育类型的筛选
        @return:
        """
        if env:
            env_context.set(env)
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetEvents'
        params = {"language": "zhcn",
                  'token': sb_token_context.get() if not token else token,
                  'orderby': 'globalShowTime asc'}
        # if page - 1 > 0:
        #     params['skip'] = (page - 1) * 250
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_utc_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_utc_search_time(end_diff, is_end=True)
        # 热门
        if only_hot:
            id_list = BusinessOperation._get_hot_event_list(sport_id_str=filter_dic['体育项目名称'], header=header)
            filter_dic['赛事id'] = f' in ({",".join(id_list)})'
            # print(id_list)

        params['query'] = SbFilterUtil.generate_query_str(filter_dic, skip=(page - 1) * 250)
        print("============")
        print(params)
        client = requests.get(url, params=params, stream=True, headers=headers_stream)

        events_dic = {}
        market_event_dic = {}  # market id 与 event的映射关系
        is_next_page_generated = False
        # while BusinessOperation.running_status.is_set():
        while True:
            time.sleep(0.6)
            for chunk in client.iter_lines(decode_unicode=False):
                if BusinessOperation.running_status.is_set():
                    msg = chunk.decode().strip()
                    if 'payload' in msg:
                        # print(msg)
                        # print("=================")
                        is_changed = False
                        data = json.loads(msg[6:])
                        if data['payload']['events']['add'] + data['payload']['events']['change']:
                            for item in data['payload']['events']['add'] + data['payload']['events']['change']:
                                # print(item)
                                is_changed = True
                                event_id = item["eventId"]
                                if 'sportType' in item:
                                    sub_info = {"赛事ID": event_id,
                                                "赛事状态": item["eventStatus"],
                                                "开赛时间": item["globalShowTime"],
                                                "是否有滚球盘口": item["hasLiveMarket"],
                                                "该赛事的所有盘口数量": item["marketCount"],
                                                "该赛事的所有盘口投注类型": item["marketCategories"],
                                                '球赛相关信息': {"目前进行到第几节": item["gameInfo"]["livePeriod"],
                                                           # "赛事时间计算方式": item["gameInfo"]["clockDirection"],
                                                           "当前赛事时间以秒为单位": item["gameInfo"]["seconds"],
                                                           "是否为中场休息": item["gameInfo"]["isHt"],
                                                           "赛事是否中断(休息时间)": item["gameInfo"]["isBreak"],
                                                           "赛事是否关闭": item["gameInfo"]["isClosed"],
                                                           "赛事是否延迟": item["gameInfo"]["delayLive"],
                                                           "球赛状态": item["gameInfo"]["gameStatus"],
                                                           "目前赛事时间": item["gameInfo"]["inPlayTime"],
                                                           "主队滚球分数": item["gameInfo"]["liveHomeScore"],
                                                           "客队滚球分数": item["gameInfo"]["liveAwayScore"]},
                                                "盘口赔率项目列表": []}
                                else:
                                    sub_info = events_dic[event_id]
                                    sub_info['球赛相关信息']['主队滚球分数'] = item["gameInfo"]["liveHomeScore"]
                                    sub_info['球赛相关信息']['客队滚球分数'] = item["gameInfo"]["liveAwayScore"]
                                    sub_info['球赛相关信息']['目前进行到第几节'] = item["gameInfo"]["livePeriod"]
                                    sub_info['球赛相关信息']['当前赛事时间以秒为单位'] = item["gameInfo"]["seconds"]
                                    sub_info['球赛相关信息']['是否为中场休息'] = item["gameInfo"]["isHt"]
                                    sub_info['球赛相关信息']['赛事是否中断(休息时间)'] = item["gameInfo"]["isBreak"]
                                    sub_info['球赛相关信息']['赛事是否关闭'] = item["gameInfo"]["isClosed"]
                                    sub_info['球赛相关信息']['赛事是否延迟'] = item["gameInfo"]["delayLive"]
                                    sub_info['球赛相关信息']['球赛状态'] = item["gameInfo"]["gameStatus"]
                                    sub_info['球赛相关信息']['目前赛事时间'] = item["gameInfo"]["inPlayTime"]
                                    sub_info['赛事状态'] = item["eventStatus"]
                                    sub_info['是否有滚球盘口'] = item["hasLiveMarket"]
                                    sub_info['该赛事的所有盘口数量'] = item["marketCount"]
                                    sub_info['该赛事的所有盘口投注类型'] = item["marketCategories"]
                                # add有下面的属性，update没有
                                if "sportType" in item:
                                    sub_info["体育项目"] = SbSportEnum.sport_dic_t_zh.value[str(item['sportType'])]
                                    sub_info["联赛ID"] = item['leagueId']
                                    sub_info["联赛名称"] = item['leagueName']
                                    sub_info["赛事代码"] = item['eventCode']
                                    sub_info["是否为主要盘口"] = item['isMainMarket']
                                    sub_info["系统开赛时间"] = item['kickOffTime']
                                    sub_info["赛事比赛有多少节"] = item['gameSession']
                                    sub_info["该赛事的母赛事ID"] = item['parentId']
                                    sub_info["是否为滚球赛事"] = item['isLive']
                                    sub_info["是否为串关赛事"] = item['isParlay']
                                    sub_info["赛事是否支持实时兑现"] = item['isCashout']
                                    sub_info["是否为虚拟赛事"] = item['isVirtualEvent']
                                    sub_info["视频代码"] = item['channelCode']
                                    sub_info["视频ID"] = item['streamingOption']
                                    sub_info["团队相关信息"] = {"主队ID": item["teamInfo"]["homeId"],
                                                          "主队名称": item["teamInfo"]["homeName"],
                                                          "客队ID": item["teamInfo"]["awayId"],
                                                          "客队名称": item["teamInfo"]["awayName"]}
                                if 'soccerInfo' in item and item["soccerInfo"]:
                                    sub_info["足球相关信息"] = {"主场红牌数": item["soccerInfo"]['homeRedCard'],
                                                          "客场红牌数": item["soccerInfo"]['awayRedCard'],
                                                          "主场黄牌数": item["soccerInfo"]['homeYellowCard'],
                                                          "客场黄牌数": item["soccerInfo"]['awayYellowCard']}
                                if 'tennisInfo' in item and item['tennisInfo']:
                                    sub_info["网球相关信息"] = {"主队每盘获得局数": item['tennisInfo']["homeGameScore"],
                                                          "客队每盘获得局数": item['tennisInfo']["awayGameScore"],
                                                          "主队目前局数比分": item['tennisInfo']["homePointScore"],
                                                          "客队目前局数比分": item['tennisInfo']["awayPointScore"],
                                                          "目前盘数": item['tennisInfo']["currentSet"],
                                                          "目前发球方": item['tennisInfo']["currentServe"]}

                                if 'beachVolleyBallInfo' in item and item['beachVolleyBallInfo']:
                                    sub_info["沙滩排球相关信息"] = {"主队每盘获得局数": item["beachVolleyBallInfo"]['homeGameScore'],
                                                            "客队每盘获得局数": item["beachVolleyBallInfo"]['awayGameScore'],
                                                            "目前盘数": item["beachVolleyBallInfo"]['currentSet'],
                                                            "目前发球方": item["beachVolleyBallInfo"]['currentServe'],
                                                            "哪支队伍有人受伤": item["beachVolleyBallInfo"]['playerInjury'],
                                                            "是否为雨天": item["beachVolleyBallInfo"]['isRain']},
                                if 'eSportInfo' in item and item['eSportInfo']:
                                    sub_info["电子竞技相关信息"] = {"标识会打几个地图": item["eSportInfo"]['bestOfMap'],
                                                            "是否即将开赛": item["eSportInfo"]['isStartingSoon'],
                                                            "游戏名称": item["eSportInfo"]['overTimeSession'],
                                                            "电子竞技联赛名称": item["eSportInfo"]['leagueGroup'],
                                                            "电子竞技联赛ID": item["eSportInfo"]['leagueGroupId']}
                                if 'basketballInfo' in item and item['basketballInfo']:
                                    sub_info["篮球相关信息"] = {"主队目前得分": item["basketballInfo"]['homeGameScore'],
                                                          "客队目前得分": item["basketballInfo"]['awayGameScore'],
                                                          "目前进行节数": item["basketballInfo"]['latestLivePeriod'],
                                                          "主隊延長賽得分": item["basketballInfo"]['homeOverTimeScore'],
                                                          "客队延长赛得分": item["basketballInfo"]['awayOverTimeScore']}
                                if 'baseballInfo' in item and item['baseballInfo']:
                                    sub_info["棒球相关信息"] = {"主队目前得分": item["baseballInfo"]['homeGameScore'],
                                                          "客队目前得分": item["baseballInfo"]['awayGameScore'],
                                                          "主隊延長賽比分": item["baseballInfo"]['homeOverTimeScore'],
                                                          "客队延长赛比分": item["baseballInfo"]['awayOverTimeScore'],
                                                          "垒上是否有跑者": item["baseballInfo"]['baseHasRunner'],
                                                          "目前局数": item["baseballInfo"]['currentInning'],
                                                          "目前打击队伍": item["baseballInfo"]['currentBattingTeam'],
                                                          "目前出局数": item["baseballInfo"]['currentOuts']}

                                if 'volleyballInfo' in item and item['volleyballInfo']:
                                    sub_info["排球相关信息"] = {"主队每盘获得局数": item['volleyballInfo']["homeGameScore"],
                                                          "客队每盘获得局数": item['volleyballInfo']["awayGameScore"],
                                                          "主队目前总比分": item['volleyballInfo']["homePointScore"],
                                                          "客队目前总比分": item['volleyballInfo']["awayPointScore"],
                                                          "目前发球方": item['volleyballInfo']["currentServe"],
                                                          "主队目前比分": item['volleyballInfo']["homeCurrentPoint"],
                                                          "客队目前比分": item['volleyballInfo']["awayCurrentPoint"],
                                                          "哪支队伍有人受伤": item['volleyballInfo']["playerInjury"],
                                                          "目前进行的节数": item['volleyballInfo']["latestLivePeriod"]},
                                if 'footballInfo' in item and item['footballInfo']:
                                    sub_info["美式足球相关信息"] = {"主队每盘获得局数": item['footballInfo']["homeGameScore"],
                                                            "客队每盘获得局数": item['footballInfo']["awayGameScore"],
                                                            "主队目前总比分": item['footballInfo']["homeCurrentPoint"],
                                                            "客队目前总比分": item['footballInfo']["awayCurrentPoint"],
                                                            "主队延长赛比分": item['footballInfo']["homeOverTimeScore"],
                                                            "客队延长赛比分": item['footballInfo']["awayOverTimeScore"]},
                                if 'tableTennisInfo' in item and item['tableTennisInfo']:
                                    sub_info["桌球相关信息"] = {"主队每盘获得局数": item["tableTennisInfo"]['homeGameScore'],
                                                          "客队每盘获得局数": item["tableTennisInfo"]['awayGameScore'],
                                                          "主队目前比分": item["tableTennisInfo"]['homeCurrentPoint'],
                                                          "客队目前比分": item["tableTennisInfo"]['awayCurrentPoint'],
                                                          "主队获得盘数": item["tableTennisInfo"]['homeSetScore'],
                                                          "客队获得盘数": item["tableTennisInfo"]['awaySetScore'],
                                                          "哪支队伍有人受伤": item["tableTennisInfo"]['playerInjury'],
                                                          "目前盘数": item["tableTennisInfo"]['CurrentSet'],
                                                          "目前发球方": item["tableTennisInfo"]['currentServe']},
                                if 'badmintonInfo' in item and item['badmintonInfo']:
                                    sub_info["羽球相关信息"] = {"主队每盘获得局数": item["badmintonInfo"]['homeGameScore'],
                                                          "客队每盘获得局数": item["badmintonInfo"]['awayGameScore'],
                                                          "主队目前比分": item["badmintonInfo"]['homeCurrentPoint'],
                                                          "客队目前比分": item["badmintonInfo"]['awayCurrentPoint'],
                                                          "主队获得盘数": item["badmintonInfo"]['homeSetScore'],
                                                          "客队获得盘数": item["badmintonInfo"]['awaySetScore'],
                                                          "哪支队伍有人受伤": item["badmintonInfo"]['playerInjury'],
                                                          "目前盘数": item["badmintonInfo"]['currentSet'],
                                                          "目前发球方": item["badmintonInfo"]['currentServe']}

                                # print(item)
                                # print(events_dic)
                                if 'sportType' in item:
                                    sport_name = str(item["sportType"])
                                elif "体育项目名称" in filter_dic:
                                    sport_name = filter_dic["体育项目名称"].split()[1]
                                else:
                                    sport_name = SbSportEnum.sport_dic_f_zh.value[events_dic[event_id]['体育项目']]
                                period_str = BusinessOperation.get_period_str(sport_name, sub_info)
                                sub_info['球赛相关信息']['阶段描述'] = period_str

                                events_dic[event_id] = sub_info
                        for item in data['payload']['events']['remove']:
                            is_changed = True
                            try:
                                if item in events_dic:
                                    events_dic.pop(item)
                            except TypeError:
                                print(item)
                                raise AssertionError()

                        if data['payload']['markets']['add']:
                            is_changed = True
                            for item in data['payload']['markets']['add']:
                                event_id = item["eventId"]
                                if 'sportType' not in item:
                                    continue
                                # print(item)
                                sub_data = {"体育项目ID": item["sportType"], "赛事ID": item["eventId"],
                                            "投注类型": item["betType"], "投注类型名称": item["betTypeName"],
                                            "盘口ID": item["marketId"], "最大投注限额": item["maxBet"],
                                            "是否为滚球赛事": item["isLive"], "盘口状态": item["marketStatus"],
                                            "游戏地图": item["gameMap"] if "gameMap" in item else "",
                                            "游戏回合": item["gameRound"] if "gameRound" in item else "",
                                            "投注类型分类": item["category"], "排序球头": item["sort"],
                                            "赛事串关数量限制": item["combo"],
                                            "盘口赔率项目列表": [{'投注选项': i['key'],
                                                          '投注类型选项名称': i['keyName'],
                                                          '球头': i['point'] if "point" in i else "",
                                                          '球头2': i['point2'] if "point2" in i else "",
                                                          '赔率相关信息': i['oddsPrice']['decimalPrice']} for i in
                                                         item["selections"]]}
                                market_event_dic[sub_data['盘口ID']] = {"赛事ID": sub_data['赛事ID'],
                                                                      "投注类型": sub_data['投注类型'],
                                                                      "体育项目ID": sub_data['体育项目ID']}
                                # 多球头，只有SportType= 43(电子竞技)sort为0
                                if sub_data['投注类型'] in (1, 3, 7, 8, 219, 220, 401, 402, 475, 476, 477, 478, 486, 487,
                                                        701, 704, 705, 3907, 3908, 3913):
                                    if sub_data['体育项目ID'] == 43:
                                        if sub_data["排序球头"] == 0:
                                            events_dic[event_id]['盘口赔率项目列表'].append(sub_data)
                                    else:
                                        # print(sub_data)
                                        if sub_data["排序球头"] == 1:
                                            events_dic[event_id]['盘口赔率项目列表'].append(sub_data)
                                else:
                                    events_dic[event_id]['盘口赔率项目列表'].append(sub_data)

                        if data['payload']['markets']['change']:
                            is_changed = True
                            for item in data['payload']['markets']['change']:
                                event_id = market_event_dic[item['marketId']]['赛事ID']
                                item["sportType"] = events_dic[event_id]['体育项目']

                                sub_data = {"是否为滚球赛事": item["isLive"], "盘口状态": item["marketStatus"],
                                            "排序球头": item["sort"], "盘口ID": item['marketId'],
                                            "盘口赔率项目列表": [{'投注选项': i['key'],
                                                          '球头': i['point'] if "point" in i else "",
                                                          '球头2': i['point2'] if "point2" in i else "",
                                                          '赔率相关信息': i['oddsPrice']['decimalPrice']} for i in
                                                         item["selections"]],
                                            }
                                for index_old, old_event_data in enumerate(events_dic[event_id]['盘口赔率项目列表']):
                                    if old_event_data['盘口ID'] == sub_data['盘口ID']:
                                        # 更新排序球头
                                        events_dic[event_id]['盘口赔率项目列表'][index_old]['排序球头'] = sub_data['排序球头']
                                        events_dic[event_id]['盘口赔率项目列表'][index_old]['是否为滚球赛事'] = sub_data['是否为滚球赛事']
                                        events_dic[event_id]['盘口赔率项目列表'][index_old]['盘口状态'] = sub_data['盘口状态']
                                        for index_new_outcome, value_new_outcome in enumerate(sub_data['盘口赔率项目列表']):
                                            # 更新原数据中对应的项的值
                                            for index_old_outcome, value_old_outcome in enumerate(
                                                    old_event_data['盘口赔率项目列表']):
                                                if value_new_outcome['投注选项'] == value_old_outcome["投注选项"]:
                                                    if "球头" in value_new_outcome:
                                                        events_dic[event_id]['盘口赔率项目列表'][index_old]['盘口赔率项目列表'][
                                                            index_old_outcome]["球头"] = value_new_outcome["球头"]
                                                    if "球头2" in value_new_outcome:
                                                        events_dic[event_id]['盘口赔率项目列表'][index_old]['盘口赔率项目列表'][
                                                            index_old_outcome]["球头2"] = value_new_outcome["球头2"]
                                                    events_dic[event_id]['盘口赔率项目列表'][index_old]['盘口赔率项目列表'][
                                                        index_old_outcome]["赔率相关信息"] = value_new_outcome["赔率相关信息"]
                                                    break
                        if data['payload']['markets']['remove']:
                            is_changed = True
                            for market_id in data['payload']['markets']['remove']:
                                event_id = market_event_dic[market_id]['赛事ID']
                                if event_id in events_dic:
                                    for index in range(len(events_dic[event_id]['盘口赔率项目列表']) - 1, -1, -1):
                                        market_data = events_dic[event_id]['盘口赔率项目列表'][index]
                                        if market_data['盘口ID'] == market_id:
                                            events_dic[event_id]['盘口赔率项目列表'].pop(index)
                                            break
                                # for index, market_data in enumerate(events_dic[event_id]['盘口赔率项目列表']):
                                #     if market_data['盘口ID'] == market_id:
                                #         events_dic[event_id]['盘口赔率项目列表'].pop(index)
                                #         break
                                market_event_dic.pop(market_id)

                        if events_dic and is_changed:
                            BusinessOperation.event_list[page - 1] = events_dic
                            if len(events_dic) == 250 and not is_next_page_generated:
                                BusinessOperation.start_stream('events', {"filter_dic": filter_dic,
                                                                          'start_diff': start_diff,
                                                                          'end_diff': end_diff, 'env': env,
                                                                          'token': token, "page": page + 1})
                                is_next_page_generated = True
                            final_event_dic = {key: value for dic in BusinessOperation.event_list for key, value in
                                               dic.items() if dic}
                            BusinessOperation.event_queue.put(final_event_dic)
                else:
                    break

    @staticmethod
    def get_leagues_sse(filter_dic=None, start_diff=None, end_diff=None, env="", token="", header=None):
        """
        获取每个联赛中的赛事数量
        @param env:
        @param filter_dic:
        @param start_diff:
        @param end_diff:
        @param token:
        @return:
        """
        if env:
            env_context.set(env)
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetLeagues'
        params = {"language": "zhcn",
                  'token': sb_token_context.get() if not token else token}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_utc_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_utc_search_time(end_diff, is_end=True)
        if filter_dic:
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        print(params)
        client = requests.get(url, params=params, stream=True, headers=headers_stream)
        league_data_dic = {}

        for chunk in client.iter_lines(decode_unicode=False):
            if BusinessOperation.running_status.is_set():
                msg = chunk.decode().strip()
                if 'payload' in msg:
                    is_changed = False
                    data = json.loads(msg[6:])
                    # print(data)
                    for item in data['payload']['leagues']['add']:
                        is_changed = True
                        league_data_dic[str(item['leagueId'])] = {"体育类型": item['sportType'],
                                                                  "联赛名称": item['leagueName'],
                                                                  "联赛ID": item['leagueId'],
                                                                  "非滚球赛事数量": item['gameCount'],
                                                                  "滚球数量": item['liveGameCount'],
                                                                  "是否支持串关": '是' if item['isParlay'] else '否'}
                    for item in data['payload']['leagues']['change']:
                        is_changed = True
                        league_id = str(item['leagueId'])
                        if str(item['leagueId']) in league_data_dic:
                            league_data_dic[league_id]['isParlay'] = item['isParlay']
                            league_data_dic[league_id]['gameCount'] = item['gameCount']
                            league_data_dic[league_id]['liveGameCount'] = item['liveGameCount']
                    for item in data['payload']['leagues']['remove']:
                        is_changed = True
                        league_data_dic.pop(str(item['leagueId']))
                    if league_data_dic and is_changed:
                        # print(league_data_dic)
                        BusinessOperation.league_queue.put(league_data_dic)
            else:
                break

    @staticmethod
    def get_markets_sse(event_id=None, env="", token="", header=None):
        """
        获取盘口更新数据
        @param event_id: 比赛id
        @param env:
        @param token:
        @return:
        """
        if env:
            env_context.set(env)
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetMarkets'
        params = {"language": "zhcn",
                  'token': sb_token_context.get() if not token else token}
        if event_id:
            params["query"] = SbFilterUtil.generate_query_str({'赛事id': f' eq {event_id}'})
        client = requests.get(url, params=params, stream=True, headers=headers_stream)
        market_data_dic = {}

        for chunk in client.iter_lines(decode_unicode=False):
            if BusinessOperation.running_status.is_set():
                msg = chunk.decode().strip()
                if 'payload' in msg:
                    # print(msg)
                    is_changed = False
                    data = json.loads(msg[6:])['payload']

                    for item in data['markets']['add']:
                        is_changed = True
                        market_id = item["marketId"]
                        if 'sportType' not in item:
                            continue
                        sub_data = {"体育项目ID": item["sportType"], "赛事ID": item["eventId"],
                                    "投注类型": item["betType"], "投注类型名称": item["betTypeName"],
                                    "盘口ID": market_id, "最大投注限额": item["maxBet"],
                                    "是否为滚球赛事": item["isLive"], "盘口状态": item["marketStatus"],
                                    "游戏地图": item["gameMap"] if "gameMap" in item else "",
                                    "游戏回合": item["gameRound"] if "gameRound" in item else "",
                                    "投注类型分类": item["category"], "排序球头": item["sort"],
                                    "赛事串关数量限制": item["combo"],
                                    "盘口赔率项目列表": [{'投注选项': i['key'],
                                                  '投注类型选项名称': i['keyName'],
                                                  '球头': i['point'] if "point" in i else "",
                                                  '球头2': i['point2'] if "point2" in i else "",
                                                  '赔率相关信息': i['oddsPrice']['decimalPrice']} for i in
                                                 item["selections"]]}
                        market_data_dic[market_id] = sub_data

                    for item in data['markets']['change']:
                        # print(item)
                        market_id = item['marketId']
                        is_changed = True
                        sub_data = {"是否为滚球赛事": item["isLive"], "盘口状态": item["marketStatus"],
                                    "排序球头": item["sort"], "盘口ID": item['marketId'],
                                    "盘口赔率项目列表": [{'投注选项': i['key'],
                                                  '球头': i['point'] if "point" in i else "",
                                                  '球头2': i['point2'] if "point2" in i else "",
                                                  '赔率相关信息': i['oddsPrice']['decimalPrice']} for i in
                                                 item["selections"]]}
                        # 遍历更新的盘口
                        for index_new, value_new in enumerate(sub_data['盘口赔率项目列表']):
                            market_data_dic[market_id]['是否为滚球赛事'] = sub_data['是否为滚球赛事']
                            market_data_dic[market_id]['盘口状态'] = sub_data['盘口状态']
                            market_data_dic[market_id]['排序球头'] = sub_data['排序球头']
                            # 更新原数据中对应的项的值
                            for index_1, value_1 in enumerate(market_data_dic[market_id]['盘口赔率项目列表']):
                                if value_new['投注选项'] == value_1["投注选项"]:
                                    if "球头" in value_new['投注选项']:
                                        market_data_dic[market_id]['盘口赔率项目列表'][index_1]["球头"] = value_new["球头"]
                                    if "球头2" in value_new['投注选项']:
                                        market_data_dic[market_id]['盘口赔率项目列表'][index_1]["球头2"] = value_new["球头2"]
                                    market_data_dic[market_id]['盘口赔率项目列表'][index_1]["赔率相关信息"] = value_new["赔率相关信息"]
                                    break
                    for item in data['markets']['remove']:
                        # print(item)
                        market_data_dic.pop(item)

                    if market_data_dic and is_changed:
                        BusinessOperation.market_queue.put(market_data_dic)

    @staticmethod
    def get_out_rights_sse(filter_dic=None, env="", token="", page=1, header=None):
        """
        获取优胜冠军赛事信息
        @param filter_dic:
        @param env:
        @param token:
        @param page:
        @return:
        """
        if env:
            env_context.set(env)
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetOutrights'
        params = {"language": "zhcn",
                  'token': sb_token_context.get() if not token else token,
                  'orderby': 'eventDate asc'}
        print("----------")
        print(params)
        if filter_dic:
            params["query"] = SbFilterUtil.generate_query_str(filter_dic, skip=(page - 1) * 250)
        client = requests.get(url, params=params, stream=True, headers=headers_stream)
        event_data_dic = defaultdict()

        is_next_page_generated = False
        while True:
            for chunk in client.iter_lines(decode_unicode=False):
                if BusinessOperation.running_status.is_set():
                    msg = chunk.decode().strip()
                    if 'payload' in msg:
                        data = json.loads(msg[6:])
                        is_changed = False
                        for item in data['payload']['outrights']['add']:
                            is_changed = True
                            if str(item['sportType']) in SbSportEnum.sport_dic_f_zh.value.values():
                                event_data_dic[item['eventCode']] = {
                                    "体育类型": SbSportEnum.sport_dic_t_zh.value[str(item['sportType'])],
                                    "联赛名称": item['leagueName'],
                                    "赛事标识符": item['eventCode'],
                                    "指定联赛的显示模式": item['lDisplayMode'],
                                    "赛事日期": item['eventDate'],
                                    "优胜冠军状态": item['outrightStatus'],
                                    "优胜冠军联赛群组": item['leagueGroup'],
                                    "队伍相关信息": [{"优胜冠军赔率ID": team['orid'],
                                                "队伍ID": team['teamId'],
                                                "队伍名称": team['teamName'],
                                                "赔率": team['price'],
                                                "最大投注额": team['maxBet'],
                                                "盘口状态": team['oddsStatus'],
                                                "赔率使否异动": team['isUpdate']} for team in
                                               item['teams']]}
                        for item in data['payload']['outrights']['change']:
                            is_changed = True
                            if 'eventCode' in item and item['eventCode'] in event_data_dic:
                                event_code = item['eventCode']
                                if event_code in event_data_dic:
                                    event_data_dic[event_code]['优胜冠军状态'] = item['eventStatus']
                                    [event_data_dic[event_code]['队伍相关信息'].update({"优胜冠军赔率ID": team['orid'],
                                                                                  "赔率": team['price'],
                                                                                  "最大投注额": team['maxBet'],
                                                                                  "盘口状态": team['oddsStatus'],
                                                                                  "赔率使否异动": team['isUpdate']}) for team
                                     in
                                     item['teams']]
                        for item in data['payload']['outrights']['remove']:
                            is_changed = True
                            event_data_dic.pop(str(item['eventCode']))
                        if event_data_dic and is_changed:
                            BusinessOperation.out_rights_list[page - 1] = event_data_dic
                            if len(event_data_dic) == 250 and not is_next_page_generated:
                                BusinessOperation.start_stream('champion', {"filter_dic": filter_dic,
                                                                            "env": env, "token": token,
                                                                            "page": page + 1})
                                is_next_page_generated = True
                            final_event_dic = {key: value for dic in BusinessOperation.out_rights_list for key, value in
                                               dic.items() if dic}
                            BusinessOperation.out_right_queue.put(final_event_dic)
                else:
                    break

    @staticmethod
    def get_game_details(event_id_list: list):
        """
        获取赛事结果等相关信息
        @param event_id_list:
        @return:
        """
        event_id_list = [str(item) for item in event_id_list]
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/betting/V1/GetGameDetails'
        params = {"language": "zhcn",
                  'eventIds': ','.join(event_id_list)}
        # rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get())
        data = rsp.json()['games'] if 'games' in rsp.json() else {}
        result_dic = {}
        for item in data:
            sub_data = {"赛事ID": item['eventId'], "开赛时间": item['gameDetail']['eventTime'],
                        "体育项目ID": item['gameDetail']['sportType'],
                        "联赛ID": item['gameDetail']['leagueId'], "联赛名称": item['gameDetail']['leagueName'],
                        "主队名称": item['gameDetail']['homeName'], "客队名称": item['gameDetail']['awayName'],
                        "主队终场得分": item['gameDetail']['homeScore'], "客队终场得分": item['gameDetail']['awayScore'],
                        "主队半场得分": item['gameDetail']['htHomeScore'], "客队半场得分": item['gameDetail']['htAwayScore'],
                        "赛事状态": item['gameDetail']['gameStatus'], "主客队终场得分": item['gameDetail']['winItem'],
                        "角球进球顺序": item['gameDetail']['cornerSequence']}
            result_dic[sub_data['赛事ID']] = sub_data
        return result_dic

    @staticmethod
    def get_sport_results(start_diff=0, end_diff=0):
        """
        用于获取指定时间区间内运动的赛果和优胜冠军赛果数量
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetSportResults'
        params = {"language": "zhcn",
                  'token': sb_token_context.get(),
                  "from": DateUtil.get_utc_search_time(start_diff),
                  "until": DateUtil.get_utc_search_time(end_diff, is_end=True)}
        print(params)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        print("【赛果数量统计】")
        if 'sportList' in rsp:
            for item in rsp['sportList']:
                if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                    print(f'{item["sportName"]}: \n    普通赛事数量: {item["eventResults"]},\n    冠军赛事数量: '
                          f'{item["outrightResults"]}')
        else:
            print('暂无数据')

    @staticmethod
    def get_event_results(sport_name=None, league_id=None, event_id=None, only_running=False, start_diff=0, end_diff=0):
        """
        获取指定时间区间内运动的赛果信息，仅支持查询最近 12 天内的结果
        @param sport_name:
        @param event_id:
        @param league_id:
        @param only_running: 是否只看进行中的赛事     True | False
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetEventResults'
        params = {"language": "zhcn",
                  'token': sb_token_context.get(),
                  "from": DateUtil.get_utc_search_time(start_diff, rtn_type='秒'),
                  "until": DateUtil.get_utc_search_time(end_diff, is_end=True, rtn_type='秒')}
        if sport_name or event_id:
            filter_dic = {}
            if sport_name:
                filter_dic["体育项目名称"] = f' eq {SbSportEnum.sport_dic_f_zh.value[sport_name]} '
            if event_id:
                filter_dic["赛事id"] = f' eq {event_id} '
            if league_id:
                filter_dic["联赛id"] = f' eq {league_id} '
            if only_running:
                filter_dic["游戏状态"] = f" eq 'Running' "
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        print(params)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        data = rsp['result']
        result_list = []
        for item in data:
            # print(item)
            sub_data = {'体育项目名称': item['sportName'], '联赛ID': item['leagueId'], '联赛名称': item['leagueName'],
                        "赛事比赛有多少节": item['gameSession'], '赛事赛果信息列表': []}
            for event in item['events']:
                event_dic = {"赛事ID": event["eventId"], "主队ID": event["homeId"], "主队名称": event["homeName"],
                             "客队ID": event["awayId"], "客队名称": event["awayName"], "主队半场得分": event["htHomeScore"],
                             "客队半场得分": event["htAwayScore"], "主队终场得分": event["homeScore"],
                             "客队终场得分": event["awayScore"],
                             "主队的总比赛得分": event["homeGameScore"], "客队的总比赛得分": event["awayGameScore"],
                             "赛事状态": event["gameStatus"], "赛事时间": event["eventTime"]}
                if event['sessionScores']:
                    event_dic['各节的详细信息'] = [{"主队节得分": session['homeScore'], '客队节得分': session['awayScore'],
                                             '此节是否需退款': session['isRefund']} for session in event['sessionScores']]
                if event['overTimeScores']:
                    if event['overTimeScores']['homeScore'] != '-':
                        event_dic['各加时赛的详细信息'] = event['overTimeScores']

                if event['soccerDetail']:
                    soccer_detail = event['soccerDetail']
                    # print(soccer_detail)
                    event_dic['足球赛果详细信息'] = {
                        "哪支球队在全场比赛中获得第一个进球": soccer_detail['firstGoal'],
                        "哪支球队在全场比赛中获得最后一个进球": soccer_detail['lastGoal'],
                        "哪支球队在上半场获得第一个进球": soccer_detail['firstHtGoal'],
                        "哪支球队在上半场获得最后一个进球": soccer_detail['lastHtGoal'],
                        "进球顺序": soccer_detail['goalSequence'],
                        "角球进球顺序": soccer_detail['cornerSequence'],
                        "点球进球顺序": soccer_detail['penaltySequence'],
                        "第一个进球的方法": soccer_detail['firstGoalMethod'],
                        "骤死赛点球进球顺序": soccer_detail['deathSuddenPenaltySequence'],
                        "此赛事是否为点球让分盘赛果": soccer_detail['isPenaltyHandicap'],
                        "此赛事是否为点球大小盘赛果": soccer_detail['isPenaltyOverUnder'],
                        "球赛事的特殊信息": []}
                    if 'specialData' in soccer_detail and soccer_detail['specialData']:
                        special = soccer_detail['specialData']
                        for special_item in special:
                            event_dic['足球赛果详细信息']["球赛事的特殊信息"].append({"联赛ID": special_item['leagueId'],
                                                                      "联赛名称": special_item['leagueName'],
                                                                      "赛事ID": special_item['eventId'],
                                                                      "主队ID": special_item['homeId'],
                                                                      "主队名称": special_item['homeName'],
                                                                      "客队ID": special_item['awayId'],
                                                                      "客队名称": special_item['awayName'],
                                                                      "主队半场得分": special_item['htHomeScore'],
                                                                      "客队半场得分": special_item['htAwayScore'],
                                                                      "主队得分": special_item['homeScore'],
                                                                      "客队得分": special_item['awayScore'],
                                                                      "排序": special_item['sort'],
                                                                      "赛事状态": special_item['status']})
                if event['eSportMapDetail']:
                    maps = event['eSportMapDetail']['maps']
                    event_dic['赛事赛果信息列表']['电子竞技赛果详细信息'] = [{"游戏地图": i['map'], "主队得分": i['homeScore'],
                                                            "客队得分": i['awayScore'], "赛事状态": i['status']} for i in maps]
                sub_data['赛事赛果信息列表'].append(event_dic)
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_outright_results(sport_name=None, event_id=None, start_diff=0, end_diff=0):
        """
        获取指定时间区间内优胜冠军赛果信息
        @param sport_name:
        @param event_id:
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetOutrightResults'
        params = {"language": "zhcn",
                  'token': sb_token_context.get(),
                  "from": DateUtil.get_utc_search_time(start_diff),
                  "until": DateUtil.get_utc_search_time(end_diff, is_end=True)}
        if sport_name or event_id:
            filter_dic = {}
            if sport_name:
                filter_dic["体育项目名称"] = f' eq {SbSportEnum.sport_dic_f_zh.value[sport_name]} '
            if event_id:
                filter_dic["赛事id"] = f' eq {event_id} '
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        print(params)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        data = rsp['result']
        result_list = []
        for item in data:
            # print(item)
            sub_data = {"体育项目ID": item['sportType'], "体育项目名称": item['sportName'], "联赛ID": item['leagueId'],
                        "联赛名称": item['leagueName'],
                        "优胜冠军详细信息": {"赛事时间": item['outrights']['eventTime'],
                                     "队伍ID": item['outrights']['teamId'], "队伍名称": item['outrights']['teamName'],
                                     "赛事状态": item['outrights']['status']}}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_announcement(sport_name=None, announcement_type='全部公告', start_diff=0, end_diff=0):
        """
        获取公告
        @param announcement_type: 全部公告 | 特殊置顶公告 | 一般公告
        @param sport_name:
        @param start_diff: 时间最长7天
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetAnnouncement'
        params = {"language": "zhcn",
                  'token': sb_token_context.get(),
                  'stickOption': {"全部公告": 0, "特殊置顶公告": 1, "一般公告": 2}[announcement_type],
                  "start": DateUtil.get_utc_search_time(start_diff),
                  "end": DateUtil.get_utc_search_time(end_diff, is_end=True)}
        print(params)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        result_list = []
        for item in rsp:
            sub_data = {"公告讯息识别ID": item['messageId'], "公告讯息张贴时间": item['postTime'],
                        "是否为置顶公告": item['isSticky'], "讯息公告内容": item['message']}
            result_list.append(sub_data)
        if not sport_name:
            sport_name_list = SbSportEnum.sport_dic_f_zh.value.keys()
        else:
            sport_name_list = [sport_name]
        announce_list = []
        for item in result_list:
            for name in sport_name_list:
                if f"请注意:[{name}]" in item['讯息公告内容']:
                    announce_list.append(item)
        return announce_list

    @staticmethod
    def _get_hot_event_list(sport_name=None, sport_id_str=None, header=None):
        """
        获取热门赛事列表
        @param sport_name:
        @param sport_id_str:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetPromotions'
        if sport_name:
            filter_dic = {"体育项目名称": f' in ({",".join(list(SbSportEnum.sport_dic_f_zh.value[sport_name]))})'}
        else:
            filter_dic = {"体育项目名称": sport_id_str}
        params = {"language": "zhcn",
                  "query": SbFilterUtil.generate_query_str(filter_dic)
                  }
        rsp = requests.get(url, params=params, headers=header).json()
        event_id_list = [str(item['eventId']) for item in rsp['events']]
        return event_id_list

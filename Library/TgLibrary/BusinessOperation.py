#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/1 16:35
import json

from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.Contexts import *
import requests
import threading
from telegram.update import Update
from Library.ApiRequests.SbApi.BusinessOperation import BusinessOperation as sb
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.SbSportEnum import SbSportEnum
from Library.Common.Utils.SbFilterUtil import SbFilterUtil

headers_stream = {
    'Content-Type': 'application/json;charset=UTF-8',
    'Accept': 'text/event-stream',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/123.0.0.0 Safari/537.36',
    "Sign": "",
    "Accept-Encoding": 'br,gzip,deflate',
    "Accept-Language": "zh-CN,zh;q=0.9"
}

sport_dic = {"1": "足球", "2": "篮球", "3": "美式足球", "4": "冰上曲棍球", "5": "网球", "6": "排球", "7": "斯诺克",
             "8": "棒球", "9": "羽毛球", "43": "电子竞技"}


class BusinessOperation(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    event = threading.Event()
    stream_type = None
    running_status = threading.Event()
    thread = None

    @staticmethod
    def start_stream(update, stream_type, token):
        if BusinessOperation.running_status.is_set():
            return "已经在运行中，不能重复运行"
        stream_type_dic = {"sports": BusinessOperation.get_sports_push,
                           "leagues": BusinessOperation.get_leagues_sse,
                           "markets": BusinessOperation.get_markets_push,
                           "events": BusinessOperation.get_events_sse}
        BusinessOperation.running_status.set()
        BusinessOperation.thread = threading.Thread(target=stream_type_dic[stream_type], args=(update, token),
                                                    daemon=True)
        BusinessOperation.thread.start()
        return "动态获取中...."

    @staticmethod
    def stop_stream():
        BusinessOperation.running_status.clear()

    @staticmethod
    def get_sports_push(update: Update, token, start_diff=0, end_diff=0):
        """
        建立连接，获取每个运动项目的赛事数量及串关赛事数量
        @param update:
        @param token:
        @param start_diff:
        @param end_diff:
        @return:
        """
        # start_date = DateUtil.get_utc_time_by_now(day_diff=start_diff)
        # end_date = DateUtil.get_utc_time_by_now(day_diff=end_diff)
        env_context.set('sit')
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetSports'
        params = {"language": "zhcn",
                  'token': token,
                  "query": "",
                  'filter': 'sportType in (1,2,3,4,5,6,7,8,9,43) and isLive eq true',
                  "$skip": 750}
        client = requests.get(url, params=params, stream=True, headers=headers_stream)

        for chunk in client.iter_content(chunk_size=None, decode_unicode=False):
            if BusinessOperation.running_status.is_set():
                msg = chunk.decode().strip()
                if 'payload' in msg:
                    data = json.loads(msg.split("\n")[1][6:])

                    result_list = []
                    for item in data['payload']['sports']['add'] + data['payload']['sports']['change']:
                        if str(item['sportType']) in sport_dic:
                            result_list.append(f"【{sport_dic[str(item['sportType'])]}】\n            "
                                               f"非滚球赛事数量:{item['gameCount']},滚球数量:{item['liveGameCount']}，"
                                               f"滚球串关赛事数量:{item['liveParlayGame']},非滚球串关赛事数量:"
                                               f"{item['parlayGame']},优胜冠军赛事数量:{item['outrightGame']}\n")
                        else:
                            break
                    if result_list:
                        update.message.reply_text('\n'.join(result_list))
            else:
                update.message.reply_text("已停止")
                break

    @staticmethod
    def get_leagues_sse(update: Update, token):
        """
        获取每个联赛中的赛事数量
        @param update:
        @param token:
        @return:
        """
        message = update.message.to_dict()
        print(f'【获取每个联赛中的赛事数量】 收到消息: {message["text"]}')
        input_list = message["text"].split()
        if len(input_list) not in (2, 3) or input_list[1] not in list(SbSportEnum.sport_dic_f_zh.value.keys()):
            update.message.reply_text(f'格式不正确，应为："/get_leagues 体育类型 时间类型(可选)(今日｜早盘)"')
            return

        env_context.set('sit')
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetLeagues'
        params = {"language": "zhcn", 'token': token}
        filter_dic = {"体育项目名称": f" eq {SbSportEnum.sport_dic_f_zh.value[input_list[1]]} "}
        if len(input_list) == 3:
            if input_list[2] == '今日':
                params['from'] = DateUtil.get_sb_search_time(0)
                params['until'] = DateUtil.get_sb_search_time(0, is_end=True)
            # elif input_list[2] == '滚球':
            #     params['from'] = DateUtil.get_sb_search_time(0)
            #     params['until'] = DateUtil.get_sb_search_time(0, is_end=True)
            #     filter_dic['赛事状态'] = "eq 'running'"
            elif input_list[2] == '早盘':
                params['from'] = DateUtil.get_sb_search_time(1)
        params['query'] = SbFilterUtil.generate_query_str(filter_dic)
        print(params)
        print(url)
        client = requests.get(url, params=params, stream=True, headers=headers_stream)
        league_data_dic = {}

        while BusinessOperation.running_status.is_set():
            for chunk in client.iter_lines(decode_unicode=False):
                if BusinessOperation.running_status.is_set():
                    msg = chunk.decode().strip()
                    print(msg)
                    if 'payload' in msg:
                        is_changed = False
                        data = json.loads(msg[6:])
                        for item in data['payload']['leagues']['add']:
                            is_changed = True
                            if str(item['sportType']) in sport_dic:
                                league_data_dic[str(item['leagueId'])] = item
                            else:
                                break
                        for item in data['payload']['leagues']['change']:
                            is_changed = True
                            if str(item['leagueId']) in league_data_dic:
                                league_data_dic[str(item['leagueId'])]['isParlay'] = item['isParlay']
                                league_data_dic[str(item['leagueId'])]['gameCount'] = item['gameCount']
                                league_data_dic[str(item['leagueId'])]['liveGameCount'] = item['liveGameCount']

                        for item in data['payload']['leagues']['remove']:
                            is_changed = True
                            league_data_dic.pop(str(item['leagueId']))
                        result_list = [f"【{sport_dic[str(element['sportType'])]} - {element['leagueName']}】\n"
                                       f"            非滚球赛事数量:{element['gameCount']},滚球数量:"
                                       f"{element['liveGameCount']},是否支持串关:"
                                       f"{'是' if element['isParlay'] else '否'}\n" for element in
                                       league_data_dic.values()]
                        if result_list and is_changed:
                            update.message.reply_text(f"最新数据：{len(result_list)}个联赛")
                            for sub_index in range(0, len(result_list), 40):
                                update.message.reply_text('\n'.join(result_list[sub_index: sub_index + 40]))
                else:
                    update.message.reply_text("已停止")
                    return
        update.message.reply_text("已停止")

    @staticmethod
    def get_markets_push(start_diff=0, end_diff=0):
        """
        获取盘口更新数据
        @param start_diff:
        @param end_diff:
        @return:
        """
        # start_date = DateUtil.get_utc_time_by_now(day_diff=start_diff)
        # end_date = DateUtil.get_utc_time_by_now(day_diff=end_diff)
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetMarkets'
        params = {"language": "zhcn",
                  'token': sb_token_context.get(),
                  "query": "",
                  'filter': 'sportType in (1,2,3,4,5,6,7,8,9,43) and isLive eq true',
                  "$skip": 750}
        client = requests.get(url, params=params, stream=True, headers=headers_stream)

        for chunk in client.iter_content(chunk_size=None, decode_unicode=False):
            msg = chunk.decode().strip()
            if 'payload' in msg:
                data = json.loads(msg.split("\n")[1][6:])

    @staticmethod
    def get_events(filter_dic=None, start_diff=None, end_diff=None):
        """
        用于获取赛事相关信息包含部分盘口信息
        @param filter_dic:
        @param start_diff:
        @param end_diff:
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/V1/GetEvents'
        params = {"language": "zhcn",
                  'token': sb_token_context.get()}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_sb_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_sb_search_time(end_diff, is_end=True)
        if filter_dic:
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        rsp = requests.get(url, params=params, headers=sb_client_header_context.get()).json()
        # print(rsp)
        data = rsp['events']

        result_list = []
        for item in data:
            if str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                sub_info = {"体育项目": item["sportType"], "联赛ID": item["leagueId"],
                            "联赛名称": item["leagueName"], "赛事ID": item["eventId"],
                            "赛事代码": item["eventCode"], "赛事状态": item["eventStatus"],
                            "是否为主要盘口": item["isMainMarket"], "系统开赛时间": item["kickOffTime"],
                            "开赛时间": item["globalShowTime"], "赛事比赛有多少节": item["gameSession"],
                            "该赛事的母赛事ID": item["parentId"], "是否为滚球赛事": item["isLive"],
                            "是否为串关赛事": item["isParlay"], "赛事是否支持实时兑现": item["isCashout"],
                            "是否为虚拟赛事": item["isVirtualEvent"], "是否有滚球盘口": item["hasLiveMarket"],
                            "该赛事的所有盘口数量": item["marketCount"], "该赛事的所有盘口投注类型": item["marketCategories"],
                            "视频ID": item["streamingOption"], "网球相关信息": item["tennisInfo"],
                            '团队相关信息': {"主队ID": item["teamInfo"]["homeId"], "主队名称": item["teamInfo"]["homeName"],
                                       "客队ID": item["teamInfo"]["awayId"], "客队名称": item["teamInfo"]["awayName"]},
                            '球赛相关信息': {"目前进行到第几节": item["gameInfo"]["livePeriod"],
                                       "当前赛事时间以秒为单位": item["gameInfo"]["seconds"],
                                       "是否为中场休息": item["gameInfo"]["isHt"],
                                       "赛事是否中断(休息时间)": item["gameInfo"]["isBreak"],
                                       "赛事是否关闭": item["gameInfo"]["isClosed"],
                                       "赛事是否延迟": item["gameInfo"]["delayLive"],
                                       "球赛状态": item["gameInfo"]["gameStatus"],
                                       "目前赛事时间": item["gameInfo"]["inPlayTime"],
                                       "主队滚球分数": item["gameInfo"]["liveHomeScore"],
                                       "客队滚球分数": item["gameInfo"]["liveAwayScore"]}}
                if item["soccerInfo"]:
                    sub_info["足球相关信息"] = {"主场红牌数": item["soccerInfo"]['homeRedCard'],
                                          "客场红牌数": item["soccerInfo"]['awayRedCard'],
                                          "主场黄牌数": item["soccerInfo"]['homeYellowCard'],
                                          "客场黄牌数": item["soccerInfo"]['awayYellowCard']}
                if item['tennisInfo']:
                    sub_info["美式足球相关信息"] = {"主队每盘获得局数": item['tennisInfo']["homeGameScore"],
                                            "客队每盘获得局数": item['tennisInfo']["awayGameScore"],
                                            "主队目前局数比分": item['tennisInfo']["homePointScore"],
                                            "客队目前局数比分": item['tennisInfo']["awayPointScore"],
                                            "目前盘数": item['tennisInfo']["currentSet"],
                                            "目前发球方": item['tennisInfo']["currentServe"]}

                if item['beachVolleyBallInfo']:
                    sub_info["沙滩排球相关信息"] = {"主队每盘获得局数": item["beachVolleyBallInfo"]['homeGameScore'],
                                            "客队每盘获得局数": item["beachVolleyBallInfo"]['awayGameScore'],
                                            "目前盘数": item["beachVolleyBallInfo"]['currentSet'],
                                            "目前发球方": item["beachVolleyBallInfo"]['currentServe'],
                                            "哪支队伍有人受伤": item["beachVolleyBallInfo"]['playerInjury'],
                                            "是否为雨天": item["beachVolleyBallInfo"]['isRain']},
                if item['eSportInfo']:
                    sub_info["电子竞技相关信息"] = {"标识会打几个地图": item["eSportInfo"]['bestOfMap'],
                                            "是否即将开赛": item["eSportInfo"]['isStartingSoon'],
                                            "游戏名称": item["eSportInfo"]['overTimeSession'],
                                            "电子竞技联赛名称": item["eSportInfo"]['leagueGroup'],
                                            "电子竞技联赛ID": item["eSportInfo"]['leagueGroupId']}
                if item['basketballInfo']:
                    sub_info["篮球相关信息"] = {"主队目前得分": item["basketballInfo"]['homeGameScore'],
                                          "客队目前得分": item["basketballInfo"]['awayGameScore'],
                                          "目前进行节数": item["basketballInfo"]['latestLivePeriod'],
                                          "主隊延長賽得分": item["basketballInfo"]['homeOverTimeScore'],
                                          "客队延长赛得分": item["basketballInfo"]['awayOverTimeScore']}
                if item['baseballInfo']:
                    sub_info["棒球相关信息"] = {"主队目前得分": item["baseballInfo"]['homeGameScore'],
                                          "客队目前得分": item["baseballInfo"]['awayGameScore'],
                                          "主隊延長賽比分": item["baseballInfo"]['homeOverTimeScore'],
                                          "客队延长赛比分": item["baseballInfo"]['awayOverTimeScore'],
                                          "垒上是否有跑者": item["baseballInfo"]['baseHasRunner'],
                                          "目前局数": item["baseballInfo"]['currentInning'],
                                          "目前打击队伍": item["baseballInfo"]['currentBattingTeam'],
                                          "目前出局数": item["baseballInfo"]['currentOuts']}

                if item['volleyballInfo']:
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
                                            "主隊延長賽比分": item['footballInfo']["homeOverTimeScore"],
                                            "客隊延長賽比分": item['footballInfo']["awayOverTimeScore"]},
                if item['tableTennisInfo']:
                    sub_info["桌球相关信息"] = {"主队每盘获得局数": item["tableTennisInfo"]['homeGameScore'],
                                          "客队每盘获得局数": item["tableTennisInfo"]['awayGameScore'],
                                          "主队目前比分": item["tableTennisInfo"]['homeCurrentPoint'],
                                          "客队目前比分": item["tableTennisInfo"]['awayCurrentPoint'],
                                          "主队获得盘数": item["tableTennisInfo"]['homeSetScore'],
                                          "客队获得盘数": item["tableTennisInfo"]['awaySetScore'],
                                          "哪支队伍有人受伤": item["tableTennisInfo"]['playerInjury'],
                                          "目前盘数": item["tableTennisInfo"]['CurrentSet'],
                                          "目前发球方": item["tableTennisInfo"]['currentServe']},
                if item['badmintonInfo']:
                    sub_info["羽球相关信息"] = {"主队每盘获得局数": item["badmintonInfo"]['homeGameScore'],
                                          "客队每盘获得局数": item["badmintonInfo"]['awayGameScore'],
                                          "主队目前比分": item["badmintonInfo"]['homeCurrentPoint'],
                                          "客队目前比分": item["badmintonInfo"]['awayCurrentPoint'],
                                          "主队获得盘数": item["badmintonInfo"]['homeSetScore'],
                                          "客队获得盘数": item["badmintonInfo"]['awaySetScore'],
                                          "哪支队伍有人受伤": item["badmintonInfo"]['playerInjury'],
                                          "目前盘数": item["badmintonInfo"]['CurrentSet'],
                                          "目前发球方": item["badmintonInfo"]['currentServe']}
                result_list.append(sub_info)

            else:
                break
        return result_list

    @staticmethod
    def get_events_sse(filter_dic=None, start_diff=None, end_diff=None):
        """
        建立连接，获取赛事相关信息包含部分盘口信息
        :param event_id
        @return:
        """
        host = YamlUtil().load_common_config('sb')
        url = host['login_host'] + f'/sports/stream/V1/GetEvents'
        params = {"language": "zhcn",
                  'token': sb_token_context.get()}
        if start_diff or start_diff == 0:
            params['from'] = DateUtil.get_sb_search_time(start_diff)
        if end_diff or end_diff == 0:
            params['until'] = DateUtil.get_sb_search_time(end_diff, is_end=True)
        if filter_dic:
            params["query"] = SbFilterUtil.generate_query_str(filter_dic)
        client = requests.get(url, params=params, stream=True, headers=headers_stream)

        events_dic = {}
        while BusinessOperation.running_status.is_set():
            for chunk in client.iter_lines(decode_unicode=False):
                if BusinessOperation.running_status.is_set():
                    msg = chunk.decode().strip()
                    print("--------------------------")
                    print(msg)
                    if 'payload' in msg:
                        is_changed = False
                        data = json.loads(msg[6:])

                        for item in data['payload']['events']['add'] + data['payload']['events']['change']:
                            is_changed = True
                            print("============")
                            print(item)
                            # 平台需要的类型
                            if 'sportType' in item and str(item['sportType']) in SbSportEnum.sport_dic_t_zh.value:
                                sub_info = {"体育项目": item["sportType"], "联赛ID": item["leagueId"],
                                            "联赛名称": item["leagueName"], "赛事ID": item["eventId"],
                                            "赛事代码": item["eventCode"], "赛事状态": item["eventStatus"],
                                            "是否为主要盘口": item["isMainMarket"],
                                            "系统开赛时间": item["kickOffTime"],
                                            "开赛时间": item["globalShowTime"],
                                            "赛事比赛有多少节": item["gameSession"],
                                            "该赛事的母赛事ID": item["parentId"],
                                            "是否为滚球赛事": item["isLive"],
                                            "是否为串关赛事": item["isParlay"],
                                            "赛事是否支持实时兑现": item["isCashout"],
                                            "是否为虚拟赛事": item["isVirtualEvent"],
                                            "是否有滚球盘口": item["hasLiveMarket"],
                                            "该赛事的所有盘口数量": item["marketCount"],
                                            "该赛事的所有盘口投注类型": item["marketCategories"],
                                            "视频ID": item["streamingOption"],
                                            '团队相关信息': {"主队ID": item["teamInfo"]["homeId"],
                                                       "主队名称": item["teamInfo"]["homeName"],
                                                       "客队ID": item["teamInfo"]["awayId"],
                                                       "客队名称": item["teamInfo"]["awayName"]},
                                            '球赛相关信息': {"目前进行到第几节": item["gameInfo"][
                                                "livePeriod"],
                                                       "当前赛事时间以秒为单位": item["gameInfo"]["seconds"],
                                                       "是否为中场休息": item["gameInfo"]["isHt"],
                                                       "赛事是否中断(休息时间)": item["gameInfo"]["isBreak"],
                                                       "赛事是否关闭": item["gameInfo"]["isClosed"],
                                                       "赛事是否延迟": item["gameInfo"]["delayLive"],
                                                       "球赛状态": item["gameInfo"]["gameStatus"],
                                                       "目前赛事时间": item["gameInfo"]["inPlayTime"],
                                                       "主队滚球分数": item["gameInfo"]["liveHomeScore"],
                                                       "客队滚球分数": item["gameInfo"]["liveAwayScore"]}}
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
                                                            "主隊延長賽比分": item['footballInfo']["homeOverTimeScore"],
                                                            "客隊延長賽比分": item['footballInfo']["awayOverTimeScore"]},
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
                                                          "目前盘数": item["badmintonInfo"]['CurrentSet'],
                                                          "目前发球方": item["badmintonInfo"]['currentServe']}
                                events_dic[item["eventId"]] = sub_info
                        for item in data['payload']['events']['remove']:
                            is_changed = True
                            events_dic.pop(item['eventId'])

                        if events_dic and is_changed:
                            BusinessOperation.msg_queue.put(events_dic)
                else:
                    break

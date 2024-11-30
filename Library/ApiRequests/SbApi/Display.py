#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/6/22 11:09
import re

from Library.Common.Utils.Contexts import *
from Library.Common.Enum.SbSportEnum import SbSportEnum
import time
from collections import defaultdict

from Library.ApiRequests.SbApi.BaseOperation import BaseOperation
from Library.ApiRequests.SbApi.BusinessOperation import BusinessOperation
from Library.Common.Utils.DateUtil import DateUtil
from Library.Dao import Dao


class Display(object):

    @staticmethod
    def front(query_type, start_diff=1, end_diff=1):
        """
        显示上方球类数量
        @param query_type:
        @param start_diff:  开始时间，今天为0，昨天为-1，明天为1
        @param end_diff:  结束时间
        @return:
        """
        # 1.1 滚球
        if query_type == '滚球':
            BusinessOperation.start_stream('sports', {'env': 'sit', 'token': sb_token_context.get()})
            while True:
                time.sleep(0.1)
                if not BusinessOperation.sports_queue.empty():
                    data = BusinessOperation.sports_queue.get()
                    print("-------------------")
                    print('       '.join(
                        [f"【{value['体育类型']}】: {value['滚球数量']}" for key, value in data.items() if value['滚球数量']]))
        # 1.2 今日
        elif query_type == '今日':
            BusinessOperation.start_stream('sports', {'start_diff': 0, "end_diff": 0, 'env': 'sit',
                                                      'token': sb_token_context.get()})
            while True:
                time.sleep(0.1)
                if not BusinessOperation.sports_queue.empty():
                    data = BusinessOperation.sports_queue.get()
                    print("-------------------")
                    print('       '.join(
                        [f"【{value['体育类型']}】: {value['非滚球赛事数量'] + value['滚球数量']}" for key, value in data.items() if
                         value['非滚球赛事数量'] + value['滚球数量']]))
        elif query_type == '今日未开赛':
            BusinessOperation.start_stream('sports', {'start_diff': 0, "end_diff": 0, 'env': 'sit',
                                                      'token': sb_token_context.get()})
            while True:
                time.sleep(0.1)
                if not BusinessOperation.sports_queue.empty():
                    data = BusinessOperation.sports_queue.get()
                    print("-------------------")
                    print('       '.join(
                        [f"【{value['体育类型']}】: {value['非滚球赛事数量']}" for key, value in data.items() if
                         value['非滚球赛事数量']]))
        # 1.3 早盘
        elif query_type == '早盘':
            BusinessOperation.start_stream('sports', {'start_diff': start_diff, 'end_diff': end_diff, 'env': 'sit',
                                                      'token': sb_token_context.get()})
            while True:
                time.sleep(0.1)
                if not BusinessOperation.sports_queue.empty():
                    data = BusinessOperation.sports_queue.get()
                    print("-------------------")
                    print('       '.join(
                        [f"【{value['体育类型']}】: {value['非滚球赛事数量'] + value['滚球数量']}" for key, value in data.items() if
                         value['非滚球赛事数量']]))
        # 1.4 冠军
        elif query_type == '冠军':
            # start_stream('champion', {'env': 'sit', 'token': sb_token_context.get()})
            BusinessOperation.start_stream('sports', {'env': 'sit', 'token': sb_token_context.get()})
            while True:
                time.sleep(0.4)
                if not BusinessOperation.sports_queue.empty():
                    data = BusinessOperation.sports_queue.get()
                    print("-------------------")
                    print('       '.join(
                        [f"【{key}】: {value['优胜冠军赛事数量']}" for key, value in data.items() if value['优胜冠军赛事数量']]))

    @staticmethod
    def _print_base_info(event_data):
        event_id = event_data['赛事ID']
        team_info = event_data['团队相关信息']
        event_info = event_data['球赛相关信息']
        second = event_info['当前赛事时间以秒为单位']

        print(
            f"------------- \033[1;34m比赛ID: {event_id} 赛事状态: {event_data['赛事状态']}  比赛开始时间: UTC "
            f"{event_data['开赛时间']}  本地时间 {DateUtil.convert_utc_time_to_local(event_data['开赛时间'])}\033[0m-------"
            f"------")
        print(f"\033[32m{team_info['主队名称']}\033[0m VS \033[32m{team_info['客队名称']}"
              f"\033[0m  \033[31m{event_info['主队滚球分数']}\033[0m : \033[31m{event_info['客队滚球分数']}\033[0m")
        # 赛事时间：如果值为 0，则前端不显示时间
        if event_data['体育项目'] == '棒球':
            if '棒球相关信息' in event_data:
                event_time = f"\033[35m当前阶段: {event_data['棒球相关信息']['目前局数']} {event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
            else:
                event_time = f"\033[35m{event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
        elif event_data['体育项目'] == '网球':
            if '网球相关信息' in event_data:
                current_set = event_data['网球相关信息']['目前盘数']
                if current_set == 0:
                    event_time = f"\033[35m当前阶段: {event_data['网球相关信息']['目前盘数']} 未开始\033[0m"
                else:
                    event_time = f"\033[35m当前阶段: {event_data['网球相关信息']['目前盘数']} {event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
            else:
                event_time = f"\033[35m{event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
        # elif event_data['体育项目'] == '电子竞技':
        #     if event_info['阶段描述'] == '未开赛':
        #         event_time = f"\033[35m当前阶段: {event_info['阶段描述']}\033[0m"
        #     else:
        #         event_time = f"\033[35m当前阶段: {event_info['目前进行到第几节']} {event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
        elif event_data['体育项目'] == '羽毛球':
            parent_id = event_data['该赛事的母赛事ID'] if event_data['该赛事的母赛事ID'] != 0 else ""
            parent_str = f" 母赛事为:{parent_id}" if parent_id else ""
            if event_info['目前进行到第几节'] == 0:
                event_time = f'\033[35m(未开赛) 开赛时间：{DateUtil.convert_utc_time_to_local(event_data["开赛时间"])} {parent_str}\033[0m'
            else:
                event_time = f'\033[35m当前阶段: {event_info["目前进行到第几节"]} {event_info["阶段描述"]} {parent_str}\033[0m'
        elif event_data['体育项目'] == '斯诺克':
            period = event_info["主队滚球分数"] + event_info["客队滚球分数"]
            # if event_info['目前进行到第几节'] == 0:
            if period == 0:
                if event_data['该赛事的母赛事ID']:
                    event_time = f'\033[35m{DateUtil.convert_utc_time_to_local(event_data["开赛时间"])} 母赛事为:{event_data["该赛事的母赛事ID"]}\033[0m'
                else:
                    event_time = f'\033[35m当前阶段: {period} {event_info["阶段描述"]}\033[0m'
            else:
                event_time = f"\033[35m当前阶段: {period} {event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
        else:
            if event_info['目前进行到第几节'] == 0:
                if event_data['该赛事的母赛事ID']:
                    event_time = f'\033[35m{DateUtil.convert_utc_time_to_local(event_data["开赛时间"])} 母赛事为:{event_data["该赛事的母赛事ID"]}\033[0m'
                else:
                    event_time = f'\033[35m当前阶段: {event_info["目前进行到第几节"]} {event_info["阶段描述"]}\033[0m'
            else:
                event_time = f"\033[35m当前阶段: {event_info['目前进行到第几节']} {event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
        print(event_time)
        # 串关
        if event_data['是否为串关赛事']:
            support_parlay = '支持串关: '
            combo_str = f'{support_parlay}:  最少选择{event_data["盘口赔率项目列表"][0]["赛事串关数量限制"]}' if event_data[
                '盘口赔率项目列表'] else f'{support_parlay}:  暂无'

        else:
            combo_str = '不支持串关'
        support_video = "支持直播" if event_data['视频代码'] else "不支持直播"
        support_live = "支持滚球" if event_data['是否有滚球盘口'] else "不支持滚球"
        # print(f"上半场比分【{detail_dic[event_id]['主队半场得分']}:{detail_dic[event_id]['客队半场得分']}】
        # {support_video}  {support_live}    {combo_str}    总盘口数：\033[35m{event_data['该赛事的所有盘口数量']}\033[0m")
        if '球赛相关信息' in event_data:
            if event_data['体育项目'] == '网球':
                home_score = event_data['网球相关信息']['主队目前局数比分']
                away_score = event_data['网球相关信息']['客队目前局数比分']
            else:
                home_score = event_data['球赛相关信息']['主队滚球分数']
                away_score = event_data['球赛相关信息']['客队滚球分数']
            score_str = f"比分【{home_score}:{away_score}】     {support_video}  {support_live}    {combo_str}    "
        else:
            score_str = ""
        print(f"{score_str} 总盘口数：\033[35m{event_data['该赛事的所有盘口数量']}\033[0m")

    @staticmethod
    def _main_display_football(event_list, display_outcome_status=False):
        """
        大厅，足球显示
        @param event_list:
        @param display_outcome_status: 是否显示投注项状态
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['足球']
        for event_data in event_list:
            # print(event_data['赛事赛果信息列表']['各节的详细信息'])
            event_id = event_data['赛事ID']
            team_info = event_data['团队相关信息']
            event_info = event_data['球赛相关信息']
            second = event_info['当前赛事时间以秒为单位']

            print(
                f"------------- \033[1;34m比赛ID: {event_id} 赛事状态: {event_data['赛事状态']}  比赛开始时间: UTC "
                f"{event_data['开赛时间']}  美东 {DateUtil.convert_utc_time_to_local(event_data['开赛时间'])}\033[0m-----"
                f"--------")
            socket_info = event_data['足球相关信息']
            extra_str_home = f'({socket_info["主场黄牌数"]}黄{socket_info["主场红牌数"]}红)'
            extra_str_away = f'({socket_info["客场黄牌数"]}黄{socket_info["客场红牌数"]}红)'
            print(f"\033[32m{team_info['主队名称']}{extra_str_home}\033[0m VS \033[32m{team_info['客队名称']}"
                  f"{extra_str_away}\033[0m  \033[31m{event_info['主队滚球分数']}\033[0m : \033[31m{event_info['客队滚球分数']}\033[0m")
            # 赛事时间：如果值为 0，则前端不显示时间
            if event_info['目前进行到第几节'] == 0:
                event_time = f"\033[35m当前阶段: {event_info['目前进行到第几节']} {event_info['阶段描述']}\033[0m"
            else:
                event_time = f"\033[35m当前阶段: {event_info['目前进行到第几节']} {event_info['阶段描述']}, 进行时间:  {second // 60}:{second % 60}\033[0m"
            print(event_time)
            # 串关
            if event_data['是否为串关赛事']:
                support_parlay = '支持串关: '
                combo_str = f'{support_parlay}:  最少选择{event_data["盘口赔率项目列表"][0]["赛事串关数量限制"]}' if event_data[
                    '盘口赔率项目列表'] else f'{support_parlay}:  暂无'

            else:
                combo_str = '不支持串关'
            support_video = "支持直播" if event_data['视频代码'] else "不支持直播"
            support_live = "支持滚球" if event_data['是否有滚球盘口'] else "不支持滚球"
            # print(f"上半场比分【{detail_dic[event_id]['主队半场得分']}:{detail_dic[event_id]['客队半场得分']}】
            # {support_video}  {support_live}    {combo_str}    总盘口数：\033[35m{event_data['该赛事的所有盘口数量']}\033[0m")
            if '球赛相关信息' in event_data:
                home_score = event_data['球赛相关信息']['主队滚球分数']
                away_score = event_data['球赛相关信息']['客队滚球分数']
                score_str = f"比分【{home_score}:{away_score}】     {support_video}  {support_live}    {combo_str}    "
            else:
                score_str = ""
            print(f"{score_str} 总盘口数：\033[35m{event_data['该赛事的所有盘口数量']}\033[0m")
            markets = event_data['盘口赔率项目列表']
            # print(markets)
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让球'] and x['排序球头'] == 1, markets))
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic['大小'] and x['排序球头'] == 1, markets))
            half_win = list(filter(lambda x: str(x['投注类型']) in markets_dic['半场独赢'], markets))  # 包括上下半场
            half_handicap = list(
                filter(lambda x: str(x['投注类型']) in markets_dic['半场让球'] and x['排序球头'] == 1, markets))  # 包括上下半场
            half_dx = list(
                filter(lambda x: str(x['投注类型']) in markets_dic['半场大小'] and x['排序球头'] == 1, markets))  # 包括上下半场
            line_1 = []
            line_2 = []
            line_3 = []

            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场独赢
                    line_1.append(
                        f'{bet_dic["主胜"]["投注类型选项名称"]} {bet_dic["主胜"]["赔率相关信息"]}{status_str}' if '主胜' in bet_list else "")
                    line_3.append(
                        f'{bet_dic["客胜"]["投注类型选项名称"]} {bet_dic["客胜"]["赔率相关信息"]}{status_str}' if '客胜' in bet_list else "")
                    line_2.append(
                        f'{bet_dic["和局"]["投注类型选项名称"]} {bet_dic["和局"]["赔率相关信息"]}{status_str}' if '和局' in bet_list else "")
                else:
                    line_1.append(f'{bet_dic["主胜"]["投注类型选项名称"]} 🔒{status_str}        ' if '主胜' in bet_list else "")
                    line_3.append(f'{bet_dic["客胜"]["投注类型选项名称"]} 🔒{status_str}        ' if '客胜' in bet_list else "")
                    line_2.append(f'{bet_dic["和局"]["投注类型选项名称"]} 🔒{status_str}        ' if '和局' in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
                line_3.append("———")
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                home_name = event_data['团队相关信息']["主队名称"]
                away_name = event_data['团队相关信息']["客队名称"]
                operate_home = "+" if bet_dic[home_name]["球头"] > 0 else ""
                operate_away = "+" if bet_dic[away_name]["球头"] > 0 else ""
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':

                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_dic else "")
                else:
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]}  🔒{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]}  🔒{status_str}' if away_name in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            if full_dx:
                status_str = f"-{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'大{bet_dic["大"]["球头"]} 🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'小{bet_dic["小"]["球头"]} 🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            if half_win:
                status_str = f"-{event_data['赛事状态']} {half_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = half_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if half_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{bet_dic["主胜"]["投注类型选项名称"]}{bet_dic["主胜"]["赔率相关信息"]}{status_str}' if '主胜' in bet_list else "")
                    line_3.append(
                        f'{bet_dic["客胜"]["投注类型选项名称"]}{bet_dic["客胜"]["赔率相关信息"]}{status_str}' if '客胜' in bet_list else "")
                    line_2.append(
                        f'{bet_dic["和局"]["投注类型选项名称"]}{bet_dic["和局"]["赔率相关信息"]}{status_str}' if '和局' in bet_list else "")
                else:
                    line_1.append(f'{bet_dic["主胜"]["投注类型选项名称"]}🔒{status_str}' if '主胜' in bet_list else "")
                    line_3.append(f'{bet_dic["客胜"]["投注类型选项名称"]}🔒{status_str}' if '客胜' in bet_list else "")
                    line_2.append(f'{bet_dic["和局"]["投注类型选项名称"]}🔒{status_str}' if '和局' in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
                line_3.append("———")

            if half_handicap:
                status_str = f"-{event_data['赛事状态']} {half_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = half_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                home_name = event_data['团队相关信息']["主队名称"]
                away_name = event_data['团队相关信息']["客队名称"]
                operate_home = "+" if bet_dic[home_name]["球头"] > 0 else ""
                operate_away = "+" if bet_dic[away_name]["球头"] > 0 else ""
                if half_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_dic else "")
                else:
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} 🔒{status_str}' if home_name in bet_dic else " ")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} 🔒{status_str}' if away_name in bet_dic else " ")
            else:
                line_1.append("———")
                line_2.append("———")
            if half_dx:
                status_str = f"-{event_data['赛事状态']} {half_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = half_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if half_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'大{bet_dic["大"]["球头"]} 🔒{status_str}' if '大' in bet_dic else " ")
                    line_2.append(f'小{bet_dic["小"]["球头"]} 🔒{status_str}' if '小' in bet_dic else " ")
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 16
            line_0 = [item.ljust(fill_len - 3, ' ') for item in ['全场独赢', '全场让球', '全场大小', '半场独赢', '半场让球', '半场大小']]
            line_3.insert(1, " " * fill_len)
            line_3.insert(1, "")
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            line_3 = [item.ljust(fill_len, ' ') for item in line_3]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))
            print("".join(line_3))

    @staticmethod
    def _main_display_basketball(event_list, display_outcome_status=False):
        """
        大厅，篮球显示
        @param event_list:
        @param display_outcome_status: 是否显示投注项状态
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['篮球']
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场独赢
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic["独赢"], markets))
            # 让分
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic["让分"] and x['排序球头'] == 1, markets))
            # 总分大小盘
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic["大小盘"] and x['排序球头'] == 1, markets))
            # 球队大小盘
            home_team_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic["主队大小盘"] and x['排序球头'] == 1, markets))
            away_team_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic["客队大小盘"] and x['排序球头'] == 1, markets))
            line_1 = []
            line_2 = []
            # 全场独赢
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(
                        f'{bet_dic[home_name]["投注类型选项名称"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'{bet_dic[away_name]["投注类型选项名称"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'{bet_dic[home_name]["投注项类型选项名称"]} 🔒{status_str}' if '主胜' in bet_list else "")
                    line_2.append(f'{bet_dic[away_name]["投注项类型选项名称"]} 🔒{status_str}' if '客胜' in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 让分
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                home_name = event_data['团队相关信息']["主队名称"]
                away_name = event_data['团队相关信息']["客队名称"]
                operate_home = "+" if bet_dic[home_name]["球头"] > 0 else ""
                operate_away = "+" if bet_dic[away_name]["球头"] > 0 else ""
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}'
                        if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}'
                        if away_name in bet_dic else "")
                else:
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} 🔒{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} 🔒{status_str}' if away_name in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 总分大小
            if full_dx:
                status_str = f"-{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{bet_dic["大"]["投注类型选项名称"]}{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'{bet_dic["小"]["投注类型选项名称"]}{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'{bet_dic["大"]["投注类型选项名称"]}🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'{bet_dic["小"]["投注类型选项名称"]}🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 球队总分大小
            if home_team_dx:
                status_str = f"{event_data['赛事状态']} {home_team_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = home_team_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if home_team_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    over = f'{bet_dic["大"]["投注类型选项名称"]}{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else ""
                    below = f'{bet_dic["小"]["投注类型选项名称"]}{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else ""
                else:
                    over = f'大🔒{status_str}' if '大' in bet_dic else ""
                    below = f'小🔒{status_str}' if '小' in bet_dic else ""
                line_1.append(over + "  " + below)
            else:
                line_1.append("———")
                line_2.append("———")
            if away_team_dx:
                status_str = f"-{event_data['赛事状态']} {away_team_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = away_team_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if away_team_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    over = f'{bet_dic["大"]["投注类型选项名称"]}{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else ""
                    below = f'{bet_dic["小"]["投注类型选项名称"]}{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else ""
                else:
                    over = f'大 🔒{status_str}' if '大' in bet_dic else ""
                    below = f'小 🔒{status_str}' if '小' in bet_dic else ""
                line_2.append(over + "  " + below)
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 15
            line_0 = [item.ljust(fill_len, ' ') for item in ['全场独赢', '让分', '总分', '球队总分']]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

            if "篮球相关信息" in event_data:
                home_score: list = event_data["篮球相关信息"]["主队目前得分"]
                away_score: list = event_data["篮球相关信息"]["客队目前得分"]
                period = event_data['球赛相关信息']['目前进行到第几节']

                print("局比分： ", "  ".join([f'{home_score[index]}-{away_score[index]}' for index in
                                          range(period if period != 99 else 4)]))

    @staticmethod
    def _main_display_volleyball(event_list, display_outcome_status=False):
        """
        大厅，排球显示
        @param event_list:
        @param display_outcome_status:
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['排球']
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场胜负
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            # 让分
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让分'] and x['排序球头'] == 1, markets))
            # 总分大小盘
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic['大小'] and x['排序球头'] == 1, markets))
            # 球队大小盘
            team_dx = list(filter(lambda x: str(x['投注类型']) in markets_dic['球队大小'] and x['排序球头'] == 1, markets))
            line_1 = []
            line_2 = []
            # 全场胜负
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(
                        f'{bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'{bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 让分
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    operate_home = "+" if bet_dic['主队']["球头"] > 0 else ""
                    operate_away = "+" if bet_dic['客队']["球头"] > 0 else ""
                    line_1.append(
                        f'{operate_home}{bet_dic["主队"]["球头"]} {bet_dic["主队"]["赔率相关信息"]}{status_str}' if '主队' in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic["客队"]["球头"]} {bet_dic["客队"]["赔率相关信息"]}{status_str}' if '客队' in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}' if '主队' in bet_dic else "")
                    line_2.append(f'🔒{status_str}' if '客队' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 总分大小
            if full_dx:
                status_str = f"-{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'🔒' if '大' in bet_dic else "")
                    line_2.append(f'🔒' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 15 if not display_outcome_status else 30
            line_0 = [item.ljust(fill_len, ' ') for item in ['独赢', '让分', '总分']]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

            total_loop = event_data["赛事比赛有多少节"]

            if '排球相关信息' in event_data:
                if event_data["排球相关信息"]:
                    home_score: list = event_data["排球相关信息"][0]["主队每盘获得局数"]
                    away_score: list = event_data["排球相关信息"][0]["客队每盘获得局数"]
                    print("局比分： ", "  ".join([f'{home_score[index]}-{away_score[index]}' for index in
                                              range(event_data['排球相关信息'][0]['目前进行的节数'])]),
                          f"    {total_loop}局{total_loop // 2 + 1}胜",
                          f'总分{sum(home_score)}-{sum(away_score)}({sum(home_score + away_score)})')

    @staticmethod
    def _main_display_tennis(event_list, display_outcome_status=False):
        """
        大厅，网球显示
        @param event_list:
        @param display_outcome_status:
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['网球']
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场胜负
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            # 让盘
            set_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让盘'] and x['排序球头'] == 1, markets))
            # 让局
            ju_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让局'] and x['排序球头'] == 1, markets))
            # 总局数
            total_set = list(filter(lambda x: str(x['投注类型']) == markets_dic['局数'] and x['排序球头'] == 1, markets))
            line_1 = []
            line_2 = []
            # 全场胜负
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(
                        f'主{bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'客{bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 让盘
            if set_handicap:
                status_str = f"-{event_data['赛事状态']} {set_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = set_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if set_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    operate_home = "+" if bet_dic["主队"]["球头"] > 0 else ""
                    operate_away = "+" if bet_dic["客队"]["球头"] > 0 else ""
                    line_1.append(
                        f'{operate_home}{bet_dic["主队"]["球头"]} ({bet_dic["主队"]["赔率相关信息"]}){status_str}' if '主队' in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic["客队"]["球头"]} ({bet_dic["客队"]["赔率相关信息"]}){status_str}' if '客队' in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}' if '主队' in bet_dic else "")
                    line_2.append(f'🔒{status_str}' if '客队' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 让局
            if ju_handicap:
                status_str = f"-{event_data['赛事状态']} {ju_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = ju_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if ju_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    operate_home = "+" if bet_dic["主队"]["球头"] > 0 else ""
                    operate_away = "+" if bet_dic["客队"]["球头"] > 0 else ""
                    line_1.append(
                        f'{operate_home}{bet_dic["主队"]["球头"]} ({bet_dic["主队"]["赔率相关信息"]}){status_str}' if '主队' in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic["客队"]["球头"]} ({bet_dic["客队"]["赔率相关信息"]}){status_str}' if '客队' in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}' if '主队' in bet_dic else "")
                    line_2.append(f'🔒{status_str}' if '客队' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 总局数
            if total_set:
                status_str = f"-{event_data['赛事状态']} {total_set[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = total_set[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if total_set[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'[让局]{bet_dic["大"]["球头"]} ({bet_dic["大"]["赔率相关信息"]}){status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'[让局]{bet_dic["小"]["球头"]} ({bet_dic["小"]["赔率相关信息"]}){status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 15
            line_0 = [item.ljust(fill_len, ' ') for item in ['独赢', '让盘', '让局', '总局数']]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

            total_loop = event_data["赛事比赛有多少节"]
            if '网球相关信息' in event_data:
                home_score: list = event_data["网球相关信息"]["主队每盘获得局数"]
                away_score: list = event_data["网球相关信息"]["客队每盘获得局数"]
                print("局比分： ", "  ".join([f'{home_score[index]}-{away_score[index]}' for index in
                                          range(event_data['网球相关信息']['目前盘数'])]),
                      f"    {total_loop}盘{total_loop // 2 + 1}胜",
                      f'总分{sum(home_score)}-{sum(away_score)}({sum(home_score + away_score)})')

    @staticmethod
    def _main_display_baseball(event_list, display_outcome_status=False):
        """
        大厅，棒球显示
        @param event_list:
        @param display_outcome_status:
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['棒球']
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场胜负
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            # 让球
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让球'] and x['排序球头'] == 1, markets))
            # 全场大小
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic['大小'] and x['排序球头'] == 1, markets))
            # 单双
            full_ds = list(filter(lambda x: str(x['投注类型']) == markets_dic['单双'], markets))
            line_1 = []
            line_2 = []
            # 全场胜负
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(f'{bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(f'{bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 让球
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    operate_home = "+" if bet_dic[home_name]["球头"] > 0 else ""
                    operate_away = "+" if bet_dic[away_name]["球头"] > 0 else ""
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}        ' if home_name in bet_dic else "")
                    line_2.append(f'🔒{status_str}        ' if away_name in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场大小
            if full_dx:
                status_str = f"-{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 单双
            if full_ds:
                print("-=-=-=-=-=!!!!!")
                status_str = f"-{event_data['赛事状态']} {full_ds[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_ds[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_ds[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'{bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 15
            line_0 = [item.ljust(fill_len, ' ') for item in ['独赢', '让球', '大小', '单/双']]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

            if '棒球相关信息' in event_data:
                total_loop = event_data["棒球相关信息"]['目前局数']
                home_score: list = event_data["棒球相关信息"]["主队目前得分"]
                away_score: list = event_data["棒球相关信息"]["客队目前得分"]
                print("局比分： ", " ".join([f'{home_score[index]}-{away_score[index]}' for index in
                                         range(total_loop)]), f"出局{event_data['棒球相关信息']['目前出局数']}")

    @staticmethod
    def _main_display_snooker(event_list, display_outcome_status=False):
        """
        大厅，斯诺克显示
        @param event_list:
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['斯诺克']
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场胜负
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            # 全场让局
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让局'] and x['排序球头'] == 1, markets))
            # 总局数
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic['总局数'] and x['排序球头'] == 1, markets))
            line_1 = []
            line_2 = []
            # 全场胜负
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(
                        f'{bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'{bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场让球
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    operate_home = "+" if bet_dic[home_name]["球头"] > 0 else ""
                    operate_away = "+" if bet_dic[away_name]["球头"] > 0 else ""
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_dic else "")
                else:
                    line_1.append(f'{bet_dic[home_name]["球头"]}🔒{status_str}' if home_name in bet_dic else "")
                    line_2.append(f'{bet_dic[away_name]["球头"]}🔒{status_str}' if away_name in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场大小
            if full_dx:
                status_str = f"-{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} ({bet_dic["大"]["赔率相关信息"]}){status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}){status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'大{bet_dic["大"]["球头"]}🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'小{bet_dic["小"]["球头"]}🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 15
            line_0 = [item.ljust(fill_len - 1, ' ') for item in ['独赢', '让局', '总局数']]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

            if '桌球相关信息' in event_data:
                total_loop = event_data["桌球相关信息"]['目前盘数']
                home_score: list = event_data["桌球相关信息"]["主队获得盘数"]
                away_score: list = event_data["桌球相关信息"]["客队获得盘数"]
                print("局比分： ", " ".join([f'{home_score[index]}-{away_score[index]}' for index in range(total_loop)]))

    @staticmethod
    def _main_display_badminton(event_list, display_outcome_status=False):
        """
        大厅，羽毛球显示
        @param event_list:
        @param display_outcome_status:
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value['羽毛球']
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场独赢
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            # 全场让局
            # print(markets_dic)
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['全场让局'] and x['排序球头'] == 1,
                                        markets))
            # 让分
            full_score_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让分'] and x['排序球头'] == 1,
                                              markets))
            # 全场总分
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic['全场总分'] and x['排序球头'] == 1, markets))
            line_1 = []
            line_2 = []
            # 全场胜负
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(
                        f'主 {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'客 {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场让局
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    operate_home = "+" if bet_dic["主队"]["球头"] > 0 else ""
                    operate_away = "+" if bet_dic["客队"]["球头"] > 0 else ""
                    line_1.append(
                        f'{operate_home}{bet_dic["主队"]["球头"]} {bet_dic["主队"]["赔率相关信息"]}'
                        f'{operate_away}{status_str}' if '主队' in bet_dic else "")
                    line_2.append(
                        f'{bet_dic["客队"]["球头"]} {bet_dic["客队"]["赔率相关信息"]}'
                        f'{status_str}' if '客队' in bet_dic else "")
                else:
                    line_1.append(
                        f'{bet_dic["主队"]["球头"]}🔒{status_str}' if '主队' in bet_dic else "")
                    line_2.append(
                        f'{bet_dic["客队"]["球头"]}🔒{status_str}' if '客队' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            # 全场让分
            if full_score_handicap:
                status_str = f"-{event_data['赛事状态']} {full_score_handicap[0]['盘口状态']} " if \
                    display_outcome_status else ""
                list_1 = full_score_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                operate_home = "+" if bet_dic["主队"]["球头"] > 0 else ""
                operate_away = "+" if bet_dic["客队"]["球头"] > 0 else ""
                if full_score_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{operate_home}{bet_dic["主队"]["球头"]} {bet_dic["主队"]["赔率相关信息"]}'
                        f'{status_str}' if "主队" in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic["客队"]["球头"]} {bet_dic["客队"]["赔率相关信息"]}'
                        f'{status_str}' if "客队" in bet_dic else "")
                else:
                    line_1.append(
                        f'{operate_home}{bet_dic["主队"]["球头"]}🔒{status_str}' if "主队" in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic["客队"]["球头"]}🔒{status_str}' if "客队" in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场总分
            if full_dx:
                status_str = f"{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            fill_len = 15
            line_0 = [item.ljust(fill_len - 2, ' ') for item in ['全场独赢', '全场让局', '让分', '全场总分']]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

            if '羽球相关信息' in event_data and event_data["羽球相关信息"]:
                home_score: list = event_data["羽球相关信息"]["主队每盘获得局数"]
                away_score: list = event_data["羽球相关信息"]["客队每盘获得局数"]
                total_loop = event_data["赛事比赛有多少节"]
                current_loop = event_data["球赛相关信息"]["目前进行到第几节"]
                print("局比分： ",
                      " ".join([f'{home_score[index]}-{away_score[index]}' for index in range(current_loop)]),
                      ' ' * 50 + f"{total_loop}盘{total_loop // 2 + 1}胜")

    @staticmethod
    def _main_display_esports(event_list, sport_name, display_outcome_status=False):
        """
        大厅，电子竞技显示
        @param event_list:
        @param sport_name:
        @param display_outcome_status:
        @return:
        """
        markets_dic = SbSportEnum.main_markets_dic.value[sport_name]
        for event_data in event_list:
            # print(event_data)
            home_name = event_data["团队相关信息"]["主队名称"]
            away_name = event_data["团队相关信息"]["客队名称"]
            Display._print_base_info(event_data)
            markets = event_data['盘口赔率项目列表']
            # 全场胜负
            full_win = list(filter(lambda x: str(x['投注类型']) == markets_dic['独赢'], markets))
            # 全场让球
            point = 0 if sport_name == '电子竞技' else 1
            full_handicap = list(filter(lambda x: str(x['投注类型']) == markets_dic['让球'] and x['排序球头'] == point,
                                        markets))
            # 全场大小
            full_dx = list(filter(lambda x: str(x['投注类型']) == markets_dic['大小'] and x['排序球头'] == point, markets))
            line_1 = []
            line_2 = []
            # 全场胜负
            if full_win:
                status_str = f"-{event_data['赛事状态']} {full_win[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_win[0]["盘口赔率项目列表"]
                bet_list = [i["投注类型选项名称"] for i in list_1]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_win[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    # 全场胜负
                    line_1.append(
                        f'主 {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_list else "")
                    line_2.append(
                        f'客 {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_list else "")
                else:
                    line_1.append(f'主 🔒{status_str}' if home_name in bet_list else "")
                    line_2.append(f'客 🔒{status_str}' if away_name in bet_list else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场让球
            if full_handicap:
                status_str = f"-{event_data['赛事状态']} {full_handicap[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_handicap[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                operate_home = "+" if bet_dic[home_name]["球头"] > 0 else ""
                operate_away = "+" if bet_dic[away_name]["球头"] > 0 else ""
                if full_handicap[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} {bet_dic[home_name]["赔率相关信息"]}{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} {bet_dic[away_name]["赔率相关信息"]}{status_str}' if away_name in bet_dic else "")
                else:
                    line_1.append(
                        f'{operate_home}{bet_dic[home_name]["球头"]} 🔒{status_str}' if home_name in bet_dic else "")
                    line_2.append(
                        f'{operate_away}{bet_dic[away_name]["球头"]} 🔒{status_str}' if away_name in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")
            # 全场大小
            if full_dx:
                status_str = f"-{event_data['赛事状态']} {full_dx[0]['盘口状态']} " if display_outcome_status else ""
                list_1 = full_dx[0]["盘口赔率项目列表"]
                bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                if full_dx[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                    line_1.append(
                        f'大{bet_dic["大"]["球头"]} {bet_dic["大"]["赔率相关信息"]}{status_str}' if '大' in bet_dic else "")
                    line_2.append(
                        f'小{bet_dic["小"]["球头"]} {bet_dic["小"]["赔率相关信息"]}{status_str}' if '小' in bet_dic else "")
                else:
                    line_1.append(f'大{bet_dic["大"]["球头"]} 🔒{status_str}' if '大' in bet_dic else "")
                    line_2.append(f'小{bet_dic["小"]["球头"]} 🔒{status_str}' if '小' in bet_dic else "")
            else:
                line_1.append("———")
                line_2.append("———")

            # 全场单双
            if sport_name == '冰上曲棍球':
                full_ds = list(filter(lambda x: str(x['投注类型']) == markets_dic['单双'], markets))
                if full_ds:
                    status_str = f"-{event_data['赛事状态']} {full_ds[0]['盘口状态']} " if display_outcome_status else ""
                    list_1 = full_ds[0]["盘口赔率项目列表"]
                    bet_dic = {i["投注类型选项名称"]: i for i in list_1}
                    if full_ds[0]['盘口状态'] in ['running'] and event_data['赛事状态'] == 'running':
                        line_1.append(
                            f'单{bet_dic["单"]["球头"]} {bet_dic["单"]["赔率相关信息"]}{status_str}' if '单' in bet_dic else "")
                        line_2.append(
                            f'双{bet_dic["双"]["球头"]} {bet_dic["双"]["赔率相关信息"]}{status_str}' if '双' in bet_dic else "")
                    else:
                        line_1.append(f'单{bet_dic["单"]["球头"]}🔒{status_str}' if '单' in bet_dic else "")
                        line_2.append(f'双{bet_dic["双"]["球头"]}🔒{status_str}' if '双' in bet_dic else "")
                else:
                    line_1.append("———")
                    line_2.append("———")

            fill_len = 15
            markets_name_list = ['全场独赢', '全场让球', '全场大小']
            if sport_name == '冰上曲棍球':
                markets_name_list.append("全场单双")
            line_0 = [item.ljust(fill_len - 3, ' ') for item in markets_name_list]
            line_1 = [item.ljust(fill_len, ' ') for item in line_1]
            line_2 = [item.ljust(fill_len, ' ') for item in line_2]
            print()
            print("".join(line_0))
            print("".join(line_1))
            print("".join(line_2))

    @staticmethod
    # 2.大厅比赛信息 早盘、今日、滚球
    def main_page(sport_name, date_type="", league_id=None, event_id=None, start_diff=1, end_diff=15,
                  only_hot=False, grep_not_live=False):
        """
        大厅比赛信息
        @param sport_name: 体育类型
        @param date_type: 滚球 ｜ 今日 ｜ 早盘 ｜ 冠军
        @param only_hot:  只要热门  False | True
        @param league_id: 联赛id
        @param event_id: 比赛id
        @param start_diff:  开始时间，今天为0，昨天为-1，明天为1
        @param end_diff:  结束时间
        @param grep_not_live:  只针对pc今日，筛选 今日未开赛的比赛列表
        @return:
        """
        # filter_dic = {f'体育项目名称': f' in ({",".join(list(SbSportEnum.sport_dic_t_zh.value.keys()))})'}
        filter_dic = {}
        args = {"header": sb_client_header_context.get()}
        if league_id:
            filter_dic["联赛id"] = f" eq {league_id}"
            args = {'env': 'sit', 'token': sb_token_context.get(), "filter_dic": filter_dic}
        if date_type == '滚球':
            filter_dic["是否为滚球赛事"] = " eq true"
            filter_dic["体育项目名称"] = f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"
            if event_id:
                filter_dic["赛事id"] = f" eq {event_id}"
            args = {'env': 'sit', 'token': sb_token_context.get(), "filter_dic": filter_dic}
        elif date_type == '今日':
            filter_dic["体育项目名称"] = f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"
            if event_id:
                filter_dic["赛事id"] = f" eq {event_id}"
            if grep_not_live:
                filter_dic["是否为滚球赛事"] = f" ne true"
            args = {'env': 'sit', 'token': sb_token_context.get(), "start_diff": 0, "end_diff": 0,
                    "filter_dic": filter_dic}
        elif date_type == '早盘':
            filter_dic["体育项目名称"] = f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"
            if event_id:
                filter_dic["赛事id"] = f" eq {event_id}"
            args = {'env': 'sit', 'token': sb_token_context.get(), 'start_diff': start_diff,
                    'end_diff': end_diff, "filter_dic": filter_dic}

        all_markets_id = []
        [all_markets_id.extend(item1) for item1 in [item if type(item) in (list, tuple) else [item] for item in
                                                    SbSportEnum.main_markets_dic.value[sport_name].values()]]
        filter_dic['包括的盘口'] = ",".join(all_markets_id)
        args['only_hot'] = only_hot
        args['header'] = sb_client_header_context.get()
        BusinessOperation.start_stream('events', args)
        # print("------------")
        # print()
        # print(args)
        while True:
            time.sleep(0.5)
            if not BusinessOperation.event_queue.empty():
                data = BusinessOperation.event_queue.get().values()
                # 联赛列表
                league_list = list(set([(item["联赛名称"], item["联赛ID"]) for item in data]))
                league_list = [_[0] for _ in sorted(league_list, key=lambda _: _[1])]
                for index, league in enumerate(league_list):
                    event_list = list(filter(lambda x: x['联赛名称'] == league, data))
                    event_list = sorted(event_list, key=lambda _: _["开赛时间"])
                    print("|" * 100)
                    print(f"||              \033[1;34m{index + 1}/{len(league_list)}【{league}  "
                          f"联赛ID:{event_list[0]['联赛ID']}】  比赛数量({len(event_list)})\033[0m"
                          f"               总比赛({len(data)})")
                    print("|" * 100)
                    if sport_name == '足球':
                        Display._main_display_football(event_list)
                    elif sport_name == '篮球':
                        Display._main_display_basketball(event_list)
                    elif sport_name == '排球':
                        Display._main_display_volleyball(event_list)
                    elif sport_name == '网球':
                        Display._main_display_tennis(event_list)
                    elif sport_name == '斯诺克':
                        Display._main_display_snooker(event_list)
                    elif sport_name == '羽毛球':
                        Display._main_display_badminton(event_list)
                    elif sport_name == '棒球':
                        Display._main_display_baseball(event_list)
                    elif sport_name in ('电子竞技', "冰上曲棍球", "美式足球"):
                        Display._main_display_esports(event_list, sport_name)

    @staticmethod
    # 2.大厅比赛信息 - 冠军
    def main_page_champion(sport_name, league_name=""):
        """
        大厅比赛信息
        @param sport_name: 体育类型
        @param league_name:
        @return:
        """
        filter_dic = {f'体育项目名称': f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"}
        if league_name:
            filter_dic["联赛名称"] = f" eq '{league_name}'"
        BusinessOperation.start_stream('champion',
                                       {'env': 'sit', 'token': sb_token_context.get(), "filter_dic": filter_dic})
        while True:
            time.sleep(0.5)
            if not BusinessOperation.out_right_queue.empty():
                data = list(BusinessOperation.out_right_queue.get().values())
                # event_count = [ for item in data]
                for index, league in enumerate(data):
                    print("|" * 100)
                    print(
                        f"||  \033[1;34m第{index + 1}/{len(data)}【{league['联赛名称']}】   总投注项数量:{len(league['队伍相关信息'])}   \033[0m")
                    print(
                        f"|| \033[1;34m赛事日期 UTC {league['赛事日期']}  美东 {DateUtil.convert_utc_time_to_local(league['赛事日期'])}  联赛ID: {league['赛事标识符']}  \033[0m")
                    print("|" * 100)
                    # print(league)
                    for event_data in league['队伍相关信息']:
                        if event_data['盘口状态'] == 'running':
                            print(
                                f"  \033[1;34m{event_data['队伍名称']}  赔率：{event_data['赔率']}   最大投注额:{event_data['最大投注额']}\033[0m")
                        else:
                            print(f"  \033[1;34m{event_data['队伍名称']}  🔒\033[0m")

    # 3.大厅联赛列表
    @staticmethod
    def get_main_page_league_list(sport_name, league_id="", date_type=None, ignore_sport_type='是', start_diff=0,
                                  end_diff=15):
        """
        大厅联赛列表信息
        @param sport_name: 体育类型
        @param date_type: 今日 ｜ 滚球 ｜ 早盘
        @param league_id:
        @param ignore_sport_type: 是否忽略球类过滤项     是 ｜ 否
        @param start_diff
        @param end_diff
        @return:
        """
        filter_dic = {f'体育项目名称': f' eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}'}
        if league_id:
            filter_dic["联赛ID"] = f" eq '{league_id}'"
        if ignore_sport_type == '是':
            BusinessOperation.start_stream('leagues',
                                           {'env': 'sit', 'token': sb_token_context.get(), "filter_dic": filter_dic})
        else:
            if date_type == '滚球':
                filter_dic["该体育项目的滚球赛事数量"] = " gt 0"
                filter_dic["体育项目名称"] = f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"
                BusinessOperation.start_stream('leagues', {'env': 'sit', 'token': sb_token_context.get(),
                                                           "filter_dic": filter_dic})
            elif date_type == '今日':
                filter_dic["体育项目名称"] = f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"
                BusinessOperation.start_stream('leagues',
                                               {'env': 'sit', 'token': sb_token_context.get(), "start_diff": 0,
                                                "end_diff": 0, "filter_dic": filter_dic})
            elif date_type == '早盘':
                filter_dic["体育项目名称"] = f" eq {SbSportEnum.sport_dic_f_zh.value[sport_name]}"
                BusinessOperation.start_stream('leagues',
                                               {'env': 'sit', 'token': sb_token_context.get(), 'start_diff': start_diff,
                                                'end_diff': end_diff, "filter_dic": filter_dic})
        while True:
            time.sleep(0.1)
            if not BusinessOperation.league_queue.empty():
                data = BusinessOperation.league_queue.get().values()
                print(f"\033[34m{'*' * 30}\033[0m")
                print(f"共 {len(data)} 个联赛")
                [print(f"{item['联赛名称']}") for item in data]

    @staticmethod
    def _detail_front_football(event_data):
        """
        赛事详情页 - 上方统计
        @param event_data:
        @return:
        """
        event_msg = []
        event_id = event_data["赛事ID"]
        team_info = event_data['团队相关信息']
        event_info = event_data['球赛相关信息']
        second = event_info['当前赛事时间以秒为单位']
        # detail_dic = BusinessOperation.get_game_details([event_id])[event_id]
        event_msg.append(f"\033[31m【{event_data['联赛名称']}】\033[0m  {event_id}")
        event_time = f"\033[35m当前阶段:\033[0m \033[31m{event_info['目前进行到第几节']} {event_info['阶段描述']}\033[0m  " \
                     f"\033[35m进行时间:\033[0m  \033[31m{second // 60}:{second % 60}\033[0m"
        event_msg.append(event_time)

        # 串关
        if event_data['是否为串关赛事']:
            support_parlay = '支持串关: '
            combo_str = f'{support_parlay}最少选择{event_data["盘口赔率项目列表"][0]["赛事串关数量限制"]}' if event_data[
                '盘口赔率项目列表'] else f'{support_parlay}:  暂无'

        else:
            combo_str = '不支持串关'
        support_video = "支持直播" if event_data['视频代码'] else "不支持直播"

        event_msg.append(f'\033[35m {combo_str}   {support_video}\033[0m')

        home_line = defaultdict(int)
        away_line = defaultdict(int)
        home_line["队名"] = team_info['主队名称']
        away_line["队名"] = team_info['客队名称']
        # 半场得分
        # home_line["半场"] = detail_dic['主队半场得分']
        # away_line["半场"] = detail_dic['客队半场得分']
        # 全场得分
        home_line["全场"] = event_info['主队滚球分数']
        away_line["全场"] = event_info['客队滚球分数']
        # 红黄牌
        # football_data = event_data['足球相关信息']
        # home_line["红牌"] = football_data['主场红牌数']
        # away_line["红牌"] = football_data['客场红牌数']
        # home_line["黄牌"] = football_data['主场黄牌数']
        # away_line["黄牌"] = football_data['客场黄牌数']
        # detail_dic[event_id]['角球进球顺序']
        event_msg.append(f"\033[35m {'      '.join([f'[{key}]{value}' for key, value in home_line.items()])}\033[0m")
        event_msg.append(f"\033[35m {'      '.join([f'[{key}]{value}' for key, value in away_line.items()])}\033[0m")
        return event_msg

    # 4.比赛详情
    @staticmethod
    def get_match_detail_page(event_id):
        BusinessOperation.start_stream('markets', {'env': 'sit', 'token': sb_token_context.get(), "event_id": event_id})
        BusinessOperation.start_stream('events', {'env': 'sit', 'token': sb_token_context.get(),
                                                  "filter_dic": {"赛事id": f" eq {event_id}"},
                                                  "header": sb_client_header_context.get()})
        last_msg = [[], []]
        event_status = ""
        while True:
            latest_msg = [[], []]
            time.sleep(1)
            if not BusinessOperation.event_queue.empty():
                data = BusinessOperation.event_queue.get()[event_id]
                # print(data)
                event_status = data['赛事状态']
                if not event_status:
                    event_msg = '该赛事已结束'
                else:
                    if data['体育项目'] == '足球':
                        event_msg = Display._detail_front_football(data)
                    else:
                        event_msg = Display._detail_front_football(data)
                latest_msg[0] = event_msg
                last_msg[0] = event_msg
            if event_status:
                if not BusinessOperation.market_queue.empty():
                    market_msg = ["\033[34m==================== 盘口信息 ==================== \033[0m"]
                    data = BusinessOperation.market_queue.get()

                    data = sorted(data.values(), key=lambda x: x['投注类型'])
                    bet_type_data_dic = {}
                    # 1.分组
                    for market_data in data:
                        if market_data['投注类型名称'] not in bet_type_data_dic:
                            bet_type_data_dic[market_data['投注类型名称']] = [market_data]
                        else:
                            bet_type_data_dic[market_data['投注类型名称']].append(market_data)
                    # 2.按bet_type升序
                    # bet_type_data_list = sorted(list(bet_type_data_dic.values()), key=lambda x: x[0]['投注类型'])
                    # bet_type_data_list = list(bet_type_data_dic.values())

                    # 4.同bet_type，不同bet_type_name，按bet_type和name排序
                    bet_type_data_list = sorted(list(bet_type_data_dic.values()),
                                                key=lambda x: (x[0]['投注类型'], x[0]['盘口ID']))
                    # # 3.同bet_type按market id 升序
                    # for index, value in enumerate(bet_type_data_list):
                    #     bet_type_data_list[index] = sorted(value, key=lambda x: x['盘口ID'])

                    market_msg.append(f"(总盘口数{len(data)},详情总盘口数{len(bet_type_data_dic.keys())},"
                                      f"赛事状态: {event_status})")
                    bd_market_list = [4, 30, 152, 416, 413, 414, 165, 166, 392, 399, 405, 413, 414, 1302, 1317, 3900,
                                      3910, 3917]
                    for bet_type_data in bet_type_data_list:
                        market_msg.append(
                            f'\033[36m---- {bet_type_data[0]["投注类型名称"]} 投注类型:{bet_type_data[0]["投注类型"]} '
                            f'盘口ID:{bet_type_data[0]["盘口ID"]} ----\033[0m')
                        for market in bet_type_data:
                            # 波胆固定显示两列
                            if bet_type_data[0]["投注类型"] in bd_market_list:
                                width = 2
                            else:
                                width = 2 if len(list(filter(lambda x: x['赔率相关信息'] > 0,
                                                             market['盘口赔率项目列表']))) % 2 == 0 else 3
                            if event_status:
                                order = 1
                                market_str = ''
                                # 盘口状态正常
                                if market['盘口状态'] in ('running',) and event_status == 'running':
                                    # 大小让球盘口，需展示球头
                                    if market['投注类型'] in (SbSportEnum.dx_market_list.value +
                                                          SbSportEnum.handicap_market_list.value):
                                        for outcome in market['盘口赔率项目列表']:
                                            odds = outcome['赔率相关信息']
                                            # 赔率为0的不显示
                                            if odds > 0:
                                                # 让球正赔率需在前面添加加号
                                                operate = "+" if market['投注类型'] in \
                                                                 SbSportEnum.handicap_market_list.value and \
                                                                 outcome['球头'] > 0 else ""
                                                # 让球中的和局，不显示球头
                                                if outcome['投注选项'] != 'x':
                                                    outcome_str = f"\033[32m{outcome['投注类型选项名称']}{operate}" \
                                                                  f"{outcome['球头']}  {odds}\033[0m      "
                                                else:
                                                    outcome_str = f"\033[32m{outcome['投注类型选项名称']}  {odds}" \
                                                                  f"\033[0m      "
                                                if order != width:
                                                    market_str += outcome_str
                                                    order += 1
                                                    if outcome == market['盘口赔率项目列表'][-1]:
                                                        market_msg.append(market_str)
                                                else:
                                                    order = 1
                                                    market_str += outcome_str
                                                    market_msg.append(market_str)
                                                    market_str = ''
                                    # 其他盘口
                                    else:

                                        for outcome in market['盘口赔率项目列表']:
                                            odds = outcome['赔率相关信息']
                                            if odds > 0:
                                                outcome_str = f"\033[32m{outcome['投注类型选项名称']}" \
                                                              f"  {odds}\033[0m      "
                                                if order != width:
                                                    order += 1
                                                    market_str += outcome_str
                                                    if outcome == market['盘口赔率项目列表'][-1]:
                                                        market_msg.append(market_str)
                                                else:
                                                    order = 1
                                                    market_str += outcome_str
                                                    market_msg.append(market_str)
                                                    market_str = ''
                                # 盘口状态不正常
                                else:
                                    # 大小让球盘口，需展示球头
                                    if market['投注类型'] in (SbSportEnum.dx_market_list.value +
                                                          SbSportEnum.handicap_market_list.value):
                                        for outcome in market['盘口赔率项目列表']:
                                            odds = outcome['赔率相关信息']
                                            # print(outcome)
                                            if odds > 0:
                                                # print(outcome)
                                                # 让球正赔率需在前面添加加号
                                                operate = "+" if market['投注类型'] in \
                                                                 SbSportEnum.handicap_market_list.value and \
                                                                 outcome['球头'] > 0 else ""
                                                # 让球中的和局，不显示球头
                                                if outcome['投注选项'] != 'x':
                                                    outcome_str = f"\033[32m{outcome['投注类型选项名称']}" \
                                                                  f"{operate}{outcome['球头']}\033[0m 🔒    "
                                                else:
                                                    outcome_str = f"\033[32m{outcome['投注类型选项名称']}\033[0m 🔒    "
                                                if order != width:
                                                    market_str += outcome_str
                                                    order += 1
                                                    if outcome == market['盘口赔率项目列表'][-1]:
                                                        market_msg.append(market_str)
                                                else:
                                                    order = 1
                                                    market_str += outcome_str
                                                    market_msg.append(market_str)
                                                    market_str = ''
                                    else:
                                        for outcome in market['盘口赔率项目列表']:
                                            odds = outcome['赔率相关信息']
                                            if odds > 0:
                                                outcome_str = f"\033[32m{outcome['投注类型选项名称']}" \
                                                              f" 🔒\033[0m      "
                                                if order != width:
                                                    order += 1
                                                    market_str += outcome_str
                                                    if outcome == market['盘口赔率项目列表'][-1]:
                                                        market_msg.append(market_str)
                                                else:
                                                    order = 1
                                                    market_str += outcome_str
                                                    market_msg.append(market_str)
                                                    market_str = ''
                                    # market_msg.append('🔒' + '  🔒'.join(
                                    #     [f"\033[32m{outcome['投注类型选项名称']}[{market['盘口状态']}]\033[0m" for
                                    #      outcome in market['盘口赔率项目列表'] if outcome['赔率相关信息'] > 0]))
                    latest_msg[1] = market_msg
                    last_msg[1] = market_msg

            if latest_msg[0] or latest_msg[1]:
                for index in range(2):
                    if not latest_msg[index]:
                        latest_msg[index] = last_msg[index]
                print('\n')
                print("*" * 100)
                [print(log_sr) for item in latest_msg for log_sr in item]

    # 5.比赛详情页获取联赛下所有比赛列表
    @staticmethod
    def get_event_list_of_league(league_id):
        """
        比赛详情页获取联赛下所有比赛列表
        @param league_id: 联赛id
        @return:
        """
        # print(111)
        filter_dic = {"联赛id": f" eq {league_id}"}
        BusinessOperation.start_stream('events', {'env': 'sit', 'token': sb_token_context.get(),
                                                  "filter_dic": filter_dic, "header": sb_client_header_context.get()})
        # print(222)
        while True:
            time.sleep(0.2)
            if not BusinessOperation.event_queue.empty():
                data = BusinessOperation.event_queue.get().values()
                # 加载比赛详情信息
                event_id_list = [item['赛事ID'] for item in data]
                # 排序
                data = sorted(data, key=lambda x: x["联赛ID"])
                # 联赛列表
                league_list = list(set([item["联赛名称"] for item in data]))
                for index, league in enumerate(league_list):
                    event_list = list(filter(lambda x: x['联赛名称'] == league, data))
                    # print(event_list)
                    print(f"\n\033[31m【  {league} - 赛事数量: {len(event_list)}】\033[0m\n")
                    for event_data in event_list:
                        team_info = event_data['团队相关信息']
                        print(f"{event_data['赛事ID']} \033[32m{team_info['主队名称']}\033[0m   "
                              f"{DateUtil.convert_utc_time_to_local(event_data['开赛时间'])}   "
                              f"\033[32m{team_info['客队名称']}\033[0m")

    # 6.赛果
    @staticmethod
    def get_event_result(sport_name, league_id=None, event_id=None, only_running=False, start_diff=0, end_diff=0):
        fill_len = 30
        data = BusinessOperation.get_event_results(sport_name, league_id, event_id, only_running,
                                                   start_diff=start_diff, end_diff=end_diff)
        # print(data)
        print_list = []
        if sport_name == '足球':
            print_list.append(["日期".ljust(fill_len - 10, ' ')] + [item.ljust(fill_len - 3, ' ') for item in
                                                                  ["联赛", "      赛事", "黄牌", "红牌"]])
            for league_data in data:
                # print(league_data)
                for event_data in league_data['赛事赛果信息列表']:
                    # print(event_data)
                    league_name = league_data['联赛名称']
                    league_name = f'{league_name[:15]}...{league_name[-15:]}' if len(league_name) > 25 else league_name
                    sub_data = [DateUtil.convert_utc_time_to_local(event_data['赛事时间']), league_name,
                                f'  {event_data["主队名称"]} VS {event_data["客队名称"]}']
                    print_list.append([f"{sub_data[0]}  "] + [item.ljust(fill_len, ' ') for item in sub_data[1:]])

        for item in print_list:
            print("".join(item))
        print(f"================  总数：{len(print_list)}  =======================")

    # 7.公告
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
        data = BusinessOperation.get_announcement(sport_name, announcement_type, start_diff, end_diff)
        print(f"【公告总条数： {len(data)}】")
        grep_data_dic = {}
        for item in data:
            name = re.search('^请注意:\[(.+?)\]', item['讯息公告内容']).group(1)
            if name not in grep_data_dic:
                grep_data_dic[name] = [item]
            else:
                grep_data_dic[name].append(item)
        for key, announcement_list in grep_data_dic.items():
            print(f"--------  {key}的公告条数: {len(announcement_list)} --------")
            for announcement in announcement_list:
                print(key)
                print(announcement['讯息公告内容'])
                print(DateUtil.convert_utc_time_to_local(announcement['公告讯息张贴时间'][:-3]))
                print("-" * 25)


if __name__ == '__main__':
    env_context.set('sit')
    BusinessOperation.running_status.set()
    BaseOperation.login_sb('xy2')

    # 首页
    # 1.上方计数:   sport_name, date_type, league_name="", event_id="", start_diff=0, end_diff=6
    # Display.front('今日', start_diff=7, end_diff=7)
    # Display.front('今日')
    # 2.联赛列表  sport_name, date_type, league_name="", event_id="", start_diff=0, end_diff=6
    # Display.get_main_page_league_list('篮球', '滚球')
    # Display.get_main_page_league_list('足球', date_type='滚球', start_diff=0, end_diff=0, ignore_sport_type='否')
    # 3.大厅列表 sport_name, date_type, league_name="", event_id=None, start_diff=0, end_diff=6
    # 大厅列表， 不筛选热门
    # Display.main_page('足球', '滚球')
    # Display.main_page('足球', league_id=95730, start_diff=0, end_diff=1)
    # Display.main_page('足球', '今日', grep_not_live=True)
    # Display.main_page('足球', '滚球', event_id=87362033)
    # Display.main_page('足球', '冠军')
    # 大厅列表， 筛选热门 pc 不区分日期
    # Display.main_page('足球', '早盘', only_hot=True)
    # 大厅列表， 筛选热门 pc外区分日期
    # Display.main_page('足球', '早盘', only_hot=True, start_diff=1, end_diff=1)
    # PC, 今日未开赛
    # Display.main_page('足球', '今日', grep_not_live=True)
    # Display.main_page('篮球', '滚球')
    # Display.main_page('足球', league_id=46859, start_diff=0, end_diff=1)  # 按联赛搜索
    # Display.main_page('足球', event_id=147230, start_diff=0, end_diff=0)  # 按比赛搜索
    # 4.大厅列表 - 冠军
    # Display.main_page_champion('足球')
    # Display.main_page('足球', '滚球', event_id=87219993)
    # 5.比赛详情  event_id
    Display.get_match_detail_page(88125229)
    # 6.比赛详情页获取联赛下所有比赛列表
    # Display.get_event_list_of_league(95731)

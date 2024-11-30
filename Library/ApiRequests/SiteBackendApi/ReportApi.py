#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/11/25 20:12
from os import path
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Dao import Dao
from collections import defaultdict


class ReportApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def get_vip_data_report_api(site_code, day_diff, vip_rank=None, vip_grade=None, check_code=True,
                                site_index='1'):
        """
        VIP数据报表
        :return: order_no
        """
        url = YamlUtil.get_site_host() + '/site/vipData/queryVIPData'
        timezone = Dao.get_site_timezone(site_code)
        start_time, _ = DateUtil.get_timestamp_range(day_diff, day_diff, 0, '日', timezone)
        params = {"startTime": start_time, "vipRankCode": vip_rank, "vipGradeCode": vip_grade, "pageNumber": 1,
                  "pageSize": 200}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            return [{"VIP段位": _["vipRankCodeName"], "VIP等级": _["vipGradeCodeName"],
                     "现有人数": _["currentGradeNum"], "新达成人数": _["achieveGradeNum"],
                     "已领取红利": _["receiveBonus"]} for _ in resp[0]], resp[1]["receiveBonus"]
        else:
            return resp['message']

    @staticmethod
    def get_venue_report_api(site_code, start_diff=0, end_diff=0, currency="", to_site_coin=False,
                             check_code=True, site_index='1'):
        """
        VIP数据报表
        :return: order_no
        """
        url = YamlUtil.get_site_host() + '/site/venue-win-lose-report/api/pageList'
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, 0, '日', timezone)
        params = {"startTime": start_time, "endTime": end_time, "venueCodeList": [], "currency": currency,
                  "convertPlatCurrency": to_site_coin, "pageNumber": 1, "pageSize": 200}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            detail = [{"场馆": _["venueCodeText"], "主币种": _["currency"], "投注人数": _["bettorCount"],
                       "注单量": _["betCount"], "投注金额": _["betAmount"], "有效投注": _["validBetAmount"],
                       "平台输赢": _["winlossAmount"]} for _ in resp[0]]
            total = {"投注人数": resp[1]['bettorCount'], "注单量": resp[1]['betCount'],
                     "投注金额": resp[1]['betAmount'], "有效投注": resp[1]['validBetAmount'],
                     "平台输赢": resp[1]['winlossAmount']}
            return detail, total
        else:
            return resp['message']

    @staticmethod
    def get_daily_report_api(site_code, start_diff=0, end_diff=0, currency="", to_site_coin=False,
                             check_code=True, site_index='1'):
        """
        每日盈亏数据报表
        :return: order_no
        """
        url = YamlUtil.get_site_host() + '/site/win-lose-report/api/dailyWinLosePage'
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, 0, '日', timezone)
        params = {"startDay": start_time, "endDay": end_time, "mainCurrency": currency, "toPlatCurr": to_site_coin,
                  "pageNumber": 1, "pageSize": 200}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            detail = [{"日期": DateUtil.timestamp_to_date(_["dayMillis"], timezone), "主币种": _["mainCurrency"],
                       "VIP福利": _["vipAmount"],
                       "活动优惠": _["activityAmount"], "已使用优惠": _["alreadyUseAmount"], "其他调整": _["adjustAmount"],
                       "投注人数": _["betMemNum"], "注单量": _["betNum"], "投注金额": _["betAmount"],
                       "有效投注": _["validBetAmount"], "会员输赢": _["betWinLose"], "净盈利": _["profitAndLoss"]}
                      for _ in resp[0]]
            total = {"投注人数": resp[1]['betMemNum'], "注单量": resp[1]['betNum'],
                     "投注金额": resp[1]['betAmount'], "有效投注": resp[1]['validBetAmount'],
                     "会员输赢": resp[1]['betWinLose'], "VIP福利": resp[1]['vipAmount'],
                     "活动优惠": resp[1]['activityAmount'], "已使用优惠": resp[1]['alreadyUseAmount'],
                     "其他调整": resp[1]['adjustAmount'], "净盈利": resp[1]['profitAndLoss']}
            return detail, total
        else:
            return resp['message']

    @staticmethod
    def get_user_win_lose_report_api(site_code, start_diff=0, end_diff=0, user_account="", super_agent=None,
                                     account_type=None, order_cnt_min=None, order_cnt_max=None, bet_amount_min=None,
                                     bet_amount_max=None, win_lose_min=None, win_lose_max=None,
                                     sum_win_lose_min=None, sum_win_lose_max=None, currency="", to_site_coin=False,
                                     check_code=True, site_index='1'):
        """
        会员盈亏报表
        :return: order_no
        """
        url = YamlUtil.get_site_host() + '/site/user-win-lose/api/getUserWinLosePage'
        print(url)
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, 0, '日', timezone)
        params = {"startDay": start_time, "endDay": end_time, "userAccount": user_account,
                  "superAgentAccount": super_agent,
                  "accountType": Dao.get_user_account_type()[account_type] if account_type else "",
                  "betNumMin": order_cnt_min, "betNumMax": order_cnt_max,
                  "betAmountMin": bet_amount_min, "betAmountMax": bet_amount_max, "betWinLoseMin": win_lose_min,
                  "betWinLoseMax": win_lose_max, "profitAndLossMin": sum_win_lose_min,
                  "profitAndLossMax": sum_win_lose_max, "mainCurrency": currency, "convertPlatCurrency": to_site_coin,
                  "pageNumber": 1, "pageSize": 200}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            print(resp[0])
            detail = [{"会员账号": _["userAccount"], "账号类型": _["accountTypeText"], "主币种": _["mainCurrency"],
                       "VIP段位": _["vipRankCodeName"], "VIP等级": _["vipGradeCodeName"],
                       "会员标签": _["userLabelId"], "上级代理": _["superAgentAccount"], "注单量": _["betNum"],
                       "投注金额": _["betAmount"], "有效投注": _["validBetAmount"],
                       "会员输赢": _["betWinLose"], "VIP福利": _["vipAmount"], "活动优惠": _["activityAmount"],
                       "已使用优惠": _["alreadyUseAmount"], "其他调整": _["adjustAmount"], "会员净盈利": _["profitAndLoss"]}
                      for _ in resp[0]]
            total = {"注单量": resp[1]["betNum"], "投注金额": resp[1]["betAmount"], "有效投注": resp[1]["validBetAmount"],
                     "会员输赢": resp[1]["betWinLose"], "VIP福利": resp[1]["vipAmount"],
                     "活动优惠": resp[1]["activityAmount"],
                     "已使用优惠": resp[1]["alreadyUseAmount"], "其他调整": resp[1]["adjustAmount"],
                     "会员净盈利": resp[1]["profitAndLoss"]}
            return detail, total
        else:
            return resp['message']

    @staticmethod
    def get_game_report_api(site_code, start_diff=0, end_diff=0, currency="", venue_type=None, to_site_coin=False,
                            check_code=True, site_index='1'):
        """
        游戏报表
        :return: order_no
        """
        venue_type_dic = Dao.get_venue_type()
        url = YamlUtil.get_site_host() + '/site/site-integrate/api/site/pageList'
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, 0, '日', timezone)
        params = {"startTime": start_time, "endTime": end_time, "currency": currency, "platCurrency": "",
                  "venueType": venue_type_dic[venue_type] if venue_type else "", "convertPlatCurrency": to_site_coin,
                  "pageNumber": 1, "pageSize": 200}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            detail = [{"游戏类型": _["venueTypeText"], "币种": _["currency"],
                       "投注人数": _["bettorNum"], "投注量": _["betNum"], "投注金额": _["betAmount"],
                       "有效投注": _["validBetAmount"], "平台输赢": _["winLoseAmount"]}
                      for _ in resp[0]]
            return detail
        else:
            return resp['message']

    # @staticmethod
    # def get_game_report_api(site_code, start_diff=0, end_diff=0, currency="", venue_type=None, to_site_coin=False,
    #                         check_code=True, site_index='1'):
    #     """
    #     游戏报表
    #     :return: order_no
    #     """
    #     venue_type_dic = Dao.get_venue_type()
    #     url = YamlUtil.get_site_host() + '/site/site-integrate/api/site/pageList'
    #     timezone = Dao.get_site_timezone(site_code)
    #     start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, 0, '日', timezone)
    #     params = {"startTime": start_time, "endTime": end_time, "currency": currency, "platCurrency": "",
    #               "venueType": venue_type_dic[venue_type] if venue_type else "", "convertPlatCurrency": to_site_coin,
    #               "pageNumber": 1, "pageSize": 200}
    #     resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
    #                                 return_total=True)
    #
    #     if check_code:
    #         detail = [{"游戏类型": _["venueTypeText"], "币种": _["currency"],
    #                    "投注人数": _["bettorNum"], "投注量": _["betNum"], "投注金额": _["betAmount"],
    #                    "有效投注": _["validBetAmount"], "平台输赢": _["winLoseAmount"]}
    #                   for _ in resp[0]]
    #         return detail
    #     else:
    #         return resp['message']

    @staticmethod
    def get_task_report_api(site_code, start_diff=0, end_diff=0, task_id="", task_type="", task_name="",
                            stop_diff=0, date_type='日', check_code=True, site_index='1'):
        """
        任务数据报表
        @return:
        """
        task_type_dic = Dao.get_task_type()
        url = YamlUtil.get_site_host() + '/site/report-task-order/api/getReportTaskOrderPage'
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        params = {"startTime": start_time, "endTme": end_time, "taskName": task_name, "taskId": task_id,
                  "taskType": task_type_dic[task_type] if task_type else "", "pageNumber": 1, "pageSize": 200}
        resp = HttpRequestUtil.post(url, params, all_page=True, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            detail = [{"统计日期": _["staticDate"], "任务ID": _["taskId"], "任务名称": _['subTaskTypeText'],
                       "任务类型": _['taskTypeText'], "发放人数": _["allCount"], "发放彩金金额": _["sendAmount"],
                       "已领取人数": _["receiveCount"], "已领取彩金金额": _["receiveAmount"]} for _ in resp[0]]
            total = {"发放人数": resp[1]['allCount'], "发放彩金金额": resp[1]['sendAmount'],
                     "已领取人数": resp[1]['receiveCount'], "已领取彩金金额": resp[1]['receiveAmount']}
            return detail, total
        else:
            return resp['message']

    @staticmethod
    def get_user_report_api(site_code, start_diff=0, end_diff=0, register_start_diff=None, register_end_diff=None,
                            user_account=None, agent_account=None, account_type="正式", order_quantity_min=None,
                            order_quantity_max=None, bet_amount_min=None, bet_amount_max=None, valid_amount_min=None,
                            valid_amount_max=None, win_lose_amount_min=None, win_lose_amount_max=None,
                            deposit_amount_min=None, deposit_amount_max=None, withdraw_amount_min=None,
                            withdraw_amount_max=None, currency=None, stop_diff=None, to_site_coin=False,
                            date_type='日', check_code=True, site_index='1'):
        url = YamlUtil.get_site_host() + '/site/report-userInfo-statement/api/pageList'
        timezone = Dao.get_site_timezone(site_code)

        params = {"pageNumber": 1, "pageSize": 200}
        if start_diff or start_diff != 0:
            start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
            params["statisticalDateStart"] = start_time
            params["statisticalDateEnd"] = end_time
        if type(register_start_diff) == int:
            start_time, end_time = DateUtil.get_timestamp_range(register_start_diff, register_end_diff, stop_diff,
                                                                date_type, timezone)
            params["registerTimeStart"] = start_time
            params["registerTimeEnd"] = end_time
        if user_account:
            params["userAccount"] = user_account
        if agent_account:
            params["superAgentAccount"] = agent_account
        if account_type:
            params["accountType"] = Dao.get_user_account_type(account_type)
        if type(order_quantity_min) == int:
            params["betMin"] = order_quantity_min
            params["betMax"] = order_quantity_max
        if type(bet_amount_min) == int:
            params["betAmountMin"] = bet_amount_min
            params["betAmountMax"] = bet_amount_max
        if type(valid_amount_min) == int:
            params["activeBetMin"] = valid_amount_min
            params["activeBetMax"] = valid_amount_max
        if type(win_lose_amount_min) == int:
            params["bettingProfitLossMin"] = win_lose_amount_min
            params["bettingProfitLossMax"] = win_lose_amount_max
        if type(deposit_amount_min) == int:
            params["totalDepositMin"] = deposit_amount_min
            params["totalDepositMax"] = deposit_amount_max
        if type(withdraw_amount_min) == int:
            params["totalWithdrawalMin"] = withdraw_amount_min
            params["totalWithdrawalMax"] = withdraw_amount_max
        if currency:
            params["mainCurrency"] = currency
        if to_site_coin:
            params["convertPlatCurrency"] = to_site_coin

        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            detail = [{"会员账号": _["userAccount"], "账号类型": _["accountTypeText"], "主币种": _['mainCurrency'],
                       "VIP段位": _['vipRankCodeName'], "VIP等级": _["vipGradeCodeName"], "会员标签": _["userLabelId"],
                       "上级代理": _["superAgentAccount"], "转代次数": _['transAgentTime'],
                       "注册时间": _['registerTimeStr'], "首存金额": _["firstDepositAmount"],
                       "总存款": _["totalDeposit"], "存款次数": _["numberDeposit"], "上级转入": _["advancedTransfer"],
                       "转入次数": _["numberTransfer"], "总取款": _["totalWithdrawal"], "取款次数": _["numberWithdrawal"],
                       "大额取款次数": _["numberLargeWithdrawal"], "存取差": _["poorAccess"], "VIP福利": _["vipAmount"],
                       "活动优惠": _["activityAmount"], "已使用优惠": _["alreadyUseAmount"],
                       "其他调整": _["otherAdjustments"], "注单量": _["placeOrderQuantity"], "投注金额": _["betAmount"],
                       "有效投注": _["activeBet"], "会员输赢": _["bettingProfitLoss"],
                       "会员净盈利": _["totalPreference"]} for _ in resp["data"]["reportUserInfoStatementVOList"][
                          "records"]]
            total_data = resp["data"]["totalPage"]
            if total_data:
                total = {"首存金额": total_data['firstDepositAmount'], "总存款": total_data['totalDeposit'],
                         "存款次数": total_data['numberDeposit'], "上级转入": total_data['advancedTransfer'],
                         "转入次数": total_data['numberTransfer'], "总取款": total_data['totalWithdrawal'],
                         "取款次数": total_data['numberWithdrawal'], "大额取款次数": total_data['numberLargeWithdrawal'],
                         "存取差": total_data['poorAccess'], "VIP福利": total_data['vipAmount'],
                         "活动优惠": total_data['activityAmount'], "已使用优惠": total_data['alreadyUseAmount'],
                         "其他调整": total_data['otherAdjustments'], "注单量": total_data['placeOrderQuantity'],
                         "投注金额": total_data['betAmount'], "有效投注": total_data['activeBet'],
                         "会员输赢": total_data['bettingProfitLoss'], "会员净盈利": total_data['totalPreference']}
            else:
                total = {}
            return detail, total
        else:
            return resp['message']

    @staticmethod
    def get_comprehensive_report_api(site_code, start_diff=0, end_diff=0, stop_diff=0, date_type='月',
                                     currency=None, to_site_coin=False, check_code=True, site_index='1'):
        """
        获取综合报表
        @return:
        """
        url = YamlUtil.get_site_host() + '/site/site-integrate/api/getSiteIntegrateDataReportPage'
        timezone = Dao.get_site_timezone(site_code)

        start_time, end_time = DateUtil.get_timestamp_range(start_diff, end_diff, stop_diff, date_type, timezone)
        params = {"beginTime": start_time, "endTime": end_time, "currencyCode": currency, "toPlatCurr": to_site_coin,
                  "pageNumber": 1, "pageSize": 200}

        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index,
                                    return_total=True)

        if check_code:
            detail = [{"日期": _["staticDate"], "币种": _["currencyCode"],
                       "会员注册人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                           "IOS_APP", "IOS_H5"],
                                          [_["memberRegister"][k] for k in ("total", "backed", "pc", "androidAPP",
                                                                            "androidH5", "iosAPP", "iosH5")])),
                       "会员登录人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                           "IOS_APP", "IOS_H5"],
                                          [_["memberLogin"][k] for k in ("total", "backed", "pc", "androidAPP",
                                                                         "androidH5", "iosAPP", "iosH5")])),
                       "会员总存款": {"总额": _["memberTotalDeposit"]["totalDeposit"],
                                 "存款人数": _["memberTotalDeposit"]["depositPeopleNums"],
                                 "存款次数": _["memberTotalDeposit"]["depositNums"]},
                       "会员总取款": {"总额": _["memberTotalWithdraw"]["totalWithdraw"],
                                 "取款人数": _["memberTotalWithdraw"]["withdrawPeopleNums"],
                                 "取款次数": _["memberTotalWithdraw"]["withdrawNums"],
                                 "大额取款人数": _["memberTotalWithdraw"]["largeWithdrawPeopleNums"],
                                 "大额取款次数": _["memberTotalWithdraw"]["largeWithdrawNums"]},
                       "会员存取差": _["memberAccessDifference"],
                       "会员首存": {"总额": _["memberFirstDeposit"]["amount"],
                                "首存人数": _["memberFirstDeposit"]["peopleNums"]},
                       "会员投注": dict(zip(["投注金额", "有效投注", "投注人数", "注单量"],
                                        [_["memberBetInfo"][k] for k in ("betAmount", "effectiveBetAmount",
                                                                         "bettorNums", "bettingOrderAmount")])),
                       "会员输赢": _["memberWinOrLose"],
                       "会员VIP福利": {"总额": _["vipWelfare"]["amount"], "人数": _["vipWelfare"]["peopleNums"]},
                       "会员活动优惠": {"总额": _["memberPromotion"]["amount"], "人数": _["vipWelfare"]["peopleNums"]},
                       "已使用优惠": _["usedPromotion"],
                       "会员调整": dict(zip(["总额", "加额", "加额人数", "减额", "减额人数"],
                                        [_["memberAdjustment"][k] for k in ["totalAdjust", "addAmount",
                                                                            "addAmountPeopleNum", "reduceAmount",
                                                                            "reducePeopleNums"]])),
                       "代理下注册人数": dict(
                           zip(["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP",
                                "IOS_H5"],
                               [_["agentRegister"][k] for k in ("total", "backed", "pc", "androidAPP",
                                                                "androidH5", "iosAPP", "iosH5")])),
                       "代存会员": {"人数": _["agentDepositInfo"]["credit"], "次数": _["agentDepositInfo"]["creditTimes"],
                                "额度": _["agentDepositInfo"]["creditPeopleNums"]}
                       } for _ in resp["data"]["integrateDataReportRspVOPage"]["records"]]
            _ = resp["data"]["allDataRespVO"]
            total = {"会员注册人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                         "IOS_APP", "IOS_H5"],
                                        [_["memberRegister"][k] for k in ("total", "backed", "pc", "androidAPP",
                                                                          "androidH5", "iosAPP", "iosH5")])),
                     "会员登录人数": dict(zip(["总数", "后台", "PC", "Android_APP", "Android_H5",
                                         "IOS_APP", "IOS_H5"],
                                        [_["memberLogin"][k] for k in ("total", "backed", "pc", "androidAPP",
                                                                       "androidH5", "iosAPP", "iosH5")])),
                     "会员总存款": {"总额": _["memberTotalDeposit"]["totalDeposit"],
                               "存款人数": _["memberTotalDeposit"]["depositPeopleNums"],
                               "存款次数": _["memberTotalDeposit"]["depositNums"]},
                     "会员总取款": {"总额": _["memberTotalWithdraw"]["totalWithdraw"],
                               "取款人数": _["memberTotalWithdraw"]["withdrawPeopleNums"],
                               "取款次数": _["memberTotalWithdraw"]["withdrawNums"],
                               "大额取款人数": _["memberTotalWithdraw"]["largeWithdrawPeopleNums"],
                               "大额取款次数": _["memberTotalWithdraw"]["largeWithdrawNums"]},
                     "会员存取差": _["memberAccessDifference"],
                     "会员首存": {"总额": _["memberFirstDeposit"]["amount"],
                              "首存人数": _["memberFirstDeposit"]["peopleNums"]},
                     "会员投注": dict(zip(["投注金额", "有效投注", "投注人数", "注单量"],
                                      [_["memberBetInfo"][k] for k in ("betAmount", "effectiveBetAmount",
                                                                       "bettorNums", "bettingOrderAmount")])),
                     "会员输赢": _["memberWinOrLose"],
                     "会员VIP福利": {"总额": _["vipWelfare"]["amount"], "人数": _["vipWelfare"]["peopleNums"]},
                     "会员活动优惠": {"总额": _["memberPromotion"]["amount"], "人数": _["vipWelfare"]["peopleNums"]},
                     "已使用优惠": _["usedPromotion"],
                     "会员调整": dict(zip(["总额", "加额", "加额人数", "减额", "减额人数"],
                                      [_["memberAdjustment"][k] for k in ["totalAdjust", "addAmount",
                                                                          "addAmountPeopleNum", "reduceAmount",
                                                                          "reducePeopleNums"]])),
                     "代理下注册人数": dict(
                         zip(["总数", "后台", "PC", "Android_APP", "Android_H5", "IOS_APP",
                              "IOS_H5"],
                             [_["agentRegister"][k] for k in ("total", "backed", "pc", "androidAPP",
                                                              "androidH5", "iosAPP", "iosH5")])),
                     "代存会员": {"人数": _["agentDepositInfo"]["credit"], "次数": _["agentDepositInfo"]["creditTimes"],
                              "额度": _["agentDepositInfo"]["creditPeopleNums"]}}
            return detail, total
        else:
            return resp['message']

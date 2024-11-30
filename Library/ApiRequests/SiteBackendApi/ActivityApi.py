#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/2 22:53
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.ApiRequests.CommonFunc import CommonFunc
from Library.Dao import Dao
from Library.Dao.Mysql.ChainQery.System import System
from Library.MysqlTableModel.site_activity_labs_model import SiteActivityLab
from Library.MysqlTableModel.site_activity_base_model import SiteActivityBase


class ActivityApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def _create_activity_param_base(site_code, activity_name, time_range_type, activity_type,
                                    activity_start_diff, activity_end_diff, display_start_diff, display_end_diff,
                                    flow_rate, label_name="", support_terminal='',
                                    enable_account_type='正式', date_type='秒', stop_diff=0):
        if not support_terminal:
            support_terminal = 'PC,IOS_H5,IOS_APP,Android_H5,Android_APP'
        timezone = Dao.get_site_timezone(site_code)
        img = CommonFunc.upload_file_api()
        print("a1")
        label_info: SiteActivityLab = Dao.get_activity_label_list_dao(site_code, label_name, status='开启中')[0][0]
        start_time, end_time = DateUtil.get_timestamp_range(activity_start_diff, activity_end_diff,
                                                            date_type=date_type, stop_diff=stop_diff, timezone=timezone)
        show_start_time, show_end_time = DateUtil.get_timestamp_range(display_start_diff, display_end_diff,
                                                                      date_type=date_type, stop_diff=stop_diff,
                                                                      timezone=timezone)
        print("a2")
        terminal_dic = System.get_user_register_client()
        language_dic = Dao.get_site_language_dao(site_code)
        param = {
            "id": "",  # 新增传空，编辑传值
            "activityNameI18nCodeList": [{"message": activity_name, "language": code} for code in
                                         language_dic.values()],
            "labelId": label_info.id,
            "activityDeadline": System.get_activity_prescription_type(time_range_type),
            "activityStartTime": start_time,
            "activityEndTime": end_time,
            "showStartTime": show_start_time,
            "showEndTime": show_end_time,
            "activityTemplate": System.get_activity_template(activity_type),
            "washRatio": flow_rate,
            "accountType": System.get_user_account_type(enable_account_type),
            "showTerminal": ",".join([str(terminal_dic[_]) for _ in support_terminal.split(",")]),
            "entrancePictureI18nCodeList": [{"message": img, "language": code} for code in language_dic.values()],
            "entrancePicturePcI18nCodeList": [{"message": img, "language": code} for code in language_dic.values()],
            "headPictureI18nCodeList": [{"message": img, "language": code} for code in language_dic.values()],
            "headPicturePcI18nCodeList": [{"message": img, "language": code} for code in language_dic.values()],
            "activityRuleI18nCodeList": [{"message": "string", "language": "string"}],
            "activityDescI18nCodeList": [{"message": "string", "language": "string"}],
        }
        return param

    @staticmethod
    def create_first_deposit_activity_api(site_code, activity_name, activity_start_diff, activity_end_diff,
                                          display_start_diff, display_end_diff, time_range_type='限时活动', label_name="",
                                          flow_rate=1, discount_type='固定金额', min_deposit=1,
                                          discount_percent=2, daily_max=100000, discount_range_list=None,
                                          participation_type='自动参与',
                                          distribution_type='立即派发', eligibility_type='同登录IP只能1次',
                                          describe="test describe",
                                          support_terminal='PC,IOS_H5,IOS_APP,Android_H5,Android_APP',
                                          enable_account_type='正式', date_type='秒', stop_diff=0,
                                          check_code=True, site_index='1'):
        """
        创建首存活动
        :param activityEligibility: 参与资格   同登录IP只能1次| 完成邮箱绑定才能参与 | 完成手机号绑定才能参与
        :param distribution_type: 派发方式
        :param flow_rate: 流水倍数
        :param discount_range_list: 固定金额需要传此项，列表 [赠送金额-存款最小值-存款最大值,...]
        :param support_terminal: PC | IOS_H5 | IOS_APP | Android_H5 | Android_APP
        @return:
        """
        language_dic = Dao.get_site_language_dao(site_code)
        eligibility_dic = Dao.get_activity_eligibility()
        url = YamlUtil.get_site_host() + '/site/activity/api/save'
        print(22222)
        params = ActivityApi._create_activity_param_base(site_code, activity_name, time_range_type, "首次充值",
                                                         activity_start_diff, activity_end_diff, display_start_diff,
                                                         display_end_diff, flow_rate, label_name, support_terminal,
                                                         enable_account_type, date_type, stop_diff)
        params["discountType"] = System.get_activity_discount_type(discount_type)
        print("111111")
        if discount_type == '百分比':
            params["percentageVO"] = {"minDeposit": min_deposit, "discountPct": discount_percent,
                                      "maxDailyBonus": daily_max}
        else:
            params["fixedAmountVOS"] = []
            for item in discount_range_list:
                _ = item.split("-")
                if item != discount_range_list[-1]:
                    params["fixedAmountVOS"].append(dict([("minDeposit", _[1]), ("maxDeposit", _[2]),
                                                         ("bonusAmount", _[0])]))
                else:
                    params["fixedAmountVOS"].append(dict([("minDeposit", _[1]), ("bonusAmount", _[0])]))
        print(3333)
        params["participationMode"] = System.get_activity_participation_type(participation_type)
        params['distributionType'] = System.get_activity_distribution_type(distribution_type)
        params['activityRuleI18nCodeList'] = [{"message": f'<p>{describe}</p>', "language": code} for code in
                                              language_dic.values()]
        params['activityEligibility'] = [eligibility_dic[_] for _ in eligibility_type.split(",")] if \
            eligibility_type else []
        params = {"id": "", "activityTemplate": System.get_activity_template("首次充值"),
                  "activityFirstRechargeVO": params}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def set_activity_status(site_code, activity_type, status, activity_name="", check_code=True, site_index='1'):
        """
        设置活动状态
        @param site_code:
        @param activity_type: 模版名称: 首次充值｜二次充值｜免费旋转｜指定日期存款｜体育负盈利｜每日竞赛｜转盘｜红包雨
        @param activity_name: 未指明活动名称，则指定改模版第一个活动
        @param status: 启用 ｜ 禁用
        @param check_code:
        @param site_index:
        @return:
        """
        url = YamlUtil.get_site_host() + "/site/activity/api/operateStatus"
        if not activity_name:
            data = Dao.get_activity_list_dao(site_code, activity_name, activity_type)
            if not data:
                return
            activity_info: SiteActivityBase = data[0]
        else:
            activity_info: SiteActivityBase = Dao.get_activity_list_dao(site_code, activity_name, activity_type)[0]
        print("--------")
        print(dir(activity_info))
        params = {"id": activity_info.id, "status": System.get_enable_status(status)}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

    @staticmethod
    def delete_activity(site_code, activity_name, check_code=True, site_index='1'):
        """
        删除活动
        @return:
        """
        activity_info: SiteActivityBase = Dao.get_activity_list_dao(site_code, activity_name=activity_name)[0]
        url = YamlUtil.get_site_host() + "/site/activity/api/delete"
        params = {"id": activity_info.id, "status": 0}
        resp = HttpRequestUtil.post(url, params, check_code=check_code, site_index=site_index)
        return resp['message']

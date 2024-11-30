#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/10/23 15:03
# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/28 11:35
from collections import defaultdict
from Library.Common.Utils.Contexts import *
from Library.MysqlTableModel.site_vip_change_record_model import SiteVipChangeRecord
from Library.MysqlTableModel.site_vip_grade_model import SiteVipGrade
from Library.MysqlTableModel.site_vip_rank_model import SiteVipRank

from Library.Dao import Dao
from sqlalchemy.sql.functions import func
from Library.Common.Utils.DateUtil import DateUtil


class VipDataReport(object):
    """
    VIP数据报表
    """

    @staticmethod
    def get_vip_data_report_vo(site_code, day_diff=0, vip_rank=None, vip_grade_name=None, date_type='日',
                               stop_diff=0):
        """
        获取VIP数据报表
        :param account_type: 正式 ｜ 测试
        :param sort_by: 首存金额 ｜ 总存款 ｜ 存款次数 ｜ 上级转入 ｜ 转入次数 ｜ 总取款 ｜ 取款次数 ｜ 大额取款次数
        @return:
        """
        timezone = Dao.get_site_timezone(site_code)
        start_time, end_time = DateUtil.get_timestamp_range(day_diff, day_diff, stop_diff, date_type, timezone)
        # vip 等级配置
        grade_data = ms_context.get().session.query(SiteVipGrade.vip_grade_code, SiteVipGrade.vip_grade_name,
                                                    SiteVipRank.vip_rank_name).\
            join(SiteVipRank, SiteVipGrade.vip_rank_code == SiteVipRank.vip_rank_code).\
            filter(SiteVipGrade.site_code == site_code).all()
        grade_dic = {_[0]: _ for _ in grade_data}
        data_1 = ms_context.get().session.query(func.sum(func.if_(SiteVipChangeRecord.after_change != None, 1, 0)).
                                                label('new_cnt'), SiteVipChangeRecord.after_change). \
            filter(SiteVipChangeRecord.site_code == site_code,
                   SiteVipChangeRecord.change_time.between(start_time, end_time)).\
            group_by(SiteVipChangeRecord.after_change).all()
        # 当前存量
        data_2 = Dao.get_user_info_sql(site_code=site_code)
        data_2_1 = defaultdict(int)
        for _ in data_2:
            data_2_1[_[0].vip_grade_code] += 1
        # 已领取红利
        data_3 = Dao.get_vip_award_record_base(site_code, receive_start_diff=day_diff, receive_end_diff=day_diff,
                                               stop_diff=stop_diff, date_type=date_type).subquery()
        data_3 = ms_context.get().session.query(data_3.c.vip_grade_code, data_3.c.currency,
                                                func.sum(data_3.c.award_amount)). \
            group_by(data_3.c.vip_grade_code, data_3.c.currency).all()
        # 转平台币
        currency_rate = Dao.currency_rate(site_code)
        result_dic = defaultdict(lambda: {"VIP段位": None, "VIP等级": None, "现有人数": 0, "新达成人数": 0,
                                          "已领取红利": 0})
        for _ in data_1:
            grade_id = int(_[1])
            result_dic[grade_id]["新达成人数"] = _[0]
            result_dic[grade_id]["VIP段位"] = grade_dic[int(_[1])][2]
            result_dic[grade_id]["VIP等级"] = grade_dic[int(_[1])][1]
        for key, value in data_2_1.items():
            result_dic[key]["现有人数"] = data_2_1[key]
            result_dic[key]["VIP段位"] = grade_dic[int(key)][2]
            result_dic[key]["VIP等级"] = grade_dic[int(key)][1]
        for _ in data_3:
            result_dic[_[0]]["已领取红利"] += _[2] / currency_rate[_[1]] if _[1] != 'WTC' else _[2]
            result_dic[_[0]]["VIP段位"] = grade_dic[int(_[0])][2]
            result_dic[_[0]]["VIP等级"] = grade_dic[int(_[0])][1]

        result_data = list(result_dic.values())
        if vip_rank:
            result_data = list(filter(lambda _: _["VIP段位"] == vip_rank, result_data))
        if vip_grade_name:
            result_data = list(filter(lambda _: _["VIP等级"] == vip_grade_name, result_data))
        # result_data = list(filter(lambda _: _["新达成人数"] > 0 or _["已领取红利"] > 0, result_data))
        return result_data, sum([_['已领取红利'] for _ in result_data])

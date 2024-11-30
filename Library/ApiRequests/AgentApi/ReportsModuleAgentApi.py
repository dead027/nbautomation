#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/1/25 11:47
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil


class ReportsModuleAgentApi(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    agent_host = YamlUtil.get_agent_host()

    @classmethod
    def get_total_commission_agent_api(cls, date_diff=0, date_type='月', stop_diff=0):
        """
        首页-佣金总览
        :param date_diff:
        :param date_type:
        :param stop_diff:
        :return:
        """
        start_timestamp, _ = DateUtil.get_timestamp_range(date_diff, date_diff, stop_diff, date_type)
        url = cls.agent_host + "/api/admin-agent/client-commission/api/getTotalCommission"
        json = {"reportDay": start_timestamp}
        rtn = HttpRequestUtil.post(url, json)["data"]
        data = [rtn[key] for key in ["userWinLoss", "agentWinLoss", "rebateAmount", "agentRate", "activeValidNumber",
                                     "activeNumber", "newActiveNumber", "discountAmount", "adjustCommission",
                                     "venueFee", "commissionAmount", "feeAmount", "lastMonthRemain",
                                     "currentMonthRemain"]]
        return dict(zip(["总输赢", "净输赢", "返水", "佣金比例", "有效活跃用户", "活跃用户", "有效新增", "红利", "调整",
                         "平台费", "佣金", "存取手续费", "上月结余", "本月结余"], data))


if __name__ == '__main__':
    pass

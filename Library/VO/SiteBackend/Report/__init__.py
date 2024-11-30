#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/8/28 16:30

from Library.VO.SiteBackend.Report.UserIoReport import UserIoReport
from Library.VO.SiteBackend.Report.UserReport import UserReport
from Library.VO.SiteBackend.Report.GameReport import GameReport
from Library.VO.SiteBackend.Report.VenueWinLoseReport import VenueWinLoseReport
from Library.VO.SiteBackend.Report.DailyWinLoseReport import DailyWinLoseReport
from Library.VO.SiteBackend.Report.UserWinLoseReport import UserWinLoseReport
from Library.VO.SiteBackend.Report.ActReport import ActReport
from Library.VO.SiteBackend.Report.VipDataReport import VipDataReport
from Library.VO.SiteBackend.Report.TaskReport import TaskReport
from Library.VO.SiteBackend.Report.CommissionReport import CommissionReport
from Library.VO.SiteBackend.Report.ComprehensiveReport import ComprehensiveReport


class Report(UserIoReport, UserReport, GameReport, VenueWinLoseReport, DailyWinLoseReport, UserWinLoseReport,
             ActReport, VipDataReport, TaskReport, CommissionReport, ComprehensiveReport):
    def __init__(self):
        super().__init__()

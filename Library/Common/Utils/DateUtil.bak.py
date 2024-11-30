#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/7 22:22
import datetime
import arrow
import calendar
import time


class DateUtil(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def get_month_day_num(diff=0):
        now = DateUtil.get_current_time("shanghai")
        now = now.shift(days=int(diff))
        days = calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1]
        return days

    def get_md_month_day_num(self, diff=0):
        now = self.get_current_time("shanghai")
        diff = self.get_md_diff_unit(diff)
        now = now.shift(days=int(diff))
        days = calendar.monthrange(int(now.strftime("%Y")), int(now.strftime("%m")))[1]
        return days

    def get_md_diff_unit(self, diff_unit=0):
        """
        获取美东日期偏移值
        :return:
        """
        now = self.get_current_time("shanghai")
        now_time = now.strftime("%H")
        if int(now_time) < 13:
            diff_unit -= 1
        return diff_unit

    @staticmethod
    def _get_relative_time(day=0, hour=0, minute=0, second=0, now=""):
        """
        获取相对日期
        :param now: 指定时间则以指定的时间为准，否则以当前时间
        :param day: 之后传正值，之前传负值
        :param hour: 之后传正值，之前传负值
        :param minute: 之后传正值，之前传负值
        :param second: 之后传正值，之前传负值
        :return:
        """
        now = now if now else datetime.datetime.now()
        now = now + datetime.timedelta(days=float(day), hours=float(hour), minutes=float(minute), seconds=float(second))
        return now.strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def get_current_time(timezone="shanghai"):
        """
        根据时区返回当前时间
        :param timezone: (default)shanghai|UTC|md
        :return:
        """
        if timezone.lower() == "utc":
            now = arrow.utcnow()
        elif timezone.lower() == "md":
            now = arrow.now("GMT-5")
        else:
            now = arrow.now("Asia/Shanghai")
        return now

    @staticmethod
    def get_timestamp_by_now(diff=-1, timezone="md"):
        """
        获取当前日期前的时间，不包含小时分钟秒
        :param diff:之后传正值，之前传负值
        :param timezone: shanghai|UTC(default)|md
        :return:
        """
        now = DateUtil.get_current_time(timezone).shift(days=int(diff))
        return now.timestamp() * 1000

    @staticmethod
    def get_date_by_now(date_type="日", diff=-1, timezone="md"):
        """
        获取当前日期前的时间，不包含小时分钟秒
        :param date_type: 年|月|日，默认为日
        :param diff:之后传正值，之前传负值
        :param timezone: shanghai|UTC(default)|md
        :return:
        """
        now = DateUtil.get_current_time(timezone)
        if date_type == '秒':
            return now.shift(days=int(diff)).strftime("%Y-%m-%d %H:%M:%S")
        elif date_type in ("日", "今日"):
            return now.shift(days=int(diff)).strftime("%Y-%m-%d")
        elif date_type in ("月", "本月"):
            return now.shift(months=int(diff)).strftime("%Y-%m")
        elif date_type == "年":
            return now.shift(years=int(diff)).strftime("%Y")
        else:
            raise AssertionError("类型只能为年月日，实际传参为： %s" % date_type)

    @staticmethod
    def get_sb_search_time(diff=-1, date_type="秒", is_end=False):
        """
        获取沙巴体育的查询时间字符串 美东时区
        :param date_type: 年|月|日，默认为日
        :param diff:之后传正值，之前传负值
        :param is_end:是否是一天的最后
        :return:
        """
        now = DateUtil.get_current_time('md')
        if date_type == '秒':
            if is_end:
                return now.shift(days=int(diff)).replace(hour=23, minute=59, second=59).strftime(
                    "%Y-%m-%dT%H:%M:%S")
            else:
                return now.shift(days=int(diff)).replace(hour=0, minute=0, second=0).strftime(
                    "%Y-%m-%dT%H:%M:%S")
        elif date_type == '日':
            return now.shift(days=int(diff)).strftime("%Y-%m-%d")

    @staticmethod
    def get_utc_search_time(diff=-1, is_end=False, rtn_type='秒'):
        """
        获取沙巴体育的查询时间字符串   基础时区是美东，此处转为utc
        :param diff:之后传正值，之前传负值
        :param is_end:是否是一天的最后
        :param rtn_type: 返回数据类型  秒 ｜ 日
        :return:
        """
        now = DateUtil.get_current_time('md')
        str_format = "%Y-%m-%dT%H:%M:%S" if rtn_type == '秒' else "%Y-%m-%d"
        if is_end:
            return now.shift(days=int(diff)).replace(hour=23, minute=59, second=59).shift(hours=5).strftime(str_format)
        else:
            return now.shift(days=int(diff)).replace(hour=0, minute=0, second=0).shift(hours=5).strftime(str_format)

    @staticmethod
    def convert_utc_time_to_md(utc_time):
        """
        utc时间转美东时间
        :param utc_time
        :return:
        """
        return arrow.get(utc_time, 'YYYY-MM-DDTHH:mm:ss').shift(hours=-5).strftime("%Y-%m-%dT%H:%M:%S")

    @staticmethod
    def get_day_range(date_type="月", diff=0, stop_diff=None, timezone="shanghai"):
        """
        获取年、月的起始和结束日期，不含小时分钟秒
        :param date_type: 年|月|周|日，默认为月
        :param diff:之后传正值，之前传负值
        :param stop_diff: 月，今天的前几天
        :param timezone: (default)shanghai|UTC
        :return: 该月起始及最后一天
        """
        now = DateUtil.get_current_time(timezone)
        if date_type == "月":
            new_date = now.shift(months=int(diff))
            month = new_date.month
            year = new_date.year
            if diff == 0 and stop_diff is not None:
                max_day = int(now.shift(days=int(diff)).strftime("%d")) + int(stop_diff)
            else:
                max_day = calendar.monthrange(year, month)[1]
            start = new_date.replace(day=1).strftime("%Y-%m-%d")
            end = new_date.replace(day=max_day).strftime("%Y-%m-%d")
        elif date_type == "周":
            new_date = now.shift(weeks=int(diff))
            start = new_date - datetime.timedelta(days=new_date.weekday())
            start = start.strftime("%Y-%m-%d")
            end = new_date + datetime.timedelta(days=6 - new_date.weekday())
            end = end.strftime("%Y-%m-%d")
        elif date_type == "年":
            new_date = now.shift(years=int(diff))
            year = new_date.year
            start = new_date.replace(year=year, month=1, day=1).strftime("%Y-%m-%d")
            end = new_date.replace(year=year, month=12, day=31).strftime("%Y-%m-%d")
        elif date_type == "日":
            new_date = now.shift(days=int(diff))
            start = new_date.strftime("%Y-%m-%d")
            end = new_date.strftime("%Y-%m-%d")
        else:
            raise AssertionError("类型只能为年月，实际传参为： %s" % date_type)
        return start, end

    def get_md_day_range(self, date_type="月", diff=-1, timezone="shanghai"):
        """
        获取美东时区的年、月的起始和结束日期，不含小时分钟秒
        :param date_type: 年|月|周，默认为月
        :param diff:之后传正值，之前传负值
        :param timezone: (default)shanghai|UTC
        :return: 该月起始及最后一天
        """
        diff = self.get_md_diff_unit(diff)
        now = self.get_current_time(timezone)
        new_date = now.shift(days=int(diff))
        if date_type == "月":
            month = new_date.month
            year = new_date.year
            max_day = calendar.monthlen(year, month)
            start = new_date.replace(day=1).strftime("%Y-%m-%d")
            end = new_date.replace(day=max_day).strftime("%Y-%m-%d")
        elif date_type == "周":
            start = new_date - datetime.timedelta(days=new_date.weekday())
            start = start.strftime("%Y-%m-%d")
            end = new_date + datetime.timedelta(days=6 - new_date.weekday())
            end = end.strftime("%Y-%m-%d")
        elif date_type == "年":
            year = new_date.year
            start = new_date.replace(year=year, month=1, day=1).strftime("%Y-%m-%d")
            end = new_date.replace(year=year, month=12, day=31).strftime("%Y-%m-%d")
        else:
            raise AssertionError("类型只能为年月，实际传参为： %s" % date_type)
        return start, end

    @staticmethod
    def str_to_timestamp(time_str, is_end=False, timezone="md"):
        """
        将字符串转为时间戳
        :param time_str:
        :param is_end: 是否是结束时间，如果是则精确到毫秒
        :param timezone: md |
        :return:
        """
        if timezone == 'md':
            diff = 46800000
        else:
            diff = 0
        timestamp = int(time.mktime(time.strptime(time_str, "%Y-%m-%d %H:%M:%S"))) * 1000 + diff
        return timestamp if not is_end else timestamp + 999

    @staticmethod
    def get_timestamp(day=0, hour=0, minute=0, second=0, now=None):
        """
        获取距当前多久时间的时间戳
        :param day:
        :param hour:
        :param minute:
        :param second:
        :param now:
        :return:
        """
        return DateUtil.str_to_timestamp(DateUtil._get_relative_time(day, hour, minute, second, now))

    @staticmethod
    def get_day_start_timestamp(diff=0, timezone="shanghai"):
        """
        获取指定日期的起始时间戳
        :param diff:
        :param timezone:shanghai|UTC(default)
        :return:
        """
        now_date = [int(item) for item in DateUtil.get_date_by_now(diff=diff, timezone=timezone).split("-")]
        now = datetime.datetime(now_date[0], now_date[1], now_date[2], 0, 0, 0, 0)
        return DateUtil.get_timestamp(now=now)

    @staticmethod
    def timestamp_to_date(timestamp, timezone='美东', exact_type='日', day_diff=0):
        """
        时间戳转日期
        :param timestamp:
        :param timezone: utc | Asia/Shanghai | 美东
        :param exact_type: 精确度： 日 ｜ 秒
        :param day_diff:
        :return:
        """
        timezone_dic = {"北京": 'Asia/Shanghai', '美东': 'GMT-5'}
        if exact_type == "日":
            format_str = '%Y-%m-%d'
        else:
            format_str = '%Y-%m-%d %H:%M:%S'
        return arrow.get(timestamp).to(timezone_dic[timezone]).shift(days=int(day_diff)).strftime(format_str)

    @staticmethod
    def timestamp_to_time(timestamp, timezone='GMT-5'):
        """
        时间戳转日期
        :param timestamp:
        :param timezone: utc | Asia/Shanghai | GMT-5
        :return:
        """
        return arrow.get(timestamp).to(timezone).strftime("%Y-%m-%d %H:%M:%S")

    # @staticmethod
    # def get_timestamp_range(start_diff=0, end_diff=0, stop_diff=None, date_type="日", timezone="md"):
    #     start_day, _ = DateUtil.get_day_range(date_type, start_diff, stop_diff, timezone)
    #     _, end_day = DateUtil.get_day_range(date_type, end_diff, stop_diff, timezone)
    #     start_timestamp = DateUtil.str_to_timestamp(f"{start_day} 00:00:00", timezone=timezone)
    #     end_timestamp = DateUtil.str_to_timestamp(f"{end_day} 23:59:59", is_end=True, timezone=timezone)
    #     return start_timestamp, end_timestamp

    @staticmethod
    def get_timestamp_range(start_diff=0, end_diff=0, stop_diff=None, date_type="日", timezone="md"):
        start_day, _ = DateUtil.get_day_range(date_type, start_diff, stop_diff, timezone)
        _, end_day = DateUtil.get_day_range(date_type, end_diff, stop_diff, timezone)
        start_timestamp = DateUtil.str_to_timestamp(f"{start_day} 00:00:00", timezone=timezone)
        end_timestamp = DateUtil.str_to_timestamp(f"{end_day} 23:59:59", is_end=True, timezone=timezone)
        return start_timestamp, end_timestamp


if __name__ == '__main__':
    tp = int(time.mktime(time.strptime('2024-01-01', "%Y-%m-%d"))) * 1000
    result = arrow.get(tp).to('Asia/Shanghai').shift(days=2).strftime("%Y-%m-%d")
    print(result)

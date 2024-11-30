# -*- coding: utf-8 -*-
import copy
import datetime
import json
import random
import arrow
import calendar
import time
import string
import base64
import hmac
import struct
import hashlib
import os
import collections
from hashlib import sha256
from tzlocal import get_localzone
from decimal import Decimal
from Crypto.Cipher import AES
from collections import *
from Library.LiveLibrary.PublicVariables import value_order_dic, number_dic
from Library.LiveLibrary.PokerGenerator import poker, colors


class CommonFunc(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self, *args, **kwargs):
        self.pub_key = "-----BEGIN PUBLIC KEY-----\nMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL1XuLmIZttk13hmAGVuXiKSfQggfVck" \
                       "p+iNr9jBIxkmBBfmygJ9D5A7lhUbhBEY1SqyGNIHI1DsNLfxfRvW2EcCAwEAAQ==\n-----END PUBLIC KEY-----"
        super().__init__()

    def get_md_search_time(self, diff=0):
        """
        对应客户端的今日早盘滚球的搜索，获取美东的一天对应的UTC的开始和结束时间
        :param diff:
        :return:start_time, end_time
        """
        now_date = self.get_md_date_by_now(diff=diff)
        next_date = self.get_md_date_by_now(diff=diff + 1)
        start_date_list = now_date.split("-")
        end_date_list = next_date.split("-")
        start_time = datetime.datetime(int(start_date_list[0]), int(start_date_list[1]),
                                       int(start_date_list[2]), 4, 00, 00)
        end_time = datetime.datetime(int(end_date_list[0]), int(end_date_list[1]), int(end_date_list[2]), 4, 00, 00)
        return start_time, end_time

    @staticmethod
    def get_element_counter(list_obj: list):
        """
        对列表元素进行计数
        :param list_obj:
        :return:
        """
        return sorted(collections.Counter(list_obj).items(), key=lambda value: value[1], reverse=True)

    def get_month_day_num(self, diff=0):
        now = self.get_current_time("shanghai")
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
        if int(now_time) < 12:
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
        return now.strftime("%Y/%m/%d %H:%M:%S")

    @staticmethod
    def get_current_time(timezone="md"):
        """
        根据时区返回当前时间
        :param timezone: (default)shanghai|UTC|md
        :return:
        """
        if timezone == "utc":
            now = arrow.utcnow()
        elif timezone == "md":
            now = arrow.now("GMT-5")
        else:
            now = arrow.now("Asia/Shanghai")
        return now

    def get_date_by_now(self, date_type="日", diff=-1, timezone="shanghai"):
        """
        获取当前日期前的时间，不包含小时分钟秒
        :param date_type: 年|月|日，默认为日
        :param diff:之后传正值，之前传负值
        :param timezone: shanghai|UTC(default)
        :return:
        """
        now = self.get_current_time(timezone)
        if date_type in ("日", "今日"):
            return now.shift(days=int(diff)).strftime("%Y-%m-%d")
        elif date_type in ("月", "本月"):
            return now.shift(months=int(diff)).strftime("%Y-%m")
        elif date_type == "年":
            return now.shift(years=int(diff)).strftime("%Y")
        else:
            raise AssertionError("类型只能为年月日，实际传参为： %s" % date_type)

    def get_md_date_by_now(self, date_type="日", diff=0):
        """
        获取美东时区的当前日期前的时间，不包含小时分钟秒
        :param date_type: 年|月|日，默认为日
        :param diff:之后传正值，之前传负值
        :return:
        """
        diff = self.get_md_diff_unit(int(diff))
        return self.get_date_by_now(date_type, int(diff), "shanghai")

    @staticmethod
    def get_current_time_for_client(time_type="now", day_diff=0):
        now = arrow.now().shift(days=+day_diff)
        if time_type == "now":
            return now.strftime("%Y-%m-%dT%H:%M:%S+07:00")
        elif time_type == "begin":
            return now.strftime("%Y-%m-%dT00:00:00+07:00")
        elif time_type == "end":
            return now.strftime("%Y-%m-%dT23:59:59+07:00")
        else:
            raise AssertionError("【ERR】传参错误")

    def get_day_range(self, date_type="月", diff=0, timezone="shanghai"):
        """
        获取年、月的起始和结束日期，不含小时分钟秒
        :param date_type: 年|月|周，默认为月
        :param diff:之后传正值，之前传负值
        :param timezone: (default)shanghai|UTC
        :return: 该月起始及最后一天
        """
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
    def _get_time_area():
        dt = get_localzone()
        if "Asia/Bangkok" in dt:
            return 1
        else:
            return 2

    @staticmethod
    def convert_to_percent(number):
        """
        将数字转为百分数
        :param number:
        :return:
        """
        return int(number * 10000) / 100

    @staticmethod
    def two_list_should_be_equal(data1, data2, if_sort="是"):
        """
        断言两个列表值相同,abandon
        :param data1:
        :param data2:
        :param if_sort: 是否对列表中的元素进行排序:   是|否，默认为是
        :return:
        """
        data1 = list(data1)
        data2 = list(data2)
        if len(data1) != len(data2):
            print(data1)
            print(data2)
            raise AssertionError("两个列表长度不一致！")
        if if_sort == "是":
            data1.sort()
            data2.sort()
        for i in range(len(data1)):
            item_1 = data1[i] if data1[i] else 0
            item_2 = data2[i] if data2[i] else 0
            if item_1 == item_2:
                continue
            if (type(item_1) in (float, int)) or (type(item_2) in (int, float)):
                item_1 = float(round(float(item_1), 3))
                item_2 = float(round(float(item_2), 3))
            if item_1 != item_2:
                try:
                    if float(item_1) == float(item_2):
                        pass
                    else:
                        print(data1)
                        print(data2)
                        raise AssertionError(f"两个列表数据不一致！第{i}项,分别为{data1[i]}和{data2[i]}")
                except ValueError:
                    try:
                        if float(item_1) != float(item_2):
                            pass
                    except ValueError:
                        print(data1)
                        print(data2)
                        raise AssertionError(f"两个列表数据不一致！第{i}项,分别为{data1[i]}和{data2[i]}")

    @staticmethod
    def convert_none_to_zero_in_list(list_obj):
        list_obj = list(list_obj)
        for index, item in enumerate(list_obj):
            if not item:
                list_obj[index] = 0
        return list_obj

    @staticmethod
    def get_key(key) -> bytes:
        hash_obj = sha256(key.encode("utf-8"))
        hash_data = hash_obj.digest()
        return hash_data[:16]

    @staticmethod
    def encrypt(token, data):
        def padding(s):
            return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

        # padding = lambda s: s + (16 - len(s) % 16) * chr(16 - len(s) % 16)
        cipher_text = AES.new(CommonFunc.get_key(token), AES.MODE_ECB).encrypt(
            padding(json.dumps(data)).encode("utf-8"))
        return base64.b64encode(cipher_text).decode("utf-8")

    @staticmethod
    def decrypt(token, data):
        try:
            meg = AES.new(CommonFunc.get_key(token), AES.MODE_ECB).decrypt(base64.b64decode(data)).decode("utf-8")
            return json.loads(meg[:-ord(meg[-1])])
        except Exception as e:
            return f"解码失败: {str(e)}"

    @staticmethod
    def _str_to_timestamp(time_str):
        """
        将字符串转为时间戳
        :param time_str:
        :return:
        """
        return int(time.mktime(time.strptime(time_str, "%Y/%m/%d %H:%M:%S"))) * 1000

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
        return CommonFunc._str_to_timestamp(CommonFunc._get_relative_time(day, hour, minute, second, now))

    @staticmethod
    def compare_value_with_ignore(value_1, value_2, ignore=0.01):
        """
        比较两个数字，允许差异
        :param value_1:
        :param value_2:
        :param ignore:
        :return:
        """
        if abs(float(value_1) - float(value_2)) <= float(ignore):
            return True
        else:
            raise AssertionError(f"{value_1}和{value_2}不相等")

    @staticmethod
    def list_data_should_be_equal(data_list_1, data_list_2, ignore_value=0.01):
        """
        列表数据校验
        :param data_list_1:
        :param data_list_2:
        :param ignore_value:
        :return:
        """
        if len(data_list_1) != len(data_list_2):
            print(data_list_1)
            print(data_list_2)
            raise AssertionError(f"两列表长度不一致: {len(data_list_1)} : {len(data_list_2)}")
        for index in range(len(data_list_1)):
            # print(f"{data_list_1[index]}, {data_list_2[index]}")
            if type(data_list_1[index]) in (list, tuple):
                CommonFunc.list_data_should_be_equal(data_list_1[index], data_list_2[index], ignore_value)
            else:
                if (type(data_list_1[index]) not in (int, float) or type(data_list_1[index]) not in (int, float)) \
                        and not data_list_1[index]:
                    if data_list_2[index]:
                        raise AssertionError("数据不一致,第%d-%d项\n后台为：%s\n数据库为：%s"
                                             % (index, index, data_list_1, data_list_2))
                elif (type(data_list_1[index]) in (int, float)) or (type(data_list_2[index]) in (int, float)):
                    data_1 = Decimal(str(data_list_1[index]))
                    data_2 = Decimal(str(data_list_2[index])) if data_list_2[index] else 0
                    if data_1 == data_2:
                        continue
                    else:
                        if abs(data_2 - data_1) > ignore_value:
                            print(abs(data_2 - data_1))
                            raise AssertionError(f"数据不一致,第{index}项，data1为：{data_1}, data2为：{data_2}\n原数据:\n"
                                                 f"data1: {data_list_1}\ndata2: {data_list_2}")
                elif type(data_list_1[index]) == str:
                    data_1 = data_list_1[index].upper().strip()
                    data_2 = data_list_2[index].upper().strip()
                    assert data_1 == data_2, f"数据不一致,第{index}项，data1为：{data_1}, data2为：{data_2}.\n原数据:\n" \
                                             f"data1: {data_list_1}\ndata2: {data_list_2}"
                else:
                    raise AssertionError("没有见过这种场景！")

    @staticmethod
    def compare_list_with_index(int_data, sql_data, com_index=0, com_index_1=None, com_index_2=None,
                                ignore_value=0.011):
        """
        双层列表,指定关联索引
        :param int_data:
        :param sql_data:
        :param com_index:
        :param com_index_1:
        :param com_index_2:
        :param ignore_value
        :return:
        """
        com_index_1 = int(com_index_1) if com_index_1 else com_index_1
        com_index_2 = int(com_index_2) if com_index_2 else com_index_2
        int_data = list(int_data)
        sql_data = list(sql_data)
        assert len(int_data) == len(sql_data), f"接口查询的结果与数据库查询长度不一致!接口为{len(int_data)},sql为{len(sql_data)}"
        if int_data == sql_data:
            return
        for index in range(len(int_data) - 1, -1, -1):
            for item in sql_data:
                temp_data11 = 0 if not item[com_index] else item[com_index]
                temp_data21 = 0 if not int_data[index][com_index] else int_data[index][com_index]
                if not com_index_2:
                    if not com_index_1:
                        if temp_data11 == temp_data21:
                            CommonFunc.list_data_should_be_equal(int_data[index], item, ignore_value)
                            break
                    else:
                        temp_data12 = 0 if not item[com_index_1] else item[com_index_1]
                        temp_data22 = 0 if not int_data[index][com_index_1] else int_data[index][com_index_1]
                        if temp_data11 == temp_data21 and temp_data12 == temp_data22:
                            CommonFunc.list_data_should_be_equal(int_data[index], item, ignore_value)
                            break
                else:
                    temp_data12 = 0 if not item[com_index_1] else item[com_index_1]
                    temp_data22 = 0 if not int_data[index][com_index_1] else int_data[index][com_index_1]
                    temp_data13 = 0 if not item[com_index_2] else item[com_index_2]
                    temp_data23 = 0 if not int_data[index][com_index_2] else int_data[index][com_index_2]
                    if temp_data11 == temp_data21 and temp_data12 == temp_data22 and temp_data23 == temp_data13:
                        CommonFunc.list_data_should_be_equal(int_data[index], item, ignore_value)
                        break

            else:
                raise AssertionError(f"数据未找到:{int_data[index]}")

    @staticmethod
    def compare_multiple_list(backend_data, sql_data):
        """
        双层列表
        :param backend_data:
        :param sql_data:
        :return:
        """
        for index in range(len(backend_data)):
            for index_sub in range(len(backend_data[index])):
                try:
                    if not backend_data[index][index_sub]:
                        if sql_data[index][index_sub]:
                            raise AssertionError("数据不一致,第%d-%d项，后台为：%s, 数据库为：%s"
                                                 % (index, index_sub, backend_data[index][index_sub],
                                                    sql_data[index][index_sub]))
                        else:
                            continue
                    data_backend = float(backend_data[index][index_sub])
                    data_sql = float(sql_data[index][index_sub]) if sql_data[index][index_sub] else 0
                    if float(data_sql) not in ((int(data_backend * 100) + 1) / 100,
                                               (int(data_backend * 100) - 1) / 100,
                                               int(data_backend * 100) / 100,
                                               (int(data_backend * 100) + 2) / 100,
                                               (int(data_backend * 100) - 2) / 100):
                        print(backend_data[index])
                        print(sql_data[index])
                        raise AssertionError("数据不一致,第%d-%d项，后台为：%s, 数据库为：%s" % (index, index_sub,
                                                                                data_backend, data_sql))
                except ValueError:
                    data_sql = sql_data[index][index_sub].upper()
                    data_backend = backend_data[index][index_sub].upper()
                    if data_sql != data_backend:
                        print(backend_data[index])
                        print(sql_data[index])
                        raise AssertionError("数据不一致,第%d-%d项，后台为：%s, 数据库为：%s" % (index, index_sub,
                                                                                data_backend, data_sql))

    @staticmethod
    def check_index_list_data(backend_data, sql_data):
        """
        单层列表
        :param backend_data:
        :param sql_data:
        :return:
        """
        backend_data = list(backend_data)
        sql_data = list(sql_data)
        if len(backend_data) != len(sql_data):
            raise AssertionError("Err: 列表长度不一致")
        for index in range(len(backend_data)):
            try:
                if sql_data[index] == backend_data[index]:
                    continue
                if not sql_data[index]:
                    sql_data[index] = 0
                sql_item = float(sql_data[index])
                data_list = [sql_item, sql_item + 0.01, sql_item - 0.01, sql_item + 0.02, sql_item - 0.02]
                if float(backend_data[index]) not in data_list:
                    raise AssertionError("数据不一致,第%d项，后台为：%s, 数据库为：%s" % (index, backend_data[index],
                                                                         sql_data[index]))
            except Exception as e:
                print(e)
                data_sql = str(sql_data[index]).upper()
                data_backend = str(backend_data[index]).upper()
                if data_sql != data_backend:
                    raise AssertionError("数据不一致,第%d项，后台为：%s, 数据库为：%s" % (index, backend_data[index],
                                                                         sql_data[index]))

    @staticmethod
    def check_index_multi_list_data(backend_data, sql_data):
        """
        列表嵌套列表的类型
        :param backend_data:
        :param sql_data:
        :return:
        """
        if len(backend_data) != len(sql_data):
            raise AssertionError("数据列表长度不一致,后台为：%d, 数据库为：%d" % (len(sql_data), len(backend_data)))
        for index in range(len(backend_data)):
            CommonFunc.check_index_list_data(sql_data[index], backend_data[index])

    @staticmethod
    def generate_string(random_length, random_type=""):
        """
        随机生成指定长度的指定字符类型的字符串
        :param random_type 类型： 大写字母|小写字母|数字
        :param random_length 长度
        """
        if random_type == "大写字母":
            seed = string.ascii_lowercase
        elif random_type == '小写字母':
            seed = string.ascii_uppercase
        elif random_type == "字母":
            seed = string.ascii_letters
        elif random_type == '数字':
            seed = string.digits
        else:
            seed = string.digits + string.ascii_letters
        return ''.join([random.choice(seed) for _ in range(int(random_length))])

    @staticmethod
    def get_day_start_timestamp(diff=0, timezone="shanghai"):
        """
        获取指定日期的起始时间戳
        :param diff:
        :param timezone:shanghai|UTC(default)
        :return:
        """
        now_date = [int(item) for item in CommonFunc.get_date_by_now(diff=diff, timezone=timezone).split("-")]
        now = datetime.datetime(now_date[0], now_date[1], now_date[2], 0, 0, 0, 0)
        return CommonFunc.get_timestamp(now=now)

    @staticmethod
    def get_mongo_search_date(diff=-1, timezone="shanghai", is_end=False):
        now = CommonFunc.get_current_time(timezone)
        now = now.shift(days=int(diff))
        year = int(now.strftime("%Y"))
        month = int(now.strftime("%m"))
        day = int(now.strftime("%d"))
        if is_end:
            return datetime.datetime(year, month, day, 23, 59, 59) - datetime.timedelta(hours=8)
        else:
            return datetime.datetime(year, month, day, 0, 0, 0) - datetime.timedelta(hours=8)

    @staticmethod
    def exactly_round(value, digits=2):
        if int(value) != value:
            left = int(value * 10 ** (digits + 1) % 10)
            main = int(value * 10 ** digits) / 10 ** digits
            if left == 5:
                if main == round(value, digits):
                    if digits:
                        main += 1 / (10 ** digits)
                    else:
                        main += 1
                else:
                    main = round(value, digits)
            return main
        else:
            return value

    @staticmethod
    def round_value_up(value, digits=2):
        """
        向上进1
        :param value:
        :param digits:
        :return:
        """
        value = round(value, 4)
        new_value = int(value * 10 ** digits) / 10 ** digits
        if new_value < value:
            new_value += 1 / 10 ** 2
        return new_value

    @staticmethod
    def cal_google_code(secret_key):
        input_str = int(time.time()) // 30
        key = base64.b32decode(secret_key)
        msg = struct.pack(">Q", input_str)
        google_code = hmac.new(key, msg, hashlib.sha1).digest()
        o = google_code[19] & 15
        google_code = str((struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000)
        if len(google_code) == 5:  # 如果验证码的第一位是0，则不会显示。此处判断若是5位码，则在第一位补上0
            google_code = '0' + google_code
        return google_code

    @staticmethod
    def add_paths():
        """
        将路径添加到环境变量中
        :return:
        """
        os.environ["PATH"] = os.pathsep.join([str(os.path.dirname(__file__)), os.environ["PATH"]])

    @staticmethod
    def change_card_str_to_object(card_str):
        """
        将字符串格式的牌转换为对象
        :param card_str:
        :return:
        """
        cp_value_order_dic = copy.deepcopy(value_order_dic)
        cp_value_order_dic["A"] = 14
        color = card_str[0]
        value: str = card_str[1:]
        return poker(colors[int(color) - 1], color, value, cp_value_order_dic[value.upper()], number_dic[value.upper()])

    @staticmethod
    def get_ordered_card_list(card_list: list):
        """
        返回按数量及点数排序后的排序，降序
        :param card_list: card object
        :return:
        """
        natural_number_card_list = [item.naturalNumber for item in card_list]
        natural_number_card_list.sort(reverse=True)
        natural_number_count_result = Counter(natural_number_card_list).most_common(len(natural_number_card_list))
        result_list = []
        for card in natural_number_count_result:
            result_list.extend(list(filter(lambda item: item.naturalNumber == card[0], card_list)))
        return result_list

    @staticmethod
    def get_poker_max_origin_number(card_list: str):
        """
        获取牌型最大牌的原始点数
        :param card_list:
        :return:
        """
        card_list = [CommonFunc.change_card_str_to_object(item) for item in card_list.split(",")]
        card_list = CommonFunc.get_ordered_card_list(card_list)
        card_list = CommonFunc.get_ordered_card_list(card_list)
        return card_list[0].originNumber

    @staticmethod
    def generate_card_value_list(card_list):
        """
        生成牌型的自然数列表
        :param card_list:
        :return:
        """
        if type(card_list) == str:
            return f"{card_list[0]}{value_order_dic[card_list[1:]]}"
        else:
            return [f"{card[0]}{value_order_dic[card[1:]]}" for card in card_list]

    @staticmethod
    def generate_card_value_list_gf(card_list, has_color=True, change_a_to_max=False):
        """
        生成牌型的自然数列表
        :param card_list:
        :param has_color: 针对传列表的场景，每个元素是否包含花色
        :param change_a_to_max: 将A转为14点或转1点， True | False
        :return:
        """
        value_order_dic_cp = copy.deepcopy(value_order_dic)
        if not change_a_to_max:
            value_order_dic_cp["A"] = 14
        if type(card_list) == str:
            return [f'{item[0]}{value_order_dic[item[1:]]}' for item in card_list.split(",")]
        else:
            result = []
            for card in card_list:
                if not has_color:
                    result.append(value_order_dic[card])
                else:
                    result.append(f"{card[0]}{value_order_dic[card[1:]]}")
            return result

    @staticmethod
    def get_distinct_card_list_by_natural_number(card_list):
        """
        传入card类型的列表，生成按点数去重的牌列表
        :param card_list:
        :return: 从大到小的去重后的列表
        """
        distinct_card_dic = {}
        for item in card_list:
            if item.naturalNumber not in distinct_card_dic:
                distinct_card_dic[item.naturalNumber] = item
        distinct_card_list = sorted(distinct_card_dic.values(), key=lambda element: element.naturalNumber, reverse=True)
        return distinct_card_list

    @staticmethod
    def add_min_a_to_card_list(card_list):
        """
        牌里面若遇到A则塞相同花色的1点的A
        :param card_list:
        :return:
        """
        # 将14点的A替换为1点的A
        cp_card_list = copy.deepcopy(card_list)
        card_a_result = list(filter(lambda item: item.naturalNumber == 14, cp_card_list))
        # 若有A，则往里面塞一个点数为1的A
        if card_a_result:
            [cp_card_list.append(poker(element.color, element.colorValue, element.originNumber, 1, 1)) for
             element in card_a_result]
        return cp_card_list

    @staticmethod
    def valid_bet_amount(bet_amount, win_lose_amount):
        """
        根据新规则生成有效投注金额
        :param bet_amount:
        :param win_lose_amount:
        :return:
        """
        return min(abs(float(win_lose_amount)), float(bet_amount))


class SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(SingletonType, cls).__call__(*args, **kwargs)
        # print(cls._instances)
        return cls._instances[cls]


if __name__ == "__main__":
    cf = CommonFunc()
    print(cf.valid_bet_amount(98, 0))

# -*- coding: utf-8 -*-
import random
import string
import hashlib
import os
import collections


class CommonUtil(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def get_element_counter(list_obj: list):
        """
        对列表元素进行计数
        :param list_obj:
        :return:
        """
        return sorted(collections.Counter(list_obj).items(), key=lambda value: value[1], reverse=True)

    @staticmethod
    def convert_to_percent(number):
        """
        将数字转为百分数
        :param number:
        :return:
        """
        return int(number * 10000) / 100

    @staticmethod
    def convert_none_to_zero_in_list(list_obj):
        list_obj = list(list_obj)
        for index, item in enumerate(list_obj):
            if not item:
                list_obj[index] = 0
        return list_obj

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
    def add_paths():
        """
        将路径添加到环境变量中
        :return:
        """
        os.environ["PATH"] = os.pathsep.join([str(os.path.dirname(__file__)), os.environ["PATH"]])


if __name__ == "__main__":
    cf = CommonUtil()

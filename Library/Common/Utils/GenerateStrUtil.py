#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/8 12:48
import string
import random


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


def generate_string_user_account(account_type):
    if account_type == '手机号码':
        account = '180' + generate_string(8, '数字')
    else:
        account = generate_string(7) + '@gmail.com'
    return account

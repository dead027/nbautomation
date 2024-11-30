# -*- coding: UTF-8 -*-

"""
@Project : AutomatedTest-Bw
@File    : decimal_util.py
@Author  : 带篮子
@Date    : 2024/4/17 14:06
@Describe: 运算工具
"""
from decimal import Decimal, localcontext, ROUND_HALF_UP


class DecimalChain:
    def __init__(self, value, precision=8, rounding=ROUND_HALF_UP):
        self.value = Decimal(value)
        self.precision = precision
        self.rounding = rounding

    def add(self, other):
        self.value += Decimal(other)
        return self

    def subtract(self, other):
        self.value -= Decimal(other)
        return self

    def multiply(self, other):
        self.value *= Decimal(other)
        return self

    def divide(self, other):
        if Decimal(other) == 0:
            raise ZeroDivisionError("除数不能为零")
        self.value /= Decimal(other)
        return self

    def quantize(self, precision=None):
        precision = precision if precision is not None else self.precision
        quantize_precision = Decimal('1.' + '0' * precision)
        with localcontext() as ctx:
            ctx.rounding = self.rounding
            self.value = self.value.quantize(quantize_precision, rounding=self.rounding)
        return self

    def result(self):
        return self.value


class DecimalUtil:
    def __init__(self, precision=8, rounding_method=ROUND_HALF_UP):
        self.precision = precision
        self.rounding_method = rounding_method

    def create_chain(self, value):
        return DecimalChain(value, self.precision, self.rounding_method)


# 使用示例
if __name__ == '__main__':
    util = DecimalUtil()  # 设置默认精度为2位小数
    divide = util.create_chain(50).subtract(1).divide(1).quantize(2).value
    print(divide)

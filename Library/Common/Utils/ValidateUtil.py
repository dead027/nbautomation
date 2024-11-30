#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/5/8 09:59
from decimal import Decimal


class ValidateUtil(object):
    @staticmethod
    def _compare_value_with_ignore(value_1, value_2, ignore=0.01):
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
    def dict_data_should_be_equal(dict1, dict2, ignore=0.01):
        """
        比较两个字典，允许差异
        :param dict1:
        :param dict2:
        :param ignore:
        :return:
        """
        assert len(dict1.keys()) == len(dict2.keys()), f"字典长度不一致, dict1: {len(dict1.keys())}, " \
                                                       f"dict2: {len(dict2.keys())}"
        for key, value in dict1.items():
            if key not in dict2:
                raise AssertionError(f"{key} 在dict2不存在")
            try:
                if value != dict2[key]:
                    ValidateUtil._compare_value_with_ignore(value, dict2[key], ignore)
            except AssertionError:
                print(dict1)
                print(dict2)
                raise AssertionError(f"{key} 对应的值不一致，dict1：{value}, dict2: {dict2[key]}")

    @classmethod
    def list_data_should_be_equal(cls, data_list_1, data_list_2, ignore_value=0.01, dict_key_1="", dict_key_2="",
                                  ignore_sort=False):
        """
        列表数据校验
        :return:
        """
        if len(data_list_1) != len(data_list_2):
            print(data_list_1)
            print(data_list_2)
            raise AssertionError(f"两列表长度不一致: {len(data_list_1)} : {len(data_list_2)}")
        for index in range(len(data_list_1)):
            # print(f"{data_list_1[index]}, {data_list_2[index]}")
            if type(data_list_1[index]) in (list, tuple):
                ValidateUtil.list_data_should_be_equal(data_list_1[index], data_list_2[index], ignore_value)
            elif type(data_list_1[index]) == dict:
                if ignore_sort:
                    for index_1 in range(len(data_list_2)):
                        if data_list_1[index][dict_key_1] == data_list_2[index_1][dict_key_1]:
                            if dict_key_2 and data_list_1[index][dict_key_2] == data_list_2[index_1][dict_key_2]:
                                print(dict_key_1, dict_key_2)
                                ValidateUtil.dict_data_should_be_equal(data_list_1[index], data_list_2[index_1],
                                                                       ignore_value)
                else:
                    ValidateUtil.dict_data_should_be_equal(data_list_1[index], data_list_2[index], ignore_value)
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

    @classmethod
    def compare_list_with_index(cls, int_data, sql_data, com_index=0, com_index_1=None, com_index_2=None,
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
                            ValidateUtil.list_data_should_be_equal(int_data[index], item, ignore_value)
                            break
                    else:
                        temp_data12 = 0 if not item[com_index_1] else item[com_index_1]
                        temp_data22 = 0 if not int_data[index][com_index_1] else int_data[index][com_index_1]
                        if temp_data11 == temp_data21 and temp_data12 == temp_data22:
                            ValidateUtil.list_data_should_be_equal(int_data[index], item, ignore_value)
                            break
                else:
                    temp_data12 = 0 if not item[com_index_1] else item[com_index_1]
                    temp_data22 = 0 if not int_data[index][com_index_1] else int_data[index][com_index_1]
                    temp_data13 = 0 if not item[com_index_2] else item[com_index_2]
                    temp_data23 = 0 if not int_data[index][com_index_2] else int_data[index][com_index_2]
                    if temp_data11 == temp_data21 and temp_data12 == temp_data22 and temp_data23 == temp_data13:
                        ValidateUtil.list_data_should_be_equal(int_data[index], item, ignore_value)
                        break

            else:
                raise AssertionError(f"数据未找到:{int_data[index]}")

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


if __name__ == '__main__':
    a = [{'订单号': 'R258457462750466048', '会员ID': 'Ujj27GRH', '会员注册信息': '11000000001', 'VIP等级': 'VIP0', '调整方式': '人工增加额度', '订单状态': '审核通过', '调整类型': '会员存款(后台)', '调整金额': Decimal('100.00'), '申请人': 'xingyao5', '申请时间': 1717053941027, '备注': 'By script'}]
    b = [{'订单号': 'R258457462750466048', '会员ID': 'Ujj27GRH', '会员注册信息': '11000000001', 'VIP等级': 'VIP0', '调整方式': '人工增加额度', '订单状态': '审核通过', '调整类型': '会员存款(后台)', '调整金额': 100.0, '申请人': 'xingyao5', '申请时间': 1717053941027, '备注': 'By script'}]
    print(ValidateUtil.list_data_should_be_equal(a, b, dict_key='订单号'))
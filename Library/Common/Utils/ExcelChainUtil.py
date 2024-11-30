# -*- coding: UTF-8 -*-

"""
@Project : AutomatedTest-Bw 
@File    : excel_chain_util
@Author  : 带篮子
@Date    : 2024/4/27 12:20
@Describe: excel链式工具
"""
import copy
import logging
from pprint import pprint
from typing import Dict, List

from common.annotation.auto_repr_decorator import auto_repr
from common.utils.excel_plus_util import ExcelPlusUtil
from constant import FILE_NAME
from pojo.domain.common.excel_model import ExcelCaseModel


@auto_repr
class ExcelDataChain:

    def __init__(self, file_name: str = FILE_NAME):
        self.sheet_name = None
        self.file_name = file_name
        self.initial_data: Dict[str, List[ExcelCaseModel]] = ExcelPlusUtil.read_all_excel(file_name)
        self.data: List[ExcelCaseModel] = []

    def get_sheet(self, sheet_name):
        self.sheet_name = sheet_name
        self.data = copy.deepcopy(self.initial_data.get(sheet_name, []))
        return self

    def filter(self, group_name: str, case_id: int = 0):
        self.data = ExcelPlusUtil.filter_excel_cases(self.data, group_name, case_id)
        return self

    def list(self):
        return self.data

    def first(self):
        if not self.data:
            raise Exception("ExcelDataChain.data is Empty !")
        return self.data[0]

    def update(self, update_case: List[ExcelCaseModel]):
        try:
            logging.info(f"Updating rows in file {self.file_name}, sheet {self.sheet_name}.")
            ExcelPlusUtil.update_excel(self.file_name, self.sheet_name, update_case)
            logging.info("Update successful.")
        except Exception as e:
            logging.error(f"Failed to update rows: {e}")
            raise

    def __call__(self):
        return self.list()


if __name__ == '__main__':
    data = ExcelDataChain().get_sheet('bw-admin').data
    pprint(data)

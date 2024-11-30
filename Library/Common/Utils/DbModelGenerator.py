#!/usr/bin/env python
# -*- coding:utf-8 -*-
import subprocess
import os
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.Contexts import *


class ModelGenerator(object):
    def __init__(self):
        server = YamlUtil().load_common_config('mysql')
        self.db_url = f'mysql+pymysql://{server["username"]}:{server["password"]}@{server["ip"]}:{server["port"]}/' \
                      f'{server["database"]}'
        self.output_path = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__)))) + '/Library/MysqlTableModel'

    def generate_models(self, tables):
        for table in tables.split(','):
            outfile = f"{self.output_path}/{table}_model.py"
            command = f"sqlacodegen --tables {table} --outfile {outfile} {self.db_url}"
            try:
                subprocess.run(command, shell=True, check=True)
                print(f"模型已生成: {outfile}")
            except subprocess.CalledProcessError as e:
                print(f"生成模型失败: {e}")


if __name__ == "__main__":
    env_context.set('sit')
    generator = ModelGenerator()
    generator.generate_models(input("请输入要生成模型的表名（逗号分隔）："))

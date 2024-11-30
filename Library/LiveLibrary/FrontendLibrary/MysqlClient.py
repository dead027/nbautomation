import time
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.LiveLibrary.ServerConnector.Mysql import MysqlBase
from Library.LiveLibrary.ServerConnector.Structures import DeskStruct, GameTypeStruct


class MysqlClient(MysqlBase):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    def __init__(self):
        super().__init__()

    def get_desk_info(self, desk_no):
        """
        获取桌台信息
        :param desk_no:
        :return:
        """
        sql = f"select * from field_desk where desk_code='{desk_no}'"
        rtn = self.query_data(sql)[0]
        return DeskStruct(*rtn[:11])

    def get_gift_info(self, gift_name):
        sql = f"select id, chinese_name, english_name, picture, amount from platform_gift where " \
              f"chinese_name='{gift_name}'"
        return self.query_data(sql)[0]

    def get_game_type_info(self, type_id=None, type_name=None):
        """
        查询游戏类型信息
        :param type_id:
        :param type_name:
        :return:
        """
        if type_id:
            sql = f"select * from desk_game_type where id='{type_id}'"
        else:
            sql = f"select * from desk_game_type where ='{type_name}'"
        rtn = self.query_data(sql)[0]
        return GameTypeStruct(*rtn[:4])

    def get_user_balance(self, user_id="", user_name=""):
        """
        查询用户余额
        :param user_id:
        :param user_name:
        :return:
        """
        assert user_name or user_id, "必传1个"
        if user_id:
            sql = f"select * from user_coin where user_id='{user_id}'"
        else:
            sql = f"select * from user_coin where user_name='{user_name}'"
        return float(self.query_data(sql)[0][3])

    def wait_until_user_balance_change_to_sh(self, expect_balance, user_id="", user_name="", retry_times=10):
        """
        等待会员余额更新为指定金额
        :param expect_balance:
        :param user_id:
        :param user_name:
        :param retry_times: 最大尝试次数
        :return:
        """
        assert user_name or user_id, "必传1个"
        if user_id:
            sql = f"select * from user_coin where user_id='{user_id}'"
        else:
            sql = f"select * from user_coin where user_name='{user_name}'"
        current_times = 0
        query_balance = 0
        while current_times < retry_times:
            query_balance = float(self.query_data(sql)[0][3])
            if round(query_balance, 2) == round(expect_balance, 2):
                return query_balance
            time.sleep(1)
            current_times += 1
        raise AssertionError(f"当前余额为：{query_balance}，与预期金额{expect_balance}不一致")

    def get_user_id_sh(self, user_name):
        sql = f"select user_id from user_info where user_name='{user_name}'"
        rtn = self.query_data(sql)
        return rtn[0][0]


if __name__ == "__main__":
    mc = MysqlClient()

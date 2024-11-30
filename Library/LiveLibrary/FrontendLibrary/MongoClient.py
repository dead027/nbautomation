import json
import time
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from Library.LiveLibrary.ServerConnector.Structures import *
from Library.Common.Utils.Contexts import *
from Library.LiveLibrary.CommonUtil import CommonFunc
from Library.LiveLibrary.FrontendLibrary.RedisClient import RedisClient


class MongoClient(object):
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'

    @staticmethod
    def get_latest_game_info(table_no):
        """
        获取最后一局游戏的牌型数据
        :return:
        """
        data = live_mg_context.get().mg_select("game_result", {"deskNo": table_no}, sort=[("createdTime", -1)], limit=1)
        if data:
            data = data[0]
            print(f"游戏数据: {data}")
            return data["issueNo"], data["bootNo"], data["issueStatus"], data["createdTime"]. \
                strftime('%Y-%m-%d %H:%M:%S')
        else:
            return None, None, None, None

    @staticmethod
    def generate_next_game_info(table_no, game_struct_name="百家乐"):
        """
        生成下一局游戏的各属性值
        :param table_no:
        :param game_struct_name: 百家乐 | 龙虎 | 三公 | 牛牛 ｜ 德州扑克 | 龙凤炸金花 ｜ 印度炸金花 | 新炸金花
        :return:
        """
        game_strct_type_dic = {"百家乐": BaccaratGameStruct, "龙虎": DtGameStruct, "三公": CattleTgGameStruct,
                               "牛牛": CattleTgGameStruct, "德州扑克": DzGameStruct, "龙凤炸金花": GoldFlowerGameStruct,
                               "印度炸金花": GoldFlowerGameStruct, "新炸金花": CattleTgGameStruct,
                               "色碟": ColorDishGameStruct,
                               "轮盘": RouletteGameStruct, "骰宝": SicboGameStruct, "番摊": FTGameStruct}
        game_struct_type = game_strct_type_dic[game_struct_name]
        identify_start_time = str(CommonFunc.get_current_time()).split(".")[0]
        # temp_game_no = self.rds.hash_get("TempGameNo", table_no)
        cur_boot_no = RedisClient.get_boot_no(table_no)
        game_no, boot_no, game_status, _ = MongoClient.get_latest_game_info(table_no)
        if cur_boot_no != boot_no and cur_boot_no:
            boot_no = cur_boot_no
        if game_no:
            game_no_origin = game_no
            game_no_list: list = list(game_no_origin[-3:])
            # 末位为9，则进1
            if int(game_no_list[-1]) == 9:
                game_no_list[-1] = "0"
                # 中位为Z，首位进1
                if game_no_list[1] == "Z":
                    game_no_list[1] = "A"
                    game_no_list[0] = chr(ord(game_no_list[0]) + 1)
                else:
                    game_no_list[1] = chr(ord(game_no_list[1]) + 1)
            else:
                game_no_list[-1] = str(int(game_no_list[-1]) + 1)
            game_no = game_no_origin[: -3] + "".join(game_no_list)
        else:
            # 生成局号
            month = CommonFunc.get_current_time("md").strftime("%m")
            if month == "10":
                month = "A"
            elif month == "11":
                month = "B"
            elif month == "12":
                month = "C"
            date_str = CommonFunc.get_current_time("md").strftime("%y%d")
            date_str = date_str[:2] + month + date_str[2:]
            game_no = f'G{table_no}{date_str}AA0'

        next_game_info: game_struct_type = game_struct_type(game_no, boot_no, table_no, start_time=identify_start_time)
        return next_game_info

    @staticmethod
    def wait_until_game_status_changed(desk_no, game_no, game_status="下注中", timeout=5):
        game_status_dic = {"下注中": 1, "已结算": 4}
        passed_second = 0
        while passed_second < timeout:
            game_info = MongoClient.get_latest_game_info(desk_no)
            print(game_info)
            if game_info[0] == game_no:
                if game_info[2] == game_status_dic[game_status]:
                    return
            time.sleep(1)
            passed_second += 1
        raise AssertionError("Err: 未等到游戏状态变化")

    @staticmethod
    def generate_next_boot_info(table_no, game_struct_name="龙虎"):
        """
        生成下一靴数据
        :param table_no:
        :param game_struct_name:
        :return:
        """
        game_strct_type_dic = {"龙虎": DtGameStruct}
        # redis_data = self.rds.get_latest_game_info(table_no)
        game_no, boot_no, game_status, _ = MongoClient.get_latest_game_info(table_no)
        cur_boot_no = RedisClient.get_boot_no(table_no)
        if cur_boot_no != boot_no and cur_boot_no:
            boot_no = cur_boot_no

        # 若桌台已存在，且本日新局的靴号与今日相同，则+1
        # if boot_no and int(re.findall(r"(\d+)", boot_no)[1][-2:]) == int(time.strftime("%d", time.localtime())):
        if boot_no and int(boot_no[-10: -8]) == int(CommonFunc.get_current_time("md").strftime("%d")):
            boot_no_list: list = list(boot_no[-4:])
            # 末位为9，则进1
            if int("".join(boot_no_list[-2:])) == 99:
                boot_no_list[-2:] = "00"
                # 中位为Z，首位进1
                if boot_no_list[1] == "Z":
                    boot_no_list[1] = "A"
                    boot_no_list[0] = chr(ord(boot_no_list[0]) + 1)
                else:
                    boot_no_list[1] = chr(ord(boot_no_list[1]) + 1)
            else:
                boot_no_list[-2:] = "%2.f" % (int("".join(boot_no_list[-2:])) + 1)
            boot_no = boot_no[:-4] + "".join(boot_no_list)
        # 桌台不存在，或者跨日了，则为新日的靴号
        else:
            month = CommonFunc.get_current_time("md").strftime("%m")
            if month == "10":
                month = "A"
            elif month == "11":
                month = "B"
            elif month == "12":
                month = "C"
            date_str = CommonFunc.get_current_time("md").strftime("%y%d")
            date_str = date_str[:2] + month + date_str[2:]
            boot_no = f"B0{table_no}"
            boot_no += date_str + CommonFunc.generate_string(2, "字母") + CommonFunc.generate_string(2, "数字") + "AA01"
            game_no = ""

        boot_no = boot_no.replace(" ", "0")
        print(game_struct_name)
        next_game_info = game_strct_type_dic[game_struct_name](game_no, boot_no, table_no)
        return next_game_info

    @staticmethod
    def wait_until_order_status(order_id, status=1, timeout=5):
        """
        等待注单状态更新为指定状态，默认已结算
        :param order_id:
        :param status: 0 未结算，1 已结算
        :param timeout:
        :return:
        """
        start_time = int(time.time())
        while True:
            data = live_mg_context.mg_select("order", {"orderId": order_id, "orderStatus": status})
            print(data)
            if data:
                return
            if int(time.time()) - start_time >= timeout:
                raise AssertionError(f"注单状态未变为{status}, 当前为:{data[0]['orderStatus']}")
            time.sleep(0.25)

    @staticmethod
    def get_game_result_dt(game_no):
        """
        查询游戏局信息
        :param game_no:
        :return:
        """
        data = live_mg_context.get().mg_select("dragon_tiger_game_result", {"gameNo": game_no})
        if data:
            data = data[0]
            return DtGameStruct(*[data[key] for key in ("gameNo", "bootNo", "deskNo", "dragonCard", "tigerCard",
                                                        "isFinish", "createdDate")])
        else:
            return None

    @staticmethod
    def get_game_count_of_boot(boot_no):
        """
        获取boot下有多少局
        :param boot_no:
        :return:
        """
        data = live_mg_context.get().mg_aggregate("game_result", [{"$match": {"bootNo": boot_no}},
                                                                  {"$group": {"_id": None, "count": {"$sum": 1}}}])
        return data[0]["count"] if data else 0

    @staticmethod
    def get_order_info_by_game_no(game_no, user_id, if_all=False, timeout=200):
        """
        查询注单信息
        :param game_no:
        :param user_id:
        :param timeout:
        :param if_all: 是否返回所有数据， False 只返回一条
        :return:
        """
        start_time = time.time()
        while time.time() - start_time < timeout:
            data = live_mg_context.get().mg_aggregate("order", [{"$match": {"gameNo": game_no, "userId": user_id}}])
            if data:
                order_info_list = []
                for item in data:
                    settlement_detail = []
                    if "settlementDetail" in item:
                        detail_origin = json.loads(item["settlementDetail"])

                        dragon = detail_origin["dragonCard"]["pokerPattern"] + detail_origin["dragonCard"][
                            "pokerNumber"]
                        tiger = detail_origin["tigerCard"]["pokerPattern"] + detail_origin["tigerCard"]["pokerNumber"]
                        settlement_detail = [dragon, tiger]

                    order_info = BetOrderStruct(*[item[key] if key in item else None for
                                                  key in ("userId", "merchantId", "merchantNo", "deskNo", "gameNo",
                                                          "bootNo", "roomNo", "gameType", "gameTypeId", "playType",
                                                          "rate", "payAmount", "winLossAmount", "totalAmount",
                                                          "priorAmount", "validAmount", "orderStatus", "betTime",
                                                          "orderId", "currency", "createdTime", "userName",
                                                          "merchantName", "settlementTime", "settlementNum")],
                                                settlement_detail, item["betResult"] if "betResult" in item else "",
                                                item["betIp"], item["betDevice"], None, item["costAmount"])
                    order_info.pay_amount = float(str(order_info.pay_amount))
                    order_info.total_amount = float(str(order_info.total_amount))
                    order_info.valid_amount = float(str(order_info.valid_amount))
                    order_info.prior_amount = float(str(order_info.prior_amount))
                    order_info.rate = float(str(order_info.rate))
                    order_info.cost_amount = float(str(order_info.cost_amount))
                    order_info.settlement_num = int(
                        str(order_info.settlement_num)) if order_info.settlement_num else order_info.settlement_num
                    order_info.win_lose_amount = float(str(order_info.win_lose_amount))
                    order_info.prior_amount = float(str(order_info.prior_amount))
                    order_info.reload_json()
                    name_origin = {"LH_DRAGON": "龙", "LH_TIGER": "虎", "LH_TIE": "和"}[order_info.play_type]
                    name_origin = f"{name_origin}-{int(order_info.total_amount)}"
                    order_info.play_type_origin = name_origin
                    order_info_list.append(order_info)
                    print("------")
                    print(order_info_list[0])
                return order_info_list if if_all else order_info_list[0]
            time.sleep(0.1)
        raise AssertionError("等待注单生成超时")


if __name__ == "__main__":
    env_context.set('sit')
    from Library.LiveLibrary.ServerConnector.Mongo import MongoBase

    MongoBase()
    db = MongoClient()
    # print(db.get_latest_game_info("GA08"))

    # print(db.get_game_result_baccarat("GGA08230211AL9").json)
    print(db.get_order_info_by_game_no('GLH01240614AB3', '5DpAN4Y9'))

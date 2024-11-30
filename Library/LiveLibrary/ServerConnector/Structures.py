#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/6/25 13:31

from copy import deepcopy


# 用户属性
class PlayerStruct(object):
    def __init__(self, user_id=None, user_name=None, nick_name=None, merchant_id=None, merchant_no=None, agent_id=None,
                 agent_no=None, agent_name=None, path=None, wallet_address=None, password=None, user_type=None,
                 user_status=None, currency=None, cus_language=None, login_time=None, login_ip=None, limit_id=None,
                 allow_bet=None, user_belong=None, merchant_name=None, token=None, game_url=None):
        self.game_url = game_url
        self.token = token
        self.user_id = user_id
        self.user_name = user_name
        self.nick_name = nick_name
        self.merchant_id = merchant_id
        self.merchant_no = merchant_no
        self.agent_id = agent_id
        self.agent_no = agent_no
        self.agent_name = agent_name
        self.path = path
        self.wallet_address = wallet_address
        self.password = password
        self.user_type = user_type
        self.user_status = user_status
        self.currency = currency
        self.cus_language = cus_language
        self.login_time = login_time
        self.login_ip = login_ip
        self.limit_id = limit_id
        self.allow_bet = allow_bet
        self.user_belong = user_belong
        self.merchant_name = merchant_name
        self.json = deepcopy(self.__dict__)


# 游戏对局属性
class GameStruct(object):
    def __init__(self, game_type, game_type_id, desk_no, game_no, boot_no):
        self.game_type = game_type  # 游戏类型
        self.game_type_id = game_type_id  # 游戏类型ID
        self.desk_no = desk_no
        self.game_no = game_no
        self.boot_no = boot_no
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 服务器类型
class ServerStruct(object):
    def __init__(self, ip, port="", user_name="", password="", db_name=""):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.json = deepcopy(self.__dict__)


# websocket返回值格式
class WsResponseStruct(object):
    def __init__(self, status: int, data):
        self.status = status
        self.data = data
        self.json = deepcopy(self.__dict__)


# 游戏局信息-百家乐
class BaccaratGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, play_card: list = (), banker_card: list = (),
                 player_bo: bool = False, banker_bo: bool = False, is_finish: bool = False, created_date="",
                 start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.play_card = play_card
        self.banker_card = banker_card
        self.player_bo = player_bo
        self.banker_bo = banker_bo
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-德州扑克
class DzGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, public_card: list = (), play_card: list = (), banker_card: list = (),
                 player_bo: bool = False, banker_bo: bool = False, is_finish: bool = False, created_date="",
                 start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.play_card = play_card
        self.public_card = public_card
        self.banker_card = banker_card
        self.player_bo = player_bo
        self.banker_bo = banker_bo
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-炸金花
class GoldFlowerGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, dragon_card: list = (), phoenix_card: list = (),
                 is_finish: bool = False, created_date="", start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.dragon_card = dragon_card
        self.phoenix_card = phoenix_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-牛牛,三公
class CattleTgGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, banker_card: list = (), player_card_1: list = (),
                 player_card_2: list = (), player_card_3: list = (), is_finish: bool = False, created_date="",
                 start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.play_card_1 = player_card_1
        self.play_card_2 = player_card_2
        self.play_card_3 = player_card_3
        self.banker_card = banker_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-龙虎
class DtGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, dragon_card: list = (), tiger_card: list = (),
                 is_finish: bool = False, created_date="", start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.dragon_card = dragon_card
        self.tiger_card = tiger_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 牛牛牌型类
class CattleResultStruct(object):
    # 庄闲, 是否有牛，点数，颜色，赔率，最大牌值，最大牌字符串，最大牌花色值，最大牌花色字符串，原始牌列表, 是否五公, 牌型
    def __init__(self, side=None, if_has_cattle=False, score=0, color=0, odds_win=0, odds_lose=0):
        self.side = side
        self.if_has_cattle = if_has_cattle
        self.score = score
        self.color = color
        self.odds_win = odds_win
        self.odds_lose = odds_lose
        self.max_number = 0
        self.max_number_str = None
        self.max_color = 0
        self.max_color_str = None
        self.origin_cards = None
        self.if_five_cattle = False
        self.card_type = None
        self.card_type_value = 0


# 三公牌型类
class TgResultStruct(object):
    # 庄闲, 几公，点数，赔率，最大牌值，最大牌字符串，最大牌花色值，最大牌花色字符串，原始牌列表, 牌型, 牌型大小
    def __init__(self, side=None, gong_count=0, score=0, color=0, odds_win=0, odds_lose=0):
        self.side = side
        self.gong_count = gong_count
        self.score = score
        self.color = color
        self.odds_win = odds_win
        self.odds_lose = odds_lose
        self.max_number = 0
        self.max_number_str = None
        self.max_color = 0
        self.max_color_str = None
        self.origin_cards = None
        self.card_type = None
        self.card_type_value = None
        self.full_card_type = None


# 炸金花牌型类
class GoldFlowerResultStruct(object):
    # 龙凤, 牌型，最大牌值，最大牌字符串，最大牌花色值，原始牌列表, 排序后的自然数值牌列表, 牌型, 牌型大小,赢的赔率，输的赔率
    def __init__(self, side=None):
        self.side = side
        self.card_type = 0
        self.max_number = 0
        self.max_number_str = None
        self.max_color = 0
        self.origin_cards = None
        self.ordered_natural_cards = None
        self.card_type_value = None
        self.full_card_type = None
        self.odds_win = None
        self.odds_lose = None


# 游戏局信息-色碟
class ColorDishGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, cd_card: list = (),
                 is_finish: bool = False, created_date="", start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.gameResult = cd_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-轮盘
class RouletteGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, roulette_card: list = (),
                 is_finish: bool = False, created_date="", start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.gameResult = roulette_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-骰宝
class SicboGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, sicbo_card: list = (),
                 is_finish: bool = False, created_date="", start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.gameResult = sicbo_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏局信息-番摊
class FTGameStruct(object):
    def __init__(self, game_no, boot_no, table_no, ft_card: list = (),
                 is_finish: bool = False, created_date="", start_time=None, end_time=None):
        self.game_no = game_no
        self.boot_no = boot_no
        self.table_no = table_no
        self.gameResult = ft_card
        self.is_finish = is_finish
        self.created_date = created_date
        self.start_time = start_time
        self.end_time = end_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏结果
class GameResultStruct(object):
    def __init__(self, game_type="", game_hall="", desk_no="", boot_no="", game_no="",
                 game_status="", game_begin_time="", created_time="", abnormal_mark="", bet_result="",
                 settlement_detail="", settlement_time="", video_url="", is_doing_settlement_again="", set_times=0):
        self.set_times = set_times
        self.is_doing_settlement_again = is_doing_settlement_again
        self.game_type = game_type
        self.game_hall = game_hall
        self.desk_no = desk_no
        self.boot_no = boot_no
        self.game_no = game_no
        self.game_status = game_status
        self.game_begin_time = game_begin_time
        self.created_time = created_time
        self.abnormal_mark = abnormal_mark
        self.bet_result = bet_result
        self.settlement_detail = settlement_detail
        self.settlement_time = settlement_time
        self.video_url = video_url
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 桌台
class DeskStruct(object):
    def __init__(self, desk_id, game_category_id="", game_type_id="", game_hall_id="", label_id="", desk_code="",
                 video_address="", desk_ip="", current_dealer_code="", dealer_name="", status="", table_name="",
                 min_bet_amount=None, max_bet_amount=None, dealer_photo_url=None, dealer_country=None,
                 dealer_country_picture=None, total_online_count=None, identify_start_time=None, game_status=None,
                 game_result_vo_list=None):
        self.desk_id = desk_id  # 游戏类型
        self.game_category_id = game_category_id  # 游戏类型ID
        self.game_type_id = game_type_id
        self.game_hall_id = game_hall_id
        self.label_id = label_id
        self.desk_code = desk_code
        self.video_address = video_address
        self.desk_ip = desk_ip
        self.current_dealer_code = current_dealer_code
        self.dealer_name = dealer_name
        self.status = status
        self.table_name = table_name
        self.min_bet_amount = min_bet_amount
        self.max_bet_amount = max_bet_amount
        self.dealer_photo_url = dealer_photo_url
        self.dealer_country = dealer_country
        self.dealer_country_picture = dealer_country_picture
        self.total_online_count = total_online_count
        self.identify_start_time = identify_start_time
        self.game_status = game_status
        self.game_result_vo_list = game_result_vo_list
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 游戏类型
class GameTypeStruct(object):
    def __init__(self, type_id, game_type, count_down, status):
        self.type_id = type_id
        self.game_type = game_type
        self.count_down = count_down
        self.status = status


# 注单类型
class BetOrderStruct(object):
    def __init__(self, user_id="", merchant_id="", merchant_no="", desk_no="", game_no="",
                 boot_no="", room_no="", game_type="", game_type_id="", play_type="", rate="", pay_amount="",
                 win_lose_amount="", total_amount="", prior_amount="", valid_amount="", order_status="", bet_time="",
                 order_id="", currency="", created_time="", user_name="", merchant_name="", settlement_time="",
                 settlement_num="", settlement_detail="", bet_result="", bet_ip="", bet_device="",
                 play_type_origin="", cost_amount=0):
        self.play_type_origin = play_type_origin
        self.prior_amount = prior_amount
        self.created_time = created_time
        self.user_name = user_name
        self.merchant_name = merchant_name
        self.bet_ip = bet_ip
        self.bet_device = bet_device
        self.user_id = user_id
        self.merchant_id = merchant_id
        self.merchant_no = merchant_no
        self.order_id = order_id
        self.order_status = order_status
        self.desk_no = desk_no
        self.game_no = game_no
        self.boot_no = boot_no
        self.room_no = room_no
        self.total_amount = total_amount
        self.valid_amount = valid_amount
        self.game_type = game_type
        self.game_type_id = game_type_id
        self.play_type = play_type
        self.rate = rate
        self.pay_amount = pay_amount
        self.win_lose_amount = win_lose_amount
        self.settlement_detail = settlement_detail
        self.bet_result = bet_result
        self.currency = currency
        self.bet_time = bet_time
        self.settlement_time = settlement_time
        self.settlement_num = settlement_num
        self.cost_amount = cost_amount
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 商户类型
class MerchantStruct(object):
    def __init__(self, merchant_id="", merchant_no="", cus_language="", merchant_account="", merchant_pwd="",
                 merchant_name="", email="", merchant_nation="",
                 province_city_district="", address="", merchant_level="", is_internal="", currency="",
                 calculation_standard="", platform_rate="", user_rebate_rate="", platform_payment_cycle="",
                 membership_fee="",
                 member_payment_cycle="", service_fee="", tec_payment_cycle="", merchant_maintainer="",
                 wallet_type="", ip_whitelist="", server_whitelist="", api_sign="", merchant_status="",
                 merchant_category="", merchant_type="", parent_id="", path="", is_direct="", level="",
                 consociation_type="", verify_code_type="", api_md5="", rate_effect_time="", future_platform_rate="",
                 limit_id="", rate_id="", is_activation="", origin=""):
        self.user_rebate_rate = user_rebate_rate
        self.merchant_id = merchant_id
        self.merchant_no = merchant_no
        self.merchant_account = merchant_account
        self.merchant_name = merchant_name
        self.email = email
        self.cus_language = cus_language
        self.merchant_pwd = merchant_pwd
        self.api_sign = api_sign
        self.api_md5 = api_md5
        self.merchant_nation = merchant_nation
        self.province_city_district = province_city_district
        self.address = address
        self.merchant_level = merchant_level
        self.is_internal = is_internal
        self.currency = currency
        self.calculation_standard = calculation_standard
        self.platform_rate = platform_rate
        self.platform_payment_cycle = platform_payment_cycle
        self.membership_fee = membership_fee
        self.member_payment_cycle = member_payment_cycle
        self.service_fee = service_fee
        self.tec_payment_cycle = tec_payment_cycle
        self.merchant_maintainer = merchant_maintainer
        self.wallet_type = wallet_type
        self.ip_whitelist = ip_whitelist
        self.server_whitelist = server_whitelist
        self.merchant_status = merchant_status
        self.merchant_category = merchant_category
        self.merchant_type = merchant_type
        self.parent_id = parent_id
        self.path = path
        self.is_direct = is_direct
        self.level = level
        self.consociation_type = consociation_type
        self.verify_code_type = verify_code_type
        self.future_platform_rate = future_platform_rate
        self.limit_id = limit_id
        self.rate_id = rate_id
        self.is_activation = is_activation
        self.origin = origin
        self.rate_effect_time = rate_effect_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 会员账变类型
class BalanceChangeRecordStruct(object):
    def __init__(self, user_name="", nick_name="", merchant_name="", merchant_no="", agent_name="", agent_no="",
                 order_no="",
                 coin_type="", coin_detail="", coin_value="", coin_from="", coin_to="", coin_amount="", balance_type="",
                 remark="", created_time=""):
        self.agent_name = agent_name
        self.agent_no = agent_no
        self.nick_name = nick_name
        self.user_name = user_name
        self.merchant_name = merchant_name
        self.merchant_no = merchant_no
        self.order_no = order_no
        self.balance_type = balance_type
        self.coin_type = coin_type
        self.coin_detail = coin_detail
        self.coin_value = coin_value
        self.coin_from = coin_from
        self.coin_to = coin_to
        self.coin_amount = coin_amount
        self.remark = remark
        self.created_time = created_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 代理账变类型
class BalanceChangeRecordAgentStruct(object):
    def __init__(self, agent_name="", agent_account="", agent_account_status="", currency="", merchant_id="",
                 merchant_name="", merchant_no="", before_amount="", amount="", after_amount="", balance_type="",
                 change_type="", business_type="", order_type="", relate_order_no="", remark="", created_time=""):
        self.order_type = order_type
        self.agent_name = agent_name
        self.business_type = business_type
        self.agent_account = agent_account
        self.agent_account_status = agent_account_status
        self.currency = currency
        self.merchant_id = merchant_id
        self.merchant_name = merchant_name
        self.merchant_no = merchant_no
        self.before_amount = before_amount
        self.amount = amount
        self.after_amount = after_amount
        self.balance_type = balance_type
        self.change_type = change_type
        self.relate_order_no = relate_order_no
        self.remark = remark
        self.created_time = created_time
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 账变类型
class RewardStruct(object):
    def __init__(self, reward_no, merchant_id, merchant_no, merchant_name, user_id, reward_type, currency, amount,
                 dealer_id, dealer_code, dealer_name, desk_code, game_type, game_no, platform_gift_chinese_name,
                 platform_gift_english_name, created_date):
        self.reward_no = reward_no
        self.merchant_id = merchant_id
        self.merchant_no = merchant_no
        self.merchant_name = merchant_name
        self.user_id = user_id
        self.reward_type = reward_type
        self.currency = currency
        self.amount = amount
        self.dealer_id = dealer_id
        self.dealer_code = dealer_code
        self.dealer_name = dealer_name
        self.desk_code = desk_code
        self.game_type = game_type
        self.game_no = game_no
        self.platform_gift_chinese_name = platform_gift_chinese_name
        self.platform_gift_english_name = platform_gift_english_name
        self.created_date = created_date
        self.json = deepcopy(self.__dict__)


# 代理信息
class AgentInfoStruct(object):
    def __init__(self, agent_id, merchant_id, merchant_name, merchant_no, agent_no, agent_account, agent_pwd,
                 agent_name, currency, agent_rebate_rate, user_rebate_rate, is_modify_user_rebate, status,
                 agent_category, parent_id, path, level, verify_code_type, limit_id, is_activation, agent_domain,
                 wallet_address):
        self.agent_id = agent_id
        self.merchant_id = merchant_id
        self.merchant_name = merchant_name
        self.merchant_no = merchant_no
        self.agent_no = agent_no
        self.agent_account = agent_account
        self.agent_pwd = agent_pwd
        self.agent_name = agent_name
        self.currency = currency
        self.agent_rebate_rate = agent_rebate_rate
        self.user_rebate_rate = user_rebate_rate
        self.is_modify_user_rebate = is_modify_user_rebate
        self.status = status
        self.agent_category = agent_category  # 1 占成，2 洗码
        self.parent_id = parent_id
        self.path = path
        self.level = level
        self.verify_code_type = verify_code_type
        self.limit_id = limit_id
        self.is_activation = is_activation
        self.agent_domain = agent_domain
        self.wallet_address = wallet_address
        self.json = deepcopy(self.__dict__)


# 牌型
class CardStruct(object):
    # 原始牌值，颜色，牌牛牛数值，颜色自然数值, 牌的自然值
    def __init__(self, origin_num_str, color_str, value, color_value, order_value):
        self.origin_num_str = origin_num_str
        self.color_str = color_str
        self.value = value
        self.color_value = color_value
        self.order_value = order_value



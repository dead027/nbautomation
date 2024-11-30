#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2022/11/11 10:50

# 百家乐 投注项名称与bet code对应字典
outcome_dic_baccarat = {
    "庄家": "BJL_BANKER_NO_COMM",
    "庄": "BJL_BANKER_NO_COMM",
    "庄免佣": "BJL_BANKER_NO_COMM",
    "庄家（非免佣）": "BJL_BANKER_COMM",
    "庄（非免佣）": "BJL_BANKER_COMM",
    "闲家": "BJL_PLAYER",
    "闲": "BJL_PLAYER",
    "和局": "BJL_TIE",
    "和": "BJL_TIE",
    "庄对子": "BJL_BANKER_PAIR",
    "庄对": "BJL_BANKER_PAIR",
    "闲对子": "BJL_PLAYER_PAIR",
    "闲对": "BJL_PLAYER_PAIR",
    "超级六": "BJL_SUPER_SIX",
    "闲龙宝": "BJL_PLAYER_DRAGON",
    "庄龙宝": "BJL_BANKER_DRAGON",
    "任意对子": "BJL_ANY_PAIR",
    "BJL_ANY_PAIR": "BJL_ANY_PAIR",
    "完美对子": "BJL_PERFECT_PAIR",
    "超级对": "BJL_SUPER_PAIR",
    "熊猫八": "BJL_PANDA_8",
    "熊猫8": "BJL_PANDA_8",
    "龙七": "BJL_DRAGON_7",
    "龙7": "BJL_DRAGON_7",
    "超和零": "BJL_SUPER_TIE_0",
    "超和(0)": "BJL_SUPER_TIE_0",
    "超和一": "BJL_SUPER_TIE_1",
    "超和(1)": "BJL_SUPER_TIE_1",
    "超和二": "BJL_SUPER_TIE_2",
    "超和(2)": "BJL_SUPER_TIE_2",
    "超和三": "BJL_SUPER_TIE_3",
    "超和(3)": "BJL_SUPER_TIE_3",
    "超和四": "BJL_SUPER_TIE_4",
    "超和(4)": "BJL_SUPER_TIE_4",
    "超和五": "BJL_SUPER_TIE_5",
    "超和(5)": "BJL_SUPER_TIE_5",
    "超和六": "BJL_SUPER_TIE_6",
    "超和(6)": "BJL_SUPER_TIE_6",
    "超和七": "BJL_SUPER_TIE_7",
    "超和(7)": "BJL_SUPER_TIE_7",
    "超和八": "BJL_SUPER_TIE_8",
    "超和(8)": "BJL_SUPER_TIE_8",
    "超和九": "BJL_SUPER_TIE_9",
    "超和(9)": "BJL_SUPER_TIE_9",
    "老虎和": "BJL_TIGER_TIE",
    "大老虎": "BJL_TIGER_BIG",
    "小老虎": "BJL_TIGER_SMALL",
    "老虎对": "BJL_TIGER_PAIR",
    "闲天牌": "BJL_PLAYER_SKY_CARD",
    "庄天牌": "BJL_BANKER_SKY_CARD",
    "天牌": "BJL_SKY_CARD",
    "虎": "BJL_TIGER",
    "龙": "BJL_DRAGON",
    "龙虎和": "BJL_DRAGON_TIGER_TIE",
}
outcome_dic_baccarat_reverse = dict([(item[1], item[0]) for item in outcome_dic_baccarat.items()])

# 龙虎 投注项名称与bet code对应字典
outcome_dic_dt = {
    "龙": "LH_DRAGON",
    "虎": "LH_TIGER",
    "和": "LH_TIE"
}
outcome_dic_dt_reverse = dict([(item[1], item[0]) for item in outcome_dic_dt.items()])

# 牛牛 投注项名称与bet code对应字典
outcome_dic_cattle = {
    "闲1庄平倍": "P1_BANKER_EQUAL",
    "闲1庄翻倍": "P1_BANKER_DOUBLE",
    "闲1庄超倍": "P1_BANKER_SUPER",
    "闲2庄平倍": "P2_BANKER_EQUAL",
    "闲2庄翻倍": "P2_BANKER_DOUBLE",
    "闲2庄超倍": "P2_BANKER_SUPER",
    "闲3庄平倍": "P3_BANKER_EQUAL",
    "闲3庄翻倍": "P3_BANKER_DOUBLE",
    "闲3庄超倍": "P3_BANKER_SUPER",
    "闲1闲平倍": "P1_PLAYER_EQUAL",
    "闲1闲翻倍": "P1_PLAYER_DOUBLE",
    "闲1闲超倍": "P1_PLAYER_SUPER",
    "闲2闲平倍": "P2_PLAYER_EQUAL",
    "闲2闲翻倍": "P2_PLAYER_DOUBLE",
    "闲2闲超倍": "P2_PLAYER_SUPER",
    "闲3闲平倍": "P3_PLAYER_EQUAL",
    "闲3闲翻倍": "P3_PLAYER_DOUBLE",
    "闲3闲超倍": "P3_PLAYER_SUPER",
}
outcome_dic_cattle_reverse = dict([(item[1], item[0]) for item in outcome_dic_cattle.items()])

# 三公 投注项名称与bet code对应字典
outcome_dic_tg = {
    "闲1庄平倍": "P1_BANKER_EQUAL",
    "闲1庄翻倍": "P1_BANKER_DOUBLE",
    "闲1庄超倍": "P1_BANKER_SUPER",
    "闲2庄平倍": "P2_BANKER_EQUAL",
    "闲2庄翻倍": "P2_BANKER_DOUBLE",
    "闲2庄超倍": "P2_BANKER_SUPER",
    "闲3庄平倍": "P3_BANKER_EQUAL",
    "闲3庄翻倍": "P3_BANKER_DOUBLE",
    "闲3庄超倍": "P3_BANKER_SUPER",
    "闲1闲平倍": "P1_PLAYER_EQUAL",
    "闲1闲翻倍": "P1_PLAYER_DOUBLE",
    "闲1闲超倍": "P1_PLAYER_SUPER",
    "闲2闲平倍": "P2_PLAYER_EQUAL",
    "闲2闲翻倍": "P2_PLAYER_DOUBLE",
    "闲2闲超倍": "P2_PLAYER_SUPER",
    "闲3闲平倍": "P3_PLAYER_EQUAL",
    "闲3闲翻倍": "P3_PLAYER_DOUBLE",
    "闲3闲超倍": "P3_PLAYER_SUPER",
}
outcome_dic_tg_reverse = dict([(item[1], item[0]) for item in outcome_dic_tg.items()])

# 龙凤炸金花 投注项名称与bet code对应字典
outcome_dic_gold_flower = {"龙": "GF_DRAGON", "凤": "GF_PHOENIX", "豹子": "GF_THREE_KIND", "同花顺": "GF_STRAIGHT_FLUSH",
                           "同花": "GF_FLUSH", "顺子": "GF_STRAIGHT", "对8以上": "GF_PAIR_8_ABOVE"}
outcome_dic_gold_flower_reverse = dict([(item[1], item[0]) for item in outcome_dic_gold_flower.items()])

# 印度炸金花 投注项名称与bet code对应字典
outcome_dic_india_gold_flower = {"A": "IGF_A_WIN", "B": "IGF_B_WIN", "和": "IGF_TIE", "A对+": "IGF_A_PAYOUT_ABOVE",
                                 "B对+": "IGF_B_PAYOUT_ABOVE", "红利六": "IGF_BONUS_SIX"}
outcome_dic_india_gold_flower_reverse = dict([(item[1], item[0]) for item in outcome_dic_india_gold_flower.items()])

# 德州扑克 投注项名称与bet code对应字典
outcome_dic_dz_poker = {"闲1AA边注": "P1_WIN_BLOCK_SIDE", "闲1底注": "P1_WIN_BLOCK_BASE",
                        "闲1跟注": "P1_WIN_BLOCK_ADDITION", "闲2AA边注": "P2_WIN_BLOCK_SIDE",
                        "闲2底注": "P2_WIN_BLOCK_BASE", "闲2跟注": "P2_WIN_BLOCK_ADDITION"}
outcome_dic_dz_poker_reverse = dict([(item[1], item[0]) for item in outcome_dic_dz_poker.items()])

# 骰宝
outcome_dic_sic_bo = {"大": "SB_BIG", "小": "SB_SMALL", "单": "SB_ODD", "双": "SB_EVEN", "单点1": "SB_TUO_1",
                      "单点2": "SB_TUO_2", "单点3": "SB_TUO_3", "单点4": "SB_TUO_4", "单点5": "SB_TUO_5",
                      "单点6": "SB_TUO_6", "和值4": "SB_4", "和值5": "SB_5", "和值6": "SB_6", "和值7": "SB_7",
                      "和值8": "SB_8", "和值9": "SB_9", "和值10": "SB_10", "和值11": "SB_11", "和值12": "SB_12",
                      "和值13": "SB_13", "和值14": "SB_14", "和值15": "SB_15", "和值16": "SB_16", "和值17": "SB_17",
                      "牌九式12": "SB_1_2", "牌九式13": "SB_1_3", "牌九式14": "SB_1_4", "牌九式15": "SB_1_5",
                      "牌九式16": "SB_1_6", "牌九式23": "SB_2_3", "牌九式24": "SB_2_4", "牌九式25": "SB_2_5",
                      "牌九式26": "SB_2_6", "牌九式34": "SB_3_4", "牌九式35": "SB_3_5", "牌九式36": "SB_3_6",
                      "牌九式45": "SB_4_5", "牌九式46": "SB_4_6", "牌九式56": "SB_5_6",
                      "对子1": "SB_1_1", "对子2": "SB_2_2", "对子3": "SB_3_3", "对子4": "SB_4_4", "对子5": "SB_5_5",
                      "对子6": "SB_6_6", "全围": "SB_ALL_WEI", "围骰1": "SB_1_1_1", "围骰2": "SB_2_2_2",
                      "围骰3": "SB_3_3_3", "围骰4": "SB_4_4_4", "围骰5": "SB_5_5_5", "围骰6": "SB_6_6_6"}
outcome_dic_sic_bo_reverse = dict([(item[1], item[0]) for item in outcome_dic_sic_bo.items()])

# 番摊
outcome_dic_ft = {
    "单": "FT_DAN", "双": "FT_SHUANG",
    "1番": "FT_FAN_1", "2番": "FT_FAN_2", "3番": "FT_FAN_3", "4番": "FT_FAN_4",
    "1念2": "FT_NIAN_1_2", "1念3": "FT_NIAN_1_3", "1念4": "FT_NIAN_1_4",
    "2念1": "FT_NIAN_2_1", "2念3": "FT_NIAN_2_3", "2念4": "FT_NIAN_2_4",
    "3念1": "FT_NIAN_3_1", "3念2": "FT_NIAN_3_2", "3念4": "FT_NIAN_3_4",
    "4念1": "FT_NIAN_4_1", "4念2": "FT_NIAN_4_2", "4念3": "FT_NIAN_4_3",
    "1.2角": "FT_JIAO_1_2", "2.3角": "FT_JIAO_2_3", "3.4角": "FT_JIAO_3_4", "4.1角": "FT_JIAO_4_1",
    "2.3一通": "FT_TONG_1_2_3", "2.4一通": "FT_TONG_1_2_4", "3.4一通": "FT_TONG_1_3_4",
    "1.3二通": "FT_TONG_2_1_3", "1.4二通": "FT_TONG_2_1_4", "3.4二通": "FT_TONG_2_3_4",
    "1.2三通": "FT_TONG_3_1_2", "1.4三通": "FT_TONG_3_1_4", "2.4三通": "FT_TONG_3_2_4",
    "1.2四通": "FT_TONG_4_1_2", "1.3四通": "FT_TONG_4_1_3", "2.3四通": "FT_TONG_4_2_3",
    "三门432": "FT_MEN_4_3_2", "三门143": "FT_MEN_1_4_3", "三门214": "FT_MEN_2_1_4", "三门321": "FT_MEN_3_2_1"
}
outcome_dic_ft_reverse = dict([(item[1], item[0]) for item in outcome_dic_ft.items()])

# 色碟
outcome_dic_cd = {"0": "CD_RED_0", "1": "CD_RED_1", "3": "CD_RED_3", "4": "CD_RED_4", "大": "CD_BIG", "小": "CD_SMALL",
                  "单": "CD_DAN", "双": "CD_SHUANG"}
outcome_dic_cd_reverse = dict([(item[1], item[0]) for item in outcome_dic_cd.items()])

# 轮盘 ---------- start ---------------
# 法式轮盘列表
roulette_number_list = [12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24,
                        16, 33, 1, 20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
outcome_dic_roulette = {"大": "BIG", "小": "SMALL", "单": "DAN", "双": "SHUANG", "红": "RED", "黑": "BLACK",
                        "第一列": "LIST_BET_1", "第二列": "LIST_BET_2", "第三列": "LIST_BET_3", "第一打": "DOZEN_BET_1",
                        "第二打": "DOZEN_BET_2", "第三打": "DOZEN_BET_3", "分注0_1": "SEPARATE_BET_0_1",
                        "分注0_2": "SEPARATE_BET_0_2", "分注0_3": "SEPARATE_BET_0_3", "三数_0_1_2": "THREE_BET_0_1_2",
                        "三数_0_2_3": "THREE_BET_0_2_3", "四号": "FOUR_BET"}

# 直注
direct_bet_dic = {f'直注_{index}': f'DIRECT_BET_{index}' for index in range(37)}
direct_bet_dic_reverse = dict([(item[1], item[0]) for item in direct_bet_dic.items()])
outcome_dic_roulette.update(direct_bet_dic)
# [outcome_dic_roulette.update({f'直注_{index}': f'DIRECT_BET_{index}'}) for index in range(37)]

# 角注
for row in range(1, 32, 3):
    outcome_dic_roulette.update({f"角注_{row}_{row + 1}_{row + 3}_{row + 4}": f"HORN_BET_{row}_{row + 1}_"
                                                                            f"{row + 3}_{row + 4}"})
    outcome_dic_roulette.update({f"角注_{row + 1}_{row + 2}_{row + 4}_{row + 5}": f"HORN_BET_{row + 1}_"
                                                                                f"{row + 2}_{row + 4}_{row + 5}"})

for row in range(1, 35):
    # 分注
    if row != 34:
        # 竖分注
        if row % 3 == 1:
            outcome_dic_roulette.update({f"分注_{row}_{row + 1}": f"SEPARATE_BET_{row}_{row + 1}"})
        elif row % 3 == 2:
            outcome_dic_roulette.update({f"分注_{row}_{row + 1}": f"SEPARATE_BET_{row}_{row + 1}"})
            outcome_dic_roulette.update({f"分注_{row - 1}_{row}": f"SEPARATE_BET_{row - 1}_{row}"})
        else:
            outcome_dic_roulette.update({f"分注_{row - 1}_{row}": f"SEPARATE_BET_{row - 1}_{row}"})
        # 横向
        outcome_dic_roulette.update({f"分注_{row}_{row + 3}": f"SEPARATE_BET_{row}_{row + 3}"})
        outcome_dic_roulette.update({f"分注_{row + 1}_{row + 4}": f"SEPARATE_BET_{row + 1}_{row + 4}"})
        outcome_dic_roulette.update({f"分注_{row + 2}_{row + 5}": f"SEPARATE_BET_{row + 2}_{row + 5}"})
        # 法式额外分注
        outcome_dic_roulette.update({'分注_0_3': 'SEPARATE_BET_0_3'})
    # 街注
    outcome_dic_roulette.update({f"街注_{row}_{row + 1}_{row + 2}": f"STREET_BET_{row}_{row + 1}_{row + 2}"})

# 线注
for row in range(1, 32, 3):
    outcome_dic_roulette[f"线注_{row}_{row + 1}_{row + 2}_{row + 3}_{row + 4}_{row + 5}"] = \
        f"WIRE_BET_{row}_{row + 1}_{row + 2}_{row + 3}_{row + 4}_{row + 5}"
outcome_dic_roulette_reverse = dict([(item[1], item[0]) for item in outcome_dic_roulette.items()])

# 法式 - 相邻投注
for num in range(0, 37):
    current_index = roulette_number_list.index(num) if num in (3, 26) and num not in (12, 35) else \
        roulette_number_list.index(num, 2)
    outcome_dic_roulette[f"相邻投注_{num}"] = {f"DIRECT_BET_{roulette_number_list[current_index - 2]}": 1,
                                           f"DIRECT_BET_{roulette_number_list[current_index - 1]}": 1,
                                           f"DIRECT_BET_{roulette_number_list[current_index]}": 1,
                                           f"DIRECT_BET_{roulette_number_list[current_index + 1]}": 1,
                                           f"DIRECT_BET_{roulette_number_list[current_index + 2]}": 1}

# 法式-轮上零旁
outcome_dic_roulette.update({"轮上零旁": {"SEPARATE_BET_0_3": 1, "SEPARATE_BET_12_15": 1, "SEPARATE_BET_32_35": 1,
                                      "DIRECT_BET_26": 1}})
# 法式-零旁注上角
outcome_dic_roulette.update({"零旁注上角": {"SEPARATE_BET_4_7": 1, "SEPARATE_BET_12_15": 1, "SEPARATE_BET_18_21": 1,
                                       "SEPARATE_BET_19_22": 1, "SEPARATE_BET_32_35": 1, "THREE_BET_0_2_3": 2,
                                       "HORN_BET_25_26_28_29": 2}})
# 法式-轮上孤注
outcome_dic_roulette.update({"轮上孤注": {"SEPARATE_BET_6_9": 1, "DIRECT_BET_1": 1, "SEPARATE_BET_31_34": 1,
                                      "SEPARATE_BET_17_20": 1, "SEPARATE_BET_14_17": 1}})
# 法式-轮盘下角注
outcome_dic_roulette.update({"轮盘下角注": {"SEPARATE_BET_5_8": 1, "SEPARATE_BET_10_11": 1, "SEPARATE_BET_13_16": 1,
                                       "SEPARATE_BET_23_24": 1, "SEPARATE_BET_27_30": 1, "SEPARATE_BET_33_36": 1}})
# 轮盘 ---------- END ---------------

game_category_type_dic = {}

# 牌型
number_dic = {str(item): item for item in range(1, 11)}
number_dic.update({"10": 0, "J": 0, "Q": 0, "K": 0, "A": 1})
# 自然数
value_order_base_dic = {str(item): item for item in range(2, 11)}
value_order_dic = {"K": 13, "Q": 12, "J": 11, "A": 1}
value_order_dic.update(value_order_base_dic)
# color_dic = {"1": "♠️", "2": "♥️", "3": "♣️", "4": "♦️"}
# 黑桃为1，最大
color_dic = {"黑桃": 1, "红心": 2, "梅花": 3, "方块": 4}
order_value_dic = dict([(item[1], item[0]) for item in value_order_dic.items()])
order_status_dic = {"未结算": 0, "已结算": 1, "取消局": 2, "重算局": 3}
game_type_dic = {"极速百家乐": 1, "经典百家乐": 2, "牛牛": 3, "龙虎": 4, "三公": 5, "龙凤炸金花": 6, "印度炸金花": 7,
                 "德州扑克": 8, "新炸金花": 12, "劲舞百家乐": 13, "色碟": 14, "轮盘": 15, "番摊": 16, "骰宝": 17}
game_code_type_dic = {"BJL_SPEED": 1, "BJL_CLASSIC": 2, "BULL": 3, "DT": 4, "SAN_GONG": 5, "GOLDEN_FLOWER": 6,
                      "COLOR_DISH": 14, "ROULETTE": 15, "FT": 16, "SICBO": 17}
type_game_dic = dict([(item[1], item[0]) for item in game_type_dic.items()])
game_status_dic = {"下注中": 1, "开牌中": 2, "结算中": 3, "已结算": 4, "跳局": 5, "取消局": 6, "重算局": 7}
abnormal_mark_dic = {"正常": 0, "重算": 1, "取消": 2, "跳局": 3}
status_abnormal_dic = dict([(item[1], item[0]) for item in abnormal_mark_dic.items()])
game_type_code_dic = {"经典百家乐": "BJL_CLASSIC", "极速百家乐": "BJL_SPEED", "牛牛": "BULL", "三公": "SAN_GONG",
                      "龙虎": "DT", "龙凤炸金花": "GOLDEN_FLOWER", "印度炸金花": "INDIA_GOLDEN_FLOWER", "德州扑克": "Texas",
                      "炸金花": "THREE_CARD_POKER", "色碟": "COLOR_DISH" , "轮盘": "ROULETTE", "骰宝": "SICBO", "番摊": "FT"}
boot_change_queue_name_dic = {"百家乐": "baccarat_change_boots", "三公": "sangong_change_boot",
                              "牛牛": "bull_change_boot", "龙虎": "dt_change_boots",
                              "龙凤炸金花": "golden_flower_change_boot", "德州扑克": "texas_hold_change_boot",
                              "印度炸金花": "india_golden_flower_change_boot", "新炸金花": "three_card_poker_change_boot",
                              "色碟": "color_dish_change_boot", "轮盘": "roulette_open_or_end_game",
                              "骰宝": "sicbo_change_boot", "番摊": "ft_change_boot"}
open_end_queue_dic = {"百家乐": "baccarat_open_or_end_game", "三公": "sangong_open_or_end_game",
                      "牛牛": "bull_open_or_end_game", "龙虎": "dt_open_or_end_game",
                      "龙凤炸金花": "golden_flower_open_or_end_game", "德州扑克": "texas_hold_open_or_end_game",
                      "印度炸金花": "india_golden_flower_open_or_end_game", "新炸金花": "three_card_poker_open_or_end_game",
                      "色碟": "color_dish_open_or_end_game", "轮盘": "roulette_open_or_end_game",
                      "骰宝": "sicbo_open_or_end_game", "番摊": "ft_open_or_end_game"}
identify_cart_queue_dic = {"百家乐": "baccarat_identify_card", "三公": "sangong_identify_card",
                           "牛牛": "bull_identify_card", "龙虎": "dt_identify_card",
                           "龙凤炸金花": "golden_flower_identify_card", "德州扑克": "texas_hold_identify_card",
                           "印度炸金花": "india_golden_flower_identify_card", "新炸金花": "three_card_poker_identify_card",
                           "轮盘": "roulette_identify_card", "骰宝": "sicbo_identify_card",
                           "番摊": "ft_identify_card"}
# 德州扑克跟注阶段
dz_poker_addition_period_queue = 'texas_hold_addition'

# 账变类型
order_change_type_dic = {"转入": 1, "转出": 2, "投注": 3, "结算": 4, "下注取消": 5, "结算回滚": 6, "二次结算": 7, "打赏": 8,
                         "优惠": 9}
order_change_type_reverse_dic = dict([(item[1], item[0]) for item in order_change_type_dic.items()])
# 收支类型
balance_type_dic = {1: "收入", 2: "支出"}
balance_type_reverse_dic = dict([(item[1], item[0]) for item in balance_type_dic.items()])
# 代理业务类型
agent_business_dic = {"代理存款": 1, "代理代存": 2, "代理提款": 3, "代理转账": 4, "优惠": 5}
agent_business_dic_reverse = dict([(item[1], item[0]) for item in agent_business_dic.items()])
# 代理账变类型
agent_change_type_dic = {"代理存款(后台)": 1, "代理提款(后台)": 2, "代理存款": 3, "代理提款": 4, "转给下级会员": 5,
                         "转给下级代理": 6, "上级转入": 7, "返水": 8, "提款失败": 99}
agent_change_type_dic_reverse = dict([(item[1], item[0]) for item in agent_change_type_dic.items()])
# 交易来源
change_resource_dic = dict(zip(range(1, 13), ("会员存款", "会员提款", "下注", "结算", "取消", "结算取消", "打赏",
                                              "会员存款（后台）", "会员提款（后台）", "代理代存", "提款失败", "返水")))
change_resource_dic_reverse = dict([(item[1], item[0]) for item in change_resource_dic.items()])

currency_dic = {"人民币": 1, "美元": 2}
player_password = "abcd1234"

# 第三方商户给我司分配的信息： merchant_id, key
third_merchant_info_dic = {"yidian": [40033, 'B2OJQPexYXKrWVPKBeXotil4FOncrcQh']}

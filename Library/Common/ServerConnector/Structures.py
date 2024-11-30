#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2023/9/15 16:02
from copy import deepcopy

venue_platform_dic = {"神话视讯": "SH", "WE游戏": "WE", "开元游戏": "KY", "LEG游戏": "LEG", "小艾电竞": "IA"}
venue_code_dic = deepcopy(venue_platform_dic)

order_info_struct = dict.fromkeys(["userAccount", "userName", "accountType", "casinoUserName", "vipRankCode",
                                   "venuePlatform", "venueName", "venueCode", "gameType", "gameName", "playType",
                                   "betTime", "settleTime", "reSettleTime", "betAmount", "validAmount", "payoutAmount",
                                   "winLossAmount", "orderId", "thirdOrderId", "orderStatus", "orderClassify",
                                   "gameNo", "deskNo", "bootNo", "resultList", "betContent", "rebateRate",
                                   "rebateAmount", "changeStatus", "betIp", "currency", "diviceType", "createdTime",
                                   "changeTime", "updatedTime", "gameCode", "parlayInfo", "roomType",
                                   "firstSettleTime", "resultTime"])


class UserInfo(object):
    def __init__(self, user_id, user_account, user_name, gender, birthday, phone, email, account_type, account_status,
                 risk_level_id, first_deposit_time, first_deposit_amount, last_login_time, last_login_ip,
                 offline_days, register_time, member_domain, register_ip, registry, super_agent_id,
                 super_agent_account, binding_agent_time, user_label_id, trans_agent_time, vip_rank_code, vip_rank_up,
                 withdraw_pwd, account_remark, device_control_id, last_device_no, creator, created_time,
                 updater, updated_time, wallet_address):
        self.user_id = user_id
        self.user_account = user_account
        self.user_name = user_name
        self.gender = gender
        self.birthday = birthday
        self.phone = phone
        self.email = email
        self.account_type = account_type
        self.account_status = account_status
        self.risk_level_id = risk_level_id
        self.first_deposit_time = first_deposit_time
        self.first_deposit_amount = first_deposit_amount
        self.last_login_time = last_login_time
        self.last_login_ip = last_login_ip
        self.offline_days = offline_days
        self.register_time = register_time
        self.member_domain = member_domain
        self.register_ip = register_ip
        self.registry = registry
        self.super_agent_id = super_agent_id
        self.super_agent_account = super_agent_account
        self.binding_agent_time = binding_agent_time
        self.user_label_id = user_label_id
        self.trans_agent_time = trans_agent_time
        self.vip_rank_code = vip_rank_code
        self.vip_rank_up = vip_rank_up
        self.withdraw_pwd = withdraw_pwd
        self.account_remark = account_remark
        self.device_control_id = device_control_id
        self.last_device_no = last_device_no
        self.creator = creator
        self.created_time = created_time
        self.updater = updater
        self.updated_time = updated_time
        self.wallet_address = wallet_address
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 服务器类型
class ServerStruct(object):
    def __init__(self, ip, port="", user_name="", password="", db_name="", auth_db=""):
        self.ip = ip
        self.port = port
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.auth_db = auth_db
        self.json = deepcopy(self.__dict__)


# 场馆类型
class VenueStruct(object):
    def __init__(self, venue_code, venue_name, venue_platform, venue_proportion, wallet_name,
                 status):
        self.venue_code = venue_code
        self.venue_name = venue_name
        self.venue_platform = venue_platform
        self.venue_proportion = venue_proportion
        self.wallet_name = wallet_name
        self.status = status
        self.json = deepcopy(self.__dict__)


class AgentInfo(object):
    def __init__(self, agent_id=None, name=None, gender=None, birthday=None, phone=None, email=None, qq=None,
                 telegram=None, parent_id=None, path=None, level=None, max_level=None,
                 agent_account=None, agent_type=None, contract_model_commission=None, contract_model_rebate=None,
                 status=None, contract_status=None, entrance_perm=None, force_contract_effect=None,
                 remove_recharge_limit=None, register_way=None,
                 register_device_type=None, register_time=None, register_ip=None, last_login_time=None,
                 offline_days=None, invite_code=None,
                 agent_label_id=None, risk_level_id=None, is_agent_arrears=None, wallet_address=None, remark=None):
        self.agent_id = agent_id
        self.name = name
        self.gender = gender
        self.birthday = birthday
        self.phone = phone
        self.email = email
        self.qq = qq
        self.telegram = telegram
        self.parent_id = parent_id
        self.path = path
        self.level = level
        self.max_level = max_level
        self.agent_account = agent_account
        self.agent_type = agent_type
        self.contract_model_commission = contract_model_commission
        self.contract_model_rebate = contract_model_rebate
        self.status = status
        self.contract_status = contract_status
        self.entrance_perm = entrance_perm
        self.force_contract_effect = force_contract_effect
        self.remove_recharge_limit = remove_recharge_limit
        self.register_way = register_way
        self.register_device_type = register_device_type
        self.register_time = register_time
        self.register_ip = register_ip
        self.last_login_time = last_login_time
        self.offline_days = offline_days
        self.invite_code = invite_code
        self.agent_label_id = agent_label_id
        self.risk_level_id = risk_level_id
        self.is_agent_arrears = is_agent_arrears
        self.wallet_address = wallet_address
        self.remark = remark
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


# 佣金按月统计信息
class CommissionMonthRecordInfo(object):
    def __init__(self, agent_account, report_day, status, user_win_loss, venue_fee, discount_amount, rebate_amount,
                 adjust_amount, patch_amount, point_amount, agent_win_loss, last_month_remain, total_win_loss,
                 agent_rate, commission_amount, team_commission, sub_commission, my_commission, adjust_commission,
                 current_month_remain):
        self.agent_account = agent_account
        self.report_day = report_day
        self.status = status
        self.user_win_loss = user_win_loss
        self.venue_fee = venue_fee
        self.discount_amount = discount_amount
        self.rebate_amount = rebate_amount
        self.adjust_amount = adjust_amount
        self.patch_amount = patch_amount
        self.point_amount = point_amount
        self.agent_win_loss = agent_win_loss
        self.last_month_remain = last_month_remain
        self.agent_account = agent_account
        self.total_win_loss = total_win_loss
        self.agent_rate = agent_rate
        self.team_commission = team_commission
        self.status = status
        self.commission_amount = commission_amount
        self.sub_commission = sub_commission
        self.my_commission = my_commission
        self.adjust_commission = adjust_commission
        self.current_month_remain = current_month_remain
        self.json = deepcopy(self.__dict__)

    def reload_json(self):
        self.json = deepcopy(self.__dict__)
        self.json.pop("json")


if __name__ == "__main__":
    agent = AgentInfo()
    agent.reload_json()

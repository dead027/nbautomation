#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: yaoxing
# datetime: 2024/9/10 16:55
from Library.MysqlTableModel.agent_login_record_model import AgentLoginRecord
from Library.MysqlTableModel.agent_info_model import AgentInfo

from Library.Dao import Dao
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.functions import func

from Library.Common.Utils.DateUtil import DateUtil


class AgentDetailPage(object):
    @staticmethod
    def get_agent_login_record_vo(site_code, agent_account):
        """
        代理详情  - 登录信息
        @return:
        """
        data = Dao.get_agent_login_info(site_code, agent_account)
        result_list = []
        login_status_dic = Dao.get_user_login_status(to_zh=True)
        login_device_dic = Dao.get_device(to_zh=True)
        for item in data:
            item: AgentLoginRecord
            sub_data = {"登录时间": DateUtil.timestamp_to_time(item.login_time),
                        "状态": login_status_dic[item.login_status], "IP地址&风控层级": item.login_ip + item.ip_control_id,
                        "IP归属地": item.ip_attribution, "登录网址": item.login_address,
                        "登录终端": login_device_dic[item.login_device],
                        "设备号&风控层级": item.device_number + item.device_control_id,
                        "设备版本": item.device_version}
            result_list.append(sub_data)
        return result_list

    @staticmethod
    def get_agent_base_info_vo(site_code, agent_account):
        """
        获取代理基本信息
        @return:
        """
        agent_info: AgentInfo = Dao.get_agent_info(site_code, agent_account)
        label_data = Dao.get_agent_label_info(site_code)
        label_dic = {_.id: _.name for _ in label_data}

        data = {"代理账号": agent_account, "账号状态": Dao.get_agent_status(to_zh=True)[agent_info.status],
                "风控层级": agent_info.risk_level_id,
                "代理标签": ','.join([label_dic[_] for _ in agent_info.agent_label_id.split(",")]),
                "合营代码": agent_info.invite_code,
                "直属上级": agent_info.parent_id, "代理层级": agent_info.level,
                "代理类型": Dao.get_agent_type(to_zh=True)[agent_info.agent_type],
                "代理归属": Dao.get_agent_belong(to_zh=True)[agent_info.agent_attribution],
                "代理类别": Dao.get_agent_belong(to_zh=True)[agent_info.agent_category],
                "佣金方案": "", "会员福利": "", "入口权限": "开启" if agent_info.entrance_perm == 1 else "关闭",
                "充值限制": "", "离线天数": "",
                "IP白名单": agent_info.agent_white_list,
                "注册时间": DateUtil.timestamp_to_time(agent_info.register_time),
                "注册端": "", "注册IP": agent_info.register_ip,
                "最后登录时间": DateUtil.timestamp_to_time(agent_info.last_login_time) if agent_info.last_login_time else "",
                "姓名": agent_info.name, "性别": Dao.get_sex(agent_info.gender),
                "出生日期": DateUtil.timestamp_to_time(agent_info.birthday) if agent_info.birthday else "",
                "手机号码": agent_info.phone, "邮箱": agent_info.email, "QQ": agent_info.qq,
                "Telegram": agent_info.telegram, "支付密码": "-"}
        return data

    @staticmethod
    def get_team_info_vo(site_code, agent_account):
        agent_info: AgentInfo = Dao.get_agent_info(site_code, agent_account)
        sub_agent_data = Dao.get_sub_agent_list()
        sub_user_data = Dao.get_users_of_agent(site_code)[agent_account]

        data = {"下级代理人数": len(sub_agent_data[agent_account]["团队不包括自己"]),
                "直属代理人数": len(sub_agent_data[agent_account]["直属"]),
                "下级会员人数": len(sub_user_data["团队不包括自己"]),
                "直属会员人数": len(sub_user_data["直属"]),
                "首存人数": agent_info.invite_code,
                "首存金额": agent_info.parent_id, "有效会员": "",
                "今日新增": Dao.get_new_user_count_sql(site_code, date_type='日')[agent_account],
                "今日活跃人数": Dao.get_valid_user_amount(site_code, date_type='日')[agent_account],
                "今日新增活跃人数": Dao.get_new_valid_user_amount(site_code, date_type='日')[agent_account],
                "今日有效活跃人数": Dao.get_valid_user_amount(site_code, date_type='日', valid_type='有效活跃')[agent_account],
                "今日新增有效活跃人数": Dao.get_new_valid_user_amount(site_code, date_type='日', valid_type='有效活跃')[agent_account],
                "本月新增": Dao.get_new_user_count_sql(site_code)[agent_account],
                "本月活跃人数": Dao.get_valid_user_amount(site_code)[agent_account],
                "本月新增活跃人数": Dao.get_new_valid_user_amount(site_code)[agent_account],
                "本月有效活跃人数": Dao.get_valid_user_amount(site_code, valid_type='有效活跃')[agent_account],
                "本月新增有效活跃人数": Dao.get_new_valid_user_amount(site_code, valid_type='有效活跃')[agent_account],
                "今日优惠": "", "今日返水": agent_info.register_ip,
                "今日净输赢": DateUtil.timestamp_to_time(agent_info.last_login_time) if agent_info.last_login_time else "",
                "今日总投注": agent_info.name, "今日总有效投注": Dao.get_sex(agent_info.gender),
                "今日总输赢": DateUtil.timestamp_to_time(agent_info.birthday) if agent_info.birthday else "",
                "本月优惠": agent_info.phone, "本月返水": agent_info.email, "本月净输赢": agent_info.qq,
                "本月总投注": agent_info.telegram, "本月总有效投注": "-", "本月总输赢": ""}
        return data

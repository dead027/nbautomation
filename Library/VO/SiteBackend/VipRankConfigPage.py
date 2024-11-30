# from Library.Common.Utils.Contexts import *
# from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Enum.UserEnum import UserEnum
from Library.MysqlTableModel.site_vip_rank_currency_config_model import SiteVipRankCurrencyConfig
from Library.MysqlTableModel.site_vip_rank_model import SiteVipRank
from Library.Common.Utils.DateUtil import DateUtil
from Library.Common.Utils.YamlUtil import YamlUtil
from Library.Common.Utils.HttpRequestUtil import HttpRequestUtil
# from Library.Common.Enum.UserEnum import UserEnum
# from Library.Common.Enum.FundsEnum import *
from Library.Dao import Dao
# from sqlalchemy.orm.session import Session
# from sqlalchemy.sql.functions import func


class VipRankConfigPage(object):

    @staticmethod
    def get_vip_rank_config_list_api(site_code):
        """
        获取vip段位列表
        @return:
        """
        result = Dao.get_user_vip_rank_config_sql(site_code)
        result_list = []
        for data_1, data_2 in result:
            data_1: SiteVipRank
            data_2: SiteVipRankCurrencyConfig
            sub_data = {"段位名称": data_1.vip_rank_name, "单日提现次数": data_2.daily_withdrawals,
                        "单日提款上限": data_2.day_withdraw_limit, "提款手续费": data_2.withdraw_fee,
                        "VIP等级": data_1.vip_grade_codes, "备注": data_1.remark}
            result_list.append(sub_data)
        return result_list
    """
    @staticmethod
    def get_user_vip_rank_config_list_aip():
        url = YamlUtil.get_backend_host() + '/vip/api/queryVIPRank'
        parser = {"pageNumber": 1, "pageSize": 200}

        resp = HttpRequestUtil.post(url, parser, all_page=True)
        map_dic = {"段位名称": vipRankName, "VIP等级": "vipGradeList", "备注": "remark"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]
    """

    @staticmethod
    def get_vip_level_config_list_api():
        url = YamlUtil.get_backend_host() + '/vip/api/queryGrade'
        parser = {"pageNumber": 1, "pageSize": 200}

        resp = HttpRequestUtil.post(url, parser, all_page=True)
        map_dic = {"VIP等级": "vipGradeName", "所属段位": "vipRankCode", "晋级礼金": "upgradeBonus", "升级条件 所需XP": "upgradeXp"}
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_vip_level_change_api(user_account=None, operator=None, start_diff=0, end_diff=0):
        """
        获取 VIP 等级变更记录
        @return: 返回格式化的 VIP 等级变更记录列表
        """
        # 构造请求 URL
        url = YamlUtil.get_backend_host() + '/vip/changeRecord/queryChangeRecordPage'
        upd_start, upd_end = DateUtil.get_timestamp_range(start_diff, end_diff)
        # 设置请求参数
        parser = {"userAccount": user_account, "operator": operator, "pageNumber": 1, "pageSize": 200,
                  "startTime": upd_start, "endTime": upd_end}
        # 发送 POST 请求并获取所有分页数据
        resp = HttpRequestUtil.post(url, parser, all_page=True)
        # 字段映射，确保从 resp 数据中取出对应的字段
        map_dic = {
            "变更时间": "changeTimeStr", "变更类型": "changeType", "会员账号": "userAccount",
            "账号类型": "accountTypeName",
            "标签": "userLabel", "变更前VIP等级": "beforeChange", "变更后等级": "afterChange",
            "风控层级": "controlRank",
            "账号状态": "accountStatus", "操作人": "operator"
        }
        # 处理API返回的数据，成新的字典列表
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]

    @staticmethod
    def get_user_vip_rank_change_api(user_account=None, operator=None, start_diff=0, end_diff=0):
        """
        获取用户VIP段位变更记录
        @param user_account: 账号
        @param operator: 操作人
        @param start_diff: 开始时间
        @param end_diff: 结束时间
        @return:
        """
        # 构造请求 URL
        url = YamlUtil.get_backend_host() + '/vip/api/queryVIPRankOperation'
        # 时间转换
        upd_start, upd_end = DateUtil.get_timestamp_range(start_diff, end_diff)
        # 设置请求参数
        parser = {"userAccount": user_account, "operator": operator, "pageNumber": 1, "pageSize": 200,
                  "startTime": upd_start, "endTime": upd_end}
        # 发送 POST 请求并获取所有分页数据
        resp = HttpRequestUtil.post(url, parser, all_page=True)
        # 字段映射，确保从 resp 数据中取出对应的字段
        map_dic = {
            "变更时间": "changeTimeStr", "会员账号": "userAccount", "账号类型": "accountTypeName",
            "变更前VIP等级": "beforeChange", "变更后等级": "afterChange", "标签": "userLabel",
            "风控层级": "controlRank",
            "账号状态": "accountStatus", "操作人": "operator"
        }
        # 处理API返回的数据，成新的字典列表
        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]
    """ 
    @staticmethod
    def get_user_list_vo(register_time=None, start_diff=0, end_diff=0, account_type=None, user_id=None, user_account=None,
                         super_agent_ac=None, register_ip=None, main_currency=None,vip_rank=None, vip_grade_code=None,
                         user_level_id=None, registry=None, account_status=""):
        url = YamlUtil.get_backend_host() + ''

        upd_start, upd_end = DateUtil.get_timestamp_range(start_diff, end_diff)
        parser = {"register_time":register_time,"upd_start":upd_start,"upd_end":upd_end,"user_id":user_id,
                  "user_account":user_account, "super_agent_ac":super_agent_ac,"register_ip":register_ip,
                  "main_currency":main_currency, "vip_rank":vip_rank, "vip_grade_code":vip_grade_code,
                  "user_level_id":user_level_id, "registry":registry, "pageNumber": 1, "pageSize": 200}

        if register_time:
            parser["register_time"] = register_time
        if account_type:
            parser["account_type"] = [UserEnum.account_type_dic_t_zh.value[item] for item in account_type.split(",")]
        if main_currency:
            parser["main_currency"] = main_currency
        if vip_rank:
            parser["vip_rank"] = vip_rank
        if vip_grade_code:
            parser["vip_grade_code"] = vip_grade_code
        if registry:
            parser["registry"] = registry
        if account_status:
            parser["account_status"] = [UserEnum.user_status_dic_t_zh.value[item] for item in account_status.split(",")]
        resp = HttpRequestUtil.post(url, parser, all_page=True)
        map_dic = {
            "注册时间": "register_time", "会员ID": "user_id", "账号类型": "account_type", "会员账号": "user_account",
            "钱包余额":"", "主货币": "main_currency","VIP段位":"", "VIP等级": "vip_rank","标签":"", "上级代理": "super_agent_account",
            "账号状态": "account_status", "在线状态":"", "邀请码":"friend_invite_co", "首存金额":"first_deposit_amount",
            "首存时间":"first_deposit_time", "注册IP": "register_ip", "注册IP归属地":"registry", "注册终端":"registry",
            "最后登陆IP":"last_login_ip", "最后登陆时间":"last_login_time"

        }

        return [dict(zip(list(map_dic.keys()), [item[key] for key in map_dic.values()])) for item in resp]"""
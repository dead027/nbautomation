# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipRank(Base):
    __tablename__ = 'site_vip_rank'
    __table_args__ = {'comment': '站点VIP段位配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(30, 'utf8mb4_0900_bin'), comment='站点code')
    vip_rank_code = Column(INTEGER(11), comment='vip段位code')
    vip_rank_name = Column(String(30, 'utf8mb4_0900_bin'), comment='vip段位名称')
    vip_rank_name_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='段位名称-多语言')
    vip_grade_codes = Column(String(200, 'utf8mb4_0900_bin'), comment='支持的vip等级数组')
    vip_icon = Column(String(100, 'utf8mb4_0900_bin'), comment='vip段位图标地址')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    luck_flag = Column(TINYINT(4), comment='转盘是否参与(0:不参与,1:参与)')
    luck = Column(DECIMAL(20, 2), comment='转盘次数')
    week_amount_flag = Column(TINYINT(4), comment='周流水奖励是否参与(0:不参与,1:参与)')
    week_amount_limit = Column(DECIMAL(20, 2), comment='周流水达成条件')
    week_amount_prop1 = Column(DECIMAL(20, 2), comment='周流水奖励比例1')
    week_amount_prop2 = Column(DECIMAL(20, 2), comment='周流水奖励比例2')
    week_amount_multiple = Column(DECIMAL(20, 2), comment='周流水倍数')
    month_amount_flag = Column(TINYINT(4), comment='月流水奖励是否参与(0:不参与,1:参与)')
    month_amount_limit = Column(DECIMAL(20, 2), comment='月流水达成条件')
    month_amount_prop1 = Column(DECIMAL(20, 2), comment='月流水奖励比例1')
    month_amount_prop2 = Column(DECIMAL(20, 2), comment='月流水奖励比例2')
    month_amount_multiple = Column(DECIMAL(20, 2), comment='月流水倍数')
    week_sport_flag = Column(TINYINT(4), comment='是否参加周体育奖励(0:不参与,1:参与)')
    encry_coin_fee = Column(TINYINT(4), comment='是否有加密货币提款手续费(0:没有,1:有)')
    svip_welfare = Column(TINYINT(4), comment='是否有SVIP专属福利(0:没有,1:有)')
    luxurious_gifts = Column(TINYINT(4), comment='是否有豪华赠品(0:没有,1:有)')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

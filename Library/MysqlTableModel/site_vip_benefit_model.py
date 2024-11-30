# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipBenefit(Base):
    __tablename__ = 'site_vip_benefit'
    __table_args__ = {'comment': '站点VIP权益配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    vip_grade_code = Column(TINYINT(4), index=True, comment='VIP等级code')
    vip_grade_name = Column(String(20, 'utf8mb4_0900_bin'), comment='VIP等级名称')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    daily_withdrawals = Column(INTEGER(11), comment='日提款次数')
    day_withdraw_limit = Column(DECIMAL(20, 2), comment='每日累计提款额度')
    week_rebate = Column(DECIMAL(20, 2), comment='每周返还奖金比例')
    week_min_bet_amount = Column(DECIMAL(20, 2), comment='每周下注最低流水')
    week_bet_multiple = Column(DECIMAL(20, 2), comment='周流水倍数')
    month_rebate = Column(DECIMAL(20, 2), comment='每月返还奖金比例')
    month_min_bet_amount = Column(DECIMAL(20, 2), comment='每月下注最低流水')
    month_bet_multiple = Column(DECIMAL(20, 2), comment='每月流水倍数')
    week_sport_min_bet = Column(DECIMAL(20, 2), comment='周体育最低流水')
    week_sport_multiple = Column(DECIMAL(20, 2), comment='周体育倍数')
    week_sport_rebate = Column(DECIMAL(20, 2), comment='周体育奖金')
    upgrade = Column(DECIMAL(20, 2), comment='晋级奖金')
    luck_time = Column(INTEGER(11), comment='转盘次数')
    withdraw_fee = Column(DECIMAL(20, 2), comment='提款手续费')
    creator = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

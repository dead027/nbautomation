# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityDailyRecord(Base):
    __tablename__ = 'site_activity_daily_record'
    __table_args__ = (
        Index('idnex_time', 'site_code', 'venue_code', 'ranking', 'time', unique=True),
        {'comment': '每日竞赛-排名发放记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='venueCode')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='会员id')
    user_account = Column(String(20, 'utf8mb4_0900_bin'), comment='会员账号')
    role = Column(INTEGER(5), comment='0=机器人,1=真实用户')
    ranking = Column(INTEGER(11), comment='排名')
    bet_amount = Column(DECIMAL(20, 2), comment='投注金额')
    award_amount = Column(DECIMAL(20, 2), comment='奖励金额')
    award_percentage = Column(DECIMAL(20, 2), comment='奖励百分比')
    activity_discount_type = Column(INTEGER(11), comment='优惠方式:0:百分比,1:固定金额')
    time = Column(Date, comment='排名发放日期')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityDailyCompetition(Base):
    __tablename__ = 'site_activity_daily_competition'
    __table_args__ = {'comment': '每日竞赛'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    competition_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='多语言竞赛名称')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    activity_id = Column(BIGINT(20), comment='所属活动')
    venue_type = Column(INTEGER(11), comment='场馆类型')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='venueCode')
    init_amount = Column(DECIMAL(20, 2), comment='初始化金额')
    venue_percentage = Column(DECIMAL(20, 2), comment='场馆百分比')
    activity_discount_type = Column(INTEGER(11), comment='优惠方式:0:百分比,1:固定金额')
    activity_detail = Column(String(200, 'utf8mb4_0900_bin'), comment='活动详情配置,存数组')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

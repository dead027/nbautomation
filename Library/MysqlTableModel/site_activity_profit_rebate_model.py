# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityProfitRebate(Base):
    __tablename__ = 'site_activity_profit_rebate'
    __table_args__ = {'comment': '负盈利-返利'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    activity_id = Column(BIGINT(20), comment='所属活动')
    user_type = Column(INTEGER(11), comment='状态 0:全体会员 1:新注册会员')
    register_day = Column(INTEGER(11), comment='注册天数')
    venue_type = Column(INTEGER(11), comment='场馆类型')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='venueCode')
    activity_discount_type = Column(INTEGER(11), comment='优惠方式:0:百分比,1:固定金额')
    activity_detail = Column(String(200, 'utf8mb4_0900_bin'), comment='活动详情配置,存数组')
    calculate_type = Column(String(20, 'utf8mb4_0900_bin'), comment='结算周期,0:日结,1:周结,2:月结')
    participation_mode = Column(INTEGER(11), comment='参与方式,0.手动参与，1.自动参与')
    upper_limit = Column(DECIMAL(20, 2), comment='奖励上限')
    distribution_type = Column(INTEGER(11), comment='派发方式: 0:玩家自领-过期作废，1:玩家自领-过期自动派发，2:立即派发')
    receive_type = Column(INTEGER(11), comment='领取方式: 0:次日领取,1:每日领取')
    receive_date = Column(String(100, 'utf8mb4_0900_bin'), comment='领取时间。0表示周期结束才过期')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

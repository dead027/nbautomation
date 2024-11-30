# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivitySpinWheel(Base):
    __tablename__ = 'site_activity_spin_wheel'
    __table_args__ = {'comment': '转盘活动配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    deposit_times = Column(INTEGER(11), comment='存款奖励次数')
    deposit_amount = Column(DECIMAL(10, 2), comment='存款金额')
    bet_amount = Column(DECIMAL(10, 2), comment='投注流水')
    bet_times = Column(INTEGER(11), comment='投注奖励次数')
    init_amount = Column(DECIMAL(10, 2), comment='转盘初始获得金额')
    max_time_type = Column(INTEGER(11), comment='每日领取次数上限类型：0-全部会员，1-根据VIP等级限制')
    max_times = Column(INTEGER(11), comment='每日领取次数上限（适用于全部会员）')
    base_id = Column(String(20, 'utf8mb4_0900_bin'), comment='活动主键id')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

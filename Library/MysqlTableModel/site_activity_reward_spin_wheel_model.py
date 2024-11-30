# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityRewardSpinWheel(Base):
    __tablename__ = 'site_activity_reward_spin_wheel'
    __table_args__ = {'comment': '转盘活动配置奖励'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    reward_rank = Column(INTEGER(11), comment='奖励段位，青铜，白银，黄金')
    prize_level = Column(INTEGER(11), comment='奖品等级')
    prize_type = Column(String(30, 'utf8mb4_0900_bin'), comment='奖品类型')
    prize_name = Column(String(50, 'utf8mb4_0900_bin'), comment='奖品名称')
    prize_amount = Column(DECIMAL(10, 2), comment='奖品价值')
    prize_picture_url = Column(String(100, 'utf8mb4_0900_bin'), comment='奖品展示图')
    probability = Column(DECIMAL(10, 2), comment='活动概率')
    base_id = Column(BIGINT(20), index=True, comment='活动id')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityLotteryRecord(Base):
    __tablename__ = 'site_activity_lottery_record'
    __table_args__ = (
        Index('index_userId_time', 'user_id', 'created_time'),
        {'comment': '转盘活动抽奖次数记录表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    vip_rank_code = Column(INTEGER(11), comment='vip段位code')
    vip_grade_code = Column(INTEGER(11), comment='VIP等级code')
    prize_source = Column(String(50, 'utf8mb4_0900_bin'), comment='获取来源')
    operation_type = Column(TINYINT(1), comment='操作类型：0表示减少，1表示增加')
    start_count = Column(INTEGER(11), comment='原次数')
    reward_count = Column(INTEGER(11), comment='获取次数')
    end_count = Column(INTEGER(11), comment='获取后次数')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='会员id')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='会员账号')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    order_number = Column(String(64, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='奖励订单号')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

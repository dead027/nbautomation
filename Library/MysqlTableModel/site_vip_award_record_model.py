# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipAwardRecord(Base):
    __tablename__ = 'site_vip_award_record'
    __table_args__ = (
        Index('ix_receive_time_type', 'receive_time', 'award_type'),
        {'comment': 'VIP奖励发放记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(40, 'utf8mb4_0900_bin'), comment='站点code')
    order_id = Column(String(40, 'utf8mb4_0900_bin'), unique=True, comment='订单号')
    award_type = Column(String(5, 'utf8mb4_0900_bin'), comment='奖励类型(0:升级礼金，1:周流水,2:月流水,3:周体育流水)')
    currency = Column(String(10, 'utf8mb4_0900_bin'), comment='币种')
    award_amount = Column(DECIMAL(10, 2), comment='奖励金额')
    agent_id = Column(String(20, 'utf8mb4_0900_bin'), comment='上级代理id')
    agent_account = Column(String(30, 'utf8mb4_0900_bin'), comment='代理账号')
    receive_type = Column(String(5, 'utf8mb4_0900_bin'), comment='领取方式(0:手动领取,1:自动领取)')
    receive_status = Column(String(5, 'utf8mb4_0900_bin'), comment='领取状态(0:未领取,1:已领取,2:已过期)')
    user_id = Column(String(30, 'utf8mb4_0900_bin'), comment='会员id')
    user_account = Column(String(30, 'utf8mb4_0900_bin'), index=True, comment='会员账号')
    vip_grade_code = Column(INTEGER(11), comment='VIP等级')
    vip_rank_code = Column(INTEGER(11), comment='VIP段位code')
    account_type = Column(String(5, 'utf8mb4_0900_bin'), comment='账号类型')
    record_start_time = Column(BIGINT(20), comment='统计开始时间')
    record_end_time = Column(BIGINT(20), comment='统计结束时间')
    receive_time = Column(BIGINT(20), comment='领取时间')
    expired_time = Column(BIGINT(20), comment='过期时间')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

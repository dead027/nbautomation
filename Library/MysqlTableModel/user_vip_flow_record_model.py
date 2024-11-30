# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserVipFlowRecord(Base):
    __tablename__ = 'user_vip_flow_record'
    __table_args__ = (
        Index('ix_user_account', 'user_account', 'vip_rank_code'),
        {'comment': 'VIP流水记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    user_account = Column(String(30, 'utf8mb4_0900_bin'), comment='会员账户')
    vip_rank_code = Column(INTEGER(11), comment='VIP等级code')
    status = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='升降级标识(0:升级,1:j降级,2:保级)')
    valid_amount = Column(DECIMAL(10, 2), comment='单次有效流水金额')
    valid_sum_amount = Column(DECIMAL(10, 2), comment='累计有效流水金额')
    last_vip_time = Column(String(12, 'utf8mb4_0900_bin'), comment='该VIP等级的初始时间yyyy-mm-dd')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

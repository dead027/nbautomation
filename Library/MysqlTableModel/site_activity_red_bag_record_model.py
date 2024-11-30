# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityRedBagRecord(Base):
    __tablename__ = 'site_activity_red_bag_record'
    __table_args__ = (
        Index('idx_sitecode_session_uid_status', 'site_code', 'session_id', 'user_id', 'status'),
        {'comment': '红包雨活动红包记录表'}
    )

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    session_id = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='场次id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    user_id = Column(String(20, 'utf8mb4_0900_bin'), comment='用户id')
    user_account = Column(String(20, 'utf8mb4_0900_bin'), comment='用户编码')
    redbag_amount = Column(DECIMAL(20, 2), comment='红包金额')
    remaining_amount = Column(DECIMAL(20, 2), comment='奖池剩余金额')
    receive_time = Column(BIGINT(20), comment='发放时间')
    status = Column(TINYINT(1), comment='状态 0 未发放 1 已发放\\n')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20))
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20))

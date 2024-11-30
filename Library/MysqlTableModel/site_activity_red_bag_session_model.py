# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, JSON, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityRedBagSession(Base):
    __tablename__ = 'site_activity_red_bag_session'
    __table_args__ = (
        Index('idx_site_code_day_end_str', 'site_code', 'day', 'end_time_str'),
        Index('idx_site_code_status', 'site_code', 'status'),
        {'comment': '红包雨活动场次历史表'}
    )

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    session_id = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='场次id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    day = Column(String(20, 'utf8mb4_0900_bin'), comment='站点时区的日期格式')
    start_time_str = Column(String(20, 'utf8mb4_0900_bin'), comment='站点配置开始时间时分 20:00')
    end_time_str = Column(String(20, 'utf8mb4_0900_bin'), comment='站点配置结束时间时分 20:00')
    start_time = Column(String(20, 'utf8mb4_0900_bin'), comment='开始时间')
    end_time = Column(String(20, 'utf8mb4_0900_bin'), comment='结束时间')
    deposit_amount = Column(DECIMAL(20, 2), comment='存款金额')
    bet_amount = Column(DECIMAL(20, 2), comment='投注流水')
    rank_limit_config = Column(JSON, comment='段位要求 配置')
    advance_time = Column(INTEGER(20), comment='提前时间 秒')
    latest = Column(TINYINT(1), comment='是否当天最后一场次 1是 0否')
    total_amount = Column(DECIMAL(20, 2), comment='红包总金额')
    drop_time = Column(INTEGER(8), comment='红包掉落时间 秒')
    status = Column(TINYINT(4), comment='状态 1 进行中 2 已结束')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20))
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20))

# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityRedBag(Base):
    __tablename__ = 'site_activity_red_bag'
    __table_args__ = {'comment': '红包雨活动配置'}

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), unique=True, comment='站点code')
    deposit_amount = Column(DECIMAL(20, 2), comment='存款金额')
    bet_amount = Column(DECIMAL(20, 2), comment='投注流水')
    rank_limit = Column(String(200, 'utf8mb4_0900_bin'), comment='段位要求 vip_rank_code 数组')
    session_start_time = Column(String(500, 'utf8mb4_0900_bin'), comment='红包雨场次开始时间 数组')
    session_end_time = Column(String(500, 'utf8mb4_0900_bin'), comment='红包雨场次结束时间 数组')
    advance_time = Column(INTEGER(20), comment='提前时间 秒')
    total_amount = Column(DECIMAL(20, 2), comment='红包总金额')
    drop_time = Column(INTEGER(20), comment='红包掉落时间 秒')
    base_id = Column(String(20, 'utf8mb4_0900_bin'), comment='活动主键id')
    start_job_id = Column(String(500, 'utf8mb4_0900_bin'), comment='红包雨开始jobid')
    end_job_id = Column(String(500, 'utf8mb4_0900_bin'), comment='红包雨结束jobid')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

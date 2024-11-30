# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipRankChangeRecord(Base):
    __tablename__ = 'site_vip_rank_change_record'

    id = Column(String(20, 'utf8mb4_0900_bin'), primary_key=True)
    site_code = Column(String(30, 'utf8mb4_0900_bin'), comment='站点code')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), comment='会员id')
    user_label = Column(String(1000, 'utf8mb4_0900_bin'), comment='会员标签')
    user_risk_level = Column(String(50, 'utf8mb4_0900_bin'), comment='会员风控层级')
    vip_rank_old = Column(String(30, 'utf8mb4_0900_bin'), comment='变更前VIP段位')
    vip_rank_now = Column(String(30, 'utf8mb4_0900_bin'), comment='变更后VIP段位')
    change_time = Column(BIGINT(20), comment='变更时间')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

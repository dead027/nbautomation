# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class VipRank(Base):
    __tablename__ = 'vip_rank'
    __table_args__ = {'comment': 'VIP段位配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    vip_rank_code = Column(INTEGER(11), comment='VIP段位code')
    vip_rank_name = Column(String(30, 'utf8mb4_0900_bin'), comment='VIP段位名称')
    creator = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(30, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

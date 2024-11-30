# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVenue(Base):
    __tablename__ = 'site_venue'
    __table_args__ = (
        Index('site_venue_index', 'site_code', 'venue_code', unique=True),
        {'comment': '站点关联场馆表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏场馆CODE')
    handling_fee = Column(DECIMAL(10, 2), comment='手续费')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

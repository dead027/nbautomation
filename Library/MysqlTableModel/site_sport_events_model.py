# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteSportEvent(Base):
    __tablename__ = 'site_sport_events'
    __table_args__ = (
        Index('index', 'site_code', 'events_id', unique=True),
        {'comment': '站点-体育赛事推荐关联'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    events_id = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='赛事ID')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

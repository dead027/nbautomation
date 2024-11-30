# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipVenueExe(Base):
    __tablename__ = 'site_vip_venue_exe'

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(40, 'utf8mb4_0900_bin'), comment='站点code')
    venue_type = Column(String(20, 'utf8mb4_0900_bin'), comment='场馆大类')
    experience = Column(DECIMAL(20, 2), comment='对应升级经验值')
    creator = Column(String(40, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(40, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

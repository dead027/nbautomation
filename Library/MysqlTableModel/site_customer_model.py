# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteCustomer(Base):
    __tablename__ = 'site_customer'
    __table_args__ = {'comment': '站点关联客服通道表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    channel_code = Column(String(50, 'utf8mb4_0900_bin'), comment='通道代码')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BusinessAdminRole(Base):
    __tablename__ = 'business_admin_role'
    __table_args__ = {'comment': '职员和角色关联信息'}

    admin_id = Column(BIGINT(30), primary_key=True, nullable=False, comment='职员ID')
    role_id = Column(BIGINT(30), primary_key=True, nullable=False, comment='角色ID')

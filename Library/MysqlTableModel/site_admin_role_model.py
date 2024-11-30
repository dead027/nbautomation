# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteAdminRole(Base):
    __tablename__ = 'site_admin_role'
    __table_args__ = {'comment': '职员和角色关联信息'}

    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, server_default=text("''"), comment='站点code')
    admin_id = Column(BIGINT(30), primary_key=True, nullable=False, comment='职员ID')
    role_id = Column(BIGINT(30), primary_key=True, nullable=False, comment='角色ID')

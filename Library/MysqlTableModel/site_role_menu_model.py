# coding: utf-8
from sqlalchemy import Column
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteRoleMenu(Base):
    __tablename__ = 'site_role_menu'
    __table_args__ = {'comment': '角色和菜单关联信息'}

    role_id = Column(BIGINT(30), primary_key=True, nullable=False, comment='角色ID')
    menu_id = Column(BIGINT(30), primary_key=True, nullable=False, comment='菜单ID')

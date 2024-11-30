# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentHomeAllButtonEntrance(Base):
    __tablename__ = 'agent_home_all_button_entrance'
    __table_args__ = {'comment': '代理客户端-快捷入口(全部功能)'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    code = Column(INTEGER(11), comment='快捷菜单code')
    name = Column(String(30, 'utf8mb4_0900_bin'), comment='快捷菜单name')
    pc_or_h5 = Column(INTEGER(11), comment='1:PC端 2:H5端')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    creator = Column(String(64, 'utf8mb4_0900_bin'))
    updater = Column(String(64, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

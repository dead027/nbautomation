# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentWithdrawConfig(Base):
    __tablename__ = 'agent_withdraw_config'
    __table_args__ = {'comment': '代理提款设置'}

    id = Column(String(64), primary_key=True, comment='主键id')
    status = Column(INTEGER(11), comment='状态 1开启 0关闭 -1 删除')
    agent_account = Column(String(15, 'utf8mb4_0900_bin'), comment='代理账号')
    site_code = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='站点编码')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

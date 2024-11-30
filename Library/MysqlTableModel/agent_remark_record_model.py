# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentRemarkRecord(Base):
    __tablename__ = 'agent_remark_record'
    __table_args__ = {'comment': '代理备注表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    agent_account = Column(String(50, 'utf8mb4_0900_ai_ci'), nullable=False, comment='代理账号')
    remark = Column(String(255, 'utf8mb4_0900_ai_ci'), comment='备注')
    status = Column(TINYINT(4), comment='状态 0删除 1有效')
    operator = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='操作人')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    created_time = Column(BIGINT(20), comment='创建时间')
    creator = Column(String(64, 'utf8mb4_0900_ai_ci'), comment='创建人')
    updated_time = Column(BIGINT(20), comment='更新时间')
    updater = Column(String(64, 'utf8mb4_0900_ai_ci'), comment='更新人')

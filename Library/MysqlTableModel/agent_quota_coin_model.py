# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentQuotaCoin(Base):
    __tablename__ = 'agent_quota_coin'
    __table_args__ = {'comment': '代理额度钱包'}

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    agent_account = Column(String(15, 'utf8mb4_0900_bin'), index=True, comment='代理账号')
    currency = Column(String(50, 'utf8mb4_0900_bin'), comment='币种')
    agent_name = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='代理名称')
    parent_id = Column(BIGINT(20), comment='代理ID父节点')
    path = Column(String(500, 'utf8mb4_general_ci'), comment='层次id逗号分隔')
    level = Column(INTEGER(11), server_default=text("'1'"), comment='层级')
    total_amount = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='总金额')
    freeze_amount = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='冻结金额')
    available_amount = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='可用余额')
    creator = Column(String(64, 'utf8mb4_0900_ai_ci'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_ai_ci'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

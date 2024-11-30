# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentCommissionRate(Base):
    __tablename__ = 'agent_commission_rate'

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    level = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='级别')
    min_win_loss_amount = Column(DECIMAL(20, 2), nullable=False, server_default=text("'0.00'"), comment='最小团队总输赢')
    new_active_number = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='有效新增会员数')
    active_number = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='有效活跃人数')
    rate = Column(String(50, 'utf8mb4_0900_ai_ci'), nullable=False, comment='佣金比例')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

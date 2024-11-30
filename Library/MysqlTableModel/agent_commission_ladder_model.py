# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentCommissionLadder(Base):
    __tablename__ = 'agent_commission_ladder'
    __table_args__ = {'comment': '盈利分成阶梯配置'}

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    plan_id = Column(String(64, 'utf8mb4_0900_bin'), nullable=False)
    level_name = Column(String(20, 'utf8mb4_0900_bin'), comment='阶梯档位')
    win_loss_amount = Column(DECIMAL(20, 2), comment='平台最少盈利')
    valid_amount = Column(DECIMAL(20, 2), comment='最少有效投注金额')
    active_number = Column(INTEGER(11), server_default=text("'0'"), comment='最少活跃玩家数量')
    new_valid_number = Column(INTEGER(11), server_default=text("'0'"), comment='最少有效新增玩家数量')
    rate = Column(String(10, 'utf8mb4_0900_bin'), comment='盈利分成比例')
    settle_cycle = Column(INTEGER(11), comment='结算周期  1 自然日 2 自然周  3 自然月')
    creator = Column(String(20, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updater = Column(String(20, 'utf8mb4_0900_bin'))
    updated_time = Column(BIGINT(20))

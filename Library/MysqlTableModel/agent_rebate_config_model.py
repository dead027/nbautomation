# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentRebateConfig(Base):
    __tablename__ = 'agent_rebate_config'
    __table_args__ = {'comment': '流水返点配置'}

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    plan_id = Column(String(64, 'utf8mb4_0900_bin'), nullable=False, comment='有效新增人头费')
    settle_cycle = Column(INTEGER(11), nullable=False, comment='结算周期')
    new_user_amount = Column(DECIMAL(20, 2), nullable=False, comment='有效新增人头费')
    slot_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, server_default=text("'0'"), comment='电子有效流水返点比例')
    lottery_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, server_default=text("'0'"), comment='彩票有效流水返点比例')
    lottery_plan_id = Column(BIGINT(20), comment='彩票赔率方案id')
    live_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, server_default=text("'0'"), comment='真人有效流水返点比例')
    sports_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment=' 体育有效流水返点比例')
    sports_plan_id = Column(BIGINT(20), comment='体育赔率方案id')
    chess_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='棋牌有效流水返点比例')
    esports_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='电竞有效流水返点比例')
    esports_plan_id = Column(BIGINT(20), comment='电竞赔率方案id')
    cockfight_rate = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='斗鸡有效流水返点比例')
    creator = Column(String(20, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updater = Column(String(20, 'utf8mb4_0900_bin'))
    updated_time = Column(BIGINT(20))

# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentCommissionPlan(Base):
    __tablename__ = 'agent_commission_plan'
    __table_args__ = {'comment': '佣金方案配置'}

    id = Column(String(64), primary_key=True)
    site_code = Column(String(50), comment='站点code')
    plan_code = Column(String(50), unique=True, comment='方案code')
    plan_name = Column(String(50), comment='方案名称')
    active_deposit = Column(DECIMAL(20, 2), comment='活跃人数最少充值金额')
    active_bet = Column(DECIMAL(20, 2), comment='活跃人数最少有效投注金额')
    valid_deposit = Column(DECIMAL(20, 2), comment='有效新增最少充值金额')
    valid_bet = Column(DECIMAL(20, 2), comment='有效新增最少有效投注额')
    status = Column(INTEGER(11), server_default=text("'1'"), comment='0 已编辑  1 未编辑')
    creator = Column(String(20))
    created_time = Column(BIGINT(20))
    updater = Column(String(20))
    updated_time = Column(BIGINT(20))

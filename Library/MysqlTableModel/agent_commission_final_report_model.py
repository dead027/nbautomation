# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentCommissionFinalReport(Base):
    __tablename__ = 'agent_commission_final_report'
    __table_args__ = (
        Index('agent_index', 'agent_id', 'end_time', unique=True),
        {'comment': '代理佣金结算表'}
    )

    id = Column(String(60), primary_key=True)
    site_code = Column(String(20), comment='siteCode')
    agent_account = Column(String(50, 'utf8mb4_0900_ai_ci'), nullable=False, comment='代理账号')
    agent_id = Column(String(50), comment='agent_id')
    super_agent_id = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='上级代理Id')
    agent_type = Column(INTEGER(11))
    agent_level = Column(INTEGER(11), comment='代理层级')
    risk_level_id = Column(String(64), comment='风控层级id')
    start_time = Column(BIGINT(20), comment='结算开始时间')
    end_time = Column(BIGINT(20), comment='结算结束时间')
    settle_cycle = Column(INTEGER(11), comment='结算周期  1 自然日 2 自然周  3 自然月')
    status = Column(INTEGER(11), comment='状态 1 已发放 2 已取消 3 无佣金 4 已结清 5 未结清')
    early_settle = Column(DECIMAL(11, 0), server_default=text("'0'"), comment='提前结算')
    user_win_loss = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='会员输赢')
    user_win_loss_total = Column(DECIMAL(20, 2), comment='会员总输赢')
    venue_fee = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='场馆费')
    transfer_amount = Column(DECIMAL(20, 2), comment='平台币钱包转化金额')
    access_fee = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='总存取手续费')
    adjust_amount = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='调整金额')
    discount_amount = Column(DECIMAL(20, 2), comment='活动优惠')
    vip_amount = Column(DECIMAL(20, 2), comment='vip福利')
    valid_bet_amount = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='有效流水')
    last_month_remain = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='待冲正金额')
    net_win_loss = Column(DECIMAL(20, 2), comment='会员净输赢')
    active_number = Column(INTEGER(11), server_default=text("'0'"), comment='有效活跃人数')
    new_valid_number = Column(INTEGER(11), server_default=text("'0'"), comment='有效新增')
    agent_rate = Column(DECIMAL(20, 2), comment='负盈利返佣比例')
    commission_amount = Column(DECIMAL(20, 2), server_default=text("'0.00'"), comment='负盈利佣金')
    plan_code = Column(String(20), comment='佣金方案code')
    creator = Column(String(20))
    updater = Column(String(20))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

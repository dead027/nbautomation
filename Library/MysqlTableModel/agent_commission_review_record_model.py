# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentCommissionReviewRecord(Base):
    __tablename__ = 'agent_commission_review_record'
    __table_args__ = {'comment': '代理佣金审核记录表'}

    id = Column(BIGINT(20), primary_key=True)
    site_code = Column(String(20, 'utf8mb4_0900_ai_ci'), comment='siteCode')
    agent_id = Column(String(20, 'utf8mb4_0900_ai_ci'), nullable=False, comment='代理ID')
    agent_account = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='代理账号')
    agent_name = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='代理姓名')
    order_no = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='订单号')
    agent_status = Column(String(5, 'utf8mb4_0900_ai_ci'), comment='账号状态 1正常 2登录锁定 3充提锁定(状态多选,用逗号分开)')
    commission_type = Column(String(5, 'utf8mb4_0900_ai_ci'), comment='佣金类型')
    commission_amount = Column(DECIMAL(20, 2), comment='佣金金额')
    start_time = Column(BIGINT(20), comment='结算开始时间')
    end_time = Column(BIGINT(20), comment='结算结束时间')
    apply_time = Column(BIGINT(20), comment='申请时间')
    settle_time = Column(BIGINT(20), comment='重算时间')
    settle_status = Column(INTEGER(11), comment='是否重算  0 不是  1是')
    currency = Column(String(20, 'utf8mb4_0900_ai_ci'), comment='币种')
    settle_cycle = Column(INTEGER(11), comment='结算周期  1 自然日 2 自然周  3 自然月')
    one_review_start_time = Column(BIGINT(20), comment='一审开始时间')
    one_review_finish_time = Column(BIGINT(20), comment='一审完成时间')
    one_reviewer = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='一审人')
    one_review_remark = Column(String(256, 'utf8mb4_0900_ai_ci'), comment='一审备注')
    order_status = Column(INTEGER(11), comment='订单状态')
    lock_status = Column(INTEGER(11), comment='锁单状态 0未锁 1已锁')
    locker = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='锁单人')
    creator = Column(String(50, 'utf8mb4_0900_ai_ci'))
    updater = Column(String(50, 'utf8mb4_0900_ai_ci'))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

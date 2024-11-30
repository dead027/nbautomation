# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentReview(Base):
    __tablename__ = 'agent_review'
    __table_args__ = {'comment': '代理审核表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    parent_id = Column(BIGINT(20), comment='父节点')
    level = Column(INTEGER(11), comment='代理层级')
    max_level = Column(INTEGER(11), comment='代理线层级上限')
    agent_account = Column(String(20, 'utf8mb4_0900_bin'), comment='代理账号')
    agent_password = Column(String(50, 'utf8mb4_0900_bin'), comment='登录密码')
    agent_type = Column(INTEGER(11), comment='代理类型 1正式 2商务 3置换')
    agent_attribution = Column(INTEGER(11), comment='代理归属 1推广 2招商 3官资')
    agent_category = Column(INTEGER(11), comment='代理类别 1常规代理 2流量代理')
    agent_white_list = Column(String(255, 'utf8mb4_0900_bin'), comment='IP白名单(只有流量代理需要)，使用英文逗号隔开')
    contract_model_commission = Column(INTEGER(11), comment='代理契约模式-佣金契约 1是 0否')
    contract_model_rebate = Column(INTEGER(11), comment='代理契约模式-返点契约 1是 0否')
    review_order_no = Column(String(30, 'utf8mb4_0900_bin'), comment='审核单号')
    apply_info = Column(String(255, 'utf8mb4_0900_bin'), comment='申请信息')
    apply_time = Column(BIGINT(20), comment='申请时间')
    applicant = Column(String(50, 'utf8mb4_0900_bin'), comment='申请人')
    one_review_finish_time = Column(BIGINT(20), comment='一审完成时间')
    reviewer = Column(String(50, 'utf8mb4_0900_bin'), comment='一审人')
    review_operation = Column(INTEGER(11), comment='审核操作')
    review_status = Column(INTEGER(11), comment='审核状态')
    lock_status = Column(INTEGER(11), comment='锁单状态 0未锁 1已锁')
    locker = Column(String(50, 'utf8mb4_0900_bin'), comment='锁单人')
    review_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='一审备注')
    creator = Column(String(64, 'utf8mb4_0900_bin'))
    updater = Column(String(64, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')

# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserTransferAgent(Base):
    __tablename__ = 'user_transfer_agent'
    __table_args__ = {'comment': '会员转代审核表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    user_account = Column(String(255, 'utf8mb4_unicode_ci'), nullable=False, comment='会员ID')
    account_type = Column(INTEGER(11), comment='会员账号类型')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    current_agent_name = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='当前上级代理账号')
    current_agent_id = Column(String(64, 'utf8mb4_unicode_ci'), comment='当前上级代理id')
    transfer_agent_name = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='转入上级代理账号')
    transfer_agent_id = Column(String(64, 'utf8mb4_unicode_ci'), comment='转代后的上级代理id')
    locker_id = Column(String(64, 'utf8mb4_unicode_ci'), comment='锁单人id')
    lock_status = Column(TINYINT(4), server_default=text("'0'"), comment='锁单状态（0-未锁定 1-已锁定）')
    lock_datetime = Column(BIGINT(20), comment='锁单时间')
    lock_name = Column(String(20, 'utf8mb4_unicode_ci'), comment='锁单人')
    audit_status = Column(TINYINT(4), server_default=text("'0'"), comment='审核状态（0-待处理 1-处理中，2-审核通过，3-审核拒绝）')
    audit_datetime = Column(BIGINT(20), comment='审核完成时间')
    audit_id = Column(String(64, 'utf8mb4_unicode_ci'), comment='审核人id')
    audit_name = Column(String(20, 'utf8mb4_unicode_ci'), comment='审核人')
    audit_remark = Column(String(800, 'utf8mb4_unicode_ci'), comment='审核备注')
    event_id = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='单号')
    apply_id = Column(String(64, 'utf8mb4_unicode_ci'), comment='申请人id')
    apply_name = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='申请人')
    apply_remark = Column(String(800, 'utf8mb4_unicode_ci'), comment='申请备注')
    audit_step = Column(TINYINT(4), comment='审核环节（0-结单查看 1-一审审核）')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

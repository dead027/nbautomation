# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentUserOverflow(Base):
    __tablename__ = 'agent_user_overflow'
    __table_args__ = {'comment': '会员溢出审核表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    member_name = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, index=True, comment='会员账号')
    account_type = Column(String(5, 'utf8mb4_unicode_ci'), comment='账号类型;0-试玩,1-测试,2-正式,3-商务,4-置换')
    transfer_agent_name = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='转入上级代理账号')
    agent_type = Column(TINYINT(4), comment='代理类型 1正式 2商务 3置换')
    device = Column(TINYINT(4), comment='推广设备 1APP 2PC 3H5')
    link = Column(String(100, 'utf8mb4_unicode_ci'), comment='推广链接')
    image = Column(String(500, 'utf8mb4_unicode_ci'), comment='上传图片')
    lock_status = Column(TINYINT(4), server_default=text("'0'"), comment='锁单状态（0-未锁定 1-已锁定）')
    lock_datetime = Column(BIGINT(20), comment='锁单时间')
    lock_name = Column(String(20, 'utf8mb4_unicode_ci'), comment='锁单人')
    audit_status = Column(TINYINT(4), server_default=text("'1'"), comment='审核状态（0-待处理 1-处理中，2-审核通过，3-审核拒绝）')
    audit_datetime = Column(BIGINT(20), comment='审核完成时间')
    audit_name = Column(String(20, 'utf8mb4_unicode_ci'), comment='审核人')
    audit_remark = Column(String(800, 'utf8mb4_unicode_ci'), comment='审核备注')
    event_id = Column(String(50, 'utf8mb4_unicode_ci'), nullable=False, comment='单号')
    apply_name = Column(String(20, 'utf8mb4_unicode_ci'), nullable=False, comment='申请人')
    apply_remark = Column(String(800, 'utf8mb4_unicode_ci'), comment='申请备注')
    audit_step = Column(TINYINT(4), comment='审核环节（0-结单查看 1-一审审核）')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    user_register = Column(String(50, 'utf8mb4_unicode_ci'), comment='会员注册信息')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    transfer_agent_id = Column(String(100, 'utf8mb4_unicode_ci'), comment='转入代理id')

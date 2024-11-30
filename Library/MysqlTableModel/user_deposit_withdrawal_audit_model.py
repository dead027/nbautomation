# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserDepositWithdrawalAudit(Base):
    __tablename__ = 'user_deposit_withdrawal_audit'
    __table_args__ = {'comment': '会员存取款订单审核信息'}

    id = Column(BIGINT(20), primary_key=True)
    order_no = Column(String(100, 'utf8mb4_0900_bin'), index=True, comment='存取款订单编号')
    num = Column(TINYINT(4), comment='第X审核')
    audit_user = Column(String(50, 'utf8mb4_0900_bin'), comment='审核人员')
    lock_time = Column(BIGINT(20), comment='锁单时间')
    audit_time = Column(BIGINT(20), comment='审核时间')
    audit_time_consuming = Column(BIGINT(20), comment='审核耗时 单位秒')
    audit_status = Column(TINYINT(4), comment='审核状态 1通过 2不通过')
    audit_info = Column(String(500, 'utf8mb4_0900_bin'), comment='提交审核信息')
    creator = Column(BIGINT(20))
    updater = Column(BIGINT(20))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

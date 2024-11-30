# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserManualUpDownRecord(Base):
    __tablename__ = 'user_manual_up_down_record'
    __table_args__ = (
        Index('agent_account_status_index', 'agent_account', 'audit_status'),
        Index('agent_id_status_index', 'agent_id', 'audit_status'),
        Index('user_account_status_index', 'user_account', 'audit_status'),
        {'comment': '会员人工加减额记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    agent_id = Column(BIGINT(20), comment='代理id')
    agent_account = Column(String(20, 'utf8mb4_0900_bin'), comment='代理账号')
    user_account = Column(String(30, 'utf8mb4_0900_bin'), comment='会员账号')
    user_id = Column(String(20, 'utf8mb4_0900_bin'), comment='会员id')
    user_name = Column(String(30, 'utf8mb4_0900_bin'), comment='姓名')
    vip_grade_code = Column(INTEGER(11), comment='vip等级code')
    order_no = Column(String(30, 'utf8mb4_0900_bin'), comment='订单号')
    adjust_way = Column(INTEGER(11), index=True, comment='调整方式:1-加额，2-减额')
    adjust_type = Column(INTEGER(11), index=True, comment='调整类型:3.其他调整,4.会员提款(后台),5.会员VIP优惠,6.会员活动')
    activity_template = Column(String(20, 'utf8mb4_0900_bin'), comment='活动模板system_param activity_template code值')
    activity_id = Column(String(10, 'utf8mb4_0900_bin'), comment='活动ID')
    currency_code = Column(String(30, 'utf8mb4_0900_bin'), comment='\xa0币种code')
    adjust_amount = Column(DECIMAL(15, 2), comment='调整金额')
    running_water_multiple = Column(DECIMAL(8, 2), comment='流水倍数')
    certificate_address = Column(String(100, 'utf8mb4_0900_bin'), comment='上传附件地址')
    apply_reason = Column(String(255, 'utf8mb4_0900_bin'), comment='申请原因')
    apply_time = Column(BIGINT(20), comment='申请时间')
    applicant = Column(String(50, 'utf8mb4_0900_bin'), comment='申请人')
    audit_datetime = Column(BIGINT(20), comment='审核时间')
    audit_id = Column(String(50, 'utf8mb4_0900_bin'), comment='审核人')
    audit_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='审核备注')
    audit_status = Column(INTEGER(11), comment='审核状态（1-待处理 2-处理中，3-审核通过，4-审核拒绝）')
    review_operation = Column(INTEGER(11), comment='审核操作1.一审审核，2.结单查看')
    balance_change_status = Column(INTEGER(11), comment='账变状态0。账变失败，1.账变成功')
    lock_status = Column(INTEGER(11), comment='锁单状态 0未锁 1已锁')
    locker = Column(String(50, 'utf8mb4_0900_bin'), comment='锁单人')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20), index=True)
    is_big_money = Column(CHAR(1, 'utf8mb4_0900_bin'), index=True, server_default=text("'0'"), comment='会员提款（后台）是否大额出款;0-否，1-是')
    fee_rate = Column(DECIMAL(20, 4), comment='手续费率')
    fee_amount = Column(DECIMAL(20, 4), comment='手续费')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

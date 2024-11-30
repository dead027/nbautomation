# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentManualUpDownRecord(Base):
    __tablename__ = 'agent_manual_up_down_record'
    __table_args__ = {'comment': '代理人工加减额记录'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='site_code')
    agent_id = Column(String(20, 'utf8mb4_0900_bin'), comment='代理id')
    agent_account = Column(String(20, 'utf8mb4_0900_bin'), comment='代理账号')
    agent_name = Column(String(50, 'utf8mb4_0900_bin'), comment='代理姓名')
    order_no = Column(String(30, 'utf8mb4_0900_bin'), comment='订单号')
    wallet_type = Column(INTEGER(11), comment='钱包类型 1佣金钱包 2额度钱包')
    adjust_way = Column(INTEGER(11), comment='调整方式:1-加额，2-减额')
    adjust_type = Column(INTEGER(11), comment='调整类型 1代理存款(后台) 1代理提款(后台) 2佣金 3返点 4代理活动 5其他调整')
    adjust_amount = Column(DECIMAL(15, 2), comment='调整金额')
    certificate_address = Column(String(100, 'utf8mb4_0900_bin'), comment='上传附件地址')
    apply_reason = Column(String(255, 'utf8mb4_0900_bin'), comment='申请原因')
    apply_time = Column(BIGINT(20), comment='申请时间')
    applicant = Column(String(50, 'utf8mb4_0900_bin'), comment='申请人')
    one_review_start_time = Column(BIGINT(20), comment='一审开始时间')
    one_review_finish_time = Column(BIGINT(20), comment='一审完成时间')
    one_reviewer = Column(String(50, 'utf8mb4_0900_bin'), comment='一审人')
    one_review_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='一审备注')
    two_review_start_time = Column(BIGINT(20), comment='二审开始时间')
    two_review_finish_time = Column(BIGINT(20), comment='二审完成时间')
    two_reviewer = Column(String(50, 'utf8mb4_0900_bin'), comment='二审人')
    two_review_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='二审备注')
    review_operation = Column(INTEGER(11), comment='审核操作，1.一审审核，2.二审审核，3.结单查看')
    order_status = Column(INTEGER(11), comment='订单状态;0-待一审，1-一审审核，2-一审拒绝，3-待二审，4-二审审核，5-二审拒绝，6-审核通过')
    balance_change_status = Column(INTEGER(11), comment='账变状态0.账变失败，1.账变成功')
    lock_status = Column(INTEGER(11), comment='锁单状态 0未锁 1已锁')
    locker = Column(String(50, 'utf8mb4_0900_bin'), comment='锁单人')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    is_big_money = Column(CHAR(1, 'utf8mb4_0900_bin'), server_default=text("'0'"), comment='代理提款（后台）是否大额出款;0-否，1-是')
    last_operator = Column(String(30, 'utf8mb4_0900_bin'), comment='最近操作人')
    currency_code = Column(String(30, 'utf8mb4_0900_bin'), comment='当前站点对应平台币代码')

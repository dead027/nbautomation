# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentInfoModifyReview(Base):
    __tablename__ = 'agent_info_modify_review'
    __table_args__ = {'comment': '代理账户修改审核表'}

    id = Column(BIGINT(30), primary_key=True)
    application_time = Column(BIGINT(20), comment=' 申请时间\\n\\n提交审核的时间信息\\n\\n')
    first_review_time = Column(BIGINT(20), comment=' 一审完成时间\\n\\n一审完成后的的时间信息\\n\\n')
    review_order_number = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核单号\\n\\n系统生成\\n\\n')
    review_operation = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核操作\\n\\n')
    review_status = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核状态\\n\\n')
    applicant = Column(String(45, 'utf8mb4_0900_bin'), comment=' 申请人\\n\\n审核提出的后台账号信息\\n\\n')
    first_instance = Column(String(45, 'utf8mb4_0900_bin'), comment=' 一审人\\n\\n一审审核的后台账号信息\\n\\n')
    lock_status = Column(String(45, 'utf8mb4_0900_bin'), comment=' 锁单状态 1锁单 0 解锁')
    review_application_type = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核申请类型\\n\\n')
    agent_account = Column(String(45, 'utf8mb4_0900_bin'), comment=' 代理账号\\n\\n 注册成功后的登录账号信息\\n\\n')
    agent_type = Column(INTEGER(11), comment=' 账号类型\\n账号创建时赋予的会员类型信息\\n\\n\\n')
    before_fixing = Column(String(45, 'utf8mb4_0900_bin'), comment=' 修改前\\n\\n对应审核类型审核前最近的原始数据信息\\n\\n')
    after_modification = Column(String(45, 'utf8mb4_0900_bin'), comment=' 修改后\\n\\n对应审核类型审核时需要修改的数据信息\\n\\n')
    locker = Column(String(45, 'utf8mb4_0900_bin'), comment='锁单人')
    review_remark = Column(String(100, 'utf8mb4_0900_bin'), comment='一审完成备注')
    application_information = Column(String(100, 'utf8mb4_0900_bin'), comment=' 申请信息')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    creator = Column(String(64, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updater = Column(String(64, 'utf8mb4_0900_bin'))
    updated_time = Column(BIGINT(20))

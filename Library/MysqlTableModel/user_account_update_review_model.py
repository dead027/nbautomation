# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserAccountUpdateReview(Base):
    __tablename__ = 'user_account_update_review'
    __table_args__ = {'comment': '会员账号修改审核'}

    id = Column(BIGINT(30), primary_key=True, unique=True)
    application_time = Column(BIGINT(30), comment=' 申请时间提交审核的时间信息')
    first_review_time = Column(BIGINT(30), comment=' 一审完成时间一审完成后的的时间信息')
    review_order_number = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核单号系统生成')
    review_operation = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核操作')
    review_status = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核状态')
    applicant = Column(String(45, 'utf8mb4_0900_bin'), comment=' 申请人审核提出的后台账号信息')
    first_instance = Column(String(45, 'utf8mb4_0900_bin'), comment=' 一审人一审审核的后台账号信息')
    lock_status = Column(String(45, 'utf8mb4_0900_bin'), comment=' 锁单状态')
    review_application_type = Column(String(45, 'utf8mb4_0900_bin'), comment=' 审核申请类型')
    member_account = Column(String(45, 'utf8mb4_0900_bin'), comment=' 会员账号 注册成功后的登录账号信息')
    account_type = Column(String(45, 'utf8mb4_0900_bin'), comment=' 账号类型 账号创建时赋予的会员类型信息')
    before_fixing = Column(String(500, 'utf8mb4_0900_bin'), comment=' 修改前 对应审核类型审核前最近的原始数据信息')
    after_modification = Column(String(500, 'utf8mb4_0900_bin'), comment=' 修改后 对应审核类型审核时需要修改的数据信息')
    locker = Column(String(45, 'utf8mb4_0900_bin'), comment='锁单人')
    review_remark = Column(String(100, 'utf8mb4_0900_bin'), comment='一审完成备注')
    application_information = Column(String(100, 'utf8mb4_0900_bin'), comment=' 申请信息')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(String(64, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(30))
    updater = Column(String(64, 'utf8mb4_0900_bin'))
    updated_time = Column(BIGINT(30))

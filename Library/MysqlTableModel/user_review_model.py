# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserReview(Base):
    __tablename__ = 'user_review'
    __table_args__ = {'comment': '会员审核表'}

    id = Column(BIGINT(0), primary_key=True, comment='主键id')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), comment='会员注册信息')
    password = Column(String(50, 'utf8mb4_0900_bin'), comment='密码')
    account_type = Column(INTEGER(0), comment='账号类型')
    area_code = Column(String(20, 'utf8mb4_0900_bin'), comment='区号')
    phone = Column(String(20, 'utf8mb4_0900_bin'), comment='手机号码')
    email = Column(String(50, 'utf8mb4_0900_bin'), comment='邮箱')
    main_currency = Column(String(10, 'utf8mb4_0900_bin'), comment='主货币')
    super_agent_id = Column(BIGINT(0), comment='上级代理id')
    super_agent_account = Column(String(30, 'utf8mb4_0900_bin'), comment='上级代理账号')
    vip_grade = Column(INTEGER(0), comment='vip等级')
    review_order_no = Column(String(30, 'utf8mb4_0900_bin'), comment='审核单号')
    apply_info = Column(String(255, 'utf8mb4_0900_bin'), comment='申请信息')
    apply_time = Column(BIGINT(0), comment='申请时间')
    applicant = Column(String(50, 'utf8mb4_0900_bin'), comment='申请人')
    one_review_finish_time = Column(BIGINT(0), comment='一审完成时间')
    reviewer = Column(String(50, 'utf8mb4_0900_bin'), comment='一审人')
    review_operation = Column(INTEGER(0), comment='审核操作')
    review_status = Column(INTEGER(0), comment='审核状态')
    lock_status = Column(INTEGER(0), comment='锁单状态 0未锁 1已锁')
    locker = Column(String(50, 'utf8mb4_0900_bin'), comment='锁单人')
    review_remark = Column(String(255, 'utf8mb4_0900_bin'), comment='一审备注')
    user_id = Column(String(64, 'utf8mb4_0900_bin'), comment='用户id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    updater = Column(String(64, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(0))
    updated_time = Column(BIGINT(0))
    salt = Column(String(15, 'utf8mb4_0900_bin'), comment='加密盐')
    creator = Column(String(50, 'utf8mb4_0900_bin'))

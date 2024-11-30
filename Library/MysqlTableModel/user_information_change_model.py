# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserInformationChange(Base):
    __tablename__ = 'user_information_change'

    id = Column(BIGINT(20), primary_key=True)
    operating_time = Column(BIGINT(20), comment=' 操作时间')
    member_account = Column(String(45, 'utf8mb4_0900_bin'), comment=' 会员账号')
    operator = Column(String(45, 'utf8mb4_0900_bin'), comment=' 操作人')
    change_type = Column(String(45, 'utf8mb4_0900_bin'), comment=' 变更类型')
    account_type = Column(String(45, 'utf8mb4_0900_bin'), comment=' 账号类型')
    Information_before_change = Column(String(1000, 'utf8mb4_0900_bin'), comment=' 变更前信息')
    Information_after_change = Column(String(1000, 'utf8mb4_0900_bin'), comment='  变更后信息')
    submit_information = Column(String(100, 'utf8mb4_0900_bin'), comment='提交信息')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(BIGINT(20))
    created_time = Column(BIGINT(20))
    updater = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

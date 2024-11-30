# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserTypingAmount(Base):
    __tablename__ = 'user_typing_amount'
    __table_args__ = {'comment': '会员打码量信息'}

    id = Column(BIGINT(20), primary_key=True)
    user_account = Column(String(50, 'utf8mb4_0900_bin'), comment='会员账号')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    typing_amount = Column(DECIMAL(20, 2), comment='打码量')
    start_time = Column(BIGINT(20), comment='流水开始统计时间')
    user_id = Column(BIGINT(20), unique=True, comment='会员ID')
    currency = Column(String(20, 'utf8mb4_0900_bin'), comment='币种')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

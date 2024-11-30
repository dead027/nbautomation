# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserCoin(Base):
    __tablename__ = 'user_coin'
    __table_args__ = {'comment': '会员钱包'}

    id = Column(BIGINT(30), primary_key=True, comment='ID')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    user_account = Column(String(20, 'utf8mb4_0900_bin'), comment='会员账号')
    user_id = Column(BIGINT(20), comment='会员ID')
    currency = Column(String(50, 'utf8mb4_0900_bin'), comment='币种')
    total_amount = Column(DECIMAL(20, 2), comment='总金额')
    freeze_amount = Column(DECIMAL(20, 2), comment='冻结金额')
    available_amount = Column(DECIMAL(20, 2), comment='可用余额')
    is_bring_in_venue = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='是否自动带入场馆（ 0否 1是）')
    created_time = Column(BIGINT(30), comment='创建时间')
    updated_time = Column(BIGINT(30), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

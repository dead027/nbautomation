# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserHotWalletAddres(Base):
    __tablename__ = 'user_hot_wallet_address'
    __table_args__ = {'comment': '热钱包地址'}

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    account = Column(String(100, 'utf8mb4_0900_bin'), comment='会员ID')
    china_type = Column(String(20, 'utf8mb4_0900_bin'), comment='链类型')
    network_type = Column(String(50, 'utf8mb4_0900_bin'), comment='协议类型')
    address = Column(String(255, 'utf8mb4_0900_bin'), comment='地址')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

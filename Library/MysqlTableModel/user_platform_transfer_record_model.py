# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserPlatformTransferRecord(Base):
    __tablename__ = 'user_platform_transfer_record'
    __table_args__ = {'comment': '会员平台币转换记录'}

    id = Column(BIGINT(30), primary_key=True, comment='ID')
    order_no = Column(String(50, 'utf8mb4_0900_bin'), unique=True, comment='订单号')
    order_time = Column(String(50, 'utf8mb4_0900_bin'), comment='转换时间')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    user_account = Column(String(20, 'utf8mb4_0900_bin'), comment='会员账号')
    user_id = Column(BIGINT(20), comment='会员ID')
    agent_id = Column(String(10, 'utf8mb4_bin'), comment='代理编号')
    agent_account = Column(String(15, 'utf8mb4_0900_bin'), comment='代理账号')
    plat_currency_code = Column(String(50, 'utf8mb4_0900_bin'), comment='平台币币种')
    target_currency_code = Column(String(50, 'utf8mb4_0900_bin'), comment='转换币种')
    transfer_amount = Column(DECIMAL(20, 2), comment='转换金额')
    transfer_rate = Column(DECIMAL(20, 2), comment='汇率')
    target_amount = Column(DECIMAL(20, 2), comment='目标金额')
    created_time = Column(BIGINT(30), comment='创建时间')
    updated_time = Column(BIGINT(30), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

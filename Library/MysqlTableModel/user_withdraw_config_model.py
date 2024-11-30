# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserWithdrawConfig(Base):
    __tablename__ = 'user_withdraw_config'
    __table_args__ = {'comment': '会员提款设置'}

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    site_code = Column(String(64, 'utf8mb4_0900_bin'))
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='货币代码')
    vip_rank_code = Column(INTEGER(11), comment='段位')
    single_day_withdraw_count = Column(INTEGER(11), comment='单日提款总次数')
    single_max_withdraw_amount = Column(DECIMAL(20, 2), comment='单日最高提款总额')
    bank_card_single_withdraw_min_amount = Column(DECIMAL(20, 2), comment='银行卡单次提款最低限额')
    bank_card_single_withdraw_max_amount = Column(DECIMAL(20, 2), comment='银行卡单次提款最高限额')
    crypto_currency_single_withdraw_min_amount = Column(DECIMAL(20, 2), comment='加密货币单次提款最低限额')
    crypto_currency_single_withdraw_max_amount = Column(DECIMAL(20, 2), comment='加密货币单次提款最高限额')
    electronic_wallet_withdraw_min_amount = Column(DECIMAL(10, 2), comment='电子钱包单次提款最低限额')
    electronic_wallet_withdraw_max_amount = Column(DECIMAL(10, 2), comment='电子钱包单次提款最高限额')
    large_withdraw_mark_amount = Column(DECIMAL(20, 2), comment='大额提款标记金额')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

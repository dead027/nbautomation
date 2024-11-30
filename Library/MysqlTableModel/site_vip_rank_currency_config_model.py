# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipRankCurrencyConfig(Base):
    __tablename__ = 'site_vip_rank_currency_config'
    __table_args__ = {'comment': '站点vip段位币种信息配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    vip_rank_code = Column(INTEGER(11), nullable=False, comment='段位code.根据siteCode+段位code=段位')
    currency_code = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='货币代码')
    daily_withdrawals = Column(INTEGER(11), comment='日提款次数')
    day_withdraw_limit = Column(DECIMAL(10, 2), comment='单日提款上限')
    withdraw_fee = Column(DECIMAL(10, 2), comment='提现手续费')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='修改时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

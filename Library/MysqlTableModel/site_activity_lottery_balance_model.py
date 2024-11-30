# coding: utf-8
from sqlalchemy import Column, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityLotteryBalance(Base):
    __tablename__ = 'site_activity_lottery_balance'
    __table_args__ = (
        Index('idx_user_account_site_code', 'user_account', 'site_code', unique=True),
        {'comment': '抽奖次数余额表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='会员ID')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='会员账号')
    balance = Column(INTEGER(11), server_default=text("'0'"), comment='当前抽奖次数余额')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

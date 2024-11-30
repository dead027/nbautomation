# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CasinoMemberLogin(Base):
    __tablename__ = 'casino_member_login'
    __table_args__ = (
        Index('name_log_index', 'user_account', 'venue_code', 'site_code', unique=True),
    )

    id = Column(BIGINT(30), primary_key=True)
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_account = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='用户账号')
    venue_user_account = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='游戏账号')
    venue_platform = Column(String(50, 'utf8mb4_0900_bin'))
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='场馆')
    last_login_time = Column(BIGINT(20), comment='最后登录时间')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

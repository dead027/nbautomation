# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CasinoMember(Base):
    __tablename__ = 'casino_member'
    __table_args__ = (
        Index('name_index', 'user_account', 'venue_code', 'site_code', unique=True),
    )

    id = Column(BIGINT(30), primary_key=True)
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_account = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='用户账号')
    venue_user_account = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='游戏账号')
    casino_password = Column(String(50, 'utf8mb4_0900_bin'))
    user_id = Column(String(50, 'utf8mb4_0900_bin'), comment='本地用户id')
    venue_user_id = Column(String(50, 'utf8mb4_0900_bin'), comment='三方游戏用户id')
    venue_platform = Column(String(50, 'utf8mb4_0900_bin'), comment='三方平台')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='场馆')
    status = Column(String(255, 'utf8mb4_0900_bin'), comment='状态  0 失败  1 成功')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

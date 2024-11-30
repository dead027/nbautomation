# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ReportUserVenueWinLose(Base):
    __tablename__ = 'report_user_venue_win_lose'
    __table_args__ = (
        Index('day_code_index', 'day', 'venue_code', 'user_account', unique=True),
        {'comment': '会员每日场馆盈亏'}
    )

    id = Column(String(100, 'utf8mb4_0900_bin'), primary_key=True)
    day = Column(BIGINT(20), nullable=False, comment='日期')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编号')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), comment='会员账号')
    agent_account = Column(String(100, 'utf8mb4_0900_bin'), comment='上级代理')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='游戏平台CODE')
    game_name = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏名称')
    bet_count = Column(INTEGER(11), nullable=False, server_default=text("'0'"), comment='注单数')
    bet_amount = Column(DECIMAL(20, 4), nullable=False, comment='投注金额')
    valid_amount = Column(DECIMAL(20, 4), nullable=False, comment='有效投注')
    win_loss_amount = Column(DECIMAL(20, 4), nullable=False, comment='投注盈亏')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))

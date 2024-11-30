# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameCollection(Base):
    __tablename__ = 'game_collection'
    __table_args__ = (
        Index('index', 'user_id', 'game_id', unique=True),
        {'comment': '游戏收藏'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    user_id = Column(BIGINT(20), comment='用户id')
    game_id = Column(BIGINT(20), comment='游戏id')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

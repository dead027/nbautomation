# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteGame(Base):
    __tablename__ = 'site_game'
    __table_args__ = (
        Index('index_game', 'site_code', 'game_info_id', unique=True),
        {'comment': '站点关联游戏表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏场馆CODE')
    game_info_id = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏id')
    corner_labels = Column(String(50, 'utf8mb4_0900_bin'), comment='角标')
    label = Column(INTEGER(11), comment='标签')
    creator = Column(INTEGER(11), comment='创建人')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人名称')
    updated_time = Column(BIGINT(20), comment='更新时间')

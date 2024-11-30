# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SportEventsRecommend(Base):
    __tablename__ = 'sport_events_recommend'
    __table_args__ = {'comment': '体育赛事推荐'}

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    league_id = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='联赛ID')
    league_name = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='联赛名称')
    events_id = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='赛事ID')
    events_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='赛事CODE')
    home_name = Column(String(200, 'utf8mb4_0900_bin'), nullable=False, comment='主队名称')
    home_id = Column(String(200, 'utf8mb4_0900_bin'), nullable=False, comment='主队id')
    away_id = Column(String(200, 'utf8mb4_0900_bin'), nullable=False, comment='客队id')
    away_name = Column(String(200, 'utf8mb4_0900_bin'), nullable=False, comment='客队名称\t')
    date_time = Column(BIGINT(20), nullable=False, comment='开赛时间')
    sport_type = Column(INTEGER(50), nullable=False, comment='体育项目ID:1: 足球。2: 篮球。3: 美式足球。4: 冰上曲棍球。9: 羽毛球。24: 手球。26: 橄榄球。43: 电子竞技')
    sport_name = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='体育项目名称')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

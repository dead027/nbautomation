# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SportFollow(Base):
    __tablename__ = 'sport_follow'
    __table_args__ = (
        Index('index_id', 'user_id', 'type', 'third_id', 'site_code', unique=True),
        {'comment': '体育赛事关注表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    user_id = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='用户')
    type = Column(String(50, 'utf8mb4_0900_ai_ci'), nullable=False, comment='盘口类型:1:冠军，2:赛事')
    third_id = Column(String(200, 'utf8mb4_0900_bin'), nullable=False, comment='三方ID')
    remark = Column(String(100, 'utf8mb4_0900_bin'), comment='备注')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

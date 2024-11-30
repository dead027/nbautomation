# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class VipGrade(Base):
    __tablename__ = 'vip_grade'
    __table_args__ = {'comment': 'Vip等级配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    vip_grade_code = Column(INTEGER(11), comment='vip等级code')
    vip_grade_name = Column(String(30, 'utf8mb4_0900_bin'), comment='vip等级名称')
    creator = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

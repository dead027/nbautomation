# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class LanguageNameConfig(Base):
    __tablename__ = 'language_name_config'
    __table_args__ = (
        Index('index_code', 'code', 'param_id', 'language', 'site_code', unique=True),
        {'comment': '多语言名称配置'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    code = Column(String(50, 'utf8mb4_0900_bin'), comment='业务code')
    param_id = Column(BIGINT(20), comment='关联关系ID')
    name = Column(String(50, 'utf8mb4_0900_bin'), comment='名称')
    language = Column(String(50, 'utf8mb4_0900_bin'), comment='语言')
    creator = Column(BIGINT(20), comment='创建人')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

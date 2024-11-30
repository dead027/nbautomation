# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityLab(Base):
    __tablename__ = 'site_activity_labs'
    __table_args__ = {'comment': '站点-活动页签'}

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    lab_name_i18_code = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='分类名称多语言code')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='所属站点')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    status = Column(INTEGER(11), nullable=False, server_default=text("'1'"), comment='0.禁用，1.启用')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='修改时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

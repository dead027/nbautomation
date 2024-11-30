# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class LanguageManager(Base):
    __tablename__ = 'language_manager'
    __table_args__ = {'comment': '语种管理表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), index=True, comment='站点code')
    name = Column(String(32, 'utf8mb4_0900_bin'), comment='名称')
    code = Column(String(32, 'utf8mb4_0900_bin'), comment='语种code')
    show_code = Column(String(64, 'utf8mb4_0900_bin'), comment='展示code')
    icon = Column(String(512, 'utf8mb4_0900_bin'), comment='图标')
    sort = Column(INTEGER(11), comment='排序')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='状态 1启用 0禁用')
    operate_time = Column(BIGINT(20), comment='操作时间')
    operator = Column(String(64, 'utf8mb4_0900_bin'), comment='操作人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='修改时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameOneClassInfo(Base):
    __tablename__ = 'game_one_class_info'
    __table_args__ = {'comment': '游戏类型(一级分类配置)'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    directory_name = Column(String(50, 'utf8mb4_0900_bin'), comment='目录名称')
    directory_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='目录名称-多语言')
    home_name = Column(String(50, 'utf8mb4_0900_bin'), comment='首页名称')
    home_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='首页名称-多语言')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点CODE')
    status = Column(INTEGER(11), server_default=text("'1'"), comment='状态（ 1 开启中 2 维护中 3 已禁用）')
    directory_sort = Column(INTEGER(11), server_default=text("'1'"), comment='目录排序')
    home_sort = Column(INTEGER(11), server_default=text("'1'"), comment='首页排序')
    model_code = Column(String(20, 'utf8mb4_0900_bin'), comment='前端模版code')
    remark = Column(String(200, 'utf8mb4_0900_bin'), server_default=text("''"), comment='备注')
    icon = Column(String(100, 'utf8mb4_0900_bin'), comment='图标')
    creator = Column(BIGINT(20), comment='创建人')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

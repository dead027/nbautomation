# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameTwoClassInfo(Base):
    __tablename__ = 'game_two_class_info'
    __table_args__ = {'comment': '游戏类型(二级分类配置)'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    type_name = Column(String(50, 'utf8mb4_0900_bin'), comment='分类名称')
    type_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='分类名称-多语言')
    game_one_id = Column(BIGINT(20), comment='geme_one_class_info.id')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='\t')
    model_code = Column(String(20, 'utf8mb4_0900_bin'), comment='前端模版code')
    sort = Column(INTEGER(11), comment='排序')
    status = Column(INTEGER(11), server_default=text("'1'"), comment='状态（ 1 开启中 2 维护中 3 已禁用）')
    remark = Column(String(200, 'utf8mb4_0900_bin'), server_default=text("''"), comment='备注')
    icon = Column(String(100, 'utf8mb4_0900_bin'), comment='图标')
    creator = Column(BIGINT(20), comment='创建人')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

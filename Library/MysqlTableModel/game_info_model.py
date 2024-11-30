# coding: utf-8
from sqlalchemy import Column, Index, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class GameInfo(Base):
    __tablename__ = 'game_info'
    __table_args__ = (
        Index('game_name_index', 'game_name', 'venue_code', unique=True),
        Index('game_code_venue_access', 'venue_id', 'access_parameters', unique=True),
        {'comment': '游戏信息'}
    )

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    game_id = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏ID')
    game_name = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏名称')
    game_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏名称-多语言')
    venue_id = Column(BIGINT(20), comment='平台ID')
    venue_code = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏平台CODE')
    venue_name = Column(String(50, 'utf8mb4_0900_bin'), comment='平台名称')
    venue_type = Column(INTEGER(11), comment='场馆类型:1:体育 2:视讯 3:棋牌 4:电子')
    status = Column(INTEGER(11), server_default=text("'1'"), comment='状态（ 1 开启中 2 维护中 3 已禁用）')
    support_device = Column(String(100, 'utf8mb4_0900_bin'), server_default=text("''"), comment='支持终端（ 1 pc 2 ios_app 3 ios_app 4 android_h5 4 android_app) 多个逗号隔开')
    label = Column(INTEGER(11), server_default=text("'0'"), comment='标签')
    corner_labels = Column(INTEGER(11), server_default=text("'0'"), comment='角标')
    icon_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='多语言-游戏图片')
    game_desc = Column(String(50, 'utf8mb4_0900_bin'), comment='游戏描述')
    game_desc_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='多语言-游戏描述')
    remark = Column(String(200, 'utf8mb4_0900_bin'), server_default=text("''"), comment='备注')
    is_rebate = Column(INTEGER(11), server_default=text("'0'"), comment='是否返水（ 0 否 1 是 ）')
    access_parameters = Column(String(100, 'utf8mb4_0900_bin'), server_default=text("''"), comment='接入参数')
    maintenance_start_time = Column(BIGINT(20), comment='维护开始时间')
    maintenance_end_time = Column(BIGINT(20), comment='维护结束时间')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

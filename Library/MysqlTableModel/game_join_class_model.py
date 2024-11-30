# coding: utf-8
from sqlalchemy import Column, Index, MetaData, String, Table, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

metadata = MetaData()


t_game_join_class = Table(
    'game_join_class', metadata,
    Column('id', BIGINT(20), nullable=False, comment='主键id'),
    Column('game_id', BIGINT(20), comment='game_info.id'),
    Column('game_two_id', BIGINT(20), comment='geme_two_class_info.id'),
    Column('site_code', String(50, 'utf8mb4_0900_bin'), comment='站点CODE'),
    Column('sort', INTEGER(11), server_default=text("'1'"), comment='排序'),
    Column('creator', BIGINT(20), comment='创建人'),
    Column('creator_name', String(50, 'utf8mb4_0900_bin'), comment='创建人'),
    Column('created_time', BIGINT(20), comment='创建时间'),
    Column('updater', BIGINT(20), comment='更新人'),
    Column('updater_name', String(50, 'utf8mb4_0900_bin'), comment='更新人'),
    Column('updated_time', BIGINT(20), comment='更新时间'),
    Index('site_game_join_index', 'game_id', 'game_two_id', 'site_code', unique=True),
    comment='游戏分类配置关系表'
)

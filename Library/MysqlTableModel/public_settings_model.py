# coding: utf-8
from sqlalchemy import Column, Index, MetaData, String, Table, text
from sqlalchemy.dialects.mysql import BIGINT

metadata = MetaData()


t_public_settings = Table(
    'public_settings', metadata,
    Column('id', BIGINT(20), nullable=False, comment='ID'),
    Column('site_code', String(50, 'utf8mb4_0900_bin'), comment='站点CODE'),
    Column('user_id', String(50, 'utf8mb4_0900_bin'), nullable=False, comment='用户'),
    Column('type', String(50, 'utf8mb4_0900_ai_ci'), nullable=False, server_default=text("'1'"), comment='类型标记'),
    Column('value', String(200, 'utf8mb4_0900_bin'), nullable=False, comment='值'),
    Column('remark', String(100, 'utf8mb4_0900_bin'), comment='备注'),
    Column('creator', BIGINT(20), comment='创建人'),
    Column('created_time', BIGINT(20), comment='创建时间'),
    Column('updater', BIGINT(20), comment='更新人'),
    Column('updated_time', BIGINT(20), comment='更新时间'),
    Index('index_user', 'user_id', 'type', 'value', 'site_code', unique=True),
    comment='公共参数设置'
)

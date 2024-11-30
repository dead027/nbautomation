# coding: utf-8
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.dialects.mysql import BIGINT

metadata = MetaData()


t_agent_label = Table(
    'agent_label', metadata,
    Column('id', BIGINT(30), unique=True, comment='主键'),
    Column('site_code', String(30, 'utf8mb4_0900_bin'), comment='站点code'),
    Column('name', String(100, 'utf8mb4_0900_bin'), comment='标签名称'),
    Column('description', String(255, 'utf8mb4_0900_bin'), comment='标签描述'),
    Column('operator', String(30, 'utf8mb4_0900_bin'), comment='操作人'),
    Column('creator', String(30, 'utf8mb4_0900_bin'), comment='创建人'),
    Column('created_time', BIGINT(30), comment='创建时间'),
    Column('updater', String(30, 'utf8mb4_0900_bin'), comment='修改人'),
    Column('updated_time', BIGINT(30), comment='修改时间'),
    comment='代理标签'
)

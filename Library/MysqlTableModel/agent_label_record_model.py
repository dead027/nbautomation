# coding: utf-8
from sqlalchemy import Column, MetaData, String, Table
from sqlalchemy.dialects.mysql import BIGINT, INTEGER

metadata = MetaData()


t_agent_label_record = Table(
    'agent_label_record', metadata,
    Column('id', BIGINT(30), unique=True, comment='主键'),
    Column('site_code', String(20, 'utf8mb4_0900_bin'), comment='站点code'),
    Column('type', INTEGER(10), comment='0.修改名称,1.修改描述,2新增,3.删除'),
    Column('agent_label_id', BIGINT(30), comment='标签id'),
    Column('agent_label_name', String(100, 'utf8mb4_0900_bin'), comment='标签名称'),
    Column('change_before', String(100, 'utf8mb4_0900_bin'), comment='变更前'),
    Column('change_after', String(100, 'utf8mb4_0900_bin'), comment='变更后'),
    Column('operator', String(30, 'utf8mb4_0900_bin'), comment='操作人'),
    Column('creator', String(30, 'utf8mb4_0900_bin')),
    Column('created_time', BIGINT(20)),
    Column('updater', String(30, 'utf8mb4_0900_bin')),
    Column('updated_time', BIGINT(20))
)

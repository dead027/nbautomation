# coding: utf-8
from sqlalchemy import Column, Index, MetaData, String, Table

metadata = MetaData()


t_mail_site_link = Table(
    'mail_site_link', metadata,
    Column('site_code', String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code'),
    Column('channel_code', String(20, 'utf8mb4_0900_bin'), nullable=False),
    Index('mail_site_index', 'site_code', 'channel_code', unique=True),
    comment='邮箱站点关联表'
)

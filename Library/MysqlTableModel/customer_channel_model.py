# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CustomerChannel(Base):
    __tablename__ = 'customer_channel'
    __table_args__ = {'comment': '客服通道管理'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    channel_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='通道代码')
    channel_name = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='通道名称')
    customer_type = Column(TINYINT(4), nullable=False, server_default=text("'1'"), comment='客服类型;1-在线客服')
    channel_addr = Column(String(100, 'utf8mb4_0900_bin'), comment='通道地址')
    status = Column(TINYINT(4), server_default=text("'1'"), comment='状态;1-启用,2-禁用')
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注')
    creator = Column(BIGINT(20), comment='创建人')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人名称')
    updated_time = Column(BIGINT(20), comment='更新时间')

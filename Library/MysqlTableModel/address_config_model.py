# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AddressConfig(Base):
    __tablename__ = 'address_config'
    __table_args__ = {'comment': '地址配置表'}

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    add_type = Column(String(10, 'utf8mb4_0900_bin'), comment='类型code')
    add_type_name = Column(String(30, 'utf8mb4_0900_bin'), comment='类型名称')
    address = Column(String(100, 'utf8mb4_0900_bin'), comment='地址')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    operator = Column(String(20, 'utf8mb4_0900_bin'), comment='操作人')
    operator_time = Column(BIGINT(20), comment='操作时间')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

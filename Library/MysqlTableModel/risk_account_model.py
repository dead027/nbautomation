# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RiskAccount(Base):
    __tablename__ = 'risk_account'
    __table_args__ = {'comment': '风控账号'}

    id = Column(BIGINT(0), primary_key=True)
    risk_control_account = Column(String(50, 'utf8mb4_0900_bin'), comment='风控账号')
    risk_control_type = Column(String(50, 'utf8mb4_0900_bin'), comment='风控类型')
    risk_control_type_code = Column(String(5, 'utf8mb4_0900_bin'), comment='风控类型code')
    risk_control_level_id = Column(BIGINT(0), comment='风控层级id')
    risk_control_level = Column(String(50, 'utf8mb4_0900_bin'), comment='风控层级')
    risk_desc = Column(String(1024, 'utf8mb4_0900_bin'), comment='备注')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(BIGINT(0))
    created_time = Column(BIGINT(0))
    updater = Column(BIGINT(0))
    updated_time = Column(BIGINT(0))

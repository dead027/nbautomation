# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RiskCtrlLevel(Base):
    __tablename__ = 'risk_ctrl_level'
    __table_args__ = {'comment': '风控层级'}

    id = Column(BIGINT(30), primary_key=True, unique=True)
    risk_control_type = Column(String(45, 'utf8mb4_0900_bin'), nullable=False, comment='风控类型——需要风控的字段\\n\\n')
    risk_control_level = Column(String(45, 'utf8mb4_0900_bin'), nullable=False, comment='风控层级—新增风控层级时填写的风控层级信息')
    risk_control_level_code = Column(BIGINT(0))
    risk_control_level_describe = Column(String(50, 'utf8mb4_0900_bin'), comment='风控层级描述—新增风控层级时填写的风控层级信息')
    delete_flag = Column(String(45, 'utf8mb4_0900_bin'), nullable=False, server_default=text("'1'"), comment='删除数据标记—默认为1表示数据存在，0表示数据已经删除')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(String(45, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(0))
    updater = Column(String(45, 'utf8mb4_0900_bin'))
    updated_time = Column(BIGINT(0), nullable=False)

# coding: utf-8
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemParam(Base):
    __tablename__ = 'system_param'
    __table_args__ = {'comment': '系统lookup表'}

    id = Column(BIGINT(30), primary_key=True)
    type = Column(String(255, 'utf8mb4_0900_bin'), nullable=False, comment='配置類型')
    code = Column(String(255, 'utf8mb4_0900_bin'), nullable=False, comment='配置代碼')
    value = Column(String(255, 'utf8mb4_0900_bin'), nullable=False, comment='配置數值')
    value_desc = Column(String(255, 'utf8mb4_0900_bin'), comment='配置值中文描述-为翻译')
    description = Column(Text(collation='utf8mb4_0900_bin'), comment='描述')
    creator = Column(BIGINT(0), nullable=False, comment='建置人員')
    created_time = Column(BIGINT(0), nullable=False, comment='建置時間')
    updater = Column(BIGINT(0), comment='更新人員')
    updated_time = Column(BIGINT(0), comment='更新時間')

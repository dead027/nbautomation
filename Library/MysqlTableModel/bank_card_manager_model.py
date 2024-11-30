# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class BankCardManager(Base):
    __tablename__ = 'bank_card_manager'
    __table_args__ = {'comment': '银行卡管理'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    bank_name = Column(String(128, 'utf8mb4_0900_bin'), comment='银行名称')
    show_name = Column(String(128, 'utf8mb4_0900_bin'), comment='前端显示名称')
    bank_code = Column(String(64, 'utf8mb4_0900_bin'), comment='银行代码')
    icon = Column(String(512, 'utf8mb4_0900_bin'), comment='图标')
    currency = Column(String(16, 'utf8mb4_0900_bin'), comment='币种')
    sort = Column(INTEGER(8), comment='排序')
    status = Column(TINYINT(1), server_default=text("'0'"), comment='状态 1启用 0禁用')
    operate_time = Column(BIGINT(20), comment='操作时间')
    operator = Column(String(64, 'utf8mb4_0900_bin'), comment='操作人')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

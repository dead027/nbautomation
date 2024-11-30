# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemRechargeType(Base):
    __tablename__ = 'system_recharge_type'
    __table_args__ = {'comment': '充值类型配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='货币代码')
    recharge_code = Column(String(20, 'utf8mb4_0900_bin'), comment='充值类型CODE')
    recharge_type = Column(String(64, 'utf8mb4_0900_bin'), comment='充值类型')
    recharge_type_i18 = Column(String(128, 'utf8mb4_0900_bin'), comment='充值类型名称多语言')
    sort_order = Column(INTEGER(11), server_default=text("'1'"), comment='排序')
    memo = Column(String(128, 'utf8mb4_0900_bin'), comment='备注')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemCurrencyInfo(Base):
    __tablename__ = 'system_currency_info'
    __table_args__ = {'comment': '币种信息'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), unique=True, comment='货币代码')
    currency_name = Column(String(128, 'utf8mb4_0900_bin'), comment='货币名称 中文')
    currency_name_i18 = Column(String(128, 'utf8mb4_0900_bin'), comment='货币名称 多语言')
    currency_symbol = Column(String(16, 'utf8mb4_0900_bin'), comment='货币符号')
    currency_decimal = Column(String(16, 'utf8mb4_0900_bin'), comment='精度 TWO:2位小数 K:千位')
    currency_icon = Column(String(256, 'utf8mb4_0900_bin'), comment='图标')
    final_rate = Column(DECIMAL(65, 2), comment='和平台币转换汇率')
    sort_order = Column(INTEGER(11), server_default=text("'1'"), comment='排序')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='修改时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

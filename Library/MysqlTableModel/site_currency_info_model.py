# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteCurrencyInfo(Base):
    __tablename__ = 'site_currency_info'
    __table_args__ = {'comment': '站点主币种汇率转换'}

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编号')
    plat_currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='平台币种')
    plat_currency_name = Column(String(128, 'utf8mb4_0900_bin'), comment='平台币种名称')
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='货币代码')
    final_rate = Column(DECIMAL(65, 2), comment='转换后汇率')
    status = Column(INTEGER(11), comment='状态 1:生效 0:未生效')
    sort_order = Column(INTEGER(11), comment='排序')
    creator = Column(String(40, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(40, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

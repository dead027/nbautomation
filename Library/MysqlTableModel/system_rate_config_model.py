# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemRateConfig(Base):
    __tablename__ = 'system_rate_config'
    __table_args__ = {'comment': '加密货币汇率配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='货币代码')
    base_currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='主货币代码')
    show_way = Column(String(64, 'utf8mb4_0900_bin'), comment='展示方式 WITHDRAW:取款 RECHARGE:存款')
    third_rate = Column(DECIMAL(65, 8), comment='三方汇率')
    adjust_way = Column(String(255, 'utf8mb4_0900_bin'), comment='汇率调整方式')
    adjust_num = Column(String(16, 'utf8mb4_0900_bin'), comment='调整数值')
    final_rate = Column(DECIMAL(65, 8), comment='调整后最终汇率')
    status = Column(INTEGER(11), server_default=text("'0'"), comment='状态 1:生效 0:未生效')
    rate_type = Column(String(64, 'utf8mb4_0900_bin'), comment='汇率类型: ENCRYPT:加密货币 CURRENCY:主货币')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

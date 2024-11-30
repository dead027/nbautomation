# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SystemRechargeWay(Base):
    __tablename__ = 'system_recharge_way'
    __table_args__ = {'comment': '充值方式配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    currency_code = Column(String(64, 'utf8mb4_0900_bin'), comment='货币代码')
    recharge_code = Column(String(64, 'utf8mb4_0900_bin'), comment='充值类型代码')
    recharge_type = Column(String(64, 'utf8mb4_0900_bin'), comment='充值类型')
    recharge_way = Column(String(64, 'utf8mb4_0900_bin'), comment='充值方式')
    recharge_way_i18 = Column(String(128, 'utf8mb4_0900_bin'), comment='充值方式多语言')
    way_fee = Column(DECIMAL(16, 4), comment='手续费 5 代表5%')
    quick_amount = Column(String(255, 'utf8mb4_0900_bin'), comment='快捷金额 多个中间逗号分隔')
    sort_order = Column(INTEGER(11), server_default=text("'1'"), comment='排序')
    way_icon = Column(String(128, 'utf8mb4_0900_bin'), comment='图标')
    memo = Column(String(128, 'utf8mb4_0900_bin'), comment='备注')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    recommend_flag = Column(INTEGER(11), comment='是否推荐 0:未推荐 1:推荐')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

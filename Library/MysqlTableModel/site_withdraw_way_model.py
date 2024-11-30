# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteWithdrawWay(Base):
    __tablename__ = 'site_withdraw_way'
    __table_args__ = {'comment': '站点提款方式配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    withdraw_id = Column(BIGINT(20), nullable=False, comment='提款配置ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点代码')
    way_fee = Column(DECIMAL(16, 4), comment='手续费 5 代表5%')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

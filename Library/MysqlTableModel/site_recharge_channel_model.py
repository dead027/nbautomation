# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteRechargeChannel(Base):
    __tablename__ = 'site_recharge_channel'
    __table_args__ = {'comment': '站点充值通道配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    channel_id = Column(BIGINT(20), nullable=False, comment='通道配置ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点代码')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

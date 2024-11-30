# coding: utf-8
from sqlalchemy import Column, String, Text, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityFirstRecharge(Base):
    __tablename__ = 'site_activity_first_recharge'
    __table_args__ = {'comment': '首存活动规则配置信息表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    activity_id = Column(BIGINT(20), comment='所属活动id')
    discount_type = Column(INTEGER(11), nullable=False, comment='优惠方式类型，0.百分比，1.固定')
    conditional_value = Column(Text(collation='utf8mb4_0900_bin'), comment='对应的活动条件值')
    participation_mode = Column(INTEGER(11), comment='参与方式,0.手动参与，1.自动参与')
    distribution_type = Column(INTEGER(11), comment='派发方式0.过期作废，1.过期自动派发,2.立即派发')
    status = Column(INTEGER(11), server_default=text("'1'"), comment='启用状态，0.禁用，1.启用')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='修改时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

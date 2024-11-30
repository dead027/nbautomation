# coding: utf-8
from sqlalchemy import Column, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityRedBagConfig(Base):
    __tablename__ = 'site_activity_red_bag_config'
    __table_args__ = (
        Index('idx_sitecode_sort', 'site_code', 'sort', unique=True),
        {'comment': '红包雨活动配置附表'}
    )

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    vip_rank_code = Column(INTEGER(11), comment='段位code')
    red_bag_maximum = Column(String(20, 'utf8mb4_0900_bin'), comment='有效红包数量上限')
    amount_type = Column(INTEGER(11), comment='红包金额类型 1 固定金额 2 随机金额')
    sort = Column(INTEGER(11), comment='序号')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

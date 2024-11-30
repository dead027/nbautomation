# coding: utf-8
from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityFreeWheel(Base):
    __tablename__ = 'site_activity_free_wheel'
    __table_args__ = {'comment': '免费旋转活动配置表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    activity_id = Column(BIGINT(20), comment='所属活动')
    week_days = Column(String(64, 'utf8mb4_0900_bin'), comment='指定日期 周一、周二等')
    discount_type = Column(INTEGER(11), comment='优惠方式 0:阶梯次数 1:固定次数')
    participation_mode = Column(INTEGER(11), comment='参与方式 0:手动参与 1:自动参与')
    condition_val = Column(Text(collation='utf8mb4_0900_bin'), comment='匹配条件 json格式 固定次数:{min_deposit_amt,acquire_num} jsonArray格式阶梯次数:{min_deposit_amt,max_deposit_amt,acquire_num}')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

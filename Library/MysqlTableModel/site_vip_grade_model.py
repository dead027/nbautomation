# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipGrade(Base):
    __tablename__ = 'site_vip_grade'
    __table_args__ = {'comment': 'VIP等级配置(站点)'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    vip_grade_code = Column(INTEGER(11), comment='VIP等级code')
    vip_grade_name = Column(String(30, 'utf8mb4_0900_bin'), comment='VIP等级名称')
    vip_rank_code = Column(INTEGER(11), comment='VIP段位code')
    upgrade_xp = Column(DECIMAL(20, 2), comment='升级条件所需XP')
    upgrade_bonus = Column(DECIMAL(20, 2), comment='晋级礼金')
    pic_icon = Column(String(50, 'utf8mb4_0900_bin'), comment='图标地址')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

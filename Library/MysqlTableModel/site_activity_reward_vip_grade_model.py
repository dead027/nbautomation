# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityRewardVipGrade(Base):
    __tablename__ = 'site_activity_reward_vip_grade'
    __table_args__ = {'comment': 'VIP等级活动配置奖励'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    vip_grade_code = Column(INTEGER(11), comment='VIP等级code')
    vip_grade_name = Column(String(30, 'utf8mb4_0900_bin'), comment='VIP等级名称')
    vip_rank_code = Column(INTEGER(11), comment='VIP段位code')
    vip_rank_name = Column(String(30, 'utf8mb4_0900_bin'), comment='vip段位名称')
    vip_rank_name_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='段位名称-多语言')
    activity_template = Column(String(20, 'utf8mb4_0900_bin'), comment='活动模板-同system_param activity_template')
    base_id = Column(BIGINT(20), index=True, comment='活动id')
    reward_count = Column(INTEGER(11), comment='领取次数')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

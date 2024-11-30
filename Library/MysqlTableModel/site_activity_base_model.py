# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityBase(Base):
    __tablename__ = 'site_activity_base'
    __table_args__ = {'comment': '优惠活动-基本表'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    xxl_job_id = Column(BIGINT(20), comment='任务ID')
    activity_no = Column(String(10, 'utf8mb4_0900_bin'), unique=True, comment='活动编号')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点code')
    activity_name_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='活动名称-多语言')
    label_id = Column(String(20, 'utf8mb4_0900_bin'), comment='活动分类-活动分类主键')
    activity_deadline = Column(INTEGER(11), comment='活动时效-ActivityDeadLineEnum')
    activity_start_time = Column(BIGINT(20), comment='活动开始时间')
    activity_end_time = Column(BIGINT(20), comment='活动结束时间')
    show_start_time = Column(BIGINT(20), comment='活动展示开始时间')
    show_end_time = Column(BIGINT(20), comment='活动展示结束时间')
    activity_template = Column(String(20, 'utf8mb4_0900_bin'), comment='活动模板-同system_param activity_template')
    wash_ratio = Column(DECIMAL(8, 2), comment='洗码倍率')
    account_type = Column(String(5, 'utf8mb4_0900_bin'), comment='活动生效的账户类型')
    support_terminal = Column(String(20, 'utf8mb4_0900_bin'), comment='活动参与终端')
    show_terminal = Column(String(20, 'utf8mb4_0900_bin'), comment='活动展示终端')
    entrance_picture_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='入口图-移动端')
    entrance_picture_pc_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='入口图-PC端')
    head_picture_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='活动头图-移动端')
    head_picture_pc_i18n_code = Column(String(100, 'utf8mb4_0900_bin'), comment='活动头图-PC端')
    switch_phone = Column(INTEGER(11), comment='完成手机号绑定才能参与：0：关，1:开')
    switch_email = Column(INTEGER(11), comment='完成邮箱绑定才能参与：0：关，1:开')
    switch_ip = Column(INTEGER(11), comment='同登录IP只能1次：0：关，1:开')
    activity_rule_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='活动规则,多语言')
    activity_desc_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='活动描述,多语言')
    sort = Column(INTEGER(11), comment='顺序')
    status = Column(INTEGER(11), comment='状态 0已禁用 1开启中')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

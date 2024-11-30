# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteUserLabelConfigRecord(Base):
    __tablename__ = 'site_user_label_config_record'
    __table_args__ = {'comment': '会员标签配置记录'}

    id = Column(BIGINT(30), primary_key=True)
    label_name = Column(String(30, 'utf8mb4_0900_bin'), nullable=False, comment='标签名称')
    change_type = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='变更类型')
    before_change = Column(String(100, 'utf8mb4_0900_bin'), comment='变更前')
    after_change = Column(String(100, 'utf8mb4_0900_bin'), comment='变更后')
    site_user_label_config_id = Column(BIGINT(30), nullable=False, comment='会员标签ID')
    site_code = Column(String(10, 'utf8mb4_0900_bin'), comment='站点编码')
    last_operator = Column(String(30, 'utf8mb4_0900_bin'), comment='最近操作人')
    creator = Column(BIGINT(20), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(BIGINT(20), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

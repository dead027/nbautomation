# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteUserLabelConfig(Base):
    __tablename__ = 'site_user_label_config'
    __table_args__ = {'comment': '会员标签配置'}

    id = Column(BIGINT(0), primary_key=True, comment='id')
    label_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='标签ID')
    label_name = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, index=True, comment='标签名称')
    label_describe = Column(String(255, 'utf8mb4_0900_bin'), comment='标签描述')
    create_name = Column(String(30, 'utf8mb4_0900_bin'), comment='创建人')
    last_operator = Column(String(30, 'utf8mb4_0900_bin'), comment='最近操作人')
    customize_status = Column(INTEGER(1), comment='标签状态 0:非定制，1定制')
    color = Column(String(10, 'utf8mb4_0900_bin'), comment='颜色')
    site_code = Column(String(10, 'utf8mb4_0900_bin'), comment='站点编码')
    creator = Column(BIGINT(0), comment='创建人')
    created_time = Column(BIGINT(0), comment='创建时间')
    updater = Column(BIGINT(0), comment='更新人')
    updated_time = Column(BIGINT(0), comment='更新时间')
    status = Column(INTEGER(0), server_default=text("'1'"), comment='标签状态 0：停用； 1：启用')
    deleted = Column(INTEGER(0), server_default=text("'0'"), comment='删除状态 0：未删除； 2：已删除')

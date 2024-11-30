# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class DomainInfo(Base):
    __tablename__ = 'domain_info'
    __table_args__ = {'comment': '域名管理'}

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    domain_addr = Column(String(255, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='域名地址')
    side_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, server_default=text("''"), comment='使用站点')
    domain_type = Column(TINYINT(4), nullable=False, comment='域名类型;1-代理端,2-H5端,3-app端,4-后端')
    primary_domain = Column(TINYINT(4), comment='是否主域名;0-否,1-是')
    status = Column(TINYINT(4), server_default=text("'1'"), comment='状态;1-启用,2-禁用')
    bind = Column(TINYINT(4), nullable=False, server_default=text("'0'"), comment='绑定状态;0-未绑定;1-已绑定')
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注')
    creator_name = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater_name = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人名称')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

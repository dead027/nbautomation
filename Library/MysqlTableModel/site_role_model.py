# coding: utf-8
from sqlalchemy import CHAR, Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteRole(Base):
    __tablename__ = 'site_role'
    __table_args__ = {'comment': '角色信息'}

    id = Column(BIGINT(30), primary_key=True, comment='角色ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), server_default=text("''"), comment='站点code')
    name = Column(String(30, 'utf8mb4_0900_bin'), comment='角色名称')
    status = Column(CHAR(1, 'utf8mb4_0900_bin'), comment='角色状态（0正常 1停用）')
    creator = Column(BIGINT(20), comment='创建人')
    updater = Column(BIGINT(20), comment='更新人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    remark = Column(String(500, 'utf8mb4_0900_bin'), comment='备注')
    use_nums = Column(INTEGER(4), comment='使用数量')

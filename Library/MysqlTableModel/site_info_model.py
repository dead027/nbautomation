# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteInfo(Base):
    __tablename__ = 'site_info'
    __table_args__ = {'comment': '站点列表'}

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), unique=True, comment='站点编号')
    site_name = Column(String(20, 'utf8mb4_0900_bin'), comment='站点名称')
    company = Column(String(100, 'utf8mb4_0900_bin'), comment='所属公司')
    site_prefix = Column(String(20, 'utf8mb4_0900_bin'), comment='站点前缀')
    site_type = Column(TINYINT(4), comment='站点类型')
    site_model = Column(TINYINT(4), comment='站点模式')
    status = Column(TINYINT(4), comment='状态(0:禁用,1:启用)')
    commission_plan = Column(TINYINT(4), comment='抽成方案')
    bk_name = Column(String(30, 'utf8mb4_0900_bin'), comment='站点后台名称')
    skin = Column(String(20, 'utf8mb4_0900_bin'), comment='皮肤模版code')
    long_logo = Column(String(150, 'utf8mb4_0900_bin'), comment='长logo')
    short_logo = Column(String(150, 'utf8mb4_0900_bin'), comment='短logo')
    site_admin_account = Column(String(30, 'utf8mb4_0900_bin'), comment='管理员账号')
    last_step = Column(TINYINT(4), comment='最近的保存步骤')
    remark = Column(String(200, 'utf8mb4_0900_bin'), comment='备注')
    timezone = Column(String(100, 'utf8mb4_0900_bin'), comment='时区code,同system_timezone表')
    created_time = Column(BIGINT(20), comment='创建时间')
    updated_time = Column(BIGINT(20), comment='更新时间')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    plat_currency_code = Column(String(10, 'utf8mb4_0900_bin'), comment='站点平台币code')
    plat_currency_name = Column(String(50, 'utf8mb4_0900_bin'), comment='站点平台币名称')

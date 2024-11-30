# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteLoginInfo(Base):
    __tablename__ = 'site_login_info'
    __table_args__ = {'comment': '系统登录日志'}

    id = Column(BIGINT(30), primary_key=True, comment='ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), server_default=text("''"), comment='站点code')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), server_default=text("''"), comment='用户账号')
    ipaddr = Column(String(128, 'utf8mb4_0900_bin'), server_default=text("''"), comment='登录IP地址')
    login_location = Column(String(255, 'utf8mb4_0900_bin'), server_default=text("''"), comment='登录地点')
    browser = Column(String(50, 'utf8mb4_0900_bin'), server_default=text("''"), comment='浏览器类型')
    os = Column(String(50, 'utf8mb4_0900_bin'), server_default=text("''"), comment='操作系统')
    device_code = Column(String(50, 'utf8mb4_0900_bin'), server_default=text("''"), comment='终端设备号')
    status = Column(TINYINT(4), server_default=text("'0'"), comment='登录状态（0成功 1失败）')
    msg = Column(String(255, 'utf8mb4_0900_bin'), server_default=text("''"), comment='提示消息')
    access_time = Column(BIGINT(20), comment='访问时间')

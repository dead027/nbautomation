# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserLoginInfo(Base):
    __tablename__ = 'user_login_info'

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    user_account = Column(String(30, 'utf8mb4_0900_bin'), comment='会员账号')
    account_type = Column(INTEGER(11), comment='账号类型')
    ip = Column(String(100, 'utf8mb4_0900_bin'), comment='ip')
    ip_address = Column(String(100, 'utf8mb4_0900_bin'), comment='IP归属地')
    login_type = Column(INTEGER(11), comment='登录状态')
    login_address = Column(String(1024, 'utf8mb4_0900_bin'), comment='登录网址')
    login_terminal = Column(String(50, 'utf8mb4_0900_bin'), comment='登录终端;1-PC,2-IOS_H5,3-IOS_APP,4-Android_H5,5-Android_APP')
    login_time = Column(BIGINT(20), comment='登录时间')
    device_no = Column(String(100, 'utf8mb4_0900_bin'), comment='设备号')
    device_version = Column(String(100, 'utf8mb4_0900_bin'), comment='设备版本')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建者')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='更新者')
    updated_time = Column(BIGINT(20), comment='更新时间')

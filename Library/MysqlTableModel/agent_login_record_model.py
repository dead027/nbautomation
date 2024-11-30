# coding: utf-8
from sqlalchemy import CHAR, Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentLoginRecord(Base):
    __tablename__ = 'agent_login_record'
    __table_args__ = {'comment': '代理登录信息记录'}

    id = Column(BIGINT(30), primary_key=True, comment='主键id')
    agent_account = Column(String(50, 'utf8mb4_0900_bin'), comment='代理账号')
    agent_type = Column(CHAR(2, 'utf8mb4_0900_bin'), comment='代理类型(1:正式,2:商务,3:置换)')
    login_ip = Column(String(100, 'utf8mb4_0900_bin'), comment='登录IP')
    ip_control_id = Column(BIGINT(20), comment='ip风控层级id')
    ip_attribution = Column(String(100, 'utf8mb4_0900_bin'), comment='IP归属地')
    login_device = Column(CHAR(20, 'utf8mb4_0900_bin'), comment='登录终端(1:PC,2:IOS_H5,3:IOS_APP,4:Android_H5,5:Android_APP)')
    device_number = Column(String(100, 'utf8mb4_0900_bin'), comment='终端设备号')
    device_control_id = Column(BIGINT(20), comment='终端设备号风控层级id')
    login_address = Column(String(100, 'utf8mb4_0900_bin'), comment='登录地址')
    login_time = Column(BIGINT(20), comment='登录时间')
    device_version = Column(String(50, 'utf8mb4_0900_bin'), comment='设备版本')
    login_status = Column(CHAR(2, 'utf8mb4_0900_bin'), comment='登录状态(0:登录成功,1:登录失败)')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    site_code = Column(String(10, 'utf8mb4_0900_bin'), comment='站点编码')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

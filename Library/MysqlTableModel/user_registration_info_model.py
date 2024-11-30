# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserRegistrationInfo(Base):
    __tablename__ = 'user_registration_info'
    __table_args__ = {'comment': '用户注册信息'}

    id = Column(BIGINT(20), primary_key=True, unique=True, comment='ID')
    registration_time = Column(BIGINT(20), comment='注册时间')
    member_id = Column(String(100, 'utf8mb4_0900_bin'), comment='会员Id')
    member_account = Column(String(100, 'utf8mb4_0900_bin'), comment='注册信息')
    member_name = Column(String(45, 'utf8mb4_0900_bin'), comment='会员姓名')
    phone = Column(String(20), comment='手机号码')
    email = Column(String(50), comment='邮箱')
    main_currency = Column(String(10, 'utf8mb4_0900_bin'), comment='主货币')
    member_type = Column(String(45, 'utf8mb4_0900_bin'), comment='账号类型')
    superior_agent = Column(String(100, 'utf8mb4_0900_bin'), comment='上级代理')
    agent_id = Column(String(20), comment='代理id')
    register_ip = Column(String(100, 'utf8mb4_0900_bin'), comment=' 注册IP')
    ip_attribution = Column(String(100, 'utf8mb4_0900_bin'), comment=' IP归属地')
    terminal_device_number = Column(String(45, 'utf8mb4_0900_bin'), comment=' 终端设备号')
    register_terminal = Column(String(45, 'utf8mb4_0900_bin'), comment='注册终端')
    member_domain = Column(String(150, 'utf8mb4_0900_bin'), comment='注册域名')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

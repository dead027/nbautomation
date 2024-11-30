# coding: utf-8
from sqlalchemy import Column, String, text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SmsChannelConfig(Base):
    __tablename__ = 'sms_channel_config'
    __table_args__ = {'comment': '短信通道配置表'}

    id = Column(String(64, 'utf8mb4_0900_bin'), primary_key=True)
    address = Column(String(50, 'utf8mb4_0900_bin'), comment='使用地区')
    address_code = Column(String(20, 'utf8mb4_0900_bin'), comment='使用地区code')
    area_code = Column(String(20, 'utf8mb4_0900_bin'), comment='区号')
    channel_id = Column(String(50, 'utf8mb4_0900_bin'), comment='通道ID')
    channel_name = Column(String(50, 'utf8mb4_0900_bin'), comment='通道名称')
    channel_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, unique=True, comment='通道代码')
    auth_count = Column(INTEGER(2), server_default=text("'0'"), comment='授权数量')
    status = Column(INTEGER(2), comment='状态 0 启动 1 禁用')
    host = Column(String(100, 'utf8mb4_0900_bin'), comment='请求地址')
    user_id = Column(String(100, 'utf8mb4_0900_bin'))
    user_account = Column(String(100, 'utf8mb4_0900_bin'), comment='用户账号')
    password = Column(String(100, 'utf8mb4_0900_bin'), comment='密码')
    template = Column(String(100, 'utf8mb4_0900_bin'), comment='密码')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(20))
    updater = Column(String(50, 'utf8mb4_0900_bin'))
    updated_time = Column(BIGINT(20))

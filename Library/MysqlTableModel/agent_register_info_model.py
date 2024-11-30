# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class AgentRegisterInfo(Base):
    __tablename__ = 'agent_register_info'
    __table_args__ = {'comment': '代理注册记录表'}

    id = Column(String(64, 'utf8mb4_0900_ai_ci'), primary_key=True, comment='主键id')
    site_code = Column(String(50, 'utf8mb4_0900_ai_ci'), nullable=False, comment='站点编码')
    agent_account = Column(String(20, 'utf8mb4_0900_ai_ci'), comment='代理账号')
    agent_type = Column(String(2, 'utf8mb4_0900_ai_ci'), comment='代理类型')
    register_ip = Column(String(20, 'utf8mb4_0900_ai_ci'), comment='注册IP')
    register_ip_control_id = Column(BIGINT(20), comment='注册IP风控层级')
    ip_attribution = Column(String(20, 'utf8mb4_0900_ai_ci'), comment='IP归属地')
    register_device = Column(String(10, 'utf8mb4_0900_ai_ci'), comment='注册终端')
    device_control_id = Column(BIGINT(20), comment='终端设备风控层级')
    device_number = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='终端设备号')
    register_time = Column(BIGINT(20), comment='注册时间')
    register_domain = Column(String(255, 'utf8mb4_0900_bin'), comment='注册域名')
    created_time = Column(BIGINT(20), comment='创建时间')
    creator = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='创建人')
    updater = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')

# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteUserLabelRecord(Base):
    __tablename__ = 'site_user_label_record'

    id = Column(BIGINT(30), primary_key=True)
    before_change = Column(String(1000, 'utf8mb4_0900_bin'), comment='数据产生变化前字段的内容——变更前')
    after_change = Column(String(1000, 'utf8mb4_0900_bin'), comment='数据产生变化后字段的内容——变更后')
    member_account = Column(String(45, 'utf8mb4_0900_bin'), nullable=False, comment='注册成功后的登录账号信息——会员账号')
    account_type = Column(String(45, 'utf8mb4_0900_bin'), nullable=False, comment='对应会员账号下的属性——账号类型')
    risk_control_level = Column(String(45, 'utf8mb4_0900_bin'), comment="对应会员账号下的属性———'风控层级'")
    account_status = Column(String(45, 'utf8mb4_0900_bin'), comment="'账号状态’——对应会员账号下的属性")
    site_code = Column(String(10, 'utf8mb4_0900_bin'), comment='站点编码')
    updater = Column(String(45, 'utf8mb4_0900_bin'), nullable=False, comment="'操作人’——后台账号信息")
    updated_time = Column(BIGINT(0), comment='变更时间—信息变更的的时间区间范围\\n\\n')
    creator = Column(String(45, 'utf8mb4_0900_bin'))
    created_time = Column(BIGINT(0))
    operator = Column(String(50, 'utf8mb4_0900_bin'), comment='操作人')

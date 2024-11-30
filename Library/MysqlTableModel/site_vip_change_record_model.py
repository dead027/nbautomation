# coding: utf-8
from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import BIGINT, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteVipChangeRecord(Base):
    __tablename__ = 'site_vip_change_record'
    __table_args__ = {'comment': '站点-vip等级变更记录表'}

    id = Column(BIGINT(20), primary_key=True)
    site_code = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_id = Column(String(100, 'utf8mb4_0900_bin'), comment='会员id,备用')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), nullable=False, comment='会员账号')
    operation_type = Column(TINYINT(4), comment='操作记录类型(0:VIP段位,1:VIP等级)')
    account_type = Column(String(20, 'utf8mb4_0900_bin'), comment='账号类型')
    change_type = Column(String(10, 'utf8mb4_0900_bin'), comment='变更类型。升级降级（system_param表）')
    before_change = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='变更前vip')
    after_change = Column(String(20, 'utf8mb4_0900_bin'), nullable=False, comment='变更后vip等级')
    change_time = Column(BIGINT(20), nullable=False, comment='变更时间')
    control_rank = Column(String(30, 'utf8mb4_0900_bin'), comment='风控层级（预留）')
    user_label = Column(String(255, 'utf8mb4_0900_bin'), comment='标签id,多个id以英文逗号拼接')
    account_status = Column(String(20, 'utf8mb4_0900_bin'), comment='账号状态')
    operator = Column(String(64, 'utf8mb4_0900_bin'), comment='操作人')
    creator = Column(String(64, 'utf8mb4_0900_bin'), nullable=False, comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

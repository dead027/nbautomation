# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteTaskOrderRecord(Base):
    __tablename__ = 'site_task_order_record'
    __table_args__ = (
        Index('idx_user_account', 'user_id', 'task_id'),
        {'comment': '会员领取任务记录表'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    order_no = Column(String(128, 'utf8mb4_0900_bin'), unique=True, comment='订单号')
    task_id = Column(BIGINT(20), comment='所属活动')
    task_type = Column(String(20, 'utf8mb4_0900_bin'), comment='活动模板')
    sub_task_type = Column(String(20, 'utf8mb4_0900_bin'), comment='子任务类型')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='会员id')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='姓名')
    user_account = Column(String(64, 'utf8mb4_0900_bin'), comment='会员账号')
    super_agent_id = Column(String(20, 'utf8mb4_0900_bin'), comment='代理账号')
    vip_grade_code = Column(INTEGER(11), comment='VIP等级')
    vip_rank_code = Column(INTEGER(11), comment='vip段位code')
    distribution_type = Column(INTEGER(11), comment='派发方式 (0: 玩家自领-过期作废，1: 玩家自领-过期不作废)')
    receive_start_time = Column(BIGINT(20), comment='可领取开始时间')
    receive_end_time = Column(BIGINT(20), comment='可领取结束时间')
    receive_status = Column(INTEGER(11), index=True, comment='领取状态')
    final_rate = Column(DECIMAL(65, 2), comment='发放彩金时的汇率')
    task_amount = Column(DECIMAL(16, 2), comment='任务赠送金额')
    currency_code = Column(String(10, 'utf8mb4_0900_bin'), comment='币种')
    wash_ratio = Column(DECIMAL(15, 2), comment='流水倍数')
    running_water = Column(DECIMAL(16, 2), comment='流水要求')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    receive_time = Column(BIGINT(20), comment='领取时间')
    device_no = Column(String(80, 'utf8mb4_0900_bin'), comment='领取时用户-设备号')
    ip = Column(String(80, 'utf8mb4_0900_bin'), index=True, comment='领取时用户-ip')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

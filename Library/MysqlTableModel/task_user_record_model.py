# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TaskUserRecord(Base):
    __tablename__ = 'task_user_record'
    __table_args__ = (
        Index('idx_user_account', 'user_account', 'task_id', 'task_type'),
        {'comment': '会员任务记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    order_no = Column(String(30, 'utf8mb4_0900_bin'), index=True, comment='订单号')
    order_generate_time = Column(BIGINT(20), comment='订单生成时间')
    receive_way = Column(INTEGER(11), comment='领取方式')
    receive_time = Column(BIGINT(20), comment='领取时间')
    user_id = Column(BIGINT(20), comment='会员id')
    user_account = Column(String(20, 'utf8mb4_0900_bin'), comment='会员账号')
    agent_account = Column(String(50, 'utf8mb4_0900_bin'), comment='代理账号')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='姓名')
    task_type = Column(INTEGER(11), comment='任务类型')
    task_id = Column(BIGINT(20), comment='任务id')
    task_name = Column(String(50, 'utf8mb4_0900_bin'), comment='任务名称')
    complex_id = Column(BIGINT(20), comment='场馆id/支付方式id')
    complex_name = Column(String(30, 'utf8mb4_0900_bin'), comment='场馆名称/支付方式')
    bet_valid_amount = Column(DECIMAL(15, 2), comment='有效投注')
    award_amount = Column(DECIMAL(20, 2), comment='奖励金额')
    running_water_multiple = Column(DECIMAL(20, 2), comment='流水倍数')
    running_water = Column(DECIMAL(20, 2), comment='流水要求')
    receive_status = Column(INTEGER(11), index=True, comment='领取状态')
    dispatcher = Column(String(50, 'utf8mb4_0900_bin'), comment='派发人')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    creator = Column(BIGINT(20))
    updater = Column(BIGINT(20))
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    device_no = Column(String(80, 'utf8mb4_0900_bin'), comment='设备号')
    ip = Column(String(80, 'utf8mb4_0900_bin'), index=True, comment='ip')
    reward_details = Column(String(255, 'utf8mb4_0900_bin'), comment='奖励详细信息')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')

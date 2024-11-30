# coding: utf-8
from sqlalchemy import Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class SiteActivityOrderRecord(Base):
    __tablename__ = 'site_activity_order_record'
    __table_args__ = (
        Index('idx_user_account', 'user_id', 'activity_id'),
        {'comment': '会员活动记录'}
    )

    id = Column(BIGINT(20), primary_key=True, comment='主键id')
    activity_name_i18n_code = Column(String(50, 'utf8mb4_0900_bin'), comment='活动名称-多语言')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点编码')
    order_no = Column(String(128, 'utf8mb4_0900_bin'), unique=True, comment='订单号')
    activity_id = Column(BIGINT(20), comment='所属活动')
    activity_template = Column(String(20, 'utf8mb4_0900_bin'), comment='活动模板')
    activity_no = Column(String(64, 'utf8mb4_0900_bin'), comment='活动编号')
    user_id = Column(String(10, 'utf8mb4_0900_bin'), nullable=False, comment='会员id')
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='姓名')
    user_account = Column(String(64, 'utf8mb4_0900_bin'), comment='会员账号')
    account_type = Column(String(5, 'utf8mb4_0900_bin'), comment='账号类型 1-测试 2-正式')
    super_agent_id = Column(String(20, 'utf8mb4_0900_bin'), comment='代理账号')
    vip_grade_code = Column(INTEGER(11), comment='VIP等级')
    vip_rank_code = Column(INTEGER(11), comment='vip段位code')
    distribution_type = Column(INTEGER(11), comment='派发方式: 0:玩家自领-过期作废，1:玩家自领-过期自动派发，2:立即派发')
    receive_start_time = Column(BIGINT(20), comment='可领取开始时间')
    receive_end_time = Column(BIGINT(20), comment='可领取结束时间')
    receive_status = Column(INTEGER(11), index=True, comment='领取状态')
    final_rate = Column(DECIMAL(65, 2), comment='发放礼金时的汇率')
    activity_amount = Column(DECIMAL(15, 2), comment='活动赠送金额')
    plat_activity_amount = Column(DECIMAL(15, 2), comment='赠送金额-转成平台币金额-用于报表')
    currency_code = Column(String(10, 'utf8mb4_0900_bin'), comment='币种')
    principal_amount = Column(DECIMAL(12, 2), comment='本金')
    running_water_multiple = Column(DECIMAL(15, 2), comment='流水倍数')
    running_water = Column(DECIMAL(15, 2), comment='流水要求')
    remark = Column(String(255, 'utf8mb4_0900_bin'), comment='备注')
    receive_time = Column(BIGINT(20), comment='领取时间')
    device_no = Column(String(80, 'utf8mb4_0900_bin'), comment='领取时用户-设备号')
    ip = Column(String(80, 'utf8mb4_0900_bin'), index=True, comment='领取时用户-ip')
    redbag_session_id = Column(String(30, 'utf8mb4_0900_bin'), comment='红包雨场次id')
    reward_rank = Column(INTEGER(11), comment='奖品vip段位')
    prize_type = Column(String(30, 'utf8mb4_0900_bin'), comment='奖品类型')
    prize_name = Column(String(50, 'utf8mb4_0900_bin'), comment='奖品名称')
    created_time = Column(BIGINT(20))
    updated_time = Column(BIGINT(20))
    creator = Column(String(50, 'utf8mb4_0900_bin'))
    updater = Column(String(50, 'utf8mb4_0900_bin'))

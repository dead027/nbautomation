# coding: utf-8
from sqlalchemy import Column, DECIMAL, String, Text
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MedalAcquireRecord(Base):
    __tablename__ = 'medal_acquire_record'
    __table_args__ = {'comment': '勋章获取记录'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    order_no = Column(String(64, 'utf8mb4_0900_bin'), comment='订单号')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点代码')
    user_id = Column(String(20, 'utf8mb4_0900_bin'), comment='会员ID')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), comment='会员ID')
    medal_id = Column(BIGINT(20), comment='勋章编号')
    medal_code = Column(String(16, 'utf8mb4_0900_bin'), comment='勋章编码')
    medal_name = Column(String(64, 'utf8mb4_0900_bin'), comment='勋章名称')
    complete_time = Column(BIGINT(20), comment='达成条件时间')
    unlock_time = Column(BIGINT(20), comment='解锁时间')
    reward_amount = Column(DECIMAL(20, 4), comment='奖励金额')
    typing_multiple = Column(DECIMAL(20, 4), comment='打码倍数')
    cond_num1 = Column(String(128, 'utf8mb4_0900_bin'), comment='达成条件1 N')
    cond_num2 = Column(String(128, 'utf8mb4_0900_bin'), comment='达成条件2 N')
    lock_status = Column(INTEGER(11), comment='解锁状态 0:可点亮 1:已点亮')
    medal_desc = Column(Text(collation='utf8mb4_0900_bin'), comment='解锁条件说明')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MedalRewardRecord(Base):
    __tablename__ = 'medal_reward_record'
    __table_args__ = {'comment': '勋章奖励获取记录'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    order_no = Column(String(64, 'utf8mb4_0900_bin'), comment='订单号')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点代码')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), comment='会员账号')
    complete_time = Column(BIGINT(20), comment='达成条件时间')
    open_time = Column(BIGINT(20), comment='打开时间')
    reward_amount = Column(DECIMAL(20, 4), comment='奖励金额')
    typing_multiple = Column(DECIMAL(20, 4), comment='打码倍数')
    cond_num = Column(INTEGER(11), comment='达成数量')
    open_status = Column(INTEGER(11), comment='解锁状态 0:可打开 1:已打开')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

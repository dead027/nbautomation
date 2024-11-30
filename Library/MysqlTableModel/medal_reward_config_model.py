# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MedalRewardConfig(Base):
    __tablename__ = 'medal_reward_config'
    __table_args__ = {'comment': '勋章数量奖励配置'}

    id = Column(BIGINT(20), primary_key=True, comment='主键ID')
    site_code = Column(String(20, 'utf8mb4_0900_bin'), comment='站点代码 -1代表总站 默认值')
    unlock_medal_num = Column(INTEGER(11), comment='解锁勋章数')
    reward_amount = Column(DECIMAL(20, 2), comment='奖励金额')
    typing_multiple = Column(DECIMAL(20, 2), comment='打码倍数')
    status = Column(INTEGER(11), comment='状态 0:禁用 1:启用')
    creator = Column(String(64, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), comment='创建时间')
    updater = Column(String(64, 'utf8mb4_0900_bin'), comment='修改人')
    updated_time = Column(BIGINT(20), comment='修改时间')

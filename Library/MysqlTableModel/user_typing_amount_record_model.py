# coding: utf-8
from sqlalchemy import Column, DECIMAL, String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserTypingAmountRecord(Base):
    __tablename__ = 'user_typing_amount_record'
    __table_args__ = {'comment': '会员打码量-会员调整记录'}

    id = Column(BIGINT(20), primary_key=True, comment='ID')
    order_no = Column(String(50, 'utf8mb4_0900_ai_ci'), unique=True, comment='订单号')
    user_account = Column(String(50, 'utf8mb4_0900_ai_ci'), index=True, comment='会员ID')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), nullable=False, comment='站点code')
    user_register = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='会员注册信息')
    vip_rank_code = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='VIP等级')
    vip_rank_code_name = Column(String(50, 'utf8mb4_0900_ai_ci'), comment='VIP等级名称')
    adjust_way = Column(String(2, 'utf8mb4_0900_ai_ci'), comment='调整方式 1增加 2扣除')
    adjust_type = Column(String(2, 'utf8mb4_0900_ai_ci'), comment='调整类型 1人工增加流水 2人工清除流水 3系统自动清除 4投注扣减流水 5活动增加流水 6充值添加流水 7返水添加流水 8VIP奖励添加流水')
    coin_from = Column(DECIMAL(20, 2), comment='调整前流水')
    coin_value = Column(DECIMAL(20, 2), comment='调整流水')
    coin_to = Column(DECIMAL(20, 2), comment='调整后流水')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    remark = Column(String(255, 'utf8mb4_0900_ai_ci'), comment='备注')

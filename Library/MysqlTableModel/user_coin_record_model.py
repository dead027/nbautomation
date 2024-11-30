# coding: utf-8
from sqlalchemy import CHAR, Column, DECIMAL, Index, String
from sqlalchemy.dialects.mysql import BIGINT, CHAR, INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class UserCoinRecord(Base):
    __tablename__ = 'user_coin_record'
    __table_args__ = (
        Index('idx_coin_type', 'business_coin_type', 'coin_type', 'customer_coin_type', 'balance_type'),
        {'comment': '用户账变记录表'}
    )

    id = Column(BIGINT(20), primary_key=True)
    user_name = Column(String(50, 'utf8mb4_0900_bin'), comment='用户名称')
    user_account = Column(String(100, 'utf8mb4_0900_bin'), index=True, comment='会员账号')
    user_register = Column(String(100, 'utf8mb4_0900_bin'), index=True, comment='会员注册信息')
    account_status = Column(String(10, 'utf8mb4_0900_bin'), comment='账号状态')
    account_status_name = Column(String(50, 'utf8mb4_0900_bin'), comment='账号状态名称')
    risk_control_level_id = Column(BIGINT(20), comment='风控层级ID')
    risk_control_level = Column(String(50, 'utf8mb4_0900_bin'), comment='风控级别')
    vip_rank = Column(INTEGER(11), comment='VIP等级')
    agent_id = Column(BIGINT(20), comment='代理ID')
    agent_name = Column(String(100, 'utf8mb4_0900_bin'), comment='代理名称')
    wallet_type = Column(String(1), comment='钱包类型 1 中心钱包')
    currency = Column(String(50, 'utf8mb4_0900_bin'), comment='币种')
    order_no = Column(String(50, 'utf8mb4_0900_bin'), index=True, comment='关联订单号')
    business_coin_type = Column(String(2, 'utf8mb4_0900_bin'), comment='账变业务类型 1 会员存款 2 会员取款 3 会员VIP优惠 4 会员活动 5 投注 6 派彩 7 会员返水 8 VIP权益 9 其他调整  10 派彩取消 11 投注并派彩 12 代客充值')
    coin_type = Column(String(2, 'utf8mb4_0900_bin'), comment='账变类型 1会员存款 2会员存款（后台）3会员提款 4提款失败 5会员提款(后台) 6 会员VIP优惠 7 会员VIP优惠增加调整 8会员VIP优惠扣除调整  9 活动优惠 10 活动优惠增加金额 11 活动优惠扣除金额 12 投注 13派彩 14其他增加调整 15 其他扣除调整 16返水增加金额 17 返水扣除金额 18VIP权益 19重算派彩 20派彩取消 21投注并派彩 22代理代存')
    customer_coin_type = Column(String(2, 'utf8mb4_0900_bin'), comment='客户端账变类型')
    balance_type = Column(String(1, 'utf8mb4_0900_bin'), comment='收支类型1收入,2支出 3冻结 4 解冻')
    coin_value = Column(DECIMAL(20, 2), comment='金额改变数量')
    coin_from = Column(DECIMAL(20, 2), comment='账变前金额')
    coin_to = Column(DECIMAL(20, 2), comment='账变后金额')
    coin_amount = Column(DECIMAL(20, 2), comment='当前金额')
    remark = Column(String(500, 'utf8mb4_0900_bin'), comment='备注')
    creator = Column(String(50, 'utf8mb4_0900_bin'), comment='创建人')
    created_time = Column(BIGINT(20), index=True, comment='创建时间')
    updater = Column(String(50, 'utf8mb4_0900_bin'), comment='更新人')
    updated_time = Column(BIGINT(20), comment='更新时间')
    site_code = Column(String(50, 'utf8mb4_0900_bin'), comment='站点code')
